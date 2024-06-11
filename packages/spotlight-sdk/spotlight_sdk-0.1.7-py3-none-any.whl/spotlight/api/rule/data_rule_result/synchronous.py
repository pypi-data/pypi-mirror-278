from typing import Dict, Any, List, Optional

from spotlight.api.rule.data_rule_result.__util import (
    _get_data_rule_result_request_info,
    _get_data_rule_results_request_info,
)
from spotlight.core.common.decorators import data_request
from spotlight.core.common.requests import (
    __get_request,
)


@data_request()
def get_data_rule_result(id: str) -> Dict[str, Any]:
    """
    Get data rule result by ID.

    Args:
        id (str): Data rule result ID

    Returns:
        Dict[str, Any]: Data rule result responses
    """
    request_info = _get_data_rule_result_request_info(id)
    return __get_request(**request_info)


@data_request()
def get_data_rule_results(
    data_rule_id: Optional[str] = None,
    start: Optional[int] = None,
    end: Optional[int] = None,
    override_find_all: Optional[bool] = False,
) -> List[Dict[str, Any]]:
    """
    Retrieves a list of data rule results. If a `data_rule_id` is provided, it returns results specific to that data rule.
    Results can also be filtered by a time range, specified by `start` and `end` timestamps.

    Args:
        data_rule_id (Optional[str]): The ID of the specific data rule to get results for. If None, results for all data rules are returned.
        start (Optional[int]): The start of the time range as a Unix timestamp. If provided without `end`, fetches results from this timestamp onward.
        end (Optional[int]): The end of the time range as a Unix timestamp. If provided without `start`, fetches results up to this timestamp.
        override_find_all (Optional[bool]): If True, overrides the default limitation to fetch all results. This parameter is restricted to admin use only. Non-admin users will receive a 'Forbidden' exception if they attempt to use it. Defaults to False.

    Returns:
        List[Dict[str, Any]]: A list of data rule result responses.
    """
    request_info = _get_data_rule_results_request_info(
        data_rule_id, start, end, override_find_all
    )
    return __get_request(**request_info)
