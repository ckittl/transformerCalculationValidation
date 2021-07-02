import re
import uuid as uuid_module
from dataclasses import dataclass
from datetime import datetime

import dateutil.parser


@dataclass
class Transformer3WResult:
    uuid: uuid_module.UUID = uuid_module.uuid4()
    time: datetime = dateutil.parser.isoparse('1970-01-01T00:00:00Z')
    input_model: uuid_module.UUID = uuid_module.uuid4()
    i_a_ang_degree: float = 0.0
    i_b_ang_degree: float = 0.0
    i_c_ang_degree: float = 0.0
    i_a_mag_ampere: float = 0.0
    i_b_mag_ampere: float = 0.0
    i_c_mag_ampere: float = 0.0
    tap_pos: int = 0


def from_dict(dct: dict) -> Transformer3WResult:
    return Transformer3WResult(
        uuid_module.UUID(dct['uuid']),
        dateutil.parser.isoparse(re.sub('\\[UTC]$', "", dct['time'])),
        uuid_module.UUID(dct['inputModel']),
        float(dct['iAAng']),
        float(dct['iBAng']),
        float(dct['iCAng']),
        float(dct['iAMag']),
        float(dct['iBMag']),
        float(dct['iCMag']),
        int(dct['tapPos'])
    )
