# Entrega A5 — DEV.4 fictícia

O HTML principal é `Manfrin-Arnez-Dashboard-6.2-DEV-04-A5.html`. A DEV.3 original está em `referencias/`, byte a byte preservada. Não substituir o site institucional. Não usar dados, backups ou perfil do Chrome reais. Aguarda auditoria independente antes de implantação.

Leia o relatório, a matriz e as políticas antes de testar. Extraia todo o ZIP; `SHA256SUMS.txt` permite conferir os arquivos com `shasum -a 256 -c SHA256SUMS.txt` no Mac. O hash externo do ZIP é informado separadamente; não pode estar dentro de si mesmo.

## Reprodução dos testes

Python 3.12, pacote Python Playwright, Chromium/Chrome compatível. Cada teste cria contextos descartáveis e seu próprio servidor em 127.0.0.1 com porta livre, bloqueando tráfego externo. Não acessa o perfil principal do navegador. Nenhum teste executa clear().

Na pasta extraída:

```sh
python3 testes_n1_n2_n3.py
python3 testes_a5.py
```

O binário padrão é `/usr/bin/chromium`. Se outro Chromium for usado, definir `CHROMIUM_BIN` com seu caminho. No Mac, por exemplo:

```sh
CHROMIUM_BIN='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' python3 testes_a5.py
```

O teste por file:// tenta abrir somente o HTML fictício em um contexto isolado. O ambiente cloud bloqueou esse protocolo, por isso os testes de comportamento usaram HTTP local. Testar file:// no Mac é uma pendência, não um resultado aprovado desta execução. Se precisar abrir para avaliação por HTTP local, pode usar `python3 -m http.server 8765 --bind 127.0.0.1` e acessar o HTML em `http://127.0.0.1:8765/`; isso cria outra origem e não migra dados anteriores.

Para repetir apenas um grupo: `python3 testes_a5.py --group recoveryedge` (ou unified, legacy, partial, failure, tabs, volume, safety, regression, filecheck). A matriz entregue corresponde às execuções finais registradas, não aos diagnósticos intermediários.

A reexecução dos 13 casos sanitários da suíte independente requer Node e pacote Node Playwright: `python3 independente-adaptada/executar.py`. As adaptações e a origem estão documentadas nessa pasta. Esta reexecução pelo Codex não substitui nova auditoria do Claude.

## Código e evidências

`fontes/` contém o novo código legível e gerador. `python3 fontes/build_dev4.py` reproduz o HTML a partir da DEV.3 fornecida, exigindo seu SHA-256 conhecido. O gerador modifica somente a saída DEV.4.

`resultados-a5/`, `resultados-fase1.json`, logs e `independente-adaptada/t5.json` registram os testes executados. Os JSONs em downloads e os históricos exportados são exclusivamente fictícios. Não importar esses arquivos em um Dashboard com dados reais. O resultado da Fase 1 original, anterior ao desenvolvimento do backup A5, é separado da regressão final.

## Download externo

A publicação de uma nova branch de desenvolvimento depende de confirmação expressa. Nenhum link interno `/workspace/` deve ser considerado download externo. Não há push, merge, implantação ou alteração da branch principal autorizados nesta entrega.
