from dataclasses import dataclass

from tdm.abstract.datamodel import FactStatus
from tdm.abstract.json_schema import generate_model
from tdm.datamodel.domain import RelationType as BaseRelationType
from tdm.datamodel.facts import ConceptFact, RelationFact

from ._concept import ConceptType
from ._relext import RelExtBasedType

__deps = (ConceptType,)


@generate_model(label='relation')
@dataclass(frozen=True)
class RelationType(RelExtBasedType, BaseRelationType):
    def __post_init__(self):
        BaseRelationType.__post_init__(self)

    def build_fact(self, status: FactStatus, source: ConceptFact, target: ConceptFact) -> RelationFact:
        return RelationFact(status, self, source, target)
