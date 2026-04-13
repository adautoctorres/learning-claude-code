# learning-ai

Exemplos práticos para aprender a estender o **Claude Code** com skills, agents/subagents e servidores MCP. Toda configuração é local (`.claude/`) — nada é instalado globalmente.

## Estrutura

```
.
├── .claude/
│   ├── agents/          # Definições de agents/subagents
│   ├── commands/        # Skills (slash commands)
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

## Skills (slash commands)

| Comando | O que faz |
|---------|-----------|
| `/resumir <arquivo>` | Resume código em português com propósito, I/O e pontos de atenção |
| `/revisar <arquivo>` | Revisão estruturada: bugs, segurança e qualidade |

## Agents/Subagents

| Agent | Especialidade |
|-------|---------------|
| `revisor-codigo` | Análise de qualidade, bugs e segurança de código |
| `pesquisador-docs` | Pesquisa em documentação local ou web |

Exemplo de uso explícito:
```
Analise este arquivo e depois delegue a revisão ao agent especializado.
```

## Servidores MCP

### Registrar

```bash
# Servidor de soma
claude mcp add --scope local mcp-somar python mcp/mcp-somar.py

# Servidor de mensagem
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

- [Skills](docs/guia-skills.md)
- [Agents e Subagents](docs/guia-agents-subagents.md)
- [Servidor MCP](docs/guia-mcp.md)
