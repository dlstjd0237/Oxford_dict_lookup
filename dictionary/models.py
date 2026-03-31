from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Definition:
    definition: str
    example: Optional[str] = None
    synonyms: list[str] = field(default_factory=list)


@dataclass
class Meaning:
    part_of_speech: str
    definitions: list[Definition]


@dataclass
class WordResult:
    word: str
    phonetic: Optional[str]
    audio_url: Optional[str]
    meanings: list[Meaning]
    source: str

    def to_json(self) -> str:
        d = {
            'word': self.word,
            'phonetic': self.phonetic,
            'audio_url': self.audio_url,
            'source': self.source,
            'meanings': [
                {
                    'part_of_speech': m.part_of_speech,
                    'definitions': [
                        {
                            'definition': df.definition,
                            'example': df.example,
                            'synonyms': df.synonyms,
                        }
                        for df in m.definitions
                    ],
                }
                for m in self.meanings
            ],
        }
        return json.dumps(d, ensure_ascii=False)

    @classmethod
    def from_json(cls, data_json: str) -> 'WordResult':
        d = json.loads(data_json)
        meanings = []
        for m in d['meanings']:
            defs = [
                Definition(
                    definition=df['definition'],
                    example=df.get('example'),
                    synonyms=df.get('synonyms', []),
                )
                for df in m['definitions']
            ]
            meanings.append(Meaning(part_of_speech=m['part_of_speech'], definitions=defs))
        return cls(
            word=d['word'],
            phonetic=d.get('phonetic'),
            audio_url=d.get('audio_url'),
            meanings=meanings,
            source=d.get('source', 'cache'),
        )
