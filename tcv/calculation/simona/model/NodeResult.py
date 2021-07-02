import re
import uuid as uuid_module
from dataclasses import dataclass
from datetime import datetime

import dateutil.parser


@dataclass
class NodeResult:
    uuid: uuid_module.UUID = uuid_module.uuid4()
    time: datetime = dateutil.parser.isoparse('1970-01-01T00:00:00Z')
    input_model: uuid_module.UUID = uuid_module.uuid4()
    v_ang_degree: float = 0.0
    v_mag_pu: float = 0.0


def from_dict(dct: dict) -> NodeResult:
    return NodeResult(
        uuid_module.UUID(dct['uuid']),
        dateutil.parser.isoparse(re.sub('\\[UTC]$', "", dct['time'])),
        uuid_module.UUID(dct['inputModel']),
        float(dct['vAng']),
        float(dct['vMag'])
    )
