# Everest × North 50 — Brief

One self-contained HTML page, published via GitHub Pages.

**Live:** https://feldtdesign-ship-it.github.io/everest-n50-brief/

## Structure

`index.html` is the whole site. Two tabs at the top switch between:

- **Part I — Strategic and technical brief** (from `source/Everest_N50_Brief.html`)
- **Part II — Corrections and fact check** (from `source/Everest_Briefing_Jason_v2.html`)

The sidebar nav follows the active tab. Deep links work: `#part-b` opens the second tab, and any section anchor (`#a05`, `#b07`) opens the right tab and scrolls to it. Printing outputs both parts. No dependencies except Google Fonts.

## Sources

The `source/` folder keeps the original standalone documents for reference. `Everest_Briefing_Jason.html` is the superseded first version and is **not** part of the published page.

## Rebuilding

`index.html` is generated. After editing a file in `source/`, regenerate it:

```bash
python3 build.py
```

`build.py` pulls the two parts out of the source documents, namespaces their section ids (`a01…`, `b01…`) so they can share one page, and adds the tab bar and the merged stylesheet. Edits made directly to `index.html` will be overwritten.
