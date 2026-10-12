# A4 — Matriz dos 43 testes

**9 APROVADOS · 31 REPROVADOS · 3 NÃO TESTADOS.**

✓ APROVADO: comportamento/medição confirmados no escopo registrado. ✗ REPROVADO: ao menos um contraexemplo reproduzido viola o oráculo; não significa que todos os subcasos falharam. ○ NÃO TESTADO: o conjunto não pôde ser validado; subcasos e motivos estão registrados. ⚠ Necessita revisão: política/escopo dependente de decisão ou auditoria.

Os 43 são casos de teste, não 43 defeitos independentes. Subcasos ainda não exercitados não herdam aprovação. Os IDs T-A4 e IDs originais do diagnóstico foram preservados. Detalhes estruturados contêm cenário, oráculo, ações, resultados e referências aos logs.

| Teste | IDs históricos | Resultado | Observação |
|---|---|---|---|
| [T-A4-01](resultados/T-A4-01.json) | P0-3; A1-45; B-120 | ✗ REPROVADO | Persistido: 2 linhas bancárias; modelo rows: 1. A projeção não acompanha o merge. |
| [T-A4-02](resultados/T-A4-02.json) | P0-3; P1-3 | ✗ REPROVADO | Paciente recente desaparece; pagamento 98765 centavos volta a 12345; evolução marcada volta a pendente. |
| [T-A4-03](resultados/T-A4-03.json) | A1-44; A1-45 | ✗ REPROVADO | Após merge, correção bancária e cadastro clínico são recusados por referências de comparação/modelos antigos. |
| [T-A4-04](resultados/T-A4-04.json) | B-102; C-92/C-93/C-94 | ✗ REPROVADO | Cópia ANTES-MESCLAR contém care antigo; não captura o estado clínico autoritativo mais recente. |
| [T-A4-05](resultados/T-A4-05.json) | A1-56/57; P1-7b (regressão A5) | ✗ REPROVADO | Falhas transitórias na segunda/terceira escrita fazem rollback exato; falha também no rollback deixa clínico aplicado, livro antigo e guard vazio. |
| [T-A4-06](resultados/T-A4-06.json) | N-1; A1-48 (regressão A5) | ✗ REPROVADO | Merge prossegue apesar de captureOperation sinteticamente indisponível, sem criar journal/preimage A5. |
| [T-A4-07](resultados/T-A4-07.json) | P1-7b; B-123 (regressão A5) | ○ NÃO TESTADO | Interrupção tentada três vezes; perda da conexão de automação impediu validar a reabertura. Fases journal/marker do merge inexistentes. |
| [T-A4-08](resultados/T-A4-08.json) | P1-3; C-46 | ✗ REPROVADO | Com confirmação aberta em B, A salva lançamento bancário com amount=99999; ao confirmar B, volta a 1001. |
| [T-A4-09](resultados/T-A4-09.json) | A1-45 | ✗ REPROVADO | Nova evolução persistida pelo merge não aparece no note-list já montado. |
| [T-A4-10](resultados/T-A4-10.json) | Sem ID histórico específico | ✓ APROVADO | Rascunhos montados de cadastro/pagamento/evolução legada e taxa personalizada sobreviveram ao merge na amostra. |
| [T-A4-11](resultados/T-A4-11.json) | P0-3 (família) | ✓ APROVADO | Reaplicar o mesmo arquivo não duplica IDs nem muda o estado persistido. |
| [T-A4-12](resultados/T-A4-12.json) | Sem ID histórico específico | ✗ REPROVADO | Mesmo ID com valor diferente recebe “já está presente” sem conflito, embora os conteúdos sejam divergentes. |
| [T-A4-13](resultados/T-A4-13.json) | Sem ID histórico específico | ✗ REPROVADO | Mesmo conteúdo com novo ID entra novamente, sem aviso de possível duplicação semântica. |
| [T-A4-14](resultados/T-A4-14.json) | B-119; B-120 (escopos diferenciados) | ✗ REPROVADO | V2 com ID numérico 123, ID textual 123, banco legado e centavos fracionários é recusado pelo merge. |
| [T-A4-15](resultados/T-A4-15.json) | Sem ID histórico específico | ✗ REPROVADO | Paciente com ID colidente e identidade divergente é ignorado; novo pagamento fica vinculado ao cadastro existente. |
| [T-A4-16](resultados/T-A4-16.json) | Sem ID histórico específico | ✗ REPROVADO | Duplicados clínicos/vínculo ausente são recusados; duplicados internos bancários divergentes são aceitos, primeiro vence silenciosamente. |
| [T-A4-17](resultados/T-A4-17.json) | B-119; B-120 | ✓ APROVADO | V2 clínico válido mantém módulos administrativos/taxas ausentes; parcial só livro é recusado sem substituir care. |
| [T-A4-18](resultados/T-A4-18.json) | BKP-02 (regressão A5) | ✓ APROVADO | Backup v3 produzido pela DEV.4 é recusado pelo merge, sem alterar bases ativas (recusa segura, mensagem genérica). |
| [T-A4-19](resultados/T-A4-19.json) | BKP-05 (nova execução, sem herdar aprovação) | ✗ REPROVADO | V2 com version=99 é aceito e aplicado pelo merge. |
| [T-A4-20](resultados/T-A4-20.json) | A1-46; B-121 | ✗ REPROVADO | Linha com data/amount/kind inválidos e HTML sintético entra na base ativa; não houve execução do marcador XSS nesta amostra. |
| [T-A4-21](resultados/T-A4-21.json) | Sem ID histórico específico | ✗ REPROVADO | Com base de taxas ausente, mapa contendo taxa 150 e campo inesperado é persistido sem validação. |
| [T-A4-22](resultados/T-A4-22.json) | P0-4 (algoritmo) | ✗ REPROVADO | Nome igual e CPF vazio fundem cadastros sem pending, apesar de IDs distintos. |
| [T-A4-23](resultados/T-A4-23.json) | Sem ID histórico específico | ✗ REPROVADO | Campo preenchido de origem histórica sem proveniência é sobrescrito; manual explícito e entrada vazia foram preservados em subcasos. |
| [T-A4-24](resultados/T-A4-24.json) | B-123 (regressão A5) | ✓ APROVADO | Duas sincronizações pelo botão original mantêm IDs e vínculos; restore v3 e reload preservam base original e supressão de seeds. |
| [T-A4-25](resultados/T-A4-25.json) | Sem ID histórico específico | ✓ APROVADO | Múltiplos candidatos e CodentalId conflitante geram pending; não ocorre escolha arbitrária nos subcasos. |
| [T-A4-26](resultados/T-A4-26.json) | P1-3; A1-40/41/42/43; C-46 | ✗ REPROVADO | Pausa após comparação clínica e antes da escrita: B salva; A retoma e apaga o novo paciente de B. CAS sem serialização não é atômico. |
| [T-A4-27](resultados/T-A4-27.json) | P1-3 | ✗ REPROVADO | Taxa 2x salva em B desaparece quando A desatualizada salva 3x. |
| [T-A4-28](resultados/T-A4-28.json) | P1-3 | ✗ REPROVADO | Tarefa salva em B desaparece quando A salva outra tarefa do checklist56. |
| [T-A4-29](resultados/T-A4-29.json) | P1-3 | ✗ REPROVADO | Retornar ao foco não corrige modelo antigo de taxas antes da próxima escrita. |
| [T-A4-30](resultados/T-A4-30.json) | A1-45; navegação 18 telas | ✗ REPROVADO | Menu das 18 telas mantém página/menu coerentes; após merge, navegar não reidrata o modelo bancário antigo. |
| [T-A4-31](resultados/T-A4-31.json) | P1-7b; P1-3 (regressões A5) | ✓ APROVADO | Restore com duas abas é recusado; escrita bancária assíncrona com epoch sinteticamente trocado é bloqueada e preserva livro. |
| [T-A4-32](resultados/T-A4-32.json) | P1-6; SEC-01; ISO-05 (dependências) | ○ NÃO TESTADO | file:// bloqueado por ERR_BLOCKED_BY_ADMINISTRATOR; localhost e falta de locks/IndexedDB foram testados. Conjunto integral não aprovado. |
| [T-A4-33](resultados/T-A4-33.json) | A1-56/57 como referência | ✗ REPROVADO | Quota real: taxa não persiste e há mensagem de erro, mas o campo é rotulado “Personalizada · salva”. |
| [T-A4-34](resultados/T-A4-34.json) | Sem ID histórico específico | ✗ REPROVADO | Inclusão de material recusada fica em memória; repetir inclusão persiste dois materiais iguais. |
| [T-A4-35](resultados/T-A4-35.json) | MA61-1 (escopo distinto); P1-3 | ✗ REPROVADO | Anotação sanitária recusada aparece no export específico apesar de base persistida inalterada. |
| [T-A4-36](resultados/T-A4-36.json) | BKP-02; B-101 (regressões e escopos) | ✗ REPROVADO | Após falha de inclusão, export Academia contém 2 materiais; backup v3 confirmado contém apenas 1. |
| [T-A4-37](resultados/T-A4-37.json) | Sem ID histórico específico; BKP-08 separado | ✗ REPROVADO | Import Academia B altera pai; filho58 continua exibindo base A2 em vez de A3. |
| [T-A4-38](resultados/T-A4-38.json) | Sem ID histórico específico | ✗ REPROVADO | Interagir no filho58 depois de importar B grava base/checks antigos sobre o progresso importado. |
| [T-A4-39](resultados/T-A4-39.json) | BKP-02; B-123 (regressões A5) | ✓ APROVADO | Restore v3 e reload mantêm Academia; três PDFs baixados são idênticos aos payloads incorporados, com SHA-256 registrados. |
| [T-A4-40](resultados/T-A4-40.json) | Sem ID histórico específico | ✗ REPROVADO | Mês escolhido 2027-01 é substituído por 2026-10 sem escolha específica ao mesclar pagamentos de outubro. |
| [T-A4-41](resultados/T-A4-41.json) | Sem ID histórico específico | ✗ REPROVADO | Snapshot histórico é preservado e explicado; taxa manual 12.34 vira automática 10 após salvar apuração ma57, sem confirmação específica do campo. |
| [T-A4-42](resultados/T-A4-42.json) | P0-4; PERF-01 | ○ NÃO TESTADO | Baseline original medido; não há candidata autorizada para comparação de equivalência. |
| [T-A4-43](resultados/T-A4-43.json) | PERF-01 | ✓ APROVADO | Aberturas frias/quentes e navegação medidas; aprovação refere-se ao registro do baseline, não à meta de desempenho ou prontidão clínica. |

## Limites de cobertura

T07: tentativas de crash não produziram estado final verificável; sem conclusão de recuperação/perda. T32: file:// impedido por política; não contornada. T42: não existe candidata de correção autorizada.

T06 injeta indisponibilidade em captureOperation; quota física de IndexedDB, abort de transação e leitura divergente não foram exercitados. T10 inclui campos legados montados, inclusive evolução atualmente oculta pela interface estruturada. T26 forçou a corrida clínica, não a janela CAS dos demais módulos. T27 reproduziu ma53/ma53; ma57 aparece também no T41, mas alternância completa entre duas abas ma53/ma57 permanece não exercitada. T28 reproduziu tarefas concorrentes; importação específica substitutiva foi conferida por leitura, sem execução adicional. T30 cobre menu e navegação após merge; todos os atalhos internos não foram exercitados. T33 falha real da taxa e falha injetada foram executadas; quota física da configuração não foi exercitada separadamente. T34 material/retry foi executado; equipamento/análise não foram exercitados. T35 anotação/export foi executada; mudança de cor com quota não foi exercitada.

T39 confirma restore/reload e os três PDFs efetivamente baixados; não instrumenta todas as escritas de inicialização. T43 registra baseline amostral (3 aberturas frias/quentes), não certifica p95 populacional nem meta de 5 segundos. Nenhum teste negativo com contraexemplo é convertido em aprovado pela falta de execução de outro subcaso.
