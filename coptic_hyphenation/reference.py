import unicodedata
from functools import lru_cache

from .rules import Rules, load

SOFT_HYPHEN = "­"


def is_mark(ch: str) -> bool:
    return unicodedata.category(ch) == "Mn"


def is_word_char(ch: str) -> bool:
    return ch.isalpha() or is_mark(ch)


def units(word: str) -> list[str]:
    out: list[str] = []
    for ch in word:
        if is_mark(ch) and out:
            out[-1] += ch
        else:
            out.append(ch)
    return out


@lru_cache(maxsize=None)
def default_rules() -> Rules:
    return load()


class Hyphenator:
    def __init__(self, rules: Rules | None = None):
        self.rules = rules or default_rules()
        self._prefixes = sorted(
            ((units(p.text), p.followed_by) for p in self.rules.prefixes),
            key=lambda entry: len(entry[0]),
            reverse=True,
        )

    def kind(self, unit: str) -> str:
        lower = unit.lower()
        if lower in self.rules.syllabic:
            return "syllable"
        if lower[0] in self.rules.vowels:
            return "vowel"
        return "consonant"

    @staticmethod
    def _matches(lower: list[str], kinds: list[str], start: int, slots) -> bool:
        if start + len(slots) > len(lower):
            return False
        for offset, slot in enumerate(slots):
            unit, kind = lower[start + offset], kinds[start + offset]
            if slot in ("consonant", "vowel"):
                if kind != slot:
                    return False
            elif unit not in slot:
                return False
        return True

    def unit_breaks(self, us: list[str]) -> set[int]:
        r = self.rules
        n = len(us)
        lower = [u.lower() for u in us]
        kinds = [self.kind(u) for u in us]

        standalone: set[int] = set()
        for i, kind in enumerate(kinds):
            if kind == "syllable":
                standalone |= {i, i + 1}

        prefix_length = 0
        for prefix, followed_by in self._prefixes:
            size = len(prefix)
            if n > size and lower[:size] == prefix and self._matches(lower, kinds, size, followed_by):
                prefix_length = size
                standalone.add(prefix_length)
                break

        hosts = {i + 1 for i, kind in enumerate(kinds) if kind == "syllable"}
        if prefix_length:
            hosts.add(prefix_length)
        held: set[int] = set()
        for h in hosts:
            if h + 1 < n and kinds[h] == kinds[h + 1] == "consonant" and lower[h] in r.articles:
                end = h
                while end < n and kinds[end] == "consonant":
                    end += 1
                held |= set(range(h + 1, end))

        onset_rule: set[int] = set()
        i = 0
        while i < n:
            if kinds[i] != "consonant":
                i += 1
                continue
            end = i
            while end < n and kinds[end] == "consonant":
                end += 1
            if i > 0 and end < n:
                if end - i == 1:
                    onset_rule.add(i)
                elif lower[end - 2] + lower[end - 1] in r.onsets:
                    onset_rule.add(end - 2)
                else:
                    onset_rule.add(end - 1)
            i = end

        breaks = {b for b in standalone if b >= r.min_before_syllable}
        breaks |= {b for b in onset_rule if b >= r.min_before and b >= prefix_length and b not in held}
        breaks = {b for b in breaks if n - b >= r.min_after}
        if not r.lone_consonants:
            breaks = self._join_lone_consonants(lower, kinds, hosts, breaks)
        return breaks

    def _has_vowel(self, lower: list[str], kinds: list[str]) -> bool:
        return any(k != "consonant" or u in self.rules.carry_a_vowel for u, k in zip(lower, kinds))

    def _join_lone_consonants(self, lower, kinds, hosts, breaks: set[int]) -> set[int]:
        n = len(lower)
        if not self._has_vowel(lower, kinds):
            return set()
        breaks = set(breaks)
        while True:
            cuts = sorted(breaks)
            for a, z in zip([0] + cuts, cuts + [n]):
                if self._has_vowel(lower[a:z], kinds[a:z]):
                    continue
                if a == 0:
                    breaks.discard(z)
                elif z == n:
                    breaks.discard(a)
                elif a in hosts and kinds[z] != "syllable":
                    breaks.discard(z)
                else:
                    breaks.discard(a)
                break
            else:
                return breaks

    def word_breaks(self, word: str) -> list[int]:
        us = units(word)
        chosen = self.unit_breaks(us)
        offsets, offset = [], 0
        for i, u in enumerate(us):
            if i in chosen:
                offsets.append(offset)
            offset += len(u)
        return offsets

    def breaks(self, text: str) -> list[int]:
        offsets: list[int] = []
        i = 0
        while i < len(text):
            if not is_word_char(text[i]):
                i += 1
                continue
            end = i
            while end < len(text) and is_word_char(text[end]):
                end += 1
            offsets.extend(i + o for o in self.word_breaks(text[i:end]))
            i = end
        return offsets

    def hyphenate(self, text: str, mark: str = SOFT_HYPHEN) -> str:
        out, last = [], 0
        for offset in self.breaks(text):
            out.append(text[last:offset])
            out.append(mark)
            last = offset
        out.append(text[last:])
        return "".join(out)


def hyphenate(text: str, mark: str = SOFT_HYPHEN) -> str:
    return Hyphenator().hyphenate(text, mark)
