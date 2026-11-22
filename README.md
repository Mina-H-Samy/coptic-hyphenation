# Coptic hyphenation

Rules for dividing Coptic words at the end of a line, written down as a
specification, kept as data, and turned into the TeX pattern file that TeX,
Typst and other software use to hyphenate.

**Status: version 1, work in progress.** The list of consonant pairs that stay
together has been rebuilt from nothing; 49 pairs whose answer depends on the
word are still open.
[SPEC.md](SPEC.md) describes the rules, the problems found so far and the
decisions still open. There is no pattern file yet.

## Layout

| Path | What it is |
|---|---|
| [`SPEC.md`](SPEC.md) | The specification: text model, rules, known problems, open decisions, evidence |
| [`rules/coptic.toml`](rules/coptic.toml) | The rules as data: vowels, syllabic units, prefixes, onset clusters, minimums |
| [`coptic_hyphenation/`](coptic_hyphenation) | The reference implementation, which carries out the rules exactly as written |
| [`tests/cases.txt`](tests/cases.txt) | Words written out the way they must break, one per line |

## Use

Python 3.11 or later, no other dependencies.

```bash
python3 -m unittest discover -s tests
```

```bash
echo "ⲡⲓⲭⲣⲓⲥⲧⲟⲥ ⲙ̀ⲫⲣⲏϯ" | python3 -m coptic_hyphenation
```

That prints `ⲡⲓ-ⲭⲣⲓ-ⲥⲧⲟⲥ ⲙ̀-ⲫⲣⲏϯ`; `--mark soft` puts U+00AD SOFT HYPHEN at
each break instead.

## Where the output goes

The pattern file, `hyph-cop.tex`, will be generated from the rules and never
edited by hand. It is meant for:

- [tex-hyphen](https://github.com/hyphenation/tex-hyphen), the hyphenation
  patterns of TeX Live and MiKTeX, replacing the Coptic patterns Claudio
  Beccari wrote in 2004;
- [hypher](https://github.com/typst/hypher), the hyphenation library of
  [Typst](https://typst.app), which copies tex-hyphen's files;
- applications that bundle a copy.

## Licence

MIT, see [LICENSE](LICENSE).
