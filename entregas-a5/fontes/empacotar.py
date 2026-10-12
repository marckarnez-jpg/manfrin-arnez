"""Pacote fictício auditável; não publica ou usa serviços externos."""
from pathlib import Path
import hashlib,json,zipfile,shutil
R=Path(__file__).resolve().parent.parent
OUT=R.parent/'pacote-a5-final';OUT.mkdir(exist_ok=True)
DEST=OUT/'Entrega-Manfrin-Arnez-A5-DEV4'
if DEST.exists():raise SystemExit('Use diretório de empacotamento vazio; não sobrescrever pacote anterior.')
DEST.mkdir()
# Incluir entregáveis e últimas evidências; diagnósticos preservados explicitamente em referencias.
files=[p for p in R.iterdir() if p.is_file() and (p.suffix in ['.md','.json','.diff','.py','.txt'] or p.name=='Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html' or p.name in ['testes-a5-definitivo.log','testes-fase1-definitivo.log','testes-sanitarios-definitivo.log','testes-fase1.log']) and not p.name.endswith('-diagnostico.log')]
for p in files:shutil.copyfile(p,DEST/p.name)
for name in ['fontes','referencias','evidencias-fase1','resultados-a5','independente-adaptada']:
 shutil.copytree(R/name,DEST/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc','falha.png','node_modules'))
# Evidência de download precisa acompanhar os prefixos preservados (mesmo diretório compartilhado).
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=''.join(f'{sha(p)}  {p.relative_to(DEST).as_posix()}\n' for p in sorted(DEST.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt')
(DEST/'SHA256SUMS.txt').write_text(manifest)
zipPath=OUT/'Entrega-Manfrin-Arnez-A5-DEV4.zip'
with zipfile.ZipFile(zipPath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(DEST.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(OUT))
with zipfile.ZipFile(zipPath) as z:
 assert z.testzip() is None
 for line in manifest.splitlines():
  digest,name=line.split('  ',1);assert hashlib.sha256(z.read(DEST.name+'/'+name)).hexdigest()==digest,name
receipt={'zip':zipPath.name,'bytes':zipPath.stat().st_size,'sha256':sha(zipPath),'html':json.loads((DEST/'Matriz-Testes-A5.json').read_text())['html_sha256'],'files':sum(p.is_file() for p in DEST.rglob('*')),'delivery':'Publicação em branch de desenvolvimento somente após confirmação expressa; sem deploy/main/site.'}
(OUT/'Comprovante-Pacote-A5.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2));print(json.dumps(receipt,ensure_ascii=False))
