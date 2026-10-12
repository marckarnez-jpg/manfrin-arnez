# DEV.5 — recomendações condicionadas à auditoria Claude

1. Receber a auditoria A5 e tratar suas exigências antes de alterar o mecanismo transacional/recovery. Congelar baseline DEV.4 e DEV.3, hashes e fixtures desta entrega.
2. Autorizar bloqueio técnico preventivo do merge legado, preservando os recursos de proteção/export auditados. Não habilitar o merge com apenas aviso ou só fechar abas.
3. Definir contrato comum de escrita: mutex, revisão por base, epoch, leitura autoritativa, preimage e journal verificados. Cobrir escritores clínicos, taxas/checklist, importadores específicos e operações assíncronas; CAS isolado não é transação entre abas.
4. Definir política de merge/conflitos: ID/tipo exatos, conteúdo divergente, vínculos de paciente, duplicados internos/semânticos, formatos v2/v3, módulos ausentes, identidade Codental e proveniência por campo. Nenhuma fusão por nome recebe aprovação automática.
5. Separar estado confirmado e rascunho. Mutação de material/equipamento/análise não deve entrar no confirmado antes do save; retry não deve acumular entradas. Exports oficiais devem corresponder ao persistido ou identificar explicitamente rascunho.
6. Reidratar pai/filhos ma58/59/60 e projeções clínicas/bancárias a partir da revisão confirmada. Preservar textos e escolhas de filtro; avisar revisão stale antes de gravar. Não usar reload automático que apague formulários.
7. Manter snapshot histórico de pagamentos. Troca de taxa manual/automática e mês escolhido exige rótulo/decisão claros.
8. Somente depois, otimizar mergeCodental com índices e comprovar equivalência de identidade, campos, pending e estatísticas. Nenhuma proteção A5 deve ser retirada para reduzir tempo.
9. Reexecutar os 43 casos, completar subcasos não exercitados e adicionar harness confiável de interrupção. Rodar regressões A1.2/A5 e suite independente; entregar candidata separada apenas após autorização.

## Decisões pendentes da auditoria/usuário

⚠ Adequação do journal/preimage A5 e rollback verificado; todos os escritores que devem usar mutex; política de recovery/reserva/retention; compatibilidade de versões e v3 no merge; regras de identidade e proveniência; aceitação de IDs numéricos/valores legados; semântica de duplicados; cobertura de backups e exports; comportamento de rascunhos/rehidratação; alvo de desempenho e hardware/protocolo do Mac; método de publicação privada/branch de desenvolvimento para download.

✓ Esta entrega não altera algoritmo, formato, módulos, arquitetura A5, branch main ou site. Não há PR, merge, deploy, publicação, dashboard hospedado ou uso clínico.
