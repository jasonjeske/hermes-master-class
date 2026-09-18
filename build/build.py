#!/usr/bin/env python3
"""Build the masterclass into a single self-contained HTML page.
Reads source.md: YAML frontmatter plus typed fenced blocks."""
import re, sys, base64, html as H, os
from pathlib import Path

SRC   = Path(sys.argv[1])
OUT   = Path(sys.argv[2])
ROOT  = SRC.parent
HERE  = Path(__file__).parent
MERMAID = Path(sys.argv[3]) if len(sys.argv) > 3 else None

raw = SRC.read_text(encoding="utf8")
m = re.match(r'^---\n(.*?)\n---\n', raw, re.S)
meta, body = {}, raw
if m:
    for line in m.group(1).split("\n"):
        if ":" in line and not line.startswith("#"):
            k, v = line.split(":", 1); meta[k.strip()] = v.strip()
    body = raw[m.end():]

MIME = {".png":"image/png",".jpg":"image/jpeg",".jpeg":"image/jpeg",".webp":"image/webp",
        ".gif":"image/gif",".svg":"image/svg+xml"}
_cache = {}
def datauri(rel):
    if rel in _cache: return _cache[rel]
    p = (ROOT / rel).resolve()
    if not p.exists():
        print(f"  ! missing image {rel}", file=sys.stderr); return rel
    uri = f"data:{MIME.get(p.suffix.lower(),'application/octet-stream')};base64," + \
          base64.b64encode(p.read_bytes()).decode()
    _cache[rel] = uri
    return uri

def esc(t): return H.escape(t, quote=False)

def inline(t):
    t = esc(t)
    t = re.sub(r'`([^`]+)`', lambda m: f"<code>{m.group(1)}</code>", t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    return t

def attrs_of(s):
    a = {}
    for mm in re.finditer(r'(\w+)=("([^"]*)"|\S+)', s):
        a[mm.group(1)] = mm.group(3) if mm.group(3) is not None else mm.group(2)
    return a

def render_table(content, at):
    rows = [r for r in content.strip().split("\n") if r.strip()]
    if not rows: return ""
    cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
    head = cells(rows[0]); n = len(head)
    out = ["<div class='tablewrap'><table>"]
    if at.get("title"): out.append(f"<caption>{esc(at['title'])}</caption>")
    out.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>")
    for r in rows[1:]:
        c = cells(r) + [""] * n
        out.append("<tr>" + "".join(f"<td>{inline(x)}</td>" for x in c[:n]) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)

def render_block(kind, attrline, content):
    at = attrs_of(attrline)
    if kind == "table":  return render_table(content, at)
    if kind == "diagram":
        cap = f"<div class='cap'>{esc(at.get('title',''))}</div>" if at.get("title") else ""
        return f"<figure class='figure'>{cap}<div class='mermaid'>{content.strip()}</div></figure>"
    if kind == "callout":
        k = at.get("kind","note"); t = at.get("title","")
        ttl = f"<div class='ct'>{esc(t)}</div>" if t else ""
        paras = "".join(f"<p>{inline(x.strip())}</p>" for x in content.strip().split("\n\n") if x.strip())
        return f"<div class='callout {esc(k)}'>{ttl}{paras}</div>"
    if kind == "checklist":
        items = []
        for l in content.strip().split("\n"):
            l = l.strip()
            if l.startswith("[x]"): items.append(f"<li class='done'>{inline(l[3:].strip())}</li>")
            elif l.startswith("[ ]"): items.append(f"<li>{inline(l[3:].strip())}</li>")
            elif l: items.append(f"<li>{inline(l)}</li>")
        return "<ul class='check'>" + "".join(items) + "</ul>"
    if kind == "data-model":
        rows = [r for r in content.strip().split("\n") if r.strip()]
        out = ["<div class='tablewrap'><table>"]
        if at.get("name"): out.append(f"<caption>{esc(at['name'])}</caption>")
        out.append("<thead><tr><th>Field</th><th>Type</th><th>Notes</th></tr></thead><tbody>")
        for r in rows:
            p = [c.strip() for c in r.split("|")] + ["",""]
            out.append("<tr>" + "".join(f"<td>{inline(x)}</td>" for x in p[:3]) + "</tr>")
        out.append("</tbody></table></div>")
        return "".join(out)
    if kind in ("file-tree","code"):
        f = at.get("file") or at.get("title","")
        fn = f"<div class='fname'>{esc(f)}</div>" if f else ""
        return f"<div class='codeblk'>{fn}<pre><code>{esc(content.rstrip())}</code></pre></div>"
    return f"<div class='codeblk'><pre><code>{esc(content.rstrip())}</code></pre></div>"

# ---- walk the body -------------------------------------------------------
lines = body.split("\n")
out, i = [], 0
sections, sec_open, part_no = [], False, 0
buf_p = []

def flush():
    global buf_p
    if buf_p:
        txt = " ".join(buf_p).strip()
        if txt: out.append(f"<p>{inline(txt)}</p>")
        buf_p = []

list_open = None
def close_list():
    global list_open
    if list_open: out.append(f"</{list_open}>"); list_open = None

while i < len(lines):
    ln = lines[i]
    fm = re.match(r'^```([a-z-]+)(.*)$', ln)
    if fm:
        flush(); close_list()
        kind, attrline = fm.group(1), fm.group(2)
        j = i + 1; blk = []
        while j < len(lines) and not lines[j].startswith("```"):
            blk.append(lines[j]); j += 1
        out.append(render_block(kind, attrline, "\n".join(blk)))
        i = j + 1; continue

    img = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)\s*$', ln)
    if img:
        flush(); close_list()
        alt, src = img.group(1), img.group(2)
        cls = "hero" if "hero" in src else "sec-banner"
        out.append(f"<div class='{cls}'><img src='{datauri(src)}' alt='{esc(alt)}'></div>")
        i += 1; continue

    h2 = re.match(r'^## (.+)$', ln)
    if h2:
        flush(); close_list()
        if sec_open: out.append("</section>")
        title = h2.group(1).strip()
        sid = re.sub(r'[^a-z0-9]+','-', title.lower()).strip('-')
        sections.append((title, sid))
        out.append(f"<section id='{sid}'>")
        sec_open = True
        out.append(f"<h2><span class='num'>{esc(title.split(':')[0] if ':' in title else 'Section')}</span>{esc(title.split(':',1)[1].strip() if ':' in title else title)}</h2>")
        i += 1; continue

    h3 = re.match(r'^### (.+)$', ln)
    if h3:
        flush(); close_list()
        t = h3.group(1).strip()
        hid = re.sub(r'[^a-z0-9]+','-', t.lower()).strip('-')
        out.append(f"<h3 id='{hid}'>{inline(t)}</h3>")
        i += 1; continue

    if re.match(r'^\s*[-*] ', ln):
        flush()
        if list_open != "ul": close_list(); out.append("<ul>"); list_open = "ul"
        item = re.sub(r'^\s*[-*] ', '', ln)
        out.append("<li>" + inline(item) + "</li>"); i += 1; continue
    if re.match(r'^\s*\d+\. ', ln):
        flush()
        if list_open != "ol": close_list(); out.append("<ol>"); list_open = "ol"
        item = re.sub(r'^\s*\d+\. ', '', ln)
        out.append("<li>" + inline(item) + "</li>"); i += 1; continue
    if ln.strip().startswith("> "):
        flush(); close_list()
        out.append(f"<div class='callout'><p>{inline(ln.strip()[2:])}</p></div>"); i += 1; continue
    if ln.strip() == "---":
        flush(); close_list(); out.append("<hr>"); i += 1; continue
    if not ln.strip():
        flush(); close_list(); i += 1; continue
    buf_p.append(ln.strip()); i += 1

flush(); close_list()
if sec_open: out.append("</section>")

PRINT = os.environ.get("MC_PRINT") == "1"
css = (HERE / ("print.css" if PRINT else "style.css")).read_text(encoding="utf8")
mer = MERMAID.read_text(encoding="utf8") if MERMAID and MERMAID.exists() else ""

PAL = dict(FS="15pt", MBG="#f5f7fa", MPRI="#e8eef6", MTXT="#10151f", MBRD="#1668a8",
           MSEC="#dce6f0", MTER="#eef2f7", MLINE="#3d7ea8", MCLU="rgba(22,104,168,.05)",
           MCLB="rgba(22,104,168,.25)", MTTL="#8a6410") if PRINT else \
      dict(FS="17px", MBG="#0e1118", MPRI="#141c2b", MTXT="#e9eef6", MBRD="#4db6f0",
           MSEC="#16202f", MTER="#101722", MLINE="#5fa8d8", MCLU="rgba(77,182,240,.05)",
           MCLB="rgba(120,160,210,.30)", MTTL="#e3b23c")
title = meta.get("title","Document")
doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<style>{css}</style></head><body>
<div class="progress" id="prog"></div>
<div class="wrap">
<header class="mast">
  <div class="kicker">{esc(meta.get('eyebrow','Documentation'))}</div>
  <h1>{esc(title)}</h1>
  <p class="sub">{esc(meta.get('subtitle',''))}</p>
  <div class="why"><b>Why this exists:</b> {esc(meta.get('why',''))}</div>
</header>
{"".join(out)}
</div>
<!-- Bundled: Mermaid (MIT), https://github.com/mermaid-js/mermaid . See THIRD-PARTY-NOTICES.md -->
<script>{mer}</script>
<script>
(function(){{
  if(window.mermaid){{
    mermaid.initialize({{
      startOnLoad:false, securityLevel:"loose", theme:"base",
      flowchart:{{curve:"basis", nodeSpacing:54, rankSpacing:64, padding:14, useMaxWidth:true}},
      themeVariables:{{
        fontFamily:'"Inter","SF Pro Text",-apple-system,sans-serif', fontSize:"{PAL['FS']}",
        background:"{PAL['MBG']}",
        primaryColor:"{PAL['MPRI']}", primaryTextColor:"{PAL['MTXT']}", primaryBorderColor:"{PAL['MBRD']}",
        secondaryColor:"{PAL['MSEC']}", secondaryTextColor:"{PAL['MTXT']}", secondaryBorderColor:"{PAL['MBRD']}",
        tertiaryColor:"{PAL['MTER']}", tertiaryTextColor:"{PAL['MTXT']}", tertiaryBorderColor:"{PAL['MBRD']}",
        lineColor:"{PAL['MLINE']}", textColor:"{PAL['MTXT']}",
        mainBkg:"{PAL['MPRI']}", nodeBorder:"{PAL['MBRD']}", clusterBkg:"{PAL['MCLU']}",
        clusterBorder:"{PAL['MCLB']}", edgeLabelBackground:"{PAL['MBG']}",
        titleColor:"{PAL['MTTL']}", nodeTextColor:"{PAL['MTXT']}"
      }}
    }});
    mermaid.run({{querySelector:".mermaid"}});
  }}
  var p=document.getElementById("prog");
  addEventListener("scroll", function(){{
    var h=document.documentElement;
    p.style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+"%";
  }}, {{passive:true}});
}})();
</script>
</body></html>"""
OUT.write_text(doc, encoding="utf8")
print(f"built {OUT}  ({len(doc)/1024/1024:.2f} MB)  sections={len(sections)}  images={len(_cache)}")
