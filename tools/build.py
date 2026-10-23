"""Generates the multi-page trilingual thresher demo site.
Run:  python tools/build.py        (SITE_URL env sets canonical/sitemap domain)
"""
import os, re, json, html, posixpath, shutil, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools')
SITE = os.environ.get('SITE_URL', 'https://www.example.com').rstrip('/')
WA = '919999999999'
PHONE = '+91 99999 99999'
LANGS = ['gu', 'hi', 'en']
LABEL = {'gu': 'ગુ', 'hi': 'हि', 'en': 'EN'}
OGL = {'gu': 'gu_IN', 'hi': 'hi_IN', 'en': 'en_IN'}
TINT = ['#8fd0a5', '#f2cf7a', '#e8a98a', '#8cc8e0']
GAL = [['wheat', 'wheat2', 'harvest'], ['castor', 'castor-seed', 'farm'], ['groundnut', 'groundnut-field', 'farm'], ['maize', 'farm', 'harvest']]
HERO_IMG = {0: 'harvest', 1: 'castor', 2: 'groundnut', 3: 'maize'}

def load(lang):
    spec = importlib.util.spec_from_file_location('c_' + lang, os.path.join(TOOLS, 'c_%s.py' % lang))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m.D

DATA = {l: load(l) for l in LANGS}
e = html.escape

# ---------------------------------------------------------------- pages
PAGES = [('home', ''), ('products', 'products/')]
PAGES += [('m%d' % i, 'products/%s/' % DATA['en']['M'][i]['slug']) for i in range(4)]
PAGES += [('crops', 'crop-guide/'), ('manufacturing', 'manufacturing/'), ('service', 'spares-and-service/'),
          ('subsidy', 'subsidy-help/'), ('about', 'about/'), ('faq', 'faq/'), ('contact', 'contact/')]
PATH = dict(PAGES)

def cur_dir(lang, key):
    p = PATH[key].rstrip('/')
    return lang + ('/' + p if p else '')

def rel(frm, to):
    r = posixpath.relpath(to, frm)
    return '' if r == '.' else r + '/'

def link(lang, key, to_key, to_lang=None):
    to_lang = to_lang or lang
    return rel(cur_dir(lang, key), cur_dir(to_lang, to_key)) + 'index.html'

def asset(lang, key, path):
    return posixpath.relpath(path, cur_dir(lang, key))

def abs_url(lang, key):
    return '%s/%s/%s' % (SITE, lang, PATH[key])

# ---------------------------------------------------------------- art
def machine(label, v):
    cls = {'multi': ('#1f5a3a', '#2e7a50'), 'castor': ('#e0a526', '#c68a0f'), 'gn': ('#b4532a', '#d2693b'), 'maize': ('#1f7aa3', '#3aa0cc')}[v]
    bars = '<g fill="#12201a" opacity=".28"><rect x="112" y="146" width="116" height="7" rx="3.5"/><rect x="112" y="162" width="116" height="7" rx="3.5"/><rect x="112" y="178" width="116" height="7" rx="3.5"/></g>'
    extra = {
        'multi': '<g stroke="#fff" stroke-width="3" opacity=".35" stroke-linecap="round"><path d="M116 150h110M116 164h110M116 178h110"/></g>',
        'castor': bars,
        'gn': '<g fill="#12201a" opacity=".28"><rect x="112" y="146" width="116" height="7" rx="3.5"/><rect x="112" y="170" width="116" height="7" rx="3.5"/></g><g fill="#f4d9a0" stroke="#8a5a2a" stroke-width="2"><ellipse cx="58" cy="262" rx="9" ry="6"/><ellipse cx="76" cy="268" rx="9" ry="6"/><ellipse cx="94" cy="262" rx="9" ry="6"/></g>',
        'maize': '<g fill="#f0bc4a" stroke="#b07a00" stroke-width="2"><ellipse cx="88" cy="44" rx="20" ry="7" transform="rotate(-14 88 44)"/><ellipse cx="136" cy="36" rx="20" ry="7" transform="rotate(8 136 36)"/></g><g fill="#12201a" opacity=".28"><rect x="112" y="150" width="116" height="7" rx="3.5"/><rect x="112" y="174" width="116" height="7" rx="3.5"/></g>'}[v]
    return ('<svg viewBox="0 0 500 300" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg">' % e(label) + MACHINE_BODY.format(c0=cls[0], c1=cls[1], extra=extra) + '</svg>')

MACHINE_BODY = '''<ellipse cx="250" cy="282" rx="205" ry="12" fill="#12201a" opacity=".16"/>
<path d="M40 214H6" stroke="#12201a" stroke-width="8" stroke-linecap="round"/><circle cx="8" cy="214" r="7" fill="#12201a"/>
<rect x="38" y="208" width="380" height="20" rx="8" fill="#12201a"/>
<path d="M388 132L410 66L468 40" fill="none" stroke="#12201a" stroke-width="30" stroke-linecap="round" stroke-linejoin="round" opacity=".18"/>
<path d="M388 132L410 66L468 40" fill="none" stroke="{c1}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M446 32l30 14-8 20-30-14z" fill="{c0}"/>
<rect x="66" y="22" width="206" height="12" rx="6" fill="#12201a" opacity=".82"/>
<path d="M74 34h190l-34 90H108z" fill="{c1}"/>
<path d="M74 34h190l-6 16H80z" fill="#fff" opacity=".2"/>
{extra}
<rect x="82" y="116" width="330" height="96" rx="18" fill="{c0}"/>
<rect x="82" y="116" width="330" height="18" rx="9" fill="#fff" opacity=".18"/>
<circle cx="338" cy="168" r="42" fill="#12201a" opacity=".9"/>
<circle cx="338" cy="168" r="32" fill="none" stroke="#e0a526" stroke-width="7" stroke-dasharray="9 7"><animateTransform attributeName="transform" type="rotate" from="0 338 168" to="360 338 168" dur="9s" repeatCount="indefinite"/></circle>
<circle cx="338" cy="168" r="8" fill="#e0a526"/>
<circle cx="64" cy="176" r="22" fill="#12201a"/><circle cx="64" cy="176" r="9" fill="#e0a526"/>
<path d="M64 154L82 140M64 198L82 196" stroke="#12201a" stroke-width="4" opacity=".6"/>
<g fill="#12201a"><circle cx="150" cy="250" r="34"/><circle cx="352" cy="250" r="34"/></g>
<g fill="#d5ddd8"><circle cx="150" cy="250" r="15"/><circle cx="352" cy="250" r="15"/></g>
<g fill="#12201a"><circle cx="150" cy="250" r="5"/><circle cx="352" cy="250" r="5"/></g>'''

ANN = {
 'en': ['Feed hopper', 'Threshing drum', 'Sieves', 'Blower pipe', 'PTO / motor pulley', 'Wheels', 'Chassis & frame'],
 'gu': ['ફીડ હોપર', 'થ્રેશિંગ ડ્રમ', 'ચાળણી', 'બ્લોઅર પાઇપ', 'PTO / મોટર પુલી', 'વ્હીલ', 'ચેસિસ અને ફ્રેમ'],
 'hi': ['फीड हॉपर', 'थ्रेशिंग ड्रम', 'छलनी', 'ब्लोअर पाइप', 'PTO / मोटर पुली', 'व्हील', 'चेसिस और फ्रेम'],
}
ANN_T = {'en': 'Inside a thresher', 'gu': 'થ્રેશરની અંદર', 'hi': 'थ्रेशर के अंदर'}

def annotated(lang):
    t = ANN[lang]
    body = MACHINE_BODY.format(c0='#1f5a3a', c1='#2e7a50', extra='<g stroke="#fff" stroke-width="3" opacity=".35" stroke-linecap="round"><path d="M116 150h110M116 164h110M116 178h110"/></g>')
    # callouts: (label, target x,y (machine coords), text x,y, anchor)
    co = [(t[0], 170, 60, 60, 20, 'start'), (t[1], 338, 150, 470, 20, 'start'), (t[2], 170, 164, 20, 140, 'start'),
          (t[3], 440, 50, 580, 70, 'start'), (t[4], 64, 176, 20, 330, 'start'), (t[5], 352, 250, 520, 330, 'start'), (t[6], 250, 218, 330, 330, 'start')]
    g = ''
    for lab, tx, ty, lx, ly, an in co:
        g += '<path d="M%d %d L%d %d" stroke="#c68a0f" stroke-width="2" fill="none"/><circle cx="%d" cy="%d" r="5" fill="#c68a0f"/><text x="%d" y="%d" text-anchor="%s">%s</text>' % (
            lx + 4, ly + 6, tx + 90, ty + 40, tx + 90, ty + 40, lx, ly, an, e(lab))
    return '<svg viewBox="0 0 700 360" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg"><g transform="translate(90 40)">%s</g>%s</svg>' % (e(ANN_T[lang]), body.replace('{extra}', ''), g)

# ---------------------------------------------------------------- shared html
def wa_link(text):
    from urllib.parse import quote
    return 'https://wa.me/%s?text=%s' % (WA, quote(text))

def jsonld(items):
    return ''.join('<script type="application/ld+json">%s</script>\n' % json.dumps(i, ensure_ascii=False) for i in items)

def org(lang):
    L = DATA[lang]
    return {'@context': 'https://schema.org', '@type': ['Organization', 'LocalBusiness'], 'name': L['brand'],
            'url': SITE + '/', 'telephone': '+919999999999', 'areaServed': 'Gujarat',
            'description': DATA['en']['home']['desc'],
            'address': {'@type': 'PostalAddress', 'addressLocality': 'Visnagar', 'addressRegion': 'Gujarat', 'addressCountry': 'IN'}}

def crumbs_ld(lang, trail):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': abs_url(lang, k)} for i, (n, k) in enumerate(trail)]}

def faq_ld(pairs):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in pairs]}

def head(lang, key, title, desc, extra_ld=(), og='hero', noindex=False):
    L = DATA[lang]
    A = lambda p: asset(lang, key, p)
    alts = ''.join('<link rel="alternate" hreflang="%s" href="%s">\n' % (l, abs_url(l, key)) for l in LANGS)
    alts += '<link rel="alternate" hreflang="x-default" href="%s">\n' % abs_url('gu', key)
    return ('<!doctype html>\n<html lang="%s">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n%s<link rel="canonical" href="%s">\n<meta name="theme-color" content="#0f3322">\n'
            '<meta property="og:type" content="website"><meta property="og:site_name" content="%s"><meta property="og:locale" content="%s">\n'
            '<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s"><meta property="og:image" content="%s/assets/img/%s.jpg">\n'
            '<meta name="twitter:card" content="summary_large_image">\n%s'
            '<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 64 64\'%%3E%%3Crect width=\'64\' height=\'64\' rx=\'16\' fill=\'%%230f3322\'/%%3E%%3Ccircle cx=\'32\' cy=\'32\' r=\'12\' fill=\'none\' stroke=\'%%23e0a526\' stroke-width=\'6\' stroke-dasharray=\'5 4\'/%%3E%%3Ccircle cx=\'32\' cy=\'32\' r=\'4\' fill=\'%%23e0a526\'/%%3E%%3C/svg%%3E">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Inter:wght@400;500;600;700&family=Noto+Sans+Gujarati:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
            '<link rel="stylesheet" href="%s">\n%s%s</head>\n') % (
        L['htmllang'], e(title), e(desc), alts, abs_url(lang, key), e(L['brand']), OGL[lang], e(title), e(desc), abs_url(lang, key), SITE, og,
        '<meta name="robots" content="noindex">\n' if noindex else '', A('assets/css/style.css'), jsonld([org(lang)] + list(extra_ld)),
        '<link rel="preload" as="image" href="%s" type="image/webp">\n' % A('assets/img/hero.webp') if key == 'home' else '')

CHEV = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 4l4 4 4-4"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.2 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .5l-.4.6c-.1.2-.3.3-.1.6.2.3.8 1.3 1.8 2.1 1.2 1 2.2 1.4 2.5 1.5.3.1.4.1.6-.1l.8-1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.3.1.2.1.8-.1 1.4z"/></svg>'
PHONE_ICON = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>'

def active_dd(key, keys):
    return ' aria-current="page"' if key in keys else ''

def header(lang, key):
    L = DATA[lang]; N = L['nav']; M = L['M']
    h = lambda k: link(lang, key, k)
    cur = lambda k: ' aria-current="page"' if key == k else ''
    prod_keys = ['products'] + ['m%d' % i for i in range(4)]
    fac_keys = ['manufacturing', 'about']
    sup_keys = ['service', 'subsidy', 'faq']
    prod_items = '<a class="all" href="%s"%s>%s</a>' % (h('products'), cur('products'), N['all_products']) + ''.join(
        '<a href="%s"%s>%s<small>%s</small></a>' % (h('m%d' % i), cur('m%d' % i), e(M[i]['name']), e(M[i]['best'])) for i in range(4))
    def dd(label, keys, items):
        return '<div class="dd"><button type="button" aria-haspopup="true" aria-expanded="false"%s>%s%s</button><div class="dd-menu">%s</div></div>' % (active_dd(key, keys), label, CHEV, items)
    nav = ('<a href="%s"%s>%s</a>' % (h('home'), cur('home'), N['home']) +
           dd(N['products'], prod_keys, prod_items) +
           '<a href="%s"%s>%s</a>' % (h('crops'), cur('crops'), N['crops']) +
           dd(N['factory'], fac_keys, '<a href="%s"%s>%s</a><a href="%s"%s>%s</a>' % (h('manufacturing'), cur('manufacturing'), N['manufacturing'], h('about'), cur('about'), N['about'])) +
           dd(N['support'], sup_keys, ''.join('<a href="%s"%s>%s</a>' % (h(k), cur(k), N[k]) for k in sup_keys)) +
           '<a href="%s"%s>%s</a>' % (h('contact'), cur('contact'), N['contact']))
    langs = ''.join('<a href="%s" hreflang="%s" lang="%s" data-lang="%s"%s>%s</a>' % (
        link(lang, key, key, l), l, l, l, ' aria-current="true"' if l == lang else '', LABEL[l]) for l in LANGS)
    dnav = ('<a href="%s">%s</a>' % (h('home'), N['home']) + '<span class="dl">%s</span>' % N['products'] +
            '<a class="sub" href="%s">%s</a>' % (h('products'), N['all_products']) +
            ''.join('<a class="sub" href="%s">%s</a>' % (h('m%d' % i), e(M[i]['name'])) for i in range(4)) +
            '<a href="%s">%s</a>' % (h('crops'), N['crops']) + '<span class="dl">%s</span>' % N['factory'] +
            '<a class="sub" href="%s">%s</a><a class="sub" href="%s">%s</a>' % (h('manufacturing'), N['manufacturing'], h('about'), N['about']) +
            '<span class="dl">%s</span>' % N['support'] + ''.join('<a class="sub" href="%s">%s</a>' % (h(k), N[k]) for k in sup_keys) +
            '<a href="%s">%s</a>' % (h('contact'), N['contact']))
    return ('<a class="skip" href="#main">%s</a>\n<header class="hdr" id="hdr"><div class="hdr-in">'
            '<a class="logo" href="%s" aria-label="%s"><svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="18" fill="#e0a526"/><g fill="none" stroke="#0f3322" stroke-width="5" stroke-linecap="round"><circle cx="32" cy="34" r="10" stroke-dasharray="6 4.5"/><path d="M32 18v-6M22 22l-4-4M42 22l4-4"/></g><circle cx="32" cy="34" r="3.5" fill="#0f3322"/></svg><span><span>%s</span><small>%s</small></span></a>'
            '<nav class="nav" aria-label="Main">%s</nav><div class="lang" role="group" aria-label="Language">%s</div>'
            '<a class="btn btn-gold" href="%s">%s</a>'
            '<button class="burger" id="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h10"/></svg></button></div></header>\n'
            '<div class="drawer" id="drawer" aria-hidden="true"><div class="drawer-top"><span class="logo"><span>%s</span></span>'
            '<button class="burger" id="close" type="button" aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>'
            '<nav aria-label="Mobile">%s</nav><div class="lang" role="group" aria-label="Language">%s</div><a class="btn btn-gold" style="margin-top:24px" href="%s">%s</a></div>\n') % (
        L['skip'], h('home'), e(L['brand']), e(L['brand']), L['city'], nav, langs, h('contact'), N['quote'], e(L['brand']), dnav, langs, h('contact'), N['quote'])

def footer(lang, key):
    L = DATA[lang]; N = L['nav']; U = L['ui']
    h = lambda k: link(lang, key, k)
    links = ''.join('<a href="%s">%s</a><br>' % (h(k), N[k]) for k in ['products', 'crops', 'manufacturing', 'service', 'subsidy', 'about', 'faq', 'contact'])
    mach = ''.join('<a href="%s">%s</a><br>' % (h('m%d' % i), e(L['M'][i]['name'])) for i in range(4))
    credits = ('Hero: “Threshing mustard with thresher in India” (CC BY-SA 4.0) · Wheat: “Wheat harvest, Raisen district, Madhya Pradesh, India” (CC BY-SA 4.0) · Wheat field: “Wheat field, gujarat” (CC BY-SA 4.0) · '
               'Harvest: “Wheat bundles harvested” (CC BY-SA 4.0) · Groundnut: “Groundnut Seed” (CC BY 4.0), “Groundnuts farm” (CC BY-SA 4.0) · Maize: “Sundrying maize on cobs 03” (CC BY 4.0) · '
               'Castor: “A castor field” (CC0), “Ricinus communis-seeds-yercaud-salem-India” (CC BY-SA 4.0) · Farm: “7 Agriculture, Tractor and Rural life in India Red Chili Peppers” (CC BY 2.0). All via Wikimedia Commons. Machine illustrations are original vector artwork.')
    return ('<footer><div class="wrap"><div class="foot"><div><span class="logo"><span>%s</span></span><p>%s</p></div>'
            '<div><b style="color:#fff">%s</b><p>%s</p></div><div><b style="color:#fff">%s</b><p>%s</p><p>%s<br>Visnagar, Mehsana, Gujarat</p></div></div>'
            '<details class="credits"><summary>%s</summary><p>%s</p><p>%s</p></details></div></footer>\n'
            '<div class="mbar"><a href="tel:+919999999999">%s<span>%s</span></a><a href="%s" target="_blank" rel="noopener">%s WhatsApp</a><a class="q" href="%s">%s</a></div>\n'
            '<script src="%s" defer></script>\n</body>\n</html>\n') % (
        e(L['brand']), U['foot_t'], U['quick'], links, N['products'], mach, PHONE, U['credits'], U['credits_n'], credits,
        PHONE_ICON, U['call'], wa_link(L['hello']), WA_ICON, h('contact'), N['quote'], asset(lang, key, 'assets/js/app.js'))

def phero(lang, key, trail, h1, lead, extra='', split=''):
    L = DATA[lang]; U = L['ui']
    items = ''
    for i, (name, k) in enumerate(trail):
        items += '<li>%s</li>' % (('<a href="%s">%s</a>' % (link(lang, key, k), e(name))) if k and i < len(trail) - 1 else '<span aria-current="page">%s</span>' % e(name))
    inner = '<ol class="crumbs" aria-label="Breadcrumb">%s</ol><h1>%s</h1><p class="lead">%s</p>%s' % (items, h1, lead, extra)
    if split:
        inner = '<div class="split"><div>%s</div>%s</div>' % (inner, split)
    return '<main id="main"><section class="phero"><div class="wrap">%s</div></section>\n' % inner

def band(lang, key, text):
    L = DATA[lang]; U = L['ui']
    return ('<div class="band"><div class="wrap band-in"><h2 class="rv">%s</h2><div class="cta-row rv"><a class="btn btn-dark" href="%s">%s</a>'
            '<a class="btn btn-outline" style="border-color:rgba(18,32,26,.4)" href="%s" target="_blank" rel="noopener">%s</a></div></div></div>\n') % (
        text, link(lang, key, 'contact'), U['cta_quote'], wa_link(L['hello']), U['wa'])

def prod_card(lang, key, i, d=0):
    L = DATA[lang]; m = L['M'][i]; U = L['ui']
    return ('<article class="card rv" style="--d:%ss;--tint:%s"><a class="card-art" href="%s" aria-label="%s">%s</a><div class="card-body"><h3><a href="%s" style="text-decoration:none">%s</a></h3><p>%s</p><p><strong>%s</strong></p>'
            '<div class="tags">%s</div><a class="more" href="%s">%s%s</a></div></article>') % (
        d, TINT[i], link(lang, key, 'm%d' % i), e(m['name']), machine(m['name'], m['key']), link(lang, key, 'm%d' % i), e(m['name']), m['short'], m['best'],
        ''.join('<span class="tag">%s</span>' % t for t in m['tags']), link(lang, key, 'm%d' % i), U['view'], ARROW)

def faq_items(pairs, first_open=True):
    return ''.join('<details class="rv" %s><summary>%s</summary><p>%s</p></details>' % ('open' if (i == 0 and first_open) else '', q, a) for i, (q, a) in enumerate(pairs))

def form(lang, machines_opt=True, fields=('name', 'mobile', 'village', 'machine', 'message'), msg_label=None):
    L = DATA[lang]; U = L['ui']
    inp = lambda n, lab, extra='': '<label><span>%s</span><input name="%s" data-l="%s" %s></label>' % (lab, n, e(lab), extra)
    opts = ''.join('<option>%s</option>' % e(x) for x in [U['not_sure']] + [m['name'] for m in L['M']])
    ml = msg_label or U['message']
    return ('<form data-wa="%s" novalidate class="rv"><div class="f2">%s%s</div><div class="f2">%s<label><span>%s</span><select name="machine" data-l="%s">%s</select></label></div>'
            '<label><span>%s</span><textarea name="msg" data-l="%s"></textarea></label>'
            '<button class="btn btn-dark" type="submit">%s<span>%s</span></button><p class="note">%s</p></form>') % (
        WA, inp('name', U['name'], 'autocomplete="name" required'), inp('mobile', U['mobile'], 'type="tel" inputmode="tel" autocomplete="tel" pattern="[0-9 +]{10,14}" required'),
        inp('village', U['village'], 'autocomplete="address-level2"'), U['machine'], e(U['machine']), opts, ml, e(ml), WA_ICON, U['send'], U['form_note'])

def head_sec(k, h, s=''):
    return '<div class="section-head rv"><span class="kicker">%s</span><h2>%s</h2>%s</div>' % (k, h, ('<p class="lead">%s</p>' % s) if s else '')

def img(lang, key, name, alt, w=1200, h=800, lazy=True, extra=''):
    return '<img src="%s" alt="%s" width="%d" height="%d"%s%s>' % (asset(lang, key, 'assets/img/%s.webp' % name), e(alt), w, h, ' loading="lazy"' if lazy else '', extra)

# ---------------------------------------------------------------- pages
def page_home(lang):
    key = 'home'; L = DATA[lang]; H = L['home']; U = L['ui']; M = L['M']; N = L['nav']
    o = head(lang, key, H['title'], H['desc'], [faq_ld(L['faq']['F'][:4])])
    o += '<body>\n' + header(lang, key)
    o += ('<main id="main"><section class="hero"><div class="wrap hero-grid"><div><span class="kicker rv">%s</span><h1 class="rv" style="--d:.08s">%s</h1><p class="lead rv" style="--d:.16s">%s</p>'
          '<div class="cta-row rv" style="--d:.24s"><a class="btn btn-gold" href="%s">%s</a><a class="btn btn-ghost" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a></div>'
          '<div class="chips rv" style="--d:.32s">%s</div></div>'
          '<div class="hero-media rv" style="--d:.2s"><div class="hero-frame"><img id="heroimg" src="%s" width="1600" height="1100" alt="%s" fetchpriority="high"></div>'
          '<div class="float f2"><svg class="gear" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"><circle cx="24" cy="24" r="12" stroke-dasharray="6 5"/><circle cx="24" cy="24" r="3" fill="currentColor"/></svg><div><b>%s</b><span>%s</span></div></div>'
          '<div class="float f1"><b>%s</b><span>%s</span></div></div></div></section>\n') % (
        H['kicker'], H['h1'], H['sub'], link(lang, key, 'contact'), U['cta_quote'], wa_link(L['hello']), WA_ICON, U['wa'],
        ''.join('<span class="chip"><i></i>%s</span>' % c for c in H['chips']), asset(lang, key, 'assets/img/hero.webp'), e(H['hero_alt']), H['f2t'], H['f2s'], H['f1t'], H['f1s'])
    mq = ''.join('<span>%s</span>' % x for x in [c['k'] for c in L['C']] + [m['name'] for m in M])
    o += '<div class="marquee" aria-hidden="true"><div class="marquee-track">%s%s</div></div>\n' % (mq, mq)
    icons = ['<path d="M12 21V8M12 8c-3 0-5-2-5-5 3 0 5 2 5 5zM12 8c3 0 5-2 5-5-3 0-5 2-5 5zM12 14c-3 0-5-2-5-5M12 14c3 0 5-2 5-5"/>',
             '<circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/>',
             '<path d="M3 21V10l9-6 9 6v11z"/><path d="M9 21v-6h6v6"/>']
    facts = ''.join('<div class="fact rv" style="--d:%ss"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">%s</svg><div><b>%s</b><span>%s</span></div></div>' % (i * .08, icons[i], a, b) for i, (a, b) in enumerate(H['facts']))
    o += '<section class="intro"><div class="wrap intro-grid"><div class="rv"><span class="kicker">%s</span><p class="big" style="margin-top:18px">%s</p></div><div class="facts">%s</div></div></section>\n' % (H['intro_k'], H['intro_p'], facts)
    o += '<section style="padding-top:0"><div class="wrap">%s<div class="prod-grid">%s</div></div></section>\n' % (
        head_sec(H['prod_k'], H['prod_h'], H['prod_s']), ''.join(prod_card(lang, key, i, i * .08) for i in range(4)))
    # picker
    tabs = ''.join('<button class="tab" type="button" role="tab" id="tab%d" aria-selected="%s" aria-controls="pn%d" tabindex="%d">%s%s</button>' % (
        i, 'true' if i == 0 else 'false', i, 0 if i == 0 else -1, img(lang, key, c['img'], '', 44, 44), c['k']) for i, c in enumerate(L['C']))
    panels = ''
    for i, c in enumerate(L['C']):
        m = M[c['m']]
        panels += ('<div class="panel" role="tabpanel" id="pn%d" aria-labelledby="tab%d"%s><div class="panel-img">%s</div><div class="panel-body"><span class="kicker">%s</span><h3 style="font-size:var(--step-2)">%s</h3>'
                   '<div class="rec">%s<span class="note">%s</span></div><ul>%s</ul><div class="cta-row"><a class="btn btn-dark" href="%s">%s</a><a class="btn btn-outline" href="%s" target="_blank" rel="noopener">%s</a></div></div></div>') % (
            i, i, '' if i == 0 else ' hidden', img(lang, key, c['img'], c['k']), U['rec'], e(m['name']), machine(m['name'], m['key']), m['best'],
            ''.join('<li>%s</li>' % x for x in c['l']), link(lang, key, 'm%d' % c['m']), U['view'], wa_link('%s / %s' % (m['name'], c['k'])), U['pick_cta'])
    o += '<section class="picker"><div class="wrap">%s<div class="pick-grid"><div class="tabs" role="tablist" aria-label="%s">%s</div><div>%s</div></div></div></section>\n' % (
        head_sec(H['pick_k'], H['pick_h'], H['pick_s']), e(H['pick_k']), tabs, panels)
    # why
    ic = ['<path d="M3 21V9l6 4V9l6 4V5h6v16z"/>', '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
          '<circle cx="12" cy="12" r="3.5"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>', '<path d="M12 3c4 0 7 3 7 7 0 2.5-1.5 4-3 5.5V18H8v-2.5C6.5 14 5 12.5 5 10c0-4 3-7 7-7z"/><path d="M9 21h6"/>']
    tiles = ['<div class="tile %s rv" style="--d:%ss"><span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">%s</svg></span><h3>%s</h3><p>%s</p></div>' % (
        'gold' if i == 2 else '', i * .08, ic[i], h, p) for i, (h, p) in enumerate(H['W'])]
    tiles.insert(1, '<div class="tile photo rv">%s<div><h3>%s</h3><p>%s</p></div></div>' % (img(lang, key, 'farm', '', 1200, 900), H['why_photo'][0], H['why_photo'][1]))
    o += '<section><div class="wrap">%s<div class="bento">%s</div></div></section>\n' % (head_sec(H['why_k'], H['why_h']), ''.join(tiles))
    # process
    steps = ''.join('<div class="step rv" style="--d:%ss"><span class="num">0%d</span><h3>%s</h3><p>%s</p></div>' % (i * .06, i + 1, h, p) for i, (h, p) in enumerate(L['manufacturing']['S']))
    o += ('<section class="process"><div class="wrap">%s<div class="steps">%s</div><div style="margin-top:32px"><a class="btn btn-gold" href="%s">%s</a></div></div></section>\n') % (
        head_sec(H['proc_k'], H['proc_h'], H['proc_s']), steps, link(lang, key, 'manufacturing'), H['proc_more'])
    tl = ''.join('<li class="tl rv" style="--d:%ss"><span class="dot">%d</span><div><h3>%s</h3><p>%s</p></div></li>' % (i * .07, i + 1, h, p) for i, (h, p) in enumerate(H['O']))
    o += '<section><div class="wrap">%s<ol class="timeline">%s</ol></div></section>\n' % (head_sec(H['ord_k'], H['ord_h']), tl)
    o += ('<section class="faq" style="padding-top:0"><div class="wrap faq-grid"><div class="faq-side rv"><span class="kicker">%s</span><h2 style="margin-top:14px">%s</h2><p class="lead" style="margin-top:16px">%s</p>'
          '<a class="btn btn-outline" style="margin-top:22px" href="%s">%s</a></div><div>%s</div></div></section>\n') % (
        H['faq_k'], H['faq_h'], H['faq_s'], link(lang, key, 'faq'), H['faq_more'], faq_items(L['faq']['F'][:4]))
    o += '<section class="area"><div class="wrap">%s<div class="area-chips">%s</div></div></section>\n' % (head_sec(H['area_k'], H['area_h']), ''.join('<span>%s</span>' % a for a in H['A']))
    o += band(lang, key, H['band_h']) + '</main>\n' + footer(lang, key)
    return o

def page_products(lang):
    key = 'products'; L = DATA[lang]; P = L['products']; U = L['ui']; N = L['nav']; M = L['M']
    o = head(lang, key, P['title'], P['desc'], [crumbs_ld(lang, [(N['home'], 'home'), (N['products'], key)])])
    o += '<body>\n' + header(lang, key) + phero(lang, key, [(N['home'], 'home'), (N['products'], key)], P['h1'], P['lead'])
    o += '<section><div class="wrap"><div class="prod-grid">%s</div></div></section>\n' % ''.join(prod_card(lang, key, i, i * .08) for i in range(4))
    rows = ''.join('<tr><td><a href="%s">%s</a></td><td>%s</td><td>%s</td></tr>' % (link(lang, key, 'm%d' % i), e(m['name']), m['best'], ' / '.join(m['tags'])) for i, m in enumerate(M))
    o += ('<section class="picker"><div class="wrap">%s<div class="table-wrap rv"><table class="spec"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div></div></section>\n') % (
        head_sec('', P['cmp_h']).replace('<span class="kicker"></span>', ''), ''.join('<th scope="col">%s</th>' % c for c in P['cmp_cols']), rows)
    o += band(lang, key, P['pick_h']) + '</main>\n' + footer(lang, key)
    return o

def page_product(lang, i):
    key = 'm%d' % i; L = DATA[lang]; m = L['M'][i]; U = L['ui']; N = L['nav']
    prod_ld = {'@context': 'https://schema.org', '@type': 'Product', 'name': m['name'], 'description': m['answer'],
               'brand': {'@type': 'Brand', 'name': L['brand']}, 'category': 'Agricultural machinery',
               'image': '%s/assets/img/%s.jpg' % (SITE, GAL[i][0]), 'manufacturer': {'@type': 'Organization', 'name': L['brand'], 'address': {'@type': 'PostalAddress', 'addressLocality': 'Visnagar', 'addressCountry': 'IN'}}}
    trail = [(N['home'], 'home'), (N['products'], 'products'), (m['name'], key)]
    o = head(lang, key, m['title'], m['desc'], [prod_ld, faq_ld(m['faq']), crumbs_ld(lang, trail)], og=GAL[i][0])
    o += '<body>\n' + header(lang, key)
    art = '<div class="art" style="--tint:%s">%s</div>' % (TINT[i], machine(m['name'], m['key']))
    o += phero(lang, key, trail, e(m['name']), m['answer'],
               '<div class="cta-row"><a class="btn btn-gold" href="%s">%s</a><a class="btn btn-ghost" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a></div>' % (
                   link(lang, key, 'contact'), U['cta_quote'], wa_link('%s - %s' % (m['name'], L['hello'])), WA_ICON, U['wa']), split=art)
    gal = ''.join('<figure class="rv">%s</figure>' % img(lang, key, g, '%s, %s' % (m['name'], m['best']), 1200, 800) for g in GAL[i])
    specs = ''.join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (a, b) for a, b in m['specs'])
    how = ''.join('<li class="tl rv"><span class="dot">%d</span><div><h3>%s</h3><p>%s</p></div></li>' % (j + 1, h, p) for j, (h, p) in enumerate(m['how']))
    related = ''.join(prod_card(lang, key, j, k * .08) for k, j in enumerate([x for x in range(4) if x != i]))
    main = ('<div class="pd-main"><div class="gallery">%s</div>'
            '<div class="rv"><h2>%s</h2><ul class="checks">%s</ul></div>'
            '<div class="rv"><h2>%s</h2><div class="table-wrap"><table class="spec"><tbody>%s</tbody></table></div></div>'
            '<div class="rv"><h2>%s</h2><div class="pills">%s</div></div>'
            '<div><h2 class="rv">%s</h2><ol class="timeline" style="grid-template-columns:1fr">%s</ol></div>'
            '<div class="faq"><h2 class="rv">%s</h2>%s</div></div>') % (
        gal, U['features'], ''.join('<li>%s</li>' % f for f in m['feats']), U['specs'], specs, U['suitable'],
        ''.join('<span class="pill">%s</span>' % c for c in m['crops']), U['how'], how, U['qfaq'], faq_items(m['faq']))
    aside = ('<aside class="pd-aside"><div class="qcard"><h3>%s</h3><p>%s</p><div class="tags">%s</div>'
             '<a class="btn btn-gold" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a><a class="btn btn-ghost" href="tel:+919999999999">%s<span>%s</span></a>'
             '<a class="btn btn-ghost" href="%s">%s</a></div></aside>') % (
        U['card_q'], U['card_s'], ''.join('<span class="tag">%s</span>' % t for t in m['tags']), wa_link('%s - %s' % (m['name'], L['hello'])), WA_ICON, U['wa'],
        PHONE_ICON, PHONE, link(lang, key, 'contact'), U['cta_quote'])
    o += '<section><div class="wrap pd">%s%s</div></section>\n' % (main, aside)
    o += '<section class="picker related"><div class="wrap">%s<div class="prod-grid">%s</div></div></section>\n' % (head_sec('', U['related']).replace('<span class="kicker"></span>', ''), related)
    o += band(lang, key, L['home']['band_h']) + '</main>\n' + footer(lang, key)
    return o

def page_crops(lang):
    key = 'crops'; L = DATA[lang]; P = L['crops']; U = L['ui']; N = L['nav']; M = L['M']
    trail = [(N['home'], 'home'), (N['crops'], key)]
    o = head(lang, key, P['title'], P['desc'], [crumbs_ld(lang, trail)]) + '<body>\n' + header(lang, key) + phero(lang, key, trail, P['h1'], P['lead'])
    cards = ''
    for c in L['C']:
        m = M[c['m']]
        cards += ('<article class="crop-card rv">%s<div class="b"><span class="kicker">%s</span><h2 style="font-size:var(--step-2)">%s</h2><ul class="checks">%s</ul>'
                  '<div class="cta-row"><a class="btn btn-dark" href="%s">%s: %s</a><a class="btn btn-outline" href="%s" target="_blank" rel="noopener">%s</a></div></div></article>') % (
            img(lang, key, c['img'], c['k']), U['rec'], c['k'], ''.join('<li>%s</li>' % x for x in c['l']), link(lang, key, 'm%d' % c['m']), U['view'], e(m['name']), wa_link('%s / %s' % (m['name'], c['k'])), U['pick_cta'])
    o += '<section><div class="wrap"><div class="crop-list">%s</div></div></section>\n' % cards
    o += '<section class="picker"><div class="wrap"><div class="box rv" style="max-width:720px"><h3>%s</h3><ul class="checks">%s</ul></div></div></section>\n' % (P['share_h'], ''.join('<li>%s</li>' % x for x in P['share']))
    return o + band(lang, key, L['home']['band_h']) + '</main>\n' + footer(lang, key)

def page_manufacturing(lang):
    key = 'manufacturing'; L = DATA[lang]; P = L['manufacturing']; U = L['ui']; N = L['nav']
    trail = [(N['home'], 'home'), (N['manufacturing'], key)]
    o = head(lang, key, P['title'], P['desc'], [crumbs_ld(lang, trail)]) + '<body>\n' + header(lang, key) + phero(lang, key, trail, P['h1'], P['lead'])
    o += '<section><div class="wrap"><div class="annot rv">%s</div></div></section>\n' % annotated(lang)
    steps = ''.join('<div class="step rv" style="--d:%ss"><span class="num">0%d</span><h3>%s</h3><p>%s</p></div>' % (i * .06, i + 1, h, p) for i, (h, p) in enumerate(P['S']))
    o += '<section class="process"><div class="wrap">%s<div class="steps">%s</div></div></section>\n' % (head_sec(L['home']['proc_k'], L['home']['proc_h'], L['home']['proc_s']), steps)
    o += '<section><div class="wrap two"><div class="rv">%s</div><div class="box rv"><ul class="checks">%s</ul></div></div></section>\n' % (
        head_sec('', P['cust_h'], P['cust_s']).replace('<span class="kicker"></span>', ''), ''.join('<li>%s</li>' % x for x in P['cust']))
    return o + band(lang, key, L['home']['band_h']) + '</main>\n' + footer(lang, key)

def page_service(lang):
    key = 'service'; L = DATA[lang]; P = L['service']; U = L['ui']; N = L['nav']
    trail = [(N['home'], 'home'), (N['service'], key)]
    o = head(lang, key, P['title'], P['desc'], [crumbs_ld(lang, trail)]) + '<body>\n' + header(lang, key) + phero(lang, key, trail, P['h1'], P['lead'])
    ul = lambda xs: '<ul class="checks">%s</ul>' % ''.join('<li>%s</li>' % x for x in xs)
    o += ('<section><div class="wrap"><div class="cards3"><div class="box rv"><h3>%s</h3>%s</div><div class="box rv"><h3>%s</h3>%s</div><div class="box rv"><h3>%s</h3><p>%s</p></div></div></div></section>\n') % (
        P['parts_h'], ul(P['parts']), P['svc_h'], ul(P['svc']), P['war_h'], P['war'])
    o += '<section class="picker"><div class="wrap two"><div class="rv">%s%s</div><div>%s</div></div></section>\n' % (
        head_sec('', P['chk_h']).replace('<span class="kicker"></span>', ''), ul(P['chk']), head_sec('', P['req_h'], P['req_s']).replace('<span class="kicker"></span>', '') + form(lang, msg_label=P['req_f']))
    return o + '</main>\n' + footer(lang, key)

def page_subsidy(lang):
    key = 'subsidy'; L = DATA[lang]; P = L['subsidy']; U = L['ui']; N = L['nav']
    trail = [(N['home'], 'home'), (N['subsidy'], key)]
    o = head(lang, key, P['title'], P['desc'], [crumbs_ld(lang, trail)]) + '<body>\n' + header(lang, key) + phero(lang, key, trail, P['h1'], P['lead'])
    tl = ''.join('<li class="tl rv" style="--d:%ss"><span class="dot">%d</span><div><h3>%s</h3><p>%s</p></div></li>' % (i * .07, i + 1, h, p) for i, (h, p) in enumerate(P['steps']))
    ul = lambda xs: '<ul class="checks">%s</ul>' % ''.join('<li>%s</li>' % x for x in xs)
    o += '<section><div class="wrap"><ol class="timeline" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">%s</ol></div></section>\n' % tl
    o += ('<section class="picker"><div class="wrap"><div class="cards2"><div class="box rv"><h3>%s</h3>%s</div><div class="box rv"><h3>%s</h3>%s</div></div>'
          '<div class="notice rv" style="margin-top:20px"><h3>%s</h3><p>%s</p></div></div></section>\n') % (P['docs_h'], ul(P['docs']), P['help_h'], ul(P['help']), P['notice_h'], P['notice'])
    return o + band(lang, key, L['home']['band_h']) + '</main>\n' + footer(lang, key)

def page_about(lang):
    key = 'about'; L = DATA[lang]; P = L['about']; U = L['ui']; N = L['nav']
    trail = [(N['home'], 'home'), (N['about'], key)]
    o = head(lang, key, P['title'], P['desc'], [crumbs_ld(lang, trail)]) + '<body>\n' + header(lang, key) + phero(lang, key, trail, P['h1'], P['lead'])
    o += '<section><div class="wrap two"><div class="rv"><h2 style="font-size:var(--step-2);margin-bottom:18px">%s</h2><div class="prose">%s</div></div><div class="hero-frame rv" style="aspect-ratio:4/3">%s</div></div></section>\n' % (
        P['story_h'], ''.join('<p>%s</p>' % p for p in P['story']), img(lang, key, 'farm', '', 1200, 900))
    o += '<section class="picker"><div class="wrap">%s<div class="cards3">%s</div></div></section>\n' % (
        head_sec('', P['vals_h']).replace('<span class="kicker"></span>', ''), ''.join('<div class="box rv"><h3>%s</h3><p>%s</p></div>' % (h, p) for h, p in P['vals']))
    o += '<section><div class="wrap"><div class="notice rv"><h3>%s</h3><p>%s</p></div></div></section>\n' % (P['certs_h'], P['certs'])
    return o + band(lang, key, L['home']['band_h']) + '</main>\n' + footer(lang, key)

def page_faq(lang):
    key = 'faq'; L = DATA[lang]; P = L['faq']; N = L['nav']
    trail = [(N['home'], 'home'), (N['faq'], key)]
    o = head(lang, key, P['title'], P['desc'], [faq_ld(P['F']), crumbs_ld(lang, trail)]) + '<body>\n' + header(lang, key) + phero(lang, key, trail, P['h1'], P['lead'])
    o += '<section><div class="wrap"><div class="faq" style="max-width:860px;margin-inline:auto">%s</div></div></section>\n' % faq_items(P['F'])
    return o + band(lang, key, L['home']['band_h']) + '</main>\n' + footer(lang, key)

def page_contact(lang):
    key = 'contact'; L = DATA[lang]; P = L['contact']; U = L['ui']; N = L['nav']
    trail = [(N['home'], 'home'), (N['contact'], key)]
    o = head(lang, key, P['title'], P['desc'], [crumbs_ld(lang, trail)]) + '<body>\n' + header(lang, key) + phero(lang, key, trail, P['h1'], P['lead'])
    info = ('<div class="info rv"><div class="box" style="background:var(--forest-900);color:#fff"><b>%s</b><a href="tel:+919999999999">%s</a><p class="note" style="color:rgba(255,255,255,.6);margin:6px 0 0">%s</p></div>'
            '<div class="box"><b style="color:var(--accent-text);font-size:.74rem;letter-spacing:.14em;text-transform:uppercase">%s</b><span>%s</span></div>'
            '<div class="box"><b style="color:var(--accent-text);font-size:.74rem;letter-spacing:.14em;text-transform:uppercase">%s</b><span>%s</span></div>'
            '<a class="btn btn-outline" target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query=Visnagar%%2C+Gujarat">%s</a></div>') % (
        U['ph'], PHONE, U['ph_n'], U['addr'], U['addr_v'], U['hrs'], U['hrs_v'], U['map'])
    o += '<section><div class="wrap"><div class="contact-grid">%s%s</div></div></section>\n' % (form(lang), info)
    return o + '</main>\n' + footer(lang, key)

def page_404(lang):
    L = DATA[lang]; P = L['nf']; U = L['ui']
    key = 'home'
    # 404 lives at <lang>/404.html (same depth as <lang>/index.html)
    o = head(lang, key, P['title'], P['p'], noindex=True) + '<body>\n' + header(lang, key)
    o += '<main id="main" class="nf"><div class="wrap"><h1>%s</h1><p class="lead" style="margin:16px auto 28px">%s</p><div class="cta-row" style="justify-content:center"><a class="btn btn-dark" href="index.html">%s</a><a class="btn btn-outline" href="products/index.html">%s</a></div></div></main>\n' % (
        P['h1'], P['p'], U['home'], L['nav']['all_products']) + footer(lang, key)
    return o

# ---------------------------------------------------------------- write
def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)

def build():
    # css + js
    base = open(os.path.join(TOOLS, 'base.css'), encoding='utf-8').read()
    extra = open(os.path.join(TOOLS, 'extra.css'), encoding='utf-8').read()
    write('assets/css/style.css', base + extra)
    os.makedirs(os.path.join(ROOT, 'assets/js'), exist_ok=True)
    shutil.copyfile(os.path.join(TOOLS, 'app.js'), os.path.join(ROOT, 'assets/js/app.js'))
    n = 0
    for lang in LANGS:
        write('%s/index.html' % lang, page_home(lang))
        write('%s/products/index.html' % lang, page_products(lang))
        for i in range(4):
            write('%s/products/%s/index.html' % (lang, DATA['en']['M'][i]['slug']), page_product(lang, i))
        for key, fn in [('crops', page_crops), ('manufacturing', page_manufacturing), ('service', page_service), ('subsidy', page_subsidy), ('about', page_about), ('faq', page_faq), ('contact', page_contact)]:
            write('%s/%sindex.html' % (lang, PATH[key]), fn(lang))
        write('%s/404.html' % lang, page_404(lang))
        n += 11 + 1
    # root chooser
    chooser = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shree Krushi Thresher Works | ગુજરાતી · हिन्दी · English</title>'
               '<meta name="robots" content="noindex"><link rel="stylesheet" href="assets/css/style.css">'
               '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Inter:wght@500;600&family=Noto+Sans+Gujarati:wght@500;600&family=Noto+Sans+Devanagari:wght@500;600&display=swap" rel="stylesheet">'
               '<script>try{var l=localStorage.getItem("lang");if(["gu","hi","en"].indexOf(l)>-1&&location.search.indexOf("choose")<0)location.replace(l+"/index.html");else if(location.search.indexOf("choose")<0)location.replace("gu/index.html")}catch(e){}</script></head>'
               '<body><main class="chooser"><div><span class="kicker" style="color:var(--gold-400)">Visnagar · Gujarat</span><h1>Shree Krushi Thresher Works</h1><p class="lead" style="color:rgba(255,255,255,.8);margin:0 auto">Choose your language · ભાષા પસંદ કરો · भाषा चुनें</p>'
               '<div class="row"><a class="btn btn-gold" href="gu/index.html" data-lang="gu">ગુજરાતી</a><a class="btn btn-ghost" href="hi/index.html" data-lang="hi">हिन्दी</a><a class="btn btn-ghost" href="en/index.html" data-lang="en">English</a></div></div></main>'
               '<script src="assets/js/app.js" defer></script></body></html>')
    write('index.html', chooser)
    # sitemap / robots / llms
    urls = ''
    for key, p in PAGES:
        for l in LANGS:
            alts = ''.join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (x, abs_url(x, key)) for x in LANGS)
            urls += '<url><loc>%s</loc>%s</url>\n' % (abs_url(l, key), alts)
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n%s</urlset>\n' % urls)
    write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % SITE)
    E = DATA['en']
    write('llms.txt', '# %s\n> %s\n\n## Machines\n%s\n\n## Pages\n%s\n' % (
        E['brand'], E['home']['desc'], '\n'.join('- [%s](%s/en/products/%s/): %s' % (m['name'], SITE, m['slug'], m['short']) for m in E['M']),
        '\n'.join('- [%s](%s)' % (E['nav'].get(k, k), abs_url('en', k)) for k, _ in PAGES if k in E['nav'])))
    print('built %d pages + chooser, sitemap, robots, llms' % n)

if __name__ == '__main__':
    build()
