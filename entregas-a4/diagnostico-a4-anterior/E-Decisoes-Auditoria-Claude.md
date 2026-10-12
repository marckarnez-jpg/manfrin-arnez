# E. Decisões condicionadas à auditoria independente

**○ Pendente:** o resultado do Claude sobre a DEV.4 não foi recebido nesta etapa. Não inferir aprovação com base na publicação do ZIP ou nos testes do Codex.

| Decisão | Evidência necessária | Condição para avançar | Se não houver aprovação |
|---|---|---|---|
| Infraestrutura de recuperação A5 reutilizável no merge? | Journal, reserva, marker, rollback, interrupção e preimage íntegra | Auditoria aprova ou exige ajustes documentados | Corrigir A5 em cópia futura autorizada antes de integrar A4 |
| APIs por file:// no Mac e coordenação de abas | Teste independente de IndexedDB/Web Locks/Web Crypto na origem real de abertura | Ambiente suportado e limites explícitos | Manter restrições/recusa; não inserir fallback inseguro para gravar |
| Registro de proteção do merge e compatibilidade v3 | Leitor atual só aceita operation/restore/cleanup | Decidir envelope existente com origem MERGE ou evolução versionada compatível | Não criar kind novo informalmente nem exportar arquivo que o próprio leitor recuse |
| Mutex único para todos os escritores | Casos de corrida em clínico/Academia/Sanitária/taxas/checklist | Política de lock e revisão validada, sem deadlock | Limitar escopo e recusar operações concorrentes; não alegar atomização universal |
| Exclusividade para merge multibase | Comportamento com outra DEV.4 e rascunhos | Recomendar primeiro merge exclusivo, como restore | Não remover locks para permitir duas abas sem protocolo alternativo auditado |
| Política de IDs e de conflitos | Mesmo ID divergente, IDs diferentes equivalentes, referência a paciente conflitante | Usuário define preservação/resolução manual e fontes confiáveis | Padrão conservador: mostrar conflito e recusar trecho inseguro |
| Política de correspondência Codental | Homônimos, CPF vazio, CodentalId divergente, campo manual de origem antiga | Critério e proveniência por campo aprovados | Conservar ambiguidades e não unir apenas por nome silenciosamente |
| Escopo v3 no merge | Cobertura de clínico/livro/taxas versus Academia/checklists/proteções | Declaração dos módulos aplicáveis e não mesclados, sem falsa completude | Recusar v3 com motivo explícito até suporte validado; restauração A5 continua separada |
| Rascunhos e preferências | Campos não salvos e seleção/mês/taxa manual | Definir preservar, oferecer revisar ou descartar com confirmação | Nenhum refresh/reload automático que descarte preenchimento |
| Snapshot histórico versus cadastro atual | Regra já explícita no clínico | Manter história original; atualização apenas por ação consciente | Não uniformizar pagamentos antigos por estética |
| Política de seeds após merge/sync | B-123 e suppress-seeds A5 | Não reabilitar reinjeção; ação de sync tem prévia separada | Manter marca de supressão e exigir decisão explícita |
| Limites de memória/cota e desempenho | Volumes fictícios e falhas reais/simuladas classificados | Limites e tempo-alvo aceitos sem trocar recuperação por velocidade | Manter bloqueio seguro; não remover históricos/avisos automaticamente |

## Decisões já resolvidas pelo comando desta etapa

✓ Não alterar DEV.4, DEV.3, site ou main. ✓ Não publicar, criar nova versão, implementar A4, importar pacientes, realizar merge/deploy ou enfraquecer A5. ✓ Análise só estática/documental. ○ Qualquer execução/correção futura requer autorização; não há autorização implícita por constar neste plano.

Se o Claude identificar falha crítica A5, reordenar o plano em favor dessa falha e manter a candidata A4 suspensa. Se a auditoria alterar o formato ou o protocolo de recuperação, atualizar esta especificação e a matriz D antes de desenvolver. A DEV.4 em auditoria continua imutável.
