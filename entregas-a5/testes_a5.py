import os
"""A5: Chromium isolado, HTML completo, fixtures exclusivamente fictícias.
python3 testes_a5.py [--group nome]
"""
import argparse,json,hashlib,threading,time,traceback
from pathlib import Path
from functools import partial
from contextlib import contextmanager
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).parent;HTML=ROOT/'Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html';PREFIX='__MA_DEV61_SANDBOX__:'
def row(index=1,**x):return dict(id='Cora:F'+str(index),date='2026-10-10',bank='Cora',description='Fictício '+str(index),amount=1000+index if isinstance(index,int) else 1000,kind='Receita')|x
def care(label='A',amount=12345):
 p=dict(id='p'+label,name='Paciente Fictício '+label,cpf='',phone='',email='',address='',cep='')
 return dict(version=2,patients=[p],records=[dict(id='r'+label,patientId=p['id'],date='2026-10-10',month='2026-10',amount=amount,service='Serviço fictício '+label,payment='Pix',status='Recebido',snapshot={k:p[k] for k in ['name','cpf','phone','email','address','cep']})],notes=[dict(id='n'+label,patientId=p['id'],date='2026-10-10',tooth='11',text='Evolução fictícia '+label,done=False)])
def academy(label='A'):
 return dict(version=1,settings={'monthly':100,'hours':20,'target':25,'minimum':10,'tax':0,'rates':{}},materials=[dict(id='m'+label,name='Material fictício',price=10,size=100,unit='g',category='Teste')],equipment=[],sessions=[],customPops=[],checks={},training=[],ma58={'version':1,'kind':'anterior','base':'A2','target':'A2','step':{'anterior':0,'posterior':0},'checks':{'anterior':[False]*6,'posterior':[False]*6}},ma59={'version':1,'checks':{},'step':{},'current':'crown','filter':'Todas','search':''},ma60={'version':1,'kind':'crown','material':{'crown':'onx','model':'acqua','splint':'cosmos'},'washStage':0,'blastMaterial':'printed','blastStage':0,'colorZone':{'anterior':'cervical','posterior':'cervical'},'washChecks':{},'blastChecks':{}})
SENT={'ma-care-v2':'SENTINELA-REAL-FICTICIA','ma-ledger-v1':'SENTINELA-REAL-FICTICIA-LIVRO','ma-ledger-v1-prev':'SENTINELA-REAL-FICTICIA-PREV','ma61-sanitary-checklist-v1':'SENTINELA-REAL-FICTICIA-SAN'}
BASES=lambda:{'ma-care-v2':json.dumps(care(),ensure_ascii=False),'ma-ledger-v1':json.dumps([row()]),'ma-academy-v55':json.dumps(academy(),ensure_ascii=False),'ma-installment-rates-v1':'{"5":3.1,"10":5.2}','ma-account-month-last-v1':'2026-10','ma56-project-checklist-v1':'{"version":1,"states":{},"updated":{}}','ma61-sanitary-checklist-v1':'{"version":1,"states":{},"evidence":{},"notes":{},"responsible":{},"due":{},"updated":{}}'}
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
class Suite:
 def __init__(self,b,url,out):self.b=b;self.url=url;self.out=out;self.checks=[];self.seq=0
 def check(self,id,ok,evidence=''):
  r=dict(id=id,status='APROVADO' if ok else 'REPROVADO',evidence=evidence);self.checks.append(r);print(json.dumps(r,ensure_ascii=False),flush=True);assert ok,(id,evidence)
 @contextmanager
 def context(self,override=None,remove=None):
  c=self.b.new_context(accept_downloads=True,viewport={'width':1280,'height':900});values=BASES();values.update(override or {})
  for k in remove or []:values.pop(k,None)
  seeds={PREFIX+k:v for k,v in values.items()}|SENT|{PREFIX+'ma5-suppress-seeds-v1':'1'}
  c.add_init_script("""(()=>{const s=localStorage;if(s.getItem('__MA_DEV61_SANDBOX__:ma5-suppress-seeds-v1')!==null)return;for(const [k,v] of Object.entries(DATA))s.setItem(k,v);})();""".replace('DATA',json.dumps(seeds)))
  c.route('**/*',lambda r:r.continue_() if r.request.url.startswith(self.url.rsplit('/',1)[0]) else r.abort())
  p=c.new_page();p.set_default_timeout(90000);p.on('dialog',lambda d:d.accept());errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(self.url,timeout=180000);p.wait_for_function('MA5.appReady===true',timeout=180000)
  try:yield p,c,errors
  finally:
   if __import__('sys').exc_info()[0]:
    print('DIAGNOSTICO',p.evaluate('({guard:MA5.guardFailure,restore:document.querySelector("#ma5-restore-status")?.textContent,backup:document.querySelector("#backup-message")?.textContent})'),flush=True);p.screenshot(path=str(self.out/'falha.png'),full_page=True)
   self.check('AUX-PAGEERROR-'+str(len(self.checks)),not errors,errors)
   native=p.evaluate("""()=>{const f=document.createElement('iframe');document.body.append(f);const s=f.contentWindow.localStorage,keys=KEYS;const o={sent:Object.fromEntries(keys.map(k=>[k,s.getItem(k)])),extra:Array.from({length:s.length},(_,i)=>s.key(i)).filter(k=>!k.startsWith('__MA_DEV61_SANDBOX__:')&&!keys.includes(k))};f.remove();return o;}""".replace('KEYS',json.dumps(list(SENT))))
   self.check('AUX-ISOLAMENTO-'+str(len(self.checks)),native['sent']==SENT and not native['extra'],native);c.close()
 def state(self,p):return p.evaluate('MA5.localEntries().filter(x=>!MA5.transient(x.key))')
 def get(self,p,k):return p.evaluate('(k)=>localStorage.getItem(k)',k)
 def dl(self,p,selector,name=None):
  with p.expect_download(timeout=90000) as event:p.locator(selector).evaluate('(e)=>e.click()')
  d=event.value;self.seq+=1;file=self.out/'downloads'/(str(self.seq)+'-'+(name or d.suggested_filename));file.parent.mkdir(exist_ok=True,parents=True);d.save_as(file);assert not d.failure();return file
 def preview(self,p,file):
  p.evaluate('go("backup")');p.locator('#backup-load').set_input_files(str(file));p.wait_for_function('MA5.pendingPreview!==null || document.querySelector("#ma5-restore-status").textContent.includes("RECUSADA")');return p.locator('#ma5-restore-status').text_content()
 def fixture(self,name,data):
  f=self.out/name;f.write_text(json.dumps(data,ensure_ascii=False,indent=2));return f
 def restore(self,p,file):
  text=self.preview(p,file);assert p.evaluate('MA5.pendingPreview!==null'),text
  with p.expect_navigation(wait_until='load',timeout=90000):p.locator('#ma5-restore-confirm').click()
  p.wait_for_function('MA5.appReady===true',timeout=180000);return True
 def backup(self,p):p.evaluate('go("backup")');return self.dl(p,'#backup-save')
 def filecheck(self):
  c=self.b.new_context();p=c.new_page()
  try:p.goto(HTML.as_uri(),timeout=30000);p.wait_for_function('MA5.appReady',timeout=30000);status='file:// disponível'
  except Exception as e:status=str(e).splitlines()[0]
  finally:c.close()
  self.check('METODO-FILE-OU-BLOQUEIO-DOCUMENTADO','file:// disponível' in status or 'ERR_BLOCKED_BY_ADMINISTRATOR' in status,status)
 def unified(self):
  q='ma-ledger-v1-rejeitados-20260101';body=json.dumps({'rows':[{'index':2,'row':None}]});review='ma-ledger-v1-quarantine-review:'+q
  with self.context({q:body,review:json.dumps({'version':1,'key':q,'originalBody':body,'reviewedAt':'2026-10-10','acknowledged':True}),'ma-ledger-v1-prev':'ANTERIOR-FICTICIO','ma-ledger-v1-session-prev-antiga':'[ ]'}) as (p,c,e):
   before=self.state(p);f=self.backup(p);bk=json.loads(f.read_text())
   self.check('BKP02-UNIFICADO-TODAS-BASES',bk['version']==3 and bk['coverage']['status']=='COMPLETO_ESTADO_PERSISTIDO' and {x['key']:x['raw'] for x in bk['state']}=={x['key']:x['raw'] for x in before})
   self.check('BKP02-LAB-CHECKLISTS-QUARENTENAS',all(k in [x['key'] for x in bk['state']] for k in ['ma-academy-v55','ma56-project-checklist-v1','ma61-sanitary-checklist-v1',q,review]))
   self.check('BACKUP-SOLICITADO-NAO-VERIFICADO','SOLICITADO' in p.locator('#backup-message').text_content() and 'NÃO verificado' in p.locator('#backup-message').text_content())
   p.locator('#ma62-verify-backup').set_input_files(str(f));p.wait_for_function('document.querySelector("#backup-message").textContent.includes("ARQUIVO VERIFICADO")');self.check('BACKUP-ARQUIVO-EFETIVAMENTE-VERIFICADO','ARQUIVO VERIFICADO' in p.locator('#backup-message').text_content())
   filebad=self.fixture('arquivo-alterado.json',bk|{'appVersion':'alterado'});baseline=self.state(p);msg=self.preview(p,filebad)
   self.check('BACKUP-HASH-ERRADO-RECUSADO',p.evaluate('MA5.pendingPreview===null') and self.state(p)==baseline and 'Integridade' in msg,msg)
   # Altera bases reais do perfil fictício para testar restauração byte a byte.
   for k,v in [('ma-care-v2',json.dumps(care('B'))),('ma-ledger-v1',json.dumps([row(2)])),('ma-academy-v55',json.dumps(academy('B')))]:p.evaluate('([k,v])=>localStorage.setItem(k,v)',[k,v])
   ok=self.restore(p,f);self.check('RESTAURAR-V3-TODAS-BASES',ok and self.state(p)==before)
   histories=p.evaluate('MA5.all()');journals=[x for x in histories if x['kind']=='restore'];self.check('P17B-PREIMAGE-INTEGRAL',len(journals)==1 and journals[0]['phase']=='committed' and any(x['key']=='ma-care-v2' and json.loads(x['raw'])==care('B') for x in json.loads(journals[0]['raw'])['preimage']))
   stored=self.get(p,'ma-care-v2');p.reload();p.wait_for_function('MA5.appReady===true');self.check('B123-SEM-REINJECAO',self.get(p,'ma-care-v2')==stored and json.loads(stored)==care())
   p.evaluate('go("backup")');p.locator('#ma5-restore-panel details summary').click();p.locator('#ma5-restore-journals button').first.click();p.wait_for_function('MA5.pendingPreview!==null')
   with p.expect_navigation(wait_until='load'):p.locator('#ma5-restore-confirm').click()
   p.wait_for_function('MA5.appReady===true');self.check('A148-RECUPERAR-ESTADO-ANTERIOR',json.loads(self.get(p,'ma-care-v2'))==care('B') and json.loads(self.get(p,'ma-ledger-v1'))==[row(2)])
 def legacy(self):
  with self.context() as (p,c,e):
   old=self.state(p);payload=dict(format='manfrin-arnez-backup',version=2,care=care('LEGADO'),ledger=[row(1,id=123,bank='Itau',amount=1000.5,extra='preservado'),row(2,id='123')],rateSettings={'5':'3.1'})
   f=self.fixture('backup-v2-ficticio.json',payload);msg=self.preview(p,f);self.check('V2-PREVIA-NAO-ALTERA',self.state(p)==old and 'Legado v2 sem hash' in msg and 'SUBSTITUIR' in p.locator('#ma5-restore-preview').text_content())
   p.locator('#ma5-restore-cancel').click();self.check('V2-CANCELAR-MANTEM-TUDO',self.state(p)==old)
   ok=self.restore(p,f);self.check('B119-V2-LEGADO-NUMERICO-BANCO-VALOR',ok and json.loads(self.get(p,'ma-ledger-v1'))==payload['ledger'] and json.loads(self.get(p,'ma-care-v2'))==payload['care'])
   self.check('V2-MODULOS-ADMIN-AUSENTES-MANTIDOS',all(self.get(p,x['key'])==x['raw'] for x in old if x['key'] in ['ma-academy-v55','ma56-project-checklist-v1','ma61-sanitary-checklist-v1']))
   p.wait_for_function('document.querySelector("#ma5-restore-status").textContent.startsWith("Última restauração:")');receipt=p.locator('#ma5-restore-status').text_content();counts=json.loads(receipt.split('Contagens/ações: ',1)[1]);a=next(x for x in counts if x['key']=='ma-academy-v55');self.check('RESULTADO-CONTAGENS-MODULO-MANTIDO-REAIS',a['after']==a['before'] and a['after']['materials']==1 and a['file']=={'absent':True})
   self.check('LEGADO-CATEGORIA-TOTAIS-PRESERVADOS',p.evaluate('Finance.aggregate(rows,"").revenue')==2002.5 and p.evaluate('rows[0].id===123'))
   backup=self.backup(p);self.check('N2-V3-INCLUI-NUMERICOS',json.loads(backup.read_text())['coverage']['status']=='COMPLETO_ESTADO_PERSISTIDO')
   # v2 parcial: care ausente deve preservar pacientes, pagamentos e evoluções.
   current=self.get(p,'ma-care-v2');partial=self.fixture('v2-parcial-livro.json',{'format':'manfrin-arnez-backup','version':2,'ledger':[row(99)]});ok=self.restore(p,partial)
   self.check('V2-PARCIAL-CARE-AUSENTE-PRESERVADO',ok and self.get(p,'ma-care-v2')==current)
   before=self.state(p);wrong=self.fixture('v2-versao99.json',payload|{'version':99});msg=self.preview(p,wrong);self.check('VERSAO-DESCONHECIDA-RECUSADA',self.state(p)==before and p.evaluate('MA5.pendingPreview===null') and 'não suportada' in msg,msg)
 def partial(self):
  with self.context({'ma-care-v2':'{"version":99,"marker":"FICTICIO-INTEGRAL"}','checklist56':'{"versao_antiga":55,"bytes":"FICTICIOS"}'}) as (p,c,e):
   original=self.get(p,'ma-care-v2');f=self.backup(p);bk=json.loads(f.read_text());self.check('CARE-ILEGIVEL-BACKUP-PARCIAL-SEM-SEED',bk['coverage']['status']=='PARCIAL' and next(x['raw'] for x in bk['state'] if x['key']=='ma-care-v2')==original and self.get(p,'ma-care-v2')==original)
   self.check('CHECKLIST56-OPACO-INCLUIDO',any(x['key']=='checklist56' and x['raw']=='{"versao_antiga":55,"bytes":"FICTICIOS"}' for x in bk['state']) and any('checklist56' in s for s in bk['coverage']['warnings']))
  with self.context(remove=['ma-care-v2','ma-academy-v55','ma61-sanitary-checklist-v1']) as (p,c,e):
   f=self.backup(p);bk=json.loads(f.read_text());self.check('BASES-AUSENTES-IDENTIFICADAS-NAO-INVENTADAS',set(['ma-care-v2','ma-academy-v55','ma61-sanitary-checklist-v1']).issubset(bk['coverage']['absent']) and self.get(p,'ma-care-v2') is None)
  with self.context({'ma-ledger-v1':'[{"truncado":'}) as (p,c,e):
   original=self.get(p,'ma-ledger-v1');f=self.backup(p);bk=json.loads(f.read_text());self.check('LIVRO-JSON-CORROMPIDO-PRESERVADO-EM-PARCIAL',bk['coverage']['status']=='PARCIAL' and next(x['raw'] for x in bk['state'] if x['key']=='ma-ledger-v1')==original)
   raw=self.dl(p,'#ma5-export-ledger-raw');self.check('N2-BRUTO-CORROMPIDO-EXATO',raw.read_text()==original)
 def recoveryedge(self):
  with self.context(remove=['ma-care-v2']) as (p,c,e):
   before=self.state(p);f=self.fixture('care-adicionado.json',{'format':'manfrin-arnez-backup','version':2,'care':care('NOVO')});self.restore(p,f)
   self.check('RESTAURO-BASE-ANTES-AUSENTE-ADICIONADA',self.get(p,'ma-care-v2') is not None)
   p.evaluate('go("backup")');p.locator('#ma5-restore-panel details summary').click();p.locator('#ma5-restore-journals button').first.click();p.wait_for_function('MA5.pendingPreview!==null')
   self.check('RECUPERACAO-PREVIA-IDENTIFICA-REMOCAO-BASE-ADICIONADA','REMOVER BASE ADICIONADA' in p.locator('#ma5-restore-preview').text_content())
   with p.expect_navigation(wait_until='load'):p.locator('#ma5-restore-confirm').click()
   p.wait_for_function('MA5.appReady===true');self.check('RECUPERACAO-ESTADO-ANTERIOR-INCLUSIVE-AUSENCIA',self.state(p)==before and self.get(p,'ma-care-v2') is None)
  with self.context() as (p,c,e):
   f=self.backup(p);bk=json.loads(f.read_text());current=self.get(p,'ma-care-v2');bad='{"version":99,"ficticio":true}'
   for x in bk['state']:
    if x['key']=='ma-care-v2':x['raw']=bad;x['sha256']=hashlib.sha256(bad.encode()).hexdigest()
    if x['key']=='ma-ledger-v1':x['raw']=json.dumps([row(60)]);x['sha256']=hashlib.sha256(x['raw'].encode()).hexdigest()
   text=json.dumps(bk);sealed=p.evaluate('async text=>{const x=JSON.parse(text);delete x.integrity;return JSON.stringify({...x,integrity:{algorithm:"SHA-256",digest:await MA5.sha(MA5.canonical(x))}})}',text);f=self.out/'parcial-care-ilegivel.json';f.write_text(sealed);self.restore(p,f)
   self.check('RESTAURO-PARCIAL-BASE-ILEGIVEL-MANTEM-CURRENT',self.get(p,'ma-care-v2')==current and json.loads(self.get(p,'ma-ledger-v1'))==[row(60)])
   self.check('RESTAURO-PARCIAL-BYTES-IGNORADOS-PROTEGIDOS',p.evaluate('(bad)=>MA5.all().then(a=>a.some(x=>x.kind==="restore"&&JSON.parse(x.raw).skipped.some(t=>t.raw===bad)))',bad))
  q='ma-ledger-v1-rejeitados-FICTICIO-CONFLITO'
  with self.context({q:'QUARENTENA-FICTICIA-ORIGINAL'}) as (p,c,e):
   f=self.backup(p);bk=json.loads(f.read_text());baseline=self.state(p)
   for x in bk['state']:
    if x['key']==q:x['raw']='OUTRA-QUARENTENA-FICTICIA';x['sha256']=hashlib.sha256(x['raw'].encode()).hexdigest()
   text=p.evaluate('async text=>{const x=JSON.parse(text);delete x.integrity;return JSON.stringify({...x,integrity:{algorithm:"SHA-256",digest:await MA5.sha(MA5.canonical(x))}})}',json.dumps(bk));f=self.out/'conflito-quarentena.json';f.write_text(text);msg=self.preview(p,f)
   self.check('QUARENTENA-CONFLITO-RECUSA-SEM-SOBRESCREVER',self.state(p)==baseline and p.evaluate('MA5.pendingPreview===null') and 'Conflito de proteção' in msg,msg)
 def failure(self):
  with self.context() as (p,c,e):
   initial=self.state(p);f=self.fixture('restauracao-falha.json',{'format':'manfrin-arnez-backup','version':2,'care':care('FALHA'),'ledger':[row(5)],'rateSettings':{'5':1}});self.preview(p,f)
   p.evaluate("""()=>{const original=localStorage.setItem;window.origA5Set=original;let failed=false;localStorage.setItem=(k,v)=>{if(k==='ma-ledger-v1'&&!failed){failed=true;throw new DOMException('Falha fictícia durante restauração','QuotaExceededError');}return original.call(localStorage,k,v);};}""")
   p.locator('#ma5-restore-confirm').click();p.wait_for_function('document.querySelector("#ma5-restore-status").textContent.includes("FALHOU")');self.check('FALHA-MEIO-RESTAURACAO-ROLLBACK-EXATO',self.state(p)==initial and self.get(p,'ma5-restore-pending-v1') is None,p.locator('#ma5-restore-status').text_content())
   self.check('FALHA-PREIMAGE-RECUPERAVEL',p.evaluate('MA5.all().then(a=>a.some(x=>x.kind==="restore"&&x.phase==="rolledback"))'))
   p.reload();p.wait_for_function('MA5.appReady===true');self.check('FALHA-REABRIR-SEM-PERDA-OU-SEED',self.state(p)==initial)
   # Interrupção após journal comprometido e primeiro módulo aplicado.
   self.preview(p,f)
   p.evaluate("""async()=>{await MA5.lock(()=>MA5.singleTab(async()=>{const j=await MA5.prepareRestore(MA5.pendingPreview);window.crashJournal=j.id;MA5.managedWrite('ma-care-v2',JSON.parse(j.raw).targets.find(x=>x.key==='ma-care-v2').raw);}));}""")
   self.check('INTERRUPCAO-ESTADO-INTERMEDIARIO',self.get(p,'ma5-restore-pending-v1') is not None and json.loads(self.get(p,'ma-care-v2'))==care('FALHA'))
   p.reload();p.wait_for_function('MA5.appReady===true',timeout=180000);self.check('INTERRUPCAO-RECARGA-RECUPERA-ANTES',self.state(p)==initial and self.get(p,'ma5-restore-pending-v1') is None)
  with self.context() as (p,c,e):
   before=self.get(p,'ma-ledger-v1');p.evaluate('()=>{MA5.captureOperation=async()=>{throw new DOMException("Cota fictícia IndexedDB","QuotaExceededError")}}');ok=p.evaluate('ma62ApplyCorrection(0,"description","não deve gravar")')
   self.check('IDB-FALHA-PROTECAO-BLOQUEIA-OPERACAO',ok is False and self.get(p,'ma-ledger-v1')==before)
   self.check('IDB-FALHA-PROTECAO-ALERTA-REAL',p.locator('#ma62-ledger-alert').count()==1 and 'histórico indisponível' in p.locator('#ledger-message').text_content())
 def tabs(self):
  with self.context() as (a,c,e):
   b=c.new_page();b.set_default_timeout(90000);b.on('dialog',lambda d:d.accept());b.on('pageerror',lambda x:e.append(str(x)));b.goto(self.url);b.wait_for_function('MA5.appReady===true')
   before=self.state(a);f=self.fixture('duas-abas.json',{'format':'manfrin-arnez-backup','version':2,'care':care('DUAS'),'ledger':[row(5)]});self.preview(a,f);a.locator('#ma5-restore-confirm').click();a.wait_for_function('document.querySelector("#ma5-restore-status").textContent.includes("FALHOU")');self.check('DUAS-ABAS-RESTAURO-RECUSADO-SEM-MUTACAO',self.state(a)==before and 'Outra aba' in a.locator('#ma5-restore-status').text_content())
   a.evaluate('ma62ApplyCorrection(0,"description","Aba A fictícia")');original=self.get(a,'ma-ledger-v1');result=b.evaluate('ma62ApplyCorrection(0,"description","Aba B desatualizada")');self.check('DUAS-ABAS-LIVRO-NAO-SOBRESCREVE',result is False and self.get(a,'ma-ledger-v1')==original)
   b.close();self.check('UMA-ABA-PODE-RESTAURAR',self.restore(a,f))
 def volume(self):
  for n in [6500,12000]:
   with self.context({'ma-ledger-v1':json.dumps([row(i) for i in range(n)])}) as (p,c,e):
    before=self.get(p,'ma-ledger-v1');result=p.evaluate("""async()=>{for(let i=0;i<5;i++)if(!await ma62ApplyCorrection(0,'description','Volume fictício '+i))return false;return {rows:rows.length,history:(await MA5.all()).length};}""")
    self.check('VOLUME-'+str(n),result and result['rows']==n and result['history']==5,result)
    self.check('VOLUME-ORIGINAL-RECUPERAVEL-'+str(n),p.evaluate('(raw)=>MA5.all().then(a=>a.some(x=>x.raw===raw))',before))
    f=self.backup(p);self.check('VOLUME-BACKUP-COM-HISTORICO-'+str(n),len(json.loads(f.read_text())['protection'])==5)
 def safety(self):
  with self.context() as (p,c,e):
   initial=self.get(p,'ma-ledger-v1');clinical=self.get(p,'ma-care-v2')
   p.evaluate('ma62ApplyCorrection(0,"description","Primeira fictícia")');p.evaluate('ma62ApplyCorrection(0,"description","Segunda fictícia")')
   p.evaluate('go("backup")');archive=self.dl(p,'#ma5-history-export');p.locator('#ma5-history-verify').set_input_files(str(archive));p.wait_for_function('MA5.verifiedArchive!==null')
   ids=p.evaluate('MA5.history().then(a=>a.filter(x=>x.kind==="operation").slice(0,1).map(x=>x.storage+":"+x.id))');p.evaluate('(ids)=>MA5.deleteVerified(ids)',ids)
   self.check('RETENCAO-COMPROVANTE-EXTERNO-PERSISTIDO',p.evaluate('MA5.all().then(a=>a.some(x=>x.kind==="cleanup"))'))
   f=self.backup(p);bk=json.loads(f.read_text());self.check('RETENCAO-BACKUP-PARCIAL-INDICA-ARQUIVO-EXTERNO',bk['coverage']['status']=='PARCIAL' and bk['coverage']['separateExports'][0]['sha256']==hashlib.sha256(archive.read_bytes()).hexdigest())
   p.locator('#ma5-archive-record').select_option('0');p.locator('#ma5-archive-recover').click();p.wait_for_function('MA5.pendingPreview!==null')
   with p.expect_navigation(wait_until='load'):p.locator('#ma5-restore-confirm').click()
   p.wait_for_function('MA5.appReady===true');self.check('RETENCAO-RECUPERA-ESTADO-EXTERNO-EXCLUIDO',self.get(p,'ma-ledger-v1')==initial and self.get(p,'ma-care-v2')==clinical)
   # Um snapshot após a limpeza deve ser importável mesmo com referências históricas
   # a cópias que agora vivem no arquivo externo.
   self.check('RETENCAO-SNAPSHOT-POS-LIMPEZA-IMPORTAVEL',bool(p.evaluate('(text)=>MA5.inspectText(text).then(x=>x.version===3)',f.read_text())))
  with self.context({'ma-academy-v55':'{"version":99,"marker":"FICTICIO-PRESERVADO"}'}) as (p,c,e):
   before=self.get(p,'ma-academy-v55');p.evaluate('go("ma55-cost")');p.locator('#m55-monthly').fill('100');p.locator('#m55-hours').fill('20');p.locator('#m55-config-save').click();self.check('P10-VERSAO-ACADEMIA-DESCONHECIDA-NAO-SOBRESCREVE',self.get(p,'ma-academy-v55')==before)
   f=self.backup(p);self.check('VERSAO-ACADEMIA-DESCONHECIDA-RAW-PARCIAL',json.loads(f.read_text())['coverage']['status']=='PARCIAL' and any(x['raw']==before for x in json.loads(f.read_text())['state']))
  with self.context() as (p,c,e):
   # Saturação REAL, apenas de chaves fictícias dentro do sandbox. Nunca clear().
   p.evaluate("""()=>{let n=0;for(const size of [200000,50000,5000,500,50,5,1])for(;;){try{localStorage.setItem('ma-ledger-v1-session-prev-FICTICIO-COTA-'+n,'x'.repeat(size));n++;}catch(e){if(e.name!=='QuotaExceededError')throw e;break;}}return n;}""")
   baseline=self.state(p);f=self.fixture('cota-restaura.json',{'format':'manfrin-arnez-backup','version':2,'care':care('COTA'),'ledger':[row(20)]});self.preview(p,f);p.locator('#ma5-restore-confirm').click();p.wait_for_function('document.querySelector("#ma5-restore-status").textContent.includes("FALHOU")')
   self.check('COTA-REAL-RESTAURACAO-RECUSA-ANTES-DADOS',self.state(p)==baseline and self.get(p,'ma5-restore-pending-v1') is None,p.locator('#ma5-restore-status').text_content())
   self.check('COTA-REAL-PREIMAGE-RETIDA',p.evaluate('MA5.all().then(a=>a.some(x=>x.kind==="restore"&&x.phase==="refused"))'))
 def routes(self):
  bad='{bad json FICTICIO';q='ma-ledger-v1-rejeitados-FICTICIO-ROTAS';body='{"rows":[{"ficticio":true}]}'
  with self.context({'ma-care-v2':bad,q:body}) as (p,c,e):
   before=self.state(p);f=self.backup(p);a=json.loads(f.read_text());p.evaluate('go("accounting")');g=self.dl(p,'#ma53-account-backup');b=json.loads(g.read_text())
   self.check('AJ11-B100-ROTAS-CADASTRO-ILEGIVEL-PARCIAL-EXATO',a['coverage']['status']==b['coverage']['status']=='PARCIAL' and a['state']==b['state'] and any(x['key']=='ma-care-v2' and x['raw']==bad for x in b['state']) and self.state(p)==before)
   msg=p.locator('#ma53-recovery-status').text_content();self.check('AJ11-CONTABILIDADE-SOLICITADO-NAO-VERIFICADO','SOLICITADO' in msg and 'NÃO verificado' in msg,msg)
   p.evaluate('go("backup")');h=self.dl(p,'#ma62-export-care-raw');self.check('AJ12B-CADASTRO-BRUTO-EXATO',h.read_text()==bad and self.get(p,'ma-care-v2')==bad)
   changed=self.out/'verificador-um-espaco.json';changed.write_text(g.read_text()+' ');p.locator('#ma62-verify-backup').set_input_files(str(changed));p.wait_for_function('document.querySelector("#backup-message").textContent.includes("NÃO VERIFICADO")');self.check('AJ11-VERIFICADOR-RECUSA-BYTES-DIFERENTES','não corresponde' in p.locator('#backup-message').text_content())
  with self.context() as (p,c,e):
   text=p.evaluate('MA5.completeBackup().then(x=>JSON.stringify(x))');h=self.out/'sem-pedir-download.json';h.write_text(text);p.evaluate('go("backup")');p.locator('#ma62-verify-backup').set_input_files(str(h));p.wait_for_function('document.querySelector("#backup-message").textContent.includes("NÃO VERIFICADO")');self.check('AJ11-VERIFICADOR-SEM-DOWNLOAD-RECUSA','Solicite um backup' in p.locator('#backup-message').text_content())
 def nearfull(self):
  with self.context() as (p,c,e):
   freed=p.evaluate("""()=>{let n=0,releaseKey='FICTICIO-COTA-TRANSITORIO-LIBERAVEL';localStorage.setItem(releaseKey,'x'.repeat(500));for(const size of [200000,50000,5000,500,50,5,1])for(;;){try{const key='FICTICIO-COTA-TRANSITORIO-'+n;localStorage.setItem(key,'x'.repeat(size));n++;}catch(e){if(e.name!=='QuotaExceededError')throw e;break;}}if(!releaseKey)throw Error('Fixture sem fragmento de 500 caracteres');localStorage.removeItem(releaseKey);return releaseKey;}""")
   baseline=self.state(p);f=self.fixture('cota-reserva-ficticia.json',{'format':'manfrin-arnez-backup','version':2,'ledger':[row(i) for i in range(500)]});msg=self.preview(p,f);assert p.evaluate('MA5.pendingPreview!==null'),msg;p.locator('#ma5-restore-confirm').click();p.wait_for_function('document.querySelector("#ma5-restore-status").textContent.includes("FALHOU")')
   self.check('COTA-QUASE-CHEIA-RESERVA-RECUSA-ROLLBACK',self.state(p)==baseline and self.get(p,'ma5-restore-pending-v1') is None,p.locator('#ma5-restore-status').text_content())
   self.check('COTA-QUASE-CHEIA-JOURNAL-RECUPERAVEL',p.evaluate('MA5.all().then(a=>a.some(x=>x.kind==="restore"&&x.phase==="rolledback"))'))
 def regression(self):
  with self.context() as (p,c,e):
   pages=p.locator('nav button').evaluate_all('(a)=>a.map(x=>x.dataset.page)');bad=[]
   for id in pages:
    p.evaluate('(id)=>go(id)',id)
    if not p.locator('#'+id).is_visible() or not p.locator('#'+id).text_content().strip():bad.append(id)
   self.check('REGRESSAO-18-TELAS',len(pages)==18 and not bad,pages)
   p.evaluate('go("patients")');p.locator('#new-patient').click();p.locator('#patient-form [name=name]').fill('Paciente Novo Fictício A5');p.locator('#patient-form button.primary').click();self.check('REGRESSAO-CADASTRO',any(x['name']=='Paciente Novo Fictício A5' for x in json.loads(self.get(p,'ma-care-v2'))['patients']))
   p.locator('#use-patient').click();f=p.locator('#payment-form');f.locator('[name=date]').fill('2026-10-11');f.locator('[name=amount]').fill('123.45');f.locator('[name=service]').fill('Pagamento A5');f.locator('button.primary').click();self.check('REGRESSAO-PAGAMENTO',any(x['service']=='Pagamento A5' for x in json.loads(self.get(p,'ma-care-v2'))['records']))
   p.evaluate('go("accounting")');f=self.dl(p,'#account-export');self.check('REGRESSAO-CSV-CONTABIL',b'123,45' in f.read_bytes() and b'Pagamento A5' in f.read_bytes())
   p.evaluate('go("sim")');before=p.locator('#result').text_content();p.locator('#sale').fill('4000');self.check('REGRESSAO-SIMULADOR',p.locator('#result').text_content()!=before and p.locator('#ma53-rates-table input').count()==10)
   self.check('REGRESSAO-EVOLUCOES',care()['notes'][0] in json.loads(self.get(p,'ma-care-v2'))['notes'])
   p.evaluate('go("ma61-sanitary")');self.check('REGRESSAO-SANITARIA-8-42',p.locator('.ma61-group').count()==8 and p.locator('.ma61-item').count()==42)
   f=self.dl(p,'#ma61-export');p.locator('#ma61-import').set_input_files(str(f));self.check('REGRESSAO-SANITARIA-IDAEVOLTA',json.loads(f.read_text())['data']==json.loads(self.get(p,'ma61-sanitary-checklist-v1')))
   p.evaluate('go("ma55-cost")');f=self.dl(p,'#m55-export');p.locator('#m55-import').set_input_files(str(f));self.check('REGRESSAO-ACADEMIA-LAB-PRESERVADOS',json.loads(self.get(p,'ma-academy-v55'))==academy())
   p.evaluate('go("ma55-academy")');p.locator('#ma59-open').click();p.locator('#ma59-workshop [data-piece=crown]').click();f=self.dl(p,'#ma59-workshop button[data-doc=exocad]');self.check('REGRESSAO-EXOCAD-PDF',f.read_bytes().startswith(b'%PDF-'))
   # XSS em paciente/lançamento: importação v2 mantém os textos, não os executa.
   evil=care('XSS');evil['patients'][0]['name']='<img src=x onerror="window.xssA5=1">';evil['records'][0]['snapshot']['name']=evil['patients'][0]['name'];f=self.fixture('xss-ficticio.json',{'format':'manfrin-arnez-backup','version':2,'care':evil,'ledger':[row(1,description='<svg onload="window.xssA5=1"></svg>')]});self.restore(p,f)
   for id in pages:p.evaluate('(id)=>go(id)',id)
   self.check('SEGURANCA-HTML-MALICIOSO',p.evaluate('window.xssA5===undefined') and p.locator('#transactions svg').count()==0)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--group',choices=['filecheck','unified','legacy','partial','failure','recoveryedge','tabs','volume','safety','nearfull','routes','regression']);parser.add_argument('--from-group',choices=['failure','recoveryedge','tabs','volume','safety','nearfull','routes','regression']);args=parser.parse_args();out=ROOT/('resultados-a5-'+args.group if args.group else 'resultados-a5');out.mkdir(exist_ok=True)
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();failure=None;suite=None
 try:
  with sync_playwright() as pw:
   b=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_BIN','/usr/bin/chromium'),headless=True,args=['--no-sandbox']);suite=Suite(b,f'http://127.0.0.1:{server.server_port}/{HTML.name}',out)
   groups=['filecheck','unified','legacy','partial','failure','recoveryedge','tabs','volume','safety','nearfull','routes','regression']
   if args.from_group:groups=groups[groups.index(args.from_group):]
   for group in [args.group] if args.group else groups:
    print('GRUPO',group,flush=True);getattr(suite,group)()
   b.close()
 except Exception as e:traceback.print_exc();failure=str(e)
 finally:
  server.shutdown();server.server_close();result=dict(html_sha256=hashlib.sha256(HTML.read_bytes()).hexdigest(),group=args.group or ('from-'+args.from_group if args.from_group else 'all'),failure=failure,checks=suite.checks if suite else []);result['counts']={s:sum(x['status']==s for x in result['checks']) for s in ['APROVADO','REPROVADO']};(out/'resultados.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(result['counts'],flush=True)
 raise SystemExit(1 if failure else 0)
if __name__=='__main__':main()
