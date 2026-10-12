from pathlib import Path
import re,subprocess,tempfile,hashlib,json,difflib
r=Path(__file__).resolve().parent.parent
old=(r/'referencias/Manfrin-Arnez-Dashboard-6.2-DEV-03-A1.2.html').read_text();new=(r/'Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html').read_text()
extract=lambda s:re.findall(r'<script([^>]*)>(.*?)</script>',s,re.S)
checks=[]
with tempfile.TemporaryDirectory() as t:
 for i,(attrs,code) in enumerate(extract(new)):
  p=Path(t)/f'{i}.js';p.write_text(code);result=subprocess.run(['node','--check',str(p)],capture_output=True,text=True);checks.append({'script':i,'attributes':attrs,'status':'APROVADO' if result.returncode==0 else 'REPROVADO','message':result.stderr});assert result.returncode==0,result.stderr
oldScripts=extract(old);newScripts=[(a,c) for a,c in extract(new) if not any(f'id="{x}"' in a for x in ['ma5-protection','ma5-backup-engine','ma5-bootstrap'])];assert len(oldScripts)==len(newScripts)
comparison=[];diff=[]
def abbreviate(line):
 if len(line)>1200:return line[:120]+' … [linha longa: '+str(len(line))+' caracteres; SHA-256 '+hashlib.sha256(line.encode()).hexdigest()+']\n'
 return line
for i,((a,c),(aa,cc)) in enumerate(zip(oldScripts,newScripts)):
 comparison.append({'original_script':i,'attributes_original':a,'attributes_dev4':aa,'original_sha256':hashlib.sha256(c.encode()).hexdigest(),'dev4_sha256':hashlib.sha256(cc.encode()).hexdigest(),'changed':c!=cc})
 if c!=cc:diff.extend(difflib.unified_diff([abbreviate(x) for x in c.splitlines(True)],[abbreviate(x) for x in cc.splitlines(True)],fromfile=f'DEV3-script-{i}',tofile=f'DEV4-script-{i}',n=2))
assets=lambda s:[hashlib.sha256(x.encode()).hexdigest() for x in re.findall(r'(JVBER[A-Za-z0-9+/=]+)',s)]
assert len(assets(old))>0 and assets(old)==assets(new)
(r/'Comparativo-Scripts-DEV3-DEV4.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2));(r/'Comparativo-Scripts-DEV3-DEV4.diff').write_text('Linhas >1200 caracteres abreviadas com SHA; originais completos em referencias/. Novos componentes separados em fontes/.\n'+''.join(diff));(r/'Verificacao-Estatica-A5.json').write_text(json.dumps({'syntax_checks':checks,'script_count':len(checks),'original_count':len(oldScripts),'pdf_assets_unchanged':assets(old)==assets(new),'pdf_count':len(assets(new))},ensure_ascii=False,indent=2));print({'scripts':len(checks),'original_scripts':len(oldScripts),'changed':sum(x['changed'] for x in comparison),'pdfs':len(assets(new))})
