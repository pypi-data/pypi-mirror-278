from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json, Undefined, DataClassJsonMixin, config
from dataclasses import dataclass

import dateutil.parser
import requests


class BaseResponse(DataClassJsonMixin):
    _raw_response: requests.Response

    def get_raw_response(self) -> requests.Response:
        return self._raw_response

    def with_raw_response(self, raw_response: requests.Response):
        self._raw_response = raw_response
        return self

    def is_success(self):
        return 200 <= self._raw_response.status_code < 300


class BaseRequest(DataClassJsonMixin):
    pass


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Field:
    name: str
    value: str


datetime_config = config(
    encoder=datetime.isoformat,
    decoder=lambda x: dateutil.parser.isoparse(x),
)
