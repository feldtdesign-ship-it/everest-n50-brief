# Everest × North 50 — Brief

One self-contained HTML page, published via GitHub Pages.

**Live:** https://feldtdesign-ship-it.github.io/everest-n50-brief/

## Structure

`index.html` is the whole site. It has two sections:

- **Part I — Strategic and technical brief** (from `source/Everest_N50_Brief.html`)
- **Part II — Corrections and fact check** (from `source/Everest_Briefing_Jason_v2.html`)

A single sidebar nav covers both parts. No build step, no dependencies except Google Fonts.

## Sources

The `source/` folder keeps the original standalone documents for reference. `Everest_Briefing_Jason.html` is the superseded first version and is **not** part of the published page.

To rebuild `index.html` after editing a source file, the two parts must be re-merged by hand — there is no build script.
