// T5: Central de Controle Sanitário
const L=require('./lib');const fs=require('fs');
const read=(p,k)=>p.evaluate(k=>localStorage.getItem(k),k);
const K='ma61-sanitary-checklist-v1';
const counts=p=>p.evaluate(()=>({fr:document.getElementById('ma61-front-total').textContent,cap:document.getElementById('ma61-front-caption').textContent,ok:+document.getElementById('ma61-ok').textContent,warn:+document.getElementById('ma61-warn').textContent,bad:+document.getElementById('ma61-bad').textContent,groups:document.querySelectorAll('#ma61-groups details.ma61-group').length,items:document.querySelectorAll('#ma61-groups article.ma61-item').length,perGroup:[...document.querySelectorAll('#ma61-groups details.ma61-group')].map(d=>d.querySelectorAll('article.ma61-item').length),lights:[...document.querySelectorAll('#ma61-groups .ma61-light')].map(x=>x.textContent.replace(/[^A-ZÁÉÍ]/g,''))}));
const setTone=(p,gid,idx,tone,evid)=>p.evaluate(([gid,idx,tone,evid])=>{const art=document.querySelectorAll(`#ma61-groups details.ma61-group[data-id="${gid}"] article.ma61-item`)[idx];if(evid){const ta=art.querySelector('textarea[data-field="evidence"]');ta.value=evid;}const s=art.querySelector('select');s.value=tone;s.dispatchEvent(new Event('change',{bubbles:true}));return document.getElementById('ma61-message').textContent},[gid,idx,tone,evid]);
(async()=>{const b=await L.browser();
 const r=await L.openDev(b);const p=r.page;
 await p.evaluate(()=>go('ma61-sanitary'));
 const c0=await counts(p);
 L.record('SAN-01','8 frentes e 42 subtópicos renderizados',(c0.groups===8&&c0.items===42&&c0.fr==='8'&&c0.cap.startsWith('42')&&c0.perGroup.join()==='6,5,6,7,4,5,4,5')?'APROVADO':'REPROVADO',`grupos=${c0.groups}; subtópicos=${c0.items}; por frente=${c0.perGroup.join('+')}; painel="${c0.fr} frentes / ${c0.cap}"`);
 L.record('SAN-02','Contadores do semáforo somam 42 e coincidem com a lista',(c0.ok+c0.warn+c0.bad===42)?'APROVADO':'REPROVADO',`verde=${c0.ok} amarelo=${c0.warn} vermelho=${c0.bad}; luzes das frentes=${c0.lights.join(',')}`);
 // domínio: contagem real de itens por cor no DOM
 const dom=await p.evaluate(()=>{const o={ok:0,warn:0,bad:0};document.querySelectorAll('#ma61-groups article.ma61-item').forEach(a=>o[a.dataset.tone]++);return o});
 L.record('SAN-03','Cor de cada subtópico no DOM = contadores',(dom.ok===c0.ok&&dom.warn===c0.warn&&dom.bad===c0.bad)?'APROVADO':'REPROVADO',`DOM ${JSON.stringify(dom)} vs painel ${c0.ok}/${c0.warn}/${c0.bad}`);
 // regra: verde exige evidência
 const gid='ster';
 const m1=await setTone(p,gid,3,'ok','');
 const t1=await p.evaluate(gid=>document.querySelectorAll(`details.ma61-group[data-id="${gid}"] article.ma61-item`)[3].dataset.tone,gid);
 L.record('SAN-04','Marcar VERDE sem evidência é bloqueado',(t1!=='ok'&&/evid/i.test(m1))?'APROVADO':'REPROVADO',`mensagem="${m1.slice(0,80)}"; cor do item=${t1}`);
 // lógica do semáforo da frente: tudo verde -> VERDE ; qualquer vermelho -> VERMELHO ; senão AMARELO
 for(let i=0;i<7;i++)await setTone(p,gid,i,'ok','Evidencia ficticia '+i);
 let c=await counts(p);const idx=['docs','room1','room2','ster','waste','maintenance','people','system'].indexOf(gid);
 const l1=c.lights[idx];
 await setTone(p,gid,2,'bad','');c=await counts(p);const l2=c.lights[idx];
 await setTone(p,gid,2,'warn','');c=await counts(p);const l3=c.lights[idx];
 L.record('SAN-05','Semáforo da frente: todos verdes→VERDE; um vermelho→VERMELHO; sem vermelho e nem todos verdes→AMARELO',(l1==='VERDE'&&l2==='VERMELHO'&&l3==='AMARELO')?'APROVADO':'REPROVADO',`sequência observada: ${l1} → ${l2} → ${l3}`);
 // persistência e recarga
 const stBefore=await read(p,K);const cB=await counts(p);
 await p.reload();await p.waitForFunction(()=>window.MA_DEV_SANDBOX===true&&window.MA5?.appReady===true,null,{timeout:120000});
 await p.evaluate(()=>go('ma61-sanitary'));const cA=await counts(p);
 L.record('SAN-06','Estados, evidências e luzes persistem após recarregar a página',(cA.ok===cB.ok&&cA.warn===cB.warn&&cA.bad===cB.bad&&(await read(p,K))===stBefore)?'APROVADO':'REPROVADO',`antes ${cB.ok}/${cB.warn}/${cB.bad} → depois ${cA.ok}/${cA.warn}/${cA.bad}; JSON idêntico=${(await read(p,K))===stBefore}`);
 // filtros
 await p.selectOption('#ma61-filter','bad');const fb=await counts(p);
 await p.selectOption('#ma61-filter','all');await p.selectOption('#ma61-group','waste');const fg=await counts(p);
 await p.selectOption('#ma61-group','all');await p.fill('#ma61-search','autoclave');const fs_=await counts(p);await p.fill('#ma61-search','');
 L.record('SAN-07','Filtros por semáforo, frente e busca',(fb.items===cA.bad&&fg.items===4&&fs_.items>0&&fs_.items<42)?'APROVADO':'REPROVADO',`filtro vermelho=${fb.items} (esperado ${cA.bad}); frente PGRSS=${fg.items} (esperado 4); busca "autoclave"=${fs_.items}`);
 // exportação
 const [dl]=await Promise.all([p.waitForEvent('download'),p.click('#ma61-export')]);await dl.saveAs('san_export.json');
 const ex=JSON.parse(fs.readFileSync('san_export.json','utf8'));
 L.record('SAN-08','Exportação do checklist (formato, versão, dados)',(ex.format==='manfrin-arnez-sanitary-checklist'&&ex.version===1&&ex.data&&ex.data.version===1&&Object.keys(ex.data.states).length>=7)?'APROVADO':'REPROVADO',`format=${ex.format} version=${ex.version}; estados exportados=${Object.keys(ex.data.states).length}; arquivo=${dl.suggestedFilename()}`);
 // importação ida-e-volta
 await setTone(p,'docs',0,'bad','');const mid=await read(p,K);
 await p.setInputFiles('#ma61-import','san_export.json');await p.waitForTimeout(700);
 const after=await read(p,K);
 L.record('SAN-09','Importação restaura exatamente o estado exportado (ida e volta)',(JSON.parse(after).states['docs-visa']===ex.data.states['docs-visa'])&&JSON.stringify(JSON.parse(after).states)===JSON.stringify(ex.data.states)?'APROVADO':'REPROVADO',`estado do item alterado antes de importar=${JSON.parse(mid).states['docs-visa']}; após importar=${JSON.parse(after).states['docs-visa']??'(padrão)'}; estados iguais ao exportado=${JSON.stringify(JSON.parse(after).states)===JSON.stringify(ex.data.states)}`);
 // importações inválidas
 const base=await read(p,K);const bad=[
  ['formato errado',{format:'outro',version:1,data:ex.data}],
  ['semáforo inválido',{format:'manfrin-arnez-sanitary-checklist',version:1,data:{version:1,states:{'docs-visa':'vermelho'}}}],
  ['id inexistente',{format:'manfrin-arnez-sanitary-checklist',version:1,data:{version:1,states:{'zzz-nope':'ok'}}}],
  ['__proto__',JSON.parse('{"format":"manfrin-arnez-sanitary-checklist","version":1,"data":{"version":1,"states":{"__proto__":"ok"}}}')],
  ['versão 2',{format:'manfrin-arnez-sanitary-checklist',version:2,data:{version:2,states:{}}}],
  ['grande >400KB',{format:'manfrin-arnez-sanitary-checklist',version:1,data:{version:1,states:{},notes:{'docs-visa':'x'.repeat(450000)}}}]];
 let rej=[];
 for(const [n,pl] of bad){fs.writeFileSync('imp_bad.json',JSON.stringify(pl));await p.setInputFiles('#ma61-import','imp_bad.json');await p.waitForTimeout(400);const same=(await read(p,K))===base;rej.push(n+':'+(same?'rejeitado':'ALTEROU'))}
 L.record('SAN-10','Importação rejeita arquivos inválidos sem alterar os dados',rej.every(x=>x.endsWith('rejeitado'))?'APROVADO':'REPROVADO',rej.join('; ')+`; poluição de protótipo: ({}).ok=${await p.evaluate(()=>({}).ok)}`);
 // XSS
 const xss='<img src=x onerror="window.__xss=1"><script>window.__xss=2<\/script>';
 await p.evaluate(x=>{go('ma61-sanitary');const art=document.querySelector('#ma61-groups article.ma61-item');const ta=art.querySelector('textarea[data-field="notes"]');ta.value=x;ta.dispatchEvent(new Event('change',{bubbles:true}));const ev=art.querySelector('textarea[data-field="evidence"]');ev.value=x;ev.dispatchEvent(new Event('change',{bubbles:true}));const w=art.querySelector('input[data-field="responsible"]');w.value=x;w.dispatchEvent(new Event('change',{bubbles:true}))},xss);
 await p.reload();await p.waitForFunction(()=>window.MA_DEV_SANDBOX===true&&window.MA5?.appReady===true,null,{timeout:120000});
 await p.evaluate(()=>go('ma61-sanitary'));await p.fill('#ma61-search','img src');await p.waitForTimeout(300);
 const xr=await p.evaluate(()=>({flag:window.__xss,imgs:document.querySelectorAll('#ma61-groups img').length,scripts:document.querySelectorAll('#ma61-groups script').length,shown:document.querySelectorAll('#ma61-groups article').length}));
 L.record('SAN-11','Texto com HTML/script em evidência, observação e responsável não executa (XSS armazenado)',(!xr.flag&&!xr.imgs&&!xr.scripts)?'APROVADO':'REPROVADO',`window.__xss=${xr.flag}; <img> injetadas=${xr.imgs}; <script> injetados=${xr.scripts}; item encontrado pela busca=${xr.shown}`);
 // links externos
 const links=await p.evaluate(()=>[...document.querySelectorAll('#ma61-sanitary a[href]')].map(a=>({rel:a.rel,t:a.target,ok:a.rel.includes('noopener')})));
 L.record('SAN-12','Links externos da Central usam noopener/noreferrer',links.every(l=>l.t!=='_blank'||l.ok)?'APROVADO':'REPROVADO',`links=${links.length}`);
 L.record('SAN-13','Console sem erros durante uso do checklist',r.errors.length===0?'APROVADO':'REPROVADO',`erros=${r.errors.length} ${r.errors.slice(0,2).join('|')}`);
 fs.writeFileSync('t5.json',JSON.stringify(L.results,null,1));await b.close();})().catch(e=>{console.log('ERR',e.stack);fs.writeFileSync('t5.json',JSON.stringify(L.results,null,1));process.exit(1)});
