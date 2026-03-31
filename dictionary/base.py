from abc import ABC, abstractmethod
from typing import Optional

from dictionary.models import WordResult


class DictionaryProvider(ABC):
    @abstractmethod
    def lookup(self, word: str) -> Optional[WordResult]:
        """Look up a word and return a WordResult or None on failure."""
        pass
