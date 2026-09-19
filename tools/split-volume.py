"""Volume-aware split: python3 splitvol.py <converted.md> <outdir> "<Volume title>" <full-name>
Sections split on top-level '## ' outside fences. Files: build-NN-slug.md for 'Build N:' headings,
00-N-slug.md for front sections, 99-slug.md for closing sections. Writes <outdir>/<full-name>."""
import re, os, sys
src, outdir, title, fullname = sys.argv[1:5]
c = open(src, encoding='utf8').read().strip()
lines = c.split('\n'); fence=False; idxs=[]
for i,l in enumerate(lines):
    if l.startswith('```'): fence = not fence; continue
    if not fence and l.startswith('## '): idxs.append(i)
lead = '\n'.join(lines[:idxs[0]]).strip()
chunks = ['\n'.join(lines[s:(idxs[n+1] if n+1 < len(idxs) else len(lines))]).strip() for n,s in enumerate(idxs)]
def slug(t): return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')
def fname(t, order, last):
    m = re.match(r'Build (\d+):\s*(.+)', t)
    if m: return 'build-%02d-%s.md' % (int(m.group(1)), slug(m.group(2)))
    if last: return '99-%s.md' % slug(t)
    return '00-%d-%s.md' % (order, slug(t))
os.makedirs(outdir, exist_ok=True)
written=[]
seen_build=False
for n,ch in enumerate(chunks):
    t = ch.split('\n',1)[0][3:].strip(); rest = ch.split('\n',1)[1].strip() if '\n' in ch else ''
    is_build = bool(re.match(r'Build \d+:', t))
    fn = fname(t, n, last=(seen_build and not is_build))
    seen_build = seen_build or is_build
    head = '# ' + t + '\n\n' + ((lead.replace('](assets/','](../assets/') + '\n\n') if n == 0 and lead else '')
    nav = '\n\n---\n\n[← Back to the index](../README.md) · [Whole volume in one file](%s)\n' % fullname
    open(os.path.join(outdir, fn), 'w', encoding='utf8').write(head + rest.replace('](assets/','](../assets/') + nav)
    written.append((t, fn))
def gh(t): s=re.sub(r'[^a-z0-9 \-]','',t.lower()); return re.sub(r'\s+','-',s.strip())
toc=['## Contents\n']
for ch in chunks:
    t = ch.split('\n',1)[0][3:].strip(); m = re.match(r'(Build \d+):\s*(.+)', t)
    toc.append(f"- **[{m.group(1)}](#user-content-{gh(t)})** {m.group(2)}" if m else f"- [{t}](#user-content-{gh(t)})")
full = '# ' + title + '\n\n' + lead.replace('](assets/','](../assets/') + '\n\n' + '\n'.join(toc) + '\n\n---\n\n' + '\n\n'.join(ch.replace('](assets/','](../assets/') for ch in chunks) + '\n'
open(os.path.join(outdir, fullname), 'w', encoding='utf8').write(full)
print('sections:', len(written)); [print('  %-48s %s' % (f, t[:50])) for t,f in written]
