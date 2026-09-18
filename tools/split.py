import re, os
c = open('/tmp/mc-converted.md', encoding='utf8').read().strip()

# Split on top-level "## " but ONLY outside fenced code blocks.
lines = c.split('\n')
fence = False
idxs = []
for i, l in enumerate(lines):
    if l.startswith('```'):
        fence = not fence
        continue
    if not fence and l.startswith('## '):
        idxs.append(i)

lead = '\n'.join(lines[:idxs[0]]).strip()
chunks = []
for n, start in enumerate(idxs):
    end = idxs[n+1] if n+1 < len(idxs) else len(lines)
    chunks.append('\n'.join(lines[start:end]).strip())

def fname(title, order):
    m = re.match(r'Part (\d+):\s*(.+)', title)
    if m:
        return "part-%02d-%s.md" % (int(m.group(1)), re.sub(r'[^a-z0-9]+','-',m.group(2).lower()).strip('-'))
    m = re.match(r'Appendix ([A-Z]):\s*(.+)', title)
    if m:
        return "appendix-%s-%s.md" % (m.group(1).lower(), re.sub(r'[^a-z0-9]+','-',m.group(2).lower()).strip('-'))
    m = re.match(r'Build (\d+):\s*(.+)', title)
    if m:
        return "build-%02d-%s.md" % (int(m.group(1)), re.sub(r'[^a-z0-9]+','-',m.group(2).lower()).strip('-'))
    if title.startswith('The Build Track'):
        return "build-00-0-the-build-track.md"
    if title.startswith('The Build Ledger'):
        return "build-11-the-build-ledger.md"
    return "00-%d-%s.md" % (order, re.sub(r'[^a-z0-9]+','-',title.lower()).strip('-'))

os.makedirs('masterclass', exist_ok=True)
written = []
for n, ch in enumerate(chunks):
    title = ch.split('\n',1)[0][3:].strip()
    rest  = ch.split('\n',1)[1].strip() if '\n' in ch else ''
    fn = fname(title, n)
    text = rest.replace('](assets/', '](../assets/')
    head = "# " + title + "\n\n"
    if n == 0 and lead:
        head += lead.replace('](assets/','](../assets/') + "\n\n"
    nav = "\n\n---\n\n[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)\n"
    open(os.path.join('masterclass', fn),'w',encoding='utf8').write(head + text + nav)
    written.append((title, fn))

def gh_slug(t):
    s = t.lower()
    s = re.sub(r"[^a-z0-9 \-]", "", s)     # GitHub drops punctuation
    return re.sub(r"\s+", "-", s.strip())

toc = ["## Contents\n"]
for ch in chunks:
    t = ch.split("\n", 1)[0][3:].strip()
    m = re.match(r"(Part \d+|Appendix [A-Z]|Build \d+):\s*(.+)", t)
    if m:
        toc.append(f"- **[{m.group(1)}]({'#user-content-' + gh_slug(t)})** {m.group(2)}")
    else:
        toc.append(f"- [{t}]({'#user-content-' + gh_slug(t)})")
toc = "\n".join(toc) + "\n"

full = ("# The Hermes Agent Masterclass\n\n"
        + lead.replace('](assets/','](../assets/') + "\n\n"
        + toc + "\n---\n\n"
        + "\n\n".join(ch.replace('](assets/','](../assets/') for ch in chunks) + "\n")
open('masterclass/FULL-MASTERCLASS.md','w',encoding='utf8').write(full)

print("sections:", len(written))
for t,f in written: print("  %-52s %s" % (f, t[:48]))
