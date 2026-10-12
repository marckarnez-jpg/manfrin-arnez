# F. Sequência mais segura de implementação futura

Esta sequência é uma recomendação condicionada; nenhum passo de desenvolvimento está autorizado ou começou. Uma candidata futura pode ser designada DEV.5 A4, mas **não foi criado HTML dessa versão**.

1. **Gate da auditoria A5 e autorização.** Receber relatório Claude, registrar seu hash/status, resolver primeiro falhas críticas A5 numa cópia isolada autorizada. Fixar o baseline aprovado e preservar DEV.4/DEV.3 como referências imutáveis. Confirmar ambiente file:// e política de locks.
2. **Caracterização independente.** Executar os cenários D com fixtures pequenas integralmente fictícias e perfis descartáveis; confirmar D-A4-01/02 e distinguir hipóteses de perdas efetivamente reproduzidas. Registrar bytes/hash do estado antes/depois, sem “aprovar” teste apenas por console limpo. Não executar scripts originais que fazem clear().
3. **Disciplina de persistência e recuperação.** Inventariar todos os escritores ativos, distinguindo handlers legados sobrescritos pelo bindUI A5. Projetar o coordenador e contratos; proteger o merge antes de corrigir sua aparência. Incluir taxas/checklist e escritores de módulos-filhos. Validar rollback, interrupção, cota e limites de exclusividade antes do lote visual.
4. **União e prévia determinísticas.** Tratar versões, legado, IDs, conflitos, referências, itens ignorados e formatos parciais com regras aprovadas. Não alterar dados para fazer validadores “passarem”. Testar repetição/idempotência e mesmos IDs divergentes, preservando originais e proteções.
5. **Reidratação e projeções.** Resolver A1-45/B-120: só após commit verificado, reidratar livro/clínico/tokens e atualizar views afetadas. Aplicar o mesmo contrato ao pai Academia e filhos. Conservar rascunhos, paciente selecionado, mês e entradas manuais; falha de render não desfaz um commit correto automaticamente.
6. **Abas e falhas de UI.** Notificar invalidação, reler ao recuperar foco e validar revisão sob mutex ao gravar. Estado sujo não é substituído automaticamente. Separar confirmado/rascunho e exportação oficial/específica. Validar guardas contra último escritor e recusa ao merge com outra aba ativa.
7. **Codental e otimização.** Só com política de identidade aprovada, revisar proveniência e prévias; medir e otimizar mergeCodental sem modificar sua semântica. Manter supressão de seeds após restore. Não priorizar milissegundos acima de segurança de dados.
8. **Interface e acessibilidade.** Consolidar navegação, origem, filtro e mensagens; verificar 18 telas, estados vazios, foco e uso no Mac. Melhorias de baixo risco não devem impedir a identificação de proteção bloqueada ou de dados não salvos.
9. **Regressão e nova auditoria.** Reexecutar A5 e os IDs históricos relevantes com critérios atualizados explicitamente, acrescentar 43 casos D, verificar hashes/isolamento/legado/quarentenas e receber auditoria independente da candidata. Não contar casos não executados como aprovados.
10. **Entrega somente com autorização.** Preparar comparação e pacote auditável; solicitar autorização específica antes de qualquer publicação ou implantação. Nenhum PR/merge/main ou uso clínico decorre da aprovação do planejamento.

## Critérios de interrupção do desenvolvimento futuro

- Perda de base atual, preimage não verificável, rollback inconclusivo ou operação que necessita reduzir a proteção A5: interromper o lote e preservar todas as evidências fictícias.
- Arquivo não compatível com os próprios exportadores/leitores, nova chave não inventariada ou kind sem contrato de versão: impedir entrega até resolver compatibilidade.
- Próxima gravação funciona apenas removendo a comparação de estado ou atualizando um token sem reidratar o modelo: rejeitar a abordagem.
- Semântica de ID/duplicado/manual não decidida: manter conflito para revisão, não escolher pelo usuário.
- Fonte real, paciente real, backup real ou perfil principal: não abrir/importar.

Recomendação: **segurança da mesclagem → regras de união → reidratação → concorrência/rascunhos → Codental/desempenho → interface → regressão independente.** Corrigir somente o refresh não é uma primeira entrega segura.
