from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent.parent;HTML=R/'Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html';SHA=hashlib.sha256(HTML.read_bytes()).hexdigest()
rows=[]
for name in ['resultados-fase1.json','resultados-a5/resultados.json']:
 d=json.loads((R/name).read_text());assert not d['failure'],(name,d['failure']);assert d['html_sha256']==SHA,(name,d['html_sha256'],SHA)
 for c in d['checks']:
  rows.append(dict(id=c['id'],status=c['status'],evidence=c.get('evidence',''),source=name,kind='auxiliar' if c['id'].startswith(('AUX-','JS-')) or c['id']=='METODO-FILE-OU-BLOQUEIO-DOCUMENTADO' else 'comportamento'))
assert json.loads((R/'independente-adaptada/execucao.json').read_text())['html_sha256']==SHA
for x in json.loads((R/'independente-adaptada/t5.json').read_text()):rows.append(dict(id=x['id'],status=x['resultado'],evidence=x['evidencia'],source='independente-adaptada/t5.json',kind='auxiliar' if x['id']=='SAN-13' else 'comportamento'))
assert all(x['status']=='APROVADO' for x in rows)
pending=[('FILE-MAC','file:// no Chrome/Mac do usuário; ambiente cloud bloqueou o protocolo'),('AUDITORIA-DEV4','Auditoria independente completa da DEV.4 pelo Claude'),('LEGADO-HTML61','Comparação no HTML 6.1 original não fornecido; somente fixtures v2 testadas'),('COTA-IDB-REAL','Esgotamento físico real de IndexedDB: proteção testada por falha simulada, sem consumir a origem até seu limite'),('REGRESSAO-253-ORIGINAIS','Reexecução integral dos 253 critérios originais: vários substituídos pelo A5; somente os críticos mapeados e SAN foram reexecutados')]
for id,evidence in pending:rows.append(dict(id=id,status='NAO_EXECUTADO',evidence=evidence,source='Riscos-Pendencias-A5.md',kind='pendencia'))
counts={k:sum(x['status']==k for x in rows) for k in ['APROVADO','REPROVADO','NAO_EXECUTADO']};behavior=sum(x['status']=='APROVADO' and x['kind']=='comportamento' for x in rows);aux=sum(x['status']=='APROVADO' and x['kind']=='auxiliar' for x in rows)
(R/'Matriz-Testes-A5.json').write_text(json.dumps(dict(html_sha256=SHA,counts=counts,approved_behavior=behavior,approved_auxiliary=aux,checks=rows),ensure_ascii=False,indent=2))
md=f'# Matriz executada — DEV.4 A5\n\nHTML SHA-256 `{SHA}`. {behavior} verificações de comportamento aprovadas na última execução de cada caso; {aux} verificações auxiliares aprovadas; {counts["REPROVADO"]} reprovadas; {len(pending)} não executadas. Sintaxe dos 26 scripts é verificação estática separada, não somada ao comportamento. Rodadas diagnósticas e resultados anteriores anexados não contam como aprovação desta DEV.4. Dois problemas do harness (atribuição de função e espera assíncrona da prévia) foram corrigidos; diagnósticos são preservados em referencias/. A matriz conta somente a rodada definitiva sobre o SHA entregue, sem somar rodadas anteriores.\n\n'
md+='| ID | Resultado | Classe | Evidência/origem |\n|---|---|---|---|\n'
for x in rows:
 ev=x['evidence'];ev=ev if isinstance(ev,str) else json.dumps(ev,ensure_ascii=False);ev=ev.replace('|','\\|').replace('\n',' ');md+=f'| {x["id"]} | {x["status"]} | {x["kind"]} | {(ev[:800] or "Ver asserção e execução")}; `{x["source"]}` |\n'
md+='\n## Critérios da auditoria reexecutados com a semântica A5\n\n| Referência | Evidência atual | Mudança de critério |\n|---|---|---|\n| N1 / AJ-14 / AJ-15 | N1-220-OPERACOES-500/1500, COTA, VOLUME, IDB-FALHA | Cópia verificável no IndexedDB, sem exigir chaves por operação no localStorage; cota real mantém originais |\n| N2 / AJ-11 | N2-BRUTO, V2-LEGADO, N2-V3 | Livro legível numérico incluído sem conversão; botão bruto independente da faixa |\n| N3 | N3-SEM-FAIXA-ROTINEIRA / RISCO-REAL | Históricos válidos são rotina; quarentena/falha continua risco |\n| AJ-11 / BKP-02 / B-100 | BKP02, BACKUP-ARQUIVO, HASH, PARCIAL | Novo v3 inclui bases e proteção; arquivo parcial explícito substitui recusa de toda exportação bruta |\n| AJ-12 / B-06 / B-79 | BKP02-LAB-CHECKLISTS-QUARENTENAS, QUARENTENA-CONFLITO, N1-QUARENTENA | Quarentenas/revisões passam a integrar o snapshot; revisão não significa recuperação |\n| P1-7b / A1-48 | P17B-PREIMAGE, A148, FALHA, INTERRUPCAO, RECUPERACAO | Preimage global e recuperação expressa; não só cópia financeira |\n| B-119 / B-123 | B119-V2, B123, V2-PARCIAL | Legado íntegro sem IDs/valores convertidos; reload não reinjeta seed |\n| P1-0 | P10-VERSAO-ACADEMIA-DESCONHECIDA | Versão desconhecida não pode sobrescrever raw |\n| Central Sanitária | SAN-01…SAN-13 | Critérios independentes mantidos; transporte/espera/fixtures documentados |\n\nEsse mapeamento não declara aprovação dos 253 casos originais. A4/merge e revisão clínica continuam fora da homologação. O caso METODO-FILE confirma o bloqueio documentado, não o funcionamento por file://.\n'
(R/'Matriz-Testes-A5.md').write_text(md)
report=f'''# Relatório — Manfrin Arnez 6.2 DEV.4 A5

Somente dados fictícios. Não pronta para uso clínico. Aguarda auditoria independente do Claude antes de qualquer implantação.

## Identificação

- Arquivo: `{HTML.name}`.
- Tamanho: {HTML.stat().st_size:,} bytes.
- SHA-256: `{SHA}`.
- Base DEV.3: `e4e4f49ca37e85cd9c83c67aa79b4e9d2fcb74b11137c387a5692ea8727bcc3f` — 4.077.003 bytes, preservada em referencias/.
- Site institucional: `4b6789de6fdae19e79eeddd310c5f9c680fe7758438b57a38987587f74f4d8e3`, preservado.
- Main remota observada: `d85b944d2fdb029e9b7afd57c6baa28938765330`; sem push, merge ou implantação desta etapa.
- Branch local de preparação: `dev/a5-dev4-local`.

## Resultado por prioridade

| Estado pedido | Escopo |
|---|---|
| ✓ CORRIGIDO E TESTADO | N1, N2, N3; backup unificado v3; leitura v2; prévia/confirmacao; preimage; rollback/interrupção; supressão de seeds; recuperação externa/estado anterior; testes e evidências listados na matriz |
| ⚠ CORRIGIDO, MAS PRECISA DE AUDITORIA | Arquitetura nova de inicialização, IndexedDB e coordenação; restauração transversal; nenhuma homologação independente da DEV.4 foi declarada |
| ✗ NÃO CORRIGIDO | Problemas fora de A5, inclusive A4/merge/visualização citados na auditoria, sem promessa de correção nesta etapa |
| ○ PENDENTE | file:// no Mac, auditoria Claude, HTML 6.1 original, cota física completa de IndexedDB e publicação externa após autorização |

## Ordem e implementação

A Fase 1 foi implementada e testada antes do motor de backup/restauração. O HTML intermediário comprovado tem SHA `34adf3a5409dc66cebef4b4196af875648f3f95996c288bbd33d7bef288ab997`, com 29 verificações sem falhas; fonte e resultados estão em referencias/. Estes 29 resultados anteriores não são contados novamente como testes finais.

Depois foi inventariado o armazenamento efetivo do código DEV, não presumido por nomes de telas. O v3 lê as chaves persistidas atuais e todos os registros do IndexedDB DEV, incluindo Academia e progressos ma58/59/60, dois checklists, taxas, mês, clínico, livro e proteções. PDFs fixos permanecem no HTML; rascunhos só entram quando realmente persistidos. Chaves desconhecidas/ilegíveis entram em bruto e tornam o snapshot PARCIAL. Ausências são declaradas sem fabricar pacientes, lançamentos ou configurações.

N1 desloca novas cópias de operação para IndexedDB com SHA e releitura antes da gravação financeira. Cópias antigas continuam preservadas. Diagnóstico e liberação seletiva exigem arquivo externo conferido e confirmação; uma cópia recente permanece. Quarentenas, revisões, preimages e comprovantes não são apagados automaticamente. Após limpeza autorizada, os estados retirados exigem arquivos externos identificados e o próximo snapshot é PARCIAL. N2 oferece bruto exato em Backup independentemente da faixa. N3 separa histórico rotineiro de risco ativo.

O backup v3 tem ID, versão, data, origem DEV, manifesto de inclusão/ausências/quarentenas/exportações separadas, SHA por base e SHA do envelope canônico. SHA é integridade, não assinatura de autoria. A mensagem distingue download solicitado de arquivo efetivamente selecionado/conferido. A rota da Contabilidade usa o mesmo exportador.

A importação v2 conserva os trechos JSON originais de care/ledger/rateSettings. IDs numéricos, bancos antigos, valores fracionários e campos adicionais legíveis não são convertidos. Formato v2 não possui hash original; validação estrutural é declarada. Formatos desconhecidos são recusados.

Restaurar requer prévia, contagens antes/arquivo, conflitos/duplicidades, bases ausentes mantidas e confirmação. Guarda preimage integral autocontida antes de qualquer substituição, usa marcador e reserva real conservadora de cota, verifica bytes gravados e guarda receipt. Em falha recupera os originais; em interrupção tenta recuperar antes de ativar módulos. Se não houver garantia, bloqueia gravações. Preimages podem ser recuperadas com nova proteção e confirmação. Bases antes ausentes são identificadas como remoção explícita no desfazer; proteções são retidas. Seeds embutidos não são reinjetados após restore/reload.

## Testes efetivamente executados

A matriz usa a última execução concluída de cada caso. Houve dois problemas de harness corrigidos: execução involuntária da função de injeção IDB pelo avaliador e ausência de espera da prévia assíncrona. Após corrigir o harness e o resumo visual de contagens para módulos mantidos, a suíte foi executada integralmente sobre o HTML final. Diagnósticos estão preservados, mas não são somados à matriz definitiva.

{behavior} verificações de comportamento e {aux} auxiliares aprovadas; {counts['REPROVADO']} reprovadas; {len(pending)} pendências não executadas explicitadas. As 26 verificações de sintaxe Node são separadas. Não foi declarada reexecução integral das 253 verificações históricas.

- Python 3.12.14; Playwright 1.62.0; Chromium 154.0.8037.57; Node 24.19.0, Linux cloud.
- Livros com 500 e 1.500 linhas: 220 operações sucessivas em cada tamanho, cópias exatas, limpeza externa verificada, retenção mínima e livro atual inalterado. Livros de 6.500 e 12.000 linhas: operações e backup com histórico exato.
- localStorage saturado de fato com fixtures; recusa antes dos dados; liberação de operações já exportadas, preservação de quarentenas/revisões e pagamento posterior. Quase cheio: falha real na reserva e rollback recuperável. Falha de proteção IndexedDB simulada sem alteração financeira.
- v3 integral byte a byte; arquivo baixado e verificado; adulteração recusada; bases inválidas/ausentes/opaques declaradas; v2, legado numérico/banco/valor, cancelamento, módulo ausente preservado.
- Falha no meio e recarga no estado intermediário: originais recuperados. Preimage confirmada, recuperação externa e recuperação do estado anterior incluindo ausência original.
- 18 telas, cadastro/pagamento/CSV, evoluções persistidas, simulador, Academia/Laboratório/Exocad PDF, checklist sanitário, duas abas, XSS e sentinelas fictícias fora do prefixo.
- SAN-01 a SAN-13 da suíte independente reexecutados pelo Codex, com critérios mantidos e adaptações documentadas. Isso não é nova auditoria do Claude.

`file://` foi tentado sem desativar a política do navegador, retornando `ERR_BLOCKED_BY_ADMINISTRATOR`. Comportamentos foram testados em HTTP 127.0.0.1 com origens descartáveis e tráfego externo bloqueado. A diferença importa: armazenamento é por origem, e disponibilidade de APIs em file:// pode variar. Não há migração implícita ou acesso a perfil principal. File:// no Mac continua pendente.

## Entrega e recuperação

Leia `Politica-Retencao-Recuperacao-A5.md`, `Inventario-Bases-A5.json`, `Riscos-Pendencias-A5.md`, `Matriz-Testes-A5.md` e o comparativo. Suítes e JSONs de evidência estão no pacote. `SHA256SUMS.txt` confere cada arquivo, e o hash do ZIP é externo ao ZIP.

Limites: memória e cota não são ilimitadas; IndexedDB pode ser perdido junto com a origem; preimages/comprovantes crescem sem limpeza automática; outras versões/console não participam dos locks; falha persistente de recuperação exige manter bloqueio. Documentos externos e campos não salvos ficam fora. Não há produção, instalação ou alteração da main/site.

A ferramenta desta sessão não permite anexar ZIP de saída na conversa. Para download externo, está preparada uma entrega em branch de desenvolvimento, sem push até confirmação expressa exigida pelo comando do usuário. Após autorização, publicar somente essa branch e fornecer URL direta do ZIP; não apresentar caminho interno como anexo baixável.
'''
(R/'Relatorio-Manfrin-Arnez-6.2-DEV-04-A5.md').write_text(report);print(json.dumps(dict(counts=counts,behavior=behavior,auxiliary=aux,sha=SHA),ensure_ascii=False))
