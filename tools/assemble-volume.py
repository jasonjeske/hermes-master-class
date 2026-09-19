"""Assemble a volume from its parts under src/volumes/, substituting kit files into placeholders.
Usage: python3 tools/assemble-volume.py desktop|bots|company [out.md]   (default out: /tmp/<volume>.md)
Then: python3 tools/convert-volume.py /tmp/<v>.md /tmp/<v>.converted.md
      python3 tools/split-volume.py /tmp/<v>.converted.md <v>/ "<Title>" FULL-<NAME>.md"""
import sys, os, re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SRC=f'{ROOT}/src/volumes'; KITS=f'{ROOT}/kits'
vol=sys.argv[1]
parts={'desktop':['desktop-a.md','desktop-workshop.md','desktop-b.md','desktop-c.md'],
       'bots':['bots-a.md','bots-b.md','bots-memory.md','bots-c.md'],
       'company':['company-a.md','company-b.md','company-c.md']}[vol]
# ordering fix: desktop is a, b (builds 3-4), workshop (5-8), c (9)
if vol=='desktop': parts=['desktop-a.md','desktop-b.md','desktop-workshop.md','desktop-c.md']
subs={
 'PROMPT_LIBRARY_PLUGIN_JS': f'{KITS}/desktop-plugins/prompt-library/plugin.js',
 'FLEET_BOARD_PLUGIN_JS': f'{KITS}/desktop-plugins/fleet-board/plugin.js',
 'LEDGER_PLUGIN_YAML': f'{KITS}/agent-plugins/ledger/plugin.yaml',
 'LEDGER_SCHEMAS_PY': f'{KITS}/agent-plugins/ledger/schemas.py',
 'LEDGER_CORE_PY': f'{KITS}/agent-plugins/ledger/ledger_core.py',
 'LEDGER_TOOLS_PY': f'{KITS}/agent-plugins/ledger/tools.py',
 'LEDGER_INIT_PY': f'{KITS}/agent-plugins/ledger/__init__.py',
 'LEDGER_MANIFEST_JSON': f'{KITS}/agent-plugins/ledger/dashboard/manifest.json',
 'LEDGER_API_PY': f'{KITS}/agent-plugins/ledger/dashboard/plugin_api.py',
 'LEDGER_DESKTOP_JS': f'{KITS}/agent-plugins/ledger/desktop/plugin.js',
 'OPS_ROUTINES_SH': f'{KITS}/bot-team/ops/routines.sh',
 'ATLAS_ROUTINES_SH': f'{KITS}/bot-team/atlas/routines.sh',
 'SCOUT_ROUTINES_SH': f'{KITS}/bot-team/scout/routines.sh',
 'HINDSIGHT_CONFIG_JSON': f'{KITS}/bot-team/memory/hindsight-config.json',
 'HINDSIGHT_SETUP_SH': f'{KITS}/bot-team/memory/hindsight-setup.sh',
 'MNEMOSYNE_SETUP_SH': f'{KITS}/bot-team/memory/mnemosyne-setup.sh',
 'LIFE_ROUTINES': f'{KITS}/company/life/routines.sh',
 'COMPANY_MD': f'{KITS}/company/COMPANY.md',
 'ORG_YAML': f'{KITS}/company/ORG.yaml',
 'POLICIES_MD': f'{KITS}/company/POLICIES.md',
 'CADENCE_ROUTINES_SH': f'{KITS}/company/cadence/routines.sh',
 'LINE_TEMPLATE_MD': f'{KITS}/company/production/LINE-TEMPLATE.md',
 'ATLAS_PROTOCOL_MD': f'{KITS}/company/ATLAS-PROTOCOL.md',
 'OFFER_TEMPLATE_MD': f'{KITS}/company/clients/OFFER-TEMPLATE.md',
 'CLIENT_TEMPLATE_MD': f'{KITS}/company/clients/CLIENT-TEMPLATE.md',
}
out=[]
for p in parts:
    path=f'{SRC}/{p}'
    if not os.path.exists(path): print('missing part', p); continue
    out.append(open(path,encoding='utf8').read().rstrip('\n'))
text='\n\n'.join(out)+'\n'
for key,path in subs.items():
    if key in text:
        body=open(path,encoding='utf8').read().rstrip('\n')
        assert '```' not in body, f'{path} contains a fence'
        text=text.replace(key, body)
left=re.findall(r'\b[A-Z_]{8,}\b', text)
left=[l for l in set(left) if l.endswith(('_JS','_PY','_YAML','_JSON','_SH','_MD','_ROUTINES'))]
out=sys.argv[2] if len(sys.argv)>2 else f'/tmp/{vol}.md'
open(out,'w',encoding='utf8').write(text)
print(f'{out}: {len(text)} chars, unresolved placeholders: {left}, dashes: {len(re.findall("[—–]", text))}')
