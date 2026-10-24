# CLAUDE.md

![](assets/images/1f4bb.png)
![](assets/images/1f4bb.png)
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

![](assets/images/warn.png)
![](assets/images/warn.png)
An [Obsidian](https://obsidian.md/) knowledge vault (`vault14.2`) containing interdisciplinary research documentation, simulation logs, and utility Python scripts. The primary content is markdown files organized into research domains; the Python scripts are tooling built on top of that content.

## Python Scripts

![](assets/images/1f4a2.png)
![](assets/images/1f4a2.png)
Install dependencies:
```bash
pip install -r requirements.txt
```

![](assets/images/1f4bb.png)
![](assets/images/1f4bb.png)
Run the markdown-to-HTML converter (converts all `.md` files and generates `index.html`):
```bash
python convert_to_html.py
```

![](assets/images/1f4bb.png)
![](assets/images/1f4bb.png)
Run the response prover mock (analyzes `psy-references/mail2fbi.txt` and generates a mock response):
```bash
python response_prover_mock.py
# or with a custom mail file:
python response_prover_mock.py path/to/mail.txt
```

![](assets/images/1f4a2.png)
![](assets/images/1f4a2.png)
Run the grouped-nodes test suite:
```bash
python test_response_prover_grouped_nodes.py
```

## Repository Structure

```
vault14.2/
├── SKYNET/           # Technology & systems research (RF/microwave, nav scanning, text-machine AI)
├── Red&Queen/        # Interdisciplinary research (biology, electronics, linguistics, simulation logs)
│   └── playground/models_queryer/  # sim_log_*.md — LLM query simulation logs used by response_prover_mock.py
├── axis9/            # Core strategic research, issues, planning
├── BMO/              # System/user profiles and configuration
├── Excalidraw/       # Visual diagrams and drawing exports
├── programs/         # Software tools and utilities documentation
├── textgenerator/    # AI text generation templates
├── psy-references/   # Psychological and social research references
├── copilot/          # GitHub Copilot integration notes
├── convert_to_html.py        # Batch MD→HTML converter (embeds images as base64)
├── response_prover_mock.py   # Mock FSB/FSS response generator using verb-logic analysis
├── test_response_prover_grouped_nodes.py  # Tests for the grouped-nodes detection logic
├── requirements.txt           # colorama, gpiozero, rich
└── .obsidian/        # Obsidian app config, plugins, themes (do not edit manually)
```

## Key Architectural Points

![](assets/images/warn.png)
![](assets/images/warn.png)
**`convert_to_html.py`** — `MarkdownToHTMLConverter` class. Walks all `*.md` recursively, embeds images as base64 data URIs, rewrites `.md` links to `.html`, and produces a searchable `index.html`. Hardcoded root path `/home/runner/work/named/named` in `__main__` — update when running locally.

![](assets/images/warn.png)
![](assets/images/warn.png)
**`response_prover_mock.py`** — `ResponseProverMock` class. Loads `psy-references/mail2fbi.txt`, samples up to 10 `sim_log_*.md` files from `Red&Queen/playground/models_queryer/`, runs a verb-logic categorization system (`VerbCategory` enum), and generates a structured mock response. Core decision flow: `_detect_grouped_nodes_scenario()` → grouped-nodes branch or standard APPROVE/DENY branch. Output is printed and also saved to `tmp/response_prover_output_<timestamp>.md`.

![](assets/images/warn.png)
![](assets/images/warn.png)
**Obsidian conventions** — Internal links use `[[wiki-style]]` syntax. Tags are applied via YAML frontmatter or inline `#tag`. The `.obsidian/` directory holds plugin configs (`data.json` per plugin) and themes. Do not commit plugin binary `main.js` files unless intentionally updating a plugin.

## Copilot Instructions

![](assets/images/warn.png)
![](assets/images/warn.png)
From `.github/copilot-instructions.md`: the knowledge system uses a 4-step process (LOAD → ANALYZE with 2–4 random cycles → RELOAD at 51% → OUTPUT) following Red&Queen random shuffle patterns from simulation logs.

## Notes

- Markdown files are bilingual (English and Russian); the Russian README is `README_ru.md`.
- `tracked_files.json` records file tracking metadata for the vault.
- The `expandor.c` file at the root is a C utility; no build system is present for it.
- `root.ipynb` is a Jupyter notebook at the vault root.
