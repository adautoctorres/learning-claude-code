# learning-ai

Exemplos práticos para aprender a estender o **Claude Code** com skills, agents/subagents e servidores MCP. Toda configuração é local (`.claude/`) — nada é instalado globalmente.

## Estrutura

```
.
├── .claude/
│   ├── agents/          # Definições de agents/subagents
│   ├── commands/        # Slash commands simples (atalhos de prompt)
│   ├── skills/          # Skills avançadas com templates e lógica própria
│   └── settings.json    # Configuração local (MCP, permissões)
├── docs/                # Guias detalhados
├── mcp/                 # Servidores MCP em Python
└── src/                 # Exemplos de uso da API Anthropic
```

## Pré-requisitos

```bash
python -m venv .venv
.venv/bin/pip install mcp anthropic
```

## Skills e Slash Commands

Há dois tipos de comandos disponíveis neste projeto:

**Slash commands simples** — arquivo único em `.claude/commands/`:

| Comando | O que faz |
|---------|-----------|
| `/resumir-cmd <arquivo>` | Resume código em português com propósito, I/O e pontos de atenção |
| `/revisar-cmd <arquivo>` | Revisão estruturada: bugs, segurança e qualidade |
| `/gitlab <descrição>` | Formata atividade para o GitLab usando templates markdown |

**Skills avançadas** — pasta própria em `.claude/skills/` com templates e recursos:

| Skill | O que faz |
|-------|-----------|
| `gitlab-formatter` | Formata issues, MRs e épicos para GitLab com templates em `assets/` |
| `skill-creator` | Cria e itera novas skills com evals e benchmark automatizados |

## Agents/Subagents

| Agent | Especialidade |
|-------|---------------|
| `revisor-codigo-agent` | Análise de qualidade, bugs e segurança de código |
| `pesquisador-docs-agent` | Pesquisa em documentação local ou web |

O Claude pode invocar esses agents automaticamente ou você pode solicitar explicitamente:
```
Analise este arquivo e depois delegue a revisão ao agent especializado.
```

## Servidores MCP

### Registrar

```bash
claude mcp add --scope local mcp-somar python mcp/mcp-somar.py
claude mcp add --scope local mcp-mensagem python mcp/mcp-mensagem.py
```

### Remover

```bash
claude mcp remove mcp-somar --scope local
claude mcp remove mcp-mensagem --scope local
```

### Ferramentas disponíveis

| Ferramenta MCP | Parâmetros |
|----------------|------------|
| `mcp__mcp-somar__somar` | `a: int`, `b: int` |
| `mcp__mcp-mensagem__enviar_mensagem` | `mensagem: str` |

## Exemplo de uso da API Anthropic

```bash
ANTHROPIC_API_KEY=sua-chave .venv/bin/python src/exemplo_claude.py
```

## Documentação

- [Skills e Slash Commands](docs/guia-skills.md)
- [Agents e Subagents](docs/guia-agents-subagents.md)
- [Servidor MCP](docs/guia-mcp.md)
