"""Build the no-photo copy of the invite into a separate folder / repo (bozzbala/toi).

The bride's face must not appear before беташар, so this copy is a separate site with
no couple photo at all (not just hidden): the first screen is the typographic ?text
version (names on a framed wine sheet), no hero photo is copied, no reference to one is
left in the page, and the link preview is images/og-card.jpg.

    python tools/build-nophoto.py <target-folder> <public-base-url>
    e.g. python tools/build-nophoto.py ../toi-nophoto https://bozzbala.github.io/toi/
"""
import re, shutil, sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
DST = Path(sys.argv[1]).resolve()
BASE = sys.argv[2].rstrip('/') + '/'
MAIN_BASE = 'https://bozzbala.github.io/wedding/'
PHOTOS = ('hero.webp', 'hero-hands.webp')

html = (SRC / 'index.html').read_text(encoding='utf-8')
# typographic first screen always on; no photo is ever chosen or preloaded
html, n1 = re.subn(r'var TEXTONLY = [^\n]*\n', 'var TEXTONLY = true;\n', html, count=1)
html, n2 = re.subn(r"var HERO = NOPHOTO \?[^;]*;", 'var HERO = null;', html, count=1, flags=re.S)
html = html.replace(MAIN_BASE + 'images/hero.webp', BASE + 'images/og-card.jpg').replace(MAIN_BASE, BASE)
assert n1 == 1 and n2 == 1, 'source layout changed; update the build script'
for photo in PHOTOS:
    assert photo not in html, f'{photo} still referenced'
assert BASE + 'images/og-card.jpg' in html

DST.mkdir(parents=True, exist_ok=True)
for p in DST.iterdir():                       # clean everything except the target repo's own .git
    if p.name == '.git': continue
    shutil.rmtree(p) if p.is_dir() else p.unlink()
(DST / 'index.html').write_text(html, encoding='utf-8')
shutil.copytree(SRC / 'fonts', DST / 'fonts')
shutil.copytree(SRC / 'images', DST / 'images', ignore=shutil.ignore_patterns(*PHOTOS))
(DST / '.nojekyll').write_text('')
print('built', DST, '->', BASE)
