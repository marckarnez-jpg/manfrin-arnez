# Matriz executada — DEV.4 A5

HTML SHA-256 `cc1da21a717db0e2f2bd7303284a3fd0b3af4c14be8638abb71741bfddc5fcbb`. 108 verificações de comportamento aprovadas na última execução de cada caso; 46 verificações auxiliares aprovadas; 0 reprovadas; 5 não executadas. Sintaxe dos 26 scripts é verificação estática separada, não somada ao comportamento. Rodadas diagnósticas e resultados anteriores anexados não contam como aprovação desta DEV.4. Dois problemas do harness (atribuição de função e espera assíncrona da prévia) foram corrigidos; diagnósticos são preservados em referencias/. A matriz conta somente a rodada definitiva sobre o SHA entregue, sem somar rodadas anteriores.

| ID | Resultado | Classe | Evidência/origem |
|---|---|---|---|
| N1-220-OPERACOES-500 | APROVADO | comportamento | {"linhas": 500, "operações": 220, "históricos": 220, "erro": null}; `resultados-fase1.json` |
| N1-SEM-CRESCIMENTO-COPIAS-LOCAL-500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-COPIA-ORIGINAL-RECUPERAVEL-500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N3-SEM-FAIXA-ROTINEIRA-500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-ARQUIVO-EXTERNO-VERIFICADO-500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-LIMPEZA-SELETIVA-500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-EXTERNO-PRESERVA-ESTADOS-500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-LIVRO-ATUAL-INALTERADO-PELA-LIMPEZA-500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-RETENCAO-MINIMA-500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| JS-FASE1-500 | APROVADO | auxiliar | []; `resultados-fase1.json` |
| N1-220-OPERACOES-1500 | APROVADO | comportamento | {"linhas": 1500, "operações": 220, "históricos": 220, "erro": null}; `resultados-fase1.json` |
| N1-SEM-CRESCIMENTO-COPIAS-LOCAL-1500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-COPIA-ORIGINAL-RECUPERAVEL-1500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N3-SEM-FAIXA-ROTINEIRA-1500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-ARQUIVO-EXTERNO-VERIFICADO-1500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-LIMPEZA-SELETIVA-1500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-EXTERNO-PRESERVA-ESTADOS-1500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-LIVRO-ATUAL-INALTERADO-PELA-LIMPEZA-1500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-RETENCAO-MINIMA-1500 | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| JS-FASE1-1500 | APROVADO | auxiliar | []; `resultados-fase1.json` |
| N1-COTA-REAL-SATURADA | APROVADO | comportamento | 83; `resultados-fase1.json` |
| N1-QUARENTENA-REVISAO-PRESERVADAS | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-QUARENTENA-NAO-ELEGIVEL | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N1-PAGAMENTO-POS-LIBERACAO | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N3-RISCO-REAL-CONTINUA-VISIVEL | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| JS-COTA | APROVADO | auxiliar | []; `resultados-fase1.json` |
| N2-BRUTO-ACESSIVEL-SEM-FAIXA | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| N2-ID-NUMERICO-ORIGINAL | APROVADO | comportamento | Ver asserção e execução; `resultados-fase1.json` |
| JS-N2 | APROVADO | auxiliar | []; `resultados-fase1.json` |
| METODO-FILE-OU-BLOQUEIO-DOCUMENTADO | APROVADO | auxiliar | Page.goto: net::ERR_BLOCKED_BY_ADMINISTRATOR at file:///workspace/entregas-a5/Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html; `resultados-a5/resultados.json` |
| BKP02-UNIFICADO-TODAS-BASES | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| BKP02-LAB-CHECKLISTS-QUARENTENAS | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| BACKUP-SOLICITADO-NAO-VERIFICADO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| BACKUP-ARQUIVO-EFETIVAMENTE-VERIFICADO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| BACKUP-HASH-ERRADO-RECUSADO | APROVADO | comportamento | Prévia RECUSADA: Integridade SHA-256 não confere; `resultados-a5/resultados.json` |
| RESTAURAR-V3-TODAS-BASES | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| P17B-PREIMAGE-INTEGRAL | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| B123-SEM-REINJECAO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| A148-RECUPERAR-ESTADO-ANTERIOR | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-10 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-11 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| V2-PREVIA-NAO-ALTERA | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| V2-CANCELAR-MANTEM-TUDO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| B119-V2-LEGADO-NUMERICO-BANCO-VALOR | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| V2-MODULOS-ADMIN-AUSENTES-MANTIDOS | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| RESULTADO-CONTAGENS-MODULO-MANTIDO-REAIS | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| LEGADO-CATEGORIA-TOTAIS-PRESERVADOS | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| N2-V3-INCLUI-NUMERICOS | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| V2-PARCIAL-CARE-AUSENTE-PRESERVADO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| VERSAO-DESCONHECIDA-RECUSADA | APROVADO | comportamento | Prévia RECUSADA: Versão legada não suportada: 99; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-21 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-22 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| CARE-ILEGIVEL-BACKUP-PARCIAL-SEM-SEED | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| CHECKLIST56-OPACO-INCLUIDO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-25 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-26 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| BASES-AUSENTES-IDENTIFICADAS-NAO-INVENTADAS | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-28 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-29 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| LIVRO-JSON-CORROMPIDO-PRESERVADO-EM-PARCIAL | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| N2-BRUTO-CORROMPIDO-EXATO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-32 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-33 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| FALHA-MEIO-RESTAURACAO-ROLLBACK-EXATO | APROVADO | comportamento | RESTAURAÇÃO RECUSADA/FALHOU: Restauração não concluída; estado anterior recuperado. Falha fictícia durante restauração; `resultados-a5/resultados.json` |
| FALHA-PREIMAGE-RECUPERAVEL | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| FALHA-REABRIR-SEM-PERDA-OU-SEED | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| INTERRUPCAO-ESTADO-INTERMEDIARIO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| INTERRUPCAO-RECARGA-RECUPERA-ANTES | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-39 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-40 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| IDB-FALHA-PROTECAO-BLOQUEIA-OPERACAO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| IDB-FALHA-PROTECAO-ALERTA-REAL | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-43 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-44 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| RESTAURO-BASE-ANTES-AUSENTE-ADICIONADA | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| RECUPERACAO-PREVIA-IDENTIFICA-REMOCAO-BASE-ADICIONADA | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| RECUPERACAO-ESTADO-ANTERIOR-INCLUSIVE-AUSENCIA | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-48 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-49 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| RESTAURO-PARCIAL-BASE-ILEGIVEL-MANTEM-CURRENT | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| RESTAURO-PARCIAL-BYTES-IGNORADOS-PROTEGIDOS | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-52 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-53 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| QUARENTENA-CONFLITO-RECUSA-SEM-SOBRESCREVER | APROVADO | comportamento | Prévia RECUSADA: Conflito de proteção: ma-ledger-v1-rejeitados-FICTICIO-CONFLITO. A cópia/quarentena/revisão atual não será sobrescrita.; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-55 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-56 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| DUAS-ABAS-RESTAURO-RECUSADO-SEM-MUTACAO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| DUAS-ABAS-LIVRO-NAO-SOBRESCREVE | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| UMA-ABA-PODE-RESTAURAR | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-60 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-61 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| VOLUME-6500 | APROVADO | comportamento | {"rows": 6500, "history": 5}; `resultados-a5/resultados.json` |
| VOLUME-ORIGINAL-RECUPERAVEL-6500 | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| VOLUME-BACKUP-COM-HISTORICO-6500 | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-65 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-66 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| VOLUME-12000 | APROVADO | comportamento | {"rows": 12000, "history": 5}; `resultados-a5/resultados.json` |
| VOLUME-ORIGINAL-RECUPERAVEL-12000 | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| VOLUME-BACKUP-COM-HISTORICO-12000 | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-70 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-71 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| RETENCAO-COMPROVANTE-EXTERNO-PERSISTIDO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| RETENCAO-BACKUP-PARCIAL-INDICA-ARQUIVO-EXTERNO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| RETENCAO-RECUPERA-ESTADO-EXTERNO-EXCLUIDO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| RETENCAO-SNAPSHOT-POS-LIMPEZA-IMPORTAVEL | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-76 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-77 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| P10-VERSAO-ACADEMIA-DESCONHECIDA-NAO-SOBRESCREVE | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| VERSAO-ACADEMIA-DESCONHECIDA-RAW-PARCIAL | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-80 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-81 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| COTA-REAL-RESTAURACAO-RECUSA-ANTES-DADOS | APROVADO | comportamento | RESTAURAÇÃO RECUSADA/FALHOU: Sem espaço para marcador de recuperação. Dados atuais intactos. Failed to execute 'setItem' on 'Storage': Setting the value of '__MA_DEV61_SANDBOX__:ma5-restore-pending-v1' exceeded the quota.; `resultados-a5/resultados.json` |
| COTA-REAL-PREIMAGE-RETIDA | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-84 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-85 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| COTA-QUASE-CHEIA-RESERVA-RECUSA-ROLLBACK | APROVADO | comportamento | RESTAURAÇÃO RECUSADA/FALHOU: Restauração não concluída; estado anterior recuperado. Failed to execute 'setItem' on 'Storage': Setting the value of '__MA_DEV61_SANDBOX__:ma5-reservation:restore:67658233-cbb7-47bb-922b-0b5e517e2c82' exceeded the quota.; `resultados-a5/resultados.json` |
| COTA-QUASE-CHEIA-JOURNAL-RECUPERAVEL | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-88 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-89 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| AJ11-B100-ROTAS-CADASTRO-ILEGIVEL-PARCIAL-EXATO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AJ11-CONTABILIDADE-SOLICITADO-NAO-VERIFICADO | APROVADO | comportamento | DOWNLOAD SOLICITADO: PARCIAL. Arquivo ainda NÃO verificado. 8 chaves e 0 registros de proteção incluídos. ma-care-v2: Expected property name or '}' in JSON at position 1 (line 1 column 2); `resultados-a5/resultados.json` |
| AJ12B-CADASTRO-BRUTO-EXATO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AJ11-VERIFICADOR-RECUSA-BYTES-DIFERENTES | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-94 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-95 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| AJ11-VERIFICADOR-SEM-DOWNLOAD-RECUSA | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-97 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-98 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| REGRESSAO-18-TELAS | APROVADO | comportamento | ["ma56-home", "dash", "quick", "accounting", "ma55-cost", "sim", "ledger", "ma55-contador", "sources", "patients", "notes", "tcle", "ma55-academy", "ma55-training", "ma55-materials", "ma61-sanitary", "ma56-project", "backup"]; `resultados-a5/resultados.json` |
| REGRESSAO-CADASTRO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| REGRESSAO-PAGAMENTO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| REGRESSAO-CSV-CONTABIL | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| REGRESSAO-SIMULADOR | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| REGRESSAO-EVOLUCOES | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| REGRESSAO-SANITARIA-8-42 | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| REGRESSAO-SANITARIA-IDAEVOLTA | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| REGRESSAO-ACADEMIA-LAB-PRESERVADOS | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| REGRESSAO-EXOCAD-PDF | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| SEGURANCA-HTML-MALICIOSO | APROVADO | comportamento | Ver asserção e execução; `resultados-a5/resultados.json` |
| AUX-PAGEERROR-110 | APROVADO | auxiliar | []; `resultados-a5/resultados.json` |
| AUX-ISOLAMENTO-111 | APROVADO | auxiliar | {"sent": {"ma-care-v2": "SENTINELA-REAL-FICTICIA", "ma-ledger-v1": "SENTINELA-REAL-FICTICIA-LIVRO", "ma-ledger-v1-prev": "SENTINELA-REAL-FICTICIA-PREV", "ma61-sanitary-checklist-v1": "SENTINELA-REAL-FICTICIA-SAN"}, "extra": []}; `resultados-a5/resultados.json` |
| SAN-01 | APROVADO | comportamento | grupos=8; subtópicos=42; por frente=6+5+6+7+4+5+4+5; painel="8 frentes / 42 subtópicos"; `independente-adaptada/t5.json` |
| SAN-02 | APROVADO | comportamento | verde=4 amarelo=29 vermelho=9; luzes das frentes=VERMELHO,VERMELHO,AMARELO,VERMELHO,AMARELO,AMARELO,VERMELHO,VERMELHO; `independente-adaptada/t5.json` |
| SAN-03 | APROVADO | comportamento | DOM {"ok":4,"warn":29,"bad":9} vs painel 4/29/9; `independente-adaptada/t5.json` |
| SAN-04 | APROVADO | comportamento | mensagem="Para marcar verde, preencha primeiro a evidência de "Testes biológicos semanais""; cor do item=warn; `independente-adaptada/t5.json` |
| SAN-05 | APROVADO | comportamento | sequência observada: VERDE → VERMELHO → AMARELO; `independente-adaptada/t5.json` |
| SAN-06 | APROVADO | comportamento | antes 9/25/8 → depois 9/25/8; JSON idêntico=true; `independente-adaptada/t5.json` |
| SAN-07 | APROVADO | comportamento | filtro vermelho=8 (esperado 8); frente PGRSS=4 (esperado 4); busca "autoclave"=8; `independente-adaptada/t5.json` |
| SAN-08 | APROVADO | comportamento | format=manfrin-arnez-sanitary-checklist version=1; estados exportados=7; arquivo=Manfrin-Arnez-Checklist-Sanitario-6.1.json; `independente-adaptada/t5.json` |
| SAN-09 | APROVADO | comportamento | estado do item alterado antes de importar=bad; após importar=(padrão); estados iguais ao exportado=true; `independente-adaptada/t5.json` |
| SAN-10 | APROVADO | comportamento | formato errado:rejeitado; semáforo inválido:rejeitado; id inexistente:rejeitado; __proto__:rejeitado; versão 2:rejeitado; grande >400KB:rejeitado; poluição de protótipo: ({}).ok=undefined; `independente-adaptada/t5.json` |
| SAN-11 | APROVADO | comportamento | window.__xss=undefined; <img> injetadas=0; <script> injetados=0; item encontrado pela busca=1; `independente-adaptada/t5.json` |
| SAN-12 | APROVADO | comportamento | links=2; `independente-adaptada/t5.json` |
| SAN-13 | APROVADO | auxiliar | erros=0 ; `independente-adaptada/t5.json` |
| FILE-MAC | NAO_EXECUTADO | pendencia | file:// no Chrome/Mac do usuário; ambiente cloud bloqueou o protocolo; `Riscos-Pendencias-A5.md` |
| AUDITORIA-DEV4 | NAO_EXECUTADO | pendencia | Auditoria independente completa da DEV.4 pelo Claude; `Riscos-Pendencias-A5.md` |
| LEGADO-HTML61 | NAO_EXECUTADO | pendencia | Comparação no HTML 6.1 original não fornecido; somente fixtures v2 testadas; `Riscos-Pendencias-A5.md` |
| COTA-IDB-REAL | NAO_EXECUTADO | pendencia | Esgotamento físico real de IndexedDB: proteção testada por falha simulada, sem consumir a origem até seu limite; `Riscos-Pendencias-A5.md` |
| REGRESSAO-253-ORIGINAIS | NAO_EXECUTADO | pendencia | Reexecução integral dos 253 critérios originais: vários substituídos pelo A5; somente os críticos mapeados e SAN foram reexecutados; `Riscos-Pendencias-A5.md` |

## Critérios da auditoria reexecutados com a semântica A5

| Referência | Evidência atual | Mudança de critério |
|---|---|---|
| N1 / AJ-14 / AJ-15 | N1-220-OPERACOES-500/1500, COTA, VOLUME, IDB-FALHA | Cópia verificável no IndexedDB, sem exigir chaves por operação no localStorage; cota real mantém originais |
| N2 / AJ-11 | N2-BRUTO, V2-LEGADO, N2-V3 | Livro legível numérico incluído sem conversão; botão bruto independente da faixa |
| N3 | N3-SEM-FAIXA-ROTINEIRA / RISCO-REAL | Históricos válidos são rotina; quarentena/falha continua risco |
| AJ-11 / BKP-02 / B-100 | BKP02, BACKUP-ARQUIVO, HASH, PARCIAL | Novo v3 inclui bases e proteção; arquivo parcial explícito substitui recusa de toda exportação bruta |
| AJ-12 / B-06 / B-79 | BKP02-LAB-CHECKLISTS-QUARENTENAS, QUARENTENA-CONFLITO, N1-QUARENTENA | Quarentenas/revisões passam a integrar o snapshot; revisão não significa recuperação |
| P1-7b / A1-48 | P17B-PREIMAGE, A148, FALHA, INTERRUPCAO, RECUPERACAO | Preimage global e recuperação expressa; não só cópia financeira |
| B-119 / B-123 | B119-V2, B123, V2-PARCIAL | Legado íntegro sem IDs/valores convertidos; reload não reinjeta seed |
| P1-0 | P10-VERSAO-ACADEMIA-DESCONHECIDA | Versão desconhecida não pode sobrescrever raw |
| Central Sanitária | SAN-01…SAN-13 | Critérios independentes mantidos; transporte/espera/fixtures documentados |

Esse mapeamento não declara aprovação dos 253 casos originais. A4/merge e revisão clínica continuam fora da homologação. O caso METODO-FILE confirma o bloqueio documentado, não o funcionamento por file://.
