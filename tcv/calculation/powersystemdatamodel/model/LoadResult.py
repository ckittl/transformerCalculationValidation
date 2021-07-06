import re
import uuid as uuid_module
from dataclasses import dataclass
from datetime import datetime

import dateutil.parser


@dataclass
class LoadResult:
    uuid: uuid_module.UUID = uuid_module.uuid4()
    time: datetime = dateutil.parser.isoparse('1970-01-01T00:00:00Z')
    input_model: uuid_module.UUID = uuid_module.uuid4()
    p_mw: float = 0.0
    q_mvar: float = 0.0


def from_dict(dct: dict) -> LoadResult:
    return LoadResult(
        uuid_module.UUID(dct['uuid']),
        dateutil.parser.isoparse(re.sub('\\[UTC]$', "", dct['time'])),
        uuid_module.UUID(dct['inputModel']),
        float(dct['p']),
        float(dct['q'])
    )
