"""Refresh hashes after editing inline CSS or JavaScript; no CSP weakening."""
from pathlib import Path
import re,base64,hashlib
p=Path(__file__).resolve().parents[1]/'index.html'
text=p.read_text()
def hashes(tag):
 return ' '.join("'sha256-"+base64.b64encode(hashlib.sha256(s.encode()).digest()).decode()+"'" for s in re.findall(fr'<{tag}>([\s\S]*?)</{tag}>',text))
for directive,tag in [('script-src','script'),('style-src','style')]:
 text=re.sub(fr'{directive}[^;]*;',directive+' '+hashes(tag)+';',text)
p.write_text(text)
print('Inline CSP hashes refreshed')
