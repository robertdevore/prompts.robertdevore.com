#!/usr/bin/env python3
"""Check the rendered JSON, examples and discovery surfaces against authored content."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from PIL import Image
ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent
SLUG = 'professional-esports-logo-generator-json-prompt'
URL = f'https://prompts.robertdevore.com/blog/{SLUG}/'
source = (ROOT / f'content/posts/{SLUG}.md').read_text()
expected = (ROOT / f'prompt-sources/{SLUG}.json').read_text().rstrip()
page = BeautifulSoup((ROOT / f'output/blog/{SLUG}/index.html').read_text(), 'html.parser')
blocks = page.select('pre code.language-json')
assert len(blocks) == 1 and blocks[0].get_text().rstrip() == expected
assert len(json.loads(expected)['styleProfiles']) == 6
assert len(page.select('h1')) == 1
assert page.select_one('link[rel=canonical]')['href'] == URL
examples = page.select('img[alt*="esports logo"]')
assert len(examples) == 3
for img in examples:
    path = ROOT / 'output' / urlparse(img['src']).path.lstrip('/')
    if not path.exists(): path = (ROOT / f'output/blog/{SLUG}' / img['src']).resolve()
    with Image.open(path) as im:
        assert im.width == im.height
        assert int(img['width']) == im.width and int(img['height']) == im.height
    assert img['alt'] and img['loading'] == 'lazy'
for route in ('images/index.html','index.html','blog/index.html'):
    soup = BeautifulSoup((ROOT / 'output' / route).read_text(), 'html.parser')
    assert any(SLUG in a['href'] for a in soup.select('a[href]')), route
for file in ('sitemap.xml','feed/index.xml','llms.txt'):
    assert URL in (ROOT / 'output' / file).read_text(), file
index = json.loads((ROOT / 'output/assets/js/docs-search-index.json').read_text())
item = next(i for i in index['items'] if SLUG in i['url'])
assert 'adaptive_professional_esports_logo_generator' in item['text']
assert expected in item['text']
webmcp = json.loads((ROOT / 'output/.well-known/kujo-site-index.json').read_text())
assert any(SLUG in item['url'] for item in webmcp['items'])
for block in page.select('script[type="application/ld+json"]'): json.loads(block.string)
social = page.select_one('meta[property="og:image"]')['content']
with Image.open(ROOT / 'output' / urlparse(social).path.lstrip('/')) as im: assert im.size == (1200,630)
receipt = {'result':'PASS','url':URL,'json_sha256':hashlib.sha256(expected.encode()).hexdigest(),'styles':6,'examples':3,'discovery':'home/category/archive/sitemap/feed/llms/search/WebMCP','social':social,'checks':'JSON text equality; schema parsing; canonical; square examples and actual dimensions; discovery; social image dimensions'}
(AUDIT / 'raw/new-post-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
