from pathlib import Path
import hashlib,re
ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/'referencias/Manfrin-Arnez-Dashboard-6.2-DEV-03-A1.2.html'
OUTPUT=ROOT/'Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='e4e4f49ca37e85cd9c83c67aa79b4e9d2fcb74b11137c387a5692ea8727bcc3f'
s=SOURCE.read_text()
def replace(old,new):
 global s
 assert s.count(old)==1,(s.count(old),old[:90]);s=s.replace(old,new)
def section(start,end,new):
 global s
 a=s.index(start);b=s.index(end,a);s=s[:a]+new+'\n'+s[b:]
replace('DEV — Manfrin Arnez 6.2-dev.3 — A1.2','DEV — Manfrin Arnez 6.2-dev.4 — A5')
replace('</head><body>', '<script id="ma5-protection">'+(ROOT/'fontes/protection.js').read_text()+'</script>\n<script id="ma5-backup-engine">'+(ROOT/'fontes/backup-engine.js').read_text()+'</script>\n</head><body>')
replace('let rows=[],storageOK=true;','let rows=[],storageOK=true,ma62WritePending=false;')
replace('const hasRisk=ma62LedgerBlocked||ma62LedgerRejected.length||problems.length||legacyCount||ma62LedgerManualOnly||ma62Protection||previous!==null||snapshots.length||ma62QuarantineReadError;', 'const hasRisk=ma62LedgerBlocked||ma62LedgerRejected.length||problems.some(q=>!q.archived)||legacyCount||ma62LedgerManualOnly||ma62QuarantineReadError;')
section('function persist(){', "$('storage-note').textContent=", '''async function persist(){
 const msg=$('ledger-message');
 if(ma62LedgerBlocked){msg.textContent='Gravação BLOQUEADA para proteger o livro-caixa original. '+ma62LedgerWarning;return false;}
 if(ma62WritePending){msg.textContent='Aguarde a operação protegida em andamento.';return false;}
 const next=JSON.stringify(rows),expected=ma62LedgerRaw;ma62WritePending=true;
 try{return await MA5.lock(async()=>{
  if(localStorage.getItem(ma62LedgerKey)!==expected){ma62BlockLedger('Os lançamentos foram modificados por outra aba ou módulo. Recarregue após preservar os dados.');msg.textContent='Alteração externa detectada; nada foi gravado.';return false;}
  const initial=expected===null?'[]':expected;
  if(!(ma62LedgerManualApproved&&ma62ExternalRaw===expected)){
   try{const copy=await MA5.captureOperation(initial,'Antes de operação do livro-caixa',ma62Session);ma62Protection='Cópia de operação verificada em IndexedDB: '+copy.id;ma62LedgerManualOnly=false;}
   catch(err){ma62LedgerManualOnly=true;ma62LedgerBanner();msg.textContent='Gravação bloqueada: histórico indisponível ou cheio. Original intacto. Exporte/verifique proteção externa ou libere cópias verificadas: '+err.message;return false;}
  }else ma62Protection='Operação protegida por cópia externa '+ma62ExternalMode+'. Faça nova cópia do estado atualizado.';
  if(localStorage.getItem(ma62LedgerKey)!==expected){ma62BlockLedger('Livro mudou durante a proteção; nada será gravado.');return false;}
  localStorage.setItem(ma62LedgerKey,next);
  if(localStorage.getItem(ma62LedgerKey)!==next)throw Error('Gravação principal não conferida');
  ma62LedgerRaw=next;ma62LedgerRejected=[];storageOK=true;ma62LedgerManualOnly=false;ma62LedgerManualApproved=false;ma62ExternalRaw=null;ma62ExternalMode='';msg.textContent='';
  const note=$('ma5-operation-status');if(note)note.textContent=ma62Protection;ma62LedgerBanner();return true;
 });}catch(err){storageOK=false;ma62LedgerManualApproved=false;ma62ExternalRaw=null;ma62LedgerManualOnly=true;ma62LedgerBanner('Falha de gravação/proteção: '+err.message);
  msg.textContent='Não foi possível salvar. Original preservado; cópias protegidas permanecem no histórico. '+err.message;return false;
 }finally{ma62WritePending=false;}
}''')
replace('function ma62ApplyCorrection(index,field,value){','async function ma62ApplyCorrection(index,field,value){\n  if(ma62WritePending)throw Error("Aguarde a operação protegida em andamento");')
replace('rows[index]=next;if(!persist()){rows[index]=original;return false;}','rows[index]=next;if(!await persist()){rows[index]=original;return false;}')
replace('form.onsubmit=e=>{e.preventDefault();try{if(rows[index]!==original)', 'form.onsubmit=async e=>{e.preventDefault();try{if(rows[index]!==original)')
replace('if(ma62ApplyCorrection(index,field.value,v))d.close();','if(await ma62ApplyCorrection(index,field.value,v))d.close();')
replace("s=>s.onchange=()=>{const index=Number(s.dataset.row);try{ma62ApplyCorrection(index,'kind',s.value);", "s=>s.onchange=async()=>{const index=Number(s.dataset.row);try{await ma62ApplyCorrection(index,'kind',s.value);")
replace("b=>b.onclick=()=>{const index=Number(b.dataset.delete);", "b=>b.onclick=async()=>{if(ma62WritePending)return;const index=Number(b.dataset.delete);")
replace('if(!persist())rows=oldRows;', 'if(!await persist())rows=oldRows;')
replace("$('transaction').onsubmit=e=>{e.preventDefault();", "$('transaction').onsubmit=async e=>{e.preventDefault();if(ma62WritePending){$('ledger-message').textContent='Aguarde a operação protegida em andamento.';return;}")
replace('rows.push(r);if(!persist()){', 'rows.push(r);if(!await persist()){')
replace('rows.push(...newRows);if(!persist()){', "if(ma62WritePending)throw Error('Aguarde a operação protegida em andamento');rows.push(...newRows);if(!await persist()){")
replace("seed=window.mergeCodental(window.MA_SEED,window.MA_CODENTAL).db", "seed=localStorage.getItem('ma5-suppress-seeds-v1')==='1'?{version:2,patients:[],records:[],notes:[]}:window.mergeCodental(window.MA_SEED,window.MA_CODENTAL).db")
replace('if(storage&&!readError&&records.length){', "if(storage&&!readError&&records.length&&localStorage.getItem('ma5-suppress-seeds-v1')!=='1'){")
replace("try{let old=localStorage.getItem(key);if(old)db=validate", "MA5.validateCare=validate;\ntry{let old=localStorage.getItem(key);if(old)db=validate")
section('function persist(next){', 'function storageStatus(){', '''let ma5CareExpected=localStorage.getItem(key);
function persist(next){validate(next);if(readError)throw Error('Cadastro ilegível ou armazenamento indisponível: dados preservados. Use a proteção A5.');
 if(localStorage.getItem(key)!==ma5CareExpected)throw Error('Cadastro modificado por outra aba. Recarregue; nenhum pagamento/cadastro foi sobrescrito.');
 const text=JSON.stringify(next);try{localStorage.setItem(key,text);if(localStorage.getItem(key)!==text)throw Error('Gravação não conferida');}catch(e){storage=false;storageStatus();throw Error('Não foi possível salvar. Registro não alterado. '+e.message);}
 ma5CareExpected=text;db=next;storage=true;storageStatus();
}''')
replace("function save(){try{const s=JSON.stringify(data);localStorage.setItem(K,s);", "let ma5AcademyExpected=localStorage.getItem(K);\nfunction save(){try{if(localStorage.getItem(K)!==ma5AcademyExpected)throw Error('Academia alterada por outra aba; recarregue');const s=JSON.stringify(data);localStorage.setItem(K,s);ma5AcademyExpected=s;")
replace('const validIds=new Set(items.map(t=>t.id));', 'const validIds=new Set(items.map(t=>t.id));MA5.sanitaryIDs=validIds;')
replace("function persist(){try{const json=JSON.stringify(state);localStorage.setItem(key,json);", "let ma5SanitaryExpected=localStorage.getItem(key);\nfunction persist(){try{if(localStorage.getItem(key)!==ma5SanitaryExpected)throw Error('Checklist alterado por outra aba; recarregue');const json=JSON.stringify(state);localStorage.setItem(key,json);ma5SanitaryExpected=json;")
replace('Este backup principal NÃO é uma cópia completa de todos os módulos. Quarentenas, cópias locais, Academia e checklists exigem arquivos separados. Exportação parcial restaurável e restauração ampliada de legados: pendentes para A5.', 'O formato A5 v3 inclui as bases persistidas e todo o histórico acessível. Dados ilegíveis/desconhecidos são identificados como PARCIAL, com bytes preservados. Módulos ausentes não serão inventados nem apagados na restauração. Guarde também o HTML: PDFs/manuais fixos estão embutidos nele.')
replace('Não substitui o backup completo antigo, que continua obrigatório para pacientes, evoluções e recebimentos.', 'É uma exportação específica dessas abas. O backup unificado A5 v3 também inclui esta base, além de pacientes, evoluções e recebimentos quando persistidos.')
replace('O backup geral antigo <b>não inclui automaticamente</b> este novo checklist; exporte-o separadamente.', 'O backup unificado A5 v3 inclui este checklist quando persistido. A exportação específica continua disponível.')
s=s.replace('O backup principal NÃO inclui esta quarentena.', 'O backup unificado v3 inclui esta quarentena e sua revisão; arquivar não recupera lançamentos.')
s=s.replace('quarentena(s) revisada(s)/arquivada(s), NÃO recuperadas e NÃO incluídas no backup principal. Exporte-as separadamente.', 'quarentena(s) revisada(s)/arquivada(s), NÃO recuperadas; preservadas no backup unificado v3.')
s=s.replace('cópia(s) local(is) de operações, fora do backup principal.', 'cópia(s) local(is) herdada(s), incluídas no snapshot unificado A5.')
s=s.replace('Cópias locais por operação (não incluídas no backup principal)', 'Cópias locais herdadas (incluídas no snapshot A5)')
s=s.replace('MA62-DEV3-', 'MA62-DEV4-')
def defer_scripts(m):
 attrs,code=m.group(1),m.group(2)
 if any('id="'+x+'"' in attrs for x in ['ma-dev-isolation','ma5-protection','ma5-backup-engine']):return m.group(0)
 assert 'type=' not in attrs
 return '<script type="application/x-ma5-app" data-ma5-app'+attrs+'>'+code+'</script>'
s=re.sub(r'<script([^>]*)>(.*?)</script>',defer_scripts,s,flags=re.S)
replace('</body></html>', '<script id="ma5-bootstrap">'+(ROOT/'fontes/bootstrap.js').read_text()+'</script>\n</body></html>')
OUTPUT.write_text(s)
print(OUTPUT,OUTPUT.stat().st_size,hashlib.sha256(OUTPUT.read_bytes()).hexdigest())
