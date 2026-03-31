import logging
from urllib.parse import quote

import requests
from typing import Optional

import config
from dictionary.base import DictionaryProvider
from dictionary.models import WordResult, Meaning, Definition

logger = logging.getLogger(__name__)


class FreeDictAPI(DictionaryProvider):
    def lookup(self, word: str) -> Optional[WordResult]:
        url = config.FREE_DICT_API_URL.format(word=quote(word, safe=''))
        try:
            resp = requests.get(url, timeout=config.REQUEST_TIMEOUT)
            if resp.status_code != 200:
                return None
            data = resp.json()
            if not isinstance(data, list) or len(data) == 0:
                return None
            entry = data[0]

            phonetic = entry.get('phonetic')
            audio_url = None
            for p in entry.get('phonetics', []):
                if p.get('audio'):
                    audio_url = p['audio']
                    break
                if not phonetic and p.get('text'):
                    phonetic = p['text']

            meanings = []
            for m in entry.get('meanings', []):
                defs = []
                for d in m.get('definitions', []):
                    defs.append(Definition(
                        definition=d.get('definition', ''),
                        example=d.get('example'),
                        synonyms=d.get('synonyms', [])[:5],
                    ))
                meanings.append(Meaning(
                    part_of_speech=m.get('partOfSpeech', ''),
                    definitions=defs[:5],
                ))

            return WordResult(
                word=entry.get('word', word),
                phonetic=phonetic,
                audio_url=audio_url,
                meanings=meanings,
                source='Free Dictionary API',
            )
        except Exception:
            logger.exception("FreeDictAPI lookup failed for word: %s", word)
            return None
