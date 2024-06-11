"""Entry module to Dataverse Python client."""

from collections.abc import Iterator
import csv
from http import HTTPStatus
from io import StringIO
import os
from types import TracebackType
from typing import Any
from urllib.parse import urljoin
import uuid

import pandas as pd
import requests
from requests.models import PreparedRequest

from dtvr import __version__
from dtvr.timeutil import DateLike, norm_date, norm_datetime


CEPS_AREA_DOMAIN: str = "10YCZ-CEPS-----N"
CEPS: int = 1

CSV_DELIMITER: str = ";"
DEFAULT_DATE_FMT: str = "%Y-%m-%d"
DEFAULT_DATETIME_FMT: str = "%Y-%m-%d %H:%M:%S"

USER_AGENT: str = f"dtvr/{__version__}"


class ClientResponse:
    """
    Represents an HTTP response from Dataverse and contains methods to consume it either as iterator
    over CSV rows or read into pandas dataframe.
    """

    def __init__(self, req_id: str, resp: requests.Response):
        self._req_id = req_id
        self._resp = resp

    def __enter__(self) -> "ClientResponse":
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        self._resp.close()

    @property
    def success(self) -> bool:
        """Return True if the request was successful (HTTP status 200 OK); otherwise False."""
        return self._resp.status_code == 200

    def as_csv_rows(self, skip_first: bool = False, raise_on_error: bool = False, **kwargs: Any) -> Iterator[list]:
        """
        Return iterator of CSV rows. Row is a list of strings and numbers.

        :param skip_first: If true, skips first CSV row which is headers.
        :param raise_on_error: Throws exception when HTTP response is not 200 OK; otherwise return empty iterator.
        :param kwargs: Optional arguments for csv.reader.
        :return: iterator of CSV rows (represented as list of strings and numbers)
        """
        if not self.success:
            if raise_on_error:
                status = HTTPStatus(self._resp.status_code)
                raise ValueError(
                    f"Dataverse request for {self._req_id} "
                    + f"was not successful ({self._resp.status_code} {status.phrase})."
                )
            return iter(())

        lines = (line.decode("utf-8") for line in self._resp.iter_lines())
        if skip_first:
            next(lines)

        return csv.reader(lines, delimiter=CSV_DELIMITER, **kwargs)

    def as_pandas(self, try_optimize: bool = True, **kwargs: Any) -> pd.DataFrame:
        """
        Return pandas DataFrame created from Dataverse HTTP response.

        :param try_optimize: Use hints for creation of pandas dataframe if they are available.
        Hints indicate which columns should be categorized, parsed as dates, numbers, etc.
        """
        if not self.success:
            status = HTTPStatus(self._resp.status_code)
            raise ValueError(
                f"Dataverse request for {self._req_id} "
                + f"was not successful ({self._resp.status_code} {status.phrase})."
            )
        optimizations = _Endpoints.get_pandas_optimization(self._req_id) if try_optimize else {}
        buf = StringIO(self._resp.text)
        return pd.read_csv(buf, sep=CSV_DELIMITER, **optimizations, **kwargs)

    def debug(self) -> str:
        """Return debugging string with details about HTTP request and response."""
        lines = []
        req = self._resp.request
        lines.append(f"Request GET {req.url}")
        for k, v in req.headers.items():
            if "Authorization" not in k:
                lines.append(f"{k}: {v}")
        lines.append("")
        lines.append(f"Response {self._resp.status_code}")
        for k, v in self._resp.headers.items():
            lines.append(f"{k}: {v}")
        lines.append("")
        lines.append(self._resp.text)
        return "\n".join(lines)


class DataverseClient:
    """Makes queries to the Dataverse API."""

    def __init__(self, base_url: str, token: str):
        if not (base_url and base_url.startswith("https://")):
            raise ValueError("Not a valid base URL.")
        if 0 == len(token) > 50:
            raise ValueError("Token length must be within (0, 50>.")
        self._base_url = base_url
        self._token = token
        self._connect_timeout: float = 3
        self._read_timeout: float = 30

    @property
    def connect_timeout(self) -> float:
        """Connection timout in seconds."""
        return self._connect_timeout

    @connect_timeout.setter
    def connect_timeout(self, value: float) -> None:
        self._connect_timeout = value

    @property
    def read_timeout(self) -> float:
        """Read timout in seconds."""
        return self._read_timeout

    @read_timeout.setter
    def read_timeout(self, value: float) -> None:
        self._read_timeout = value

    def last_exchange_rates(self) -> ClientResponse:
        """Get last known exchange rates. Data source is CNB and rates are calculated to CZK."""
        return self._query(None, _Endpoints.last_exchange_rates, None)

    def balancing_energy_bid(self, connecting_domain: str, start: DateLike, end: DateLike) -> ClientResponse:
        """
        Get ENTSOE balancing energy bid data for the specified connecting domain and time interval.
        Data are enriched with trading day, quarter index and ENTSOE AXX and BXX codes are translated to its names.
        Max interval range is 31 days.

        :param connecting_domain: TSO area domain identification. For example: "10YCZ-CEPS-----N" for CEPS.
        :param start: TSO local date, datetime or string representing start of the date range.
        :param end: TSO local date, datetime or string representing end of the date range.
        """
        start_dt = norm_datetime(start)
        end_dt = norm_datetime(end)
        url_params = {
            "connectingDomain": connecting_domain,
            "intervalStart": start_dt.strftime(DEFAULT_DATETIME_FMT),
            "intervalEnd": end_dt.strftime(DEFAULT_DATETIME_FMT),
        }
        return self._query(None, _Endpoints.balancing_energy_bid, url_params)

    def procured_balancing_capacity_daily(self, area_domain: str, start: DateLike, end: DateLike) -> ClientResponse:
        """
        Get ENTSOE daily (from daily auction) procured balancing capacity data for the specified area domain and time interval.
        Daily means AgreementType == "A01". Data are enriched with matching id, date time local and ENTSOE AXX
        and BXX codes are translated to its names. Matching id connects same lines in the same offer.
        Date time local is the local time increased by the position in the offer. Max interval range is 31 days.

        :param area_domain: TSO area domain identification. For example: "10YCZ-CEPS-----N" for CEPS.
        :param start: TSO local date, datetime or string representing start of the date range.
        :param end: TSO local date, datetime or string representing end of the date range.
        """
        start_dt = norm_datetime(start)
        end_dt = norm_datetime(end)
        url_params = {
            "areaDomain": area_domain,
            "intervalStart": start_dt.strftime(DEFAULT_DATETIME_FMT),
            "intervalEnd": end_dt.strftime(DEFAULT_DATETIME_FMT),
        }
        return self._query(None, _Endpoints.procured_balancing_capacity_daily, url_params)

    def procured_balancing_capacity_yearly(self, area_domain: str, year: int) -> ClientResponse:
        """
        Get ENTSOE yearly (from yearly auction) procured balancing capacity data for the specified area domain and year group by weeks offers.
        Yearly means AgreementType == "A04".
        Data are enriched with matching id, week number and ENTSOE AXX and BXX codes are translated to its names.
        Matching id connects same lines in the same offer.

        :param area_domain: TSO area domain identification. For example: "10YCZ-CEPS-----N" for CEPS.
        :param year: the year
        """
        url_params = {
            "areaDomain": area_domain,
            "year": year,
        }
        return self._query(None, _Endpoints.procured_balancing_capacity_yearly, url_params)

    def exchanged_volume(self, day: DateLike) -> ClientResponse:
        """
        Get TransnetBW exchanged volumes data for the day.

        :param day: TSO local date, datetime or string representing a date.
        """
        day_d = norm_date(day)
        url_params = {"day": day_d.strftime(DEFAULT_DATE_FMT)}
        return self._query(None, _Endpoints.exchanged_volume, url_params)

    def cross_border_marginal_price(self, day: DateLike) -> ClientResponse:
        """
        Get TransnetBW cross border marginal prices data for the day.

        :param day: TSO local date, datetime or string representing a date.
        """
        day_d = norm_date(day)
        url_params = {"day": day_d.strftime(DEFAULT_DATE_FMT)}
        return self._query(None, _Endpoints.cross_border_marginal_price, url_params)

    def ceps_current_system_imbalance_actual(self) -> ClientResponse:
        """Get last ~15 minutes of CEPS current system imbalance data. Minute averages."""
        return self._query(None, _Endpoints.ceps_current_system_imbalance_actual, None)

    def ceps_current_system_imbalance_daily(self, day: DateLike) -> ClientResponse:
        """
        Get CEPS current system imbalance data for specific day. Minute averages.

        :param day: TSO local date, datetime or string representing a date.
        """
        day_d = norm_date(day)
        url_params = {"day": day_d.strftime(DEFAULT_DATE_FMT)}
        return self._query(None, _Endpoints.ceps_current_system_imbalance_daily, url_params)

    def ceps_svr_activations_actual(self) -> ClientResponse:
        """Get last ~15 minutes of CEPS svr activations data. Minute averages."""
        return self._query(None, _Endpoints.ceps_svr_activations_actual, None)

    def ceps_svr_activations_daily(self, day: DateLike) -> ClientResponse:
        """
        Get CEPS svr activations data for specific day. Minute averages.

        :param day: TSO local date, datetime or string representing a date.
        """
        day_d = norm_date(day)
        url_params = {"day": day_d.strftime(DEFAULT_DATE_FMT)}
        return self._query(None, _Endpoints.ceps_svr_activations_daily, url_params)

    def ceps_svr_export_import_actual(self) -> ClientResponse:
        """Get last ~15 minutes of CEPS svr export import data. Minute averages."""
        return self._query(None, _Endpoints.ceps_svr_export_import_actual, None)

    def ceps_svr_export_import_daily(self, day: DateLike) -> ClientResponse:
        """
        Get CEPS svr export import data for specific day. Minute averages.

        :param day: TSO local date, datetime or string representing a date.
        """
        day_d = norm_date(day)
        url_params = {"day": day_d.strftime(DEFAULT_DATE_FMT)}
        return self._query(None, _Endpoints.ceps_svr_export_import_daily, url_params)

    def ceps_svr_maximum_dt_price(self, day: DateLike) -> ClientResponse:
        """
        Get CEPS svr maximum dt price for specific day.

        :param day: TSO local date, datetime or string representing a date.
        """
        day_d = norm_date(day)
        url_params = {"day": day_d.strftime(DEFAULT_DATE_FMT)}
        return self._query(None, _Endpoints.ceps_svr_maximum_dt_price, url_params)

    def ceps_cross_border_power_flows_actual(self) -> ClientResponse:
        """Get last ~15 minutes of CEPS cross border power flows data. Minute averages."""
        return self._query(None, _Endpoints.ceps_cross_border_power_flows_actual, None)

    def ceps_cross_border_power_flows_daily(self, day: DateLike) -> ClientResponse:
        """
        Get CEPS cross border power flow data for specific day. Minute averages.

        :param day: TSO local date, datetime or string representing a date.
        """
        day_d = norm_date(day)
        url_params = {"day": day_d.strftime(DEFAULT_DATE_FMT)}
        return self._query(None, _Endpoints.ceps_cross_border_power_flows_daily, url_params)

    def ceps_emergency_exchange(self, day: DateLike) -> ClientResponse:
        """
        Get CEPS emergency exhange data for specific day. Quarter-hour averages.

        :param day: TSO local date, datetime or string representing a date.
        """
        day_d = norm_date(day)
        url_params = {"day": day_d.strftime(DEFAULT_DATE_FMT)}
        return self._query(None, _Endpoints.ceps_emergency_exchange, url_params)

    def ceps_generation_plan(self, day: DateLike) -> ClientResponse:
        """
        Get CEPS generation plan data for specific day. Hour averages.

        :param day: TSO local date, datetime or string representing a date.
        """
        day_d = norm_date(day)
        url_params = {"day": day_d.strftime(DEFAULT_DATE_FMT)}
        return self._query(None, _Endpoints.ceps_generation_plan, url_params)

    def ceps_generation_renewable_source_actual(self) -> ClientResponse:
        """Get last ~15 minutes of CEPS generation renewable source data. Minute averages."""
        return self._query(None, _Endpoints.ceps_generation_renewable_source_actual, None)

    def ceps_generation_renewable_source_daily(self, day: DateLike) -> ClientResponse:
        """
        Get CEPS generation renewable source data for specific day. Minute averages.

        :param day: TSO local date, datetime or string representing a date.
        """
        day_d = norm_date(day)
        url_params = {"day": day_d.strftime(DEFAULT_DATE_FMT)}
        return self._query(None, _Endpoints.ceps_generation_renewable_source_daily, url_params)

    def ceps_imbalance_price_prediction(self, day: DateLike) -> ClientResponse:
        """
        Get CEPS imbalance price prediction data for specific day. Hour data.

        :param day: TSO local date, datetime or string representing a date.
        """
        day_d = norm_date(day)
        url_params = {"day": day_d.strftime(DEFAULT_DATE_FMT)}
        return self._query(None, _Endpoints.ceps_imbalance_price_prediction, url_params)

    def ceps_power_balance(self, year: int) -> ClientResponse:
        """
        Get CEPS power balance data for specific year. Max values.

        :param year: the year
        """
        url_params = {"year": year}
        return self._query(None, _Endpoints.ceps_power_balance, url_params)

    def _query(self, correlation_id: str | None, url_path: str, url_params: dict[str, Any] | None) -> ClientResponse:
        url = self._create_url(url_path, url_params)
        headers = self._create_headers(correlation_id)
        r = requests.get(url, headers=headers, stream=True, timeout=(self._read_timeout, self._connect_timeout))
        return ClientResponse(url_path, r)

    def _create_url(self, url_path: str, url_params: dict[str, Any] | None) -> str:
        url = urljoin(self._base_url, url_path)
        if url_params:
            req = PreparedRequest()
            req.prepare_url(url, params=url_params)
            url = req.url if req.url else ""
        return url

    def _create_headers(self, correlation_id: str | None) -> dict[str, str]:
        cid = correlation_id if correlation_id else uuid.uuid4().hex
        return {
            "Authorization": f"Bearer {self._token}",
            "Accept": "text/plain",
            "CorrelationId": cid,
            "User-Agent": USER_AGENT,
        }

    def __str__(self) -> str:
        return f"DataverseClient {self._base_url}"


def create_client(base_url: str | None = None, auth_token: str | None = None) -> DataverseClient:
    """Create Dataverse client from arguments and/or environment variables."""
    url = base_url if base_url else os.environ.get("DATAVERSE_BASE_URL", "")
    token = auth_token if auth_token else os.environ.get("DATAVERSE_AUTH_TOKEN", "")
    return DataverseClient(url, token)


# ruff: noqa: RUF012
class _Endpoints:
    last_exchange_rates: str = "/api/v1/exchange-rate/last"
    balancing_energy_bid: str = "/api/v1/balancing-energy-bid"
    procured_balancing_capacity_daily: str = "/api/v1/procured-balancing-capacity/daily"
    procured_balancing_capacity_yearly: str = "/api/v1/procured-balancing-capacity/yearly"
    exchanged_volume: str = "/api/v1/exchanged-volume"
    cross_border_marginal_price: str = "/api/v1/cross-border-marginal-price"
    ceps_current_system_imbalance_actual: str = "/api/v1/ceps/current-system-imbalance/actual"
    ceps_current_system_imbalance_daily: str = "/api/v1/ceps/current-system-imbalance/daily"
    ceps_svr_activations_actual: str = "/api/v1/ceps/svr-activations/actual"
    ceps_svr_activations_daily: str = "/api/v1/ceps/svr-activations/daily"
    ceps_svr_export_import_actual: str = "/api/v1/ceps/svr-export-import/actual"
    ceps_svr_export_import_daily: str = "/api/v1/ceps/svr-export-import/daily"
    ceps_svr_maximum_dt_price: str = "/api/v1/ceps/svr-maximum-dt-price"
    ceps_cross_border_power_flows_actual: str = "/api/v1/ceps/cross-border-power-flows/actual"
    ceps_cross_border_power_flows_daily: str = "/api/v1/ceps/cross-border-power-flows/daily"
    ceps_emergency_exchange: str = "/api/v1/ceps/emergency-exchange"
    ceps_generation_plan: str = "/api/v1/ceps/generation-plan"
    ceps_generation_renewable_source_actual: str = "/api/v1/ceps/generation-renewable-source/actual"
    ceps_generation_renewable_source_daily: str = "/api/v1/ceps/generation-renewable-source/daily"
    ceps_imbalance_price_prediction: str = "/api/v1/ceps/imbalance-price-prediction"
    ceps_power_balance: str = "/api/v1/ceps/power-balance"

    @staticmethod
    def get_pandas_optimization(endpoint: str) -> dict[str, Any]:
        return _Endpoints.PANDAS_OPTS.get(endpoint, {})

    # First level key is endpoint url path.
    # First level value is a dictionary that will be expanded to kwargs passed to pd.read_csv.
    PANDAS_OPTS = {
        procured_balancing_capacity_daily: {
            "dtype": {
                "ProcessType": "category",
                "AreaDomain": "category",
                "AgreementType": "category",
                "ProductType": "category",
                "PsrType": "category",
                "FlowDirection": "category",
                "Position": int,
                "Quantity": int,
                "PriceAmount": float,
            },
            "parse_dates": ["CreatedDateTimeUtc", "IntervalStartLocal", "IntervalEndLocal", "DateTimeLocal"],
            "date_format": DEFAULT_DATETIME_FMT,
        },
    }
