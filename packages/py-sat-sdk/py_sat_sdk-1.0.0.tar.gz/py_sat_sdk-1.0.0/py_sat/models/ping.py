from dataclasses_json import dataclass_json, Undefined
from dataclasses import dataclass
from py_sat.models.base import BaseResponse


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PingResponse(BaseResponse):
    buildhash: str
    sandbox: bool
    status: str
