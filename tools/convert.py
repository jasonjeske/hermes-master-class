import re, os, sys

src = open('/tmp/mc-source.md', encoding='utf8').read()
# strip the _HTMLDOC frontmatter, keep meta we need
fm = re.match(r'^---\n(.*?)\n---\n', src, re.S)
body = src[fm.end():]

def md_table(content):
    rows = [l for l in content.strip().split('\n') if l.strip()]
    if not rows: return ''
    def cells(l): return [c.strip() for c in l.strip().strip('|').split('|')]
    head = cells(rows[0])
    out = ['| ' + ' | '.join(head) + ' |',
           '|' + '|'.join(['---'] * len(head)) + '|']
    for r in rows[1:]:
        c = cells(r)
        c += [''] * (len(head) - len(c))
        out.append('| ' + ' | '.join(c[:len(head)]) + ' |')
    return '\n'.join(out)

def callout(content, attrs):
    kind = attrs.get('kind', 'note')
    title = attrs.get('title', '')
    icon = {'warn':'⚠️','info':'ℹ️','note':'📝','success':'✅'}.get(kind,'📝')
    lines = ['> ' + icon + ' **' + title + '**' if title else '> ' + icon]
    lines.append('>')
    for l in content.strip().split('\n'):
        lines.append('> ' + l if l.strip() else '>')
    return '\n'.join(lines)

def checklist(content):
    out = []
    for l in content.strip().split('\n'):
        l = l.strip()
        if l.startswith('[x]'): out.append('- [x] ' + l[3:].strip())
        elif l.startswith('[ ]'): out.append('- [ ] ' + l[3:].strip())
        elif l: out.append('- ' + l)
    return '\n'.join(out)

def data_model(content, attrs):
    name = attrs.get('name','')
    rows = [l for l in content.strip().split('\n') if l.strip()]
    out = []
    if name: out.append('**' + name + '**\n')
    out.append('| Field | Type | Notes |')
    out.append('|---|---|---|')
    for r in rows:
        p = [c.strip() for c in r.split('|')]
        p += [''] * (3 - len(p))
        out.append('| ' + ' | '.join(p[:3]) + ' |')
    return '\n'.join(out)

def parse_attrs(s):
    a = {}
    for m in re.finditer(r'(\w+)=("([^"]*)"|\S+)', s):
        a[m.group(1)] = m.group(3) if m.group(3) is not None else m.group(2)
    return a

def convert_block(kind, attrline, content):
    attrs = parse_attrs(attrline)
    title = attrs.get('title','')
    if kind == 'table':
        t = ('**' + title + '**\n\n') if title else ''
        return t + md_table(content)
    if kind == 'diagram':
        t = ('**' + title + '**\n\n') if title else ''
        return t + '```mermaid\n' + content.strip() + '\n```'
    if kind == 'callout':
        return callout(content, attrs)
    if kind == 'checklist':
        return checklist(content)
    if kind == 'data-model':
        return data_model(content, attrs)
    if kind == 'file-tree':
        t = ('**' + title + '**\n\n') if title else ''
        return t + '```text\n' + content.rstrip() + '\n```'
    if kind == 'code':
        lang = attrs.get('lang','')
        f = attrs.get('file','')
        t = ('*`' + f + '`*\n\n') if f else ''
        return t + '```' + lang + '\n' + content.rstrip() + '\n```'
    # fallback
    return '```\n' + content.rstrip() + '\n```'

# walk the body, replacing fenced typed blocks
out = []
i = 0
lines = body.split('\n')
while i < len(lines):
    m = re.match(r'^```([a-z-]+)(.*)$', lines[i])
    if m and m.group(1) not in ('mermaid','text','bash','yaml','markdown','ts','js','json','python','sh'):
        kind = m.group(1); attrline = m.group(2)
        j = i + 1; buf = []
        while j < len(lines) and not lines[j].startswith('```'):
            buf.append(lines[j]); j += 1
        out.append(convert_block(kind, attrline, '\n'.join(buf)))
        i = j + 1
    else:
        out.append(lines[i]); i += 1

converted = '\n'.join(out)
open('/tmp/mc-converted.md','w',encoding='utf8').write(converted)
print("converted chars:", len(converted))
print("mermaid blocks:", converted.count('```mermaid'))
print("md tables:", converted.count('|---'))
print("remaining typed blocks:", len(re.findall(r'^```(table|callout|checklist|data-model|file-tree|diagram)\b', converted, re.M)))
