import logging
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from typing import Optional

import config
from dictionary.base import DictionaryProvider
from dictionary.models import WordResult, Meaning, Definition

logger = logging.getLogger(__name__)


class OxfordScraper(DictionaryProvider):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    def lookup(self, word: str) -> Optional[WordResult]:
        safe_word = quote(word.lower().replace(' ', '-'), safe='-')
        url = config.OXFORD_LEARNER_URL.format(word=safe_word)
        try:
            resp = requests.get(url, headers=self.HEADERS, timeout=config.REQUEST_TIMEOUT)
            if resp.status_code != 200:
                return None
            soup = BeautifulSoup(resp.text, 'html.parser')

            # Phonetic
            phonetic = None
            phon_el = soup.select_one('.phon')
            if phon_el:
                phonetic = phon_el.get_text(strip=True)

            # Audio
            audio_url = None
            audio_el = soup.select_one('div.sound[data-src-mp3]')
            if audio_el:
                audio_url = audio_el.get('data-src-mp3')

            # Meanings
            meanings = []
            # Try to get part of speech
            pos_el = soup.select_one('.pos')
            pos = pos_el.get_text(strip=True) if pos_el else ''

            defs = []
            for sense in soup.select('.sense'):
                def_el = sense.select_one('.def')
                if not def_el:
                    continue
                definition_text = def_el.get_text(strip=True)
                example = None
                ex_el = sense.select_one('.x')
                if ex_el:
                    example = ex_el.get_text(strip=True)
                defs.append(Definition(
                    definition=definition_text,
                    example=example,
                ))
                if len(defs) >= 5:
                    break

            if defs:
                meanings.append(Meaning(part_of_speech=pos, definitions=defs))

            if not meanings:
                return None

            return WordResult(
                word=word,
                phonetic=phonetic,
                audio_url=audio_url,
                meanings=meanings,
                source='Oxford Learner\'s Dictionary',
            )
        except Exception:
            logger.exception("OxfordScraper lookup failed for word: %s", word)
            return None
