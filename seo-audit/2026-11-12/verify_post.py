"""Verify source fidelity and discovery for the strategic review publication."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib, json
root=Path(__file__).resolve().parents[2]
slug='ogilvy-mather-universal-strategic-review'
source=(root/'prompt-sources'/f'{slug}.md').read_text()
soup=BeautifulSoup((root/'output/blog'/slug/'index.html').read_text(),'html.parser')
assert soup.select_one('code.language-markdown').get_text()==source.rstrip()
assert len(soup.select('h1'))==1
assert soup.select_one('link[rel=canonical]')['href']==f'https://prompts.robertdevore.com/blog/{slug}/'
for file in ['index.html','marketing/index.html','business/index.html','sitemap.xml','feed/index.xml','llms.txt','assets/js/docs-search-index.json','.well-known/kujo-site-index.json']:
    assert slug in (root/'output'/file).read_text(),file
for node in soup.select('script[type="application/ld+json"]'): json.loads(node.string)
receipt={'status':'PASS','source_sha256':hashlib.sha256(source.encode()).hexdigest(),'verbatim_render':True,'discovery':True,'single_h1':True,'schema_parses':True}
(Path(__file__).parent/'raw/prompt-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt)
