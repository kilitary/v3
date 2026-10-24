<?php
/**
 * render.php — Markdown renderer for vault14.2
 *
 * Usage:
 *   render.php            → directory listing of all .md files
 *   render.php?f=README.md
 *   render.php?f=axis9/axis9.md
 *
 * All .md links inside documents are automatically rewritten to point back
 * through this renderer.
 */

define('VAULT_ROOT', __DIR__);
define('SELF',       basename(__FILE__));

// ── Security: restrict to VAULT_ROOT ─────────────────────────────────────────

function safe_path(string $rel): string|false {
    $abs = realpath(VAULT_ROOT . DIRECTORY_SEPARATOR . ltrim($rel, '/\\'));
    if ($abs === false) return false;
    if (strncmp($abs, VAULT_ROOT, strlen(VAULT_ROOT)) !== 0) return false;
    if (!is_file($abs)) return false;
    return $abs;
}

// ── Markdown → HTML renderer ──────────────────────────────────────────────────

function render_md(string $md, string $base_dir): string {
    $lines  = explode("\n", str_replace("\r\n", "\n", $md));
    $html   = '';
    $i      = 0;
    $n      = count($lines);

    while ($i < $n) {
        $line = $lines[$i];

        // Fenced code block
        if (preg_match('/^(`{3,}|~{3,})(\w*)/', $line, $m)) {
            $fence = $m[1];
            $lang  = htmlspecialchars($m[2]);
            $code  = '';
            $i++;
            while ($i < $n && strncmp($lines[$i], $fence, strlen($fence)) !== 0) {
                $code .= htmlspecialchars($lines[$i]) . "\n";
                $i++;
            }
            $lang_attr = $lang ? " class=\"language-$lang\"" : '';
            $html .= "<pre><code$lang_attr>$code</code></pre>\n";
            $i++;
            continue;
        }

        // Horizontal rule
        if (preg_match('/^(\*{3,}|-{3,}|_{3,})\s*$/', $line)) {
            $html .= "<hr>\n";
            $i++;
            continue;
        }

        // Setext heading (=== or ---)
        if ($i + 1 < $n) {
            if (preg_match('/^=+\s*$/', $lines[$i + 1]) && trim($line) !== '') {
                $html .= '<h1>' . inline($line, $base_dir) . "</h1>\n";
                $i += 2;
                continue;
            }
            if (preg_match('/^-+\s*$/', $lines[$i + 1]) && trim($line) !== '') {
                $html .= '<h2>' . inline($line, $base_dir) . "</h2>\n";
                $i += 2;
                continue;
            }
        }

        // ATX heading
        if (preg_match('/^(#{1,6})\s+(.+?)(?:\s+#+)?\s*$/', $line, $m)) {
            $level = strlen($m[1]);
            $html .= "<h$level>" . inline($m[2], $base_dir) . "</h$level>\n";
            $i++;
            continue;
        }

        // Blockquote
        if (preg_match('/^>\s?(.*)/', $line, $m)) {
            $bq = '';
            while ($i < $n && preg_match('/^>\s?(.*)/', $lines[$i], $bm)) {
                $bq .= $bm[1] . "\n";
                $i++;
            }
            $html .= '<blockquote>' . render_md($bq, $base_dir) . "</blockquote>\n";
            continue;
        }

        // Unordered list
        if (preg_match('/^(\s*)([-*+])\s+(.+)/', $line, $m)) {
            $indent = strlen($m[1]);
            $html  .= "<ul>\n";
            while ($i < $n && preg_match('/^(\s*)([-*+])\s+(.+)/', $lines[$i], $lm)
                            && strlen($lm[1]) === $indent) {
                $task = '';
                $text = $lm[3];
                if (preg_match('/^\[( |x)\]\s+(.+)/i', $text, $tm)) {
                    $checked = strtolower($tm[1]) === 'x' ? ' checked' : '';
                    $task = "<input type=\"checkbox\"$checked disabled> ";
                    $text = $tm[2];
                }
                $html .= '  <li>' . $task . inline($text, $base_dir) . "</li>\n";
                $i++;
            }
            $html .= "</ul>\n";
            continue;
        }

        // Ordered list
        if (preg_match('/^(\s*)\d+[.)]\s+(.+)/', $line, $m)) {
            $indent = strlen($m[1]);
            $html  .= "<ol>\n";
            while ($i < $n && preg_match('/^(\s*)\d+[.)]\s+(.+)/', $lines[$i], $lm)
                            && strlen($lm[1]) === $indent) {
                $html .= '  <li>' . inline($lm[2], $base_dir) . "</li>\n";
                $i++;
            }
            $html .= "</ol>\n";
            continue;
        }

        // Table (pipe-delimited)
        if (strpos($line, '|') !== false && $i + 1 < $n
                && preg_match('/^\|?[\s\-:]+\|/', $lines[$i + 1])) {
            $html .= "<table>\n<thead>\n<tr>";
            foreach (parse_table_row($line) as $cell)
                $html .= '<th>' . inline($cell, $base_dir) . '</th>';
            $html .= "</tr>\n</thead>\n<tbody>\n";
            $i += 2; // skip separator row
            while ($i < $n && strpos($lines[$i], '|') !== false) {
                $html .= '<tr>';
                foreach (parse_table_row($lines[$i]) as $cell)
                    $html .= '<td>' . inline($cell, $base_dir) . '</td>';
                $html .= "</tr>\n";
                $i++;
            }
            $html .= "</tbody>\n</table>\n";
            continue;
        }

        // YAML front-matter (skip)
        if ($i === 0 && $line === '---') {
            $i++;
            while ($i < $n && $lines[$i] !== '---') $i++;
            $i++;
            continue;
        }

        // Blank line
        if (trim($line) === '') {
            $i++;
            continue;
        }

        // Paragraph — collect until blank line or block element
        $para = '';
        while ($i < $n && trim($lines[$i]) !== ''
               && !preg_match('/^(#{1,6}\s|[-*+]\s|\d+[.)]\s|>|`{3}|~{3}|={3,}|-{3,})/', $lines[$i])) {
            $para .= ($para ? ' ' : '') . $lines[$i];
            $i++;
        }
        if ($para !== '') {
            $html .= '<p>' . inline($para, $base_dir) . "</p>\n";
        }
    }

    return $html;
}

function parse_table_row(string $row): array {
    $row = trim($row, "| \t");
    return array_map('trim', explode('|', $row));
}

function inline(string $text, string $base_dir): string {
    // Inline code
    $text = preg_replace('/`([^`]+)`/', '<code>$1</code>', $text);

    // Bold + italic
    $text = preg_replace('/\*\*\*(.+?)\*\*\*/', '<strong><em>$1</em></strong>', $text);
    $text = preg_replace('/___(.+?)___/', '<strong><em>$1</em></strong>', $text);
    $text = preg_replace('/\*\*(.+?)\*\*/', '<strong>$1</strong>', $text);
    $text = preg_replace('/__(.+?)__/', '<strong>$1</strong>', $text);
    $text = preg_replace('/\*(.+?)\*/', '<em>$1</em>', $text);
    $text = preg_replace('/_([^_]+)_/', '<em>$1</em>', $text);

    // Strikethrough
    $text = preg_replace('/~~(.+?)~~/', '<del>$1</del>', $text);

    // Images  ![alt](src)
    $text = preg_replace_callback('/!\[([^\]]*)\]\(([^)]+)\)/', function($m) use ($base_dir) {
        $alt = htmlspecialchars($m[1]);
        $src = $m[2];
        if (!preg_match('/^https?:\/\/|^data:/', $src)) {
            $abs = realpath($base_dir . '/' . $src);
            // serve local image as base64 if small enough
            if ($abs && is_file($abs) && filesize($abs) < 2 * 1024 * 1024) {
                $mime = mime_content_type($abs) ?: 'image/png';
                $b64  = base64_encode(file_get_contents($abs));
                $src  = "data:$mime;base64,$b64";
            }
        }
        return "<img src=\"" . htmlspecialchars($src) . "\" alt=\"$alt\">";
    }, $text);

    // Obsidian wiki-links  [[page]]  [[page|alias]]
    $text = preg_replace_callback('/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/', function($m) use ($base_dir) {
        $target = trim($m[1]);
        $alias  = isset($m[2]) ? trim($m[2]) : $target;
        $href   = relink($target . '.md', $base_dir);
        return '<a href="' . htmlspecialchars($href) . '">' . htmlspecialchars($alias) . '</a>';
    }, $text);

    // Standard links  [text](url)
    $text = preg_replace_callback('/\[([^\]]+)\]\(([^)]+)\)/', function($m) use ($base_dir) {
        $label = $m[1];
        $href  = $m[2];
        if (preg_match('/\.md(#[^)]*)?$/', $href)) {
            $href = relink($href, $base_dir);
        }
        return '<a href="' . htmlspecialchars($href) . '">' . htmlspecialchars($label) . '</a>';
    }, $text);

    // Bare URLs
    $text = preg_replace(
        '/(?<!["\'=>])(https?:\/\/[^\s<>"\']+)/',
        '<a href="$1" target="_blank" rel="noopener">$1</a>',
        $text
    );

    return $text;
}

/**
 * Rewrite a .md path (possibly relative to $base_dir) into a render.php URL.
 * Preserves any #anchor fragment.
 */
function relink(string $md_path, string $base_dir): string {
    $fragment = '';
    if (preg_match('/^(.+?)(#[^)#]*)$/', $md_path, $fm)) {
        $md_path  = $fm[1];
        $fragment = $fm[2];
    }

    // Absolute URL — leave alone
    if (preg_match('/^https?:\/\//', $md_path)) return $md_path . $fragment;

    // Resolve relative to base_dir, then make relative to VAULT_ROOT
    $abs = realpath($base_dir . '/' . $md_path);
    if ($abs && strncmp($abs, VAULT_ROOT, strlen(VAULT_ROOT)) === 0) {
        $rel = ltrim(str_replace('\\', '/', substr($abs, strlen(VAULT_ROOT))), '/');
        return SELF . '?f=' . rawurlencode($rel) . $fragment;
    }

    // Fallback: keep original
    return $md_path . $fragment;
}

// ── Directory listing ─────────────────────────────────────────────────────────

function dir_listing(): string {
    $files = [];
    $it = new RecursiveIteratorIterator(
        new RecursiveDirectoryIterator(VAULT_ROOT, FilesystemIterator::SKIP_DOTS)
    );
    foreach ($it as $f) {
        if (strtolower($f->getExtension()) !== 'md') continue;
        $rel = ltrim(str_replace('\\', '/', substr($f->getPathname(), strlen(VAULT_ROOT))), '/');
        if (str_starts_with($rel, '.obsidian/')) continue;
        $files[] = $rel;
    }
    sort($files);

    // Group by top-level directory
    $groups = [];
    foreach ($files as $rel) {
        $parts = explode('/', $rel, 2);
        $group = count($parts) > 1 ? $parts[0] : '(root)';
        $groups[$group][] = $rel;
    }
    ksort($groups);

    $html = '<div class="listing">';
    foreach ($groups as $group => $group_files) {
        $html .= '<details open><summary>' . htmlspecialchars($group) . ' <span class="cnt">(' . count($group_files) . ')</span></summary><ul>';
        foreach ($group_files as $rel) {
            $label = basename($rel, '.md');
            $href  = SELF . '?f=' . rawurlencode($rel);
            $html .= '<li><a href="' . htmlspecialchars($href) . '">' . htmlspecialchars($label) . '</a></li>';
        }
        $html .= '</ul></details>';
    }
    $html .= '</div>';
    return $html;
}

// ── Breadcrumb ────────────────────────────────────────────────────────────────

function breadcrumb(string $rel): string {
    $parts = explode('/', $rel);
    $html  = '<nav class="bread"><a href="' . SELF . '">vault</a>';
    $acc   = '';
    foreach ($parts as $idx => $part) {
        $acc .= ($acc ? '/' : '') . $part;
        if ($idx < count($parts) - 1) {
            // intermediate dirs — link to listing with search pre-filled
            $html .= ' / <a href="' . SELF . '?q=' . rawurlencode($part) . '">' . htmlspecialchars($part) . '</a>';
        } else {
            $html .= ' / <span>' . htmlspecialchars(basename($part, '.md')) . '</span>';
        }
    }
    return $html . '</nav>';
}

// ── HTML shell ────────────────────────────────────────────────────────────────

function page(string $title, string $body, string $extra_head = ''): void {
    echo <<<HTML
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{$title}</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#161b22;--border:#21262d;
  --text:#c9d1d9;--dim:#8b949e;--link:#58a6ff;--head:#e6edf3;
  --code-bg:#1c2128;--accent:#388bfd;
}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  background:var(--bg);color:var(--text);line-height:1.65;min-height:100vh;display:flex;flex-direction:column}
a{color:var(--link);text-decoration:none}
a:hover{text-decoration:underline}

/* layout */
#wrap{display:flex;flex:1;max-width:1400px;width:100%;margin:0 auto;padding:0 16px}
#sidebar{width:260px;flex-shrink:0;padding:24px 0;position:sticky;top:0;height:100vh;
  overflow-y:auto;border-right:1px solid var(--border)}
#content{flex:1;padding:32px 40px;max-width:900px}

/* topbar */
#topbar{background:var(--surface);border-bottom:1px solid var(--border);
  padding:10px 24px;display:flex;align-items:center;gap:16px}
#topbar a.logo{font-weight:700;color:var(--head);font-size:1rem}
#search-box{flex:1;max-width:400px;padding:6px 12px;background:var(--bg);
  border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:.85rem;outline:none}
#search-box:focus{border-color:var(--accent)}

/* sidebar listing */
.listing details{margin-bottom:6px}
.listing summary{cursor:pointer;padding:4px 8px;border-radius:4px;
  font-size:.8rem;font-weight:600;color:var(--dim);user-select:none;list-style:none}
.listing summary:hover{color:var(--head)}
.listing summary .cnt{font-weight:400;color:#484f58}
.listing ul{list-style:none;padding-left:14px;border-left:1px solid var(--border);margin:2px 0 4px 10px}
.listing li{margin:1px 0}
.listing li a{font-size:.8rem;color:var(--dim);display:block;padding:2px 6px;border-radius:3px}
.listing li a:hover{color:var(--link);text-decoration:none;background:var(--surface)}
.listing li a.active{color:var(--link);background:var(--surface)}

/* breadcrumb */
.bread{font-size:.78rem;color:var(--dim);margin-bottom:20px}
.bread a{color:var(--dim)}
.bread span{color:var(--head)}

/* markdown content */
#md h1,#md h2,#md h3,#md h4,#md h5,#md h6{color:var(--head);margin:1.4em 0 .5em;line-height:1.25}
#md h1{font-size:1.8rem;border-bottom:1px solid var(--border);padding-bottom:.4em}
#md h2{font-size:1.35rem;border-bottom:1px solid var(--border);padding-bottom:.3em}
#md h3{font-size:1.1rem}
#md p{margin:.7em 0}
#md ul,#md ol{padding-left:1.8em;margin:.5em 0}
#md li{margin:.2em 0}
#md blockquote{border-left:3px solid var(--border);padding:4px 16px;color:var(--dim);margin:.7em 0}
#md pre{background:var(--code-bg);border:1px solid var(--border);border-radius:6px;
  padding:16px;overflow-x:auto;margin:.8em 0}
#md code{background:var(--code-bg);padding:.15em .4em;border-radius:3px;font-size:.88em;font-family:'Courier New',monospace}
#md pre code{background:none;padding:0;font-size:.85em}
#md table{border-collapse:collapse;width:100%;margin:.8em 0}
#md th,#md td{border:1px solid var(--border);padding:6px 12px;font-size:.88rem}
#md th{background:var(--surface);color:var(--head);font-weight:600}
#md tr:nth-child(even) td{background:#0d1117}
#md hr{border:none;border-top:1px solid var(--border);margin:1.5em 0}
#md img{max-width:100%;border-radius:4px;margin:.5em 0}
#md input[type=checkbox]{margin-right:5px}
#md del{color:var(--dim)}

@media(max-width:768px){
  #sidebar{display:none}
  #content{padding:20px 16px}
}
</style>
{$extra_head}
</head>
<body>
<div id="topbar">
  <a class="logo" href="<?= SELF ?>">&#128196; vault14.2</a>
  <input id="search-box" type="text" placeholder="Filter files&hellip;" autocomplete="off">
</div>
<div id="wrap">
  <aside id="sidebar"><?= dir_listing() ?></aside>
  <main id="content">{$body}</main>
</div>
<script>
const sb = document.getElementById('search-box');
sb.addEventListener('input', () => {
  const q = sb.value.trim().toLowerCase();
  document.querySelectorAll('.listing li').forEach(li => {
    li.style.display = (!q || li.textContent.toLowerCase().includes(q)) ? '' : 'none';
  });
  document.querySelectorAll('.listing details').forEach(d => {
    const visible = d.querySelectorAll('li[style=""]').length || !q;
    const any = [...d.querySelectorAll('li')].some(l => l.style.display !== 'none');
    d.style.display = any ? '' : 'none';
  });
});
// highlight active link
const cur = location.search;
document.querySelectorAll('.listing li a').forEach(a => {
  if (a.getAttribute('href') && location.href.endsWith(a.getAttribute('href'))) a.classList.add('active');
});
</script>
</body>
</html>
HTML;
}

// ── Router ────────────────────────────────────────────────────────────────────

$requested = isset($_GET['f']) ? trim($_GET['f'], '/\\') : '';

if ($requested === '') {
    // Index / directory listing
    ob_start();
    echo '<h1 style="color:var(--head);margin-bottom:16px">vault14.2</h1>';
    echo '<p style="color:var(--dim);margin-bottom:24px">Select a document from the sidebar or use the search box above.</p>';
    echo dir_listing();
    $body = ob_get_clean();
    page('vault14.2', $body);
    exit;
}

// Validate and load file
$abs = safe_path($requested);
if ($abs === false) {
    http_response_code(404);
    page('Not found', '<h1>404</h1><p style="color:var(--dim)">File not found or outside vault root: <code>' . htmlspecialchars($requested) . '</code></p>');
    exit;
}

$md       = file_get_contents($abs);
$base_dir = dirname($abs);
$rendered = render_md($md, $base_dir);
$title    = htmlspecialchars(basename($requested, '.md')) . ' — vault14.2';
$bc       = breadcrumb($requested);

page($title, $bc . '<div id="md">' . $rendered . '</div>');
