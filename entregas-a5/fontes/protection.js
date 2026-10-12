/* A5: proteção local isolada. Não acessa nem envia dados para servidores. */
(()=>{'use strict';
const ls=window.localStorage, enc=new TextEncoder(), databaseName='__MA_DEV61_SANDBOX__:ma5-protection-v1';
const OP_PREFIX='ma-ledger-v1-session-prev-', LEDGER='ma-ledger-v1';
const A=window.MA5={version:1,dbError:'',verifiedArchive:null,lastDownload:null};
const plain=x=>!!x&&typeof x==='object'&&!Array.isArray(x);
const canonical=x=>JSON.stringify(x&&typeof x==='object'?(Array.isArray(x)?x.map(v=>JSON.parse(canonical(v))):Object.fromEntries(Object.keys(x).sort().map(k=>[k,JSON.parse(canonical(x[k]))]))):x);
async function sha(text){return [...new Uint8Array(await crypto.subtle.digest('SHA-256',enc.encode(text)))].map(x=>x.toString(16).padStart(2,'0')).join('');}
function download(name,text){const u=URL.createObjectURL(new Blob([text],{type:'application/json;charset=utf-8'})),a=document.createElement('a');a.href=u;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),10000);}
function request(store,method,...args){return new Promise((resolve,reject)=>{const r=store[method](...args);r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);});}
const ready=new Promise((resolve,reject)=>{const r=indexedDB.open(databaseName,1);r.onupgradeneeded=()=>r.result.createObjectStore('records',{keyPath:'id'});r.onsuccess=()=>{r.result.onversionchange=()=>r.result.close();resolve(r.result);};r.onerror=()=>reject(r.error);r.onblocked=()=>reject(Error('Histórico aberto com versão incompatível em outra aba'));});
ready.catch(e=>{A.dbError=String(e.message||e);});
async function tx(mode,fn){const db=await ready;return new Promise((resolve,reject)=>{const t=db.transaction('records',mode),store=t.objectStore('records');let value;
 t.oncomplete=()=>resolve(value);t.onerror=()=>reject(t.error||Error('Falha no histórico'));t.onabort=()=>reject(t.error||Error('Histórico abortado'));
 try{const result=fn(store,t);if(result&&typeof result.then==='function'){result.then(x=>{value=x;}).catch(e=>{try{t.abort();}catch(_){}reject(e);});}else value=result;}catch(e){try{t.abort();}catch(_){}reject(e);}
});}
const all=()=>tx('readonly',s=>request(s,'getAll'));
const get=id=>tx('readonly',s=>request(s,'get',id));
const put=record=>tx('readwrite',s=>{s.put(record);});
async function lock(fn){if(!navigator.locks?.request)throw Error('Navegador sem bloqueio exclusivo; operação protegida recusada');return navigator.locks.request('__MA_DEV61_SANDBOX__:ma5-write',{mode:'exclusive'},fn);}
async function captureOperation(raw,origin,session){const id='operation:'+crypto.randomUUID(),record={id,kind:'operation',createdAt:new Date().toISOString(),origin,session,key:LEDGER,raw,sha256:await sha(raw)};
 await put(record);const saved=await get(id);if(!saved||saved.raw!==raw||saved.sha256!==record.sha256)throw Error('Cópia de operação não pôde ser conferida');return record;
}
function localEntries(){const out=[];for(let i=0;i<ls.length;i++){const key=ls.key(i),raw=ls.getItem(key);out.push({key,raw});}return out.sort((a,b)=>a.key.localeCompare(b.key));}
async function history(){const result=[];
 for(const item of localEntries())if(item.key.startsWith(OP_PREFIX)||item.key===LEDGER+'-prev'||item.key.startsWith(LEDGER+'-rejeitados-')||item.key.startsWith(LEDGER+'-quarantine-review:')){
  result.push({id:item.key,storage:'localStorage',kind:item.key.startsWith(OP_PREFIX)?'operation':item.key.includes('rejeitados-')?'quarantine':item.key.includes('quarantine-review:')?'review':'previous',key:item.key,raw:item.raw,createdAt:null,origin:'Histórico anterior à A5; data não comprovada',sha256:await sha(item.raw)});
 }
 for(const r of await all())result.push({...r,storage:'indexedDB'});
 return result.sort((a,b)=>String(a.createdAt||'').localeCompare(String(b.createdAt||''))||a.id.localeCompare(b.id));
}
async function seal(payload){return {...payload,integrity:{algorithm:'SHA-256',digest:await sha(canonical(payload))}};}
async function unseal(value,format){if(!plain(value)||value.format!==format||value.version!==1||!plain(value.integrity)||value.integrity.algorithm!=='SHA-256')throw Error('Formato/versão/integridade não reconhecidos');
 const {integrity,...payload}=value;if(await sha(canonical(payload))!==integrity.digest)throw Error('SHA-256 do arquivo não confere');return payload;
}
function status(text,bad=false){const el=document.getElementById('ma5-storage-message');if(el){el.textContent=text;el.style.color=bad?'#8c3022':'#315c3d';}}
async function exportHistory(){return lock(async()=>{const records=await history();const file=await seal({format:'manfrin-arnez-protection-archive',version:1,createdAt:new Date().toISOString(),database:databaseName,records});
 const text=JSON.stringify(file,null,2);download('Manfrin-Arnez-HISTORICO-PROTECAO-A5-'+new Date().toISOString().slice(0,10)+'.json',text);status('Download do histórico solicitado. Selecione o arquivo baixado abaixo para conferir antes de liberar espaço. Não é backup completo do Dashboard.');return file;
});}
async function verifyArchive(file){const payload=await unseal(JSON.parse(await file.text()),'manfrin-arnez-protection-archive');if(payload.database!==databaseName||!Array.isArray(payload.records))throw Error('Histórico de outro ambiente ou lista inválida');
 const seen=new Set();for(const r of payload.records){if(!plain(r)||typeof r.id!=='string'||!['localStorage','indexedDB'].includes(r.storage)||typeof r.raw!=='string'&&r.kind==='operation'||seen.has(r.storage+':'+r.id))throw Error('Cópia inválida/duplicada');seen.add(r.storage+':'+r.id);if(r.kind==='operation'&&await sha(r.raw)!==r.sha256)throw Error('Cópia histórica corrompida');}
 A.verifiedArchive={file,payload,digest:await sha(await file.text())};status('Arquivo externo selecionado e verificado por SHA-256/conteúdo. Ele será relido antes de qualquer exclusão.');A.onArchiveVerified?.(payload);return payload;
}
async function deleteVerified(ids){return lock(async()=>{const proof=A.verifiedArchive;if(!proof)throw Error('Selecione e verifique a exportação externa primeiro');
 const text=await proof.file.text();if(await sha(text)!==proof.digest)throw Error('Arquivo externo mudou ou não está mais acessível');await unseal(JSON.parse(text),'manfrin-arnez-protection-archive');
 const records=await history(),selected=records.filter(r=>ids.includes(r.storage+':'+r.id));if(!selected.length||selected.length!==ids.length)throw Error('Seleção inexistente/duplicada');
 const operations=records.filter(r=>r.kind==='operation'),latest=operations.filter(r=>r.storage==='indexedDB').at(-1)||operations.at(-1);
 for(const r of selected){if(r.kind!=='operation')throw Error('Quarentenas, revisões, -prev e backups oficiais não podem ser removidos por esta limpeza');if(latest&&r.storage===latest.storage&&r.id===latest.id)throw Error('A cópia de operação mais recente é retida no navegador');
  const exported=proof.payload.records.find(x=>x.storage===r.storage&&x.id===r.id);
  if(!exported||exported.raw!==r.raw||exported.sha256!==await sha(r.raw))throw Error('Exportação não contém a cópia exata selecionada');
 }
 if(!confirm('LIBERAR ESPAÇO: excluir SOMENTE '+selected.length+' cópia(s) de operação selecionada(s)? O arquivo externo foi relido e contém os bytes exatos. Guarde esse arquivo fora do navegador. Quarentenas, revisões, -prev e a cópia mais recente ficam preservadas.'))return {cancelled:true};
 if(await sha(await proof.file.text())!==proof.digest)throw Error('Arquivo externo mudou ou deixou de estar acessível durante a confirmação');
 // Releitura final sob bloqueio exclusivo; a confirmação não autoriza outro conteúdo.
 for(const r of selected){const raw=r.storage==='localStorage'?ls.getItem(r.key):(await get(r.id))?.raw;if(raw!==r.raw)throw Error('Cópia mudou durante a confirmação; limpeza recusada');}
 const receiptRaw=canonical({version:1,createdAt:new Date().toISOString(),archiveName:proof.file.name,archiveDigest:proof.digest,entries:selected.map(r=>({id:r.id,storage:r.storage,key:r.key,sha256:r.sha256}))});
 const receipt={id:'cleanup:'+crypto.randomUUID(),kind:'cleanup',createdAt:new Date().toISOString(),origin:'Liberação expressamente autorizada com arquivo externo verificado',key:'external-protection-archive',raw:receiptRaw,sha256:await sha(receiptRaw)};
 const dbIds=selected.filter(r=>r.storage==='indexedDB').map(r=>r.id);await tx('readwrite',s=>{s.put(receipt);for(const id of dbIds)s.delete(id);});
 for(const r of selected.filter(r=>r.storage==='localStorage')){if(ls.getItem(r.key)!==r.raw)throw Error('Cópia local mudou; exclusão restante recusada');ls.removeItem(r.key);}
 status('Excluídas '+selected.length+' cópias de operação com exportação externa verificada. Nenhuma quarentena/revisão ou base ativa removida.');await refresh();return {deleted:selected.length};
});}
async function refresh(){const box=document.getElementById('ma5-history-list');if(!box)return;const entries=localEntries();let usage=entries.reduce((n,r)=>n+2*(r.key.length+r.raw.length),0);
 let records=[];try{records=await history();}catch(err){status('Histórico indisponível: '+err.message,true);}
 let estimate=null;try{estimate=await navigator.storage?.estimate?.();}catch(_){}
 const total=document.getElementById('ma5-storage-usage');total.textContent='localStorage DEV ≈ '+usage.toLocaleString('pt-BR')+' bytes (estimativa UTF-16, não é a cota exata). Histórico: '+records.length+' item(ns). '+(estimate?'Uso informado pela API da origem ≈ '+Number(estimate.usage||0).toLocaleString('pt-BR')+' / cota informada '+Number(estimate.quota||0).toLocaleString('pt-BR')+' bytes; a API pode não contabilizar o localStorage.':'Estimativa de cota da origem não disponível.');
 const bases=document.getElementById('ma5-storage-bases');bases.replaceChildren();for(const item of entries){const p=document.createElement('p');p.textContent=item.key+' · '+(2*item.raw.length).toLocaleString('pt-BR')+' bytes estimados';bases.append(p);}
 box.replaceChildren();for(const r of records){const item=document.createElement('label');item.style.cssText='display:block;padding:7px;border-bottom:1px solid #ddd;overflow-wrap:anywhere';const check=document.createElement('input');check.type='checkbox';check.style.width='auto';check.dataset.historyId=r.storage+':'+r.id;check.disabled=r.kind!=='operation';
  item.append(check,document.createTextNode(' '+r.kind+' · '+(r.createdAt||'sessão/data não comprovadas')+' · '+r.storage+' · '+r.id+' · '+(typeof r.raw==='string'?2*r.raw.length:enc.encode(JSON.stringify(r)).length)+' bytes · SHA-256 '+r.sha256));box.append(item);}
 return records;
}
function rawLedger(){const raw=ls.getItem(LEDGER);if(raw===null){status('Livro-caixa ausente: nenhum arquivo substitutivo gerado.',true);return;}download('Manfrin-Arnez-LIVRO-CAIXA-ORIGINAL-BRUTO-A5.json',raw);status('Livro-caixa bruto atual solicitado ao navegador, com os bytes originais. Não é backup completo.');}
function mount(){const backup=document.getElementById('backup');if(!backup)return;
 const raw=document.createElement('button');raw.type='button';raw.id='ma5-export-ledger-raw';raw.textContent='Baixar livro-caixa original BRUTO';raw.onclick=()=>{try{rawLedger();}catch(e){status(e.message,true);}};document.getElementById('ma62-export-care-raw').before(raw);
 const panel=document.createElement('article');panel.id='ma5-storage-panel';panel.className='panel sections';
 panel.innerHTML='<h2>Armazenamento e histórico de proteção</h2><p id="ma5-storage-usage"></p><p>Novas cópias de operações ficam em IndexedDB, separadas da cota pequena do localStorage. Nenhuma limpeza é automática. As cópias antigas permanecem onde estão. Guarde exportações externas; manter apenas dados no navegador não protege contra apagar o perfil.</p><button type="button" id="ma5-storage-refresh">Atualizar diagnóstico</button> <button type="button" id="ma5-history-export">Exportar histórico para guardar fora do navegador</button><label>Selecionar e verificar o arquivo exportado<input type="file" id="ma5-history-verify" accept=".json"></label><p id="ma5-storage-message" role="status"></p><details><summary>Tamanho das bases locais</summary><div id="ma5-storage-bases"></div></details><details><summary>Cópias históricas: selecionar para liberação segura</summary><div id="ma5-history-list"></div></details><button type="button" id="ma5-history-delete">Liberar somente cópias selecionadas e verificadas</button><p>Retenção: a cópia de operação mais recente fica no navegador; demais cópias só saem após reabrir a exportação íntegra e confirmar. Quarentenas, revisões, -prev e backups de restauração ficam protegidos nesta limpeza.</p>';
 backup.append(panel);document.getElementById('ma5-storage-refresh').onclick=()=>refresh().catch(e=>status(e.message,true));document.getElementById('ma5-history-export').onclick=()=>exportHistory().catch(e=>status('Exportação recusada: '+e.message,true));
 document.getElementById('ma5-history-verify').onchange=async e=>{try{if(e.target.files?.[0])await verifyArchive(e.target.files[0]);}catch(err){A.verifiedArchive=null;status('Verificação recusada: '+err.message,true);}finally{e.target.value='';}};
 document.getElementById('ma5-history-delete').onclick=()=>deleteVerified([...document.querySelectorAll('#ma5-history-list input:checked')].map(x=>x.dataset.historyId)).catch(e=>status('Limpeza recusada: '+e.message,true));
 const note=document.createElement('article');note.id='ma5-protection-info';note.className='panel';note.innerHTML='<h2>Proteção das operações</h2><p>Históricos íntegros são informação rotineira. Consulte data, tamanho, exportação e liberação seletiva em Backup e restauração.</p><p id="ma5-operation-status" role="status"></p>';document.getElementById('ledger').append(note);refresh().catch(e=>status(e.message,true));
}
Object.assign(A,{sha,canonical,seal,unseal,plain,download,ready,tx,all,get,put,lock,captureOperation,history,localEntries,refresh,exportHistory,verifyArchive,deleteVerified,rawLedger,status,mount});
})();
