# A4 — Riscos classificados após reprodução

**RISCO CRÍTICO CONFIRMADO NOS TESTES.** Recomendação formal: suspender o uso de “Mesclar backup” até correção autorizada e auditoria. Nenhum bloqueio foi implementado.

| ID do diagnóstico | Gravidade | Situação | Evidência e impacto |
|---|---|---|---|
| D-A4-01 | CRÍTICA | ✗ Confirmado | T02/04/05/06/08: sobrescrita clínica/financeira; preimage stale, merge sem journal e rollback não verificado. |
| D-A4-02 | ALTA | ✗ Confirmado | T01/03/09/30: modelos/telas antigos após merge, save seguinte recusado ou export/projeção divergente. |
| D-A4-03 | ALTA | ✗ Confirmado | T12/13/15/16: conflitos de conteúdo/identidade e duplicação semântica sem revisão. |
| D-A4-04 | ALTA | ✗ Confirmado | T14/19/20/21: incompatibilidade histórica e validação fraca. T18 recusa v3 sem mutação, proteção nesse subcaso. |
| D-A4-05 | ALTA | ⚠ Necessita revisão de política | T22/23: fusão por nome e substituição de campos históricos são comportamentos reproduzidos; regra final de identidade/proveniência depende de decisão. T24/25 protegem idempotência/ambiguidades testadas. |
| D-A4-06 | CRÍTICA no clínico; ALTA nos demais | ✗ Confirmado | T26 eleva prioridade: CAS clínico forçado não serializa; T27/28/29 perdem taxas/tarefas. T31 protege restore/epoch nos subcasos testados. |
| D-A4-07 | ALTA | ✗ Confirmado | T33/34/35/36: estado em memória recusado vira aparente salvo/export oficial ou duplicação no retry. |
| D-A4-08 | ALTA | ✗ Confirmado em ma58 | T37/38: cache de filho sobrescreve progresso importado. Cobertura completa ma59/ma60 segue pendente. |
| D-A4-09 | MÉDIA | ✗ Confirmado | T40: troca de mês sem decisão; T41: manual vira automático. Snapshot histórico preservado é comportamento correto. |
| D-A4-10 | MÉDIA | ⚠ Baseline medido; candidata pendente | T42/43: lentidão relevante, sem otimização autorizada nem meta aprovada. |

Não são 31 defeitos novos: 31 casos reprovados compartilham essas causas. IDs históricos P0-3, A1-45, B-120/B-121, AJ-8/AJ-18 e dependências são preservados na matriz e nos seis documentos originais. IDs D-A4 são do diagnóstico local, não IDs inventados atribuídos ao Claude.

A5 restaurar/backup não deve ser marcado como globalmente reprovado por defeitos do merge legado. A restauração v3, bloqueio de duas abas, epoch e PDFs tiveram comportamentos seguros nas amostras. A aprovação desses subcasos não substitui a auditoria independente pendente. CSV/fórmulas, TCLE, assinatura e outros módulos não recebem conclusões de segurança por estes testes.
