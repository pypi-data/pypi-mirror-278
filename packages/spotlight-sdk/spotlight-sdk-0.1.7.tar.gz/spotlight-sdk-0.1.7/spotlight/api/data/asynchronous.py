from typing import List, Optional, Any, Dict

import pandas as pd
from requests import Response

from spotlight.api.data.__util import (
    _query_dataset_csv_request_info,
    _query_timeseries_request_info,
    _query_request_info,
)
from spotlight.api.data.model import TimeseriesQueryRequest, QueryRequest
from spotlight.core.common.decorators import async_data_request
from spotlight.core.common.requests import __async_get_request, __async_post_request


@async_data_request
async def async_query(
    request: QueryRequest, one: Optional[bool] = False
) -> List[Dict[str, Any]]:
    """
    Asynchronously query dataset by query request.

    Args:
        request (QueryRequest): Query request
        one (Optional[bool]): Flag to determine whether to return only one record

    Returns:
        List[Dict[str, Any]]: List of records
    """
    request_info = _query_request_info(request, one)
    return await __async_post_request(**request_info)


@async_data_request
async def async_get_timeseries(
    request: TimeseriesQueryRequest, one: Optional[bool] = False
) -> List[Dict[str, Any]]:
    """
    Asynchronously get timeseries dataset by timeseries query request.

    Args:
        request (TimeseriesQueryRequest): Timeseries query request
        one (Optional[bool]): Flag to determine whether to return only one record

    Returns:
        pd.DataFrame: Timeseries DataFrame
    """
    request_info = _query_timeseries_request_info(request, one)
    return await __async_post_request(**request_info)


async def async_query_dataset_csv(id: str, request: TimeseriesQueryRequest) -> Response:
    """
    Asynchronously query dataset CSV by ID.

    Args:
        id (str): Dataset ID
        request (TimeseriesQueryRequest): Timeseries query request

    Returns:
        Response: HTTP response object
    """
    request_info = _query_dataset_csv_request_info(id, request)
    return await __async_get_request(**request_info)
