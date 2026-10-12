"""Reexecuta T5 independente com transporte HTTP local, sem modificar critérios SAN."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import threading,subprocess,os,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
s=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
threading.Thread(target=s.serve_forever,daemon=True).start()
env=os.environ.copy();env['DEV_URL']=f'http://127.0.0.1:{s.server_port}/Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html'
try:
 r=subprocess.run(['node','t5.js'],cwd=Path(__file__).parent,env=env)
 results=json.loads((Path(__file__).parent/'t5.json').read_text())
 code=r.returncode or int(len(results)!=13 or any(x['resultado']!='APROVADO' for x in results))
 (Path(__file__).parent/'execucao.json').write_text(json.dumps({'html_sha256':hashlib.sha256((ROOT/'Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html').read_bytes()).hexdigest(),'exit_code':code,'checks':len(results)},indent=2))
 raise SystemExit(code)
finally:s.shutdown();s.server_close()
