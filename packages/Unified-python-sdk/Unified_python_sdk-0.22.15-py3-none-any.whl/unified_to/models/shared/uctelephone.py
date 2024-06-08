"""Code generated by Speakeasy (https://speakeasyapi.dev). DO NOT EDIT."""

from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from enum import Enum
from typing import Optional
from unified_to import utils


class UcTelephoneType(str, Enum):
    WORK = 'WORK'
    HOME = 'HOME'
    OTHER = 'OTHER'
    FAX = 'FAX'
    MOBILE = 'MOBILE'


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class UcTelephone:
    telephone: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('telephone') }})
    type: Optional[UcTelephoneType] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('type'), 'exclude': lambda f: f is None }})
    

