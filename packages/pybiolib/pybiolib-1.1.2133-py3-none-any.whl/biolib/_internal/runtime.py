from biolib.typing_utils import TypedDict


class RuntimeJobDataDict(TypedDict):
    version: str
    job_requested_machine: str
    job_uuid: str
    job_auth_token: str
    app_uri: str


class BioLibRuntimeError(Exception):
    pass


class BioLibRuntimeNotRecognizedError(BioLibRuntimeError):
    def __init__(self, message='The runtime is not recognized as a BioLib app'):
        self.message = message
        super().__init__(self.message)
