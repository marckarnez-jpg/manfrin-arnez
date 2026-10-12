# Proposta — suspensão preventiva do merge

**RISCO CRÍTICO CONFIRMADO NOS TESTES.** Recomendação formal: suspender o uso de “Mesclar backup” até correção autorizada e auditoria. Nenhum bloqueio foi implementado.

✗ O risco crítico foi confirmado em T02/T08. Recomendo suspender operacionalmente “Mesclar backup” na DEV.4 até correção autorizada e auditada, inclusive em uma aba: existem também cache posterior desatualizado, validação insuficiente e rollback incompleto. Nenhum bloqueio técnico foi implementado nesta etapa.

## Cenários que exigem impedimento preventivo

- Outra aba aberta, revisão antiga ou mudança entre leitura e confirmação.
- Preimage clínica diferente do estado persistido autoritativo.
- Ausência/falha/abort de histórico, mutex ou verificação da proteção antes de gravar.
- Falha parcial, rollback não verificado ou recuperação pendente.
- IDs colidentes com conteúdo/identidade divergentes, vínculos inválidos ou duplicados internos sem revisão.
- Formato/versão não suportados; dados financeiros/taxas inválidos; cobertura omissa tratada como completa.
- Rascunhos existentes quando a reidratação pudesse substituí-los sem decisão.

## Bloqueio técnico futuro, somente mediante autorização

Bloquear botão, input e handler de merge, inclusive acionamento programático/caminhos alternativos. Explicar a suspensão e manter exportação fiel do estado persistido, cópias brutas, quarentenas, histórico e fluxo A5 auditado. Não criar substituição silenciosa por outro importador. Não bloquear indiscriminadamente o export para impedir o usuário de preservar dados.

A liberação futura exige leitura autoritativa sob mutex, revisão estável/preflight, preimage completa com journal recuperável e integridade verificada, aplicação/rollback conferidos, decisão de conflitos e reidratação coerente sem apagar rascunhos. Fechar outra aba ou recarregar o HTML, isoladamente, não resolve todos os defeitos. A arquitetura definitiva deve respeitar o resultado da auditoria Claude.

○ Aguardando autorização para qualquer modificação de código. Não há DEV.5 nesta entrega.
