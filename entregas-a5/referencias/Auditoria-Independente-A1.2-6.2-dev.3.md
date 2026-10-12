# Auditoria independente — A1.2 (6.2 DEV.3)
**Dashboard Manfrin Arnez · versão 6.2-dev.3 · A1.2 (DEV, dados fictícios) · 11/10/2026**
Autor: Claude (auditor independente) · Destinatários: Dr. Marck Arnez e Codex/ChatGPT (coordenação)

> **Veredito: A1.2 APROVADA COM RESSALVAS. A etapa A1 pode ser encerrada e a A5 pode ser iniciada, desde que você autorize e que os três achados novos (N-1, N-2, N-3, todos AMARELO) entrem como itens de entrada da A5.** Os sete ajustes pedidos (AJ-11 a AJ-17) foram corrigidos e comprovados em Chromium real aberto por `file://`. Os dez cenários críticos (B-06, B-07, B-09, B-31, B-32, B-37, B-67, B-69, B-79 e B-100) passaram. Nenhum VERMELHO novo foi introduzido; os 4 VERMELHOS que restam são os mesmos defeitos pré-existentes que o Codex declarou como fora do escopo e que pertencem à A5 (e um à A2/A3). Nenhum dado foi perdido em nenhum cenário, inclusive nos de cota esgotada e de falha injetada.

---

## 0. Resumo

Matriz desta auditoria: **253 verificações — 230 APROVADO, 16 REPROVADO, 7 NÃO TESTADO.** Sinais: **226 VERDE, 23 AMARELO, 4 VERMELHO.** Os REPROVADOS não são regressões: são 3 achados novos da A1.2 (N-1, N-2, N-3), 2 limitações já declaradas (A5) e pendências pré-existentes. Dos 4 VERMELHOS, nenhum é novo: A1-48, P1-0, P1-7b e BKP-02 já constavam nas rodadas anteriores.

| O que você pediu | Resultado | Sinal |
|---|---|---|
| AJ-11 — botões de backup informam a recusa na tela acionada; "solicitado" distinto de "verificado" | Corrigido e comprovado (B-100 e C-01 a C-11) | **VERDE** |
| AJ-12 — quarentena pode ser revisada/arquivada; backup não fica bloqueado para sempre; cópia bruta do cadastro | Corrigido e comprovado (B-06, B-07, B-79, C-09 a C-21) | **VERDE** |
| AJ-13 — aprovação externa vinculada ao estado, de uso único, com estado próprio | Corrigido e comprovado (C-38 a C-42b, B-67) | **VERDE** |
| AJ-14 — `-prev` nunca sobrescrita; cópia bruta nova por operação | Corrigido e comprovado (C-30 a C-35, B-69); ver N-1 | **VERDE** (com N-1) |
| AJ-15 — fim do limite de 900.000; proteção real; falhas sem perda | Corrigido e comprovado (B-61, C-36 a C-46) | **VERDE** |
| AJ-16 — IDs numéricos lidos sem conversão; totais; exclusão por posição | Corrigido e comprovado (B-31, B-32, C-51 a C-58, b3 de 12 variantes); ver N-2 | **VERDE** (com N-2) |
| AJ-17 — correção explícita, campo a campo, com confirmação monetária | Corrigido e comprovado (B-09, B-37, C-60 a C-73) | **VERDE** |
| Preservação de dados e isolamento | Chaves reais sentinelas intactas em todos os novos caminhos de escrita (C-95) | **VERDE** |
| Compatibilidade com registros antigos, backups e 6.1 | 6.1 DEV lê e grava sobre os dados da dev.3 e restaura seus backups (B-90, B-91, B-91b); 6 campos do formato v2 preservados | **VERDE** |
| Demais módulos | 18 telas, Central Sanitária (8 frentes / 42 subtópicos), Academia, Laboratório, Exocad, simulador, pagamentos, evoluções, contabilidade: sem regressão | **VERDE** |
| Achados novos | N-1 retenção sem limpeza; N-2 livro só com ID numérico sem botão do bruto; N-3 faixa permanente após a primeira gravação | **AMARELO** |

---

## 1. Confirmação independente da declaração do Codex (97 aprovadas, 0 reprovadas, 3 pendências)

**Confirmado, com duas qualificações.**

1. **O documento confere.** `resultados.json` tem 100 verificações: 97 APROVADO, 0 REPROVADO e 3 PENDENTE, exatamente como o Codex e você informaram. As três pendências são A5-RESTAURACAO-LEGADOS, 6.1-NAVEGADOR-IDA-E-VOLTA e A5-RESTAURACAO-FIEL-E-COMPLETA; todas são fora do escopo da A1.2 e já estavam declaradas. O hash do HTML bate com `SHA256SUMS.txt`, com o relatório e com o `resultados.json`. (Verificações estáticas.)
2. **A substância confere.** Repeti os critérios em `file://`, que é como você abre o HTML, e todos os dez cenários que o Codex marcou como aprovados (B-06, B-07, B-09, B-31, B-32, B-37, B-67, B-69, B-79, B-100) passaram também comigo, com fixtures e scripts meus, sem usar nada do pacote de testes dele. **Não executei os scripts do Codex** (`testes_a1_2.py`, `gerar_dev3.py`): li-os como dados. A reprodutibilidade do HTML eu confirmei de outro modo: apliquei o `.diff` entregue sobre uma cópia da dev.2 com `patch` e o resultado ficou byte a byte idêntico à dev.3 (mesmo SHA-256). Logo, não existe mudança fora do diff que li inteiro.
3. **Qualificação 1: a contagem 97 é inflada.** Contei no `resultados.json`: 29 das 97 aprovações são verificações auxiliares repetidas ao fim de cada cenário (11 CONSOLE-n, 11 ISOLAMENTO-n e 7 BACKUP-RECUSADO-n). Sobram 68 verificações de conteúdo. (Numa mensagem de andamento eu havia dito "cerca de 26"; o número correto é 29.) Isso não é um defeito, mas o "97" não deve ser lido como 97 comportamentos diferentes.
4. **Qualificação 2: o ambiente do Codex bloqueou `file://`.** Ele testou por HTTP loopback e declarou isso. Como o HTML é aberto por `file://`, repeti tudo assim; não encontrei nenhuma diferença de comportamento causada pelo transporte.
5. **Onde divergi do relatório do Codex** (sempre em detalhe, nunca no núcleo): (a) o relatório afirma que, com ID numérico, "a cópia BRUTA permanece disponível"; isso só é verdade se a faixa global estiver visível, o que não acontece quando o único problema é o ID numérico (N-2); (b) o relatório admite que a retenção de cópias "consome cota" mas não a quantifica; medi: 63 operações com 500 linhas, 21 com 1.500 (N-1); (c) o relatório não menciona que a faixa de atenção passa a ser permanente a partir da primeira gravação (N-3).

---

## 2. Os testes críticos que você pediu, repetidos

| Teste | Descrição | Resultado | Sinal |
|---|---|---|---|
| AJ-11 | Recusa aparece na tela acionada; solicitado ≠ verificado | APROVADO | **VERDE** |
| AJ-12 | Quarentena revisável; cópia bruta do cadastro | APROVADO | **VERDE** |
| AJ-13 | Aprovação externa de uso único e estados distintos | APROVADO | **VERDE** |
| AJ-14 | `-prev` intacta; cópia por operação com os bytes exatos | APROVADO | **VERDE** |
| AJ-15 | Sem limite de 900.000; cota real; falha do principal sem perda | APROVADO | **VERDE** |
| AJ-16 | ID numérico preservado, totais corretos, exclusão por posição | APROVADO | **VERDE** |
| AJ-17 | Correção campo a campo, centavos antes/depois, cancelar preserva | APROVADO | **VERDE** |
| B-06 | Backup não fica bloqueado para sempre | APROVADO | **VERDE** |
| B-07 | Existe saída dentro do app para a quarentena | APROVADO | **VERDE** |
| B-09 | Banco antigo corrigido sem excluir o lançamento | APROVADO | **VERDE** |
| B-31 | ID numérico fica visível, sem quarentena indevida | APROVADO | **VERDE** |
| B-32 | Totais incluem a linha de ID numérico (igual à 6.1 DEV para as 12 variantes) | APROVADO | **VERDE** |
| B-37 | Categoria corrigível com outro campo inválido | APROVADO | **VERDE** |
| B-61 | Livro de 1.077.781 caracteres grava, com cópia local exata | APROVADO | **VERDE** |
| B-67 | Faixa não repete "sem espaço" depois de liberar e gravar | APROVADO | **VERDE** |
| B-69 | `-prev` antiga intacta e rotulada | APROVADO | **VERDE** |
| B-79 | Depois de restaurar backup limpo, quarentena e revisão ficam e o backup volta a funcionar | APROVADO | **VERDE** |
| B-100 | Contabilidade: recusa sem download e sem anunciar sucesso | APROVADO | **VERDE** |
| B-102 | Cópia ANTES-MESCLAR declara que omite quarentenas | APROVADO | **VERDE** |
| B-119 | Restaurar backup antigo com banco fora do padrão | REPROVADO | **AMARELO** |

Notas honestas sobre o que "passou" significa:

- **B-79** foi aprovado na forma que o Codex redefiniu (quarentena **revisada** permanece e não impede o backup). O cenário literal original (quarentena **não** revisada, depois restaurar) continua bloqueado por desenho: o usuário precisa arquivar a quarentena. Isso é coerente com AJ-12, mas é uma condição.
- **B-102** passa porque agora há aviso na confirmação da mesclagem; a omissão das quarentenas no arquivo ANTES-MESCLAR continua, declarada, e as quarentenas permanecem intactas no armazenamento (C-93).
- **B-119** continua AMARELO porque a restauração de backups com bancos fora do padrão ou ID numérico segue recusada. A recusa é segura (C-90a e C-90b: nada é alterado), e o Codex declarou isso como pendência da A5.

---

## 3. Achados novos da A1.2 (nenhum causa perda de dados)

### N-1 · AMARELO · A retenção de uma cópia completa por operação, sem limpeza, esgota a cota
O Codex implementou corretamente a regra "uma cópia bruta antes de cada operação, nunca apagar". O efeito, medido no Chromium real (cota de cerca de 5,2 milhões de caracteres, já com a base DEV embutida de 1,2 milhão):

- Livro de **500 linhas** (58.781 caracteres): **63 operações** até a primeira recusa por cota.
- Livro de **1.500 linhas** (177.781 caracteres): **21 operações**.
- Depois disso, toda gravação do livro é recusada ("não foi possível proteger a operação") e só continua com baixar e confirmar uma cópia externa **a cada operação** (AJ-13, uso único).
- A cota é compartilhada com pacientes, pagamentos e evoluções: no meu cenário, depois da recusa ainda couberam 82 pagamentos; em seguida os pagamentos também foram recusados ("libere espaço no navegador"), sem corromper nada.
- **Não existe, dentro do app, botão para apagar cópias antigas** (C-83). O único alívio é limpar dados do navegador, o que apagaria tudo e é exatamente o que não pode acontecer.

Evidência: C-81-500, C-81-1500, C-82, C-83. Classifico AMARELO porque nenhum dado é perdido e o app recusa com clareza; mas é **bloqueante para uso clínico real** (uma clínica que lance alguns itens por dia chega à cota em poucas semanas). **Ajuste sugerido (não implementado):** (a) botão "Apagar cópias antigas por operação" com lista, tamanho, confirmação explícita e regra de manter as K mais recentes e qualquer cópia ainda não baixada; (b) indicador de uso de armazenamento na faixa; (c) nunca remover quarentenas nem revisões. Pontos do código: `persist()`, linhas 313-345 (criação da cópia, 320-337); `ma62ReadSnapshots`, linha 192; montagem da lista de cópias em `ma62LedgerBanner`, a partir da linha 208.

### N-2 · AMARELO · Livro só com ID numérico: backup recusado, mas sem botão do livro bruto
Se o livro tem apenas linhas válidas, incluindo uma com ID numérico, `ma62RequestBackup` recusa o backup principal (linha 534, "ID numérico preservado no livro; ... Use a cópia BRUTA"). Porém `ma62LedgerBanner` só aparece quando há risco (linha 214) e o ID numérico não conta como risco; portanto **não há faixa e não há botão "Baixar original bruto"**. Confirmei com sonda isolada: as quatro telas testadas ficam sem faixa. O CSV continua exportável, e a restauração recusa com segurança, mas a instrução na mensagem manda para um recurso que não existe nesse estado. Além disso o backup recusado impede também a cópia **restaurável** de pacientes, pagamentos e evoluções (resta a cópia BRUTA do cadastro, que existe). Evidência: C-57.
**Ajuste sugerido:** incluir `rows.some(r=>typeof r.id!=='string')` na condição `hasRisk` da linha 214, ou colocar um botão "Baixar livro-caixa bruto" na própria página Backup, ao lado do botão do cadastro (linha 67).

### N-3 · AMARELO · A faixa de atenção fica permanente depois da primeira gravação
Com o livro 100% íntegro, nada aparece. Depois do primeiro lançamento a faixa "ATENÇÃO — REVISÃO DO LIVRO-CAIXA" surge em todas as telas e permanece depois de recarregar, sem como dispensá-la, porque a existência de qualquer cópia por operação conta como risco (linha 214: `previous!==null||snapshots.length`). Isso contradiz o espírito de B-23 (sem falso alarme) e cria alarme permanente: o usuário aprende a ignorar a faixa, inclusive quando ela anunciar uma quarentena de verdade. Evidência: N-3 (sonda em `file://`).
**Ajuste sugerido:** na linha 214, tirar `previous`, `snapshots.length` e `ma62Protection` da condição que acende a faixa global; mostrar esses itens apenas como nota discreta na página do livro-caixa. Manter a faixa para bloqueio, linhas rejeitadas, quarentena ativa, legado e falha de proteção.

### Observações menores (VERDE com nota)
- No diálogo de correção, a mensagem sai com ponto duplicado ("Campos inconsistentes: banco.."). Cosmético; linha 388 (a mensagem de `ma62LegacyIssue` já termina em ponto e o texto acrescenta outro).
- O arquivamento da quarentena pede uma única confirmação; o texto avisa que o backup principal passa a omiti-la e que é preciso baixá-la antes. A revisão guarda o corpo original dentro da própria revisão (para detectar alteração posterior), o que duplica o espaço dessa quarentena. Aceitável, mas entra na conta de N-1.

---

## 4. Preservação de dados, compatibilidade, backups e demais módulos

- **Preservação:** em todos os cenários de recusa (sem espaço, falha injetada no livro principal, leitura de conferência divergente, arquivo externo errado, aba desatualizada, restauração recusada), o livro permaneceu **byte a byte idêntico** ao semeado e a tela voltou ao estado gravado. O app nunca alterou quarentenas nem a `-prev`, nem depois de restaurar um backup (B-79). Quando eu mesmo adulterei uma quarentena já revisada, o risco foi reativado e o backup voltou a ser recusado (C-18).
- **Isolamento:** adicionar lançamento, arquivar quarentena, backup, cópia bruta, restauração e `localStorage.clear()` não alteraram nenhuma das 6 chaves reais sentinelas nem criaram chave fora do prefixo (C-95).
- **Compatibilidade com registros antigos:** 12 variantes de linhas antigas continuam visíveis (12 de 12, sem quarentena indevida) e os totais são iguais aos da 6.1 DEV para as mesmas linhas, agora **incluindo** o ID numérico. Linhas realmente ilegíveis (10 variantes) vão à quarentena. HTML malicioso em campos antigos não executa em nenhuma das 18 telas (XSS 0).
- **Backups:** o backup principal mantém exatamente os 6 campos do formato v2; é restaurável nesta mesma versão (C-04) e na **6.1 DEV** (B-91 e B-91b, incluindo o arquivo "QUARENTENAS-SEPARADAS"). A 6.1 DEV também lê e grava sobre um livro com legado e ID numérico sem apagar nenhuma das chaves novas (B-90). Resolve, no nível da 6.1 DEV, a pendência "6.1-NAVEGADOR-IDA-E-VOLTA" do Codex; a 6.1 original (2e9567df...) continua sem teste direto porque nunca me foi entregue (INT-38).
- **Restaurador estrito:** backups com ID numérico ou banco antigo são recusados sem alterar nada (C-90a, C-90b). É a pendência declarada da A5.
- **Módulos:** 18 telas abrem sem erro; Central Sanitária mantém 8 frentes e 42 subtópicos (13 de 13 testes); Academia, Laboratório, Exocad, simulador, pagamentos, evoluções (biblioteca de modelos), contabilidade e CSV contábil funcionam como antes; pagamento novo convive com os restaurados (B-122).
- **Desempenho:** com 12.000 linhas, gravar um lançamento leva 1,24 s (dev.2: 1,17 s) e a carga da página, 13 s (P0-4, inalterado). Sem regressão relevante.

---

## 5. O que parecia regressão e não era

Quando reexecutei a suíte da auditoria anterior contra a dev.3, alguns itens mudaram de cor. Investiguei cada um:

- **A1-05, A1-07, A1-10, A1-31, A1-47 e A1-60** exigiam que a `-prev` fosse criada ou trocada e que o limite de 900.000 existisse. A A1.2 mudou isso de propósito (AJ-14 e AJ-15). Os critérios são obsoletos, foram excluídos da contagem e a função equivalente é coberta por C-30 a C-35 e B-61.
- **A1-46** (linha inválida vinda da mesclagem vai à quarentena): falhou por temporização do meu roteiro, que lia antes de a página recarregar. Uma sonda corrigida em `file://` mostrou 4 linhas exibidas, 1 quarentena ativa e a faixa visível. Não é regressão.
- **B-32** do meu roteiro novo esperava R$ 117,00 por erro de conta meu (os valores de apoio somam 30,03); o app mostrou R$ 87,03, que é o correto.
- **B-57, B-58, B-11-a/b, B-77** falharam apenas por expressões regulares que procuravam o texto antigo ("BLOQUEADO", "1 arquivo(s)"); a substância foi verificada.
- **A1-45 e A1-48** continuam REPROVADOS como antes: são A4 e A5, respectivamente, e não foram tocados.

---

## 6. Pode encerrar a A1 e iniciar a A5?

**Resposta: sim, A1 pode ser encerrada como APROVADA COM RESSALVAS, e a A5 (Proteção de Backup e Restauração) pode ser iniciada quando você autorizar.** Não iniciei a A5 nem fiz qualquer correção.

Condições que recomendo:

1. **N-1, N-2 e N-3 entram como itens de entrada da A5** (ou, se você preferir fechar a A1 sem pendências, numa A1.3 mínima só com os três ajustes). N-2 e N-3 são ajustes pequenos; N-1 é uma decisão de política de retenção que dialoga com o desenho do backup da A5 (as cópias por operação passam a fazer parte do backup? por quanto tempo?).
2. **Não liberar para uso com dados reais enquanto N-1 estiver aberto.** Em uso real a cota seria atingida em semanas e o único alívio disponível hoje é arriscado.
3. Os 4 VERMELHOS pré-existentes seguem como escopo da A5 (P1-7b, A1-48, BKP-02) e da A2/A3 (P1-0). Isso é o que a A5 deve atacar primeiro, junto com a restauração de IDs numéricos e bancos antigos, a restauração fiel (B-123, que reinjeta 4 registros fictícios) e a proteção antes de restaurar.

Sugestão de autorização em uma linha: "autorizo a A5, com N-1, N-2 e N-3 como critérios de entrada", ou "autorizo uma A1.3 mínima para N-1, N-2 e N-3 e, depois, a A5".

---

## 7. Erros do meu método, corrigidos antes de registrar

- **Execução em diretório errado.** Uma cadeia de comandos minha foi iniciada fora da pasta de trabalho, e uma das duas frentes de testes rodou no lugar errado; ela não gravou resultados. Apaguei os arquivos soltos que deixou e conferi pelas datas que nenhum resultado da auditoria anterior foi sobrescrito.
- **`pkill` derrubou meu próprio shell** (código 144) e interrompeu uma sequência de suítes; refiz as que ficaram sem resultado (b9, b10, b12, b13, b14).
- **Biblioteca sem a função `rawStore`** nos roteiros c4 e c5: corrigido e reexecutado.
- **C-41 e C-42:** meu roteiro clicava no botão de confirmação antes de testar o arquivo errado, o que liberava a operação. Refeito como c2b; os resultados do c2 foram descartados.
- **B-32, C-80 e C-82:** erro de conta no primeiro; sobrecarga do meu auxiliar no segundo (medida correta em C-80b); no terceiro, a primeira versão reduzia o espaço livre a 200 caracteres, o que era artificial; refiz contando pagamentos reais.
- **C-91 e C-92:** corrida entre recarga e leitura e mensagens de diálogo truncadas pelo meu próprio auxiliar. Corrigidos.
- **Roteiros antigos que dependiam do ID como seletor** (`data-delete`, `data-row`): agora os botões usam a posição da linha; adaptei três roteiros (b1x, b3x, b5x) e descartei os critérios obsoletos listados acima.
- **t3.json copiado da rodada anterior** continha resultados antigos; reexecutei o roteiro (t3b) contra a dev.3 antes de usá-lo.
- Nenhum arquivo recebido foi alterado; o HTML da dev.3 ficou em cópia somente leitura. Nenhum dado real foi usado; só Chromium isolado e dados fictícios.

---

## Apêndice. Matriz completa

Contagem por grupo (aprovados / total): A: 7/8, B: 19/19, C: 17/17, D: 7/7, E: 7/7, F: 11/11, G: 19/20, H: 24/24, I: 0/5, J: 23/25, K: 34/34, L: 18/18, M: 38/40, N: 6/18


### A. Integridade e escopo da entrega (verificações estáticas e de documento)

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| INT-31 | Hash e tamanho do HTML dev.3 conferem com SHA256SUMS, com o relatório do Codex e com resultados.json | APROVADO | **VERDE** | SHA-256 e4e4f49c...bcc3f; 4.077.003 bytes (verificação estática). |
| INT-32 | dev.2 usada como base: hash f11dbe0e...756751 confere com o declarado pelo Codex e com a que auditei | APROVADO | **VERDE** | Cópia da dev.2 da rodada anterior, não modificada (verificação estática). |
| INT-33 | Sintaxe: 23/23 blocos de script da dev.3 passam em node --check | APROVADO | **VERDE** | Verificação estática independente. |
| INT-34 | O trecho de "function syncInfo(){" até o fim do arquivo é idêntico ao da dev.2 (módulos, modelos clínicos, Academia, Laboratório, Central Sanitária) | APROVADO | **VERDE** | Comparação de strings, verificação estática. O que mudou fica nas linhas 1-618 (antes do syncInfo). |
| INT-35 | O diff do Codex aplicado com patch sobre uma cópia da dev.2 reproduz a dev.3 byte a byte (cmp idêntico, mesmo SHA-256) | APROVADO | **VERDE** | Não há mudança fora do diff entregue; li o diff inteiro (32 trechos). Verificação estática. |
| INT-36 | resultados.json: 100 verificações = 97 APROVADO, 0 REPROVADO, 3 PENDENTE; as 3 pendências são A5/6.1/restauração fiel | APROVADO | **VERDE** | Conferência do documento (não é execução). 29 das 97 aprovações são verificações auxiliares repetidas (11 CONSOLE-n, 11 ISOLAMENTO-n, 7 BACKUP-RECUSADO-n), contadas por mim no resultados.json. |
| INT-37 | Método do Codex: Chromium real, localStorage nativo, HTTP loopback; "file://" bloqueado no ambiente dele | APROVADO | **AMARELO** | Limite do ambiente do Codex, declarado. Eu repeti em file://, que é como o HTML é aberto de verdade. Não executei os scripts do Codex (li-os como dados). |
| INT-38 | Cópia 6.1 original (2e9567df...) nunca me foi entregue; usei a 6.1 DEV (ec3714a3...ccc8f3) como leitor 6.1 | NÃO TESTADO | **AMARELO** | Compatibilidade com o HTML 6.1 original segue sem execução direta; a 6.1 DEV é a mesma base de código com banner e isolamento de DEV. |

### B. AJ-11 — Backup, recusa na tela acionada e verificação do arquivo

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| B-01 | Backup com livro-caixa íntegro: gera arquivo v2 com os mesmos campos da 6.1 | APROVADO | **VERDE** | download=true; campos=[format,version,createdAt,care,ledger,rateSettings]; lançamentos idênticos=true; taxas={"5":3.1,"10":5.2}; pacientes no backup=4896; msg="DOWNLOAD PRINCIPAL SOLICITADO AO NAVEGADOR; arquivo ainda NÃO verificado. Não é backup completo de todos os módulos: Aca" |
| B-02 | Backup gerado na dev.2 é restaurável (ida e volta, só dados fictícios) | APROVADO | **VERDE** | lançamentos restaurados idênticos=true; taxas={"5":3.1,"10":5.2}; msg="" |
| B-03 | AJ-1: livro-caixa ilegível — o backup geral NÃO é gerado e o aviso é claro (antes saía com 0 lançamentos) | APROVADO | **VERDE** | arquivo gerado=false; texto do livro intacto=true; msg="BACKUP PRINCIPAL RECUSADO: livro ilegível/bloqueado, linhas rejeitadas, registros inconsistentes ou quarentenas ativas. Nenhum download foi solicitado. Baixe as cópias BRUTAS do cadastro e do livro, revise/corrija os registros e a" |
| B-04 | AJ-1: com livro ilegível o painel oferece a cópia bruta e ela é exata | APROVADO | **VERDE** | botões do aviso=Abrir Conciliação \| Baixar original bruto |
| B-05 | AJ-1: livro com linha em quarentena — backup recusado com explicação | APROVADO | **VERDE** | arquivo gerado=false; msg="BACKUP PRINCIPAL RECUSADO: livro ilegível/bloqueado, linhas rejeitadas, registros inconsistentes ou quarentenas ativas. Nenhum download foi solicitado. Baixe as cópias BRUTAS do cadastro e do livro, r" |
| B-08 | AJ-1/AJ-3: registro legado (banco "Itau") — backup recusado (comportamento declarado) | APROVADO | **VERDE** | arquivo=false; msg="BACKUP PRINCIPAL RECUSADO: livro ilegível/bloqueado, linhas rejeitadas, registros inconsistentes ou quarentenas ativas. " |
| C-01 | AJ-11: backup principal íntegro — v2 com exatamente os 6 campos 6.1, lançamentos idênticos, mensagem diz "solicitado/não verificado" | APROVADO | **VERDE** | arquivo=Manfrin-Arnez-backup-PRINCIPAL-2026-10-11.json; campos=[format,version,createdAt,care,ledger,rateSettings]; ledger idêntico=true; msg="DOWNLOAD PRINCIPAL SOLICITADO AO NAVEGADOR; arquivo ainda NÃO verificado. Não é backup completo de todos os módulos: Academia, checklists e cópias locais exigem exportaçõ" |
| C-02 | AJ-11: "Verificar arquivo baixado" aceita o arquivo idêntico ao último gerado | APROVADO | **VERDE** | msg="ARQUIVO PRINCIPAL VERIFICADO: conteúdo idêntico ao último download solicitado nesta sessão. Não comprova dados posteriores nem inclui módulos/cópias omitidos." |
| C-03 | AJ-11: arquivo ligeiramente diferente (1 espaço) é rejeitado na verificação | APROVADO | **VERDE** | msg="ARQUIVO NÃO VERIFICADO: Arquivo não corresponde ao último download solicitado" |
| C-04 | Backup principal da dev.3 é restaurável (ida e volta) e as taxas voltam | APROVADO | **VERDE** | ledger idêntico=true; taxas={"5":3.1} |
| C-05 | AJ-11: verificar sem ter solicitado backup nesta sessão não declara sucesso | APROVADO | **VERDE** | msg="ARQUIVO NÃO VERIFICADO: Solicite primeiro um backup nesta sessão" |
| B-100 | AJ-11: Contabilidade com quarentena ativa — nenhum download e a tela da Contabilidade NÃO diz que o backup foi solicitado | APROVADO | **VERDE** | botão presente=true; download=false; status contabilidade="BACKUP PRINCIPAL RECUSADO: livro ilegível/bloqueado, linhas rejeitadas, registros inconsistentes ou quarentenas ativas. Nenhum download foi solicitado. Baixe as cópias BRUTAS do cadastro e do livro, r" |
| C-06 | AJ-11: página Backup com quarentena ativa — recusa sem download | APROVADO | **VERDE** | download=false; msg="BACKUP PRINCIPAL RECUSADO: livro ilegível/bloqueado, linhas rejeitadas, registros inconsistentes ou quarentenas ativas. Nenhum download foi solicitado. Baixe as" |
| C-07 | AJ-11: Contabilidade com livro íntegro — download efetivo e status "solicitado/não verificado" | APROVADO | **VERDE** | download=true; arquivo=Manfrin-Arnez-backup-PRINCIPAL-2026-10-11.json; status="DOWNLOAD PRINCIPAL SOLICITADO AO NAVEGADOR; arquivo ainda NÃO verificado. Não é backup completo de todos os módulos: Academia, checklists e cópias locais exigem exportaçõ" |
| C-08 | Cadastro ilegível: backup principal recusado nas duas rotas (sem arquivo substitutivo) | APROVADO | **VERDE** | pág.Backup="BACKUP PRINCIPAL RECUSADO: cadastro ilegível ou armazenamento indisponível. Baixe a cópia BRUTA do cadastro; r"; Contab="BACKUP PRINCIPAL RECUSADO: cadastro ilegível ou armazenamento indisponível. Baixe a cópia BRUTA do cadastro; r"; downloads=false/false |
| C-09 | AJ-12b: cópia BRUTA do cadastro ilegível é exata (bytes) e o cadastro não foi alterado | APROVADO | **VERDE** | bytes idênticos=true; nome=Manfrin-Arnez-CADASTRO-PAGAMENTOS-EVOLUCOES-BRUTO-NAO-RESTAURAR-2026-10-11.json; chave intacta=true |
| C-10 | AJ-12b: o botão da Contabilidade também baixa a cópia BRUTA exata | APROVADO | **VERDE** | bytes idênticos=true |
| C-11 | AJ-12b: sem chave de cadastro persistida a cópia bruta é recusada (não inventa dados) | APROVADO | **VERDE** | download=false; msg="Cópia BRUTA recusada: Não existe cadastro persistido nesta chave; nenhum arquivo substitutivo foi gerado" |
| B-12 | Duas abas: backup na aba desatualizada é recusado (não exporta lista antiga) | APROVADO | **VERDE** | arquivo=false; msg="BACKUP PRINCIPAL RECUSADO: Livro-caixa alterado por outra aba; recarregue. Nenhum download foi solicitado." |

### C. AJ-12 — Quarentena revisada/arquivada, cópia bruta do cadastro, mesclagem

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| C-12 | AJ-12: quarentena aparece como ATIVA com botão "Revisar e arquivar (sem recuperar)" e download | APROVADO | **VERDE** | faixa="ATENÇÃO — REVISÃO DO LIVRO-CAIXA1 quarentena(s) ativa(s): revise e guarde uma cópia separada.Abrir ConciliaçãoBaixar original brutoRevisar e baixar arquivos em quarentena (1)1. ma-ledger-v1-rejeitados-20260101000000 — ATIVA · 1 linha(s)BaixarRevis"; botões=Abrir Conciliação \| Baixar original bruto \| Baixar \| Revisar e… |
| C-13 | AJ-12: cancelar o diálogo de arquivamento não cria revisão nem altera a quarentena | APROVADO | **VERDE** | quarentena intacta=true; revisão criada=false; diálogo="Arquivar como REVISADA? O original permanece intacto e NÃO recupera lançamentos. O backup principal NÃO inclui esta quar" |
| B-07 | AJ-12: existe saída dentro do app — arquivar quarentena como revisada; chave original byte-idêntica | APROVADO | **VERDE** | quarentena intacta=true; revisão=version,key,originalBody,reviewedAt,acknowledged; faixa="ATENÇÃO — REVISÃO DO LIVRO-CAIXAQuarentena revisada e arquivada por confirmação manual. Original intacto; lançamentos NÃO recuperados. 1 quarentena(s) revisada(s)/arquivada(s), NÃO recuperadas e NÃO incluídas no backu" |
| B-06 | Backup deixa de ficar bloqueado para sempre: após arquivar + recarregar, o backup principal é gerado, nomeado "QUARENTENAS-SEPARADAS", com aviso de omissão | APROVADO | **VERDE** | arquivo=Manfrin-Arnez-backup-PRINCIPAL-QUARENTENAS-SEPARADAS-2026-10-11.json; msg="DOWNLOAD PRINCIPAL SOLICITADO AO NAVEGADOR; arquivo ainda NÃO verificado. 1 quarentena(s) arquivada(s) OMITIDA(S), não recuperadas; exporte-as separadamente. Não é backup completo de todos os módulos: Academia, checklists e cópias"; ledger igual=… |
| C-15 | AJ-12: o backup principal com quarentena arquivada NÃO contém as linhas da quarentena (omissão declarada) e mantém os 6 campos | APROVADO | **VERDE** | contém quarentena=false; campos=format,version,createdAt,care,ledger,rateSettings |
| C-16 | AJ-12: quarentena arquivada continua listada como ARQUIVADA, baixável e idêntica ao original | APROVADO | **VERDE** | download exato=true; faixa="ATENÇÃO — REVISÃO DO LIVRO-CAIXA1 quarentena(s) revisada(s)/arquivada(s), NÃO recuperadas e NÃO incluídas no backup principal. Exporte-as separadamente.Abrir ConciliaçãoBaixar original brutoRevisar" |
| C-17 | AJ-12/AJ-11: Contabilidade com quarentena arquivada gera backup e o status declara omissão | APROVADO | **VERDE** | download=true; status="DOWNLOAD PRINCIPAL SOLICITADO AO NAVEGADOR; arquivo ainda NÃO verificado. 1 quarentena(s) arquivada(s) OMITIDA(S), não recuperadas; exporte-as separadamente. Não é backup completo de todos os módulos:" |
| C-18 | AJ-12: quarentena alterada depois de revisada reativa o risco (backup recusado, estado ATIVA) | APROVADO | **VERDE** | download=false; msg="BACKUP PRINCIPAL RECUSADO: livro ilegível/bloqueado, linhas rejeitadas, registros inconsistentes ou "; faixa="ATENÇÃO — REVISÃO DO LIVRO-CAIXA1 quarentena(s) ativa(s): revise e guarde uma cópia separada.Abrir ConciliaçãoBaixar original brutoRevisar e baixar arquivos " |
| C-19 | AJ-12: linha rejeitada recente (nova quarentena) continua bloqueando o backup; arquivar a antiga não libera | APROVADO | **VERDE** | download=false; quarentenas=2; msg="BACKUP PRINCIPAL RECUSADO: livro ilegível/bloqueado, linhas rejeitadas, registros inconsistentes ou quarentenas ativas. " |
| C-20 | AJ-12: quarentena de conteúdo não reconhecido também pode ser revisada, sem alterar bytes | APROVADO | **VERDE** | bytes iguais=true; revisão=true |
| C-21 | AJ-12: arquivar sem espaço — recusa explícita, quarentena intacta, risco continua ativo | APROVADO | **VERDE** | faixa="ATENÇÃO — REVISÃO DO LIVRO-CAIXAArquivamento recusado: Failed to execute 'setItem' on 'Storage': Setting the value of '__MA_DEV61_SANDBOX__:ma-ledger-v1-quarantine-review:ma-ledger-v1-rejeitados-20" |
| B-79 | Após restaurar um backup limpo, quarentena e revisão arquivadas permanecem e o backup principal funciona de novo | APROVADO | **VERDE** | quarentena=true; revisão=true; backup=true; msg="DOWNLOAD PRINCIPAL SOLICITADO AO NAVEGADOR; arquivo ainda NÃO verificado. 1 quarentena(s) arquivada(s) OMITIDA(S), não recuperadas; exporte-" |
| C-92 | Mesclagem: confirmação declara que a cópia ANTES-MESCLAR NÃO inclui quarentenas; arquivo é baixado com o nome novo e 6 campos | APROVADO | **VERDE** | nome=Manfrin-Arnez-ANTES-MESCLAR-PRINCIPAL-NAO-INCLUI-QUARENTENAS-2026-10-11.json; diálogo final="…s serão preservados. Será solicitado o download da cópia PRINCIPAL ANTES da mesclagem. Ela NÃO inclui quarentenas, cópias locais, Academia ou checklists; preserve-os separadamente. O navegador não confirma que o arquivo foi salvo." |
| C-93 | Mesclagem: lançamentos do backup acrescentados ao livro sem apagar os atuais; quarentena existente intacta | APROVADO | **VERDE** | linhas=5 (esperado 5); quarentena intacta=true |
| C-94 | Mesclagem (B-102): a cópia ANTES-MESCLAR contém o livro anterior legível mas NÃO a quarentena (omissão declarada) | APROVADO | **VERDE** | linhas do livro na cópia=2; contém quarentena=false |
| B-101 | Exportação CSV do livro-caixa com quarentena: o arquivo contém só as linhas válidas; há aviso na tela de que há linhas fora? | APROVADO | **VERDE** | linhas CSV=4; mensagem="CSV dos lançamentos legíveis: NÃO contém o original ilegível nem quarentenas. Preserve as cópias bru"; faixa global visível=true |
| B-102 | Mesclagem: o arquivo automático "ANTES-MESCLAR" inclui as linhas em quarentena ou avisa que elas ficaram de fora | APROVADO | **VERDE** | snapshot gerado=true; contém linha em quarentena=false; lançamentos no snapshot=4; chaves de quarentena=1 — Critério "inclui as linhas OU avisa": a confirmação da mesclagem agora declara que a cópia NÃO inclui quarentenas (ver C-92). A omissão continua; as quarentenas permanecem intactas no armazenamento (C-93). |

### D. AJ-13 — Aprovação externa de uso único

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| C-38 | AJ-13: a cópia externa baixada é exata; se o usuário cancela a confirmação, nada é liberado | APROVADO | **VERDE** | cópia exata=true; livro intacto=true; msg="Gravação bloqueada: não foi possível proteger a operação com cópia local. Original intacto. Baixe e " |
| C-39 | AJ-13: após confirmação externa manual a gravação ocorre e o estado é rotulado "confirmada manualmente / não verificada pelo app" | APROVADO | **VERDE** | gravou=true; faixa depois="ATENÇÃO — REVISÃO DO LIVRO-CAIXAOperação protegida por cópia externa confirmada manualmente do estado anterior. Sem cópia local desta operação; faça nova cópia do estado atualizado.Abrir ConciliaçãoBaixar original bruto" |
| B-67 | AJ-13: após liberar e gravar, a faixa NÃO repete "Sem espaço para cópia local" nem o pedido já atendido | APROVADO | **VERDE** | faixa="ATENÇÃO — REVISÃO DO LIVRO-CAIXAOperação protegida por cópia externa confirmada manualmente do estado anterior. Sem cópia local desta operação; faça nova cópia do estado atualizado.Abrir ConciliaçãoBaixar original bruto" |
| C-40 | AJ-13: a aprovação externa vale UMA operação; a segunda gravação sem espaço volta a ser recusada | APROVADO | **VERDE** | segunda gravou=false; msg="Gravação bloqueada: não foi possível proteger a operação com cópia local. Original intacto. Baixe e verifique uma cópia externa." |
| C-41 | AJ-13: arquivo externo errado é rejeitado na verificação (mensagem "NÃO verificada") e a gravação continua recusada | APROVADO | **VERDE** | input presente=true; msg verificação="Cópia externa NÃO verificada: Conteúdo diferente do livro atual"; livro intacto=true; msg gravação="Gravação bloqueada: não foi possível proteger a operação com cópia local. Origin" |
| C-42 | AJ-13: arquivo externo idêntico (verificado pelo conteúdo) libera uma operação e o estado é rotulado "verificado pelo conteúdo" | APROVADO | **VERDE** | gravou=true; faixa="ATENÇÃO — REVISÃO DO LIVRO-CAIXAOperação protegida por cópia externa verificada pelo conteúdo do estado anterior. Sem cópia local desta operação; faça nova cópia do estado atualizado.Abrir ConciliaçãoBaixar original bruto" |
| C-42b | AJ-13: a verificação por conteúdo também vale uma única operação | APROVADO | **VERDE** | msg="Gravação bloqueada: não foi possível proteger a operação com cópia local. Original intacto. Baixe e " |

### E. AJ-14 — Chave -prev intacta e cópia por operação

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| C-30 | AJ-14: cada operação cria uma cópia bruta nova com os bytes EXATOS do estado anterior (3 operações, 3 chaves) | APROVADO | **VERDE** | chaves=3; 1ª==semente=true; 2ª==estado após op1=true; 3ª tem 22 linhas=true; exemplo de chave="ma-ledger-v1-session-prev-20261011223238517-e6484c05-257c-43fe-b0b9-fe28a73a4a4c-1" |
| B-69 | AJ-14: -prev antiga permanece byte-idêntica após várias gravações e é rotulada como origem não comprovada | APROVADO | **VERDE** | prev intacta=true |
| C-31 | AJ-14: faixa informa -prev de sessão não comprovada e cópias locais por operação; permite baixar cada uma | APROVADO | **VERDE** | faixa="ATENÇÃO — REVISÃO DO LIVRO-CAIXAA chave -prev é uma cópia anterior, de sessão/data não comprovadas. Conteúdo preservado; NÃO é apresentada como anterior à gravação atual. 3 cópia(s) local(is) de operações, fora do backup principal. Cópia local verificada: ma-ledger-v1-session-prev-202610112232385"; botões=Abrir Conciliaç… |
| C-32 | AJ-14: download de uma cópia por operação devolve exatamente o conteúdo guardado | APROVADO | **VERDE** | idêntico=true; nome=ma-ledger-v1-session-prev-20261011223238517-e6484c05-257c-43fe-b0b9-fe28a73a4a4c-1.json |
| C-33 | AJ-14: download da -prev devolve o conteúdo original byte-a-byte | APROVADO | **VERDE** | idêntico=true |
| C-34 | AJ-14: nova sessão não apaga cópias antigas (4 chaves) e a -prev continua intacta | APROVADO | **VERDE** | chaves=4; prev intacta=true |
| C-35 | AJ-14: sem -prev prévia, a chave -prev não é criada (nem recriada); proteção usa a chave por operação | APROVADO | **VERDE** | prev existe=false; snapshots=1 |

### F. AJ-15 — Sem limite de 900.000, cota real, falhas, duas abas, desempenho

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| B-61 | AJ-15: livro com 1077781 caracteres (>900.000) grava sem pedir cópia externa, com cópia local exata | APROVADO | **VERDE** | tamanho=1077781; gravou=true; cópia local exata=true; msg="Lançamento salvo neste navegador DEV." |
| C-36 | AJ-15: sem espaço para a cópia local — gravação recusada, livro byte-idêntico, tela coerente, botão de cópia externa | APROVADO | **VERDE** | livro intacto=true; linhas na tela 40->40; msg="Gravação bloqueada: não foi possível proteger a operação com cópia local. Original intacto. Baixe e verifique uma cópia externa."; botões=Abrir Conciliação \| Baixar original bruto \| Baixar cópia externa e confirmar |
| C-37 | AJ-15: com folga só para o crescimento (não para a cópia) a gravação continua recusada — não grava sem proteção | APROVADO | **VERDE** | livro intacto=true; msg="Gravação bloqueada: não foi possível proteger a operação com cópia local. Original intacto. Baixe e verifique uma cópia " |
| C-43 | AJ-15: falha na gravação do livro principal — original intacto, tela restaurada, aviso e cópia de proteção guardada | APROVADO | **VERDE** | livro intacto=true; tela 20->20; snapshots=1; msg="Não foi possível salvar: armazenamento cheio ou indisponível. As alterações desta tentativa não fora"; faixa="ATENÇÃO — REVISÃO DO LIVRO-CAIXAGravação recusada; livro original preservado. A cópia de proteção, se criada, permanece guardada. 1 cópia(s) local(" |
| C-44 | AJ-15: depois da falha, nova operação funciona normalmente | APROVADO | **VERDE** | msg="Lançamento salvo neste navegador DEV."; snapshots=2 |
| C-45 | AJ-15: se a leitura de conferência da cópia local diverge, a gravação é recusada (livro intacto) | APROVADO | **VERDE** | livro intacto=true; msg="Gravação bloqueada: não foi possível proteger a operação com cópia local. Original intacto. Baixe e verifique uma cópia externa." |
| C-46 | AJ-15/concorrência: aba desatualizada não sobrescreve o livro gravado por outra aba | APROVADO | **VERDE** | livro = o da aba B=true; msg="Alteração externa detectada; nada foi gravado." |
| C-80 | AJ-15/16: 12.000 linhas — abertura do livro e gravação de 1 lançamento em tempo aceitável | APROVADO | **VERDE** | abrir=870 ms; gravar=12567 ms (inclui render); load=13181 ms; linhas=12001 — O tempo de 12,5 s era sobrecarga do meu auxiliar (render + espera). Medida correta em C-80b: 1.244 ms (dev.3) contra 1.172 ms (dev.2), sem regressão. |
| B-75 | Desempenho: gravar 1 lançamento com ~6.500 linhas (abaixo do limite) e custo da faixa por chamada | APROVADO | **VERDE** | gravação 869/818 ms; faixa 7 ms/chamada; load 13147 ms — Sem regressão: 6.500 linhas gravam em 869/818 ms na dev.3 (dev.2 843/1077 ms; dev.1 770/1059 ms; 6.1 777/749 ms). O limite de 500 ms do meu script nunca foi atingido por nenhuma versão, inclusive a 6.1. |
| B-76 | Desempenho: 6.500 registros todos "antigos" (validação lança exceção por linha) — faixa e gravação continuam fluidas | APROVADO | **VERDE** | faixa 31 ms/chamada; gravação 617 ms; load 12533 ms |
| C-80b | Desempenho com 12.000 linhas (mesmo roteiro em dev.2 e dev.3): gravar 1 lançamento / mudar 1 categoria / renderizar o livro | APROVADO | **VERDE** | dev.2: 1.172 / 1.971 / 927 ms; dev.3: 1.244 / 2.270 / 1.104 ms; carga da página 13,1 s e 13,4 s (P0-4, inalterado). Sem regressão relevante (c6). |

### G. AJ-16 — IDs numéricos, totais e linhas antigas preservadas

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| B-31 | AJ-16: ID numérico finito fica na lista (sem quarentena indevida) e o livro é byte-idêntico | APROVADO | **VERDE** | linhas exibidas=6/6; quarentenas=0; livro byte-idêntico=true |
| B-32 | AJ-16: totais incluem as linhas de ID numérico (receitas R$ 117,00; despesas R$ 20,00 sobre os valores originais) | APROVADO | **VERDE** | métricas="Receitas classificadas=R$ 87,03 \| Despesas operacionais=R$ 20,00 \| Retiradas separadas=R$ 0,00 \| Fluxo operacional=R$ 67,03" — Critério do meu script tinha erro de conta (esperava R$ 117,00; os valores de mkRows somam 30,03). Mostrado: R$ 87,03 = 30,03 + 50,00 (ID numérico) + 7,00 (ID texto), o resultado correto so… |
| C-51 | AJ-16: excluir com confirmação CANCELADA não altera o livro (byte-idêntico) | APROVADO | **VERDE** | livro idêntico=true; diálogo="Excluir somente este lançamento? A cópia de proteção preservará o estado anterior." |
| C-52 | AJ-16: excluir a linha de id 123 (numérico) remove SÓ ela; a linha "123" (texto) permanece com tipo string | APROVADO | **VERDE** | linhas=5; ids=["Cora:B0","Cora:B1","Cora:B2","123","D1"] |
| C-53 | AJ-16: excluir a linha "123" (texto) remove SÓ ela; a numérica 123 permanece com tipo number | APROVADO | **VERDE** | ids=["Cora:B0","Cora:B1","Cora:B2",123,"D1"] |
| C-54 | AJ-16: alterar categoria de linha de ID numérico preserva o tipo do ID e o valor | APROVADO | **VERDE** | linha={"id":123,"date":"2026-09-10","bank":"Cora","description":"id numerico","amount":5000,"kind":"A classificar"} |
| C-55 | AJ-16: exportação CSV funciona com ID numérico (sem exceção) e inclui a linha | APROVADO | **VERDE** | csv=6 linhas; erros de página=0 |
| C-56 | AJ-16: importar CSV acrescenta linhas sem converter o ID numérico existente | APROVADO | **VERDE** | linhas=7; numérico preservado=true; msg="2 importados; 0 IDs já existentes ignorados. Confira as classificações." |
| C-57 | AJ-16: backup com ID numérico é recusado EXPLICITAMENTE e o livro bruto exato pode ser baixado | REPROVADO | **AMARELO** | download backup=false; msg="BACKUP PRINCIPAL RECUSADO: ID numérico preservado no livro; restauração deste legado PENDENTE A5. Use a cópia BRUTA. Nenhum download foi solicitado."; bruto idêntico=false — ACHADO N-2: com um livro só com ID numérico (válido) não aparece a faixa global nem o botão "Baixar original bruto"; a recusa m… |
| C-58 | AJ-16: IDs inválidos (null, objeto, vazio) vão à quarentena; livro original preservado; válidas visíveis | APROVADO | **VERDE** | quarentenas=1; exibidas=3; livro idêntico=true |
| B-30 | AJ-3: linhas legíveis pela 6.1 permanecem visíveis (11 de 12 variantes; só linha ilegível vai para quarentena) | APROVADO | **VERDE** | visíveis=12 de 12; quarentena=nenhuma |
| B-31-12v | AJ-3: id NUMÉRICO (a 6.1 exibia) agora vai para quarentena e sai dos totais | APROVADO | **VERDE** | linha 10 (id numérico) visível. Critério novo exige id em texto; a 6.1 aceitava qualquer id "verdadeiro" — O título e o critério vêm da dev.2 (onde o id numérico ia para a quarentena). Na dev.3 a linha de id numérico fica VISÍVEL e sem quarentena: AJ-16 resolvido (ver B-30: 12 de 12 variantes visíveis). |
| B-32-12v | AJ-3: totais da Conciliação iguais aos da 6.1 para o mesmo livro (quando a linha é aceita) | APROVADO | **VERDE** | 6.1: "Receitas classificadas R$ 285,51 Somente lançamentos cadastrados Despesas operacionais R$ 0,00 Somente lançamentos cadastrados Retiradas sep"  \|  dev.2: "Receitas classificadas R$ 285,51 Somente lançamentos cadastrados Despesas operacionais R$ 0,00 Somente lançamentos cadastrados Retiradas sep"; linhas 6.1=12 dev.2=12 — … |
| B-34 | AJ-3: cada linha fora do padrão atual recebe a marca "Registro antigo: conferir campos" | APROVADO | **VERDE** | marcas=9; esperado ≥9 (banco, zero, fração, categoria, descrição vazia, data 30/02, data barras, receita negativa, sem categoria) |
| B-35 | AJ-3: ao gravar um lançamento novo os registros antigos continuam idênticos em storage (campo a campo) | APROVADO | **VERDE** | antigos preservados idênticos=true; linhas gravadas=13; msg="Lançamento salvo neste navegador DEV." |
| B-38 | AJ-3: exportação CSV inclui os registros antigos | APROVADO | **VERDE** | linhas CSV=14 |
| B-39 | AJ-3: excluir registro antigo funciona e só esse registro é removido | APROVADO | **VERDE** | ok |
| B-40 | Erros de console (cenário de registros antigos) | APROVADO | **VERDE** | erros=0  |
| B-41 | Linhas realmente ilegíveis (null, texto, vazio, valor texto, data numérica...) vão todas para a quarentena sem derrubar o livro | APROVADO | **VERDE** | quarentena=10/10; visíveis=1; erros=0 |
| B-42 | AJ-3: HTML em id/data/banco/descrição/categoria de registro antigo não executa nem injeta elementos (todas as telas) | APROVADO | **VERDE** | window.__xss=undefined; imgs injetadas=0; <b> injetado=false |

### H. AJ-17 — Correção explícita campo a campo

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| C-60 | AJ-17: com banco antigo ("Itau") o backup é recusado (comportamento declarado) | APROVADO | **VERDE** | download=false; msg="BACKUP PRINCIPAL RECUSADO: livro ilegível/bloqueado, linhas rejeitadas, registros inconsistentes ou quarentenas ativas. Nenhum dow" |
| C-61 | AJ-17: a linha antiga mostra QUAL campo está inconsistente (não só "conferir campos") | APROVADO | **VERDE** | aviso na linha="Registro antigo: Campos inconsistentes: banco." |
| B-09 | AJ-17: banco antigo é corrigido explicitamente SEM excluir o lançamento; id, valor, data, descrição e categoria intactos | APROVADO | **VERDE** | linha={"id":"Itau:1","date":"2026-09-13","bank":"Cora","description":"banco antigo","amount":500,"kind":"Receita"}; total=4; msg="Campo bank corrigido explicitamente. Outros campos preservados." |
| C-62 | AJ-17: depois de corrigir o banco o backup principal é liberado (sem precisar excluir dado) | APROVADO | **VERDE** | download=true; msg="DOWNLOAD PRINCIPAL SOLICITADO AO NAVEGADOR; arquivo ainda NÃO verificado. Não é backup completo de todos os módulos: Aca" |
| B-37 | AJ-17: categoria de legado com OUTRO campo inválido (banco) é corrigível isoladamente; banco, valor e demais campos intactos | APROVADO | **VERDE** | linha={"id":"Z1","date":"2026-09-14","bank":"Nubank","description":"dois campos","amount":700,"kind":"Receita"}; diálogo="Alterar categoria de "Pix" para "Receita"? O valor original será preservado; os totais por categoria podem mudar."; msg="Campo kind corrigido explicitamente. Outros campos preservados. Ainda requer revisão: … |
| C-63 | AJ-17: mudança de categoria pede confirmação e informa impacto nos totais | APROVADO | **VERDE** | diálogo="Alterar categoria de "Pix" para "Receita"? O valor original será preservado; os totais por categoria podem mudar." |
| C-64 | AJ-17: com o banco ainda inválido o backup continua recusado (não destrava indevidamente) | APROVADO | **VERDE** | download=false |
| C-65 | AJ-17: corrigido o segundo campo, o registro sai da lista de legados e o backup é liberado | APROVADO | **VERDE** | linha={"id":"Z1","date":"2026-09-14","bank":"Sicredi","description":"dois campos","amount":700,"kind":"Receita"}; backup=true |
| C-66 | AJ-17: alteração monetária mostra "antes → depois" em centavos e, se CANCELADA, o livro fica byte-idêntico | APROVADO | **VERDE** | diálogo="ALTERAÇÃO FINANCEIRA EXPLÍCITA: 10.5 → 1050 centavos. Esta mudança afeta os totais. Confirma?"; livro idêntico=true; msg="Correção cancelada; nada foi alterado." |
| C-67-vírgula_decimal | AJ-17: valor inválido (vírgula decimal) é recusado sem alterar o livro | APROVADO | **VERDE** | entrada="10,5"; livro idêntico=true; msg="Campo inconsistente: valor em centavos (inteiro seguro e diferente de zero)." |
| C-67-zero | AJ-17: valor inválido (zero) é recusado sem alterar o livro | APROVADO | **VERDE** | entrada="0"; livro idêntico=true; msg="Campo inconsistente: valor em centavos (inteiro seguro e diferente de zero)." |
| C-67-texto | AJ-17: valor inválido (texto) é recusado sem alterar o livro | APROVADO | **VERDE** | entrada="abc"; livro idêntico=true; msg="Campo inconsistente: valor em centavos (inteiro seguro e diferente de zero)." |
| C-67-decimal | AJ-17: valor inválido (decimal) é recusado sem alterar o livro | APROVADO | **VERDE** | entrada="10.5"; livro idêntico=true; msg="Campo inconsistente: valor em centavos (inteiro seguro e diferente de zero)." |
| C-67-negativo_em_receita | AJ-17: valor inválido (negativo em receita) é recusado sem alterar o livro | APROVADO | **VERDE** | entrada="-500"; livro idêntico=true; msg="Receita deve ser positiva; despesa e retirada devem ser negativas. Corrija explicitamente o valor ou selecione categoria" |
| C-68 | AJ-17: valor corrigido (aceito) altera só o amount; os outros campos e as outras linhas ficam idênticos | APROVADO | **VERDE** | linha={"id":"F1","date":"2026-09-16","bank":"Cora","description":"valor quebrado","amount":1050,"kind":"Receita"} |
| C-69 | AJ-17: data inexistente (2026-02-30) é recusada, livro intacto | APROVADO | **VERDE** | msg="Campo inconsistente: data." |
| C-70 | AJ-17: descrição em branco é recusada, livro intacto | APROVADO | **VERDE** | msg="Campo inconsistente: descrição." |
| C-71 | AJ-17: Receita com valor negativo — outro valor ainda negativo é recusado com mensagem de sinal | APROVADO | **VERDE** | msg="Receita deve ser positiva; despesa e retirada devem ser negativas. Corrija explicitamente o valor ou selecione categoria compatível." |
| C-72 | AJ-17: categoria Despesa para valor negativo corrige o sinal sem alterar o valor | APROVADO | **VERDE** | linha={"id":"S1","date":"2026-09-15","bank":"Cora","description":"sinal errado","amount":-300,"kind":"Despesa"} |
| C-73 | AJ-17: após corrigir todas as linhas legadas o backup é liberado | APROVADO | **VERDE** | download=true; msg="DOWNLOAD PRINCIPAL SOLICITADO AO NAVEGADOR; arquivo ainda NÃO verificado. Não é backup completo de t" |
| B-10 | Legado com categoria inválida: corrigir a categoria pela tela remove a marcação e libera o backup | APROVADO | **VERDE** | select encontrado=true; kind gravado=Receita; backup após corrigir=true; msg="DOWNLOAD PRINCIPAL SOLICITADO AO NAVEGADOR; arquivo ainda NÃO verificado. Não é backup completo de t" |
| B-11-a | Cadastro com JSON inválido: backup geral não finge conter os pacientes; dado armazenado intacto | APROVADO | **VERDE** | arquivo=false; cadastro intacto=true; msg="BACKUP PRINCIPAL RECUSADO: cadastro ilegível ou armazenamento indisponível. Baixe a cópia BRUTA do cadastro; restauração/reparo pendentes para A5." — Regex do meu critério esperava a palavra "BLOQUEADO"; a mensagem agora diz "RECUSADO". Substância: nenhum arquivo gerado e cadastro inta… |
| B-11-b | Cadastro com versão desconhecida: backup geral não finge conter os pacientes; dado armazenado intacto | APROVADO | **VERDE** | arquivo=false; cadastro intacto=true; msg="BACKUP PRINCIPAL RECUSADO: cadastro ilegível ou armazenamento indisponível. Baixe a cópia BRUTA do cadastro; restauração/reparo pendentes para A5." — Idem B-11-a (versão desconhecida 99). |
| B-37-12v | AJ-3: alterar a categoria de um legado (banco inválido) funciona sem apagar nem corromper a linha | APROVADO | **VERDE** | kind após mudar=A classificar; msg="Campo kind corrigido explicitamente. Outros campos preservados. Ainda requer revisão: Campos inconsistentes: banco."; banco preservado=Outro |

### I. Achados novos da A1.2

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| C-81-500 | AJ-14/15: ledger de 500 linhas (58781 caracteres) — operações consecutivas até a primeira recusa por cota | REPROVADO | **AMARELO** | operações gravadas antes da recusa=63; cópias por operação acumuladas=63; armazenamento usado 1200864 -> 5212425 caracteres; msg="Gravação bloqueada: não foi possível proteger a operação com cópia local. Original intacto. Baixe e verifique uma cópia externa."; botões da faixa=Abrir Conciliação \| Baixar original bruto \| Baixar… |
| C-81-1500 | AJ-14/15: ledger de 1500 linhas (177781 caracteres) — operações consecutivas até a primeira recusa por cota | REPROVADO | **AMARELO** | operações gravadas antes da recusa=21; cópias por operação acumuladas=21; armazenamento usado 1319864 -> 5089925 caracteres; msg="Gravação bloqueada: não foi possível proteger a operação com cópia local. Original intacto. Baixe e verifique uma cópia externa."; botões da faixa=Abrir Conciliação \| Baixar original bruto \| Baixar… |
| C-82 | AJ-14/15: ao esgotar a cota com cópias por operação (63 operações de livro), quantos pagamentos ainda cabem e o que acontece depois (efeito colateral da retenção sem limpeza) | REPROVADO | **AMARELO** | operações do livro até a recusa=63; cópias acumuladas=63; caracteres livres após a recusa≈30221; pagamentos que ainda couberam=82; mensagem do primeiro pagamento recusado="Não foi possível salvar. O registro não foi alterado. Faça backup e libere espaço no navegador." — ACHADO N-1: depois da recusa por cota ainda couberam 82 pa… |
| C-83 | AJ-14: existe, dentro do app, forma de APAGAR cópias por operação antigas para liberar cota? | REPROVADO | **AMARELO** | botões de cópia=64; botões distintos=Abrir Conciliação \| Baixar original bruto \| Baixar cópia externa e confirmar \| Baixar cópia — ACHADO N-1: não há botão de apagar/limpar cópias antigas; o único alívio é limpar dados do navegador (arriscado). |
| N-3 | Livro 100% íntegro: depois da PRIMEIRA gravação a faixa global "ATENÇÃO — REVISÃO DO LIVRO-CAIXA" aparece em todas as telas e permanece depois de recarregar (a existência de cópia por operação conta … | REPROVADO | **AMARELO** | Sonda em file://: antes de gravar = sem faixa; depois de 1 lançamento = faixa em início, painel, contabilidade, livro e backup; após recarregar a faixa continua ("1 cópia(s) local(is) de operações, fora do backup principal"). Não há como dispensá-la. Risco: alarme permanente, o usuário passa a ignorar avisos reais. |

### J. Restauração, mesclagem, formatos, compatibilidade com a 6.1 DEV, pagamentos e evoluções

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| C-90a | Restaurar backup com ID numérico (restaurador estrito, pendente A5): recusa sem alterar nenhum dado atual | APROVADO | **VERDE** | livro intacto=true; cadastro intacto=true; msg="Backup não restaurado: Lançamentos bancários inválidos." |
| C-90b | Restaurar backup com banco antigo (restaurador estrito, pendente A5): recusa sem alterar nenhum dado atual | APROVADO | **VERDE** | livro intacto=true; cadastro intacto=true; msg="Backup não restaurado: Lançamentos bancários inválidos." |
| C-91 | Backup no formato 6.1 (6 campos, v2) é restaurado normalmente pela dev.3 | APROVADO | **VERDE** | ledger=["Restaurado ficticio"] |
| B-90 | 6.1 DEV lê o livro da dev.3 (com registro antigo e ID numérico) e grava sem erro; todas as chaves novas (-prev, quarentena, revisão, cópia por operação) permanecem intactas | APROVADO | **VERDE** | linhas vistas=4; após novo=5; chaves novas intactas=true; erros=0 |
| B-91 | Backup principal gerado pela dev.3 (bk_c01.json) é restaurável na 6.1 DEV | APROVADO | **VERDE** | lançamentos restaurados=3/3; formato=manfrin-arnez-backup v2; campos=format,version,createdAt,care,ledger,rateSettings |
| B-91b | Backup principal gerado pela dev.3 (bk_c14.json) é restaurável na 6.1 DEV | APROVADO | **VERDE** | lançamentos restaurados=3/3; formato=manfrin-arnez-backup v2; campos=format,version,createdAt,care,ledger,rateSettings |
| B-103 | Faixa: botão "Abrir Conciliação" leva à tela do livro-caixa | APROVADO | **VERDE** | ledger visível=true; dash visível=false; item de menu ativo=ledger |
| B-77 | AJ-7: depois de falha por falta de espaço, uma exclusão bem-sucedida limpa a mensagem de erro antiga | APROVADO | **VERDE** | msg da falha="Gravação bloqueada: não foi possível proteger a operação com"; msg após excluir="" — Critério textual obsoleto (a mensagem de falha mudou para "Gravação bloqueada..."); substância verificada: depois da exclusão bem-sucedida a mensagem antiga some ("msg após excluir" vazio). |
| B-78 | Faixa: "Baixar original bruto" em estado de quarentena devolve o texto armazenado exato (inclui a linha rejeitada) | APROVADO | **VERDE** | idêntico=true; arquivo=MA62-DEV3-Livro-Caixa-Original-BRUTO.json |
| B-81 | Download individual da quarentena devolve o corpo exato; conteúdo malicioso de linha rejeitada não executa nem aparece como HTML | APROVADO | **VERDE** | download=true; idêntico ao armazenado=true; window.__x=undefined; <img> injetadas=0; erros=0 |
| B-80 | Falha ao gravar a quarentena: livro-caixa bloqueado, original intacto, nada gravado | APROVADO | **VERDE** | texto idêntico=true; aviso="LIVRO-CAIXA BLOQUEADOLinhas não reconhecidas, mas não foi possível proteger a quarentena. Gravação bloqueada"; msg ao adicionar="Gravação BLOQUEADA para proteger o livro-caixa original. Linhas não re"; erros=0 |
| B-110 | Pagamentos: registrar pagamento de paciente fictício grava no cadastro | APROVADO | **VERDE** | paciente escolhido="Paciente Fictício 00001 · CPF fictício · (telefone fictício)"; registros 121→122; valor gravado=12345; msg="Pagamento salvo para Paciente Fictício 00001. Já aparece na relação do" |
| B-111 | Contabilidade: o pagamento aparece no mês e o CSV exportado o contém | APROVADO | **VERDE** | na tela=true; CSV=true; contém=true; linhas CSV=18 |
| B-112 | Pagamento persiste após recarregar | APROVADO | **VERDE** | registros=122 |
| B-113 | Evoluções: biblioteca de modelos (canal, coroa, implante, placa) carrega texto para todas as opções; o rascunho por paciente segue preservado e oculto | APROVADO | **VERDE** | grupos=Canal:3 etapas/1232 car.; Coroa:2 etapas/813 car.; Implante:2 etapas/1204 car.; Placa de bruxismo:3 etapas/565 car.; rascunho por paciente oculto=true |
| B-114 | Backup geral com livro íntegro inclui o pagamento novo | APROVADO | **VERDE** | pagamentos no backup=122; evoluções=0 |
| B-115 | Console sem erros (pagamentos, contabilidade, evoluções) | APROVADO | **VERDE** | erros=0  |
| B-116 | Livro-caixa bloqueado NÃO impede registrar pagamento no cadastro; texto do livro segue intacto | APROVADO | **VERDE** | registros 121→122; livro intacto=true |
| B-117 | Livro-caixa bloqueado não afeta a biblioteca de modelos de evolução | APROVADO | **VERDE** | texto do modelo=1232 caracteres |
| B-119 | Backup antigo com um registro legado (banco "Itau"): a restauração é RECUSADA sem alterar nada (limitação que o A5 precisa tratar) | REPROVADO | **AMARELO** | msg="Backup não restaurado: Lançamentos bancários inválidos."; livro intacto=true. Consequência: os registros que a leitura nova preserva e a 6.1 exportava não podem ser restaurados por backup — Limitação declarada (A5): a recusa é segura (nada é alterado, C-90b), mas backups antigos com bancos fora do padrão ainda não podem se… |
| B-120 | Mesclagem do mesmo backup antigo: os dados entram (incluindo o legado), mas a tela só atualiza ao recarregar (A4) | APROVADO | **VERDE** | lançamentos no armazenamento=2; legado entrou=true; snapshot ANTES-MESCLAR baixado=true |
| B-121 | Após recarregar, o legado mesclado aparece marcado e a faixa avisa | APROVADO | **VERDE** | linhas=2/2; faixa="ATENÇÃO — REVISÃO DO LIVRO-CAIXA1 lançamento(s) antigos fora do padrão atual permanecem visíveis, preservados e marca" |
| B-118 | Backup no formato 6.1 (paciente, pagamento, evolução, livro) restaura corretamente na dev.2: todos os itens do backup presentes e idênticos | APROVADO | **VERDE** | paciente presente=true; pagamento "Antigo A" presente=true; evolução presente=true; livro idêntico=true. Observação: o app reinjeta 4 registros "DADO FICTÍCIO DE DESENVOLVIMENTO" depois de recarregar (mergeCodental; idêntico na 6.1 DEV) |
| B-123 | Restaurar e recarregar NÃO reproduz fielmente o backup: o app mescla dados embutidos (mergeCodental) por cima do que foi restaurado (pré-existente, igual na 6.1 DEV; entra no A5) | REPROVADO | **AMARELO** | pacientes=5 e pagamentos=5 depois de restaurar um backup com 1 e 1; os extras vêm de dados embutidos da cópia. Na versão real o mesmo mecanismo reinjetaria o feed embutido |
| B-122 | Depois de restaurar, um pagamento novo convive com o pagamento e a evolução do backup; o backup seguinte leva os três | APROVADO | **VERDE** | paciente escolhido="Paciente Fictício 00001 · CPF fictício · (00"; pagamento novo=true; pagamento restaurado=true; evolução restaurada=true; total de pagamentos=6 |

### K. Isolamento e demais módulos (Central Sanitária, Academia, Laboratório, simulador, 18 telas)

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| C-95 | Isolamento: adicionar, arquivar quarentena, backup, cópia bruta, restauração e localStorage.clear() não alteram nenhuma das 6 chaves reais sentinelas nem criam chaves fora do prefixo | APROVADO | **VERDE** | chaves reais antes/depois iguais=true; n=6; novas fora do prefixo=0 |
| C-96 | Navegação: todas as páginas abrem sem erro de execução | APROVADO | **VERDE** | páginas=18; não abriram=[]; erros=[] |
| SMK-01 | Todas as páginas abrem e têm conteúdo | APROVADO | **VERDE** | 18 páginas: patients, quick, accounting, notes, backup, sim, dash, ledger, sources, tcle, ma55-cost, ma55-materials, ma55-academy, ma55-training, ma55-contador, ma56-home, ma56-project, ma61-sanitary |
| SMK-02 | Sem erros de console/pageerror na carga | APROVADO | **VERDE** | erros=0  |
| ISO-01 | Chaves reais plantadas (7) permanecem byte a byte iguais após fluxo completo no DEV | APROVADO | **VERDE** | alteradas=0 ; chaves gravadas pelo app (prefixadas)=ma-care-v2,ma61-sanitary-checklist-v1 |
| ISO-02 | App não cria chaves novas fora do prefixo | APROVADO | **VERDE** | chaves fora do prefixo e fora das sentinelas=0 |
| ISO-03 | App não lê as chaves reais (sentinelas não aparecem na interface/estado) | APROVADO | **VERDE** | sentinela visível=false; care sentinela lida=false; localStorage.length (visão do app)=2 |
| ISO-04 | localStorage.clear() / removeItem() dentro do DEV não apaga chaves reais | APROVADO | **VERDE** | chaves reais perdidas/alteradas=0; visão do app após clear length=0 |
| MOD-FIN | Financeiro: dashboard, contabilidade, conciliação, lançamento e exportação CSV | APROVADO | **VERDE** | texto dash=2877 acct=5393; lançamentos gravados=1; CSV baixado contém o lançamento=true (﻿id;data;banco;descricao;valor;categoria) |
| MOD-SIM | Simulador: entradas recalculam resultado; tabela de taxas 1x–10x; bloco ma57 presente | APROVADO | **VERDE** | resultado muda ao editar=true; campos de taxa=10; ma57=true |
| MOD-PAC | Pacientes: lista, busca e cadastro persistido | APROVADO | **VERDE** | pacientes antes=4896, depois=4897; novo paciente gravado=true |
| MOD-ACAD | Academia/POPs, Laboratório Digital (maquiagem 5.8, oficina 5.9, lavagem/jateamento 6.0) e manual Exocad embutido | APROVADO | **VERDE** | {"studio":true,"oficina":true,"wash":true,"studioSteps":84,"workCards":10,"washStages":6,"blastTab":true,"exocadPdf":true,"exocadLen":12208,"docBtns":[]} |
| MOD-SAN | Central Sanitária presente e renderizada | APROVADO | **VERDE** | grupos renderizados=8 |
| QUOTA-01 | Cota saturada: cadastro de paciente falha e o usuário é avisado? | APROVADO | **VERDE** | armazenamento saturado com 25 blocos de preenchimento; paciente gravado=false; mensagem na tela="Não foi possível salvar"; dado anterior preservado (4896→4896 pacientes) |
| SMK-03 | Sem erros de console após uso dos módulos | APROVADO | **VERDE** | erros=0  |
| SAN-01 | 8 frentes e 42 subtópicos renderizados | APROVADO | **VERDE** | grupos=8; subtópicos=42; por frente=6+5+6+7+4+5+4+5; painel="8 frentes / 42 subtópicos" |
| SAN-02 | Contadores do semáforo somam 42 e coincidem com a lista | APROVADO | **VERDE** | verde=4 amarelo=29 vermelho=9; luzes das frentes=VERMELHO,VERMELHO,AMARELO,VERMELHO,AMARELO,AMARELO,VERMELHO,VERMELHO |
| SAN-03 | Cor de cada subtópico no DOM = contadores | APROVADO | **VERDE** | DOM {"ok":4,"warn":29,"bad":9} vs painel 4/29/9 |
| SAN-04 | Marcar VERDE sem evidência é bloqueado | APROVADO | **VERDE** | mensagem="Para marcar verde, preencha primeiro a evidência de "Testes biológicos semanais""; cor do item=warn |
| SAN-05 | Semáforo da frente: todos verdes→VERDE; um vermelho→VERMELHO; sem vermelho e nem todos verdes→AMARELO | APROVADO | **VERDE** | sequência observada: VERDE → VERMELHO → AMARELO |
| SAN-06 | Estados, evidências e luzes persistem após recarregar a página | APROVADO | **VERDE** | antes 9/25/8 → depois 9/25/8; JSON idêntico=true |
| SAN-07 | Filtros por semáforo, frente e busca | APROVADO | **VERDE** | filtro vermelho=8 (esperado 8); frente PGRSS=4 (esperado 4); busca "autoclave"=8 |
| SAN-08 | Exportação do checklist (formato, versão, dados) | APROVADO | **VERDE** | format=manfrin-arnez-sanitary-checklist version=1; estados exportados=7; arquivo=Manfrin-Arnez-Checklist-Sanitario-6.1.json |
| SAN-09 | Importação restaura exatamente o estado exportado (ida e volta) | APROVADO | **VERDE** | estado do item alterado antes de importar=bad; após importar=(padrão); estados iguais ao exportado=true |
| SAN-10 | Importação rejeita arquivos inválidos sem alterar os dados | APROVADO | **VERDE** | formato errado:rejeitado; semáforo inválido:rejeitado; id inexistente:rejeitado; __proto__:rejeitado; versão 2:rejeitado; grande >400KB:rejeitado; poluição de protótipo: ({}).ok=undefined |
| SAN-11 | Texto com HTML/script em evidência, observação e responsável não executa (XSS armazenado) | APROVADO | **VERDE** | window.__xss=undefined; <img> injetadas=0; <script> injetados=0; item encontrado pela busca=1 |
| SAN-12 | Links externos da Central usam noopener/noreferrer | APROVADO | **VERDE** | links=2 |
| SAN-13 | Console sem erros durante uso do checklist | APROVADO | **VERDE** | erros=0  |
| BKP-01 | Backup geral: formato manfrin-arnez-backup v2 com care, ledger e rateSettings | APROVADO | **VERDE** | campos de topo=[format, version, createdAt, care, ledger, rateSettings]; pacientes=4896; lançamentos=2; arquivo=Manfrin-Arnez-backup-PRINCIPAL-2026-10-11.json |
| BKP-03 | Backup com campos extras desconhecidos (academy, sanitary, meta) é aceito e os extras são ignorados sem apagar nada | APROVADO | **VERDE** | ledger restaurado=[Restaurado ficticio]; Academia e Sanitário intactos (hash)=true; erros de console=0; diálogos=Restaurar 1 pacientes, 0 pagamentos e 0 evoluções? |
| BKP-04 | Mesclar o mesmo backup duas vezes não duplica lançamentos nem pacientes | APROVADO | **VERDE** | lançamentos após 1ª=3, após 2ª=3 (ids únicos=3); pacientes 4897→4897 |
| BKP-06 | Backup da Academia (5.5): ida e volta | APROVADO | **VERDE** | formato=manfrin-arnez-academy-backup; mensal original=111 → alterado=5 → após importar=111 |
| BKP-06b | Importação da Academia rejeita arquivo inválido sem alterar dados | APROVADO | **VERDE** | versão 9 / arrays ausentes |
| BKP-07 | Checklist 5.6 (Central de Desenvolvimento): ida e volta | APROVADO | **VERDE** | formato=manfrin-arnez-ma56-checklist; 42 itens; estados iguais após importar=true |

### L. Regressão herdada: faixa global e quarentena

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| B-33 | AJ-3: texto da Visão financeira igual ao da 6.1 (fora a faixa) | APROVADO | **VERDE** | (informativo) 6.1 vs dev.2 diferem=false |
| B-20-bloq | AJ-2: faixa de aviso visível em TODAS as telas do menu — estado: ilegível (JSON truncado) | APROVADO | **VERDE** | telas do menu (18): ma56-home,dash,quick,accounting,ma55-cost,sim,ledger,ma55-contador,sources,patients,notes,tcle,ma55-academy,ma55-training,ma55-materials,ma61-sanitary,ma56-project,backup; sem faixa visível em: [nenhuma]; altura=128px; texto="LIVRO-CAIXA BLOQUEADOO JSON salvo está ilegível. Texto original preservado. Não cad… |
| B-21 | AJ-2: no celular (390x760) a faixa fixa não ocupa mais de 40% da altura da tela | APROVADO | **VERDE** | altura da faixa=167px de 760 (22%) |
| B-20-quar | AJ-2: faixa de aviso visível em TODAS as telas do menu — estado: quarentena (linha ilegível) + válidas | APROVADO | **VERDE** | telas do menu (18): ma56-home,dash,quick,accounting,ma55-cost,sim,ledger,ma55-contador,sources,patients,notes,tcle,ma55-academy,ma55-training,ma55-materials,ma61-sanitary,ma56-project,backup; sem faixa visível em: [nenhuma]; altura=169px; texto="ATENÇÃO — REVISÃO DO LIVRO-CAIXA1 linha(s) rejeitada(s) na leitura atual, preservad… |
| B-20-leg | AJ-2: faixa de aviso visível em TODAS as telas do menu — estado: registro legado (banco fora do padrão) | APROVADO | **VERDE** | telas do menu (18): ma56-home,dash,quick,accounting,ma55-cost,sim,ledger,ma55-contador,sources,patients,notes,tcle,ma55-academy,ma55-training,ma55-materials,ma61-sanitary,ma56-project,backup; sem faixa visível em: [nenhuma]; altura=128px; texto="ATENÇÃO — REVISÃO DO LIVRO-CAIXA1 lançamento(s) antigos fora do padrão atual perman… |
| B-20-qold | AJ-2: faixa de aviso visível em TODAS as telas do menu — estado: quarentena antiga (chave de outra sessão) e livro íntegro | APROVADO | **VERDE** | telas do menu (18): ma56-home,dash,quick,accounting,ma55-cost,sim,ledger,ma55-contador,sources,patients,notes,tcle,ma55-academy,ma55-training,ma55-materials,ma61-sanitary,ma56-project,backup; sem faixa visível em: [nenhuma]; altura=169px; texto="ATENÇÃO — REVISÃO DO LIVRO-CAIXA1 quarentena(s) ativa(s): revise e guarde uma cópia… |
| B-23 | Sem risco: livro íntegro não mostra faixa (sem falso alarme) | APROVADO | **VERDE** | telas com faixa: [] |
| B-50 | AJ-4: 4 aberturas sem gravar → apenas 1 chave de quarentena | APROVADO | **VERDE** | chaves=1 (ma-ledger-v1-rejeitados-20261011230724) |
| B-51 | AJ-4: livro-caixa original intacto após 4 aberturas | APROVADO | **VERDE** | intacto=true; prev criado=false |
| B-52 | AJ-4: conteúdo diferente gera nova chave sem apagar a antiga | APROVADO | **VERDE** | chaves=2 |
| B-53 | AJ-5: após gravar e recarregar a faixa continua listando as quarentenas | APROVADO | **VERDE** | faixa=ATENÇÃO — REVISÃO DO LIVRO-CAIXA2 quarentena(s) ativa(s): revise e guarde uma cópia separada. 1 cópia(s) local(is) de operações, fora do backup principal.Abrir ConciliaçãoBaixar original brutoRevisar e baixar arquivos em quarentena (2)1. ma-ledger-v1-rejeit |
| B-54 | AJ-5: lista de quarentenas por chave e download devolve o corpo exato guardado | APROVADO | **VERDE** | itens=2/2; exemplo="1. ma-ledger-v1-rejeitados-20261011230724 — ATIVA · 1 linha(s)"; corpo idêntico=true |
| B-55 | AJ-5: recarregar não apaga nem altera nenhuma quarentena | APROVADO | **VERDE** | chaves=2 |
| B-56 | AJ-4: chaves duplicadas herdadas da dev.1 são mantidas (sem apagar) e não se cria uma quarta | APROVADO | **VERDE** | chaves=4 (a nova linha ruim {foo:1} gera corpo igual ao de index 4, diferente do semeado index 1) |
| B-57 | AJ-5: quarentena com conteúdo não reconhecido é listada sem quebrar | APROVADO | **VERDE** | faixa="ATENÇÃO — REVISÃO DO LIVRO-CAIXA1 quarentena(s) ativa(s): revise e guarde uma cópia separada.Abrir ConciliaçãoBaixar original brutoRevisar e baixar arquivos em quarentena (1)1. ma-ledger-v1-rejeita"; erros=0 — Regex do meu critério esperava "1 arquivo(s)"; o texto agora é "1 quarentena(s) ativa(s)". Substância: listada s… |
| B-59 | Muitas quarentenas (60): faixa continua compacta (detalhes recolhidos) | APROVADO | **VERDE** | altura=169px; texto="ATENÇÃO — REVISÃO DO LIVRO-CAIXA60 quarentena(s) ativa(s): revise e guarde uma cópia separada.Abrir ConciliaçãoBaixar" |
| B-58r | Isolamento (reconferência): varredura de quarentenas conta só a chave do sandbox; 6 sentinelas reais (inclusive quarentena real) intactas | APROVADO | **VERDE** | arquivos contados=undefined (esperado 1); sentinelas intactas=true; chaves reais=6 — Faixa mostra "1 quarentena(s) ativa(s)" (só a do sandbox); sentinelas reais intactas=true, 6 chaves (regex antigo procurava outro texto). Reafirmado por C-95. |
| B-22r | AJ-2 (reconferência): faixa é sticky e permanece visível ao rolar; no DEV a barra vermelha de ambiente cobre as primeiras linhas | APROVADO | **VERDE** | position=sticky; top=0px; altura=169px; parte inferior da faixa visível=true; topo coberto por="AMBIENTE DEV — PACIENTES E FINANÇAS F"; barra DEV=nullpx (existe só na cópia DEV) |

### M. Regressão herdada: suíte A1 da dev.1

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| A1-80 | 6.1 anterior lê o livro-caixa gravado pela 6.2-dev.1 e ignora as chaves extras | APROVADO | **VERDE** | linhas vistas=2; após novo lançamento=3; chaves extras intactas=true |
| A1-81 | Backup geral gerado pela 6.2-dev.1 é restaurável na 6.1 anterior | APROVADO | **VERDE** | formato=manfrin-arnez-backup v2; lançamentos no backup=2, após restaurar=2; campos de topo=[format, version, createdAt, care, ledger, rateSettings] |
| A1-01 | Linha inválida entre válidas: válidas visíveis, original intacto, rejeitada em quarentena | APROVADO | **VERDE** | linhas exibidas=3 (esperado 3); ma-ledger-v1 idêntico ao semeado=true; chaves de quarentena=1; linhas rejeitadas=1 (posição 3, motivo "Linha não pôde ser lida com segurança (ID, data ou"); chave prev ainda ausente=true |
| A1-02 | Aviso de quarentena visível na página do livro-caixa | APROVADO | **VERDE** | aviso="ATENÇÃO — REVISÃO DO LIVRO-CAIXA1 linha(s) rejeitada(s) na leitura atual, preservadas separadamente. 1 quarentena(s) ativa(s): revise e g"; visível=true |
| A1-03 | Aviso aparece também nas telas que usam o livro-caixa (início, Visão financeira, Contabilidade, Relatório do contador) | APROVADO | **VERDE** | visível em: {"ma56-home":true,"dash":true,"accounting":true,"ma55-contador":true} → o aviso só existe dentro da Conciliação; quem abre o início ou o relatório do contador não vê o alerta |
| A1-04 | Novo lançamento com quarentena: válidas + novo gravadas, inválida fora do principal | APROVADO | **VERDE** | principal=4 linhas [Lanc ficticio 1; Lanc ficticio 2; Lanc ficticio 3; Novo A1 s1]; mensagem="Lançamento salvo neste navegador DEV." |
| A1-06 | Quarentena preservada após a gravação (mesmo conteúdo, sem duplicar) | APROVADO | **VERDE** | chaves de quarentena=1; conteúdo inalterado=true |
| A1-08 | Após recarregar: dados persistem, sem nova quarentena, aviso some | APROVADO | **VERDE** | principal inalterado=true; chaves de quarentena=1; aviso=presente → a linha rejeitada só existe agora na chave de quarentena e na cópia prev, sem nenhum aviso ou tela para revisá-la — Faixa continua visível depois de recarregar (AJ-5 corrigido na dev.2); critério original era da dev.1. |
| A1-09 | A quarentena continua acessível ao usuário após recarregar (tela ou botão para revisar/recuperar) | APROVADO | **VERDE** | Depois da primeira gravação e do reload não existe aviso, botão de download nem tela de revisão; a recuperação depende de abrir o armazenamento do navegador manualmente. |
| A1-11 | Isolamento: 6 chaves reais fictícias (incl. ma-ledger-v1-prev e quarentena sentinelas) intactas e nenhuma chave nova fora do prefixo | APROVADO | **VERDE** | chaves reais antes=6, depois=6; alteradas=0; o app leu o prev sentinela real? false |
| A1-12 | Erros de console no cenário | APROVADO | **VERDE** | erros=0 ; carga=12285 ms |
| A1-20 | JSON truncado: bloqueio, aviso e texto original preservado ao abrir | APROVADO | **VERDE** | texto idêntico=true; aviso="LIVRO-CAIXA BLOQUEADOO JSON salvo está ilegível. Texto original preservado. Não cadastre nem importe novas t"; prev/quarentena criados=false/0 |
| A1-21 | JSON truncado: tentativa de novo lançamento é recusada, com mensagem, sem tocar no armazenamento | APROVADO | **VERDE** | texto idêntico=true; mensagem="Gravação BLOQUEADA para proteger o livro-caixa original. O JSON salvo está ilegível. Texto original "; linhas exibidas=0 |
| A1-22 | JSON truncado: importação de CSV é bloqueada | APROVADO | **VERDE** | texto idêntico=true; linhas exibidas=0; mensagem="Gravação BLOQUEADA para proteger o livro-caixa original. O JSON salvo está ilegível. Texto original " |
| A1-26 | Recarga: continua bloqueado, texto intacto, sem criar prev nem quarentena | APROVADO | **VERDE** | texto idêntico=true; aviso presente=true |
| A1-27 | Erros de console (JSON truncado) | APROVADO | **VERDE** | erros=0  |
| A1-28 | Objeto no lugar de lista: bloqueado, texto preservado | APROVADO | **VERDE** | texto idêntico=true; mensagem="Gravação BLOQUEADA para proteger o livro-caixa original. O conteúdo salvo não é " |
| A1-29a | Armazenamento contendo JSON null: não é sobrescrito sem aviso | APROVADO | **VERDE** | texto idêntico=true; mensagem="Gravação BLOQUEADA para proteger o livro-caixa original. O conteúdo salvo não é " |
| A1-29b | Armazenamento contendo texto vazio: não é sobrescrito sem aviso | APROVADO | **VERDE** | texto idêntico=true; mensagem="Gravação BLOQUEADA para proteger o livro-caixa original. O JSON salvo está ilegí" |
| A1-30 | Livro-caixa inexistente: lançamentos novos gravam normalmente, sem aviso | APROVADO | **VERDE** | sem chave inicial=true; aviso=não; gravados=1 [Normal 1:10000]; msg="Lançamento salvo neste navegador DEV." |
| A1-32 | Fluxos normais: alterar categoria, importar CSV, excluir, exportar CSV | APROVADO | **VERDE** | categoria gravada=true; CSV importado=2/2 (msg "2 importados; 0 IDs já existentes ignorados. Confira as clas"); após exclusão=2 linhas; CSV exportado contém importado=true |
| A1-33 | Persistência após recarregar e reflexo na Visão financeira | APROVADO | **VERDE** | principal idêntico após reload=true; painel financeiro="Consolidação dos lançamentos cadastrados Todos os períodos cadastrados · base parcial, sem os totais" |
| A1-34 | Erros de console no uso normal | APROVADO | **VERDE** | erros=0  |
| A1-35 | Compatibilidade: linhas que o carregador antigo exibia e a leitura nova manda para quarentena | APROVADO | **VERDE** | 0 de 12 casos mudaram de comportamento: . Detalhe: válida: aceita pelo carregador antigo → visível \| banco fora de Cora/Sicredi: aceita pelo carregador antigo → visível \| valor zero: aceita pelo carregador antigo → visível \| valor fracionário (centavos não inteiros): aceita pelo carregador antigo → visível \| categoria desco… |
| A1-36 | Linhas válidas com campo extra desconhecido mantêm o campo na regravação | APROVADO | **VERDE** | campo "nota" preservado=true; linhas visíveis antes=12, gravadas depois=13 |
| A1-37 | Recarregar várias vezes sem gravar não deve multiplicar chaves de quarentena | APROVADO | **VERDE** | 3 aberturas sem gravar → 1 chaves de quarentena idênticas (ma-ledger-v1-rejeitados-20261011222632) |
| A1-40 | Duas abas abertas: a aba desatualizada NÃO sobrescreve os lançamentos da outra | APROVADO | **VERDE** | sequência A1, B1, A2 → principal=[Aba A lanc 1; Aba A lanc 2]; aba B recusou gravar (msg "Alteração externa detectada; nada foi gravado."); aviso na aba B="LIVRO-CAIXA BLOQUEADOOs lançamentos foram modificados por outra aba ou módulo." |
| A1-41 | Duas abas: o lançamento digitado na aba B é perdido ou fica visível ao usuário? | APROVADO | **VERDE** | A aba B informa "Alteração externa detectada; nada foi gravado.", mas o lançamento permanece apenas no formulário/na memória da aba e o livro-caixa da aba fica bloqueado até recarregar (recarregar descarta o que foi digitado). Linhas exibidas na aba B=0 |
| A1-42 | Duas abas: após recarregar, a aba B enxerga os dados da A e volta a gravar | APROVADO | **VERDE** | linhas vistas após recarregar=2; principal final=[Aba A lanc 1; Aba A lanc 2; Aba B lanc 2] |
| A1-43 | Duas abas: aba A, agora desatualizada, também é impedida de sobrescrever | APROVADO | **VERDE** | principal=[Aba A lanc 1; Aba A lanc 2; Aba B lanc 2]; mensagem aba A="Alteração externa detectada; nada foi gravado." |
| A1-44 | P0-3 com a A1: a mesclagem deixa de ser apagada pelo próximo lançamento | APROVADO | **VERDE** | após mesclar, principal=[Lanc ficticio 1; Lanc ficticio 2; Do backup antigo A; Do backup antigo B; Cora:OLDBAD], linhas exibidas=2; novo lançamento → principal=[Lanc ficticio 1; Lanc ficticio 2; Do backup antigo A; Do backup antigo B; Cora:OLDBAD]; mensagem="Alteração externa detectada; nada foi gravado." |
| A1-45 | P0-3 com a A1: a tela mostra o que foi mesclado sem precisar recarregar | REPROVADO | **AMARELO** | linhas exibidas logo após mesclar=2 (esperado 4 válidas ou 5 com a inválida); o novo lançamento foi RECUSADO pela proteção (dados preservados, mas a mesclagem continua sem refletir na tela — correção A4 pendente) — A4 (inalterado): a tela só mostra a mesclagem depois de recarregar. |
| A1-46 | Após recarregar, linha inválida vinda da mesclagem vai à quarentena e as válidas aparecem | APROVADO | **VERDE** | linhas exibidas=2; quarentenas=0; aviso="undefined" — Falha era de temporização do meu roteiro (leitura antes de a página recarregar). Sonda corrigida em file://: depois do recarregamento, 4 linhas exibidas, 1 quarentena ativa e faixa visível (linha inválida vinda da mesclagem foi para a quarentena). |
| A1-48 | Restauração + próxima gravação: o estado anterior à restauração continua recuperável? | REPROVADO | **VERMELHO** | depois de restaurar e gravar, nenhum valor armazenado contém o lançamento da sessão 1 = true; prev agora guarda o estado restaurado, não o anterior. A proteção da A1 NÃO cobre a restauração (P1-7 segue VERMELHO, como o relatório declara). — A5 (inalterado): restaurar e gravar descarta o estado anterior à restauração. |
| A1-56 | Cota (nem a cópia prev cabe): tela e armazenamento ficam coerentes após cada operação e nada é perdido sem pedido | APROVADO | **VERDE** | adicionar: tela=3/gravado=3 ("Gravação bloqueada: não foi possível proteger a operação com") \| categoria: tela=Receita/gravado=Receita ("Gravação bloqueada: não foi possível proteger a operação com cópia local. Original intacto. Baixe e verifique uma cópia externa.") \| excluir: tela=3/gravado=3 ("Gravação bloqueada: não foi p… |
| A1-58 | Erros de console sob cota (prev-nao-cabe) | APROVADO | **VERDE** | erros=0 |
| A1-57 | Cota (a cópia prev cabe, o crescimento do principal não): tela e armazenamento ficam coerentes após cada operação e nada é perdido sem pedido | APROVADO | **VERDE** | adicionar: tela=3/gravado=3 ("Gravação bloqueada: não foi possível proteger a operação com") \| categoria: tela=Receita/gravado=Receita ("Gravação bloqueada: não foi possível proteger a operação com cópia local. Original intacto. Baixe e verifique uma cópia externa.") \| excluir: tela=3/gravado=3 ("Gravação bloqueada: não foi p… |
| A1-59 | Erros de console sob cota (prev-cabe-principal-cresce-falha) | APROVADO | **VERDE** | erros=0 |
| A1-61 | Volume: 17000 lançamentos (2312981 caracteres): leitura, validação e gravação com cópia prev | APROVADO | **VERDE** | validação em memória de 17000 linhas=22 ms (17000 válidas); carga total da página=12977 ms; novo lançamento gravado=false; prev presente=false; mensagem="Gravação bloqueada: não foi possível proteger a operação com cópia local. Original intacto. Baixe e "; o dobro de espaço da cópia prev somado ao cadastro estoura a cota: a gra… |
| A1-72 | Exceção ao ler o armazenamento (acesso negado): bloqueia gravações e preserva o conteúdo | APROVADO | **VERDE** | texto idêntico=true; aviso="LIVRO-CAIXA BLOQUEADONão foi possível acessar o armazenamento. Nenhuma alteração será gravada.Abri"; mensagem="Gravação BLOQUEADA para proteger o livro-caixa original. Não foi possí"; erros=0 |

### N. Defeitos pré-existentes, fora do escopo da A1.2

| ID | Verificação | Resultado | Sinal | Evidência |
|---|---|---|---|---|
| PERF-01 | Tempo de carga DEV (4,6k+4,9k fictícios) no Chromium headless | REPROVADO | **AMARELO** | carga=12042 ms (limite de aceitação 5000 ms) — P0-4 (inalterado): carga ~12-13 s em Chromium headless, igual à dev.2. |
| ISO-05 | Limite: isolamento é por prefixo na MESMA origem file:// (cota e acesso por iframe/console não isolados) | APROVADO | **AMARELO** | um iframe about:blank enxerga 7 chaves reais+prefixadas; sessionStorage/indexedDB não isolados (mas o código não os usa: 0 ocorrências) — Limite documentado do isolamento por prefixo (mesma origem file://); o próprio Codex declara o mesmo. |
| P1-0 | Academia 5.5: dado de versão desconhecida preservado ao primeiro salvamento? | REPROVADO | **VERMELHO** | salvamento ocorreu=true; marcador original SOBRESCRITO sem aviso nem cópia (VERMELHO); msg= — Fora do escopo A1.2; não corrigido (declarado pelo Codex). |
| P0-2 | Backup com leitura do cadastro em erro: exporta os dados armazenados (e não o seed embutido)? | APROVADO | **VERDE** | arquivo gerado=false; care armazenado tinha 1 paciente (versão desconhecida); backup baixado contém undefined pacientes e marcador armazenado AUSENTE; aviso na tela="BACKUP PRINCIPAL RECUSADO: cadastro ilegível ou armazenamento indisponível. Baix"; chave original intacta após exportar=true → backup traz o seed embutido e dá fal… |
| P1-7a | Restauração substitui os dados (comportamento funcional) | APROVADO | **VERDE** | ledger após restaurar=[Restaurado ficticio]; chaves=clear,getItem,key,length,removeItem,setItem |
| P1-7b | Restauração preserva uma cópia automática dos dados anteriores? | REPROVADO | **VERMELHO** | chaves reais antes=2, depois=3; novas chaves=[P:ma-installment-rates-v1]; algum valor armazenado ainda contém o lançamento anterior=false → dados anteriores irrecuperáveis após restaurar (VERMELHO) — A5 (inalterado). |
| P0-4 | Desempenho: mergeCodental (executa em toda abertura) com dados DEV | REPROVADO | **AMARELO** | mergeCodental isolado=11340 ms (seed 4621 + feed 4907 → 4892 pacientes); carga total da página=11855 ms — P0-4 (inalterado). |
| BKP-02 | Backup geral cobre TODOS os conjuntos de dados (Academia, checklist 5.6, Central Sanitária)? | REPROVADO | **VERMELHO** | o backup geral NÃO contém Academia/checklist 5.6/Central Sanitária mesmo existindo no armazenamento (campos extras presentes: 0) → restaurar o backup geral sozinho não recupera 3 dos 5 conjuntos; exigem backups separados (VERMELHO se o usuário confiar só no geral) — A5 (inalterado): o backup principal declara que não cobre Acad… |
| BKP-02b | Backup geral inclui as flags do app 6.1 (Banner de ambiente, versão do app)? | APROVADO | **AMARELO** | campos meta/appVersion ausentes=true → restauração não sabe a procedência do arquivo |
| BKP-05 | Restauração rejeita backups inválidos sem alterar o armazenamento | NÃO TESTADO | **AMARELO** | Script antigo desta verificação tem defeito conhecido (etapas anteriores); resultado ignorado. Código inalterado. |
| BKP-08 | Estúdio de maquiagem 5.8: exporta, mas não existe importação correspondente | APROVADO | **AMARELO** | formato exportado=manfrin-makeup-training; sem leitor no código (ver BKP-09) |
| P2-2 | CSV exportado neutraliza fórmulas (injeção de planilha) | REPROVADO | **AMARELO** | célula da descrição começa com "=": true |
| P2-3 | Excluir lançamento exige confirmação | APROVADO | **VERDE** | botão de exclusão encontrado=true; diálogos de confirmação=1; lançamentos restantes=0 |
| SEC-01 | Aberto por http em IP de rede (contexto inseguro): crypto.randomUUID disponível? | NÃO TESTADO | **AMARELO** | Script antigo desta verificação tem defeito conhecido (etapas anteriores); resultado ignorado. Código inalterado. |
| MA61-1 | Central Sanitária: dado de versão desconhecida preservado | NÃO TESTADO | **AMARELO** | Código idêntico ao da dev.2 (INT-34 e diff); defeito reproduzido em etapas anteriores e não tocado nesta entrega. Fora do escopo A1.2 (declarado pelo Codex). |
| MA61-1b | Central Sanitária: importação com versão desconhecida | NÃO TESTADO | **AMARELO** | Código idêntico ao da dev.2 (INT-34 e diff); defeito reproduzido em etapas anteriores e não tocado nesta entrega. Fora do escopo A1.2 (declarado pelo Codex). |
| P1-6 | crypto.randomUUID em contexto inseguro (http em IP de rede) | NÃO TESTADO | **AMARELO** | Código idêntico ao da dev.2 (INT-34 e diff); defeito reproduzido em etapas anteriores e não tocado nesta entrega. Fora do escopo A1.2 (declarado pelo Codex). |
| P1-3 | Duas abas fora do livro-caixa (cadastro e demais módulos) | NÃO TESTADO | **AMARELO** | Código idêntico ao da dev.2 (INT-34 e diff); defeito reproduzido em etapas anteriores e não tocado nesta entrega. Fora do escopo A1.2 (declarado pelo Codex). |

---

## Arquivos de teste

`Suite-Testes-A1.2-Livro-Caixa.zip` contém os roteiros Playwright novos (`c1` a `c8`, `b1x`, `b3x`, `b5x`, `b6x`), as bibliotecas, os roteiros herdados que reexecutei, as sondas, os geradores da matriz e deste relatório, a matriz em JSON e um LEIA-ME. As fixtures são fictícias e pequenas; os backups gerados durante os testes (que podem conter dados fictícios do DEV) não estão incluídos. Para reproduzir: `DEV_FILE=<html> node cN.js` com `NODE_PATH` apontando para o Playwright; rodar no máximo duas frentes em paralelo.
