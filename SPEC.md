# Coptic hyphenation: specification

**Status: draft, version 1 in progress.** Version 0 was the set of rules this
work started from. Version 1 starts the onset list again from nothing and adds
the decisions of 2026-11-20: ⲉ̀ and ϣ̀ as syllabic units, the prefix ⲉ before an
article, the article rule (R3) and the rule that no piece is left without a
vowel (R6); and of 2026-11-22: ⲓ̀ and ⲁ̀ as syllabic units, and an article
written with a jinkim kept with its noun. It is not yet the proposed standard: section 7 lists the decisions
still open, and section 6 the problems they have to settle.

The rules themselves are data, in [`rules/coptic.toml`](rules/coptic.toml).
[`coptic_hyphenation/reference.py`](coptic_hyphenation/reference.py) carries
them out, and [`tests/cases.txt`](tests/cases.txt) pins them word by word. When
this document and the code disagree, that is a bug in one of them.

## 1. Scope

Bohairic Coptic in Unicode, as written in the liturgical books of the Coptic
Orthodox Church. Other dialects are an open decision (D6).

## 2. Text model

- A **letter** is a character of the Coptic alphabet.
- A **mark** is a combining mark (Unicode category Mn): the jinkim (U+0300),
  the trema (U+0308), the overline of abbreviations and numerals (U+FE26, also
  written U+0305 or U+FE24/U+FE25), and any other.
- A **unit** is one letter and the marks written after it. ⲛ̀ is one unit, so
  is ⲏ︦.
- A **word** is a run of letters and marks. Everything else (spaces,
  punctuation, digits) separates words and is never touched.
- A break falls only between two units, never between a letter and its mark.
- Case is ignored: a capital behaves exactly like its small letter.

## 3. Classes

- A **vowel** is a unit whose letter is ⲁ, ⲉ, ⲏ, ⲓ, ⲟ, ⲩ or ⲱ.
- A **syllabic unit** is a syllable by itself: ⲙ̀ or ⲛ̀ (a syllabic sonorant),
  ⲉ̀, ⲓ̀ or ⲁ̀ (a vowel standing alone) and ϣ̀ (ϣ with the vowel before it). The
  jinkim marks all six. On any other letter the jinkim is a plain mark, except
  on an article (below).
- A **consonant** is every other unit, ϯ included.
- A **nucleus** is a vowel or a syllabic unit. ϯ is a consonant for R4, but
  carries its own vowel ("ti"), so a piece holding it is never vowelless (R6).
- A **one-letter article** is ⲡ, ⲫ, ⲧ, ⲑ or ϯ. ϯ carries its own vowel, but
  is treated like the others (decided 2026-11-20).
- A **jinkim article** is ⲡ̀, ⲫ̀, ⲧ̀ or ⲑ̀: an article written with a jinkim. It
  carries its own vowel, as ϯ does, and is a consonant for R4 (decided
  2026-11-22).

## 4. Rules

**R1. Syllabic units.** A break may fall on either side of a syllabic unit.

> ⲙ̀-ⲫⲣⲏϯ, ⲛ̀-ⲥⲏⲟⲩ, ⲛ̀-ⲟⲩⲱⲧ, ⲛ̀-ⲧⲉϥⲭⲁ, ⲉ̀-ⲃⲟⲗ, ⲁϥ-ⲉ̀ⲙⲓ, ⲁϥ-ϣ̀-ⲧⲉⲙ-ϫⲓⲙⲓ,
> ϣ̀-ϫⲟⲙ, ⲁϥ-ⲓ̀ⲛⲓ, ⲛ̀-ⲛⲉϥ-ⲓ̀ⲃⲓ, ⲁ̀-ⲛⲟⲕ, ⲡⲉϥ-ⲁ̀-ϣⲁⲓ; but ⲙⲱⲩ̀-ⲥⲏⲥ, ⲥ̀ⲛⲟⲩϯ

**R2. Prefixes.** If a word begins with one of the prefixes in the rules file
(ⲡⲓ, ϯ, ⲛⲓ, ⲟⲩ, ϩⲁⲛ, ⲫⲏ, ⲛⲏ, ⲡⲉⲛ, ⲧⲉⲛ, ⲛⲉⲛ) and more follows, a break may
fall after the longest one that matches, and R4 makes no break inside it. The
preposition ⲉ written without its jinkim is a prefix only before ⲡ or ⲫ and a
consonant, where it can only be ⲉ + article: before ⲧ or ⲑ an unmarked ⲉⲧ- or
ⲉⲑ- is nearly always the relative or ⲉⲑⲃⲉ.

> ⲡⲓ-ⲕⲁϩⲓ, ϩⲁⲛ-ⲙⲏϣ, ⲡⲉⲛ-ⲓⲱⲧ (never ⲡⲉ-ⲛⲓⲱⲧ), ⲛⲏ-ⲉⲧⲭⲏ, ⲉ-ⲡϣⲱⲓ, ⲉ-ⲫⲙⲁ; but
> ⲉⲑ-ⲛⲏⲟⲩ

**R3. Articles.** When the consonants that follow a syllabic unit or a
word-initial prefix begin with a one-letter article, they all go with the next
syllable: the article stays with its noun, and R4 makes no break among them.
A one-letter subject pronoun needs no rule of its own: R4 already splits after
it.

> ⲙ̀-ⲫⲛⲟⲩϯ, ⲙ̀-ⲡϭⲟⲓⲥ, ⲉ̀-ⲡϣⲱⲓ, ⲙ̀-ⲡⲥⲧⲁⲩ-ⲣⲟⲥ, ⲛ̀-ϯⲙⲉⲑ-ⲙⲏⲓ; and the pronouns
> ⲁϥ-ⲧⲱⲛϥ, ⲁⲕ-ⲗⲉⲥ

A pattern cannot tell the article ϯ from the pronoun ϯ- "I" or the verb ϯ
"give", so these lose the break after ϯ too (ⲉ̀-ϯⲛⲁϣⲉ, ⲉ̀-ϯϩⲁⲡ). No wrong break
is added; one break is lost.

The same position also holds the start of a stem, and the rule keeps that whole
too: ⲟⲩ-ⲧϩⲉⲙⲕⲟ, ⲛⲓ-ⲧⲣⲁ-ⲡⲉⲍⲁ, ⲉ̀-ⲑⲣⲉϥ-ⲥⲉⲙⲓ. For ⲡ, ⲫ, ⲧ and ⲑ, R6 alone would
give the same result; R3 is what keeps ϯ with its noun.

A jinkim article stays with its noun wherever it stands: a break may fall
before it, with one unit before the break as for R1, but never after it.

> ϫⲉⲙ-ⲡ̀ϣⲓⲛⲓ, ⲙ̀-ⲫ̀ⲣⲏϯ, ⲙ̀-ⲡ̀ⲕⲁϩⲓ; ⲡ̀ϭⲟⲓⲥ and ⲡ̀ⲟⲩⲣⲟ have no break

**R4. Onsets.** Where one or more consonants stand between two nuclei, one break
falls among them. A single consonant goes to the next syllable. Of two or
more, the next syllable takes the last two if they are a listed onset pair,
otherwise only the last one. Consonants at the start or end of a word give no
break, and two vowels side by side are never separated.

> ⲓⲏ-ⲥⲟⲩⲥ, ⲡⲓ-ⲭⲣⲓ-ⲥⲧⲟⲥ (ⲭⲣ, ⲥⲧ are onsets), ⲁⲗ-ⲗⲏ-ⲗⲟⲩⲓⲁ (ⲗⲗ is not),
> ⲡⲓ-ⲡⲛⲉⲩⲙⲁ, ⲧⲉ-ⲧⲉⲛ-ϣⲧⲉ-ⲙⲉⲣ-ⲥⲕⲁⲛ-ⲇⲁ-ⲗⲓ-ⲍⲉⲥⲑⲉ

The onset list is in the rules file. It was started from nothing on
2026-11-20 and holds only the six pairs the pinned cases need (ⲭⲣ, ⲥⲧ, ⲡⲛ, ϣⲧ,
ⲥⲕ, ⲫⲣ), each marked *pinned* until reviewed. Every other pair is to be decided
on its own, from how it sits in real words. A consonant carrying a mark is
never part of an onset.

**R5. Minimums.** Counted in units:

- at least 2 units before a break made by R4;
- at least 1 unit before a break made by R1 or R2 (ϯ-ⲡⲁⲣ-ⲑⲉ-ⲛⲟⲥ, ⲉ-ⲡϣⲱⲓ);
- at least 3 units after any break (ϯ-ⲙⲉ-ⲧⲟⲩⲣⲟ, not ϯ-ⲙⲉ-ⲧⲟⲩ-ⲣⲟ).

> ⲛⲉⲙ, ⲁⲙⲏⲛ and ⲉⲑⲟⲩⲁⲃ have no break; ⲛⲓ-ⲉ-ⲛⲉϩ and ⲫⲏ-ⲉ-ⲑⲟⲩⲁⲃ do.

**R6. No lone consonants.** No piece between two breaks may be left without a
nucleus (or a letter that carries a vowel: ϯ or a jinkim article). Where the
rules above would leave consonants alone, a break is dropped. Consonants that
come after a prefix or a syllabic unit join what follows, as the start of a
stem; any others join what precedes, as the end of a word part such as a
pronoun. At either end of a word they join the only side there is. A word with
no nucleus at all (a numeral, an abbreviation such as ⲡⲭ︦ⲥ︦) has no break.

> ⲡⲓ-ϣⲗⲟⲗ, ⲛ̀-ⲕⲣⲓ-ⲧⲏⲥ, ⲡⲓ-ⲥⲧⲣⲁ-ⲧⲏ-ⲗⲁ-ⲧⲏⲥ; ⲡⲉϥ-ⲙ̀-ⲃⲟⲛ, ⲉⲣⲉ-ⲧⲉⲛ-ⲉ̀-ϣⲱⲧ,
> ⲙ̀-ⲡⲣⲉⲙ-ⲛ̀-ⲭⲏⲙⲓ

## 5. Relation to earlier work

**Claudio Beccari, *Hyphenation patterns for Coptic* (`hyph-cop.tex`, 2004),
in the hyph-utf8 package.** The file this standard is meant to replace in
tex-hyphen. Nothing of it is kept: its list of onset pairs, which version 0 had
started from, was guessed from written words and has been dropped (P2).

## 6. Known problems

Found on 2026-11-20 by running the rules over a private corpus of Bohairic
liturgical texts and over the Coptic SCRIPTORIUM corpora (section 8).

**P1. Two theories meet in one word.** R1 and R2 break by syllabic unit and
morpheme, R4 by onset, and together they can leave a lone consonant between
two breaks: ⲙ̀-ⲡ-ϭⲟⲓⲥ, ⲛ̀-ϧ-ⲣⲏⲓ, ⲙ̀-ⲫ-ⲛⲟⲩϯ, ϩⲁⲛ-ϣ-ⲫⲏⲣⲓ. Each break on its
own is defensible; together they are not a division into syllables.
*Settled 2026-11-20* by R3 and R6: no word of the private corpus is left with a
lone consonant (1,248 had one, 448 of them from making ⲉ̀ a syllabic unit).

**P2. The old onset list was guessed from written words.** Coptic writes articles,
possessives, prepositions and subject pronouns joined to the word, so "could
begin a word" admits almost any consonant after ⲡ, ⲧ, ⲫ, ⲑ, ⲛ, ϥ. Words in
the private corpus open with 174 different consonant pairs, 136 of them not on
the old list, most of them exactly this (ϥⲛ, ⲡϫ, ⲡϣ, ⲡϭ). The other way round,
8 of its pairs open no word in the private corpus at all (ϧⲗ ϭϧ ϭⲧ ⲇϧ ⲥϥ ⲥⲅ ⲥⲇ
ⲧⲍ), and ϥⲗ opens no stem in the Coptic SCRIPTORIUM Bohairic New Testament or
in the Coptic Compass dictionary: it is ⲡⲉϥ-, ⲁϥ- and the like joined to a
stem, and it gives ⲙ̀-ⲡⲉ-ϥⲗⲟ-ⲅⲟⲥ where the word is ⲙ̀ⲡⲉϥ-ⲗⲟⲅⲟⲥ. Stems that do
begin with an unlisted pair break wrongly: ϫⲫⲟ "beget" gives Ⲁⲥϫ-ⲫⲟϥ for
Ⲁⲥ-ϫⲫⲟϥ (139 words contain ϫⲫ).

The corpora cannot settle the list by counting. Editions write the same stems
with and without a jinkim on the first letter: in the Coptic SCRIPTORIUM texts
that keep jinkims, ⲙⲙⲟⲛ appears 50 times and ⲙ̀ⲙⲟⲛ 23 times, ⲙⲙⲁⲩ 56 times
and ⲙ̀ⲙⲁⲩ 19, so an unmarked ϩⲗⲓ or ⲥⲙⲏ may still begin with a syllabic
consonant. Each candidate pair needs a reader's decision (D2, D4), which is
why the list is being rebuilt from nothing: for every pair the rule decides,
the morpheme divisions of Coptic SCRIPTORIUM show how it sits in real words,
inside one morpheme, opening one, or straddling a morpheme boundary.

**P3. Morphemes inside the word.** R2 knows only word-opening prefixes. Others
break by syllable: ⲙⲉ-ⲧⲟⲩⲣⲟ (morphemes ⲙⲉⲧ-ⲟⲩⲣⲟ), ⲣⲉ-ϥⲉⲣ-ⲛⲟⲃⲓ (ⲣⲉϥ-ⲉⲣ-ⲛⲟⲃⲓ).

**P4. Greek loanwords.** Greek onsets such as ⲫⲑ, ⲥⲫ, ⲥⲭ, ⲅⲛ are missing,
and R4 never keeps three consonants together, so ⲁⲣⲓⲥⲫⲣⲁⲅⲓⲍⲓⲛ breaks as
ⲁⲣⲓⲥ-ⲫⲣⲁ-ⲅⲓ-ⲍⲓⲛ, where both the Greek division and the morphemes (ⲁⲣⲓ +
σφραγίζειν) give ⲁⲣⲓ-ⲥⲫⲣⲁ…. The jinkim on a Greek word's first vowel is a
spelling convention, not a syllable of its own, but R1 cannot tell: ⲧⲁ̀ⲣⲭⲏ
(the article + ἀρχή) breaks as ⲧⲁ̀-ⲣⲭⲏ, where the Greek is ἀρ-χή.

**P5. The jinkim on other letters.** Version 0 made only ⲙ̀ and ⲛ̀ syllabic
units, but in the private corpus the jinkim also stands on ⲉ (in 6,678 distinct
words), ϣ (567), ⲓ (240), ⲁ (43), ⲡ (35) and others. *Settled 2026-11-22*
(D2).

**P6. Overlined words.** Abbreviations and numerals carry an overline across
their letters. 828 such words occur in the private corpus, and in 51 of them a
break touches an overlined letter, even inside the abbreviation: ⲓⲏ︦-ⲥ︦ⲟⲩⲥ,
ⲡⲓ-ⲡ︦ⲛ︦ⲁ, ⲉⲓ-ⲗ︦ⲏ︦ⲙ︦. (R6 removed the worst, such as ⲛⲓ-ⲡ︦-ⲛ︦ⲁ︦-ⲧⲟ-ⲫⲟ-ⲣⲟⲥ.)

**P7. Minimums are counted in units.** TeX and hypher count code points, and
ⲛ̀ is two. The pattern file has to carry the difference itself.

**P8. Editions divide words differently.** The liturgical books write ϧⲉⲛ
ⲛⲓϫⲟⲙ; scholarly editions and Coptic SCRIPTORIUM join the preposition to its
noun, ϧⲉⲛⲛⲓϫⲟⲙ. The same rules have to give sensible breaks in both.

## 7. Open decisions

- **D1.** When syllables and morphemes disagree (P1, P3), which wins? *Decided
  2026-11-20 for the lone letters:* a one-letter article goes with what follows
  (R3), ϯ included (ⲛ̀-ϯⲙⲉⲑ-ⲙⲏⲓ), and a one-letter subject pronoun with what
  precedes. Still open: the other kinds of lone letter (prepositions,
  negations, object pronouns).
- **D2.** Is a letter with a jinkim always a syllable by itself (P5)?
  *Decided:* yes for ⲉ̀ and ϣ̀ (2026-11-20), and for ⲓ̀ and ⲁ̀ (2026-11-22), at
  the cost of a Greek word such as ⲧⲁ̀-ⲣⲭⲏ (P4). On an article (ⲡ̀, ⲫ̀, ⲧ̀,
  ⲑ̀) the jinkim keeps the article with its noun (R3). On the other letters,
  all rare (ⲥ̀, ⲩ̀, ⲟ̀, ⲏ̀, ϥ̀ …, under 30 words in the private corpus), it is a
  plain mark.
- **D3.** Greek onsets (P4): for every word, or only for known loanwords? A
  pattern file cannot tell a loanword from a native word except by listing
  stems.
- **D4.** *Decided 2026-11-20:* the onset list is rebuilt from nothing, pair
  by pair, from how each pair sits in Coptic SCRIPTORIUM's morpheme divisions
  (P2). Still open: the pairs themselves.
- **D5.** No break inside an overlined run, or next to one (P6)?
- **D6.** Bohairic only, or Coptic as a whole? Sahidic marks a syllabic
  consonant with the superlinear stroke, the same character as the overline of
  an abbreviation.
- **D7.** Are 2 before and 3 after the right minimums?

## 8. Evidence

- **A private corpus** of Bohairic liturgical texts and a Bohairic Bible,
  58,049 distinct words. Used only for counts and for checking; nothing of its
  text is published here.
- **Coptic SCRIPTORIUM, corpora** (github.com/CopticScriptorium/corpora,
  CC-BY 4.0). Ten Bohairic corpora, every written word divided into morphemes
  (ⲡ|ϫⲱⲙ, ⲁ|ϥ|ϫⲫⲉ) with its part of speech, Greek loanwords flagged:
  - Four keep the jinkims and overlines of their edition in their `orig`
    layer, with the morphemes divided by hand: the *Life of Shenoute*
    (Leipoldt's edition of 1906, transcribed by Hany Takla), the Bohairic
    treebank (Horner's New Testament), Habakkuk and Jonah. Together 23,340
    written words. This is the best public source for the reviewed word list.
  - The Bohairic New Testament (`bohairic.nt`, 77,294 written words) and Old
    Testament are larger but normalised without jinkims (ⲙⲙⲁⲩ for ⲙ̀ⲙⲁⲩ). They
    serve for counting morphemes, not for deciding syllables.
- **Coptic Compass dictionary** (github.com/KyroHub/CopticCompass,
  `public/data/dictionary.json`), based on W. E. Crum, *A Coptic Dictionary*
  (Oxford: Clarendon Press, 1939). 6,376 entries, 4,905 with Bohairic forms
  including the bound forms (ϫⲫⲟ, ϫⲫⲉ-, ϫⲫⲟ=), each entry tagged by origin
  (3,659 Egyptian, 2,695 Greek). The tags are the obvious source for a list of
  Greek loanword stems (D3). Its Bohairic forms carry almost no jinkims. The
  code is MIT-licensed, but the data is "subject to specific academic rights",
  so it is evidence only: nothing derived from it is published here without
  its authors' consent.
- **A reviewed word list**, still to be made: real words with their breaks,
  read by someone who reads Coptic, including the hard cases above. It becomes
  `tests/cases.txt`'s successor and the test of every output.

## 9. Outputs

The deliverable is a TeX pattern file, `hyph-cop.tex`, generated from the
rules file and never edited by hand. Its users:

- **tex-hyphen** (github.com/hyphenation/tex-hyphen), which ships it with TeX
  Live and MiKTeX. It replaces Beccari's file of 2004.
- **hypher** (github.com/typst/hypher), the hyphenation library of Typst,
  which copies tex-hyphen's files. It reads only `\patterns{}`, so nothing may
  rely on a `\hyphenation{}` exception list. It finds languages by two-letter
  code only, and Typst asks it only for two-letter codes, so `cop` needs a
  small change in both before Typst can hyphenate Coptic.
- Applications that bundle a copy of the file.
