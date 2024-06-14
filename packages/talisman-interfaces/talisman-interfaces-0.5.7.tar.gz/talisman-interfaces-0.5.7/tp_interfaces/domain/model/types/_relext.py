from dataclasses import dataclass
from typing import Optional

from tdm.abstract.datamodel import AbstractDomainType


@dataclass(frozen=True)
class RelExtModel(object):
    relation_type: str
    invert_direction: bool = False
    source_annotation: Optional[str] = None
    target_annotation: Optional[str] = None


@dataclass(frozen=True)
class RelExtBasedType(AbstractDomainType):
    pretrained_relext_models: tuple[RelExtModel, ...] = tuple()

    def __post_init__(self):
        if self.pretrained_relext_models:
            object.__setattr__(self, 'pretrained_relext_models', tuple(map(self._convert_to_model, self.pretrained_relext_models)))
        elif isinstance(self.pretrained_relext_models, list):
            object.__setattr__(self, 'pretrained_relext_models', tuple(self.pretrained_relext_models))

    @staticmethod
    def _convert_to_model(obj) -> RelExtModel:
        if isinstance(obj, RelExtModel):
            return obj
        if isinstance(obj, dict):
            return RelExtModel(**obj)
        raise ValueError
