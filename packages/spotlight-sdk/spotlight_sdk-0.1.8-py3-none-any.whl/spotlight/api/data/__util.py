from typing import Optional, Set

from spotlight.api.data.model import TimeseriesQueryRequest, DistinctQueryRequest
from spotlight.core.common.enum import AssetClass, Repository


def _query_timeseries_request_info(request: TimeseriesQueryRequest) -> dict:
    return {"endpoint": f"data/v1.1/timeseries", "json": request.request_dict()}


def _query_dataset_csv_request_info(id: str, request: TimeseriesQueryRequest) -> dict:
    return {"endpoint": f"data/v1.1/{id}.csv", "json": request.request_dict()}


def _query_distinct_fields_request_info(
    request: DistinctQueryRequest, use_cache: Optional[bool] = None
) -> dict:
    return {
        "endpoint": f"data/v1.1/distinct",
        "json": request.request_dict(),
        "params": {"cache": str(use_cache)},
    }


def _sdr_health_request_info() -> dict:
    return {"endpoint": f"data/v1.1/sdr/health"}


def _sdr_count_request_info(
    start: Optional[int] = None,
    end: Optional[int] = None,
    repository: Optional[set[Repository]] = None,
    asset_class: Optional[set[AssetClass]] = None,
    distinct: Optional[bool] = None,
) -> dict:
    endpoint = "data/v1.1/sdr/count"
    params = {
        "start": start,
        "end": end,
        "repository": repository,
        "asset_class": asset_class,
        "distinct": distinct,
    }

    filtered_params = {k: v for k, v in params.items() if v is not None}

    return {"endpoint": endpoint, "params": filtered_params}
