from typing import List
from uuid import UUID

from pydantic import BaseModel

from lqs.interface.dsm.models.__common__ import (
    DataResponseModel,
    TimeSeriesModel,
    PaginationModel,
    optional_field,
    Int64
)


class UsageTick(TimeSeriesModel):
    datastore_id: UUID
    log_count: int
    record_count: int
    record_size: int
    object_count: int
    object_size: int
    transfer_size: int


class UsageTickDataResponse(DataResponseModel[UsageTick]):
    pass


class UsageTickListResponse(PaginationModel[UsageTick]):
	pass


class UsageTickCreateRequest(BaseModel):
    timestamp: Int64
    log_count: int
    record_count: int
    record_size: int
    object_count: int
    object_size: int
    transfer_size: int


class UsageTickUpdateRequest(BaseModel):
    log_count: int = optional_field
    record_count: int = optional_field
    record_size: int = optional_field
    object_count: int = optional_field
    object_size: int = optional_field
    transfer_size: int = optional_field
