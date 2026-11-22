import random
import unicodedata
import unittest
from pathlib import Path

from coptic_hyphenation import SOFT_HYPHEN, Hyphenator, hyphenate, load, units

CASES = Path(__file__).with_name("cases.txt")


def cases() -> list[str]:
    lines = CASES.read_text(encoding="utf-8").splitlines()
    return [line for line in lines if line.strip() and not line.startswith("#")]


class PinnedCases(unittest.TestCase):
    def test_every_pinned_case(self):
        for expected in cases():
            with self.subTest(expected=expected):
                self.assertEqual(expected, hyphenate(expected.replace("-", ""), "-"))

    def test_vowel_sequences_are_never_split(self):
        for word, sequence in [("ⲟⲩⲱⲟⲩ", "ⲟⲩ"), ("ⲙ̀ⲙⲱⲟⲩ", "ⲱⲟⲩ"), ("ⲛⲓⲫⲏⲟⲩⲓ", "ⲟⲩⲓ")]:
            with self.subTest(word=word):
                self.assertIn(sequence, hyphenate(word, "-"))

    def test_capitals_break_like_small_letters(self):
        self.assertEqual("Ⲡⲓ-ⲭⲣⲓ-ⲥⲧⲟⲥ", hyphenate("Ⲡⲓⲭⲣⲓⲥⲧⲟⲥ", "-"))
        self.assertEqual("Ⲙ̀-ⲫⲣⲏϯ", hyphenate("Ⲙ̀ⲫⲣⲏϯ", "-"))


class Invariants(unittest.TestCase):
    WORDS = [
        "ⲉⲑⲟⲩⲁⲃ", "ⲡⲓⲭⲣⲓⲥⲧⲟⲥ", "ⲛⲉⲛⲛⲟⲃⲓ", "ⲙ̀ⲫⲣⲏϯ", "ⲡⲉⲛⲛⲟⲩϯ", "ⲙ̀ⲙⲱⲟⲩ", "ⲓⲏⲥⲟⲩⲥ",
        "ⲡⲓⲡⲛⲉⲩⲙⲁ", "ⲛ̀ⲧⲉϥⲭⲁ", "ⲛ̀ⲥⲏⲟⲩ", "ⲁⲗⲗⲏⲗⲟⲩⲓⲁ", "ⲡⲉⲛⲓⲱⲧ", "ⲙ̀ⲡϭⲟⲓⲥ", "ⲛ̀ϧⲏⲧϥ",
        "ⲡⲉⲛⲥⲱⲧⲏⲣ", "ϯⲡⲁⲣⲑⲉⲛⲟⲥ", "ⲛ̀ⲁⲅⲁⲑⲟⲥ", "ⲡⲓⲕⲁϩⲓ", "ⲛⲓⲫⲏⲟⲩⲓ", "ⲟⲩⲙⲉⲑⲙⲏⲓ",
        "ⲛⲓⲉⲛⲉϩ", "ⲡⲓⲉϩⲟⲟⲩ", "ⲁϥⲧⲱⲛϥ", "Ⲯⲁⲗⲙⲟⲥ", "Ⲁⲗⲗⲏⲗⲟⲩⲓⲁ",
    ]

    def test_text_is_unchanged(self):
        for word in self.WORDS:
            self.assertEqual(word, hyphenate(word).replace(SOFT_HYPHEN, ""))

    def test_no_break_at_a_word_edge_or_before_a_mark(self):
        h = Hyphenator()
        for word in self.WORDS:
            for offset in h.word_breaks(word):
                self.assertGreater(offset, 0, word)
                self.assertLess(offset, len(word), word)
                self.assertNotEqual("Mn", unicodedata.category(word[offset]), word)

    def test_text_outside_words_passes_through(self):
        self.assertEqual("", hyphenate(""))
        self.assertEqual("123 :.", hyphenate("123 :."))


class NoLoneConsonants(unittest.TestCase):
    LETTERS = "ⲁⲃⲅⲇⲉⲍⲏⲑⲓⲕⲗⲙⲛⲝⲟⲡⲣⲥⲧⲩⲫⲭⲯⲱϣϥϧϩϫϭϯ"
    MARKS = ["", "", "", "", "\u0300", "\u0308", "\ufe26"]

    def pieces_have_vowels(self, h, word):
        us = units(word)
        cuts = sorted(h.unit_breaks(us))
        if not cuts:
            return
        lower = [u.lower() for u in us]
        kinds = [h.kind(u) for u in us]
        for a, z in zip([0] + cuts, cuts + [len(us)]):
            self.assertTrue(h._has_vowel(lower[a:z], kinds[a:z]), h.hyphenate(word, "-"))

    def test_pinned_words(self):
        h = Hyphenator()
        for line in cases():
            for word in line.replace("-", "").split():
                self.pieces_have_vowels(h, word.strip(",."))

    def test_random_words(self):
        rng = random.Random(1)
        h = Hyphenator()
        for _ in range(5000):
            word = "".join(rng.choice(self.LETTERS) + rng.choice(self.MARKS) for _ in range(rng.randint(2, 14)))
            self.pieces_have_vowels(h, word)
            self.assertEqual(word, h.hyphenate(word).replace(SOFT_HYPHEN, ""))
            for offset in h.word_breaks(word):
                self.assertNotEqual("Mn", unicodedata.category(word[offset]), word)
                self.assertNotIn(word[offset - 2:offset].lower(), h.rules.jinkim_articles, word)


class RulesFile(unittest.TestCase):
    def test_the_rules_file_is_consistent(self):
        rules = load()
        h = Hyphenator(rules)
        for pair in rules.onsets:
            self.assertEqual(2, len(units(pair)), pair)
            for unit in units(pair):
                self.assertEqual("consonant", h.kind(unit), pair)
        for unit in rules.syllabic:
            self.assertEqual(1, len(units(unit)), unit)
        self.assertEqual(len(rules.prefixes), len(set(rules.prefixes)))
        for letter in rules.articles:
            self.assertEqual("consonant", h.kind(letter), letter)
        for prefix in rules.prefixes:
            for word in prefix.not_in:
                self.assertIn(prefix.text, word, word)
        for unit in rules.jinkim_articles:
            self.assertEqual(unit[0] + "\u0300", unit, unit)
            self.assertIn(unit[0], rules.articles, unit)
            self.assertNotIn(unit, rules.syllabic, unit)


if __name__ == "__main__":
    unittest.main()
