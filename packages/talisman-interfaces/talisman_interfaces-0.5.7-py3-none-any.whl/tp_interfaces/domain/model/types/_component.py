from dataclasses import dataclass

from tdm.abstract.json_schema import generate_model
from tdm.datamodel.domain import ComponentValueType as BaseComponentValueType

from ._relext import RelExtBasedType
from ._value import AtomValueType

__deps = (AtomValueType,)


@generate_model(label='component')
@dataclass(frozen=True)
class ComponentValueType(RelExtBasedType, BaseComponentValueType):
    isRequired: bool = False  # TODO: move to tdm?
