# Comparativo DEV.3 → DEV.4

DEV.3 original preservada: SHA-256 `e4e4f49ca37e85cd9c83c67aa79b4e9d2fcb74b11137c387a5692ea8727bcc3f`, 4.077.003 bytes. Site institucional preservado: `4b6789de6fdae19e79eeddd310c5f9c680fe7758438b57a38987587f74f4d8e3`.

| Área | DEV.3 | DEV.4 A5 |
|---|---|---|
| Proteção por operação do livro | Cópias integrais sucessivas no localStorage | Cópia exata em IndexedDB, comprometida e relida antes de gravar; bloqueio em falha |
| Diagnóstico/retensão | Sem liberação sustentável de cópias | Diagnóstico, histórico exportável/verificável, seleção e confirmação; guarda cópia mais recente e comprovante externo |
| Aviso global | Cópias válidas podem manter faixa de atenção | Cópia válida é informação rotineira; riscos permanecem visíveis |
| Livro original bruto | Dependente de faixa de risco | Botão sempre disponível na tela Backup |
| Backup geral | care/ledger/rateSettings v2; exclusões administrativas e de proteção | v3 com todas as chaves DEV persistidas, histórico IDB e manifesto de cobertura/ausências/integridade |
| Dados inválidos/desconhecidos | Pode recusar download geral | Arquivo bruto identificado PARCIAL; sem simular base vazia |
| Histórico já liberado | Sem rastreio | Comprovante identifica arquivo externo e SHA; próximo snapshot é PARCIAL e exige preservá-lo |
| Restore v2 | Validação financeira estrita; substituição imediata | Mantém legado legível sem conversão, mostra prévia, preserva bases ausentes |
| Restore v3 | Inexistente | Confirmação, preimage integral, marcador, reserva de cota, receipt e recarga |
| Falha/interrupção | Sem journal global recuperável | Recuperação antes de ativar módulos; bloqueio se não houver garantia |
| Recuperação de preimage | Inexistente | Prévia/novo journal; inclusive ausência anterior de base adicionada, com remoção expressamente confirmada |
| Seeds após restore | Possível reinjeção embutida | Marcador explícito de supressão; não trata ausência como autorização para reinjetar |
| Conflitos de abas | Proteção parcial legado | Restore exclusivo entre DEV.4; estado desatualizado detectado nos principais editores |
| Academia/checklists desconhecidos | Podem sobrescrever versão não suportada | Gravação bloqueada preservando bytes originais; snapshot parcial |
| Isolamento DEV | Prefixo de localStorage | Prefixo preservado + DB e locks identificados DEV; sentinelas fora do prefixo verificadas |

O HTML continua autocontido. Três componentes novos (`protection.js`, `backup-engine.js`, `bootstrap.js`) estão em `fontes/`. Os scripts legados passam por inicialização deferida: aguardam IndexedDB/coordenação/recuperação antes de ativar editores. Isso é uma mudança arquitetural sujeita à auditoria independente, especialmente file://.

`Comparativo-Scripts-DEV3-DEV4.json` identifica hashes de cada script legado. O diff dos quatro scripts cujo conteúdo mudou está em `Comparativo-Scripts-DEV3-DEV4.diff`; linhas gigantes são abreviadas com tamanho/hash para legibilidade, e o original completo permite conferir. PDFs embutidos são comparados pelo conteúdo base64 e permanecem idênticos. O teste Exocad baixa e verifica o cabeçalho PDF real.

A correção não torna a DEV clinicamente homologada, não resolve toda a etapa A4 e não produz migração de dados reais. Os formatos, políticas e limites estão nos documentos específicos.
