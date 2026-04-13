# Skills (Slash Commands)

Skills são comandos personalizados invocados com `/nome-do-comando` dentro de uma sessão do Claude Code.

## Como funcionam

Cada skill é um arquivo `.md` em `.claude/commands/`. Quando você digita `/resumir caminho/arquivo.py`, o Claude Code:

1. Localiza `.claude/commands/resumir.md`
2. Substitui `$ARGUMENTS` pelo texto que você passou (`caminho/arquivo.py`)
3. Executa o prompt resultante como uma nova instrução

## Estrutura do arquivo

```
.claude/commands/nome-do-comando.md
```

```markdown
---
description: Descrição curta — aparece no autocompletar do Claude Code
allowed-tools: Read, Write, Bash, Grep, Glob
---

Corpo do prompt.

Use $ARGUMENTS para referenciar o que o usuário passou após o comando.
```

### Campos do frontmatter

| Campo | Obrigatório | Descrição |
|-------|-------------|-----------|
| `description` | Não | Texto exibido no autocomplete |
| `allowed-tools` | Não | Lista de ferramentas permitidas. Se omitido, herda as permissões da sessão |

### Ferramentas disponíveis

`Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`, `WebSearch`, `WebFetch`, `Agent`, e qualquer ferramenta MCP configurada (ex: `mcp__exemplo__saudacao`).

## Exemplos neste projeto

| Comando | Arquivo | O que faz |
|---------|---------|-----------|
| `/resumir` | `.claude/commands/resumir.md` | Resume código/arquivo em pt-br |
| `/revisar` | `.claude/commands/revisar.md` | Revisão estruturada de código |

## Como usar

```
/resumir src/main.py
/revisar src/auth.py
/resumir "explique esta função: def processar(dados): ..."
```

## Escopo: local vs global

| Local (projeto) | Global (usuário) |
|-----------------|------------------|
| `.claude/commands/` | `~/.claude/commands/` |
| Só disponível neste projeto | Disponível em qualquer projeto |

Este projeto usa **apenas configuração local**.
