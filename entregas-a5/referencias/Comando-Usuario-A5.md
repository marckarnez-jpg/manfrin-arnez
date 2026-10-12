# PROJETO MANFRIN ARNEZ ODONTOLOGIA
## DASHBOARD 6.2 — A5: BACKUP, RESTAURAÇÃO E PROTEÇÃO INTEGRAL DOS DADOS

**MISSÃO:** Desenvolver a versão 6.2 DEV.4, implementando a etapa A5, com prioridade absoluta para evitar perda de dados clínicos, financeiros e administrativos.

Você será o programador responsável. O ChatGPT coordena o projeto, o Claude realiza os testes independentes e o Gemini poderá fazer revisões complementares.

**ARQUIVOS DE REFERÊNCIA:**
1. Entrega-Manfrin-Arnez-A1.2.zip — versão DEV.3 e testes do Codex.
2. Auditoria-Independente-A1.2-6.2-dev.3.md — relatório final do Claude.
3. Suite-Testes-A1.2-Livro-Caixa.zip — suíte independente de regressão.

Leia todos os arquivos antes de alterar o código.

### REGRAS ABSOLUTAS

1. Trabalhar exclusivamente com dados fictícios.
2. Nunca acessar pacientes reais, backups reais ou o perfil principal do Chrome.
3. Nunca modificar a DEV.3 original nem o site institucional `manfrin-arnez.html`.
4. Criar uma nova versão: `Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html`.
5. Preservar todos os módulos e recursos existentes.
6. Não publicar, instalar ou migrar para produção.
7. Não enviar dados de pacientes para servidores externos.
8. Não executar `localStorage.clear()` para liberar espaço.
9. Não apagar automaticamente cópias de segurança, quarentenas ou revisões.
10. Não apresentar uma exportação parcial como backup completo.
11. Não iniciar alterações na branch principal do GitHub; trabalhar em branch isolada, sem publicar ou mesclar sem autorização.
12. Não declarar correções aprovadas sem testes efetivamente executados.

---

## FASE 1 — CORRIGIR OS TRÊS PROBLEMAS ENCONTRADOS PELO CLAUDE

### N-1 — ARMAZENAMENTO ESGOTADO (PRIORIDADE MÁXIMA)

Problema: a DEV.3 cria uma cópia integral do livro-caixa por operação, sem mecanismo seguro de liberação de espaço.

O Claude reproduziu esgotamento de cota após aproximadamente 63 operações com 500 linhas e 21 operações com 1.500 linhas. Isso também pode bloquear pagamentos.

Implementar:

- Painel de diagnóstico do armazenamento local, com tamanho estimado das bases e cópias.
- Histórico identificável das cópias existentes: data, origem, tamanho e integridade.
- Exportação externa verificável das cópias históricas.
- Procedimento de liberação seletiva de espaço, somente após exportação comprovada e confirmação expressa do usuário.
- Política documentada de retenção, distinguindo cópias de operações, quarentenas, revisões e backups oficiais.
- Nunca remover quarentenas, revisões ou backups antigos automaticamente.
- Nunca eliminar a única cópia recuperável de um estado.
- Antes de excluir uma cópia histórica autorizada, confirmar que a exportação correspondente está íntegra e acessível.
- Se não for possível garantir recuperação segura, bloquear a limpeza e explicar o motivo.

Evitar que o crescimento ilimitado das cópias inviabilize novos pagamentos ou lançamentos.

**Não usar limpeza automática ou exclusão silenciosa como solução.**

### N-2 — BACKUP BRUTO INACESSÍVEL

Quando houver identificador numérico antigo no livro-caixa, o backup pode ser recusado sem apresentar o botão de exportação bruta.

Corrigir para que a opção de baixar o livro-caixa original esteja sempre acessível na tela de Backup, independentemente do estado da faixa global.

Preservar integralmente os registros originais.

### N-3 — FAIXA DE ALERTA PERMANENTE

Na DEV.3, a primeira operação pode acionar a faixa global de atenção permanentemente.

Separar avisos críticos de informações rotineiras.

A faixa de alerta deve aparecer diante de riscos reais: corrupção, quarentena ativa, registro inconsistente, conflito de escrita ou falha de proteção.

A simples existência de cópias históricas válidas não deve gerar alerta vermelho ou amarelo permanente.

---

## FASE 2 — BACKUP COMPLETO DO DASHBOARD

Corrigir BKP-02 e demais limitações do backup atual.

Criar um mecanismo de backup unificado que considere todas as bases persistidas relevantes do Dashboard, incluindo:

- Pacientes.
- Pagamentos e recebimentos.
- Evoluções e respectivos rascunhos persistidos.
- Livro-caixa.
- Taxas e configurações financeiras.
- Academia Manfrin Arnez.
- Materiais, Laboratório Digital e Exocad, quando houver dados locais persistidos.
- Central Sanitária: 8 frentes e 42 subtópicos.
- Checklists adicionais, inclusive checklist56 quando existente.
- Metadados necessários à restauração.
- Quarentenas, revisões e histórico de proteção, com tratamento claramente identificado.

Antes de implementar, inventariar todas as chaves `localStorage` e seus formatos reais no código DEV.

Não presumir que uma base existe apenas pelo nome de uma seção.

O backup deve informar claramente:

1. Dados incluídos.
2. Dados ausentes ou indisponíveis.
3. Dados em quarentena.
4. Dados que exigem exportação separada.
5. Versão do formato.
6. Data de criação.
7. Identificação e integridade do arquivo.

Não gerar dados artificiais para preencher lacunas.

Se algum módulo não puder ser incluído, declarar explicitamente o backup como PARCIAL e explicar como proteger o restante.

Preservar leitura compatível do formato v2 existente. Caso seja necessário um formato novo, implementar versionamento explícito, importação dos formatos anteriores e testes de migração, sem sobrescrever backups antigos.

---

## FASE 3 — RESTAURAÇÃO SEGURA

Corrigir P1-7b, A1-48 e os defeitos conhecidos de restauração.

Antes de restaurar qualquer arquivo:

- Validar formato, versão e integridade.
- Identificar os módulos presentes e ausentes.
- Comparar registros e quantidades com o estado atual.
- Identificar possíveis conflitos e duplicidades.
- Exibir uma prévia do que será restaurado, substituído, mantido ou ignorado.
- Criar uma cópia de segurança recuperável de todo o estado que possa ser afetado.
- Exigir confirmação expressa antes de substituir dados.

O processo deve preservar o estado anterior mesmo se a restauração falhar.

Restaurar não pode causar reinjeção de registros embutidos no HTML após recarregar.

Não eliminar pagamentos, pacientes ou evoluções atuais por ausência de um módulo em backup parcial.

Restaurar também os registros financeiros antigos legíveis, inclusive IDs numéricos e bancos legados, preservando seus dados originais.

Não alterar valores monetários nem converter identificadores silenciosamente.

Considerar falhas de armazenamento, interrupção da operação e recarga durante a restauração. Se não houver garantia suficiente de recuperação, recusar a restauração sem modificar o estado existente.

O resultado precisa apresentar contagens antes/depois para os módulos restaurados.

---

## FASE 4 — TESTES AUTOMATIZADOS E REGRESSÃO

Utilizar Chromium isolado, Playwright e somente dados fictícios.

Testar preferencialmente por `file://`, pois é assim que o Dashboard é aberto atualmente. Se for necessário usar HTTP local, documentar e justificar a diferença.

Reexecutar as verificações críticas da auditoria A1.2.

Testes prioritários:

**Armazenamento**
- Livro de 500, 1.500, 6.500 e 12.000 linhas.
- Centenas de operações sucessivas.
- Cota quase cheia e totalmente cheia.
- Liberação seletiva de cópias previamente exportadas e verificadas.
- Preservação de quarentenas e revisões.
- Pagamentos funcionando após liberação segura de espaço.

**Backups**
- Cadastro íntegro e ilegível.
- Livro-caixa íntegro, bloqueado e com IDs numéricos.
- Quarentenas ativas e arquivadas.
- Backup parcial devidamente identificado.
- Backup unificado com Academia e checklists.
- Arquivo baixado e verificação do seu conteúdo.
- Compatibilidade com o formato v2.

**Restauração**
- Restaurar backup antigo.
- Restaurar backup novo.
- Restaurar backup parcial sem apagar módulos ausentes.
- Falha no meio da restauração.
- Restaurar, recarregar e comparar todos os registros.
- Preservar o estado anterior e permitir recuperação.
- Testar ausência de reinjeção de dados embutidos.

**Regressão**
- Todas as 18 telas.
- Pacientes, pagamentos, evoluções e contabilidade.
- Simulador de parcelamentos.
- Academia, Laboratório Digital e Exocad.
- Vigilância Sanitária: 8 frentes e 42 subtópicos.
- Duas abas abertas simultaneamente.
- Isolamento completo das chaves DEV.
- Segurança contra HTML malicioso e alterações silenciosas.

Não considerar um teste aprovado apenas por ausência de erro no console. Verificar dados e comportamento.

---

## ENTREGAS OBRIGATÓRIAS

1. `Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html`
2. `Relatorio-Manfrin-Arnez-6.2-DEV-04-A5.md`
3. Suíte Playwright atualizada.
4. Matriz de testes aprovados, reprovados e não executados.
5. Comparativo DEV.3 → DEV.4.
6. Hash SHA-256 da versão entregue.
7. Inventário das bases incluídas no backup.
8. Descrição da política de retenção e recuperação.
9. Lista dos riscos residuais e etapas ainda pendentes.
10. Pacote ZIP completo, disponibilizado por um meio realmente baixável, não apenas por caminhos internos `/workspace/`.

**IMPORTANTE SOBRE O GITHUB:** se for necessário disponibilizar os arquivos pelo repositório, utilize somente uma branch de desenvolvimento e não altere o site institucional nem a branch principal. Solicite minha confirmação antes de publicar alterações no repositório remoto.

Ao finalizar, apresente:

✓ CORRIGIDO E TESTADO  
⚠ CORRIGIDO, MAS PRECISA DE AUDITORIA  
✗ NÃO CORRIGIDO  
○ PENDENTE

Não declarar a versão pronta para uso clínico.

**ORDEM DE EXECUÇÃO:** implementar e testar primeiro N-1, N-2 e N-3; registrar os resultados; depois desenvolver o backup e a restauração da A5. Se surgir risco de perda de dados ou necessidade de uma alteração destrutiva não prevista, interromper e solicitar autorização.

Ao terminar, aguardar auditoria independente do Claude antes de qualquer implantação.

**PRIORIDADE ABSOLUTA: PRESERVAR INTEGRALMENTE OS DADOS E A CAPACIDADE DE RECUPERAÇÃO DO DASHBOARD MANFRIN ARNEZ.**