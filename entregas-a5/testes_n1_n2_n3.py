import os
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import threading,json,hashlib,time
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).parent
PREFIX='__MA_DEV61_SANDBOX__:'
HTML='Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html'
RESULTS=[]
def check(id,ok,evidence=''):
 RESULTS.append(dict(id=id,status='APROVADO' if ok else 'REPROVADO',evidence=evidence));print(RESULTS[-1],flush=True);assert ok,id
def row(i):return dict(id='Cora:F'+str(i),date='2026-10-10',bank='Cora',description='Fictício '+str(i),amount=1000+i,kind='Receita')
CARE=dict(version=2,patients=[dict(id='fic',name='Paciente Fictício A5',cpf='',phone='',email='',address='',cep='')],records=[],notes=[])
SENT={'ma-care-v2':'SENTINELA-FICTICIA','ma-ledger-v1':'SENTINELA-FICTICIA-LEDGER','ma-ledger-v1-prev':'SENTINELA-FICTICIA-PREV'}
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
def context(browser,ledger,extras=None):
 c=browser.new_context(accept_downloads=True);seeds={PREFIX+'ma-care-v2':json.dumps(CARE),PREFIX+'ma-ledger-v1':json.dumps(ledger),**SENT,**{PREFIX+k:v for k,v in (extras or {}).items()}}
 c.add_init_script("""(()=>{const ls=localStorage;if(ls.getItem('__MA_DEV61_SANDBOX__:seeded'))return;for(const [k,v] of Object.entries(DATA))ls.setItem(k,v);ls.setItem('__MA_DEV61_SANDBOX__:seeded','1');})();""".replace('DATA',json.dumps(seeds)))
 c.route('**/*',lambda req:req.continue_() if req.request.url.startswith(f'http://127.0.0.1:{server.server_port}/') else req.abort());p=c.new_page();p.set_default_timeout(90000);p.on('dialog',lambda d:d.accept());errs=[];p.on('pageerror',lambda e:errs.append(str(e)));p.goto(f'http://127.0.0.1:{server.server_port}/{HTML}',timeout=180000);p.wait_for_function('window.MA5 && MA5.appReady===true');return c,p,errs
def store(p):return p.evaluate('MA5.localEntries()')
def get(p,key):return p.evaluate('(k)=>localStorage.getItem(k)',key)
def dl(p,id,name):
 with p.expect_download(timeout=60000) as e:p.locator('#'+id).evaluate('(e)=>e.click()')
 out=ROOT/'evidencias-fase1'/name;out.parent.mkdir(exist_ok=True);e.value.save_as(out);return out
failure=None
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_BIN','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
  for n in [500,1500]:
   c,p,errs=context(b,[row(i) for i in range(n)])
   initial=get(p,'ma-ledger-v1');p.evaluate('go("ledger")')
   out=p.evaluate("""async()=>{for(let i=0;i<220;i++){if(!await ma62ApplyCorrection(0,'description','Operação fictícia '+i))return {failed:i,msg:document.querySelector('#ledger-message').textContent};}return {failed:null,history:(await MA5.all()).length,keys:MA5.localEntries().map(x=>x.key),raw:localStorage.getItem('ma-ledger-v1')};}""")
   check('N1-220-OPERACOES-'+str(n),out['failed'] is None and out['history']==220,{'linhas':n,'operações':220,'históricos':out.get('history'),'erro':out.get('failed')})
   check('N1-SEM-CRESCIMENTO-COPIAS-LOCAL-'+str(n),not any(k.startswith('ma-ledger-v1-session-prev-') for k in out['keys']))
   first=p.evaluate('(async()=>{const x=await MA5.all();return x[0].raw})()')
   check('N1-COPIA-ORIGINAL-RECUPERAVEL-'+str(n),p.evaluate('(raw)=>MA5.all().then(a=>a.some(x=>x.raw===raw))',initial))
   check('N3-SEM-FAIXA-ROTINEIRA-'+str(n),p.locator('#ma62-ledger-alert').count()==0)
   path=dl(p,'ma5-history-export','historico-'+str(n)+'.json')
   p.locator('#ma5-history-verify').set_input_files(str(path));p.wait_for_function('MA5.verifiedArchive!==null')
   check('N1-ARQUIVO-EXTERNO-VERIFICADO-'+str(n),'verificado' in p.locator('#ma5-storage-message').text_content())
   ids=p.evaluate('MA5.history().then(a=>a.filter(x=>x.kind==="operation").slice(0,219).map(x=>x.storage+":"+x.id))')
   deleted=p.evaluate('(ids)=>MA5.deleteVerified(ids)',ids)
   check('N1-LIMPEZA-SELETIVA-'+str(n),deleted.get('deleted')==219 and p.evaluate('MA5.all().then(a=>a.filter(x=>x.kind==="operation").length)')==1)
   pack=json.loads(path.read_text());check('N1-EXTERNO-PRESERVA-ESTADOS-'+str(n),len(pack['records'])==220 and any(x['raw']==initial for x in pack['records']))
   check('N1-LIVRO-ATUAL-INALTERADO-PELA-LIMPEZA-'+str(n),get(p,'ma-ledger-v1')==out['raw'])
   # A cópia mais recente não pode ser removida mesmo com arquivo externo conferido.
   latest=p.evaluate('MA5.history().then(a=>a.filter(x=>x.kind==="operation").map(x=>x.storage+":"+x.id))')
   blocked=p.evaluate('(ids)=>MA5.deleteVerified(ids).then(()=>false).catch(e=>e.message)',latest)
   check('N1-RETENCAO-MINIMA-'+str(n),isinstance(blocked,str) and 'mais recente' in blocked)
   check('JS-FASE1-'+str(n),not errs,errs);c.close()
  old=json.dumps([row(i) for i in range(500)],ensure_ascii=False);q='ma-ledger-v1-rejeitados-20260101';review='ma-ledger-v1-quarantine-review:'+q
  c,p,errs=context(b,[row(i) for i in range(500)],{q:'QUARENTENA-FICTICIA',review:'REVISAO-FICTICIA'})
  filled=p.evaluate("""raw=>{let i=0;try{for(;i<500;i++)localStorage.setItem('ma-ledger-v1-session-prev-antiga-'+i,raw);}catch(e){if(e.name!=='QuotaExceededError')throw e;}return i;}""",old)
  check('N1-COTA-REAL-SATURADA',filled>10,filled)
  path=dl(p,'ma5-history-export','historico-cota-real.json');p.locator('#ma5-history-verify').set_input_files(str(path));p.wait_for_function('MA5.verifiedArchive!==null')
  ids=p.evaluate('MA5.history().then(a=>a.filter(x=>x.kind==="operation").slice(0,-1).map(x=>x.storage+":"+x.id))');p.evaluate('(ids)=>MA5.deleteVerified(ids)',ids)
  check('N1-QUARENTENA-REVISAO-PRESERVADAS',get(p,q)=='QUARENTENA-FICTICIA' and get(p,review)=='REVISAO-FICTICIA')
  protected=p.evaluate('(ids)=>MA5.deleteVerified(ids).then(()=>false).catch(e=>e.message)',['localStorage:'+q]);check('N1-QUARENTENA-NAO-ELEGIVEL',isinstance(protected,str) and 'Quarentenas' in protected)
  # Pagamento por UI após liberar espaço, sem acessar dados reais.
  p.evaluate('go("quick")');p.locator('#quick-search').fill('Paciente Fictício A5');p.locator('#quick-results button').first.click()
  f=p.locator('#payment-form');f.locator('[name=date]').fill('2026-10-11');f.locator('[name=amount]').fill('55.50');f.locator('[name=service]').fill('Pagamento fictício pós limpeza');f.locator('button.primary').click()
  check('N1-PAGAMENTO-POS-LIBERACAO',any(x['service']=='Pagamento fictício pós limpeza' for x in json.loads(get(p,'ma-care-v2'))['records']))
  check('N3-RISCO-REAL-CONTINUA-VISIVEL',p.locator('#ma62-ledger-alert').count()==1)
  check('JS-COTA',not errs,errs);c.close()
  c,p,errs=context(b,[row(0)|{'id':123}]);p.evaluate('go("backup")');original=get(p,'ma-ledger-v1');path=dl(p,'ma5-export-ledger-raw','livro-id-numerico.json')
  check('N2-BRUTO-ACESSIVEL-SEM-FAIXA',p.locator('#ma5-export-ledger-raw').is_visible() and p.locator('#ma62-ledger-alert').count()==0 and path.read_text()==original)
  check('N2-ID-NUMERICO-ORIGINAL',json.loads(path.read_text())[0]['id']==123)
  check('JS-N2',not errs,errs);c.close();b.close()
except Exception as e:
 import traceback;traceback.print_exc();failure=str(e)
finally:
 server.shutdown();server.server_close();(ROOT/'resultados-fase1.json').write_text(json.dumps({'phase':'Regressão N1/N2/N3 na versão entregue','failure':failure,'checks':RESULTS,'html_sha256':hashlib.sha256((ROOT/HTML).read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
raise SystemExit(1 if failure else 0)
