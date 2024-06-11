from typing import List, Optional, Tuple
from uuid import UUID

from pydantic import BaseModel

from lqs.interface.core.models.__common__ import (
     DataResponseModel,
    PaginationModel,
    ProcessModel,
    ProcessCreateRequest,
    ProcessUpdateRequest,
    optional_field,
    Int64,
)


class IngestionPartIndexEntry(BaseModel):
    topic_id: str
    data_offset: int
    data_length: int
    chunk_compression: Optional[str]
    chunk_offset: Optional[int]
    chunk_length: Optional[int]
    timestamp: Int64


# TODO: in Python 3.11, we can use Tuple[*get_type_hints(IngestionPartIndex).values()]
IngestionPartIndexTuple = Tuple[
    str, int, int, Optional[str], Optional[int], Optional[int], Int64
]


class IngestionPartIndex(BaseModel):
    ingestion_part_id: UUID
    index: Optional[List[IngestionPartIndexTuple]]


class IngestionPartIndexCreateRequest(BaseModel):
    ingestion_part_id: UUID
    index: Optional[List[IngestionPartIndexTuple]] = None


class IngestionPartIndexUpdateRequest(BaseModel):
    index: Optional[List[IngestionPartIndexTuple]] = optional_field


class IngestionPartIndexDataResponse(DataResponseModel[IngestionPartIndex]):
    pass


class IngestionPartIndexListResponse(PaginationModel[IngestionPartIndex]):
	pass


# Ingestion Part


class IngestionPart(ProcessModel["IngestionPart"]):
    sequence: int
    ingestion_id: UUID
    source: Optional[str]
    index: Optional[List[IngestionPartIndexTuple]]

    log_id: Optional[UUID] = None
    group_id: Optional[UUID] = None


class IngestionPartCreateRequest(ProcessCreateRequest):
    sequence: int
    source: Optional[str] = None
    index: Optional[List[IngestionPartIndexTuple]] = None


class IngestionPartUpdateRequest(ProcessUpdateRequest):
    sequence: int = optional_field
    source: Optional[str] = optional_field
    index: Optional[List[IngestionPartIndexTuple]] = optional_field


class IngestionPartListResponse(PaginationModel[IngestionPart]):
	pass


class IngestionPartDataResponse(DataResponseModel[IngestionPart]):
    pass
