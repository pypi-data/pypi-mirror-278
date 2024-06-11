from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

import lqs.interface.pjm.models as models
from lqs.interface.pjm.models import ProcessState


class CreateInterface(ABC):
    @abstractmethod
    def _event(self, **kwargs) -> models.EventDataResponse:
        pass

    def event(
        self,
        current_state: str,
        process_type: str,
        resource_id: UUID,
        previous_state: Optional[str] = None,
        workflow_id: Optional[UUID] = None,
        hook_id: Optional[UUID] = None,
        datastore_id: Optional[UUID] = None,
        datastore_endpoint: Optional[str] = None,
    ):
        return self._event(
            current_state=current_state,
            process_type=process_type,
            resource_id=resource_id,
            previous_state=previous_state,
            workflow_id=workflow_id,
            hook_id=hook_id,
            datastore_id=datastore_id,
            datastore_endpoint=datastore_endpoint,
        )

    def _event_by_model(self, data: models.EventCreateRequest):
        return self.event(**data.model_dump())

    @abstractmethod
    def _inference(self, **kwargs) -> models.InferenceDataResponse:
        pass

    def inference(
        self,
        datastore_id: UUID,
        topic_id: UUID,
        timestamp: int,
        pipeline_task: str,
        pipeline_model: Optional[str] = None,
        pipeline_revision: Optional[str] = None,
        max_image_size: Optional[int] = None,
        omit_output_fields: Optional[list[str]] = None,
    ):
        return self._inference(
            datastore_id=datastore_id,
            topic_id=topic_id,
            timestamp=timestamp,
            pipeline_task=pipeline_task,
            pipeline_model=pipeline_model,
            pipeline_revision=pipeline_revision,
            max_image_size=max_image_size,
            omit_output_fields=omit_output_fields,
        )

    def _inference_by_model(self, data: models.InferenceCreateRequest):
        return self.inference(**data.model_dump())

    @abstractmethod
    def _job(self, **kwargs) -> models.JobDataResponse:
        pass

    def job(
        self,
        type: str,
        process_type: str,
        resource_id: UUID,
        event_id: Optional[UUID] = None,
        datastore_id: Optional[UUID] = None,
        datastore_endpoint: Optional[str] = None,
        state: ProcessState = ProcessState.ready,
    ):
        return self._job(
            type=type,
            process_type=process_type,
            resource_id=resource_id,
            event_id=event_id,
            datastore_id=datastore_id,
            datastore_endpoint=datastore_endpoint,
            state=state,
        )

    def _job_by_model(self, data: models.JobCreateRequest):
        return self.job(**data.model_dump())
