from typing import Optional


def _get_data_rule_result_request_info(id: str) -> dict:
    return {"endpoint": f"config/data_rule_result/{id}"}


def _get_data_rule_results_request_info(
    data_rule_id: Optional[str] = None,
    start: Optional[int] = None,
    end: Optional[int] = None,
    override_find_all: Optional[bool] = False,
) -> dict:
    endpoint = "config/data_rule_result"
    params = {
        "data_rule_id": data_rule_id,
        "start": start,
        "end": end,
        "override_find_all": override_find_all,
    }

    filtered_params = {k: v for k, v in params.items() if v is not None}

    return {"endpoint": endpoint, "params": filtered_params}
