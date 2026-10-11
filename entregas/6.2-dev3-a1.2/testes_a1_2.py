"""Testes do HTML COMPLETO em Chromium descartável e localStorage nativo.
Uso: python3 testes_a1_2.py [--html caminho] [--dev2 caminho] [--results pasta]
Dependências: Python 3.12+, playwright, /usr/bin/chromium.
Sem acesso a perfis existentes, dados reais ou serviços externos.
"""
import argparse
import ast
import hashlib
import inspect
import json
import threading
import time
import textwrap
import traceback
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright

PREFIX = '__MA_DEV61_SANDBOX__:'
LEDGER = 'ma-ledger-v1'
PREV = LEDGER + '-prev'
QKEY = LEDGER + '-rejeitados-20260101000000'
QBODY = json.dumps({'format': 'ma62-dev-ledger-quarantine', 'version': 1, 'rows': [{'index': 2, 'reason': 'FICTICIO', 'row': None}]}, ensure_ascii=False)
SENTINELS = {'ma-ledger-v1': 'SENTINELA-FICTICIA-REAL', 'ma-ledger-v1-prev': 'PREV-FICTICIO-REAL',
             'ma-care-v2': 'CARE-FICTICIO-REAL', QKEY: 'QUARENTENA-FICTICIA-REAL',
             'ma55-modules-v1': 'ACADEMIA-FICTICIA-REAL', 'ma61-sanitary-checklist-v1': 'SANITARIO-FICTICIO-REAL'}

def row(id='Cora:test', **changes):
    return dict(id=id, date='2026-10-10', bank='Cora', description='Lançamento fictício '+str(id), amount=1000, kind='Receita', **{}) | changes

def care_fixture():
    p=dict(id='paciente-teste',name='Pessoa Fictícia A1.2',cpf='',phone='',email='',address='',cep='',source='Cadastro no aplicativo')
    r=dict(id='pagamento-teste',patientId=p['id'],date='2026-10-10',month='2026-10',amount=43210,service='Teste fictício',payment='Pix',status='Recebido',snapshot={k:p[k] for k in ['name','cpf','phone','email','address','cep']},source='Teste')
    n=dict(id='evolucao-teste',patientId=p['id'],date='2026-10-10',tooth='11',text='Evolução exclusivamente fictícia',done=False)
    return dict(version=2,patients=[p],records=[r],notes=[n])

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass

class Suite:
    def __init__(self, browser, url, results):
        self.browser,self.url,self.results=browser,url,results
        self.checks=[];self.errors=[];self.download_count=0;self.dialogs=[]

    def check(self, name, condition, evidence=''):
        record=dict(id=name,status='APROVADO' if condition else 'REPROVADO',evidence=evidence)
        self.checks.append(record)
        print(f"{record['status']}: {name} {str(evidence)[:200]}",flush=True)
        assert condition, f'{name}: {evidence}'

    def pending(self, name, why):
        self.checks.append(dict(id=name,status='PENDENTE',evidence=why))
        print('PENDENTE:',name,why,flush=True)

    @contextmanager
    def scenario(self, ledger=None, extras=None, care=None):
        context=self.browser.new_context(accept_downloads=True, viewport={'width':1280,'height':900})
        # Semeadura de dados FICTÍCIOS antes da execução do HTML/isolation.
        seeds={PREFIX+'ma-care-v2':json.dumps(care if care is not None else care_fixture(),ensure_ascii=False),**SENTINELS}
        if ledger is not None: seeds[PREFIX+LEDGER]=ledger if isinstance(ledger,str) else json.dumps(ledger,ensure_ascii=False)
        seeds.update({PREFIX+k:v for k,v in (extras or {}).items()})
        context.add_init_script("""(() => {const store=window.localStorage;
          if(store.getItem('__MA_DEV61_SANDBOX__:test-fixture-initialized'))return;
          for(const [key,value] of Object.entries(SEEDS))store.setItem(key,value);
          store.setItem('__MA_DEV61_SANDBOX__:test-fixture-initialized','true');
        })();""".replace('SEEDS',json.dumps(seeds,ensure_ascii=False)))
        # O aplicativo não precisa de rede externa para estes testes.
        context.route('**/*',lambda route: route.continue_() if route.request.url.startswith(self.url.rsplit('/',1)[0]) else route.abort())
        page=context.new_page();page.set_default_timeout(60000)
        errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
        start=time.monotonic();page.goto(self.url,timeout=90000)
        print('HTML completo carregado em',round(time.monotonic()-start,2),'s',flush=True)
        try:yield page,context,errors
        finally:
            if __import__('sys').exc_info()[0]:
                print('DIAGNOSTICO',page.evaluate("() => ({backup:document.querySelector('#backup-message')?.textContent,contabilidade:document.querySelector('#ma53-recovery-status')?.textContent,alerta:document.querySelector('#ma62-ledger-alert')?.textContent})"),flush=True)
                page.screenshot(path=str(self.results/'falha.png'),full_page=True)
            self.check('CONSOLE-'+str(len(self.checks)),not errors,errors)
            self.isolation(page)
            context.close()

    def isolation(self,page):
        # Storage.prototype lê apenas o contexto descartável sem acessar o perfil real.
        data=page.evaluate("""() => {
          // Um iframe novo vê a mesma origem isolada do teste e seu Storage nativo.
          const f=document.createElement('iframe');document.body.append(f);const s=f.contentWindow.localStorage;
          const keys=KEYS,all=Array.from({length:s.length},(_,i)=>s.key(i));
          const result={sentinels:Object.fromEntries(keys.map(k=>[k,s.getItem(k)])),extra:all.filter(k=>!k.startsWith('__MA_DEV61_SANDBOX__:')&&!keys.includes(k))};f.remove();return result;
        }""".replace('KEYS',json.dumps(list(SENTINELS))))
        self.check('ISOLAMENTO-'+str(len(self.checks)),data['sentinels']==SENTINELS and not data['extra'],data)

    def get(self,page,key=LEDGER):return page.evaluate('(k)=>localStorage.getItem(k)',key)
    def keys(self,page):return page.evaluate('Array.from({length:localStorage.length},(_,i)=>localStorage.key(i))')
    def goto(self,page,id):
        button=page.locator(f'nav button[data-page="{id}"]')
        group=button.locator('xpath=ancestor::details')
        if group.count() and group.get_attribute('open') is None:
            group.locator('summary').click()
        button.click()
        assert page.locator('#'+id).is_visible()
    def accept(self,page):
        def handler(dialog):
            self.dialogs.append(dialog.message);dialog.accept()
        page.a1_dialog_handler=handler;page.on('dialog',handler)

    def add(self,page,description='Novo fictício'):
        self.goto(page,'ledger')
        f=page.locator('#transaction');f.locator('[name=date]').fill('2026-10-11');f.locator('[name=bank]').select_option('Cora')
        f.locator('[name=description]').fill(description);f.locator('[name=amount]').fill('12.34');f.locator('[name=kind]').select_option('Receita');f.locator('button').click()

    def download(self,page,selector):
        with page.expect_download() as event:page.locator(selector).click()
        d=event.value;self.download_count+=1
        target=self.results/'downloads'/f'{self.download_count:02d}-{d.suggested_filename}'
        target.parent.mkdir(exist_ok=True,parents=True);d.save_as(target)
        assert not d.failure()
        return target.read_bytes(),target,d.suggested_filename

    def refused(self,page,selector,status):
        events=[];handler=lambda d:events.append(d.suggested_filename);page.on('download',handler)
        page.locator(selector).click();page.wait_for_timeout(200);page.remove_listener('download',handler)
        self.check('BACKUP-RECUSADO-'+str(len(self.checks)),not events and 'RECUSADO' in page.locator(status).inner_text(),page.locator(status).inner_text())

    def editor(self,page,index,field,value):
        self.goto(page,'ledger');page.locator(f'[data-edit-legacy="{index}"]').click()
        page.locator('#ma62-edit-field').select_option(field);page.locator('#ma62-edit-value').fill(value)
        page.locator('#ma62-edit-legacy button[type=submit]').click()

    def run(self):
        # AJ-11, backup funcional, arquivo efetivamente verificado, recusa em ambas as telas.
        with self.scenario([row()]) as (p,c,e):
            self.goto(p,'accounting');payload,path,name=self.download(p,'#ma53-account-backup')
            backup=json.loads(payload)
            self.check('AJ11-DOWNLOAD-SOLICITADO','SOLICITADO' in p.locator('#ma53-recovery-status').inner_text() and 'NÃO verificado' in p.locator('#ma53-recovery-status').inner_text(),name)
            self.check('FORMATO-61',set(backup)=={'format','version','createdAt','care','ledger','rateSettings'} and backup['version']==2 and backup['ledger']==[row()],list(backup))
            self.goto(p,'backup');p.locator('#ma62-verify-backup').set_input_files(str(path))
            self.check('AJ11-ARQUIVO-VERIFICADO','ARQUIVO PRINCIPAL VERIFICADO' in p.locator('#backup-message').inner_text())
            p.locator('#ma62-verify-backup').set_input_files({'name':'errado.json','mimeType':'application/json','buffer':b'{}'})
            self.check('AJ11-ARQUIVO-ERRADO','NÃO VERIFICADO' in p.locator('#backup-message').inner_text())
            p.evaluate('(v)=>localStorage.setItem("ma-ledger-v1",v)',json.dumps([row('outra-aba')]))
            self.goto(p,'accounting');self.refused(p,'#ma53-account-backup','#ma53-recovery-status')

        # Quarentenas históricas, arquivo bruto, revisão persistente, restauração limpa B-79.
        with self.scenario([row()],{QKEY:QBODY,PREV:'PREV-ANTIGO-FICTICIO'}) as (p,c,e):
            self.accept(p);self.goto(p,'accounting');self.refused(p,'#ma53-account-backup','#ma53-recovery-status')
            self.check('B-100','Nenhum download foi solicitado' in p.locator('#ma53-recovery-status').inner_text())
            self.goto(p,'backup');raw,path,name=self.download(p,'#ma62-export-care-raw')
            self.check('AJ12-CADASTRO-PROTEGIDO',raw.decode()==self.get(p,'ma-care-v2') and 'NAO-RESTAURAR' in name)
            p.locator('#ma62-ledger-alert details').first.locator('summary').click()
            qb,qpath,qname=self.download(p,'#ma62-ledger-alert details button:has-text("Baixar")')
            self.check('QUARENTENA-DOWNLOAD-EXATO',qb.decode()==QBODY)
            p.locator('button:has-text("Revisar e arquivar")').click()
            self.check('B-07',self.get(p,QKEY)==QBODY and 'quarentena(s) revisada(s)/arquivada(s)' in p.locator('#ma62-ledger-alert').inner_text())
            p.reload(timeout=90000);self.goto(p,'backup')
            b,path,name=self.download(p,'#backup-save')
            self.check('B-06','QUARENTENAS-SEPARADAS' in name and 'OMITIDA(S)' in p.locator('#backup-message').inner_text() and self.get(p,QKEY)==QBODY)
            b61=dict(format='manfrin-arnez-backup',version=2,care=care_fixture(),ledger=[row('restaurado')],rateSettings={})
            with p.expect_navigation(timeout=90000):p.locator('#backup-load').set_input_files({'name':'backup-6.1.json','mimeType':'application/json','buffer':json.dumps(b61).encode()})
            self.goto(p,'backup');after,path,name=self.download(p,'#backup-save')
            self.check('B-79',json.loads(after)['ledger']==b61['ledger'] and self.get(p,QKEY)==QBODY)
            restored=json.loads(self.get(p,'ma-care-v2'))
            self.check('BACKUP61-PACIENTE-PAGAMENTO-EVOLUCAO',all(x in restored[k] for k in ['patients','records','notes'] for x in care_fixture()[k]))
            self.add(p)
            self.check('AJ14-PREV-INTOCADO',self.get(p,PREV)=='PREV-ANTIGO-FICTICIO')
            self.check('AJ14-SESSAO-ANTERIOR-EXPLICITA','sessão/data não comprovadas' in p.locator('#ma62-ledger-alert').inner_text())
            p.evaluate('(v)=>localStorage.setItem("'+QKEY+'",v)',QBODY+' ')
            self.goto(p,'backup');self.refused(p,'#backup-save','#backup-message')
            self.check('ARQUIVAMENTO-REVALIDADO','quarentena(s) ativa(s)' in p.locator('#ma62-ledger-alert').inner_text())

        # Registros rejeitados ativos não são ocultados pelo arquivamento.
        with self.scenario([row(),None]) as (p,c,e):
            self.accept(p);original=self.get(p);qkeys=[k for k in self.keys(p) if k.startswith(LEDGER+'-rejeitados-')]
            self.goto(p,'ledger');p.locator('#ma62-ledger-alert details summary').first.click();p.locator('button:has-text("Revisar e arquivar")').click()
            self.goto(p,'backup');self.refused(p,'#backup-save','#backup-message')
            self.check('REJEITADOS-NAO-RECUPERADOS',self.get(p)==original)
            self.add(p);snapkeys=[k for k in self.keys(p) if k.startswith(LEDGER+'-session-prev-')]
            self.check('COPIA-ANTES-DE-SEPARAR',len(snapkeys)==1 and self.get(p,snapkeys[0])==original and self.get(p,qkeys[0]) is not None)
            p.reload(timeout=90000);self.goto(p,'backup');b,path,name=self.download(p,'#backup-save')
            self.check('QUARENTENA-ARQUIVADA-POS-GRAVACAO',len(json.loads(b)['ledger'])==2 and self.get(p,qkeys[0]) is not None)

        # AJ-16: 12 variantes lidas sem perda; IDs numéricos (incluindo zero) preservados.
        variants=[row('valida'),row('banco',bank='Outro'),row('zero',amount=0),row('fracao',amount=1000.5),
                  row('categoria',kind='Antiga'),row('descricao',description=''),row('data-impossivel',date='2026-02-30'),
                  row('data-barras',date='10/10/2026'),row('sinal',amount=-1000),row(123),row('sem-categoria'),row('xss',description='<img src=x onerror="window.__xss=1">')]
        del variants[10]['kind'];variants += [row(0),row('123')]
        with self.scenario(variants) as (p,c,e):
            self.accept(p);self.goto(p,'ledger')
            self.check('B-31',p.locator('#transactions tr').count()==len(variants) and not [k for k in self.keys(p) if k.startswith(LEDGER+'-rejeitados-')])
            expected=sum(r['amount'] for r in variants if r.get('kind')=='Receita')
            actual=p.evaluate('Finance.aggregate(rows,"").revenue')
            self.check('B-32',actual==expected,{'esperado':expected,'obtido':actual,'metodo':'agregação correspondente ao contrato 6.1; HTML 6.1 não fornecido'})
            before=self.get(p);self.add(p)
            self.check('AJ16-VALORES-ORIGINAIS',json.loads(self.get(p))[:len(variants)]==variants)
            # IDs 123 (número) e "123" (texto) não colidem nos manipuladores.
            self.editor(p,9,'description','ID numérico revisado explicitamente')
            data=json.loads(self.get(p));self.check('AJ16-IDS-SEM-COLISAO',data[9]['id']==123 and data[13]==variants[13])
            raw,path,name=self.download(p,'#export')
            self.check('AJ16-CSV-NUMERICO',b'ID num' in raw and len(raw.decode().splitlines())==len(variants)+2)
            self.check('XSS-LEGADO',p.evaluate('window.__xss === undefined') and p.locator('#transactions img').count()==0)
            # Corrigir apenas categoria apesar do banco inválido, preservar montante e outros campos.
            p.locator('[data-row="1"]').select_option('A classificar')
            self.check('B-37',json.loads(self.get(p))[1]==(variants[1]|{'kind':'A classificar'}))
            self.editor(p,1,'bank','Sicredi')
            self.check('B-09',json.loads(self.get(p))[1]==(variants[1]|{'kind':'A classificar','bank':'Sicredi'}))
            self.editor(p,3,'amount','1001')
            self.check('AJ17-VALOR-EXPLICITO',json.loads(self.get(p))[3]==(variants[3]|{'amount':1001}))
            self.check('AJ17-CONFIRMACAO-ANTES-DE-MUDAR',any('ALTERAÇÃO FINANCEIRA EXPLÍCITA: 1000.5 → 1001 centavos' in message for message in self.dialogs))
            before_cancel=self.get(p);p.remove_listener('dialog',p.a1_dialog_handler)
            dismiss=lambda dialog:dialog.dismiss();p.on('dialog',dismiss)
            self.editor(p,3,'amount','1002')
            self.check('AJ17-CANCELAMENTO-PRESERVA-VALOR',self.get(p)==before_cancel)
            p.locator('#ma62-edit-legacy button:has-text("Cancelar")').click();p.remove_listener('dialog',dismiss);self.accept(p)
            self.editor(p,6,'date','2026-02-28')
            self.check('AJ17-DATA-EXPLICITA',json.loads(self.get(p))[6]==(variants[6]|{'date':'2026-02-28'}))
            previous=self.get(p);self.editor(p,2,'amount','0')
            self.check('AJ17-INVALIDO-RECUSADO',self.get(p)==previous and 'Campo inconsistente' in p.locator('#ma62-edit-message').inner_text());p.locator('#ma62-edit-legacy button:has-text("Cancelar")').click()
            snapshot=self.get(p);p.reload(timeout=90000)
            self.check('LEGADOS-REABERTURA',self.get(p)==snapshot and p.evaluate('rows.length')==len(variants)+1)
            self.goto(p,'backup');self.refused(p,'#backup-save','#backup-message')
            self.pending('A5-RESTAURACAO-LEGADOS','Leitura preservada; restauração de IDs numéricos/bancos antigos e backup parcial restaurável não implementados nesta etapa.')

        # JSON corrompido: original não sobrescrito; cópia forense exata.
        with self.scenario('[{"id":"json-truncado"') as (p,c,e):
            self.accept(p);original=self.get(p);self.add(p)
            self.check('JSON-CORROMPIDO',self.get(p)==original and 'BLOQUEADA' in p.locator('#ledger-message').inner_text())
            self.goto(p,'accounting');self.refused(p,'#ma53-account-backup','#ma53-recovery-status')
            raw,path,name=self.download(p,'#ma62-account-care-raw')
            self.check('AJ12-PACIENTES-INDEPENDENTES',raw.decode()==self.get(p,'ma-care-v2'))
            raw,path,name=self.download(p,'#ma62-ledger-alert button:has-text("Baixar original bruto")')
            self.check('JSON-CORROMPIDO-COPIA-EXATA',raw.decode()==original)
            p.reload(timeout=90000);self.check('JSON-REABERTURA',self.get(p)==original)

        # Cópia bruta de cadastro ilegível jamais exporta a base embutida como substituta.
        with self.scenario([row()],care={'version':99,'marker':'CADASTRO-FICTICIO-ILEGIVEL'}) as (p,c,e):
            original=self.get(p,'ma-care-v2');self.goto(p,'backup');self.refused(p,'#backup-save','#backup-message')
            raw,path,name=self.download(p,'#ma62-export-care-raw')
            self.check('CARE-ILEGIVEL-EXATO',raw.decode()==original and self.get(p,'ma-care-v2')==original)

        # Falhas determinísticas em pontos de escrita (Storage real, injeção apenas de QuotaExceeded).
        with self.scenario([row()],{PREV:'PREV-ANTIGO-FICTICIO'}) as (p,c,e):
            self.accept(p);original=self.get(p)
            p.evaluate("""() => {window.testOriginalSet=localStorage.setItem;
              localStorage.setItem=function(k,v){if(k.startsWith('ma-ledger-v1-session-prev-'))throw new DOMException('Cota fictícia para cópia','QuotaExceededError');return testOriginalSet.call(localStorage,k,v);};} """)
            self.add(p);self.check('AJ15-SEM-PROTECAO-BLOQUEIA',self.get(p)==original and 'Gravação bloqueada' in p.locator('#ledger-message').inner_text())
            wrong={'name':'copia.json','mimeType':'application/json','buffer':b'[]'}
            p.locator('#ma62-verify-ledger-file').set_input_files(wrong)
            self.check('EXTERNA-DIVERGENTE-RECUSADA',not p.evaluate('ma62LedgerManualApproved') and self.get(p)==original)
            p.locator('#ma62-verify-ledger-file').set_input_files({'name':'copia-correta.json','mimeType':'application/json','buffer':original.encode()})
            self.check('EXTERNA-VERIFICADA',p.evaluate('ma62LedgerManualApproved') and 'verificado pelo conteúdo' in p.locator('#ma62-ledger-alert').inner_text())
            self.add(p)
            self.check('B-67',len(json.loads(self.get(p)))==2 and 'Sem espaço' not in p.locator('#ma62-ledger-alert').inner_text() and 'Confirme o backup externo' not in p.locator('#ma62-ledger-alert').inner_text())
            self.check('B-69',self.get(p,PREV)=='PREV-ANTIGO-FICTICIO' and 'sessão/data não comprovadas' in p.locator('#ma62-ledger-alert').inner_text())
            after=self.get(p);self.add(p,'Outra operação não protegida')
            self.check('EXTERNA-USO-UNICO',self.get(p)==after)
            raw,path,name=self.download(p,'#ma62-ledger-alert button:has-text("Baixar cópia externa e confirmar")')
            self.check('CONFIRMACAO-MANUAL-DISTINTA',raw.decode()==after and 'confirmada manualmente' in p.locator('#ma62-ledger-alert').inner_text() and 'NÃO verificou' in p.locator('#ma62-ledger-alert').inner_text())
            self.add(p,'Protegida manualmente');self.check('MANUAL-PROTEGE-UMA-OPERACAO',len(json.loads(self.get(p)))==3)
            p.evaluate('localStorage.setItem=testOriginalSet')
            original=self.get(p)
            p.evaluate("""() => {localStorage.setItem=function(k,v){if(k==='ma-ledger-v1')throw new DOMException('Cota fictícia principal','QuotaExceededError');return testOriginalSet.call(localStorage,k,v);};} """)
            self.add(p,'Falha no principal')
            snapshots=[k for k in self.keys(p) if k.startswith(LEDGER+'-session-prev-')]
            self.check('QUOTA-PRINCIPAL-ORIGINAL-INTOCADO',self.get(p)==original and any(self.get(p,k)==original for k in snapshots))

        # Cota real do Chromium: encher apenas chaves prefixadas do contexto fictício.
        with self.scenario([row()]) as (p,c,e):
            original=self.get(p);fill=p.evaluate("""() => {
              let size=256*1024,count=0;
              while(size>=1){try{localStorage.setItem('test-fill-'+count,'x'.repeat(size));count++;}catch(e){if(e.name!=='QuotaExceededError')throw e;size=Math.floor(size/2);}}
              return count;
            }""")
            self.add(p);self.check('QUOTA-REAL',self.get(p)==original and 'bloqueada' in p.locator('#ledger-message').inner_text(),{'blocos':fill})
            self.goto(p,'backup');self.accept(p)
            p.evaluate("""() => {for(const k of Array.from({length:localStorage.length},(_,i)=>localStorage.key(i)))if(k.startsWith('test-fill-'))localStorage.removeItem(k);}""")
            self.add(p,'Após liberar espaço');self.check('QUOTA-RECUPERACAO',len(json.loads(self.get(p)))==2)

        # 12 mil linhas: >900.000 caracteres, mas cópia cabe na cota real.
        big=[row('Cora:grande-'+str(i),description='Volume fictício '+str(i)) for i in range(12000)]
        with self.scenario(big) as (p,c,e):
            original=self.get(p);self.add(p,'Novo em livro grande')
            keys=[k for k in self.keys(p) if k.startswith(LEDGER+'-session-prev-')]
            self.check('AJ15-12000-LINHAS',len(original)>900000 and len(json.loads(self.get(p)))==12001 and any(self.get(p,k)==original for k in keys),{'caracteres':len(original),'linhas':12001})

        # Concorrência real entre duas páginas na mesma origem e contexto.
        with self.scenario([row()]) as (a,c,e):
            self.accept(a);b=c.new_page();b.set_default_timeout(60000);b.on('pageerror',lambda x:e.append(str(x)));self.accept(b);b.goto(self.url,timeout=90000)
            self.add(a,'Aba A');original=self.get(a);self.add(b,'Aba B desatualizada')
            self.check('DUAS-ABAS',self.get(a)==original and 'Alteração externa' in b.locator('#ledger-message').inner_text())
            b.reload(timeout=90000);self.add(b,'Aba B recarregada');latest=self.get(b);self.add(a,'Aba A desatualizada')
            self.check('DUAS-ABAS-REABERTURA',self.get(a)==latest and len(json.loads(latest))==3)
            b.close()

        # Módulos: navegação, cadastro, pagamento, modelos, backups próprios, sanitário, simulador.
        with self.scenario([row()]) as (p,c,e):
            self.accept(p);pages=p.locator('nav button').evaluate_all('(els)=>els.map(e=>e.dataset.page)')
            for pageid in pages:
                self.goto(p,pageid);assert p.locator('#'+pageid).inner_text().strip()
            self.check('MODULOS-18-TELAS',len(pages)==18,pages)
            self.goto(p,'patients');p.locator('#new-patient').click();p.locator('#patient-form [name=name]').fill('Paciente Fictício Novo A1.2');p.locator('#patient-form button.primary').click()
            data=json.loads(self.get(p,'ma-care-v2'));new=next(x for x in data['patients'] if x['name']=='Paciente Fictício Novo A1.2')
            self.check('PACIENTE-CADASTRADO',new is not None)
            p.locator('#use-patient').click();f=p.locator('#payment-form');f.locator('[name=date]').fill('2026-10-11');f.locator('[name=amount]').fill('123.45');f.locator('[name=service]').fill('Serviço fictício A1.2');f.locator('button.primary').click()
            records=json.loads(self.get(p,'ma-care-v2'))['records'];saved=next(r for r in records if r['patientId']==new['id'])
            self.check('PAGAMENTO-PRESERVACAO',saved['amount']==12345 and care_fixture()['records'][0] in records)
            self.goto(p,'accounting');csv,path,name=self.download(p,'#account-export')
            self.check('CONTABILIDADE-CSV',b'Paciente Fict' in csv and b'123,45' in csv)
            self.goto(p,'sim');before=p.locator('#result').inner_text();p.locator('#sale').fill('3000');p.locator('#sale').dispatch_event('input')
            self.check('SIMULADOR',p.locator('#result').inner_text()!=before and p.locator('#ma53-rates-table input').count()==10)
            self.goto(p,'notes')
            # Os modelos permanecem; formulário de evolução por paciente já vinha oculto.
            self.check('EVOLUCOES-PRESERVADAS',care_fixture()['notes'][0] in json.loads(self.get(p,'ma-care-v2'))['notes'] and p.locator('#notes').inner_text().strip())
            self.goto(p,'ma61-sanitary')
            self.check('SAN-8-FRENTES-42-SUBTOPICOS',p.locator('.ma61-group').count()==8 and p.locator('.ma61-item').count()==42 and p.locator('#ma61-front-total').inner_text()=='8')
            item=p.locator('.ma61-item').first;item.locator('select').select_option('ok')
            self.check('SAN-EVIDENCIA-OBRIGATORIA','preencha primeiro a evidência' in p.locator('#ma61-message').inner_text())
            item.locator('textarea[data-field=evidence]').fill('Evidência exclusivamente fictícia');item.locator('textarea[data-field=evidence]').dispatch_event('change');item.locator('select').select_option('ok')
            state=self.get(p,'ma61-sanitary-checklist-v1');raw,path,name=self.download(p,'#ma61-export')
            self.check('SAN-EXPORTACAO',json.loads(raw)['data']==json.loads(state))
            p.locator('#ma61-import').set_input_files(str(path));self.check('SAN-IMPORTACAO',self.get(p,'ma61-sanitary-checklist-v1')==state)
            self.goto(p,'ma55-cost');raw,path,name=self.download(p,'#m55-export');academy=json.loads(raw)
            p.locator('#m55-import').set_input_files(str(path));self.check('ACADEMIA-IDAEVOLTA',academy['format']=='manfrin-arnez-academy-backup')
            self.goto(p,'ma56-project');raw,path,name=self.download(p,'#ma56-export')
            p.locator('#ma56-import').set_input_files(str(path));self.check('DESENVOLVIMENTO-IDAEVOLTA',json.loads(raw)['format']=='manfrin-arnez-ma56-checklist')
            self.goto(p,'ma55-academy')
            self.check('LABORATORIO-EXOCAD',p.locator('#ma58-studio').count()==1 and p.locator('#ma59-workshop').count()==1 and p.locator('#ma60-bench').count()==1 and p.evaluate('typeof window.ma59ManualExocad==="string" && window.ma59ManualExocad.length>10000'))
            p.locator('#ma59-open').click();p.locator('#ma59-workshop [data-piece="crown"]').click()
            raw,path,name=self.download(p,'#ma59-workshop button[data-doc=exocad]')
            self.check('EXOCAD-PDF-DOWNLOAD',raw.startswith(b'%PDF-') and name=='Manfrin-Arnez-Exocad-3.2.pdf')
            self.goto(p,'backup');raw,path,name=self.download(p,'#backup-save')
            self.check('BACKUP-PACIENTES-PAGAMENTOS-EVOLUCOES',saved in json.loads(raw)['care']['records'] and care_fixture()['notes'][0] in json.loads(raw)['care']['notes'])
            before=self.get(p,'ma-care-v2');p.reload(timeout=90000)
            self.check('REABERTURA-PACIENTES-PAGAMENTOS-SANITARIO',self.get(p,'ma-care-v2')==before and self.get(p,'ma61-sanitary-checklist-v1')==state)
            self.pending('6.1-NAVEGADOR-IDA-E-VOLTA','Formato v2 e fixture 6.1 testados; HTML executável 6.1 não foi fornecido. Não declarar validação cruzada em navegador 6.1.')
            self.pending('A5-RESTAURACAO-FIEL-E-COMPLETA','Restaurador preexistente reinjeta 4 registros fictícios; cobertura integral de módulos e proteção pré-restauração permanecem fora de A1.2.')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--html',type=Path,default=Path(__file__).with_name('Manfrin-Arnez-Dashboard-6.2-DEV-03-A1.2.html'));parser.add_argument('--dev2',type=Path);parser.add_argument('--results',type=Path,default=Path(__file__).with_name('resultados-testes'));parser.add_argument('--scenario',type=int,choices=range(1,12),help='Executar somente um dos 11 grupos; por padrão executa todos')
    args=parser.parse_args();args.results.mkdir(parents=True,exist_ok=True)
    if args.scenario:
        tree=ast.parse(textwrap.dedent(inspect.getsource(Suite.run)))
        method=tree.body[0];body=[];number=0
        for node in method.body:
            if isinstance(node,ast.With):
                number+=1
                if number==args.scenario:body.append(node)
            else:body.append(node)
        method.body=body;scope={};exec(compile(ast.fix_missing_locations(tree),__file__,'exec'),globals(),scope);Suite.run=scope['run']
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(args.html.parent)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    suite=None;failure=None
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
            suite=Suite(browser,f'http://127.0.0.1:{server.server_port}/{args.html.name}',args.results)
            if args.dev2:
                original=args.dev2.read_bytes();suite.check('DEV2-HASH-ORIGINAL',len(original)==4062900 and hashlib.sha256(original).hexdigest()=='f11dbe0eccce98e30545ae94297c38bf16e1f3053b94d52589a108dfd2756751')
                # Todo o conteúdo após syncInfo (modelos, Academia, Laboratório, Exocad, Sanitário) é byte a byte.
                old=original.decode();new=args.html.read_text();anchor='function syncInfo(){'
                suite.check('MODULOS-CODIGO-INTEGRAL-PRESERVADO',old[old.index(anchor):]==new[new.index(anchor):])
            suite.run();browser.close()
    except Exception as error:
        failure=str(error);traceback.print_exc()
    finally:
        server.shutdown();server.server_close()
        result={'html':str(args.html),'sha256':hashlib.sha256(args.html.read_bytes()).hexdigest(),'scenario':args.scenario or 'all','browser':'/usr/bin/chromium','transport':'HTTP loopback; file:// bloqueado por política do ambiente','checks':suite.checks if suite else [],'failure':failure}
        result['counts']={status:sum(r['status']==status for r in result['checks']) for status in ['APROVADO','REPROVADO','PENDENTE']}
        (args.results/'resultados.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
        print(json.dumps(result['counts']),flush=True)
    raise SystemExit(1 if failure else 0)

if __name__=='__main__':main()
