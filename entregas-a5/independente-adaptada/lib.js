const { chromium } = require('playwright');
const path=require('path'),fs=require('fs'),crypto=require('crypto');
const DEV=process.env.DEV_URL;if(!DEV)throw Error('DEV_URL HTTP local obrigatório');
const BLANK=new URL('independente-adaptada/blank.html',DEV).href;
const PREFIX='__MA_DEV61_SANDBOX__:';
fs.writeFileSync(path.resolve(__dirname,'blank.html'),'<!doctype html><title>blank</title>');
const sha=s=>crypto.createHash('sha256').update(s).digest('hex').slice(0,12);
async function browser(){return chromium.launch({executablePath:process.env.CHROMIUM_BIN||'/usr/bin/chromium',headless:true,args:['--no-sandbox']});}
// abre o DEV; seed = {chaveLogica: texto} gravado COM prefixo (como o app enxerga); realSeed = {chaveReal: texto} gravado SEM prefixo (sentinelas)
async function openDev(b,{seed={},realSeed={},acceptDialogs=true,downloads=true}={}){
  const ctx=await b.newContext({acceptDownloads:downloads,viewport:{width:1280,height:900}});
  await ctx.route('**/*',r=>r.request().url().startsWith(new URL(DEV).origin)?r.continue():r.abort());await ctx.addInitScript(()=>{if(localStorage.getItem('__MA_DEV61_SANDBOX__:ma5-suppress-seeds-v1')===null){localStorage.setItem('__MA_DEV61_SANDBOX__:ma5-suppress-seeds-v1','1');localStorage.setItem('__MA_DEV61_SANDBOX__:ma-care-v2',JSON.stringify({version:2,patients:[],records:[],notes:[]}));localStorage.setItem('__MA_DEV61_SANDBOX__:ma-ledger-v1','[]');}});const page=await ctx.newPage(); const errors=[]; const dialogs=[];
  page.on('console',m=>{if(m.type()==='error')errors.push('console: '+m.text().slice(0,200))});
  page.on('pageerror',e=>errors.push('pageerror: '+e.message.slice(0,200)));
  page.on('dialog',d=>{dialogs.push(d.message().slice(0,120));acceptDialogs?d.accept():d.dismiss()});
  if(Object.keys(realSeed).length){await page.goto(BLANK);await page.evaluate(rs=>{for(const [k,v] of Object.entries(rs))localStorage.setItem(k,v)},realSeed);}
  await page.addInitScript(({seed,PREFIX})=>{try{if(!sessionStorage.getItem('__seeded')){sessionStorage.setItem('__seeded','1');for(const [k,v] of Object.entries(seed))localStorage.setItem(PREFIX+k,v);}}catch(e){}},{seed,PREFIX});
  const t0=Date.now(); await page.goto(DEV,{timeout:240000}); await page.waitForFunction(()=>window.MA_DEV_SANDBOX===true&&window.MA5?.appReady===true,null,{timeout:240000}); const loadMs=Date.now()-t0;
  return {ctx,page,errors,dialogs,loadMs};
}
// leitura do armazenamento REAL (sem isolamento) via iframe about:blank; devolve {chave:{len,hash}} e opcionalmente texto
async function rawStore(page,withText=false){
  return page.evaluate(async(withText)=>{const f=document.createElement('iframe');document.body.append(f);const ls=f.contentWindow.localStorage;const o={};
    for(let i=0;i<ls.length;i++){const k=ls.key(i),v=ls.getItem(k);o[k]={len:v.length,text:withText?v:undefined};}
    const enc=new TextEncoder();for(const k in o){const v=ls.getItem(k);const h=await crypto.subtle.digest('SHA-256',enc.encode(v));o[k].hash=[...new Uint8Array(h)].slice(0,6).map(x=>x.toString(16).padStart(2,'0')).join('');}
    f.remove();return o;},withText);
}
const appKey=(raw,k)=>raw[PREFIX+k]; // entrada gravada pelo app
const results=[];
function record(id,titulo,resultado,evidencia,extra={}){results.push({id,titulo,resultado,evidencia,...extra});console.log(`[${resultado}] ${id} ${titulo} :: ${evidencia}`)}
module.exports={browser,openDev,rawStore,appKey,record,results,PREFIX,sha,DEV,BLANK};
