"""Build a standalone, downloadable HTML preview with strict CSP hashes."""
from pathlib import Path
import base64,hashlib,re
ROOT=Path(__file__).resolve().parents[1]
def hashed(text):return "'sha256-"+base64.b64encode(hashlib.sha256(text.encode()).digest()).decode()+"'"
css=(ROOT/'src/styles.css').read_text();js=(ROOT/'src/app.js').read_text()
image='data:image/webp;base64,'+base64.b64encode((ROOT/'assets/garden.webp').read_bytes()).decode()
text=(ROOT/'src/page.html').read_text().replace('__CSS__',css).replace('__JS__',js).replace('__GARDEN_IMAGE__',image)
# Hash the exact rendered contents, including template formatting whitespace.
actual_css=re.search(r'<style>([\s\S]*?)</style>',text).group(1)
actual_js=re.search(r'<script>([\s\S]*?)</script>',text).group(1)
policy="default-src 'none'; script-src "+hashed(actual_js)+"; style-src "+hashed(actual_css)+"; img-src data:; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'"
text=text.replace('__CSP__',policy)
(ROOT/'index.html').write_text(text)
print('Built standalone index.html:',len(text.encode()),'bytes')
