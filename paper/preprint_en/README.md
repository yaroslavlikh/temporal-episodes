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
- `verify_editorial.py`, `editorial_verification.json` — the offline editorial check
  (gold intersections, aggregates, repaired outputs, network bootstrap) and its report with
  SHA-256 of the inputs read; identical to the Russian directory.
- `group_slices.json` — historical slices of the original Group run; not the source of the
  repaired accuracy reported in the manuscript.

## Build

From this directory: `tectonic main.tex`. Alternatively XeLaTeX, BibTeX,
XeLaTeX, XeLaTeX. Times New Roman, Arial and Menlo are required; substitute
installed fonts at the top of the source on another machine. The figures are
already included, so Python is not needed to build the PDF.

## Localisation note

Numbers use the English convention: period as the decimal mark, comma as the thousands
separator. The translation was checked mechanically: after normalising decimal and thousands
separators, the multiset of numeric tokens in `main.tex` is identical to the Russian source,
and the two sources have the same sections, figures, tables, labels, references and citations.
Figure scripts differ from the Russian ones only in their strings and in not converting
decimal points to commas.

The scripts read the sealed runs from the author's workspace (`.research_runs/`); in this
repository the same per-question files live under `results/`, and `figure_sources.json`
records the SHA-256 of every input.
