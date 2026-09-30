"""Build the no-face copy of the invite into a separate folder / repo.

The bride's face must not appear before беташар, so this copy is a separate site that
does not contain the couple photo at all (not just hidden): hero-hands.webp replaces it,
hero.webp is not copied, and no reference to it is left in the page.

    python tools/build-nophoto.py <target-folder> <public-base-url>
    e.g. python tools/build-nophoto.py ../toi-nophoto https://bozzbala.github.io/toi/
"""
import re, shutil, sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
DST = Path(sys.argv[1]).resolve()
BASE = sys.argv[2].rstrip('/') + '/'
MAIN_BASE = 'https://bozzbala.github.io/wedding/'

html = (SRC / 'index.html').read_text(encoding='utf-8')
html = re.sub(r'var NOPHOTO = [^\n]*\n', 'var NOPHOTO = true;\n', html, count=1)
# keep only the no-face hero choice
html = re.sub(r"var HERO = NOPHOTO \? (\{[^}]*\})\s*:\s*\{[^}]*\};", r"var HERO = \1;", html, count=1)
html = html.replace(MAIN_BASE + 'images/hero.webp', BASE + 'images/hero-hands.webp').replace(MAIN_BASE, BASE)
assert not re.search(r'images/hero\.webp', html), 'couple photo still referenced'
assert 'var NOPHOTO = true;' in html and "var HERO = { src: 'images/hero-hands.webp'" in html

DST.mkdir(parents=True, exist_ok=True)
for p in DST.iterdir():                       # clean everything except the target repo's own .git
    if p.name == '.git': continue
    shutil.rmtree(p) if p.is_dir() else p.unlink()
(DST / 'index.html').write_text(html, encoding='utf-8')
shutil.copytree(SRC / 'fonts', DST / 'fonts')
shutil.copytree(SRC / 'images', DST / 'images', ignore=shutil.ignore_patterns('hero.webp'))
(DST / '.nojekyll').write_text('')
print('built', DST, '->', BASE)
