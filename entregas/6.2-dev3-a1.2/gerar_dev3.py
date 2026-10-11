from pathlib import Path
import hashlib
import argparse

parser = argparse.ArgumentParser(description='Gerar DEV.3 sem alterar DEV.2')
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--output', type=Path, default=Path(__file__).with_name('Manfrin-Arnez-Dashboard-6.2-DEV-03-A1.2.html'))
args = parser.parse_args()
SOURCE, OUT = args.source, args.output
assert OUT.resolve() != SOURCE.resolve(), 'A DEV.2 deve permanecer intacta'
assert OUT.name != 'manfrin-arnez.html', 'O site institucional não deve ser modificado'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == 'f11dbe0eccce98e30545ae94297c38bf16e1f3053b94d52589a108dfd2756751'
s = SOURCE.read_text()
def replace(old, new):
    global s
    assert s.count(old) == 1, (old[:100], s.count(old))
    s = s.replace(old, new)
def section(start, end, new):
    global s
    a = s.index(start); b = s.index(end, a)
    s = s[:a] + new + '\n' + s[b:]

replace('DEV — Manfrin Arnez 6.2-dev.2 — Ajustes A1.1', 'DEV — Manfrin Arnez 6.2-dev.3 — A1.2')
replace('/* MA62-A1.1 — Integridade do livro-caixa, modo DEV e leitura retrocompatível.', '/* MA62-A1.2 — Integridade do livro-caixa, modo DEV e leitura retrocompatível.')
replace("let ma62LedgerQuarantines=[],ma62LedgerManualApproved=false,ma62LedgerManualOnly=false;", """let ma62LedgerQuarantines=[],ma62LedgerManualApproved=false,ma62LedgerManualOnly=false;
// AJ-12/14: chaves originais e -prev nunca são removidas ou sobrescritas.
const ma62ReviewPrefix='ma-ledger-v1-quarantine-review:';
const ma62SnapshotPrefix='ma-ledger-v1-session-prev-';
const ma62Session=new Date().toISOString().replace(/[^0-9]/g,'')+'-'+crypto.randomUUID();
let ma62SnapshotSequence=0,ma62ExternalRaw=null,ma62ExternalMode='',ma62Protection='';
let ma62QuarantineReadError=false;""")
section('function ma62ReadQuarantines(){', 'function ma62LegacyReadable(r){', """function ma62ReadQuarantines(){
  const items=[];ma62QuarantineReadError=false;
  try{
    for(let i=0;i<localStorage.length;i++){
      const key=localStorage.key(i);if(!key||!key.startsWith(ma62QuarantinePrefix))continue;
      const body=localStorage.getItem(key);let parsed=null,review=null;
      try{parsed=JSON.parse(body);}catch(_){}
      try{review=JSON.parse(localStorage.getItem(ma62ReviewPrefix+key));}catch(_){}
      // A revisão vale apenas para estes bytes; alterações posteriores reativam o risco.
      const archived=review?.version===1&&review.key===key&&review.originalBody===body
        &&typeof review.reviewedAt==='string'&&review.acknowledged===true;
      items.push({key,body,count:Array.isArray(parsed?.rows)?parsed.rows.length:null,archived,review});
    }
  }catch(_){ma62QuarantineReadError=true;}
  ma62LedgerQuarantines=items.sort((a,b)=>a.key.localeCompare(b.key));return ma62LedgerQuarantines;
}
function ma62ArchiveQuarantine(item){
  if(!confirm('Arquivar como REVISADA? O original permanece intacto e NÃO recupera lançamentos. O backup principal NÃO inclui esta quarentena. Baixe e confira o arquivo separadamente antes de confirmar.'))return;
  try{
    if(localStorage.getItem(item.key)!==item.body)throw Error('Quarentena mudou; revise novamente');
    const review={version:1,key:item.key,originalBody:item.body,reviewedAt:new Date().toISOString(),acknowledged:true};
    const key=ma62ReviewPrefix+item.key,body=JSON.stringify(review);
    localStorage.setItem(key,body);
    if(localStorage.getItem(key)!==body)throw Error('Não foi possível verificar a revisão');
    ma62LedgerBanner('Quarentena revisada e arquivada por confirmação manual. Original intacto; lançamentos NÃO recuperados.');
  }catch(err){ma62LedgerBanner('Arquivamento recusado: '+err.message+'. Original preservado.');}
}
function ma62ReadSnapshots(){
  const out=[];
  for(let i=0;i<localStorage.length;i++){const key=localStorage.key(i);
    if(key?.startsWith(ma62SnapshotPrefix))out.push({key,body:localStorage.getItem(key),current:key.startsWith(ma62SnapshotPrefix+ma62Session+'-')});}
  return out.sort((a,b)=>a.key.localeCompare(b.key));
}""")
replace("&&typeof r.id==='string'&&!!r.id&&typeof r.date==='string'&&!!r.date", "&&((typeof r.id==='string'&&!!r.id)||(typeof r.id==='number'&&Number.isFinite(r.id)))&&typeof r.date==='string'&&!!r.date")
replace("function ma62HasLedgerRisk(){return ma62LedgerBlocked||ma62LedgerRejected.length>0||ma62LedgerQuarantines.length>0||rows.some(r=>!!ma62LegacyIssue(r));}", "function ma62HasLedgerRisk(){return ma62LedgerBlocked||ma62LedgerRejected.length>0||ma62QuarantineReadError||ma62LedgerQuarantines.some(q=>!q.archived)||rows.some(r=>!!ma62LegacyIssue(r));}")
replace("  const legacyCount=rows.reduce((n,r)=>n+(ma62LegacyIssue(r)?1:0),0);\n  const hasRisk=ma62LedgerBlocked||ma62LedgerRejected.length||problems.length||legacyCount||ma62LedgerManualOnly;", """  const legacyCount=rows.reduce((n,r)=>n+(ma62LegacyIssue(r)?1:0),0);
  let previous=null,snapshots=[];try{previous=localStorage.getItem('ma-ledger-v1-prev');snapshots=ma62ReadSnapshots();}catch(_){}
  const hasRisk=ma62LedgerBlocked||ma62LedgerRejected.length||problems.length||legacyCount||ma62LedgerManualOnly||ma62Protection||previous!==null||snapshots.length||ma62QuarantineReadError;""")
replace("  if(problems.length)parts.push(problems.length+' arquivo(s) de quarentena guardado(s). Eles NÃO fazem parte do backup geral atual.');", """  const active=problems.filter(q=>!q.archived).length,archived=problems.length-active;
  if(active)parts.push(active+' quarentena(s) ativa(s): revise e guarde uma cópia separada.');
  if(archived)parts.push(archived+' quarentena(s) revisada(s)/arquivada(s), NÃO recuperadas e NÃO incluídas no backup principal. Exporte-as separadamente.');
  if(ma62QuarantineReadError)parts.push('Não foi possível verificar todas as quarentenas; backup principal bloqueado.');
  if(previous!==null)parts.push('A chave -prev é uma cópia anterior, de sessão/data não comprovadas. Conteúdo preservado; NÃO é apresentada como anterior à gravação atual.');
  if(snapshots.length)parts.push(snapshots.length+' cópia(s) local(is) de operações, fora do backup principal.');
  if(ma62Protection)parts.push(ma62Protection);""")
replace("  if(ma62LedgerManualOnly)parts.push('Sem espaço para cópia local do estado anterior. Confirme o backup externo para liberar a gravação; o risco residual será indicado.');", "  if(ma62LedgerManualOnly&&!ma62LedgerManualApproved)parts.push('Não foi possível criar a cópia local para esta operação. Baixe e verifique uma cópia externa do estado atual antes de repetir.');")
replace("'MA62-DEV2-Livro-Caixa-Original.json'", "'MA62-DEV3-Livro-Caixa-Original-BRUTO.json'")
replace("name.textContent=(i+1)+'. '+item.key+' — '+(item.count===null?'conteúdo não reconhecido':item.count+' linha(s)');", "name.textContent=(i+1)+'. '+item.key+' — '+(item.archived?'ARQUIVADA (não recuperada) · ':'ATIVA · ')+(item.count===null?'conteúdo não reconhecido':item.count+' linha(s)');")
replace("b.onclick=()=>download('MA62-DEV2-Quarentena-'+(i+1)+'.json',item.body);r.append(b);list.append(r);", """b.onclick=()=>download('MA62-DEV3-Quarentena-'+(i+1)+'.json',item.body);r.append(b);
      if(!item.archived){const archive=document.createElement('button');archive.type='button';archive.textContent='Revisar e arquivar (sem recuperar)';archive.onclick=()=>ma62ArchiveQuarantine(item);r.append(archive);}
      list.append(r);""")
section("  if(ma62LedgerManualOnly&&!ma62LedgerManualApproved&&ma62LedgerRaw!==null){", 'function ma62BlockLedger(reason){', """  if(previous!==null)makeButton('Baixar -prev de sessão anterior/não comprovada',()=>download('MA62-DEV3-PREV-SESSAO-NAO-COMPROVADA.json',previous));
  if(snapshots.length){
    const details=document.createElement('details'),summary=document.createElement('summary');summary.textContent='Cópias locais por operação (não incluídas no backup principal)';details.append(summary);
    snapshots.forEach(item=>{const line=document.createElement('p');line.textContent=(item.current?'Sessão atual · antes da operação indicada: ':'Outra sessão: ')+item.key+' ';
      const b=document.createElement('button');b.type='button';b.textContent='Baixar cópia';b.onclick=()=>download(item.key+'.json',item.body);line.append(b);details.append(line);});el.append(details);
  }
  if(ma62LedgerManualOnly&&!ma62LedgerManualApproved&&ma62LedgerRaw!==null){
    makeButton('Baixar cópia externa e confirmar',()=>{
      const raw=ma62LedgerRaw;
      download('MA62-DEV3-ANTES-GRAVAR-LIVRO-BRUTO.json',raw);
      if(confirm('Download solicitado ao navegador. O aplicativo ainda NÃO verificou o arquivo. Confirma que VOCÊ conferiu a cópia externa, abriu o arquivo e verificou seu conteúdo? Esta confirmação vale somente para o estado atual e uma operação.')){
        if(localStorage.getItem(ma62LedgerKey)!==raw){ma62BlockLedger('Livro alterado durante a confirmação externa; recarregue.');return;}
        ma62ExternalRaw=raw;ma62ExternalMode='confirmada manualmente';ma62LedgerManualApproved=true;ma62LedgerManualOnly=false;
        ma62Protection='Cópia externa confirmada manualmente para a próxima operação; sem cópia local. O aplicativo NÃO verificou o arquivo.';
        $('ledger-message').textContent='Cópia externa confirmada manualmente. Repita a operação; confirmação de uso único.';ma62LedgerBanner();
      }
    });
    const label=document.createElement('label');label.textContent='Verificar arquivo externo pelo conteúdo (sem restaurar)';
    const input=document.createElement('input');input.type='file';input.accept='.json';input.id='ma62-verify-ledger-file';label.append(input);actions.append(label);
    input.onchange=async()=>{try{
      const raw=ma62LedgerRaw,file=input.files?.[0];if(!file)return;
      if(file.size>new Blob([raw]).size+3)throw Error('Arquivo diferente do original');
      const text=await file.text();if(text!==raw)throw Error('Conteúdo diferente do livro atual');
      if(localStorage.getItem(ma62LedgerKey)!==raw)throw Error('Livro alterado por outra aba');
      ma62ExternalRaw=raw;ma62ExternalMode='verificada pelo conteúdo';ma62LedgerManualApproved=true;ma62LedgerManualOnly=false;
      ma62Protection='Arquivo externo verificado pelo conteúdo para a próxima operação; sem cópia local.';ma62LedgerBanner();
    }catch(err){$('ledger-message').textContent='Cópia externa NÃO verificada: '+err.message;}finally{input.value='';}};
  }
}""")
section('    if(!ma62LedgerPrevSaved){', "    const next=JSON.stringify(rows);", """    // AJ-14/15: preservar os bytes antes de CADA operação, sem limite arbitrário.
    const initial=ma62LedgerRaw===null?'[]':ma62LedgerRaw;
    if(!(ma62LedgerManualApproved&&ma62ExternalRaw===ma62LedgerRaw)){
      const copyKey=ma62SnapshotPrefix+ma62Session+'-'+(++ma62SnapshotSequence);
      try{
        localStorage.setItem(copyKey,initial);
        if(localStorage.getItem(copyKey)!==initial)throw Error('Cópia local não verificável');
        ma62LedgerPrevSaved=true;ma62LedgerManualOnly=false;
        ma62Protection='Cópia local verificada: '+copyKey+' (estado anterior à operação '+ma62SnapshotSequence+' desta sessão). A chave -prev permanece intacta.';
      }catch(err){
        ma62LedgerManualOnly=true;ma62LedgerManualApproved=false;ma62LedgerBanner();
        msg.textContent='Gravação bloqueada: não foi possível proteger a operação com cópia local. Original intacto. Baixe e verifique uma cópia externa.';return false;
      }
    }else{
      ma62Protection='Operação protegida por cópia externa '+ma62ExternalMode+' do estado anterior. Sem cópia local desta operação; faça nova cópia do estado atualizado.';
    }""")
replace("    ma62LedgerRaw=next;storageOK=true;msg.textContent='';", """    ma62LedgerRaw=next;storageOK=true;msg.textContent='';
    ma62LedgerManualOnly=false;ma62LedgerManualApproved=false;ma62ExternalRaw=null;ma62ExternalMode='';""")
replace("  }catch(err){storageOK=false;\n    msg.textContent='Não foi possível salvar: armazenamento cheio ou indisponível. As alterações desta tentativa não foram registradas.';", """  }catch(err){storageOK=false;
    ma62LedgerManualApproved=false;ma62ExternalRaw=null;ma62ExternalMode='';ma62LedgerManualOnly=false;
    ma62LedgerBanner('Gravação recusada; livro original preservado. A cópia de proteção, se criada, permanece guardada.');
    msg.textContent='Não foi possível salvar: armazenamento cheio ou indisponível. As alterações desta tentativa não foram registradas.';""")
section('function validRow(r){', 'ma62ReadLedger();', """function ma62RowIssues(r){
  const issues=[];
  if(!((typeof r.id==='string'&&r.id)||(typeof r.id==='number'&&Number.isFinite(r.id))))issues.push('ID');
  if(typeof r.date!=='string'||!/^\\d{4}-\\d{2}-\\d{2}$/.test(r.date)||!Number.isFinite(Date.parse(r.date))||new Date(r.date).toISOString().slice(0,10)!==r.date)issues.push('data');
  if(!['Cora','Sicredi'].includes(r.bank))issues.push('banco');
  if(typeof r.description!=='string'||!r.description.trim())issues.push('descrição');
  if(!Number.isSafeInteger(r.amount)||r.amount===0)issues.push('valor em centavos (inteiro seguro e diferente de zero)');
  if(!kinds.includes(r.kind))issues.push('categoria');
  if((r.kind==='Receita'&&r.amount<0)||(['Despesa','Retirada'].includes(r.kind)&&r.amount>0))issues.push('sinal do valor/categoria');
  return issues;
}
function validRow(r){const issues=ma62RowIssues(r);if(issues.length)throw Error('Campos inconsistentes: '+issues.join(', ')+'.');return r;}
function ma62ValidateChangedField(r,field){
  const issues=ma62RowIssues(r),match={date:'data',bank:'banco',description:'descrição',amount:'valor em centavos (inteiro seguro e diferente de zero)',kind:'categoria'};
  if(issues.includes(match[field]))throw Error('Campo inconsistente: '+match[field]+'.');
  if(['amount','kind'].includes(field)&&issues.includes('sinal do valor/categoria'))throw Error('Receita deve ser positiva; despesa e retirada devem ser negativas. Corrija explicitamente o valor ou selecione categoria compatível.');
}
function ma62ApplyCorrection(index,field,value){
  const original=rows[index];if(!original)throw Error('Lançamento não encontrado');
  const next={...original,[field]:value};ma62ValidateChangedField(next,field);
  if(field==='amount'&&value!==original.amount&&!confirm('ALTERAÇÃO FINANCEIRA EXPLÍCITA: '+JSON.stringify(original.amount)+' → '+JSON.stringify(value)+' centavos. Esta mudança afeta os totais. Confirma?'))return false;
  if(field==='kind'&&value!==original.kind&&!confirm('Alterar categoria de '+JSON.stringify(original.kind??null)+' para '+JSON.stringify(value)+'? O valor original será preservado; os totais por categoria podem mudar.'))return false;
  rows[index]=next;if(!persist()){rows[index]=original;return false;}
  renderLedger();$('ledger-message').textContent='Campo '+field+' corrigido explicitamente. Outros campos preservados.'+(ma62LegacyIssue(next)?' Ainda requer revisão: '+ma62LegacyIssue(next):'');return true;
}
function ma62EditLegacy(index){
  const original=rows[index];if(!original)return;
  const d=document.createElement('dialog');d.id='ma62-edit-legacy';
  const title=document.createElement('h2');title.textContent='Corrigir um campo do lançamento';
  const info=document.createElement('p');info.textContent='ID original: '+JSON.stringify(original.id)+'. '+(ma62LegacyIssue(original)||'Campos no padrão atual')+'. Altere um campo por vez. O original é protegido antes da gravação.';
  const form=document.createElement('form'),label=document.createElement('label'),field=document.createElement('select');field.id='ma62-edit-field';label.textContent='Campo a corrigir';
  [['bank','Banco'],['date','Data (AAAA-MM-DD)'],['description','Descrição'],['amount','Valor original em CENTAVOS'],['kind','Categoria']].forEach(([v,t])=>{const o=document.createElement('option');o.value=v;o.textContent=t;field.append(o);});label.append(field);
  const valueLabel=document.createElement('label');valueLabel.textContent='Novo valor (não altera os demais campos)';const input=document.createElement('input');input.id='ma62-edit-value';input.required=true;valueLabel.append(input);
  const update=()=>{input.value=String(original[field.value]??'');};field.onchange=update;update();
  const msg=document.createElement('p');msg.id='ma62-edit-message';msg.setAttribute('role','status');
  const save=document.createElement('button');save.type='submit';save.textContent='Confirmar correção';const cancel=document.createElement('button');cancel.type='button';cancel.textContent='Cancelar';cancel.onclick=()=>d.close();
  form.append(label,valueLabel,save,cancel,msg);d.append(title,info,form);document.body.append(d);d.onclose=()=>d.remove();
  form.onsubmit=e=>{e.preventDefault();try{if(rows[index]!==original)throw Error('Lançamento mudou; feche e abra novamente');
    const v=field.value==='amount'?Number(input.value):input.value;
    if(ma62ApplyCorrection(index,field.value,v))d.close();else msg.textContent=$('ledger-message').textContent||'Correção cancelada; nada foi alterado.';
  }catch(err){msg.textContent=err.message;}};d.showModal();
}""")
replace("'<small style=\"color:#9c5524;font-weight:bold\">⚠️ Registro antigo: conferir campos</small>'", "'<small style=\"color:#9c5524;font-weight:bold\">⚠️ Registro antigo: '+esc(ma62LegacyIssue(r))+'</small>'")
replace('data-row="${esc(r.id)}"', 'data-row="${rows.indexOf(r)}"')
replace('<button data-delete="${esc(r.id)}">Excluir</button>', '<button data-edit-legacy="${rows.indexOf(r)}">Revisar/corrigir</button> <button data-delete="${rows.indexOf(r)}">Excluir</button>')
section("$('transactions').querySelectorAll('[data-row]')", "$('month').oninput=renderLedger;", """$('transactions').querySelectorAll('[data-row]').forEach(s=>s.onchange=()=>{const index=Number(s.dataset.row);try{ma62ApplyCorrection(index,'kind',s.value);renderLedger();}catch(err){renderLedger();$('ledger-message').textContent=err.message;}});
$('transactions').querySelectorAll('[data-edit-legacy]').forEach(b=>b.onclick=()=>ma62EditLegacy(Number(b.dataset.editLegacy)));
$('transactions').querySelectorAll('[data-delete]').forEach(b=>b.onclick=()=>{const index=Number(b.dataset.delete);if(!confirm('Excluir somente este lançamento? A cópia de proteção preservará o estado anterior.'))return;const oldRows=rows;rows=rows.filter((x,i)=>i!==index);if(!persist())rows=oldRows;renderLedger();});}
""")
replace("r.id.startsWith(r.bank+':')?r.id.slice(r.bank.length+1):r.id", "String(r.id).startsWith(r.bank+':')?String(r.id).slice(r.bank.length+1):r.id")
replace("$('export').onclick=()=>{let quote", "$('export').onclick=()=>{if(ma62LedgerRejected.length||ma62LedgerQuarantines.length||ma62LedgerBlocked)$('ledger-message').textContent='CSV dos lançamentos legíveis: NÃO contém o original ilegível nem quarentenas. Preserve as cópias brutas separadamente.';let quote")
replace('<h2>Backup completo</h2>', '<h2>Backup principal · escopo do formato 6.1</h2>')
replace('id="backup-save" class="primary">Baixar backup completo', 'id="backup-save" class="primary">Baixar backup principal')
replace('<p id="backup-message" role="status"></p>', '<p id="backup-message" role="status"></p><p class="caption">Este backup principal NÃO é uma cópia completa de todos os módulos. Quarentenas, cópias locais, Academia e checklists exigem arquivos separados. Exportação parcial restaurável e restauração ampliada de legados: pendentes para A5.</p><button type="button" id="ma62-export-care-raw">Baixar cópia BRUTA do cadastro/pagamentos/evoluções</button><p id="ma62-care-raw-message" role="status"></p><label>Verificar o arquivo principal baixado (sem restaurar)<input id="ma62-verify-backup" type="file" accept=".json"></label>')
section("el('backup-save').onclick=()=>{", "el('backup-load').onchange=", """let ma62LastBackup=null;
function ma62RequestBackup(target){
  const report=(ok,message,state='refused')=>{const result={ok,message,state};el('backup-message').textContent=message;if(target)target.textContent=message;return result;};
  if(readError)return report(false,'BACKUP PRINCIPAL RECUSADO: cadastro ilegível ou armazenamento indisponível. Baixe a cópia BRUTA do cadastro; restauração/reparo pendentes para A5.');
  ma62ReadQuarantines();
  if(ma62HasLedgerRisk()){
    ma62LedgerBanner();return report(false,'BACKUP PRINCIPAL RECUSADO: livro ilegível/bloqueado, linhas rejeitadas, registros inconsistentes ou quarentenas ativas. Nenhum download foi solicitado. Baixe as cópias BRUTAS do cadastro e do livro, revise/corrija os registros e arquive somente quarentenas já conferidas. Exportação parcial restaurável: PENDENTE A5.');
  }
  try{
    const raw=localStorage.getItem('ma-ledger-v1'),ledger=raw===null?[]:JSON.parse(raw);
    if(!Array.isArray(ledger)||ledger.some(x=>!ma62LegacyReadable(x)))throw Error('Livro-caixa não validado');
    if(raw!==ma62LedgerRaw)throw Error('Livro-caixa alterado por outra aba; recarregue');
    // A1.2 preserva IDs numéricos na leitura. Ampliar o restaurador está reservado para A5.
    if(ledger.some(x=>typeof x.id!=='string'))throw Error('ID numérico preservado no livro; restauração deste legado PENDENTE A5. Use a cópia BRUTA');
    const currentCare=localStorage.getItem(key);
    if(currentCare!==null&&JSON.stringify(validate(JSON.parse(currentCare)))!==JSON.stringify(db))throw Error('Cadastro alterado por outra aba; recarregue');
    validate(db);
    const rateSettings=JSON.parse(localStorage.getItem('ma-installment-rates-v1')||'{}');
    if(!rateSettings||typeof rateSettings!=='object'||Array.isArray(rateSettings))throw Error('Taxas não reconhecidas');
    const archived=ma62LedgerQuarantines.filter(q=>q.archived).length;
    const text=JSON.stringify({format:'manfrin-arnez-backup',version:2,createdAt:new Date().toISOString(),care:db,ledger,rateSettings},null,2);
    saveFile('Manfrin-Arnez-backup-PRINCIPAL'+(archived?'-QUARENTENAS-SEPARADAS':'')+'-'+today()+'.json',text,'application/json');ma62LastBackup=text;
    return report(true,'DOWNLOAD PRINCIPAL SOLICITADO AO NAVEGADOR; arquivo ainda NÃO verificado. '+(archived?archived+' quarentena(s) arquivada(s) OMITIDA(S), não recuperadas; exporte-as separadamente. ':'')+'Não é backup completo de todos os módulos: Academia, checklists e cópias locais exigem exportações próprias.','requested');
  }catch(err){return report(false,'BACKUP PRINCIPAL RECUSADO: '+err.message+'. Nenhum download foi solicitado.');}
}
el('backup-save').onclick=()=>ma62RequestBackup(el('backup-message'));
el('ma62-verify-backup').onchange=async e=>{try{
  const file=e.target.files?.[0];if(!file)return;
  if(!ma62LastBackup)throw Error('Solicite primeiro um backup nesta sessão');
  if(file.size!==new Blob([ma62LastBackup]).size||await file.text()!==ma62LastBackup)throw Error('Arquivo não corresponde ao último download solicitado');
  el('backup-message').textContent='ARQUIVO PRINCIPAL VERIFICADO: conteúdo idêntico ao último download solicitado nesta sessão. Não comprova dados posteriores nem inclui módulos/cópias omitidos.';
}catch(err){el('backup-message').textContent='ARQUIVO NÃO VERIFICADO: '+err.message;}finally{e.target.value='';}};
function ma62ExportCareRaw(target){
  try{
    const raw=localStorage.getItem(key);if(raw===null)throw Error('Não existe cadastro persistido nesta chave; nenhum arquivo substitutivo foi gerado');
    saveFile('Manfrin-Arnez-CADASTRO-PAGAMENTOS-EVOLUCOES-BRUTO-NAO-RESTAURAR-'+today()+'.json',raw,'application/json');
    target.textContent='Cópia BRUTA do cadastro/pagamentos/evoluções solicitada ao navegador, sem validação nem alteração. NÃO é backup completo nem arquivo aceito pelo restaurador atual. Guarda forense e recuperação ampliada: A5. Confira o arquivo.';
  }catch(err){target.textContent='Cópia BRUTA recusada: '+err.message;}
}
el('ma62-export-care-raw').onclick=()=>ma62ExportCareRaw(el('ma62-care-raw-message'));
const careButton=document.createElement('button');careButton.type='button';careButton.id='ma62-account-care-raw';careButton.textContent='Baixar cópia BRUTA do cadastro/pagamentos/evoluções';careButton.onclick=()=>ma62ExportCareRaw(el('ma53-recovery-status'));el('ma53-account-backup').after(careButton);
""")
section("el('ma53-account-backup').onclick=()=>{", "el('ma53-merge-file').onchange=", "el('ma53-account-backup').onclick=()=>ma62RequestBackup(el('ma53-recovery-status'));\n")
replace("saveFile('Manfrin-Arnez-ANTES-MESCLAR-'+today()+'.json'", "saveFile('Manfrin-Arnez-ANTES-MESCLAR-PRINCIPAL-NAO-INCLUI-QUARENTENAS-'+today()+'.json'")
replace('Será baixada uma cópia dos dados atuais ANTES da mesclagem.', 'Será solicitado o download da cópia PRINCIPAL ANTES da mesclagem. Ela NÃO inclui quarentenas, cópias locais, Academia ou checklists; preserve-os separadamente. O navegador não confirma que o arquivo foi salvo.')
replace("function renderLedger(){const month=", "function renderLedger(){const rowPositions=new Map(rows.map((r,i)=>[r,i]));const month=")
s=s.replace('${rows.indexOf(r)}','${rowPositions.get(r)}')
OUT.write_text(s)
print(OUT)
print('bytes', OUT.stat().st_size, 'sha256', hashlib.sha256(OUT.read_bytes()).hexdigest())
