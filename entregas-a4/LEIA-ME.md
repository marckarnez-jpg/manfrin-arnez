# Entrega — testes/reprodução A4 da DEV.4

Somente diagnóstico experimental, dados sintéticos, nenhum código do Dashboard modificado. Consulte A-Matriz-43-Testes.md, B-Evidencias-Falhas-Reproduzidas.md, C-Riscos-Classificados.md, D-Proposta-Bloqueio-Preventivo-Merge.md e E-Recomendacoes-DEV5-Condicionais.md. Os seis documentos anteriores foram copiados sem alteração em diagnostico-a4-anterior; hashes em Conferencia-Seis-Documentos.json.

O risco crítico de sobrescrita foi confirmado. A suspensão do merge é uma recomendação; nenhum bloqueio/correção foi aplicado. Esta entrega não substitui a auditoria Claude.

## Conteúdo e reprodução

Esta publicação é exclusivamente documental: não contém HTML do Dashboard nem o scaffold A5. Use a DEV.4 original, sem modificá-la, para repetir os testes. Os hashes esperados estão em execucoes/Verificacao-Fontes-Imutaveis.json. Os manuais técnicos PDF não são redistribuídos; suas hashes/verificações T39 permanecem nos resultados. Não inclui site institucional, Git, credenciais, perfil Chromium ou dados reais. O runner cria perfis descartáveis e bloqueia tráfego externo; o servidor vincula somente 127.0.0.1.

No Mac, em uma pasta descartável, com Python 3 instalado:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install playwright==1.62.0
python3 -m playwright install chromium
A4_SOURCE_DIR="/caminho/para/fontes-originais-a5" python3 executar.py 7
```

Grupo7 reproduz a janela de confirmação do merge bancário. Grupo1 reproduz a sobrescrita clínica em duas abas. Os demais grupos: 2 validações/conflitos; 3 concorrência/exports; 4 Academia/restore; 6 protocolo/quota real; 8 baseline; 9 política Codental; 10 corrida clínica forçada; 11 subcasos/PDFs/epoch; 12 sync/restore; 13 rollback. Execute sequencialmente em uma cópia desta entrega: os resultados são gravados na pasta do runner e sobrescrevem saídas de execuções anteriores.

Group5 é NÃO TESTADO por incapacidade de completar verificação após crash. O experimento de encerramento de renderers fica desabilitado por padrão; não recomenda-se habilitá-lo nesta máquina ou inferir resultados a partir dos logs das tentativas. Nenhuma flag para contornar file:// foi usada. O suporte file:// no Mac continua por verificar.

A4_SOURCE_DIR permite indicar outra pasta com as duas fontes; A4_CHROMIUM permite selecionar binário Chromium. Os hashes devem coincidir antes de executar. O runner nunca deve ser apontado a perfil ou backup com dados reais.

## Evidência e limites

resultados contém um JSON por caso, com cenário/oráculo/resultado, observação e execução principal. execucoes contém logs, raw e histórico das tentativas. Downloads foram salvos efetivamente e lidos quando aplicável; uma mensagem de download solicitado não foi tratada como arquivo verificado. Erros do harness e tentativas substituídas são conservados, não contam como aprovação do aplicativo. Detalhes de cobertura estão na matriz.

Publicação autorizada exclusivamente na branch dev/a4-testes-reproducao. O ZIP reúne os documentos, resultados e evidências sintéticas. Nenhuma alteração de código, PR, merge ou implantação é autorizada nesta etapa. Histórico próprio sem commits anteriores do site ou do Dashboard.

## Fontes originais para reprodução

As fontes permanecem na entrega A5 já publicada, sem alteração nesta etapa: [DEV.4 original](https://github.com/marckarnez-jpg/manfrin-arnez/blob/206bd06f24db985fbc9ecb92ed2eea7a270b5f01/entregas-a5/Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html) e [scaffold A5](https://github.com/marckarnez-jpg/manfrin-arnez/blob/206bd06f24db985fbc9ecb92ed2eea7a270b5f01/entregas-a5/testes_a5.py). Guarde ambos na mesma pasta e indique A4_SOURCE_DIR. Os PDFs baixados durante os testes foram verificados, mas seus binários técnicos estão excluídos desta publicação documental; registros originais de paths permanecem como evidência histórica.
