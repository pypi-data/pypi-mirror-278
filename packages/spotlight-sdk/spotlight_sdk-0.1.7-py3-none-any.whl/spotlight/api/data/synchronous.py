from typing import List, Optional, Any, Dict

from requests import Response

from spotlight.api.data.__util import (
    _query_request_info,
    _query_dataset_csv_request_info,
    _query_timeseries_request_info,
)
from spotlight.api.data.model import TimeseriesQueryRequest, QueryRequest
from spotlight.core.common.decorators import data_request
from spotlight.core.common.requests import __get_request, __post_request


@data_request
def query(request: QueryRequest, one: Optional[bool] = False) -> List[Dict[str, Any]]:
    """
    Query dataset by query request.

    Args:
        request (QueryRequest): Query request
        one (bool): Flag to determine whether to return only one record

    Returns:
        List[Dict[str, Any]]: List of records
    """
    request_info = _query_request_info(request, one)
    return __post_request(**request_info)


@data_request
def get_timeseries(
    request: TimeseriesQueryRequest, one: Optional[bool] = False
) -> List[Dict[str, Any]]:
    """
    Get timeseries dataset by timeseries query request.

    Args:
        request (TimeseriesQueryRequest): Timeseries query request
        one (Optional[bool]): Flag to determine whether to return only one record

    Returns:
        List[Dict[str, Any]]: Timeseries data
    """
    request_info = _query_timeseries_request_info(request, one)
    return __post_request(**request_info)


def query_dataset_csv(id: str, request: TimeseriesQueryRequest) -> Response:
    """
    Query dataset CSV by ID.

    Args:
        id (str): Dataset ID
        request (TimeseriesQueryRequest): Timeseries query request

    Returns:
        Response: HTTP response object
    """
    request_info = _query_dataset_csv_request_info(id, request)
    return __get_request(**request_info)
