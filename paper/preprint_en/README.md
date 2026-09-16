# English preprint

Self-contained source of the manuscript. `main.tex` is the only build input;
the Russian version lives in `../preprint_ru/` and is kept in sync by hand.

## Files

- `main.tex` — full source.
- `references.bib` — bibliography.
- `figures/*.pdf` — vector figures; the PNGs beside them are previews.
- `build_figures.py`, `build_dissociation_figure.py` — regenerate the figures
  from the sealed reports. No API calls; numpy and matplotlib only.
- `figure_sources.json` — SHA-256 of the figure inputs.
- `group_slices.json` — integer results of the 24 GroupMemBench cells.

## Build

From this directory: `tectonic main.tex`. Alternatively XeLaTeX, BibTeX,
XeLaTeX, XeLaTeX. Times New Roman, Arial and Menlo are required; substitute
installed fonts at the top of the source on another machine. The figures are
already included, so Python is not needed to build the PDF.

## Localisation note

Numbers use the English convention: period as the decimal mark, comma as the
thousands separator. The translation was checked mechanically — the multiset of
numeric tokens in `main.tex` is identical to the Russian source (697 tokens on
both sides), so no value was altered in translation.
