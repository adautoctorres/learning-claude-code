# Agents e Subagents

## Conceitos

**Agent** é uma definição de um assistente especializado com prompt de sistema próprio, modelo específico e conjunto restrito de ferramentas.

**Subagent** é o mesmo conceito visto pelo ângulo de quem invoca: quando o Claude principal delega uma tarefa a um agent definido, esse agent está atuando como *subagent* — ele roda em contexto isolado e retorna apenas o resultado final.

A mesma definição em `.claude/agents/` serve tanto para uso autônomo (o Claude decide invocar) quanto para uso explícito (você pede).

## Estrutura do arquivo

```
.claude/agents/nome-do-agent.md
```

```markdown
---
name: nome-do-agent
description: Descrição detalhada — o Claude usa este texto para decidir quando invocar o agent autonomamente.
model: sonnet
tools: Read, Grep, Glob
---

System prompt do agent.

Defina aqui o comportamento, restrições, formato de resposta
e qualquer instrução permanente para este especialista.
```

### Campos do frontmatter

| Campo | Obrigatório | Descrição |
|-------|-------------|-----------|
| `name` | Sim | Identificador do agent |
| `description` | Sim | Texto que o Claude lê para decidir quando usar o agent |
| `model` | Não | Modelo a usar. Padrão: herda do pai |
| `tools` | Não | Ferramentas permitidas. Se omitido, herda do pai |

### Modelos disponíveis

| ID | Uso recomendado |
|----|-----------------|
| `opus` | Tarefas complexas, raciocínio profundo |
| `sonnet` | Uso geral — bom equilíbrio velocidade/qualidade |
| `haiku` | Tarefas simples, alta velocidade |
| `inherit` | Usa o mesmo modelo do agente pai (padrão) |

## Agents neste projeto

| Agent | Arquivo | Especialidade | Ferramentas |
|-------|---------|---------------|-------------|
| `revisor-codigo-agent` | `.claude/agents/revisor-codigo-agent.md` | Revisão de qualidade, bugs e segurança | Read, Grep, Glob, mcp__ide__getDiagnostics |
| `pesquisador-docs-agent` | `.claude/agents/pesquisador-docs-agent.md` | Pesquisa em docs locais e web | Read, Grep, Glob, WebSearch, WebFetch |

## Como o Claude invoca agents automaticamente

O Claude lê o campo `description` de todos os agents disponíveis. Se uma tarefa corresponde à descrição, ele pode invocar o agent sem você precisar pedir. Quanto mais precisa a `description`, melhor o match.

**Exemplo:** se você pedir *"revise o arquivo auth.py"*, o Claude pode automaticamente delegar ao `revisor-codigo-agent` porque a description menciona "revisão de código".

## Como invocar explicitamente

Em prompts ou skills, você pode pedir ao Claude que delegue a um agent:

```
Analise este arquivo e depois delegue a revisão ao agent especializado.
```

O Claude usará a ferramenta `Agent` internamente com o `subagent_type` correspondente.

## Isolamento de contexto

Subagents **não veem o histórico da conversa principal**. Eles recebem apenas:
- O prompt da tarefa que lhes foi passada
- Seu próprio system prompt (o corpo do `.md`)

Isso mantém o contexto limpo e evita vazamento de informações entre tarefas.

## Escopo: local vs global

| Local (projeto) | Global (usuário) |
|-----------------|------------------|
| `.claude/agents/` | `~/.claude/agents/` |
| Só disponível neste projeto | Disponível em qualquer projeto |

Este projeto usa **apenas configuração local**.
