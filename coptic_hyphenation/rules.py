import tomllib
from dataclasses import dataclass
from pathlib import Path

DEFAULT_RULES = Path(__file__).resolve().parent.parent / "rules" / "coptic.toml"

Slot = frozenset[str] | str


@dataclass(frozen=True)
class Prefix:
    text: str
    followed_by: tuple[Slot, ...] = ()


@dataclass(frozen=True)
class Rules:
    version: str
    vowels: frozenset[str]
    carry_a_vowel: frozenset[str]
    syllabic: frozenset[str]
    prefixes: tuple[Prefix, ...]
    articles: frozenset[str]
    jinkim_articles: frozenset[str]
    onsets: frozenset[str]
    lone_consonants: bool
    min_before: int
    min_before_syllable: int
    min_after: int


def _slot(value) -> Slot:
    return value if isinstance(value, str) else frozenset(value)


def load(path: Path = DEFAULT_RULES) -> Rules:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    minimums = data["minimums"]
    return Rules(
        version=data["meta"]["version"],
        vowels=frozenset(data["letters"]["vowels"]),
        carry_a_vowel=frozenset(data["letters"].get("carry_a_vowel", ())),
        syllabic=frozenset(data["syllabic"]["units"]),
        prefixes=tuple(
            Prefix(p["text"], tuple(_slot(s) for s in p.get("followed_by", ()))) for p in data["prefix"]
        ),
        articles=frozenset(data.get("articles", {}).get("letters", ())),
        jinkim_articles=frozenset(data.get("articles", {}).get("with_jinkim", ())),
        onsets=frozenset(entry["pair"] for entry in data.get("onsets", [])),
        lone_consonants=data.get("lone_consonants", {}).get("allowed", True),
        min_before=minimums["before"],
        min_before_syllable=minimums["before_syllable"],
        min_after=minimums["after"],
    )
