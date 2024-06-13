from typing import List

from ._mock import MockType
from .base import Base


class NER(Base, metaclass=MockType):
    def __init__(self, baseurl='http://ner-prod:8000', transport=None):
        super().__init__(baseurl, transport)

    def ner(self, *, sentences: List[str]) -> List[List]:
        result = self._do_post('ner', sentences)
        return result
