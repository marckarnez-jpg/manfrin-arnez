# A. Diagnóstico técnico A4 — Dashboard Manfrin Arnez 6.2

**Etapa exclusivamente de diagnóstico e planejamento. Nenhuma correção, nova versão HTML, importação, navegador, commit, merge, deploy ou publicação foi executada.** A DEV.4 permanece em auditoria independente pelo Claude. Este documento não substitui essa auditoria e não homologa uso clínico.

## Conclusão principal

**✗ O núcleo histórico A4 continua presente:** a mesclagem grava no armazenamento, mas não reidrata o modelo do livro nem todas as telas. O handler `ma53-merge-file` da DEV.4 é **byte a byte idêntico** ao da DEV.3; a comparação tem SHA-256 `a5912c717fab0246316d76232002e60df1caa937aaf79fe81e435d42c0ed8d87`.

**✗ Há uma lacuna estrutural de segurança no fluxo de merge:** ele não utiliza o mutex, a preimage global e o journal de restauração A5. Além da desatualização do livro, contorna a comparação clínica adicionada na A5. Portanto, a primeira correção proposta deve garantir consistência e recuperação da mesclagem; um refresh isolado pode esconder uma divergência ou legitimar um cache antigo.

**⚠ Os cenários adicionais de perda/duplicação foram inferidos pela leitura do código.** Não foram reproduzidos aqui. Há dez registros analíticos novos, um de prioridade CRÍTICA, sete ALTAS e dois MÉDIOS, detalhados no catálogo e na matriz B. Esses registros não são dez defeitos originalmente atribuídos ao Claude.

## Método, fontes e limites

✓ Confirmado: análise estática dos relatórios A1.1 rodada 2, A1.2/DEV.3, relatório técnico DEV.3, código completo DEV.3/DEV.4, componentes A5, matriz final A5 e roteiro independente A1-44/45/46/B-120. Foram consultados os pontos de escrita, modelos em memória, eventos e inicialização das 18 telas. Não foram executados os roteiros antigos, que incluem operações incompatíveis com esta etapa somente de leitura.

| Fonte | Identificação |
|---|---|
| DEV.4 A5 entregue | Commit `206bd06f24db985fbc9ecb92ed2eea7a270b5f01`; HTML SHA `cc1da21a717db0e2f2bd7303284a3fd0b3af4c14be8638abb71741bfddc5fcbb` |
| ZIP DEV.4 | SHA `b34f349d079d450c7aa1661e2d9ce63a29fb9cc87ed2b65f4aeb291717735b97` |
| DEV.3 original | SHA `e4e4f49ca37e85cd9c83c67aa79b4e9d2fcb74b11137c387a5692ea8727bcc3f` |
| Auditoria A1.1/DEV.2 rodada 2 | Anexo fornecido anteriormente; AJ-18, seção de comparação e matriz |
| Auditoria A1.2/DEV.3 | `entregas-a5/referencias/Auditoria-Independente-A1.2-6.2-dev.3.md` |
| Relatórios Codex DEV.3 e DEV.4 | Limitam explicitamente a cobertura de merge e concorrência; não são nova auditoria independente |

`Fontes-e-Verificacao.json` registra caminhos, bytes, hashes e estado Git. Os números de linha abaixo são do **HTML DEV.4 entregue**, não dos relatórios antigos. A fonte completa permanece no arquivo existente em `/workspace/manfrin-arnez/entregas-a5/Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html`. Nenhuma cópia HTML nova foi criada nesta etapa.

Símbolos: **✓ Confirmado** = evidência documental/estrutural ou proteção observável no código; **✗ Problema identificado** = lacuna ou comportamento incorreto no caminho analisado; **⚠ Necessita revisão** = cenário funcional ou política ainda não validado independentemente; **○ Pendente** = teste/decisão/implementação futura. Confirmar código não equivale a testar uma correção.

## Inventário histórico preservando os IDs

| ID original | Evidência histórica | Situação na DEV.4 por leitura | Classificação |
|---|---|---|---|
| **P0-3** | Família de mesclagem inicialmente apagada por gravação posterior; passou a ficar preservada pelo bloqueio | Bloqueio do livro continua, mas modelo/tela não recebem o resultado; merge em si permanece sem proteção global | A4 principal; separar a proteção do próximo lançamento da segurança da própria mesclagem |
| **A1-45** | REPROVADO em A1.1 e A1.2: tela não mostra merge sem recarga | ✗ Handler conserva atualização incompleta | A4 confirmado por código inalterado |
| **B-120** | APROVADO para entrada do legado; observação explícita de tela atrasada | ✗ Não fornece aprovação visual. O merge não chama renderLedger/releitura | A4; manter resultado histórico do teste, não reclassificá-lo como falha retroativa |
| **B-121** | APROVADO: legado aparece depois de recarregar | ✓ Comportamento de leitura/legado é proteção a preservar; não é atualização imediata | Regressão A4/legado |
| **AJ-8** | Referência textual em A1-45 da auditoria A1.1, apontando correção A4 | ○ Não há nova aprovação. Não foi encontrado um item autônomo AJ-8 nessas tabelas | Alias textual, não inventar descrição histórica adicional |
| **AJ-18** | Item misto: A1-45, A1-48, B-101, B-102 | ✗ A1-45 persiste; demais filhos têm escopos/status distintos abaixo | Referência transversal A4/A5, não um único bug |
| **A1-44** | APROVADO: próxima gravação antiga não apaga a mesclagem | ✓ Livro compara raw antes/depois da cópia protegida. Não desativar o bloqueio para permitir salvar cache antigo | Regressão obrigatória, não pendência a “corrigir” |
| **A1-46** | APROVADO após sonda corrigida: recarga classifica linha inválida em quarentena | ✓ Leitura/quarentena existem. ○ Revalidar quando houver reidratação sem recarga | Regressão obrigatória; respeitar erro de temporização antigo |
| **B-101** | Falhou na DEV.2; passou na DEV.3 com aviso de CSV parcial | ✓ Aviso continua no exportador, linha 682 | Exportação/UI, já mitigado; não reincluir como defeito A4 aberto |
| **B-102**, **C-92/C-93/C-94** | Passaram na DEV.3 por aviso de omissão e preservação de quarentena | ✓ Aviso existe no merge. ✗ Snapshot continua específico v2 e não é journal A5 | Critério histórico de aviso atendido; nova lacuna de preimage do merge separada |

Referências verificáveis: auditoria A1.1 linhas 88, 112–117, 274–276, 303–304, 371–372; auditoria A1.2 linhas 63–69, 213–215, 345–346, 447–449. IDs compostos/aliases acima não são somados como defeitos independentes.

## A4 relacionado, mas não originalmente classificado como A4 exclusivo

| ID | Escopo correto | Efeito da A5 e necessidade atual |
|---|---|---|
| **P1-3** | Concorrência transversal; relatório anterior também o relaciona a outras frentes | Comparações de estado adicionadas a clínico, Academia e Sanitária; livro tem mutex. Não há sincronização visual universal nem mutex em todos os escritores. ○ Auditoria/novos testes por módulo |
| **P0-4 / PERF-01** | Desempenho transversal da carga e mergeCodental | Algoritmo de filtros repetidos permanece. Supressão de seeds evita uma rota, mas syncInfo ainda simula o merge. ○ Não atribuir os tempos antigos à DEV.4 |
| **A1-40/41/42/43 / C-46** | Proteção do livro entre abas | ✓ Manter as garantias de recusa e comparação; atualizações visuais não podem mascarar conflitos |
| **A1-56/57** | Falha de cota e coerência visual do livro | ✓ Regressões a manter. Comportamentos equivalentes de outros módulos não foram automaticamente cobertos |

## Outros módulos: não absorver silenciosamente na A4

- **A1-48 / P1-7b / BKP-02 / B-119 / B-123**, **N-1/N-2/N-3**: foco da A5. O Codex registrou correções/testes, mas a auditoria independente DEV.4 está pendente. Leitura do novo engine mostra prévia, proteção global, legado, suppress-seeds e histórico IDB. Não declarar homologação pelo Claude nesta análise.
- **P1-0 / MA61-1/MA61-1b**: versões desconhecidas e preservação em Academia/Sanitária; A5 acrescentou guardas. Revisão pertence ao contrato de dados desses módulos e à auditoria A5, não é simples refresh.
- **P2-2**: neutralização de fórmulas no CSV do livro, ainda sem `safeCell` no exportador de linha 682. Segurança de exportação, não A4 visual; tratar separadamente. O CSV clínico possui função de neutralização própria, portanto não generalizar o problema a todos os CSVs.
- **BKP-08**: exportação do estúdio sem leitor específico correspondente; cobertura unificada dos subcampos em A5 não cria automaticamente um importador individual. Integração de backup/módulo, distinto da reidratação D-A4-08.
- **P1-6 / SEC-01 / ISO-05**: contexto seguro, APIs e isolamento por origem. Não resolver em A4 removendo exigências de Web Locks ou alterando o namespace DEV.
- Auditoria de conteúdo clínico, instalação, migração real e produção permanecem fora desta etapa.

## Fluxo atual e causas

### Mesclagem de backup — linhas 856–907

1. Aguarda a leitura do arquivo, confere apenas o format antigo e valida care.
2. Clona `db` da sessão; adiciona pacientes, pagamentos e notas por ID.
3. Lê o livro persistido e adiciona linhas por ID textual; validação financeira é incompleta.
4. Pede confirmação. Outra página pode ter editado as bases enquanto o usuário confirma.
5. Lê `oldCare`, mas o JSON ANTES-MESCLAR usa **`care:db`**. Pode ser o cache antigo, não o estado persistido que está prestes a ser substituído.
6. Grava care, ledger e eventualmente taxas, fora do mutex/journal A5. Em falha tenta desfazer as três chaves, engolindo erros do rollback. Não há recuperação desse merge no próximo boot.
7. Faz `db=next` e renderAccount/storageStatus, deixando `rows`, `ma62LedgerRaw`, `ma5CareExpected` e outras projeções sem a transição correspondente.

Exemplo exclusivamente fictício proposto para teste: A e B abrem uma base com F1. A grava F2; B mescla F3 usando seu cache F1. O merge de B não chama `persist(next)` e pode gravar F1+F3, substituindo F1+F2. O snapshot de B pode conter somente F1. **⚠ Esse exemplo não foi executado; descreve o caminho de risco a testar, não perda já constatada.**

A comparação clínica é feita em `persist(next)` (726–730), mas o merge escreve em 890 sem chamá-la. A comparação do livro acontece em sua gravação ordinária (595–603), por isso ela evita a gravação posterior do livro antigo. As duas observações são compatíveis: o livro pode bloquear uma perda posterior, enquanto outro escritor ainda contorna a proteção clínica.

### Sincronização Codental — linhas 684–689 e 909–910

É outro fluxo, não o merge de backup. Usa `persist(result.db)`, portanto tem a comparação clínica A5. Também preserva pagamentos/notas ao clonar a base. Porém o confronto entre campos depende de source e de heurísticas de identidade, e a função procura por filtros repetidos. Essas políticas necessitam revisão, sem apagar salvaguardas existentes de ambiguidades e campos vazios.

### Projeções e módulos

| Base real | Modelos / projeções | Pontos de atenção |
|---|---|---|
| ma-care-v2 | db, activePatient, notePatient, pesquisas, relação contábil, notas | Reidratar só depois de commit; preservar rascunhos e snapshots históricos |
| ma-ledger-v1 | rows, raw esperado, métricas, conciliação, exportação | Não atualizar raw esperado sozinho; reler/classificar e manter rejeitados/quarentenas |
| ma-installment-rates-v1 | ma53Rates, Finance.observations, campos ma57/m55 | Escritores distintos; falha pode recalcular memória; preservar taxa manual versus automática |
| ma-academy-v55 | data do pai e state de ma58/59/60 | Importação do pai não recarrega estados dos filhos; mesmo namespace/mesma base |
| ma56-project-checklist-v1 | stored, contadores, filtros | Sem comparação/mutex comum; rollback local de seleção existe, não coordenação de abas |
| ma61-sanitary-checklist-v1 | state, contadores, listas/evidências | Comparação existe; state muda antes da gravação, erro não desfaz sempre a edição em memória |
| ma-account-month-last-v1 | preferência de mês | Merge força outubro/2026 quando detecta registros desse mês; não representa necessariamente a escolha do usuário |
| IndexedDB ma5-protection-v1 | registros operation/restore/cleanup | Histórico A5, não uma nova base clínica ou mecanismo universal de sincronização |

## Comportamentos intencionais que não são bugs A4

- Pagamentos usam `snapshot` cadastral: a mensagem de edição explica que o histórico conserva os dados da época. Renomear o paciente não deve reescrever pagamentos antigos automaticamente.
- Contabilidade clínica e conciliação bancária representam conjuntos diferentes. Atualização coerente não significa copiar recebimentos automaticamente para o livro ou somar os dois como se fossem registros distintos de receita.
- Campos ausentes e módulos ausentes no backup não devem ser preenchidos com seed ou dados inventados para “corrigir” a tela.
- Cópias/quarentenas válidas são proteção; arquivar revisão não recupera o lançamento. Uma UI mais limpa não autoriza ocultar riscos ativos.
- A recusa de gravação em estado desatualizado é uma proteção. A correção é reidratar com revisão coerente e consentimento para rascunhos, não desativar o bloqueio.

## Entregáveis e estado

✓ Diagnóstico documental/estático concluído; catálogo novo e rastreabilidade histórica separados. **✗ Lacunas identificadas não corrigidas. ⚠ Políticas de identidade/concorrência/desempenho exigem revisão. ○ Todos os 43 testes propostos estão pendentes de execução e as alterações dependem de auditoria/autorização.**

B: matriz de riscos; C: propostas por problema e contrato de arquitetura; D: testes/regressões; E: decisões condicionadas à auditoria; F: sequência recomendada. Não publicar estes documentos ou modificar a cópia auditada sem autorização futura.

## Mapa das 18 telas e atualização necessária

| Tela | Relação com dados | Avaliação por leitura |
|---|---|---|
| ma56-home | Navegação/atalhos e avisos | Rota interna precisa manter página/grupo/rótulo móvel coerentes; sem inventar indicadores persistidos |
| dash | Métricas financeiras derivadas do livro | Recalcular quando rows confirmado mudar, respeitando filtro |
| quick | Paciente selecionado, lançamento clínico | Preservar formulário; escolha/label e revisão clínica coerentes |
| accounting | db.records, snapshots e mês | Merge chama renderAccount, mas outros caches permanecem; histórico cadastral intencional |
| ma55-cost | Configuração, materiais e taxas | Distinguir cálculo volátil de análise salva; preservar taxa manual |
| sim | ma53Rates/Finance.observations | Modelo pode mudar após falha de gravação; há sincronização localizada ma57, não geral |
| ledger | rows/raw esperado/classificação | Núcleo A1-45: merge não reidrata nem renderiza |
| ma55-contador | Leitura de care e cálculo de estimativas | getCareRecords lê localStorage ao calcular; não assumir o mesmo cache db do clínico. Verificar disparo de render ao entrar |
| sources | Referências fixas e exemplos financeiros | Não precisa reescrever dados por evento; manter rótulos de origem/exemplo |
| patients | Busca/formulário em db | Nova consulta já usa db atualizado; lista/seleção existente necessita tratamento de invalidação |
| notes | db.notes e formulários/geradores voláteis | Não apagar preenchimento clínico não salvo nem afirmar que o gerador já foi persistido |
| tcle | Texto/formulário documental | Preservar preenchimento; não adicionar persistência ou importar pacientes implicitamente |
| ma55-academy | data/checks e filhos ma58/59/60 | Importação do pai deve invalidar estados dos filhos; não alterar PDFs fixos |
| ma55-training | data.training e progressos | Mutação antes de save exige distinção entre confirmado e rascunho |
| ma55-materials | Materiais/equipamentos do mesmo data | Inclusão/exclusão falha não pode produzir exportação de memória como se salva |
| ma61-sanitary | state, 8 frentes/42 tópicos | CAS presente; erro e rascunho não devem parecer estado confirmado |
| ma56-project | stored checklist56 | Falta coordenação de escrita entre abas; rollback local de seleção existe |
| backup | Bases persistidas e IDB A5 | Exportador lê estado persistido; não substituir por caches para melhorar aparência. Diagnóstico visual pode necessitar invalidação/data de atualização |

⚠ Não foi feita avaliação visual por screenshots, pixels, dispositivos ou execução de navegador nesta etapa. Inconsistências descritas decorrem dos handlers/modelos lidos; responsividade, acessibilidade e detalhes de apresentação devem ser verificados na matriz futura. Uma diferença de valor entre cálculo volátil, snapshot histórico e estado persistido deve primeiro ser explicada por origem, não corrigida por gravação automática.
