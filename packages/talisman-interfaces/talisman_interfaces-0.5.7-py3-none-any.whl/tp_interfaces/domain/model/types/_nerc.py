from dataclasses import dataclass
from typing import Optional

from tdm.abstract.datamodel import AbstractDomainType


@dataclass(frozen=True)
class NERCRegexp(object):
    regexp: str
    context_regexp: Optional[str] = None
    auto_create: bool = False


@dataclass(frozen=True)
class NERCBasedType(AbstractDomainType):
    regexp: tuple[NERCRegexp, ...] = tuple()
    black_regexp: tuple[NERCRegexp, ...] = tuple()
    pretrained_nerc_models: tuple[str, ...] = tuple()
    dictionary: tuple[str, ...] = tuple()
    black_list: tuple[str, ...] = tuple()

    def __post_init__(self):
        if self.regexp:
            object.__setattr__(self, 'regexp', tuple(map(self._convert_to_regexp, self.regexp)))
        if self.black_regexp:
            object.__setattr__(self, 'black_regexp', tuple(map(self._convert_to_regexp, self.black_regexp)))

        for attr in ['regexp', 'black_regexp', 'pretrained_nerc_models', 'dictionary', 'black_list']:
            if isinstance(getattr(self, attr), list):
                object.__setattr__(self, attr, tuple(getattr(self, attr)))

    @staticmethod
    def _convert_to_regexp(obj) -> NERCRegexp:
        if isinstance(obj, NERCRegexp):
            return obj
        if isinstance(obj, dict):
            return NERCRegexp(**obj)
        raise ValueError
