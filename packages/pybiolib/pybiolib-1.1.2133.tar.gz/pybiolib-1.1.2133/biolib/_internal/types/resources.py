from .typing import Optional, TypedDict


class ExperimentDict(TypedDict):
    job_count: int
    job_running_count: int


class ResourceDict(TypedDict):
    created_at: str
    experiment: Optional[ExperimentDict]
    name: str
    uri: str
    uuid: str
