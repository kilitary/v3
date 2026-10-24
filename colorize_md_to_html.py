#!/usr/bin/env python3
"""
colorize_md_to_html.py
======================
A markdown-to-HTML converter that gives every content element a **random,
kid-fest-color** — bright, playful, carnival-style hues — while keeping
all backgrounds white and using a terminal/monospace font family for a
clean, console-like reading experience.

Usage
-----
    python colorize_md_to_html.py <input.md> [<output.html>]

* If <output.html> is omitted, `<input>.html` is written next to the markdown.
* Pass `--all` instead of a single file to convert every ``.md`` under the
  current directory tree (skips ``.obsidian/`` and ``.git/``).
* Pass `--seed N` to get reproducible colours (handy for testing).

Example
-------
    python colorize_md_to_html.py example_kidfest.md
    python colorize_md_to_html.py --all --seed 42
"""

from __future__ import annotations

import argparse
import random
import re
import sys
from pathlib import Path

import markdown

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------

# A carnival of bright, kid-friendly hex colours — no yellow, cyan, or orange.
KID_FEST_PALETTE = [
    "#C70039",  # fuchsia
    "#9B5DE8",  # violet
    "#7B61FF",  # royal purple
    "#843b62",  # raspberry
    "#B660A6",  # orchid
    "#416EB4",  # sapphire
    "#6A0572",  # deep purple
    "#2E7D32",  # forest green
]

# Dark variants for text that needs to sit on a light background.
KID_FEST_DARK = [
    "#843b62",  # raspberry
    "#416EB4",  # sapphire
    "#2D2942",  # dark purple
    "#1A535C",  # deep teal (dark accent, not cyan-bright)
]

_FONT_STACK = (
    "ui-monospace, 'Cascadia Code', 'Fira Code', "
    "'SFMono-Regular', 'Menlo', 'Consolas', "
    "'Ubuntu Mono', 'Source Code Pro', monospace"
)


def random_kid_color(rng: random.Random) -> str:
    """Pick a random bright colour from the kid-fest palette."""
    return rng.choice(KID_FEST_PALETTE)


def random_dark_color(rng: random.Random) -> str:
    """Pick a random darker colour (for contrast on light backgrounds)."""
    return rng.choice(KID_FEST_DARK)


def hash_to_rng(seed: object) -> random.Random:
    """Create a deterministic RNG from *any* hashable seed."""
    return random.Random(seed)


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* Kid-fest colors on a white terminal-style background */
        body {{
            font-family: {_font};
            line-height: 1.6;
            max-width: 960px;
            margin: 0 auto;
            padding: 30px;
            background: {body_bg};
            color: #222;
            overflow-x: hidden;
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-family: {_font};
            font-weight: 800;
            letter-spacing: 0.03em;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
            text-shadow: 3px 3px 0 rgba(0,0,0,0.08);
        }}
        a {{
            color: {link_color};
            text-decoration:  dotted {link_color_2};
            text-decoration-thickness: 2px;
            transition: all 0.2s ease;
        }}
        a:hover {{
            transform: scale(1.05) rotate(1deg);
            color: {link_hover};
            text-shadow: 2px 2px 0 rgba(0,0,0,0.1);
        }}
        p {{
            margin: 0.8em 0;
        }}
        ul, ol {{
            margin: 0.5em 0;
            padding-left: 1.8em;
        }}
        li {{
            margin: 0.3em 0;
        }}
        blockquote {{
            border-left: 6px solid {quote_border};
            padding: 0.4em 1.2em;
            margin: 1em 0;
            background: {quote_bg};
            font-style: italic;
            border-radius: 0 8px 8px 0;
        }}
        code {{
            background: {code_bg};
            padding: 0.15em 0.5em;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            color: {code_color};
        }}
        pre {{
            background: {pre_bg};
            padding: 1em;
            border-radius: 8px;
            overflow-x: auto;
            border: 3px dotted {pre_border};
        }}
        pre code {{
            background: transparent;
            padding: 0;
            color: inherit;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}
        th {{
            background: {th_bg};
            padding: 8px 12px;
            border: 2px solid {th_border};
            font-weight: bold;
        }}
        td {{
            padding: 8px 12px;
            border: 1px dashed {td_border};
        }}
        tr:nth-child(odd) td {{
            background: {tr_odd};
        }}
        tr:nth-child(even) td {{
            background: {tr_even};
        }}
        hr {{
            border: 4px solid {hr_color};
            background: transparent;
            margin: 1.5em 0;
            border-radius: 2px;
        }}
        img {{
            max-width: 90%;
            border: 6px solid {img_border};
            border-radius: 12px;
            margin: 1em 0;
        }}
        .back-link {{
            display: inline-block;
            margin-bottom: 1.5em;
            padding: 8px 16px;
            background: {back_bg};
            border-radius: 20px;
            color: {back_color};
            font-weight: bold;
        }}
        .confetti {{
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            z-index: -1;
        }}
    </style>
</head>
<body>
    <div class="confetti" id="confetti"></div>
    <a href="javascript:history.back()" class="back-link">← {back_text}</a>
    {html_body}
    <script>
        // Sprinkle animated confetti that matches the kid-fest palette
        (function() {{
            const colors = ["#9B5DE8","#7B61FF","#843b62","#B660A6","#416EB4","#6A0572","#2E7D32"];
            const confetti = document.getElementById('confetti');
            const count = 120;
            for (let i = 0; i < count; i++) {{
                const el = document.createElement('div');
                const size = Math.random() * 8 + 4;
                el.style.cssText =
                    'position:absolute;left:'+Math.random()*100+'vw+top:'+Math.random()*100+'vh+'+
                    'width:'+size+'px;height:'+size+'px;background:'+colors[Math.floor(Math.random()*colors.length)]+
                    ';border-radius:'+(Math.random()>0.5?'50%':'0')+';'+
                    'animation:float '+Math.random()*5+3+'s linear infinite;opacity:0.7';
                el.style.transform = 'rotate('+Math.random()*360+'deg)';
                confetti.appendChild(el);
            }}
            const style = document.createElement('style');
            style.textContent = '@keyframes float {{ 0% {{ transform: translateY(0) rotate(0deg); }} 100% {{ transform: translateY(-120px) rotate(720deg); }} }}';
            document.head.appendChild(style);
        }})();
    </script>
</body>
</html>"""


def _escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------
# The converter
# ---------------------------------------------------------------------------


class ColorizedMDToHTML:
    """Convert a markdown string or file to a kid-fest-colorized HTML document."""

    def __init__(self, seed: object | None = None):
        self.rng = random.Random(seed)

    # -- public API --------------------------------------------------------

    def convert_file(self, md_path: Path, out_path: Path | None = None) -> Path:
        """Convert a single ``*.md`` file and write the HTML result.

        Returns the path to the written HTML file.
        """
        md_text = md_path.read_text(encoding="utf-8", errors="ignore")
        html = self.convert_text(md_text, title=md_path.stem)

        if out_path is None:
            out_path = md_path.with_suffix(".html")
        out_path.write_text(html, encoding="utf-8")
        return out_path

    def convert_text(self, md_text: str, title: str = "Kid-Fest Document") -> str:
        """Convert a markdown *string* to a colorized HTML document string."""
        # Convert markdown → HTML body
        md = markdown.Markdown(
            extensions=["extra", "codehilite", "toc", "tables", "sane_lists"]
        )
        html_body = md.convert(md_text)

        # Inject random colours into every content element
        html_body = self._colorize(html_body)

        # Build the full document
        return self._build_document(html_body, title)

    # -- colorisation ------------------------------------------------------

    def _colorize(self, html: str) -> str:
        """Walk the HTML body and inject kid-fest colours onto elements."""

        # We process the HTML with simple tag-aware regex passes.
        # Each element type gets its own random colour so no two headings
        # (or paragraphs, or list items) share the same hue.

        # --- Headings ---
        for level in range(1, 7):
            tag = f"h{level}"
            html = self._colorize_tag(html, tag, is_heading=True)

        # --- Paragraphs ---
        html = self._colorize_tag(html, "p")

        # --- List items ---
        html = self._colorize_tag(html, "li")

        # --- Table cells ---
        html = self._colorize_tag(html, "th")
        html = self._colorize_tag(html, "td")

        # --- Blockquotes (colour the border) ---
        html = self._colorize_tag(html, "blockquote")

        # --- Inline code ---
        html = self._colorize_tag(html, "code")

        # pattern_link_end = re.compile(
        #     ,
        #     re.DOTALL | re.IGNORECASE,
        # )
        html, num_subn = re.subn(
            r"(\.md)", ".html", html, 8888, re.DOTALL | re.IGNORECASE
        )
        print(f"num_n: {num_subn}")

        return html

    def _colorize_tag(self, html: str, tag: str, is_heading: bool = False) -> str:
        """Wrap every occurrence of ``<tag>…</tag>`` with an inline style
        carrying a random kid-fest colour on text/borders (backgrounds
        stay white per the terminal colouring policy)."""

        colour = random_kid_color(self.rng)
        dark = random_dark_color(self.rng)

        pattern = re.compile(
            rf"<{tag}(\s[^>]*)?>(.*?)</{tag}>",
            re.DOTALL | re.IGNORECASE,
        )

        def _replace(match: re.Match) -> str:
            existing_attrs = match.group(1) or ""
            inner = match.group(2)

            if is_heading:
                # Headings get a random dark text colour + coloured dashed underline
                style = f' style="color:{dark};border-bottom:1px dashed {colour};padding-bottom:4px;"'
            elif tag == "blockquote":
                # Coloured border only — white background
                style = f' style="border-color:{colour};"'
            elif tag == "code":
                # Coloured text on white bg with coloured border
                style = f' style="color:{dark};background:#fafafa;border:1px solid {colour};"'
            elif tag in ("th", "td"):
                if tag == "th":
                    # White header bg, coloured text + border
                    style = f' style="background:#ffffff;color:{colour};border-color:{dark};"'
                else:
                    # White cell bg
                    style = f' style="background:#ffffff;"'
            else:
                # paragraphs, list items — random text colour on white
                style = f' style="color:{colour};"'

            return f"<{tag}{existing_attrs}{style}>{inner}</{tag}>"

        # re.sub with a function; count is fine for any number of matches
        return pattern.sub(_replace, html)

    # -- document assembly --------------------------------------------------

    def _build_document(self, html_body: str, title: str) -> str:
        # --- Random text/border colours (backgrounds are always white) ---
        link_c = random_kid_color(self.rng)
        link_hover = random_kid_color(self.rng)
        quote_border = random_kid_color(self.rng)
        code_color = random_dark_color(self.rng)
        pre_border = random_kid_color(self.rng)
        th_border = random_dark_color(self.rng)
        td_border = random_kid_color(self.rng)
        hr_color = random_kid_color(self.rng)
        img_border = random_kid_color(self.rng)
        back_color = random_dark_color(self.rng)

        # --- Fixed white / near-white backgrounds ---
        body_bg = "#ffffff"
        quote_bg = "#fafafa"
        code_bg = "#fafafa"
        pre_bg = "#fafafa"
        th_bg = "#ffffff"
        tr_odd = "#ffffff"
        tr_even = "#fafafa"
        back_bg = "#ffffff"

        return _HTML_TEMPLATE.format(
            title=title,
            _font=_FONT_STACK,
            body_bg=body_bg,
            link_color=link_c,
            link_color_2=link_hover,
            link_hover=link_hover,
            quote_border=quote_border,
            quote_bg=quote_bg,
            code_bg=code_bg,
            code_color=code_color,
            pre_bg=pre_bg,
            pre_border=pre_border,
            th_bg=th_bg,
            th_border=th_border,
            td_border=td_border,
            tr_odd=tr_odd,
            tr_even=tr_even,
            hr_color=hr_color,
            img_border=img_border,
            back_bg=back_bg,
            back_color=back_color,
            back_text=title,
            html_body=html_body,
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def convert_directory(root: Path, seed: object | None = None):
    """Recursively convert every ``.md`` under *root* to colorised HTML."""
    converter = ColorizedMDToHTML(seed=seed)
    md_files = [
        p
        for p in root.rglob("*.md")
        if ".obsidian" not in p.parts and ".git" not in p.parts
    ]
    print(f"Found {len(md_files)} markdown files to colorize …")
    for i, md_file in enumerate(md_files, 1):
        if i % 50 == 0:
            print(f"  … {i}/{len(md_files)} done")
        try:
            out = converter.convert_file(md_file)
            print(f"  ✓ {md_file.relative_to(root)} → {out.name}")
        except Exception as exc:
            print(f"  ✗ {md_file}: {exc}", file=sys.stderr)
    print("Done — kid-fest explosion complete! 🎉")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert markdown to HTML with kid-fest random colours.",
    )
    parser.add_argument("input", nargs="?", help="Markdown file to convert")
    parser.add_argument(
        "output", nargs="?", help="Output HTML path (default: <input>.html)"
    )
    parser.add_argument(
        "--all", action="store_true", help="Convert every .md in the current tree"
    )
    parser.add_argument(
        "--root", default=".", help="Root directory when using --all (default: .)"
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducible colours"
    )
    args = parser.parse_args(argv)

    if args.all:
        convert_directory(Path(args.root), seed=args.seed)
        return 0

    if not args.input:
        parser.error("provide a markdown file or use --all")

    md_path = Path(args.input)
    if not md_path.exists():
        parser.error(f"file not found: {md_path}")

    out_path = Path(args.output) if args.output else None
    converter = ColorizedMDToHTML(seed=args.seed)
    result = converter.convert_file(md_path, out_path)
    print(f"✓ {md_path} → {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
