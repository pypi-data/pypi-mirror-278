from functools import singledispatch
from typing import Iterable

from tdm import TalismanDocument
from tdm.abstract.datamodel import AbstractFact, AbstractValue, FactStatus
from tdm.datamodel.facts import AtomValueFact, ConceptFact, KBConceptValue, MentionFact, PropertyFact
from tdm.datamodel.mentions import TextNodeMention
from typing_extensions import Protocol

from tp_interfaces.domain.model.types import AtomValueType, DocumentType, PropertyType


def get_metadata(document: TalismanDocument) -> dict[str, tuple[AbstractValue, ...] | AbstractValue]:
    document_facts = document.get_facts(ConceptFact, filter_=lambda f: isinstance(f.type_id, DocumentType))
    metadata_property_facts: set[PropertyFact] = set()
    for fact in document_facts:
        metadata_property_facts.update(document.related_facts(fact, PropertyFact))

    return {property_fact.name: property_fact.target.value for property_fact in metadata_property_facts}


class MentionedFactsFactory(Protocol):
    def __call__(
            self, mention: TextNodeMention,
            status: FactStatus = FactStatus.NEW,
            value: AbstractValue | Iterable[AbstractValue] = ()
    ) -> Iterable[AbstractFact]:
        ...


@singledispatch
def mentioned_fact_factory(type_: AtomValueType | PropertyType) -> MentionedFactsFactory:
    raise NotImplementedError


@mentioned_fact_factory.register(AtomValueType)
def _value_fact_factory(type_: AtomValueType) -> MentionedFactsFactory:
    def create_facts(
            mention: TextNodeMention, status: FactStatus, value: tuple[AbstractValue, ...] | AbstractValue = ()
    ) -> tuple[AtomValueFact, MentionFact]:
        value_fact = AtomValueFact(status, type_, value)
        return value_fact, MentionFact(status, mention, value_fact)

    return create_facts


@mentioned_fact_factory.register(PropertyType)
def _concept_fact_factory(type_: PropertyType) -> MentionedFactsFactory:
    def create_facts(
            mention: TextNodeMention, status: FactStatus, value: tuple[AbstractValue, ...] | AbstractValue = ()
    ) -> tuple[ConceptFact, AtomValueFact, PropertyFact, MentionFact]:
        if status is FactStatus.APPROVED:
            concept_fact = ConceptFact(status, type_.source, KBConceptValue(value.value))
        else:
            concept_fact = ConceptFact(status, type_.source)
        value_fact = AtomValueFact(status, type_.target, value)
        return concept_fact, value_fact, PropertyFact(status, type_, concept_fact, value_fact), MentionFact(status, mention, value_fact)

    return create_facts
