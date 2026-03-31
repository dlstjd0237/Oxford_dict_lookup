import logging
import requests
import urllib.parse

logger = logging.getLogger(__name__)


def translate_to_korean(text: str) -> str:
    """Translate English text to Korean using Google Translate (free endpoint)."""
    if not text or not text.strip():
        return ''
    try:
        encoded = urllib.parse.quote(text)
        url = (
            'https://translate.googleapis.com/translate_a/single'
            f'?client=gtx&sl=en&tl=ko&dt=t&q={encoded}'
        )
        resp = requests.get(url, timeout=5, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        resp.raise_for_status()
        data = resp.json()
        # Response format: [[["translated","original",...], ...], ...]
        result_parts = []
        for segment in data[0]:
            if segment[0]:
                result_parts.append(segment[0])
        return ''.join(result_parts)
    except Exception:
        logger.debug("Translation failed", exc_info=True)
        return ''
