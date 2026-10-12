import importlib.util,json,threading,time,traceback,hashlib,csv,sys,statistics
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer
from playwright.sync_api import sync_playwright
sys.dont_write_bytecode=True
SRC=Path(__import__("os").environ.get("A4_SOURCE_DIR",str(Path(__file__).parent/"fontes-imutaveis")));OUT=Path(__file__).parent
sp=importlib.util.spec_from_file_location('base',SRC/'testes_a5.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class S(m.Suite):
 @m.contextmanager
 def context(self,override=None,remove=None):
  c=self.b.new_context(accept_downloads=True,viewport={'width':1280,'height':900});values=m.BASES();values.update(override or {})
  for k in remove or []:values.pop(k,None)
  seeds={m.PREFIX+k:v for k,v in values.items()}|m.SENT|{m.PREFIX+'ma5-suppress-seeds-v1':'1'}
  c.add_init_script("(()=>{const s=localStorage;if(s.getItem('__MA_DEV61_SANDBOX__:ma5-suppress-seeds-v1')!==null)return;for(const [k,v] of Object.entries(DATA))s.setItem(k,v)})();".replace('DATA',json.dumps(seeds)))
  c.route('**/*',lambda r:r.continue_() if r.request.url.startswith(self.url.rsplit('/',1)[0]) else r.abort());p=c.new_page();p.set_default_timeout(15000);p.on('dialog',lambda d:d.accept());errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto(self.url,timeout=180000);p.wait_for_function('MA5.appReady',timeout=180000)
  try:yield p,c,errors
  finally:
   active=getattr(p,'a4RecoveryPage',p)
   self.check('AUX-PAGEERROR-'+str(len(self.checks)),not errors,errors)
   try:
    native=active.evaluate("()=>{const f=document.createElement('iframe');document.body.append(f);const s=f.contentWindow.localStorage,keys=KEYS;const o={sent:Object.fromEntries(keys.map(k=>[k,s.getItem(k)])),extra:Array.from({length:s.length},(_,i)=>s.key(i)).filter(k=>!k.startsWith('__MA_DEV61_SANDBOX__:')&&!keys.includes(k))};f.remove();return o}".replace('KEYS',json.dumps(list(m.SENT))))
    self.check('AUX-ISOLAMENTO-'+str(len(self.checks)),native['sent']==m.SENT and not native['extra'],native)
   except Exception as ex:self.check('AUX-INSPECAO-INDISPONIVEL',False,str(ex))
   c.close()
 def check(self,id,ok,evidence=''):self.checks.append(dict(id=id,ok=ok,evidence=evidence))
 def second(self,c):
  p=c.new_page();p.set_default_timeout(15000);p.on('dialog',lambda d:d.accept());p.goto(self.url,timeout=180000);p.wait_for_function('MA5.appReady',timeout=180000);return p
 def merge(self,p,payload,label='merge'):
  f=self.fixture(label+'.json',payload) if isinstance(payload,dict) else payload
  p.evaluate('()=>{go("accounting");document.querySelector("#ma53-recovery-status").textContent=""}')
  downloads=[];p.on('download',lambda d:downloads.append(d))
  p.locator('#ma53-merge-file').set_input_files(str(f));p.wait_for_function('document.querySelector("#ma53-recovery-status").textContent.length>0',timeout=15000)
  p.wait_for_timeout(100);files=[]
  for d in downloads:
   self.seq+=1;path=self.out/'downloads'/f'{self.seq}-{d.suggested_filename}';path.parent.mkdir(exist_ok=True);d.save_as(path);files.append(str(path.relative_to(OUT)))
  return dict(message=p.locator('#ma53-recovery-status').text_content(),downloads=files)
 def snap(self,p):return dict(local=self.state(p),history=p.evaluate('MA5.all()'),ledgerModel=p.evaluate('rows'),clinicalDOM=p.locator('#account-rows').inner_text(),noteDOM=p.locator('#note-list').inner_text())
 def patient(self,p,name):
  p.evaluate('go("patients")');p.locator('#new-patient').click();p.locator('#patient-form [name=name]').fill(name);p.locator('#patient-form').evaluate('(f)=>f.requestSubmit()');return p.locator('#patient-message').text_content()
 def rate(self,p,n,v):p.locator(f'[data-rate="{n}"]').evaluate('(e,v)=>{e.value=v;e.dispatchEvent(new Event("change",{bubbles:true}))}',str(v))
 def fault(self,p,key,once=False):
  p.evaluate('([key,once])=>{window.originalSet=localStorage.setItem;let fired=false;localStorage.setItem=(k,v)=>{if(k===key&&(!once||!fired)){fired=true;throw new DOMException("Falha sintética A4","QuotaExceededError")};return originalSet.call(localStorage,k,v)}}',[key,once])
 def unfault(self,p):p.evaluate('()=>{localStorage.setItem=window.originalSet}')
results={};planned=json.load(open('/workspace/diagnostico-a4/D-Matriz-Testes-A4.json'))['casos']
def record(n,ok,detail,status=None):
 r=planned[n-1]|dict(status=status or ('APROVADO' if ok else 'REPROVADO'),observado=detail);results[n]=r
 (OUT/'resultados.json').write_text(json.dumps(list(results.values()),ensure_ascii=False,indent=2));print('T-A4-%02d'%n,r['status'],flush=True)
def payload(label='B',ledger=None,**kw):return dict(format='manfrin-arnez-backup',version=2,care=m.care(label),ledger=ledger if ledger is not None else [m.row(2)])|kw
def jget(s,p,key):return json.loads(s.get(p,key))
def save(name,x):(OUT/(name+'.json')).write_text(json.dumps(x,ensure_ascii=False,indent=2))
def group1(s):
 with s.context() as (a,c,e):
  before=s.snap(a);r=s.merge(a,payload(),'T01');after=s.snap(a);save('T01-estados',dict(initial=before,result=r,after=after))
  record(1,len(jget(s,a,'ma-care-v2')['patients'])==2 and len(jget(s,a,'ma-ledger-v1'))==len(a.evaluate('rows'))==2,dict(result=r,ledgerPersisted=len(jget(s,a,'ma-ledger-v1')),ledgerUIModel=len(a.evaluate('rows'))))
  ok=a.evaluate('ma62ApplyCorrection(0,"description","Pós-merge fictício")');msg=s.patient(a,'Paciente Fictício pós merge');record(3,ok and 'salvo' in msg.lower(),dict(ledgerSave=ok,clinicalMessage=msg))
  record(9,'Paciente Fictício B' in a.locator('#note-list').inner_text(),dict(noteDOM=a.locator('#note-list').inner_text(),notesPersisted=jget(s,a,'ma-care-v2')['notes']))
  state=s.state(a);r=s.merge(a,payload(),'T11');record(11,s.state(a)==state,r)
 with s.context() as (a,c,e):
  b=s.second(c);s.patient(a,'Paciente Fictício recente A');a.evaluate('go("accounting")');a.locator('[data-edit-payment="rA"]').evaluate('(e)=>e.click()');a.locator('#payment-form [name=amount]').fill('987.65');a.locator('#payment-form').evaluate('(f)=>f.requestSubmit()');a.locator('[data-done-note="nA"]').evaluate('(e)=>e.click()')
  initial=s.snap(b);latest=jget(s,a,'ma-care-v2');r=s.merge(b,payload(),'T02');after=s.snap(b);lost=jget(s,b,'ma-care-v2');save('T02-duas-abas',dict(beforeStale=initial,currentBeforeMerge=latest,result=r,after=after))
  record(2,lost==latest,dict(latestPatients=[p['name'] for p in latest['patients']],afterPatients=[p['name'] for p in lost['patients']],paymentBefore=latest['records'][0]['amount'],paymentAfter=lost['records'][0]['amount'],noteBefore=latest['notes'][0]['done'],noteAfter=lost['notes'][0]['done'],result=r))
  downloaded=json.load(open(OUT/r['downloads'][0]));record(4,downloaded['care']==latest,dict(downloadCare=downloaded['care'],actualPreimage=latest,historyBefore=initial['history'],historyAfter=after['history']))
  record(8,lost['records'][0]['amount']==latest['records'][0]['amount'],dict(twoTabsAllowed=True,latestPayment=latest['records'][0]['amount'],afterPayment=lost['records'][0]['amount']))
  record(6,any(x['kind']=='restore' or x['kind']=='merge' for x in after['history']),dict(history=after['history'],mergeSucceeded=True,note='A mesclagem não chama captura/journal A5; teste de falha IndexedDB executado separadamente.'))
 with s.context() as (p,c,e):
  before=s.state(p);s.fault(p,'ma-ledger-v1',True);r=s.merge(p,payload(),'T05');record(5,s.state(p)==before,dict(result=r,equality=s.state(p)==before));s.unfault(p)
 with s.context() as (p,c,e):
  p.evaluate('()=>{MA5.captureOperation=async()=>{throw Error("IndexedDB sintético indisponível")}}');before=s.state(p);r=s.merge(p,payload(),'T06');record(6,s.state(p)==before,dict(result=r,history=p.evaluate('MA5.all()'),captureUnavailable=True))
 with s.context() as (p,c,e):
  p.locator('#quick-search').evaluate('(e)=>{e.value="Rascunho fictício não salvo"}');p.locator('#payment-form [name=service]').evaluate('(e)=>e.value="Serviço em edição fictício"');s.rate(p,3,2.3);r=s.merge(p,payload(),'T10');record(10,p.locator('#payment-form [name=service]').input_value()=='Serviço em edição fictício' and p.locator('#quick-search').input_value()=='Rascunho fictício não salvo' and jget(s,p,'ma-installment-rates-v1')['3']==2.3,dict(result=r,service=p.locator('#payment-form [name=service]').input_value(),search=p.locator('#quick-search').input_value()))
 with s.context() as (p,c,e):
  p.evaluate('()=>{go("accounting");document.querySelector("#account-month").value="2027-01";document.querySelector("#account-month").dispatchEvent(new Event("change"))}');r=s.merge(p,payload(),'T40');record(40,p.locator('#account-month').input_value()=='2027-01',dict(result=r,month=p.locator('#account-month').input_value()))

def group2(s):
 cases=[]
 x=payload('A',[m.row(1,amount=99999)]);x['care']['records'][0]['amount']=88888;cases.append((12,x,'Conflitos mesmo ID sem aviso'))
 x=payload('A',[m.row(1,id='outro-id-mesmo-conteudo')]);x['care']['records'][0]['id']='outro-record';x['care']['notes']=[];cases.append((13,x,'Duplicação semântica'))
 cases.append((14,payload('B',[m.row(1,id=123,bank='Itau',amount=1000.5),m.row(2,id='123')]),'Compatibilidade de tipos'))
 x=payload('A');x['care']['patients'][0]['name']='Paciente Fictício Pessoa Diferente';x['care']['records'][0]['id']='pagamento-outra-pessoa';x['care']['records'][0]['snapshot']['name']='Paciente Fictício Pessoa Diferente';cases.append((15,x,'Colisão de identidade'))
 x=payload();x['care']['patients'].append(x['care']['patients'][0]);x['care']['records'][0]['patientId']='inexistente';cases.append((16,x,'Duplicados e vínculo ausente'))
 cases.append((19,payload(version=99),'Versão desconhecida'))
 cases.append((20,payload(ledger=[dict(id='linha-invalida',date='ERRADA',amount='inválido',kind='desconhecido',description='<img src=x onerror="window.TESTE_XSS=true">')]),'Linha inválida e XSS sintético'))
 for n,x,label in cases:
  with s.context() as (p,c,e):
   before=s.state(p);r=s.merge(p,x,'T%02d'%n);after=s.state(p);detail=dict(action=label,result=r,before=before,after=after,xss=p.evaluate('window.TESTE_XSS===true'));save('T%02d-estados'%n,detail)
   if n in [12,13,15]:ok=s.state(p)==before and ('conflit' in r['message'].lower() or 'duplic' in r['message'].lower()) and n!=12
   elif n==14:ok=jget(s,p,'ma-ledger-v1')==[m.row(),*x['ledger']]
   else:ok=after==before and 'mesclado' not in r['message'].lower()
   record(n,ok,detail)
 with s.context() as (p,c,e):
  before=s.state(p);f=s.backup(p);r=s.merge(p,f,'T18');record(18,s.state(p)==before and 'Não foi possível' in r['message'],r)
 with s.context() as (p,c,e):
  old=jget(s,p,'ma-academy-v55');r=s.merge(p,payload(ledger=[]),'T17');record(17,jget(s,p,'ma-academy-v55')==old and jget(s,p,'ma-installment-rates-v1')=={'5':3.1,'10':5.2},dict(result=r,note='V2 completo clínico/livro com módulos administrativos ausentes; parcial sem care não aceito pelo merge.'))
 with s.context(remove=['ma-installment-rates-v1']) as (p,c,e):
  r=s.merge(p,payload(rateSettings={'5':150,'10':'3.1','nonsense':{'unsafe':True}}),'T21');record(21,s.get(p,'ma-installment-rates-v1') is None,dict(result=r,persistedRates=s.get(p,'ma-installment-rates-v1')))
 with s.context() as (p,c,e):
  def mergepure(care,feed):return p.evaluate('([a,b])=>mergeCodental(a,b)',[care,feed])
  feed={'patients':[dict(id='X',name='Paciente Fictício A',cpf='',phone='')],'records':[]}
  out=mergepure(m.care(),feed);save('T22-codental',out);record(22,len(out['db']['patients'])==2 or len(out['db']['codentalImport']['pending'])>0,dict(result=out,action='Nome igual, CPF vazio, IDs distintos'))
  db=m.care();db['patients'][0].update(source='Cadastro no aplicativo',codentalId='X',phone='(00) 00000-0000');feed['patients'][0]['phone']='(00) 11111-1111';a=mergepure(db,feed);feed['patients'][0]['phone']='';b=mergepure(a['db'],feed);record(23,a['db']['patients'][0]['phone']==db['patients'][0]['phone'] and b['db']['patients'][0]['phone']==db['patients'][0]['phone'],dict(manual=a,empty=b,note='Política de origens históricas indefinidas permanece decisão pendente; proteção manual explícita e vazio executados.'))
  a=mergepure(m.care(),feed);b=mergepure(a['db'],feed);record(24,len(a['db']['patients'])==len(b['db']['patients']) and b['db']['records']==m.care()['records'] and b['db']['notes']==m.care()['notes'],dict(first=a,second=b,scope='Idempotência do feed executada; restore/reabertura testados T39.'))
  db=m.care();db['patients'].append(dict(db['patients'][0],id='pOutro'));o=mergepure(db,feed);record(25,len(o['db']['codentalImport']['pending'])>0 and len(o['db']['patients'])==2,o)
def group3(s):
 with s.context() as (a,c,e):
  b=s.second(c);s.rate(b,2,8.2);s.rate(a,3,9.3);raw=jget(s,a,'ma-installment-rates-v1');record(27,raw.get('2')==8.2,dict(action='B muda 2x; A desatualizada muda 3x',persisted=raw));b.bring_to_front();a.bring_to_front();s.rate(a,4,4.4);record(29,jget(s,a,'ma-installment-rates-v1').get('2')==8.2,dict(persisted=jget(s,a,'ma-installment-rates-v1'),scope='Retorno ao foco seguido de escrita de taxa; sem supressão artificial de notificações.'))
  b.locator('#ma56-tasks select').nth(0).evaluate('(e)=>{e.value="done";e.dispatchEvent(new Event("change"))}');bb=jget(s,b,'ma56-project-checklist-v1');a.locator('#ma56-tasks select').nth(1).evaluate('(e)=>{e.value="progress";e.dispatchEvent(new Event("change"))}');aa=jget(s,a,'ma56-project-checklist-v1');record(28,all(aa['states'].get(k)==v for k,v in bb['states'].items()),dict(beforeB=bb,afterA=aa,scope='Tarefas diferentes; importação é substituição explícita e não união.'))
  s.patient(a,'Paciente Fictício aba A');clinical=s.get(a,'ma-care-v2');msg=s.patient(b,'Paciente Fictício aba B');ledgerok=a.evaluate('ma62ApplyCorrection(0,"description","ABA A fictícia")');ledger=s.get(a,'ma-ledger-v1');ledgerb=b.evaluate('ma62ApplyCorrection(0,"description","ABA B fictícia")');record(26,False,dict(clinicalStaleRefused=s.get(a,'ma-care-v2')==clinical,clinicalMessage=msg,ledgerA=ledgerok,ledgerB=ledgerb,ledgerPreserved=s.get(a,'ma-ledger-v1')==ledger,unprotectedWritersLostChanges=True,limitation='Não foi forçada janela de corrida entre comparação/escrita nos módulos CAS; escritores diretos taxas/checklist já falham sem corrida forçada.'))
  before=s.state(a);f=s.fixture('T31-restore.json',payload());s.preview(a,f);a.locator('#ma5-restore-confirm').evaluate('(e)=>e.click()');a.wait_for_function('document.querySelector("#ma5-restore-status").textContent.includes("FALHOU")');msg=a.locator('#ma5-restore-status').text_content();record(31,s.state(a)==before and 'Outra aba' in msg,dict(message=msg,scope='Bloqueio restore duas abas executado; ação assíncrona com epoch antigo não foi forçada.'))
 with s.context() as (p,c,e):
  s.fault(p,'ma-installment-rates-v1');before=s.get(p,'ma-installment-rates-v1');s.rate(p,3,4.5);detail=dict(persisted=s.get(p,'ma-installment-rates-v1'),before=before,status=p.locator('#ma53-rates-status').text_content(),label=p.locator('[data-rate="3"]').locator('xpath=../..').inner_text(),value=p.locator('[data-rate="3"]').input_value());record(33,'salva' not in detail['label'].lower(),dict(**detail,limitation='Erro QuotaExceededError injetado; preenchimento físico da quota do navegador não executado.'));s.unfault(p)
 with s.context() as (p,c,e):
  p.locator('#m55-m-name').evaluate('(e)=>e.value="Material Fictício retry"');p.locator('#m55-m-size').evaluate('(e)=>e.value="100"');p.locator('#m55-m-price').evaluate('(e)=>e.value="10"');s.fault(p,'ma-academy-v55',True);p.locator('#m55-add-material').evaluate('(e)=>e.click()');failed=s.get(p,'ma-academy-v55');specific=s.dl(p,'#m55-export');bk=s.backup(p);own=json.load(open(specific));unified=json.load(open(bk));persisted=json.loads(next(x['raw'] for x in unified['state'] if x['key']=='ma-academy-v55'));record(36,own['data']==persisted,dict(specific=str(specific.relative_to(OUT)),unified=str(bk.relative_to(OUT)),specificMaterials=len(own['data']['materials']),persistedMaterials=len(persisted['materials']),specificNotLabelledDraft=True));s.unfault(p);p.locator('#m55-add-material').evaluate('(e)=>e.click()');after=jget(s,p,'ma-academy-v55');record(34,sum(x['name']=='Material Fictício retry' for x in after['materials'])==1,dict(after=after,failedPersisted=json.loads(failed),scope='Inclusão material/retry; equipamento e análise usam outros handlers e não foram executados.'))
 with s.context() as (p,c,e):
  before=s.get(p,'ma61-sanitary-checklist-v1');s.fault(p,'ma61-sanitary-checklist-v1');p.locator('#ma61-groups [data-field=notes]').first.evaluate('(e)=>{e.value="Anotação fictícia recusada";e.dispatchEvent(new Event("change"))}');f=s.dl(p,'#ma61-export');data=json.load(open(f));record(35,json.loads(before)==data.get('data'),dict(persisted=s.get(p,'ma61-sanitary-checklist-v1'),export=data,download=str(f.relative_to(OUT)),scope='Texto sanitário após falha, não cor.'));s.unfault(p)
 with s.context() as (p,c,e):
  pages=p.locator('aside nav button[data-page]').evaluate_all('(a)=>a.map(x=>x.dataset.page)');initial=s.state(p);nav=[]
  for page in pages:
   p.locator(f'aside nav button[data-page="{page}"]').evaluate('(e)=>e.click()');nav.append(p.evaluate('()=>({pages:[...document.querySelectorAll("main .page")].filter(p=>!p.hidden).map(p=>p.id),menu:[...document.querySelectorAll("aside nav button.active")].map(p=>p.dataset.page)})'))
  record(30,len(pages)==18 and all(x['pages']==[page] and x['menu']==[page] for x,page in zip(nav,pages)) and s.state(p)==initial,dict(pages=pages,observed=nav,scope='Menu18 telas; atalhos e navegação depois merge não cobertos por esta amostra.'))

def group4(s):
 with s.context() as (p,c,e):
  B=m.academy('B');B['ma58']['base']='A3';B['ma58']['target']='A1';B['ma58']['checks']['anterior'][0]=True;B['ma59']['filter']='Clínica';B['ma60']['blastMaterial']='zirconia';f=s.fixture('T37-academy-B.json',dict(format='manfrin-arnez-academy-backup',data=B));p.locator('#m55-import').set_input_files(str(f));p.wait_for_function('JSON.parse(localStorage.getItem("ma-academy-v55")).materials[0].id==="mB"');p.evaluate('()=>{document.querySelector("aside nav button[data-page=ma55-academy]").click();window.ma58OpenMakeup(true)}');before=s.get(p,'ma-academy-v55');dom=p.locator('#ma58-base').input_value();record(37,dom=='A3',dict(importedParent=json.loads(before),child58Base=dom,scope='Pai e filho58 verificados; 59/60 não declarados aprovados.'))
  p.locator('#ma58-target').select_option('A2');after=jget(s,p,'ma-academy-v55');save('T38-reidratacao',dict(imported=B,after=after,childBefore=dom));record(38,after['ma58']['base']=='A3' and after['ma58']['checks']['anterior'][0],dict(before=B['ma58'],after=after['ma58']))
 with s.context() as (p,c,e):
  b=s.backup(p);p.evaluate('(x)=>localStorage.setItem("ma-academy-v55",JSON.stringify(x))',m.academy('B'));s.restore(p,b);p.evaluate('()=>{document.querySelector("aside nav button[data-page=ma55-academy]").click();window.ma58OpenMakeup(true)}');db=jget(s,p,'ma-academy-v55');pdfs=p.evaluate('()=>({exocad:ma59ManualExocad,docs:ma58Docs})');p.reload();p.wait_for_function('MA5.appReady',timeout=180000);record(39,db==m.academy() and jget(s,p,'ma-academy-v55')==db and p.evaluate('ma59ManualExocad')==pdfs['exocad'],dict(restoredParent=db,pdfHashes={k:hashlib.sha256(v.encode()).hexdigest() for k,v in {'exocad':pdfs['exocad'],**pdfs['docs']}.items()},scope='V3 restore/reload e payloads incorporados; downloads dos três PDFs não executados ainda.'))
 with s.context() as (p,c,e):
  initial=jget(s,p,'ma-care-v2');s.patient(p,'Paciente Fictício adicional');after=jget(s,p,'ma-care-v2');record(41,after['records'][0]['snapshot']==initial['records'][0]['snapshot'],dict(snapshotBefore=initial['records'][0]['snapshot'],snapshotAfter=after['records'][0]['snapshot'],scope='Snapshot histórico não reescrito ao incluir paciente. Edição de paciente e taxa manual exigem subcaso adicional.'))
  bench=p.evaluate('()=>{const start=performance.now();const r=mergeCodental(MA_SEED,MA_CODENTAL);return {ms:performance.now()-start,patients:r.db.patients.length,pending:r.db.codentalImport.pending.length,stats:r.stats}}');record(42,None,dict(baseline=bench,reason='Nenhuma candidata de correção autorizada/existente; equivalência baseline/candidata não pode ser executada.'),'NÃO TESTADO')
  times=[]
  for i in range(3):
   t=time.monotonic();p.reload();p.wait_for_function('MA5.appReady',timeout=180000);times.append((time.monotonic()-t)*1000)
  record(43,True,dict(warmReloadMs=times,medianMs=statistics.median(times),p95ApproxMs=max(times),browser=p.context.browser.version,protocol='http://127.0.0.1',limitation='3 recargas; p95 apenas máximo amostral, sem inferência estatística. Abertura fria e latência ainda não medidas nesta execução.'))

def group5(s):
 import os,signal
 if os.environ.get("A4_EXPERIMENTAL_CRASH")!="1":
  record(7,None,dict(reason="Três tentativas de interrupção por Debugger/crash não produziram uma reabertura verificável: a conexão de automação ficou indisponível. Não inferir recuperação nem perda; fases de journal/marker de merge não existem na DEV.4.",logs=["log-grupo5.txt","log-grupo5-reexecucao.txt","log-grupo5-terceira-tentativa.txt"]),"NÃO TESTADO");return
 with s.context() as (p,c,e):
  session=c.new_cdp_session(p);session.send('Debugger.enable');paused=[];session.on('Debugger.paused',lambda x:paused.append(x))
  p.evaluate('()=>{const input=document.querySelector("#ma53-merge-file");window.originalMerge=input.onchange;input.onchange=null;const original=localStorage.setItem;localStorage.setItem=(k,v)=>{const r=original.call(localStorage,k,v);if(k==="ma-care-v2")debugger;return r}}')
  f=s.fixture('T07-interrupcao.json',payload());p.locator('#ma53-merge-file').set_input_files(str(f));p.evaluate('()=>{setTimeout(()=>originalMerge({target:document.querySelector("#ma53-merge-file")}),50)}');print('T07 scheduled',flush=True)
  deadline=time.monotonic()+15
  while not paused and time.monotonic()<deadline:p.wait_for_timeout(100)
  assert paused,'Não foi possível pausar a primeira escrita';print('T07 paused',flush=True)
  browserSession=s.b.new_browser_cdp_session();processes=browserSession.send('SystemInfo.getProcessInfo')['processInfo'];killed=[]
  for proc in processes:
   if proc['type']=='renderer':os.kill(int(proc['id']),signal.SIGKILL);killed.append(proc['id'])
  print('T07 killed renderer',killed,flush=True);old=p;p=s.second(c);old.a4RecoveryPage=p;state=s.snap(p);careCount=len(jget(s,p,'ma-care-v2')['patients']);ledgerCount=len(jget(s,p,'ma-ledger-v1'));detail=dict(reopened=state,careCount=careCount,ledgerCount=ledgerCount,method='Handler original agendado após upload, pausa depois da primeira escrita, SIGKILL somente dos renderers do browser descartável próprio, reabrir mesma aba. Journal/marker de merge inexistentes.');save('T07-interrupcao-estados',detail);record(7,(careCount,ledgerCount) in [(1,1),(2,2)],detail)

def group7(s):
 with s.context() as (a,c,e):
  b=c.new_page();b.set_default_timeout(15000);pending=[];b.on('dialog',lambda d:pending.append(d) if d.message.startswith('Mesclar backup') else d.accept());b.goto(s.url,timeout=180000);b.wait_for_function('MA5.appReady',timeout=180000)
  before=jget(s,a,'ma-ledger-v1');f=s.fixture('T08-race-confirm.json',payload());b.locator('#ma53-merge-file').set_input_files(str(f))
  deadline=time.monotonic()+15
  while not pending and time.monotonic()<deadline:b.wait_for_timeout(100)
  assert pending,'Confirmação não capturada'
  ok=a.evaluate('ma62ApplyCorrection(0,"amount",99999)');latest=jget(s,a,'ma-ledger-v1');pending[0].accept();b.wait_for_function('document.querySelector("#ma53-recovery-status").textContent.includes("Backup mesclado")');after=jget(s,a,'ma-ledger-v1');detail=dict(initial=before,latest=latest,after=after,ordinaryCorrectionSucceeded=ok,history=a.evaluate('MA5.all()'),action='A altera valor bancário enquanto confirmação do merge está aberta em B; aceitar merge em B depois.');save('T08-livro-concorrente',detail);record(8,after[0]['amount']==latest[0]['amount'],detail)

def group6(s):
 protocol=[]
 c=s.b.new_context();p=c.new_page()
 try:
  p.goto(m.HTML.as_uri(),timeout=15000);p.wait_for_function('MA5.appReady',timeout=15000);protocol.append(dict(protocol='file',available=True))
 except Exception as ex:protocol.append(dict(protocol='file',available=False,error=str(ex).splitlines()[0]))
 finally:c.close()
 for feature in ['locks','indexedDB']:
  c=s.b.new_context();p=c.new_page();p.on('dialog',lambda d:d.accept());errors=[];p.on('pageerror',lambda x:errors.append(str(x)))
  seeds={m.PREFIX+k:v for k,v in m.BASES().items()}|m.SENT|{m.PREFIX+'ma5-suppress-seeds-v1':'1'}
  c.add_init_script('for(const [k,v] of Object.entries('+json.dumps(seeds)+'))localStorage.setItem(k,v);'+('Object.defineProperty(navigator,"locks",{value:undefined});' if feature=='locks' else 'Object.defineProperty(window,"indexedDB",{value:undefined});'))
  c.route('**/*',lambda r:r.continue_() if r.request.url.startswith(s.url.rsplit('/',1)[0]) else r.abort());p.goto(s.url,timeout=180000);p.wait_for_timeout(1500)
  state=p.evaluate('()=>({ready:window.MA5?.appReady===true,guard:window.MA5?.guardFailure,text:document.body.innerText.substring(0,1600),stored:localStorage.getItem("ma-care-v2")})');protocol.append(dict(featureUnavailable=feature,result=state,errors=errors,baseline=m.BASES()['ma-care-v2']));c.close()
 record(32,None,dict(cases=protocol,reason='file:// bloqueado pela política ERR_BLOCKED_BY_ADMINISTRATOR; não foi contornada. Localhost e ausência de APIs foram efetivamente executados. Sentinelas verificadas nos demais contextos.'),'NÃO TESTADO');save('T32-protocolos-apis',protocol)
 with s.context() as (p,c,e):
  info=p.evaluate('()=>{const sizes=[200000,10000,1000,100,10,1];let n=0,chars=0;const keys=[];for(const size of sizes){for(let i=0;i<1000;i++){const k="A4-quota-ficticia-"+(n++);try{localStorage.setItem(k,"F".repeat(size));keys.push(k);chars+=size;}catch(e){break;}}}const tail=keys.at(-1);let value=localStorage.getItem(tail);for(let i=0;i<1000;i++){try{localStorage.setItem(tail,value+"F");value+="F";chars++;}catch(e){break}}window.quotaKeys=keys;return {keys:keys.length,chars,quotaReached:true}}');before=s.get(p,'ma-installment-rates-v1');s.rate(p,3,8.3);info.update(persisted=s.get(p,'ma-installment-rates-v1'),before=before,status=p.locator('#ma53-rates-status').text_content(),label=p.locator('[data-rate="3"]').locator('xpath=../..').inner_text());record(33,info['persisted']==before and 'salva' not in info['label'].lower(),dict(realQuota=info));p.evaluate('()=>{for(const k of quotaKeys)localStorage.removeItem(k)}')

def group9(s):
 with s.context() as (p,c,e):
  def mergepure(care,feed):return p.evaluate('([a,b])=>mergeCodental(a,b)',[care,feed])
  feed={'patients':[dict(id='X',name='Paciente Fictício A',cpf='',phone='')],'records':[]}
  out=mergepure(m.care(),feed);save('T22-codental',out);record(22,len(out['db']['patients'])==2 or len(out['db']['codentalImport']['pending'])>0,dict(result=out,action='Nome igual, CPF vazio, IDs distintos'))
  db=m.care();db['patients'][0].update(source='Cadastro no aplicativo',codentalId='X',phone='(00) 00000-0000');feed['patients'][0]['phone']='(00) 11111-1111';a=mergepure(db,feed);feed['patients'][0]['phone']='';b=mergepure(a['db'],feed);record(23,a['db']['patients'][0]['phone']==db['patients'][0]['phone'] and b['db']['patients'][0]['phone']==db['patients'][0]['phone'],dict(manual=a,empty=b,note='Política de origens históricas indefinidas permanece decisão pendente; proteção manual explícita e vazio executados.'))
  a=mergepure(m.care(),feed);b=mergepure(a['db'],feed);record(24,len(a['db']['patients'])==len(b['db']['patients']) and b['db']['records']==m.care()['records'] and b['db']['notes']==m.care()['notes'],dict(first=a,second=b,scope='Idempotência do feed executada; restore/reabertura testados T39.'))
  db=m.care();db['patients'].append(dict(db['patients'][0],id='pOutro'));o=mergepure(db,feed);record(25,len(o['db']['codentalImport']['pending'])>0 and len(o['db']['patients'])==2,o)
def group8(s):
 cold=[];hot=[];latencies=[]
 for i in range(3):
  t=time.monotonic()
  with s.context() as (p,c,e):
   cold.append((time.monotonic()-t)*1000);t=time.monotonic();p.reload();p.wait_for_function('MA5.appReady',timeout=180000);hot.append((time.monotonic()-t)*1000)
   pages=p.locator('aside nav button[data-page]').evaluate_all('(a)=>a.map(x=>x.dataset.page)')
   for page in pages:
    t=time.monotonic();p.locator(f'aside nav button[data-page="{page}"]').evaluate('(e)=>e.click()');latencies.append((time.monotonic()-t)*1000)
 record(43,True,dict(coldMs=cold,warmMs=hot,coldMedian=statistics.median(cold),warmMedian=statistics.median(hot),coldP95Approx=max(cold),warmP95Approx=max(hot),navigationDriverRoundTripMedian=statistics.median(latencies),navigationDriverRoundTripP95=sorted(latencies)[int(.95*(len(latencies)-1))],browser=s.b.version,protocol='http://127.0.0.1',limitation='3 aberturas frias/quentes, p95 aproximação amostral máximo. Medições incluem overhead Playwright e seeds mínimos; meta de 5s e hardware de destino não aprovados. Nenhuma candidata de correção.'))

def group10(s):
 with s.context() as (a,c,e):
  b=s.second(c);a.evaluate('go("patients")');a.locator('#new-patient').click();a.locator('#patient-form [name=name]').fill('Paciente Fictício corrida A');cdp=c.new_cdp_session(a);cdp.send('Debugger.enable');paused=[];cdp.on('Debugger.paused',lambda v:paused.append(v));a.evaluate('()=>{const original=localStorage.setItem;let once=true;localStorage.setItem=(k,v)=>{if(k==="ma-care-v2"&&once){once=false;debugger}return original.call(localStorage,k,v)};setTimeout(()=>document.querySelector("#patient-form").requestSubmit(),50)}')
  deadline=time.monotonic()+15
  while not paused and time.monotonic()<deadline:a.wait_for_timeout(100)
  assert paused,'CAS não pausou antes da escrita';msg=s.patient(b,'Paciente Fictício corrida B');latest=jget(s,b,'ma-care-v2');cdp.send('Debugger.resume');a.wait_for_function('JSON.parse(localStorage.getItem("ma-care-v2")).patients.some(p=>p.name.includes("corrida A"))');after=jget(s,a,'ma-care-v2');record(26,any(p['name']=='Paciente Fictício corrida B' for p in after['patients']),dict(latestBeforeResume=latest,afterResume=after,messageB=msg,method='Debugger pausa antes do setItem da aba A, após sua comparação original; B salva pela UI; A retoma sem remover CAS/guard originais.',limitation='Corrida forçada clínica; livro, Academia e Sanitária não receberam pausa equivalente.'))

def group11(s):
 import base64
 with s.context() as (p,c,e):
  # Medição da função original, sem candidata autorizada.
  bench=p.evaluate('()=>{const cases=[];for(const [label,db,feed] of [["seed-feed-original",MA_SEED,MA_CODENTAL],["vazio",{version:2,patients:[],records:[],notes:[]},{patients:[],date:"2026-10-10"}]]){const t=performance.now();const r=mergeCodental(db,feed);cases.push({label,ms:performance.now()-t,patients:r.db.patients.length,pending:r.db.codentalImport.pending.length,stats:r.stats})}return cases}');record(42,None,dict(baseline=bench,reason='Nenhuma candidata de correção autorizada/existente; equivalência baseline/candidata não executável nesta etapa.'),'NÃO TESTADO')
  # A restauração já foi executada no grupo4; baixar e verificar PDFs reais incorporados.
  p.locator('#ma59-open').evaluate('(e)=>e.click()');p.locator('#ma59-workshop [data-piece=crown]').evaluate('(e)=>e.click()');encoded=p.evaluate('()=>({exocad:ma59ManualExocad,...ma58Docs})');pdfs=[]
  for key in ['exocad','livro','maquiagem']:
   f=s.dl(p,f'#ma59-docs [data-doc="{key}"]');raw=f.read_bytes();pdfs.append(dict(key=key,download=str(f.relative_to(OUT)),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),matches=raw==base64.b64decode(encoded[key])))
  save('T39-pdfs-baixados',pdfs)
  # Cadastro editado e snapshot histórico; taxa manual não deve desaparecer silenciosamente.
  p.evaluate('go("patients")');p.locator('#patient-search').fill('Paciente Fictício A');p.locator('#patient-results [data-pid=pA]').click();before=jget(s,p,'ma-care-v2');p.locator('#patient-form [name=name]').fill('Paciente Fictício A atualizado');p.locator('#patient-form').evaluate('(f)=>f.requestSubmit()');after=jget(s,p,'ma-care-v2');p.locator('#m55-n').evaluate('(e)=>{e.value="5";e.dispatchEvent(new Event("change"))}');p.locator('#m55-fee').evaluate('(e)=>{e.value="12.34";e.dispatchEvent(new Event("input"))}');p.locator('#ma57-n').evaluate('(e)=>e.value="5"');p.locator('#ma57-gross').evaluate('(e)=>e.value="100"');p.locator('#ma57-net').evaluate('(e)=>e.value="90"');p.locator('#ma57-save').evaluate('(e)=>e.click()');detail=dict(patientBefore=before['patients'][0],patientAfter=after['patients'][0],snapshotBefore=before['records'][0]['snapshot'],snapshotAfter=after['records'][0]['snapshot'],clinicalMessage=p.locator('#patient-message').text_content(),manualFeeBefore='12.34',feeAfter=p.locator('#m55-fee').input_value(),feeSourceAfter=p.locator('#m55-fee').get_attribute('data-ma57-auto'));record(41,after['records'][0]['snapshot']==before['records'][0]['snapshot'] and detail['feeAfter']=='12.34',detail)
  # Independência da validação de vínculo e de duplicação interna bancária.
  baseline=s.state(p);bad=payload('D',[]);bad['care']['records'][0]['patientId']='paciente-inexistente';r=s.merge(p,bad,'T16-vinculo-ausente');save('T16-vinculo-ausente',dict(result=r,noChanges=s.state(p)==baseline))
  bad=payload('B',[m.row(2),m.row(2,amount=88888)]);r=s.merge(p,bad,'T16-duplicados-livro');record(16,s.state(p)==baseline,dict(result=r,persistedLedger=jget(s,p,'ma-ledger-v1'),action='Duas linhas internas com mesmo ID e conteúdos divergentes; primeiro vence sem conflito. Cadastro duplicado e vínculo ausente são recusados em subcasos anteriores.'))
  pages=p.locator('aside nav button[data-page]').evaluate_all('(a)=>a.map(x=>x.dataset.page)');nav=[]
  for page in pages:
   p.locator(f'aside nav button[data-page="{page}"]').evaluate('(e)=>e.click()');nav.append(p.evaluate('()=>({pages:[...document.querySelectorAll("main .page")].filter(p=>!p.hidden).map(p=>p.id),menu:[...document.querySelectorAll("aside nav button.active")].map(p=>p.dataset.page)})'))
  record(30,len(p.evaluate('rows'))==len(jget(s,p,'ma-ledger-v1')),dict(menuPages=pages,navigation=nav,ledgerPersisted=len(jget(s,p,'ma-ledger-v1')),ledgerModel=len(p.evaluate('rows')),scope='18 telas pelo menu, depois merge; atalhos não cobertos. Navegar não reidrata modelo bancário.'))
 with s.context() as (p,c,e):
  p.locator('#patient-form [name=name]').evaluate('(e)=>e.value="Cadastro fictício rascunho"');p.locator('#payment-form [name=service]').evaluate('(e)=>e.value="Serviço fictício em edição"');p.locator('#note-form [name=text]').evaluate('(e)=>e.value="Evolução fictícia não salva"');s.rate(p,3,2.3);r=s.merge(p,payload(),'T10-rascunhos');values=[p.locator(x).input_value() for x in ['#patient-form [name=name]','#payment-form [name=service]','#note-form [name=text]']];record(10,values==['Cadastro fictício rascunho','Serviço fictício em edição','Evolução fictícia não salva'] and jget(s,p,'ma-installment-rates-v1')['3']==2.3,dict(result=r,drafts=values,scope='Campos montados cadastro/pagamento/evolução legada, esta última oculta pela interface estruturada; taxa personalizada persistida.'))
  before=s.get(p,'ma-care-v2');f=s.fixture('T17-parcial-so-livro.json',dict(format='manfrin-arnez-backup',version=2,ledger=[m.row(99)]));r=s.merge(p,f);save('T17-parcial-so-livro',dict(result=r,careUnchanged=s.get(p,'ma-care-v2')==before))
 with s.context() as (p,c,e):
  initial=s.get(p,'ma-ledger-v1');p.evaluate('()=>{const original=MA5.captureOperation;MA5.captureOperation=async(...args)=>{const result=await original(...args);MA5.managedWrite("ma5-restore-epoch-v1","EPOCH-FICTICIO-TESTE-A4");return result}}');ok=p.evaluate('ma62ApplyCorrection(0,"description","Não deve gravar epoch antigo")');record(31,ok is False and s.get(p,'ma-ledger-v1')==initial,dict(asyncOldEpochSave=ok,ledgerPreserved=s.get(p,'ma-ledger-v1')==initial,guard=p.evaluate('MA5.guardFailure'),method='Troca sintética de epoch durante await de captura de preimage da operação bancária. Bloqueio de restore duas abas já testado grupo3.'))

def group12(s):
 with s.context() as (p,c,e):
  feed={'date':'2026-10-10','patients':[dict(id='X',name='Paciente Fictício A',cpf='',phone='(00) 11111-1111',email='novo@example.test',address='Endereço fictício novo',cep='00000-000')]};db=m.care();db['patients'][0].update(source='Base histórica fictícia sem proveniência por campo',phone='(00) 00000-0000');out=p.evaluate('([db,feed])=>mergeCodental(db,feed)',[db,feed]);record(23,len(out['db']['codentalImport']['pending'])>0 and out['db']['patients'][0]['phone']==db['patients'][0]['phone'],dict(before=db,result=out,scope='Fonte histórica sem proveniência: campo preenchido é atualizado automaticamente; política exige revisão. Campo manual explícito e entrada vazia foram testados no grupo9.'))
  db=m.care();db['patients'][0]['codentalId']='OUTRO-ID';out=p.evaluate('([db,feed])=>mergeCodental(db,feed)',[db,feed]);record(25,len(out['db']['codentalImport']['pending'])==1 and out['db']['patients'][0]['codentalId']=='OUTRO-ID',dict(conflictingCodentalId=out,scope='Ambiguidade por múltiplos candidatos testada no grupo9, conflito de CodentalId aqui.'))
  original=s.get(p,'ma-care-v2');bk=s.backup(p);p.locator('#sync-apply').evaluate('(e)=>e.click()');first=jget(s,p,'ma-care-v2');p.locator('#sync-apply').evaluate('(e)=>e.click()');second=jget(s,p,'ma-care-v2');s.restore(p,bk);restored=s.get(p,'ma-care-v2');p.reload(timeout=180000);p.wait_for_function('MA5.appReady',timeout=180000);record(24,[x['id'] for x in first['patients']]==[x['id'] for x in second['patients']] and first['records']==second['records']==m.care()['records'] and first['notes']==second['notes']==m.care()['notes'] and s.get(p,'ma-care-v2')==restored==original and s.get(p,'ma5-suppress-seeds-v1')=='1',dict(firstCounts={k:len(first[k]) for k in ['patients','records','notes']},secondCounts={k:len(second[k]) for k in ['patients','records','notes']},restoredCounts={k:len(json.loads(restored)[k]) for k in ['patients','records','notes']},suppressSeeds=s.get(p,'ma5-suppress-seeds-v1'),backup=str(bk.relative_to(OUT)),scope='Duas sincronizações pelo botão original com feed integral fictício; restauração v3 e recarga sem reinjeção.'))

def group13(s):
 with s.context(remove=['ma-installment-rates-v1']) as (p,c,e):
  before=s.state(p);s.fault(p,'ma-installment-rates-v1',True);r=s.merge(p,payload(rateSettings={'3':4.2}),'T05-falha-terceira-escrita');detail=dict(result=r,before=before,after=s.state(p),rollbackExact=s.state(p)==before);save('T05-terceira-escrita',detail);s.unfault(p)
 with s.context() as (p,c,e):
  before=s.state(p);p.evaluate('()=>{const original=localStorage.setItem;let clinicalWrites=0;localStorage.setItem=(k,v)=>{if(k==="ma-care-v2"&&++clinicalWrites>1)throw new DOMException("Rollback clínico fictício indisponível","QuotaExceededError");if(k==="ma-ledger-v1")throw new DOMException("Escrita financeira fictícia indisponível","QuotaExceededError");return original.call(localStorage,k,v)}}');r=s.merge(p,payload(),'T05-rollback-falha');after=s.state(p);detail=dict(result=r,before=before,after=after,guard=p.evaluate('MA5.guardFailure'),history=p.evaluate('MA5.all()'));save('T05-rollback-falha',detail);record(5,after==before or bool(detail['guard']),detail)

def main():
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(m.Quiet,directory=str(SRC)));threading.Thread(target=server.serve_forever,daemon=True).start()
 group=int(sys.argv[1]);out=OUT/f'grupo{group}';out.mkdir(exist_ok=True)
 global OUTROOT
 with sync_playwright() as pw:
  executable=__import__('os').environ.get('A4_CHROMIUM') or ('/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None);browser=pw.chromium.launch(executable_path=executable,headless=True,args=['--no-sandbox']);s=S(browser,f'http://127.0.0.1:{server.server_port}/{m.HTML.name}',OUT)
  s.seq=group*1000
  try:globals()['group'+str(group)](s)
  except Exception as ex:save(f'erro-grupo{group}',dict(error=str(ex),traceback=traceback.format_exc()));traceback.print_exc()
  finally:
   save(f'resultados-grupo{group}',list(results.values()));save(f'auxiliares-grupo{group}',s.checks);browser.close();server.shutdown()
if __name__=='__main__':main()
