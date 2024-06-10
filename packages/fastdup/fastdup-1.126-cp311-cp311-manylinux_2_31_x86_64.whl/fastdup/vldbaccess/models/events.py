from datetime import datetime
from typing import Optional, List
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, root_validator

from fastdup.vl.utils.annotation_utils import AnnotatedBoundingBox


class Severity(str, Enum):
    OK = 'OK'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class Event(BaseModel):
    serial: int = -1
    dataset_id: UUID
    timestamp: datetime = datetime.now()
    event_type: str = ''
    severity: Severity = Severity.OK

    @root_validator(pre=True)
    def set_event_type(cls, values):
        values['event_type'] = cls.__name__
        return values


class InvalidInput(Event):
    reason: Optional[str] = None
    severity: Severity = Severity.WARNING


class ServerFailure(Event):
    error_reference_id: UUID
    reason: Optional[str] = None
    severity: Severity = Severity.ERROR


class DatasetInitialized(Event):
    dataset_id: UUID
    dataset_name: str


class DatasetInitializationFailed(ServerFailure):
    pass


class S3Event(Event):
    s3_url: str


class FileEvent(Event):
    file_name: str


class S3InvalidURL(InvalidInput, S3Event):
    pass


class S3ValidURL(S3Event):
    pass


class S3NoAccess(InvalidInput, S3Event):
    pass


class S3Error(ServerFailure, S3Event):
    pass


class S3Connected(S3Event):
    pass


class S3FileDownloaded(FileEvent, S3Event):
    pass


class S3MediaPreview(FileEvent, S3Event):
    thumbnail: str
    scale_factor: float
    image_annotations: Optional[List[str]] = None
    object_annotations: Optional[List[AnnotatedBoundingBox]] = None


class S3NoPreview(InvalidInput, FileEvent, S3Event):
    pass


class FileUploaded(FileEvent):
    pass


class FileMediaPreview(FileEvent):
    thumbnail: str
    annotations: Optional[str] = None


class FileNoPreview(FileEvent):
    pass


class PreviewReady(Event):
    pass


class AnnotationsValid(FileEvent):
    pass


class AnnotationsInvalid(InvalidInput, FileEvent):
    pass


class AnnotatedPreview(Event):
    pass


class DatasetStatus(Event):
    status: str
    progress: int
