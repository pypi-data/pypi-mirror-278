from dataclasses import dataclass
from typing import Optional

from tdm.abstract.json_schema import generate_model
from tdm.datamodel.domain import AtomValueType as BaseAtomValueType, CompositeValueType

from ._nerc import NERCBasedType


@generate_model(label='atom')
@dataclass(frozen=True)
class AtomValueType(NERCBasedType, BaseAtomValueType):
    value_restriction: Optional[tuple[str, ...]] = None

    def __post_init__(self):
        BaseAtomValueType.__post_init__(self)
        if isinstance(self.value_restriction, list):
            object.__setattr__(self, 'value_restriction', tuple(self.value_restriction))


generate_model(label='composite')(CompositeValueType)
