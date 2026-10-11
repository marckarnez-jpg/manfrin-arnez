# Manfrin Arnez — 6.2 DEV.3 — A1.2

Entrega de desenvolvimento para auditoria independente. **Não liberar para uso clínico nem produção. A5 não foi iniciada.**

## Resultado da entrega

| Classificação | Resultado |
|---|---|
| ✓ CORRIGIDO E TESTADO | AJ-11, AJ-12b (revisão/arquivamento e cópia bruta independente), AJ-13, AJ-14, AJ-15, AJ-16 (leitura/totais/IDs originais) e AJ-17. Os dez cenários B solicitados foram aprovados. |
| ⚠ CORRIGIDO, MAS REQUER AUDITORIA | A1.2 precisa de auditoria independente do Claude/Gemini antes de qualquer decisão de liberação. A aprovação desta suíte não equivale a auditoria independente nem validação clínica. |
| ✗ NÃO CORRIGIDO | Defeitos preexistentes fora de A1.2, enumerados nas pendências: mesclagem/tela, versões desconhecidas nos módulos independentes, concorrência fora do livro, CSV de fórmulas e desempenho da carga. |
| ○ PENDENTE PARA A5 | Backup parcial restaurável, restauração ampliada de legados, restauração fiel, proteção pré-restauração e cobertura integral. A5 não foi implementada. |

**Execução final:** 11 grupos; **97 verificações executadas e aprovadas**, **0 reprovações**, **3 registros de pendência** (não aprovados). Comando concluído com **status 0**. Os 23 scripts também passaram na verificação sintática. Nenhum `pageerror` ocorreu nos cenários testados. Não houve teste desabilitado nem resultado de uma tentativa interrompida usado na contagem final.

## Origem, escopo e preservação

A solicitação é o texto colado fornecido pelo usuário, complementado pela confirmação do HTML correto. A auditoria do Claude foi usada como evidência técnica; suas propostas de autorizar acesso a dados reais ou iniciar A5 não foram tratadas como autorização. Não foi fornecido um relatório separado do Gemini.

DEV.2 acessada integralmente em UTF-8 antes de qualquer modificação:

- Nome: `Manfrin-Arnez-Dashboard-6.2-DEV-02-Ajustes-A1.1.html`.
- Tamanho: **4.062.900 bytes**.
- SHA-256: `f11dbe0eccce98e30545ae94297c38bf16e1f3053b94d52589a108dfd2756751`.

A DEV.2 foi preservada. O site institucional `/workspace/manfrin-arnez/manfrin-arnez.html` também foi preservado; seu SHA-256 original é `4b6789de6fdae19e79eeddd310c5f9c680fe7758438b57a38987587f74f4d8e3`. Todos os artefatos novos estão fora do checkout, em `/workspace/entregas-a1.2`. Nenhum dado real de paciente, backup real da clínica ou perfil principal do Chrome foi acessado. Nenhuma publicação, envio a outros auditores ou alteração em produção ocorreu.

## Alterações

| Ajuste | Implementação | Limite deliberado |
|---|---|---|
| AJ-11 | `ma62RequestBackup` centraliza o resultado `{ok,message,state}` nos botões de Backup e Contabilidade. Recusa aparece na tela acionada. Solicitação de download e verificação do arquivo são estados distintos. Selecionar o arquivo baixado permite comparar seu conteúdo exato com o último arquivo gerado na sessão, sem restaurar nada. | O navegador não comprova por si só a guarda duradoura ou atualidade de uma cópia. Verificar um arquivo não torna completa sua cobertura. |
| AJ-12 | Revisão/arquivamento em metadados adicionais, mantendo a chave e o conteúdo de cada quarentena intactos. Revisão se vincula ao conteúdo exato; alteração posterior reativa o risco. Quarentena arquivada não é recuperada. Com livro íntegro, a quarentena histórica revisada deixa de bloquear o backup **principal**, com nome e mensagem explícitos sobre suas omissões. Cópia BRUTA do cadastro/pagamentos/evoluções fica disponível mesmo quando o financeiro impede o backup. | Linhas atualmente rejeitadas continuam bloqueando o backup. Exportação parcial restaurável e restauração ampliada dos legados ficam para A5. Cópias BRUTAS são guarda forense, não backups aceitos pelo restaurador atual. |
| AJ-13 | A aprovação externa está vinculada ao texto atual, vale uma operação e tem estado próprio. A faixa distingue confirmação manual e verificação por leitura do arquivo. Após gravação não repete o pedido anterior; informa a proteção utilizada e necessidade de atualizar a cópia externa. | Confirmar manualmente não equivale a verificação pelo aplicativo. |
| AJ-14 | A chave `ma-ledger-v1-prev` nunca é sobrescrita ou removida. Se existir, recebe indicação de sessão/data não comprovadas. Cada operação financeira cria uma nova chave de cópia bruta com identificador de sessão/operação; cópias antigas podem ser consultadas e baixadas. | As cópias não são automaticamente restauradas nem incluídas no backup principal. Não há limpeza automática de gerações. |
| AJ-15 | Removido o limite de 900.000 caracteres. A gravação real da cópia e sua leitura de conferência decidem se a operação tem proteção local. Sem cópia local nem aprovação externa específica, recusa a gravação. Falha ao gravar o principal mantém o original e restaura o estado da interface. | Guardar todas as gerações consome cota; se não couber uma nova cópia, é preciso guardar/verificar uma cópia externa. A capacidade não é estimada por número de linhas. |
| AJ-16 | Leitura aceita IDs numéricos finitos sem convertê-los no armazenamento. Totais continuam calculados sobre os valores originais. Manipuladores usam a posição da linha para distinguir, por exemplo, `123` de `"123"`; CSV aceita os dois tipos. | Restaurador atual continua exigindo ID textual. Backup principal com ID numérico é recusado explicitamente e a cópia BRUTA permanece disponível. Ampliar esse restaurador é A5. |
| AJ-17 | Mensagens discriminam ID, data, banco, descrição, valor, categoria e sinal. Diálogo permite corrigir um campo por vez. Categoria pode ser corrigida sem exigir que todos os demais campos legados já estejam no padrão. Montante não editado e demais campos permanecem intactos. Mudança monetária mostra centavos antes/depois e exige confirmação; mudança de categoria também informa impacto nos totais. | Não há correção automática, arredondamento de valores antigos ou remoção automática de linhas. Correções podem continuar deixando outros campos pendentes. |

Os rótulos de backup foram ajustados para **principal / escopo 6.1**, sem afirmar cobertura integral. CSV e snapshot anterior à mesclagem agora avisam sobre omissões; isso não altera os formatos nem reescreve a mesclagem. A exclusão existente ganhou confirmação e usa a posição da linha, protegendo IDs numéricos de colisões.

## Contrato de armazenamento e backup

Todas as chaves abaixo continuam dentro do prefixo DEV existente `__MA_DEV61_SANDBOX__:`:

- `ma-ledger-v1`: livro atual; valores antigos não são normalizados na leitura.
- `ma-ledger-v1-prev`: preservada integralmente, sem inferir origem/data. Se não existe, não é criada; a proteção nova usa as chaves por operação. Expectativas antigas de sempre criar ou substituir `-prev` foram substituídas por testes da cópia bruta por operação.
- `ma-ledger-v1-rejeitados-*`: quarentenas originais intactas.
- `ma-ledger-v1-quarantine-review:<chave original>`: revisão com data, confirmação e conteúdo original exato. Manter os bytes na revisão permite detectar mudanças sem aceitar uma revisão para outro conteúdo; isso aumenta o uso de armazenamento.
- `ma-ledger-v1-session-prev-<sessão>-<sequência>`: cópia bruta antes da operação indicada. Data/hora da sessão e UUID fazem parte da chave. A aplicação identifica cópias da sessão atual e de outras sessões, inclusive abas concorrentes; não infere que uma cópia de outra sessão seja o estado imediatamente anterior à operação atual.

O backup principal mantém **exatamente os seis campos de topo** do formato v2 anterior: `format`, `version`, `createdAt`, `care`, `ledger`, `rateSettings`. Não foram adicionados campos de backup parcial. Pacientes, pagamentos e evoluções permanecem em `care`. Academia, checklists, quarentenas, revisões e cópias locais exigem arquivos separados; os avisos e nomes deixam isso explícito.

A cópia BRUTA do cadastro preserva o texto da chave `ma-care-v2`, inclusive se ilegível; não exporta uma base embutida como substituta. Não deve ser selecionada no restaurador de backup principal. Se a chave não existir ou estiver inacessível, o aplicativo recusa a exportação bruta, sem inventar dados.

## Validação

**Resultado final da suíte:** `resultados-testes/resultados.json` registra `scenario: "all"`, `failure: null`, 97 aprovados, 0 reprovados e 3 pendentes. O comando terminou com status 0. O SHA-256 registrado pelo runner corresponde ao HTML final. Resultados de tentativas exploratórias interrompidas ou de ajustes nos seletores dos testes não são usados como aprovação da entrega. A execução completa foi repetida sobre o arquivo final após os ajustes de identificação das cópias e de renderização das posições das linhas.

Método: HTML inteiro, servido em HTTP loopback; Chromium `/usr/bin/chromium` em contextos descartáveis; Playwright Python 1.62.0, Chromium 154.0.8037.57 e Python 3.12.14; armazenamento `localStorage` nativo. Nenhum trecho do app foi substituído por `set_content` ou armazenamento inteiramente simulado. As falhas pontuais de cota são injetadas em duas gravações específicas, preservando as demais operações nativas, e há também saturação da **cota real** do Chromium. As seis chaves sentinelas fora do prefixo têm conteúdo exclusivamente fictício.

`file://` foi tentado e recusado por `ERR_BLOCKED_BY_ADMINISTRATOR`. A política não foi desativada. Portanto esta entrega não alega validação do fluxo `file://` nesta máquina, nem em Chrome real, celular real ou navegador 6.1 não fornecido.

Verificações estáticas: os **23 scripts** extraídos passaram em `node --check`. O conteúdo desde `function syncInfo(){` até o fim do HTML permanece idêntico ao da DEV.2, incluindo modelos clínicos, módulos de Academia/Laboratório, documentos incorporados e Central Sanitária. O gerador reproduziu uma DEV.3 com o mesmo SHA-256. Os controladores usam um mapa de posições das linhas construído em tempo linear, evitando procurar cada linha repetidamente ao renderizar livros grandes.

| Cenário solicitado | Resultado | Critério |
|---|---|---|
| B-06 | ✓ APROVADO | Quarentena histórica revisada deixa de bloquear após recarga, sem apagar original; backup principal declara a omissão. |
| B-07 | ✓ APROVADO | Controle de revisão/arquivamento existe, original intacto, aviso visível de arquivamento sem recuperação. |
| B-09 | ✓ APROVADO | Banco antigo pode ser corrigido explicitamente sem excluir o lançamento. |
| B-31 | ✓ APROVADO | IDs numéricos finitos ficam na lista, sem quarentena indevida. |
| B-32 | ✓ APROVADO | Totais correspondem à agregação do contrato 6.1 sobre as mesmas linhas, sem excluir montantes numéricos. Não é comparação com um HTML 6.1 executável, que não foi fornecido. |
| B-37 | ✓ APROVADO | Categoria de legado com outro campo inválido é corrigível, preservando demais campos e valor. |
| B-67 | ✓ APROVADO | Após proteção externa e gravação, faixa deixa de repetir falta de espaço/pedido já atendido. |
| B-69 | ✓ APROVADO | `-prev` antiga continua intacta e é rotulada como anterior/de origem não comprovada. |
| B-79 | ✓ APROVADO | Depois de restaurar backup válido, quarentena histórica revisada permanece preservada e não impede novo backup principal. |
| B-100 | ✓ APROVADO | Contabilidade mostra recusa sem download e não anuncia sucesso. |

Os cenários usam novas fixtures fictícias equivalentes aos estados descritos na auditoria. Não são a suíte original de 184 verificações nem seus mesmos valores de exemplo: os scripts originais da auditoria não foram fornecidos.

A suíte também verifica JSON truncado, cadastro ilegível, arquivo externo errado, leitura da cópia exata, aprovação externa de uso único, falha na cópia/principal, cota real, 12.000 linhas, duas abas com estado desatualizado, reabertura, preservação de pacientes/pagamentos/evoluções, 18 páginas, CSV contábil, simulador, 8 frentes/42 subtópicos, exportações próprias e isolamento. Uma alteração de valor cancelada mantém o livro intacto; o teste também confere o texto da confirmação monetária. O campo de evolução por paciente já vinha oculto; a suíte preserva seu registro por backup e verifica os conteúdos existentes, sem afirmar um fluxo de digitação que a interface não oferece.

O arquivo recebido não tem uma página própria chamada Orçamentos; os cálculos existentes de preço/parcelamento foram preservados junto com todo o conteúdo original dos módulos. Não foi criado um módulo novo fora do escopo.

## Pendências e riscos conhecidos

**○ PENDENTE PARA A5:** exportação parcial restaurável; restauração de IDs numéricos e demais legados; proteção automática do estado anterior à restauração; restauração fiel sem reinjeção dos quatro registros fictícios embutidos; desenho do backup integral e compatibilidade ampliada com versões anteriores. As recusas desses fluxos são seguras, mas não constituem aprovação da funcionalidade futura.

**✗ NÃO CORRIGIDO / fora do escopo A1.2:** problemas preexistentes da mesclagem que não atualiza o livro em memória até recarregar (A4); sobrescrita de versões desconhecidas em módulos independentes; proteção de concorrência em cadastro e outros módulos; neutralização de fórmulas no CSV do livro; desempenho da carga/merge dos cadastros embutidos. Os módulos permaneceram preservados, não passaram a ter garantias novas por esta entrega.

**⚠ CORRIGIDO, MAS REQUER AUDITORIA:** alterações financeiras, arquivamento manual e estados de proteção externa precisam de revisão independente. Snapshot por operação retém gerações sem limpeza automática. O prefixo DEV separa chaves, mas compartilha origem/cota; não é uma barreira de segurança contra código da mesma origem. A detecção de aba desatualizada testada não é uma transação distribuída nem garantia de serialização de escritores simultâneos. O gerador e os testes nunca acessam perfis existentes.

Validação de compatibilidade executável 6.1 fica **PENDENTE** até que esse HTML seja fornecido. O contrato de backup v2 foi preservado e uma fixture nesse formato foi restaurada; isso não substitui a execução no leitor 6.1 original.

## Execução e arquivos

No diretório da entrega:

```bash
python3 testes_a1_2.py --dev2 /caminho/Manfrin-Arnez-Dashboard-6.2-DEV-02-Ajustes-A1.1.html
```

O argumento `--dev2` é opcional para executar os cenários; necessário para repetir a conferência de hash e invariância do original. O script inicia/encerra seu próprio servidor HTTP temporário e bloqueia acessos externos do contexto de teste. Usar Python sem `-O`. Dependências já disponíveis nesta instância: Python 3.12, pacote Playwright e Chromium. Não usar o Chrome principal nem restaurar arquivos reais.

Para reproduzir a DEV.3 a partir da DEV.2 imutável:

```bash
python3 gerar_dev3.py --source /caminho/Manfrin-Arnez-Dashboard-6.2-DEV-02-Ajustes-A1.1.html --output /caminho/Manfrin-Arnez-Dashboard-6.2-DEV-03-A1.2.html
```

O gerador exige o hash completo original e rejeita saída no mesmo caminho da DEV.2 ou com nome `manfrin-arnez.html`.

Entregas: HTML completo DEV.3; este relatório; `testes_a1_2.py`; `gerar_dev3.py`; `Comparacao-DEV2-DEV3-A1.2.diff` (diff unificado sem contexto, para não replicar megabytes de dados embutidos inalterados); `testes-execucao.log`; `resultados-testes/resultados.json`; downloads fictícios da execução; `versoes-ambiente.json`; `SHA256SUMS.txt`.

Foi salvo o campo `start_skill` no rascunho da configuração do ambiente, com diretórios, inicialização local e execução isolada dos testes. Não foi necessário `install_script`: os runtimes já estavam presentes. O site institucional foi servido em HTTP local com status 200, corpo igual ao original e título esperado. Salvar o rascunho não publica o ambiente nem a aplicação. Revisar e salvar nas configurações do ambiente e publicar **o ambiente** são ações posteriores do usuário; não autorizam produção clínica. A restauração do ambiente em uma nova tarefa não foi validada nesta sessão.

## Arquivo final

- Arquivo: `Manfrin-Arnez-Dashboard-6.2-DEV-03-A1.2.html`.
- Tamanho: **4.077.003 bytes**.
- SHA-256: `e4e4f49ca37e85cd9c83c67aa79b4e9d2fcb74b11137c387a5692ea8727bcc3f`.

Conferir também `SHA256SUMS.txt` e o hash em `resultados-testes/resultados.json`. O SHA-256 da DEV.2 e o do site institucional foram reconferidos ao concluir e permanecem idênticos aos originais. `git status --short --untracked-files=all` do repositório institucional permaneceu vazio.
