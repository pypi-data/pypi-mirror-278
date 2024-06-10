from typing import Any, Dict, Generic, Literal, TypeVar, Union

import pydantic
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

from classiq.interface.helpers.custom_encoders import CUSTOM_ENCODERS

from classiq._internals.enum_utils import StrEnum

JSONObject = Dict[str, Any]
T = TypeVar("T", bound=Union[pydantic.BaseModel, JSONObject])
AUTH_HEADER = "Classiq-BE-Auth"


class JobID(BaseModel):
    job_id: str


class JobStatus(StrEnum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    READY = "READY"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"

    def is_final(self) -> bool:
        return self in (self.COMPLETED, self.FAILED, self.CANCELLED)


"""
A job can be in either of 3 states: ongoing, completed successfully or completed
unsuccessfully. Each job status belongs to one of the 3 states
The class JobDescriptionBase represents a job description, regardless of its state
JobDescriptionSuccess represents a job that was completed successfully. It contains the
job result in the description field. The type of the result depends on the route, and
so it's defined as a generic class
JobDescriptionFailure represents a job that was completed unsuccessfully. It contains
the failure details (i.e., error message) in the description field
JobDescriptionNonFinal represents a job that has not terminated yet. It does not contain
any additional information
JobDescriptionUnion is used to define a discriminator field between the 3 states. Since
JobDescriptionSuccess is generic, so is the union. This means it cannot be defined
as an annotated type alias (that is, we cannot define
JobDescriptionUnion = Annotated[Union[...], Field(discriminator="kind")])
"""

SuccessStatus = Literal[JobStatus.COMPLETED]
FailureStatus = Union[
    Literal[JobStatus.FAILED],
    Literal[JobStatus.CANCELLED],
]
NonFinalStatus = Union[
    Literal[JobStatus.QUEUED],
    Literal[JobStatus.RUNNING],
    Literal[JobStatus.READY],
    Literal[JobStatus.CANCELLING],
    Literal[JobStatus.UNKNOWN],
]


class FailureDetails(BaseModel):
    details: str


class JobDescriptionBase(GenericModel, Generic[T], json_encoders=CUSTOM_ENCODERS):
    kind: str
    status: JobStatus
    description: Union[T, FailureDetails, Dict]


class JobDescriptionSuccess(JobDescriptionBase[T], Generic[T]):
    kind: Literal["success"] = pydantic.Field(default="success")
    status: SuccessStatus = Field(default=JobStatus.COMPLETED)
    description: T


class JobDescriptionFailure(JobDescriptionBase[Any]):
    kind: Literal["failure"] = pydantic.Field(default="failure")
    status: FailureStatus
    description: FailureDetails


class JobDescriptionNonFinal(JobDescriptionBase[Any]):
    kind: Literal["non_final"] = pydantic.Field(default="non_final")
    status: NonFinalStatus
    description: Dict = Field(default_factory=dict)

    @pydantic.validator("description")
    def validate_empty_description(cls, description: Dict) -> Dict:
        if description:
            raise ValueError("Non-final job description must be empty")

        return description


class JobDescriptionUnion(GenericModel, Generic[T], json_encoders=CUSTOM_ENCODERS):
    __root__: Union[
        JobDescriptionSuccess[T], JobDescriptionFailure, JobDescriptionNonFinal
    ] = Field(discriminator="kind")
