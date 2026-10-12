/* A5 — snapshot versionado, preimage recuperável e restauração exclusiva. */
(()=>{'use strict';
const A=window.MA5,ls=localStorage,rawGet=ls.getItem.bind(ls),rawSet=ls.setItem.bind(ls),rawRemove=ls.removeItem.bind(ls);
const CONTROL='ma5-restore-pending-v1',EPOCH='ma5-restore-epoch-v1',SUPPRESS='ma5-suppress-seeds-v1',RESERVE='ma5-reservation:';
const APP_LOCK='__MA_DEV61_SANDBOX__:ma5-open-apps',FORMAT='manfrin-arnez-dashboard-backup',NS='__MA_DEV61_SANDBOX__:';
const known={
 'ma-care-v2':'Pacientes, pagamentos e evoluções',
 'ma-ledger-v1':'Livro-caixa',
 'ma-installment-rates-v1':'Taxas financeiras',
 'ma-account-month-last-v1':'Preferência de mês',
 'ma-academy-v55':'Academia, materiais, equipamentos, sessões, POPs e Laboratório',
 'ma56-project-checklist-v1':'Checklist de Desenvolvimento (checklist56)',
 'ma61-sanitary-checklist-v1':'Central Sanitária'
};
let internal=0,presenceTask=null,releasePresence=null;
A.epoch=rawGet(EPOCH);A.presenceReady=false;A.exclusive=false;A.guardFailure='';A.lastBackupText=null;A.pendingPreview=null;
const protectedKey=k=>k==='ma-ledger-v1-prev'||k.startsWith('ma-ledger-v1-session-prev-')||k.startsWith('ma-ledger-v1-rejeitados-')||k.startsWith('ma-ledger-v1-quarantine-review:');
const transient=k=>k==='ma-storage-check'||k===CONTROL||k===EPOCH||k===SUPPRESS||k.startsWith(RESERVE);
const safeObject=x=>A.plain(x);
function noDanger(x,depth=0){if(depth>50)throw Error('Estrutura profunda demais');if(x&&typeof x==='object')for(const k of Object.keys(x)){if(['__proto__','prototype','constructor'].includes(k))throw Error('Propriedade insegura no conteúdo');noDanger(x[k],depth+1);}}
function blocked(message){A.guardFailure=message;showGuard();throw Error(message);}
function showGuard(){if(!document.querySelector('main'))return;let e=document.getElementById('ma5-guard-alert');if(!A.guardFailure){e?.remove();return;}
 if(!e){e=document.createElement('section');e.id='ma5-guard-alert';e.setAttribute('role','alert');e.style.cssText='border:2px solid #9c3027;background:#fff1ec;padding:12px;color:#792f24';document.querySelector('main').prepend(e);}e.textContent='GRAVAÇÃO BLOQUEADA — '+A.guardFailure;
}
function guard(k){if(internal)return;
 if(!A.presenceReady)blocked('Inicialização/recuperação ou restauração em andamento. Aguarde; nenhuma alteração será gravada.');
 if(rawGet(CONTROL)!==null)blocked('Restauração interrompida ou em andamento. Feche outras abas e use a recuperação antes de gravar.');
 if(rawGet(EPOCH)!==A.epoch)blocked('O estado foi restaurado por outra aba. Recarregue antes de editar.');
 if([CONTROL,EPOCH,SUPPRESS].includes(k)||k.startsWith(RESERVE))blocked('Metadados de recuperação não podem ser alterados por módulos comuns.');
 if(['ma-academy-v55','ma56-project-checklist-v1','ma61-sanitary-checklist-v1'].includes(k)){
  const old=rawGet(k);if(old!==null){try{const data=JSON.parse(old);if(data?.version!==1)blocked('Base '+k+' de versão desconhecida: original preservado; use o backup bruto/unificado.');}catch(e){if(A.guardFailure)throw e;blocked('Base '+k+' ilegível: original preservado.');}}
 }
}
ls.setItem=(k,v)=>{k=String(k);guard(k);return rawSet(k,String(v));};
ls.removeItem=k=>{k=String(k);guard(k);return rawRemove(k);};
ls.clear=()=>{throw Error('Limpeza global proibida. Use somente seleção de cópias exportadas e verificadas.');};
const managed=(fn)=>{internal++;try{return fn();}finally{internal--;}};
function write(k,v){return managed(()=>ls.setItem(k,v));}
function remove(k){return managed(()=>ls.removeItem(k));}
function entries(){return A.localEntries().filter(r=>!transient(r.key));}
const fingerprint=items=>A.canonical(items);
async function acquirePresence(){if(A.presenceReady)return;
 if(!navigator.locks?.request)throw Error('Navegador sem Web Locks: restauração e gravações protegidas indisponíveis');
 await new Promise((resolve,reject)=>{presenceTask=navigator.locks.request(APP_LOCK,{mode:'shared'},async()=>{A.presenceReady=true;resolve();await new Promise(r=>releasePresence=r);A.presenceReady=false;}).catch(reject);});
}
async function release(){if(releasePresence){releasePresence();releasePresence=null;await presenceTask;presenceTask=null;A.presenceReady=false;}}
async function singleTab(fn){await release();try{return await navigator.locks.request(APP_LOCK,{mode:'exclusive',ifAvailable:true},async lock=>{if(!lock)throw Error('Outra aba DEV.4 está aberta. Feche-a antes de restaurar; nenhum dado foi substituído.');A.exclusive=true;try{return await fn();}finally{A.exclusive=false;}});}finally{await acquirePresence();}}
function describe(key,raw){const result={key,module:known[key]||'Proteção/estado bruto',present:raw!==null,health:'healthy',counts:{},warning:''};if(raw===null){result.health='absent';return result;}
 try{
  if(key==='ma-account-month-last-v1'){if(!/^\d{4}-(0[1-9]|1[0-2])$/.test(raw))throw Error('Mês não reconhecido');return result;}
  if(protectedKey(key)){result.health='protected';result.counts={bytesEstimated:2*raw.length};return result;}
  if(!Object.hasOwn(known,key)){result.health='opaque';result.warning='Chave persistida sem leitor conhecido nesta versão; bytes incluídos sem presumir módulo.';result.counts={bytesEstimated:2*raw.length};return result;}
  const data=JSON.parse(raw);noDanger(data);
  if(key==='ma-care-v2'){if(!A.validateCare)throw Error('Validador clínico não inicializado');A.validateCare(data);result.counts={patients:data.patients.length,records:data.records.length,notes:data.notes.length};}
  if(key==='ma-ledger-v1'){if(!Array.isArray(data)||data.some(r=>!ma62LegacyReadable(r)))throw Error('Livro contém JSON/linhas não legíveis');result.counts={rows:data.length,legacy:data.filter(r=>!!ma62LegacyIssue(r)).length,numericIDs:data.filter(r=>typeof r.id==='number').length};}
  if(key==='ma-installment-rates-v1'){if(!safeObject(data)||Object.entries(data).some(([k,v])=>!/^(10|[1-9])$/.test(k)||!['number','string'].includes(typeof v)||!Number.isFinite(Number(v))||Number(v)<0||Number(v)>=100))throw Error('Taxas de formato/valor não reconhecido');result.counts={rates:Object.keys(data).length};}
  if(key==='ma-academy-v55'){
   if(!safeObject(data)||data.version!==1||!safeObject(data.settings)||!['materials','equipment','sessions','customPops','training'].every(k=>Array.isArray(data[k]))||data.checks!==undefined&&!safeObject(data.checks))throw Error('Academia de versão/estrutura desconhecida');
   for(const field of ['ma58','ma59','ma60'])if(data[field]!==undefined){const x=data[field];if(!safeObject(x)||x.version!==1)throw Error('Progresso '+field+' não reconhecido');for(const k of ['kind','base','target','current','filter','search','blastMaterial'])if(x[k]!==undefined&&typeof x[k]!=='string')throw Error('Campo inválido em '+field+': '+k);for(const k of ['checks','step','material','washChecks','blastChecks','colorZone'])if(x[k]!==undefined&&!safeObject(x[k]))throw Error('Mapa inválido em '+field+': '+k);}
   result.counts=Object.fromEntries(['materials','equipment','sessions','customPops','training'].map(k=>[k,data[k].length]));result.counts.labProgress=['ma58','ma59','ma60'].filter(k=>data[k]!==undefined).length;
  }
  if(key==='ma56-project-checklist-v1'){
   if(!safeObject(data)||data.version!==1||!safeObject(data.states)||!safeObject(data.updated)||Object.values(data.states).some(v=>!['todo','progress','review','done'].includes(v))||Object.values(data.updated).some(v=>typeof v!=='string'))throw Error('Checklist56 não reconhecido');result.counts={states:Object.keys(data.states).length};
  }
  if(key==='ma61-sanitary-checklist-v1'){
   if(!safeObject(data)||data.version!==1)throw Error('Checklist sanitário de versão desconhecida');
   for(const k of ['states','evidence','notes','responsible','due','updated'])if(data[k]!==undefined&&(!safeObject(data[k])||Object.entries(data[k]).some(([id,v])=>typeof v!=='string'||A.sanitaryIDs&&!A.sanitaryIDs.has(id))))throw Error('Campo sanitário inválido: '+k);
   if(Object.values(data.states||{}).some(v=>!['ok','warn','bad'].includes(v)))throw Error('Semáforo desconhecido');result.counts={states:Object.keys(data.states||{}).length,fronts:8,subtopics:42};
  }
 }catch(e){result.health='invalid';result.warning=e.message;result.counts={unavailable:true};}return result;
}
async function completeBackup(){return A.lock(async()=>{
 if(rawGet(CONTROL)!==null)throw Error('Recuperação pendente; exporte o histórico anterior, não o estado intermediário');
 const state=entries(),start=fingerprint(state),records=await A.all();
 for(const r of records)if(typeof r.raw!=='string'||await A.sha(r.raw)!==r.sha256)throw Error('Histórico corrompido: '+r.id+'; nenhum backup completo declarado');
 if(fingerprint(entries())!==start)throw Error('Dados mudaram durante a coleta; repita o backup');
 const descriptions=state.map(r=>describe(r.key,r.raw)),absent=Object.keys(known).filter(k=>!state.some(x=>x.key===k));
 const warnings=descriptions.filter(x=>['invalid','opaque'].includes(x.health)).map(x=>x.key+': '+x.warning);
 const external=records.filter(r=>r.kind==='cleanup').map(r=>JSON.parse(r.raw));
 const separateExports=external.filter(receipt=>receipt.entries.some(x=>x.storage==='indexedDB'?!records.some(r=>r.id===x.id):rawGet(x.key)===null)).map(x=>({name:x.archiveName,sha256:x.archiveDigest,scope:'Estados históricos liberados somente após exportação externa verificada; mantenha este arquivo junto ao snapshot.'}));
 if(separateExports.length)warnings.push('Existem estados históricos arquivados fora do navegador. Este arquivo não os recria; guarde os '+separateExports.length+' arquivos externos identificados.');
 const payload={format:FORMAT,version:3,id:crypto.randomUUID(),createdAt:new Date().toISOString(),namespace:NS,environment:'DEV_FICTITIOUS_ONLY',appVersion:'6.2-dev.4',baseHTMLSha256:'e4e4f49ca37e85cd9c83c67aa79b4e9d2fcb74b11137c387a5692ea8727bcc3f',coverage:{status:warnings.length?'PARCIAL':'COMPLETO_ESTADO_PERSISTIDO',included:descriptions,absent,quarantines:state.filter(x=>x.key.startsWith('ma-ledger-v1-rejeitados-')).map(x=>x.key),separateExports,warnings,scope:'Todas as chaves DEV persistidas e registros IndexedDB de proteção; arquivos fixos/rascunhos não salvos permanecem no HTML e não são inventados.'},state:[],protection:records,metadata:{suppressEmbeddedSeeds:rawGet(SUPPRESS)==='1',restoreEpoch:rawGet(EPOCH),database:'__MA_DEV61_SANDBOX__:ma5-protection-v1'}};
 for(const item of state)payload.state.push({...item,sha256:await A.sha(item.raw)});
 const file={...payload,integrity:{algorithm:'SHA-256',digest:await A.sha(A.canonical(payload))}};
 if(fingerprint(entries())!==start)throw Error('Dados mudaram durante a exportação; repita o backup');return file;
});}
async function exportBackup(target){try{target.textContent='Preparando snapshot e verificando integridade…';const file=await completeBackup(),text=JSON.stringify(file,null,2);A.download('Manfrin-Arnez-BACKUP-'+file.coverage.status+'-V3-'+file.createdAt.slice(0,10)+'.json',text);A.lastBackupText=text;
 target.textContent='DOWNLOAD SOLICITADO: '+file.coverage.status+'. Arquivo ainda NÃO verificado. '+file.state.length+' chaves e '+file.protection.length+' registros de proteção incluídos. '+(file.coverage.warnings.join(' ')||'Nenhuma base persistida foi omitida. Bases ausentes são identificadas; dados não salvos/arquivos fixos estão fora do snapshot.');return {ok:true,file,text};
 }catch(e){target.textContent='BACKUP RECUSADO: '+e.message+'. Nenhum download solicitado.';return {ok:false,message:e.message};}}
// Conserva os trechos JSON v2 sem converter IDs, valores, bancos ou formatação.
function topLevelSlices(text){let i=0;const out=new Map();const ws=()=>{while(/\s/.test(text[i]||'')&&i<text.length)i++;};ws();if(text[i++]!=='{')throw Error('Objeto JSON esperado');ws();if(text[i]==='}')return out;
 while(i<text.length){ws();const start=i;if(text[i++]!=='"')throw Error('Chave JSON inválida');while(i<text.length){if(text[i]==='\\'){i+=2;continue;}if(text[i++]==='"')break;}const key=JSON.parse(text.slice(start,i));if(out.has(key))throw Error('Chave duplicada no arquivo: '+key);ws();if(text[i++]!==':')throw Error('JSON inválido');ws();const begin=i;let depth=0,string=false;
  for(;i<text.length;i++){const c=text[i];if(string){if(c==='\\'){i++;continue;}if(c==='"')string=false;continue;}if(c==='"'){string=true;continue;}if(c==='['||c==='{')depth++;if(c===']'||c==='}'){if(depth===0)break;depth--;}if(c===','&&depth===0)break;}
  const raw=text.slice(begin,i).trim();JSON.parse(raw);out.set(key,raw);if(text[i]==='}')break;if(text[i++]!==',')throw Error('JSON inválido');
 }return out;
}
async function inspectText(text){const slices=topLevelSlices(text),file=JSON.parse(text);
 if(!safeObject(file))throw Error('Arquivo não é objeto JSON');
 if(file.format==='manfrin-arnez-backup'){
  if(file.version!==2)throw Error('Versão legada não suportada: '+file.version);const map=[['care','ma-care-v2'],['ledger','ma-ledger-v1'],['rateSettings','ma-installment-rates-v1']],state=[];
  for(const [name,key] of map)if(Object.hasOwn(file,name)){const raw=slices.get(name),d=describe(key,raw);if(d.health!=='healthy')throw Error('Backup v2 inválido em '+name+': '+d.warning);state.push({key,raw,sha256:await A.sha(raw)});}
  if(!state.length)throw Error('Backup v2 sem módulos reconhecidos');return {format:file.format,version:2,state,protection:[],coverage:{status:state.length===3?'LEGADO_V2_ESPECIFICO':'PARCIAL',warnings:['Formato v2 sem SHA-256 original e sem módulos administrativos/histórico. Campos ausentes serão mantidos.']},digest:await A.sha(text)};
 }
 if(file.format!==FORMAT||file.version!==3||file.namespace!==NS||file.environment!=='DEV_FICTITIOUS_ONLY')throw Error('Formato/versão/ambiente não suportados');
 const {integrity,...payload}=file;if(!safeObject(integrity)||integrity.algorithm!=='SHA-256'||await A.sha(A.canonical(payload))!==integrity.digest)throw Error('Integridade SHA-256 não confere');
 if(!Array.isArray(file.state)||!Array.isArray(file.protection))throw Error('Bases/histórico ausentes');const keys=new Set(),ids=new Set();
 for(const entry of file.state){if(!safeObject(entry)||typeof entry.key!=='string'||!entry.key||entry.key.length>512||transient(entry.key)||entry.key.startsWith(NS)||typeof entry.raw!=='string'||keys.has(entry.key))throw Error('Chave de estado inválida/duplicada/reservada');keys.add(entry.key);if(await A.sha(entry.raw)!==entry.sha256)throw Error('SHA-256 da base não confere: '+entry.key);}
 for(const r of file.protection){if(!safeObject(r)||typeof r.id!=='string'||!['operation','restore','cleanup'].includes(r.kind)||typeof r.raw!=='string'||ids.has(r.id)||await A.sha(r.raw)!==r.sha256)throw Error('Registro de proteção inválido');ids.add(r.id);if(r.kind==='operation'&&r.key!=='ma-ledger-v1')throw Error('Origem de operação não reconhecida');if(r.kind==='restore'){const blob=JSON.parse(r.raw);if(blob.version!==1||!Array.isArray(blob.preimage)||!Array.isArray(blob.targets))throw Error('Preimage inválida');}if(r.kind==='cleanup'){const receipt=JSON.parse(r.raw);if(receipt.version!==1||!Array.isArray(receipt.entries)||typeof receipt.archiveDigest!=='string')throw Error('Comprovante externo inválido');}}
 // historyIDs nos journals são inventário histórico, não dependência para recuperar
 // as bases: a preimage é autocontida. Cópias liberadas continuam nos arquivos externos.
 return {...file,digest:await A.sha(text)};
}
function duplicateInfo(raw){try{const data=JSON.parse(raw),rows=Array.isArray(data)?data:[...(data.patients||[]),...(data.records||[]),...(data.notes||[])];const ids=new Set();let repeats=0;for(const r of rows){const id=JSON.stringify(r.id);if(ids.has(id))repeats++;else ids.add(id);}return repeats;}catch(_){return null;}}
function conflicts(old,raw){try{const before=JSON.parse(old),after=JSON.parse(raw);const arrays=x=>Array.isArray(x)?x:[...(x.patients||[]),...(x.records||[]),...(x.notes||[])];const prior=new Map(arrays(before).map(r=>[JSON.stringify(r.id),A.canonical(r)]));return arrays(after).filter(r=>prior.has(JSON.stringify(r.id))&&prior.get(JSON.stringify(r.id))!==A.canonical(r)).length;}catch(_){return null;}}
async function planText(text){const file=await inspectText(text),before=entries(),baseFingerprint=fingerprint(before),existing=await A.all(),targets=[],skipped=[],summary=[];
 for(const item of file.state){const old=rawGet(item.key),info=describe(item.key,item.raw);if(protectedKey(item.key)&&old!==null&&old!==item.raw)throw Error('Conflito de proteção: '+item.key+'. A cópia/quarentena/revisão atual não será sobrescrita.');
  if(info.health==='invalid'){skipped.push(item);summary.push({key:item.key,action:'MANTER ATUAL; arquivo ilegível/de versão não suportada fica protegido no journal',reason:info.warning,before:describe(item.key,old).counts,incoming:info.counts});continue;}
  targets.push(item);summary.push({key:item.key,action:old===item.raw?'IDÊNTICO; manter':old===null?'ADICIONAR':protectedKey(item.key)?'MANTER PROTEÇÃO':'SUBSTITUIR COM PREIMAGE RECUPERÁVEL',before:describe(item.key,old).counts,incoming:info.counts,duplicateIDs:duplicateInfo(item.raw),changedSameIDs:conflicts(old,item.raw),warning:info.warning});
 }
 for(const r of file.protection){const prev=existing.find(x=>x.id===r.id);if(prev&&(prev.raw!==r.raw||prev.kind!==r.kind||prev.sha256!==r.sha256))throw Error('Conflito de ID de histórico: '+r.id);}
 const absent=Object.keys(known).filter(k=>!file.state.some(x=>x.key===k));for(const key of absent)summary.push({key,action:'AUSENTE NO ARQUIVO: MANTER ATUAL',before:describe(key,rawGet(key)).counts,incoming:{absent:true}});
 if(!targets.length)throw Error('Nenhuma base restaurável neste arquivo; mantenha a cópia bruta para recuperação manual.');
 return {file,baseFingerprint,targets,skipped,summary,absent,history:file.protection.filter(r=>!existing.some(x=>x.id===r.id)),historyIDs:existing.map(r=>r.id),sourceDigest:file.digest};
}
function showPreview(plan){const holder=document.getElementById('ma5-restore-preview');holder.replaceChildren();const title=document.createElement('h3');title.textContent='Prévia: '+plan.file.coverage.status+' · formato v'+plan.file.version;holder.append(title);
 const note=document.createElement('p');note.textContent='O estado anterior será protegido antes de qualquer substituição. Módulos ausentes ficam mantidos; registros/valores não são convertidos nem deduplicados. Feche todas as outras abas/versões do Dashboard. Somente dados fictícios.';holder.append(note);
 const table=document.createElement('table');for(const row of plan.summary){const tr=document.createElement('tr');for(const value of [row.key,row.action,'ANTES '+JSON.stringify(row.before),'ARQUIVO '+JSON.stringify(row.incoming),'IDs repetidos '+row.duplicateIDs+'; IDs alterados '+row.changedSameIDs+' '+(row.reason||row.warning||'')]){const td=document.createElement('td');td.textContent=value;tr.append(td);}table.append(tr);}const wrap=document.createElement('div');wrap.className='table-wrap';wrap.append(table);holder.append(wrap);
 const hist=document.createElement('p');hist.textContent=plan.history.length+' registro(s) de proteção adicionável(is); históricos atuais não serão apagados. '+plan.skipped.length+' base(s) inválida(s) não aplicada(s), com bytes guardados no arquivo e no journal.';holder.append(hist);document.getElementById('ma5-restore-confirm').disabled=false;
}
async function prepare(plan){if(rawGet(CONTROL)!==null)throw Error('Existe recuperação pendente');if(fingerprint(entries())!==plan.baseFingerprint)throw Error('Dados mudaram desde a prévia; selecione novamente o arquivo');
 const preimage=A.localEntries().filter(x=>x.key!==CONTROL&&!x.key.startsWith(RESERVE));const blob={version:1,preimage,targets:plan.targets,skipped:plan.skipped,historyIDs:plan.historyIDs,sourceDigest:plan.sourceDigest,summary:plan.summary};const raw=A.canonical(blob);
 const journal={id:'restore:'+crypto.randomUUID(),kind:'restore',phase:'prepared',createdAt:new Date().toISOString(),origin:'Antes de restauração A5',key:'dashboard-state',raw,sha256:await A.sha(raw)};
 await A.tx('readwrite',store=>{for(const r of plan.history)store.put(r);store.put(journal);});const verified=await A.get(journal.id);if(!verified||verified.raw!==raw||await A.sha(verified.raw)!==verified.sha256)throw Error('Preimage não conferida');
 if(fingerprint(entries())!==plan.baseFingerprint)throw Error('Estado mudou durante a proteção; nenhuma base foi substituída');
 try{write(CONTROL,JSON.stringify({version:1,id:journal.id,sha256:journal.sha256}));}catch(e){await A.put({...journal,phase:'refused'});throw Error('Sem espaço para marcador de recuperação. Dados atuais intactos. '+e.message);}
 return journal;
}
async function reserve(journal){const blob=JSON.parse(journal.raw),before=new Map(blob.preimage.map(x=>[x.key,x.raw]));let extra=2048;
 for(const t of blob.targets){const old=before.get(t.key);if(old===t.raw)continue;extra+=Math.max(0,(t.raw===null?0:t.raw.length+t.key.length)-(old===undefined?0:old.length+t.key.length));}
 const key=RESERVE+journal.id;const value='R'.repeat(2*extra);try{write(key,value);if(rawGet(key)?.length!==value.length)throw Error('Reserva não conferida');}finally{if(rawGet(key)!==null)remove(key);}
}
async function rollback(journal){if(await A.sha(journal.raw)!==journal.sha256)throw Error('Preimage corrompida; nenhuma recuperação automática permitida');const blob=JSON.parse(journal.raw),prior=new Map(blob.preimage.map(x=>[x.key,x.raw]));
 // Adições de proteção são retidas até em falhas; nunca apagar quarentenas/revisões.
 for(const item of blob.targets.filter(x=>!protectedKey(x.key)))remove(item.key);
 for(const item of blob.targets.filter(x=>!protectedKey(x.key)))if(prior.has(item.key))write(item.key,prior.get(item.key));
 for(const item of blob.preimage)if(![CONTROL,EPOCH,SUPPRESS].includes(item.key)&&!item.key.startsWith(RESERVE)&&rawGet(item.key)!==item.raw)throw Error('Não foi possível recuperar os bytes de '+item.key);
 write(SUPPRESS,'1');const epoch=crypto.randomUUID();write(EPOCH,epoch);A.epoch=epoch;await A.put({...journal,phase:'rolledback'});remove(CONTROL);return blob;
}
async function apply(plan){return A.lock(()=>singleTab(async()=>{const journal=await prepare(plan);let applied=false;
 try{await reserve(journal);const ordered=[...plan.targets.filter(x=>protectedKey(x.key)),...plan.targets.filter(x=>!protectedKey(x.key))];
  for(const item of ordered){if(rawGet(item.key)!==item.raw){if(item.raw===null)remove(item.key);else write(item.key,item.raw);if(rawGet(item.key)!==item.raw)throw Error('Gravação não conferida: '+item.key);}}
  write(SUPPRESS,'1');const epoch=crypto.randomUUID();write(EPOCH,epoch);A.epoch=epoch;
  const receipt={version:1,journalId:journal.id,completedAt:new Date().toISOString(),sourceDigest:plan.sourceDigest,summary:plan.summary,after:plan.targets.map(x=>describe(x.key,rawGet(x.key))),maintained:plan.absent,skipped:plan.skipped.map(x=>x.key)};
  await A.put({...journal,phase:'committed',receipt});remove(CONTROL);A.lastRestoreReceipt=receipt;applied=true;return receipt;
 }catch(err){try{await rollback(journal);}catch(recovery){A.guardFailure='Restauração interrompida: preimage preservada em IndexedDB, mas recuperação pendente. '+recovery.message;showGuard();throw Error(A.guardFailure);}
  throw Error('Restauração não concluída; estado anterior recuperado. '+err.message);
 }finally{if(!applied)A.pendingPreview=null;}
}));}
async function recoverPending(){const marker=rawGet(CONTROL);if(marker===null)return false;let control;try{control=JSON.parse(marker);}catch(_){throw Error('Marcador de recuperação ilegível: gravações bloqueadas');}
 const journal=await A.get(control.id);if(!journal||journal.kind!=='restore'||journal.sha256!==control.sha256||await A.sha(journal.raw)!==journal.sha256)throw Error('Preimage não disponível/conferida: não alterar dados');
 await rollback(journal);return true;
}
async function boot(){await A.ready;
 if(rawGet(CONTROL)!==null){const recovered=await navigator.locks.request(APP_LOCK,{mode:'exclusive',ifAvailable:true},async l=>{if(!l)return false;A.exclusive=true;try{return await recoverPending();}finally{A.exclusive=false;}});if(!recovered&&rawGet(CONTROL)!==null)throw Error('Há outra aba aberta ou recuperação pendente. Feche outras abas e recarregue. Preimage preservada.');}
 A.epoch=rawGet(EPOCH);await acquirePresence();if(rawGet(CONTROL)!==null)throw Error('Recuperação pendente. Feche outras abas e recarregue.');
}
async function revertJournal(id){const record=await A.get(id);if(!record||record.kind!=='restore'||await A.sha(record.raw)!==record.sha256)throw Error('Cópia de restauração não conferida');const blob=JSON.parse(record.raw);
 const targets=blob.preimage.filter(x=>!transient(x.key));const priorKeys=new Set(targets.map(x=>x.key));for(const t of blob.targets)if(!priorKeys.has(t.key)&&!protectedKey(t.key)&&!transient(t.key))targets.push({key:t.key,raw:null});const plan={file:{version:3,coverage:{status:'RECUPERACAO_PREIMAGE'}},targets,skipped:[],absent:Object.keys(known).filter(k=>!targets.some(x=>x.key===k)),history:[],historyIDs:(await A.all()).map(x=>x.id),baseFingerprint:fingerprint(entries()),sourceDigest:record.sha256,summary:targets.map(x=>({key:x.key,action:x.raw===null?'REMOVER BASE ADICIONADA POR ESTA RESTAURAÇÃO; ESTADO ANTERIOR AUSENTE':'RECUPERAR ESTADO ANTERIOR',before:describe(x.key,rawGet(x.key)).counts,incoming:describe(x.key,x.raw).counts}))};
 for(const t of targets)if(protectedKey(t.key)&&rawGet(t.key)!==null&&rawGet(t.key)!==t.raw)throw Error('Conflito de proteção ao recuperar '+t.key);
 showPreview(plan);A.pendingPreview=plan;document.getElementById('ma5-restore-confirm').disabled=false;return plan;
}
function bindUI(){A.mount();showGuard();const status=document.getElementById('backup-message'),panel=document.getElementById('backup').querySelector('.panel');
 panel.querySelector('h2').textContent='Backup unificado A5 · formato v3';document.getElementById('backup-save').textContent='Baixar backup unificado do estado persistido';
 const old=panel.querySelector('p');old.textContent='Inclui bases persistidas DEV, Academia, Laboratório, checklists, quarentenas, revisões e histórico de proteção em IndexedDB. Identifica bases ausentes/ilegíveis e não inventa dados.';
 const area=document.createElement('article');area.id='ma5-restore-panel';area.className='panel';area.innerHTML='<h2>Prévia e restauração recuperável</h2><p>Selecione um backup v3 ou v2. Não haverá substituição antes da prévia e confirmação. Módulos ausentes serão mantidos. Feche outras abas e versões do Dashboard. Use exclusivamente arquivos fictícios.</p><div id="ma5-restore-preview"></div><button type="button" id="ma5-restore-confirm" disabled>Confirmar restauração após a prévia</button><button type="button" id="ma5-restore-cancel">Cancelar prévia</button><p id="ma5-restore-status" role="status"></p><details><summary>Recuperar estado anterior de uma restauração</summary><div id="ma5-restore-journals"></div></details>';document.getElementById('backup').append(area);
 const feedback=document.getElementById('ma5-restore-status');document.getElementById('backup-save').onclick=()=>exportBackup(status);document.getElementById('ma53-account-backup').onclick=()=>exportBackup(document.getElementById('ma53-recovery-status'));
 A.onArchiveVerified=payload=>{let box=document.getElementById('ma5-archive-recovery');if(!box){box=document.createElement('article');box.id='ma5-archive-recovery';box.className='panel';document.getElementById('ma5-storage-panel').append(box);}box.replaceChildren();const label=document.createElement('p');label.textContent='Recuperar um estado do livro guardado no arquivo externo verificado (demais bases mantidas)';const select=document.createElement('select');select.id='ma5-archive-record';const copies=payload.records.filter(r=>r.kind==='operation'&&r.key==='ma-ledger-v1');copies.forEach((r,i)=>{const o=document.createElement('option');o.value=i;o.textContent=(r.createdAt||'data não comprovada')+' · '+r.id;select.append(o);});const button=document.createElement('button');button.type='button';button.id='ma5-archive-recover';button.textContent='Preparar prévia desta cópia externa';button.disabled=!copies.length;button.onclick=async()=>{try{const proof=A.verifiedArchive;if(!proof||await A.sha(await proof.file.text())!==proof.digest)throw Error('Arquivo externo não está mais conferido/acessível');const record=copies[Number(select.value)];if(await A.sha(record.raw)!==record.sha256)throw Error('Cópia alterada');const data={format:FORMAT,version:3,namespace:NS,environment:'DEV_FICTITIOUS_ONLY',coverage:{status:'PARCIAL_LIVRO_HISTORICO'},state:[{key:'ma-ledger-v1',raw:record.raw,sha256:record.sha256}],protection:[]};const file={...data,integrity:{algorithm:'SHA-256',digest:await A.sha(A.canonical(data))}};const plan=await planText(JSON.stringify(file));A.pendingPreview=plan;showPreview(plan);feedback.textContent='Cópia externa conferida: prévia pronta. Somente o livro será afetado; confirmação e preimage ainda obrigatórias.';}catch(e){feedback.textContent='Recuperação externa recusada: '+e.message;A.pendingPreview=null;}};box.append(label,select,button);};
 document.getElementById('backup-load').onchange=async e=>{A.pendingPreview=null;document.getElementById('ma5-restore-confirm').disabled=true;try{const file=e.target.files?.[0];if(!file)return;if(!confirm('Este arquivo contém SOMENTE dados FICTÍCIOS? É proibido abrir backups reais nesta DEV.'))return;
  feedback.textContent='Validando formato, bases e integridade…';const plan=await planText(await file.text());A.pendingPreview=plan;showPreview(plan);feedback.textContent='Prévia pronta. Nenhum dado foi substituído. '+(plan.file.version===2?'Legado v2 sem hash original: validação estrutural; dados originais preservados.':'SHA-256 do arquivo e das bases conferidos.');
 }catch(err){feedback.textContent='Prévia RECUSADA: '+err.message;A.pendingPreview=null;}finally{e.target.value='';}};
 document.getElementById('ma5-restore-cancel').onclick=()=>{A.pendingPreview=null;document.getElementById('ma5-restore-confirm').disabled=true;feedback.textContent='Prévia cancelada; dados não alterados.';};
 document.getElementById('ma5-restore-confirm').onclick=async()=>{try{const plan=A.pendingPreview;if(!plan)throw Error('Selecione novamente um arquivo');
  if(!confirm('RESTAURAÇÃO DEV: confirma as SUBSTITUIÇÕES e contagens exibidas na prévia? Módulos ausentes ficam mantidos; uma preimage de todo o estado anterior será guardada. Fechou todas as outras abas/versões do Dashboard?'))return;
  feedback.textContent='Protegendo estado anterior e restaurando…';const receipt=await apply(plan);feedback.textContent='Restauração concluída; estado anterior recuperável em '+receipt.journalId+'. Resultado com contagens antes/depois guardado no histórico. Recarregando…';A.pendingPreview=null;location.reload();
 }catch(e){feedback.textContent='RESTAURAÇÃO RECUSADA/FALHOU: '+e.message;showGuard();}};
 document.getElementById('ma62-verify-backup').onchange=async e=>{try{const file=e.target.files?.[0];if(!file)return;const text=await file.text();if(!A.lastBackupText)throw Error('Solicite um backup nesta sessão primeiro');if(text!==A.lastBackupText)throw Error('Arquivo não corresponde ao último download');await inspectText(text);status.textContent='ARQUIVO VERIFICADO: bytes idênticos ao download solicitado; SHA-256 e bases conferidos. A cobertura/ausências continuam as declaradas no arquivo.';}catch(err){status.textContent='ARQUIVO NÃO VERIFICADO: '+err.message;}finally{e.target.value='';}};
 A.all().then(records=>{const holder=document.getElementById('ma5-restore-journals');for(const r of records.filter(x=>x.kind==='restore')){const line=document.createElement('p');line.textContent=r.createdAt+' · '+r.phase+' · '+r.id+' ';const b=document.createElement('button');b.type='button';b.textContent='Preparar recuperação do estado anterior';b.onclick=()=>revertJournal(r.id).catch(e=>feedback.textContent='Recuperação recusada: '+e.message);line.append(b);holder.append(line);}
  const recent=records.filter(r=>r.kind==='restore').sort((a,b)=>a.createdAt.localeCompare(b.createdAt)).at(-1);if(recent?.receipt)feedback.textContent='Última restauração: '+recent.phase+'. Contagens/ações: '+JSON.stringify(recent.receipt.summary.map(x=>({key:x.key,before:x.before,file:x.incoming,after:recent.receipt.after.find(a=>a.key===x.key)?.counts||x.before,action:x.action})));else if(recent?.phase==='rolledback')feedback.textContent='Restauração anterior revertida: preimage e bytes anteriores preservados.';
 }).catch(e=>feedback.textContent='Histórico indisponível: '+e.message);
}
Object.assign(A,{known,protectedKey,transient,describe,completeBackup,exportBackup,inspectText,planText,showPreview,prepareRestore:prepare,applyRestore:apply,recoverPending,revertJournal,boot,bindUI,singleTab,managedWrite:write,managedRemove:remove,showGuard});
window.addEventListener('pagehide',()=>{releasePresence?.();});
})();
