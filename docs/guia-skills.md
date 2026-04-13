# Skills e Slash Commands

Este projeto usa dois mecanismos complementares para estender o Claude Code com comandos personalizados: **slash commands simples** e **skills avançadas**.

---

## Slash Commands simples

Slash commands são arquivos `.md` em `.claude/commands/`. Quando você digita `/resumir-cmd src/main.py`, o Claude Code:

1. Localiza `.claude/commands/resumir-cmd.md`
2. Substitui `$ARGUMENTS` pelo texto que você passou (`src/main.py`)
3. Executa o prompt resultante como uma nova instrução

### Estrutura do arquivo

```
.claude/commands/nome-do-comando.md
```

```markdown
---
description: Descrição curta — aparece no autocompletar do Claude Code
allowed-tools: Read, Grep, Glob
---

Corpo do prompt.

Use $ARGUMENTS para referenciar o que o usuário passou após o comando.
```

### Campos do frontmatter

| Campo | Obrigatório | Descrição |
|-------|-------------|-----------|
| `description` | Não | Texto exibido no autocomplete |
| `allowed-tools` | Não | Ferramentas permitidas. Se omitido, herda as permissões da sessão |

### Ferramentas disponíveis

`Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`, `WebSearch`, `WebFetch`, `Agent`, e qualquer ferramenta MCP configurada.

### Slash commands neste projeto

| Comando | Arquivo | O que faz |
|---------|---------|-----------|
| `/resumir-cmd` | `.claude/commands/resumir-cmd.md` | Resume código/arquivo em pt-br |
| `/revisar-cmd` | `.claude/commands/revisar-cmd.md` | Revisão estruturada de código |
| `/gitlab` | `.claude/commands/gitlab.md` | Formata atividades para o GitLab |

### Como usar

```
/resumir-cmd src/main.py
/revisar-cmd src/auth.py
/gitlab bug no login com email inválido
```

---

## Skills avançadas

Skills são pastas em `.claude/skills/` com um `SKILL.md` e recursos opcionais (templates, scripts, referências). O Claude carrega a skill quando identifica que a tarefa se encaixa na sua descrição.

### Anatomia de uma skill

```
.claude/skills/nome-da-skill/
├── SKILL.md              # Instrução principal + frontmatter
└── assets/               # Templates, exemplos, arquivos de suporte
    ├── template-x.md
    └── template-y.md
```

### Estrutura do SKILL.md

```markdown
---
name: nome-da-skill
description: Quando usar esta skill e o que ela faz. Seja específico — este texto é o mecanismo de disparo.
---

Instruções detalhadas para o Claude seguir ao executar a skill.
```

### Skills neste projeto

| Skill | Pasta | O que faz |
|-------|-------|-----------|
| `gitlab-formatter` | `.claude/skills/gitlab-formatter/` | Formata issues, MRs e épicos com templates em `assets/` |
| `skill-creator` | `.claude/skills/skill-creator/` | Cria e itera novas skills com evals automatizados |

#### gitlab-formatter

Formata atividades para o GitLab usando templates de markdown. Identifica o tipo de atividade (bug, feature, MR, épico) e preenche o template correspondente com as informações fornecidas.

Templates disponíveis em `.claude/skills/gitlab-formatter/assets/`:

| Template | Quando usar |
|----------|-------------|
| `template-bug.md` | Erros, falhas, comportamentos inesperados |
| `template-feature.md` | Novas funcionalidades, melhorias, histórias |
| `template-mr.md` | Merge requests |
| `template-epic.md` | Épicos com múltiplas issues filhas |

Para usar seus próprios templates, basta adicionar arquivos `.md` na pasta `assets/` — a skill detecta automaticamente.

**Disparo via comando:**
```
/gitlab bug no login com email inválido
/gitlab quero criar um épico para o módulo de pagamentos
```

**Disparo automático:** escreva algo como "quero abrir uma issue" ou "cria um MR para esse fix" e a skill é acionada.

---

## Escopo: local vs global

| Local (projeto) | Global (usuário) |
|-----------------|------------------|
| `.claude/commands/` | `~/.claude/commands/` |
| `.claude/skills/` | `~/.claude/skills/` |
| Só disponível neste projeto | Disponível em qualquer projeto |

Este projeto usa **apenas configuração local**.
