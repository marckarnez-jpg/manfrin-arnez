# Relatório — Manfrin Arnez 6.2 DEV.4 A5

Somente dados fictícios. Não pronta para uso clínico. Aguarda auditoria independente do Claude antes de qualquer implantação.

## Identificação

- Arquivo: `Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html`.
- Tamanho: 4,128,851 bytes.
- SHA-256: `cc1da21a717db0e2f2bd7303284a3fd0b3af4c14be8638abb71741bfddc5fcbb`.
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

108 verificações de comportamento e 46 auxiliares aprovadas; 0 reprovadas; 5 pendências não executadas explicitadas. As 26 verificações de sintaxe Node são separadas. Não foi declarada reexecução integral das 253 verificações históricas.

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
