---
name: cofre-memoria
description: 'Protocolo de contexto: consultar o cofre Obsidian, depois a memória, e salvar no cofre o que foi útil ao terminar.'
applyTo: '**'
---

# Protocolo cofre → memória → cofre

Vale para toda sessão, em qualquer agente. O cofre é o Obsidian em
`C:/Users/Raf_F/Documents/obsidian/rfsprod`.

## 1. Antes de agir: procure no cofre

1. Use `obsidian-vault/search_notes` com os termos do pedido (projeto, erro,
   componente, endpoint, pessoa). Tente ao menos dois termos diferentes antes
   de concluir que não há nada.
2. Abra as notas relevantes com `obsidian-vault/read_notes`. Comece por
   `index.md` quando não souber onde procurar.
3. Use o que encontrar e diga, em uma linha, qual nota serviu de base.

## 2. Se o cofre não tiver: procure na memória

1. `memory/search_nodes` e `memory/open_nodes` (grafo de conhecimento).
2. Se ainda faltar, `memory-cht-reader` (histórico de chats do VS Code).
3. Não encontrou em nenhum dos dois: siga investigando no código e nas fontes
   normais. Nunca invente o que deveria estar registrado.

## 3. Ao terminar a tarefa: salve no cofre

Salve quando a sessão produziu algo reutilizável: decisão, causa raiz de bug,
solução validada, comando ou configuração que funcionou, convenção do projeto.
Não salve conversa trivial, tentativa que falhou sem lição, nem segredo
(senha, token, connection string com credencial).

Grave com `cofre-fs/write_file` (nota nova) ou `cofre-fs/edit_file` (nota
existente). Antes de criar, procure se já existe nota sobre o assunto e
prefira atualizá-la.

- **Onde:** `Dev Logs/AAAA-MM-DD - <assunto curto>.md` para trabalho técnico;
  `Knowledge/<assunto>.md` para conhecimento permanente;
  `Projects/<projeto>.md` para estado de projeto.
- **Log do dia:** acrescente uma linha em `Logs/AAAA-MM-DD.md`
  (`- HH:MM copilot: <o que foi salvo> → [[nome da nota]]`). Crie o arquivo se
  não existir. Nunca reescreva linhas antigas.
- **Formato de toda nota:**

```markdown
---
type: dev-log | knowledge | project
date: AAAA-MM-DD
topic: <assunto>
tags: [copilot, <tags>]
related-projects: ["[[Projeto]]"]
sources: [<caminhos de arquivo, URLs>]
confidence: stated | high | medium | speculation
---

## For future agent
<2 a 3 frases dizendo do que se trata e quando esta nota é útil>

## Contexto
## O que foi feito / decidido
## Como validar
```

- Use `[[wikilinks]]` para projetos, pessoas e conceitos citados.
- Coloque data em fatos externos ("versão X, em AAAA-MM-DD") e a URL da fonte.
- Escreva o corpo em português; chaves do frontmatter e nomes de pasta em inglês.
- Alterar nota existente com base em fonte externa: proponha e peça confirmação.
  Apagar ou arquivar nota: sempre peça confirmação.

Ao final da resposta, informe em uma linha o que foi salvo e onde, ou
"Cofre: nada novo a salvar".
