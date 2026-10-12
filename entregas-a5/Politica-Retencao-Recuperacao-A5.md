# Política de retenção e recuperação — DEV.4 A5

Somente dados fictícios. Não usar esta DEV com pacientes ou backups reais. Nenhuma implantação está autorizada. Aguarda auditoria independente.

## Classes de proteção

| Classe | Local | Política |
|---|---|---|
| Cópias anteriores a operações novas | IndexedDB DEV isolado | Criadas e relidas antes de cada gravação do livro. Sem remoção automática. |
| Cópias de operações herdadas | localStorage DEV | Preservadas; não migradas ou apagadas silenciosamente. Datas desconhecidas são declaradas. |
| Quarentenas, revisões e `ma-ledger-v1-prev` | localStorage DEV | Incluídas em bruto no v3. Não elegíveis à limpeza de operações. Conflito na restauração é recusado. Arquivar quarentena não equivale a recuperar lançamentos. |
| Preimages de restauração e comprovantes de limpeza | IndexedDB DEV | Retidos. Preimage contém bytes anteriores, destino, itens ignorados e resumo. Comprovante identifica arquivo externo e estados retirados. Sem rotina de exclusão. |
| Backup oficial v3 | Arquivo escolhido pelo usuário | Snapshot das bases persistidas e história disponível. Não inclui documentos externos nem campos não salvos. Históricos já liberados exigem os arquivos externos identificados; snapshot é PARCIAL. |
| Arquivos anteriores v2 | Arquivos externos | Permanecem intocados. Leitor v2 aceita os campos presentes; não inventa bases administrativas nem hash anterior. |

## Liberar espaço com recuperação

1. Na tela Backup, conferir tamanho estimado das bases e histórico. Os bytes UTF-16 são estimativas; a cota real é decidida pelo navegador.
2. Exportar o histórico. O download solicitado ainda não significa arquivo verificado.
3. Salvar fora do navegador e selecionar o arquivo efetivamente baixado em “Verificar histórico”. Guardar preferencialmente duas cópias independentes.
4. Selecionar somente cópias de operação já presentes com os bytes exatos nesse arquivo. Quarentenas, revisões, `-prev`, preimages e comprovantes não são elegíveis. A cópia de operação mais recente permanece no navegador.
5. Confirmar expressamente a seleção. O arquivo é relido antes e depois da confirmação; os originais selecionados são novamente comparados. Sem arquivo acessível/íntegro, a limpeza é bloqueada.
6. O comprovante de liberação permanece no IndexedDB. Guarde o arquivo externo identificado junto aos próximos backups: ele contém estados que esses snapshots não recriam.

Não executar limpeza global nem apagar o perfil. A API File prova acesso aos bytes naquele instante; não pode garantir que um usuário nunca apagará o arquivo externo ou que um disco não falhará. A retenção externa é responsabilidade explícita, não promessa de durabilidade absoluta.

## Restaurar ou recuperar

1. Fechar todas as outras abas e versões do Dashboard. A DEV.4 bloqueia automaticamente restauração enquanto outra DEV.4 cooperante mantém a mesma origem aberta. DEV.3, console ou outras aplicações não participam desse bloqueio.
2. Selecionar exclusivamente arquivo fictício. Formato v3 exige SHA-256 do envelope e de cada base; v2 não possui hash original e passa por validação estrutural.
3. Conferir prévia: dados atuais/arquivo, inclusões, substituições, bases ausentes mantidas, bases inválidas ignoradas, IDs repetidos/alterados. Não há deduplicação nem conversão monetária silenciosa.
4. Confirmar. Antes de substituir, a DEV.4 grava e relê uma preimage autocontida no IndexedDB, registra um marcador de recuperação e verifica reserva real de espaço.
5. No sucesso, o histórico guarda as contagens antes/depois e recarrega. Seeds embutidos ficam suprimidos. No erro, tenta recuperar os bytes anteriores. Novas proteções eventualmente adicionadas são retidas; nenhuma quarentena/revisão é apagada automaticamente.
6. Em interrupção, a recuperação ocorre antes de ativar os módulos na próxima abertura. Se a preimage ou marcador não conferir, ou outra aba impedir exclusividade, a aplicação bloqueia gravações e oferece exportação FORENSE das chaves acessíveis, claramente incompleta. Não contornar esse bloqueio.
7. Para desfazer uma restauração, abrir “Recuperar estado anterior de uma restauração”, preparar a prévia e confirmar. A recuperação é uma nova restauração, com nova preimage do estado atual. Bases antes ausentes e adicionadas por aquela restauração aparecem como remoção expressa na prévia; históricos de proteção são retidos.
8. Para recuperar uma cópia de operação já liberada, verificar o histórico externo, selecionar o estado do livro e preparar a prévia. Somente o livro será substituído; as demais bases permanecem. Uma nova preimage é obrigatória.

## Capacidade

As novas operações não consomem o pequeno limite do localStorage com cópias integrais. IndexedDB também tem limite, depende de espaço/origem e pode ser removido pelo navegador. Se falhar a proteção, bloquear a gravação; não prosseguir sem confirmação externa verificada. Não há retenção infinita ou limpeza automática. Backups/exportações usam memória: históricos muito maiores que os volumes testados podem exigir mais RAM ou ser recusados por falha do navegador. A reserva de restauração é conservadora e pode recusar um arquivo que teoricamente caberia.

Trocar de protocolo, host, porta ou perfil muda a origem e pode tornar bases locais anteriores invisíveis. Não presumir migração entre file:// e HTTP. Use arquivos externos e valide na origem de destino; este pacote não instala ou migra dados.
