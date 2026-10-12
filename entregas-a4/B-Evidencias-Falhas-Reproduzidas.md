# A4 — Evidências reproduzíveis

✓ Confirmado: DEV.4 original SHA-256 `cc1da21a717db0e2f2bd7303284a3fd0b3af4c14be8638abb71741bfddc5fcbb`, Chromium 154.0.8037.57, Playwright 1.62.0, Python 3.12.14. HTTP somente em 127.0.0.1, portas descartáveis. Perfis Chromium novos, fixture com paciente pA, pagamento rA, evolução nA, livro Cora:F1 e bases administrativas fictícias. Todas as requisições fora da origem local foram bloqueadas. Nenhum perfil pessoal, paciente real ou importação real foi usado.

## T02/T04 — Sobrescrita clínica e financeira clínica

Estado inicial: ambas as abas carregam care A; pagamento rA=12345 centavos, evolução nA pendente. Abrir A e B no mesmo contexto descartável. A cadastra “Paciente Fictício recente A”, edita pagamento pela interface para R$987,65 e marca evolução como lançada. B conserva cache antigo. Importar em B fixture T02.json pelo input original #ma53-merge-file e aceitar confirmação.

Esperado: preservar todos os dados recentes de A ou recusar a operação; a preimage precisa refletir o estado persistido imediatamente anterior.

✗ Observado: paciente recente desaparece; rA volta de 98765 para 12345 centavos; nA volta de true para false. O feedback informa sucesso e preservação dos anteriores. A cópia ANTES-MESCLAR contém care antigo e não inclui as alterações recentes. O journal A5 de merge não existe.

Evidência: `execucoes/T02-duas-abas.json`, `resultados/T-A4-02.json`, `resultados/T-A4-04.json`, download indicado em seus campos. Os JSON contêm raw inicial, histórico, care corrente anterior, estado final e feedback. O teste usa handlers originais, sem alteração do algoritmo.

## T08 — Perda de lançamento bancário na janela de confirmação

Estado inicial: Cora:F1.amount=1001. B abre o merge e fica com o diálogo original de confirmação pendente. A aplica correção normal pelo mecanismo bancário protegido, `ma62ApplyCorrection`, para amount=99999 e confirma gravação. Depois aceitar o diálogo em B.

Esperado: reconhecer revisão nova e recusar/recalcular, preservando 99999.

✗ Observado: B escreve lista capturada antes do diálogo; Cora:F1 volta a 1001, nova linha F2 entra. O histórico da correção normal preserva o valor anterior 1001, e não constitui um journal da mesclagem com o valor recente 99999. A cópia externa solicitada pode conter livro mais recente, mas isso não torna a operação atômica ou recuperável por journal A5.

Evidência: `execucoes/T08-livro-concorrente.json`, resultado T08 e log grupo7. Os dados são inteiramente fictícios.

## T26 — CAS clínico não atômico entre abas

A prepara um novo paciente. O Debugger pausa uma instrumentação temporária antes do setItem clínico, depois da comparação original. B salva outro paciente pela UI. A retoma, sem remover comparação, guard ou validador.

✗ Observado: B informa cadastro salvo; após A retomar, o paciente de B desaparece. Evidência: `resultados/T-A4-26.json`, execução grupo10. Esta é uma corrida deliberadamente forçada; não estima frequência em uso normal. A escrita bancária normal, por contraste, recusou estado stale nos subcasos do grupo3.

## T05 — Rollback incompleto

Falhas transitórias da segunda e terceira escrita foram injetadas no perfil descartável: nesses subcasos houve retorno exato. Outro subcaso faz a primeira escrita clínica funcionar, impede a escrita bancária e impede também a restauração clínica no catch original.

✗ Observado: care mesclado permanece, livro anterior permanece, guard vazio, nenhum journal de merge. Feedback diz que tentou restaurar. Evidência: `execucoes/T05-rollback-falha.json` e `T05-terceira-escrita.json`. É injeção de falha, não ocorrência espontânea nem correção do aplicativo.

## T01/T03/T09/T30 — Modelos e telas antigos

Após merge válido, localStorage tem 2 linhas bancárias, rows mantém 1; note-list não mostra evolução nova. Navegar pelas 18 telas não atualiza rows. A próxima escrita normal é recusada pelas referências antigas. Evidências T01, T03, T09 e T30. A recusa protege contra outra sobrescrita, mas a UI continua desatualizada.

## T27/T28 — Escritores sem comparação

B salva taxa 2x; A salva taxa 3x com mapa antigo e apaga a taxa de B. B marca tarefa 1; A marca tarefa 2 e apaga a tarefa 1. Evidências grupo3, T27/T28/T29. Operações originais pelo DOM; nenhuma falha de storage foi necessária.

## T33/T34/T35/T36 — Estado não confirmado apresentado/exportado

Quota física foi preenchida em chaves fictícias até o limite efetivo. Taxa 3x não é persistida; status avisa falha, mas campo diz “Personalizada · salva”. Falha injetada de inclusão de material deixa objeto em memória; export específico contém 2 materiais, v3 persistido contém 1. Repetir inclusão persiste 2 materiais iguais. Anotação sanitária recusada também aparece no export específico. Evidências/downloads nos resultados T33–T36. Não foi preenchida quota física de IndexedDB.

## T37/T38 — Reidratação da Academia

Importar Academia B com ma58.base=A3 e primeiro check=true. O pai persistido contém B, mas ma58 renderiza A2. Mudar o alvo pelo handler original do filho faz base/checks voltarem a A. Evidência: `execucoes/T38-reidratacao.json`. Este subcaso demonstra o defeito em ma58; não presume execução equivalente em todos os campos ma59/ma60.

## T12–T23/T40/T41 — Integridade e interface

Mesmo ID divergente não recebe conflito; IDs diferentes permitem duplicação semântica. Colisão de ID de paciente aceita novo pagamento vinculado ao cadastro preexistente. Duplicados bancários internos divergentes recebem “mesclado”, primeiro vence. Version=99 é aceita. Linha financeira inválida entra no ativo. Taxa 150 pode ser persistida quando base ausente. Nome sem CPF é suficiente para fusão Codental. Origem histórica sem proveniência permite atualização de campo. Mês janeiro/2027 muda para outubro/2026. Apuração ma57 troca taxa manual 12.34 por 10 automática; o snapshot histórico do pagamento é corretamente preservado e explicado pela interface.

Cada cenário tem fixture, resultado/oráculo e raw em `resultados/` e `execucoes/`. Ausência de execução XSS em T20 não aprova a validação financeira nem certifica segurança XSS universal.

## NÃO TESTADOS e tentativas técnicas

○ T07: três tentativas de interrupção com Debugger/crash não permitiram reabrir e verificar estado final pela automação. Não afirmar rollback, perda ou recuperação desse cenário. Os logs registram a limitação; fases journal/marker de merge não existem na implementação atual.

○ T32: file:// bloqueado por ERR_BLOCKED_BY_ADMINISTRATOR. HTTP local e APIs indisponíveis executados; locks/IndexedDB ausentes impediram prontidão do aplicativo. Sentinelas fictícias permaneceram intactas nas verificações auxiliares executadas. Nenhuma flag contornou a política.

○ T42: baseline original medido (seed/feed original: aproximadamente 12,36s na função, 4892 pacientes resultantes, pending=0). Comparação com candidata indisponível porque nenhuma correção foi autorizada/existe. Não aprovar equivalência ou meta de performance.

Aberturas frias/quentes T43: medianas aproximadas 27,21s/26,39s nesta máquina com carga de testes; amostra n=3 cada. Máximos amostrais 28,71s/40,38s, não p95 populacional. Navegação mede round-trip do driver. Nenhuma proteção foi removida por desempenho.
