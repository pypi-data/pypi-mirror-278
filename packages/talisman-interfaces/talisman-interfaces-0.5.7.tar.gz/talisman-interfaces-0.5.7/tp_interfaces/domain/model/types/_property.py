from dataclasses import dataclass

from tdm.abstract.datamodel import FactStatus
from tdm.abstract.json_schema import generate_model
from tdm.datamodel.domain import PropertyType as BasePropertyType, RelationPropertyType as BaseRelationPropertyType
from tdm.datamodel.facts import ConceptFact, PropertyFact, ValueFact

from ._concept import ConceptType
from ._nerc import NERCBasedType
from ._relation import RelationType
from ._relext import RelExtBasedType
from ._value import AtomValueType

__deps = (AtomValueType, ConceptType, RelationType)


@generate_model(label='property')
@dataclass(frozen=True)
class PropertyType(RelExtBasedType, BasePropertyType):
    isIdentifying: bool = False

    def __post_init__(self):
        BasePropertyType.__post_init__(self)

    def build_fact(self, status: FactStatus, source: ConceptFact, target: ValueFact) -> PropertyFact:
        return PropertyFact(status, self, source, target)


@generate_model(label='id_property')
@dataclass(frozen=True)
class IdentifyingPropertyType(NERCBasedType, PropertyType):
    isIdentifying: bool = True

    def __post_init__(self):
        if not self.isIdentifying:
            raise ValueError
        PropertyType.__post_init__(self)


@generate_model(label='r_property')
@dataclass(frozen=True)
class RelationPropertyType(RelExtBasedType, BaseRelationPropertyType):
    def __post_init__(self):
        BaseRelationPropertyType.__post_init__(self)
