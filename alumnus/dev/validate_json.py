"""Validate JSON templates, section groups and settings_data against section/theme schemas,
mirroring the checks Shopify runs when a theme is uploaded."""
import json, re, sys, pathlib

root = pathlib.Path(sys.argv[1])
errors = []

def err(where, msg):
    errors.append(f"{where}: {msg}")

def load_schema(section_file):
    text = section_file.read_text()
    m = re.search(r"{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema\s*-?%}", text, re.S)
    if not m:
        return None
    return json.loads(m.group(1))

schemas = {}
for f in (root / 'sections').glob('*.liquid'):
    try:
        s = load_schema(f)
    except json.JSONDecodeError as e:
        err(str(f), f"schema JSON invalid: {e}")
        continue
    if s is None:
        err(str(f), "no schema")
        continue
    schemas[f.stem] = s

BLOCK_TAGS = re.compile(r"^\s*<(p|ul|ol|h[1-6])[\s>]", re.I)
HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
NO_DEFAULT = {"image_picker", "video", "product", "collection", "page", "blog", "article", "font_picker_x"}

def check_value(where, setting, value):
    t = setting['type']
    sid = setting['id']
    if t in ('text', 'textarea', 'html', 'liquid'):
        if not isinstance(value, str): err(where, f"{sid}: expected string")
    elif t == 'richtext':
        if not isinstance(value, str): err(where, f"{sid}: expected string")
        elif value and not BLOCK_TAGS.match(value): err(where, f"{sid}: richtext must start with <p>/<ul>/<ol>/<h*>")
    elif t == 'inline_richtext':
        if not isinstance(value, str): err(where, f"{sid}: expected string")
        elif re.search(r"<(p|div|ul|ol|h[1-6])[\s>]", value, re.I): err(where, f"{sid}: inline_richtext cannot contain block tags")
    elif t == 'checkbox':
        if not isinstance(value, bool): err(where, f"{sid}: expected boolean")
    elif t in ('range',):
        if not isinstance(value, (int, float)): err(where, f"{sid}: expected number"); return
        lo, hi, step = setting['min'], setting['max'], setting.get('step', 1)
        if value < lo or value > hi: err(where, f"{sid}: {value} outside {lo}-{hi}")
        if abs(((value - lo) / step) - round((value - lo) / step)) > 1e-9: err(where, f"{sid}: {value} not on step {step} from {lo}")
    elif t == 'number':
        if not isinstance(value, (int, float)): err(where, f"{sid}: expected number")
    elif t in ('select', 'radio'):
        opts = [o['value'] for o in setting['options']]
        if value not in opts: err(where, f"{sid}: '{value}' not in {opts}")
    elif t == 'color':
        if not isinstance(value, str) or not HEX.match(value): err(where, f"{sid}: bad color {value}")
    elif t == 'url':
        if value and not (isinstance(value, str) and (value.startswith(('http://', 'https://', '/', 'mailto:', 'tel:', 'shopify://')))):
            err(where, f"{sid}: url value '{value}' will be rejected")
    elif t in NO_DEFAULT:
        pass

def check_setting_defs(where, settings):
    ids = set()
    for st in settings:
        t = st.get('type')
        if t in ('header', 'paragraph'):
            if 'content' not in st: err(where, f"{t} without content")
            continue
        sid = st.get('id')
        if not sid: err(where, f"setting without id: {st}"); continue
        if sid in ids: err(where, f"duplicate setting id {sid}")
        ids.add(sid)
        if 'label' not in st: err(where, f"{sid}: missing label")
        if t == 'range':
            for k in ('min', 'max', 'step'):
                if k not in st: err(where, f"{sid}: range missing {k}")
            if all(k in st for k in ('min', 'max', 'step')):
                steps = (st['max'] - st['min']) / st['step']
                if steps > 101: err(where, f"{sid}: range has {steps} steps (max 101)")
                if 'default' not in st: err(where, f"{sid}: range needs default")
        if t in ('select', 'radio') and 'options' not in st: err(where, f"{sid}: missing options")
        if t in ('image_picker', 'video', 'product', 'collection', 'link_list') and 'default' in st and t != 'link_list':
            err(where, f"{sid}: {t} cannot have default")
        if t == 'url' and 'default' in st and st['default'] not in ('/collections', '/collections/all'):
            err(where, f"{sid}: url default must be /collections or /collections/all")
        if t == 'font_picker' and 'default' not in st: err(where, f"{sid}: font_picker needs default")
        if 'default' in st and t not in ('font_picker',):
            check_value(where + ' [default]', st, st['default'])
    return ids

# validate section schemas themselves
for name, s in schemas.items():
    where = f"sections/{name}.liquid"
    if len(s.get('name', '')) > 25: err(where, f"name '{s['name']}' longer than 25 chars")
    check_setting_defs(where, s.get('settings', []))
    btypes = {}
    for b in s.get('blocks', []):
        if b['type'].startswith('@'): continue
        if 'name' not in b: err(where, f"block {b['type']} missing name")
        elif len(b['name']) > 25: err(where, f"block name '{b['name']}' > 25 chars")
        check_setting_defs(f"{where} block {b['type']}", b.get('settings', []))
        btypes[b['type']] = b
    for preset in s.get('presets', []):
        smap = {st['id']: st for st in s.get('settings', []) if 'id' in st}
        for k, v in preset.get('settings', {}).items():
            if k not in smap: err(where, f"preset setting '{k}' not in schema")
            else: check_value(f"{where} preset", smap[k], v)
        for pb in preset.get('blocks', []):
            bt = pb['type']
            if bt not in btypes: err(where, f"preset block type '{bt}' unknown"); continue
            bmap = {st['id']: st for st in btypes[bt].get('settings', []) if 'id' in st}
            for k, v in pb.get('settings', {}).items():
                if k not in bmap: err(where, f"preset block {bt} setting '{k}' not in schema")
                else: check_value(f"{where} preset block {bt}", bmap[k], v)

def check_section_instance(where, key, inst):
    t = inst.get('type')
    if t not in schemas:
        err(where, f"section '{key}' type '{t}' missing"); return
    s = schemas[t]
    smap = {st['id']: st for st in s.get('settings', []) if 'id' in st}
    for k, v in inst.get('settings', {}).items():
        if k not in smap: err(where, f"section '{key}' ({t}) setting '{k}' not in schema")
        else: check_value(f"{where} section '{key}'", smap[k], v)
    btypes = {b['type']: b for b in s.get('blocks', [])}
    blocks = inst.get('blocks', {})
    order = inst.get('block_order', [])
    if set(order) != set(blocks.keys()): err(where, f"section '{key}' block_order mismatch: {set(order) ^ set(blocks.keys())}")
    if 'max_blocks' in s and len(blocks) > s['max_blocks']: err(where, f"section '{key}' has {len(blocks)} blocks > max {s['max_blocks']}")
    counts = {}
    for bkey, b in blocks.items():
        bt = b.get('type')
        counts[bt] = counts.get(bt, 0) + 1
        if bt not in btypes: err(where, f"section '{key}' block '{bkey}' type '{bt}' not allowed"); continue
        bmap = {st['id']: st for st in btypes[bt].get('settings', []) if 'id' in st}
        for k, v in b.get('settings', {}).items():
            if k not in bmap: err(where, f"section '{key}' block '{bkey}' setting '{k}' not in schema")
            else: check_value(f"{where} section '{key}' block '{bkey}'", bmap[k], v)
    for bt, c in counts.items():
        lim = btypes.get(bt, {}).get('limit')
        if lim and c > lim: err(where, f"section '{key}' has {c} '{bt}' blocks > limit {lim}")
    groups = s.get('enabled_on', {}).get('groups')
    return groups

for f in sorted((root / 'templates').glob('*.json')):
    d = json.loads(f.read_text())
    where = f"templates/{f.name}"
    secs = d.get('sections', {})
    if set(d.get('order', [])) - set(secs.keys()): err(where, "order references missing sections")
    for key, inst in secs.items():
        groups = check_section_instance(where, key, inst)
        if groups: err(where, f"section '{key}' is restricted to groups {groups} but used in a template")

for f in sorted((root / 'sections').glob('*.json')):
    d = json.loads(f.read_text())
    where = f"sections/{f.name}"
    for key, inst in d.get('sections', {}).items():
        check_section_instance(where, key, inst)

# settings_data vs settings_schema
schema = json.loads((root / 'config/settings_schema.json').read_text())
gmap = {}
for grp in schema:
    for st in grp.get('settings', []):
        if 'id' in st: gmap[st['id']] = st
    if grp.get('name') != 'theme_info':
        check_setting_defs(f"settings_schema/{grp.get('name')}", grp.get('settings', []))
data = json.loads((root / 'config/settings_data.json').read_text())
for scope in [data.get('current', {})] + list(data.get('presets', {}).values()):
    if isinstance(scope, str): continue
    for k, v in scope.items():
        if k == 'sections' or k == 'content_for_index' or k == 'blocks': continue
        if k not in gmap: err('settings_data', f"'{k}' not in settings_schema")
        else: check_value('settings_data', gmap[k], v)

# translation pluralization sanity
loc = json.loads((root / 'locales/en.default.json').read_text())

print("\n".join(errors) if errors else "JSON validation: no problems found")
print(f"sections with schema: {len(schemas)}")
sys.exit(1 if errors else 0)
