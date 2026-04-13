# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Sobre este repositório

Repositório de exemplos práticos para aprender a estender o Claude Code com **skills**, **agents/subagents** e **servidores MCP**. Toda configuração é local (`.claude/`) — nada é instalado globalmente.

## Configuração do servidor MCP

O servidor MCP usa um virtualenv local. Para configurar:

```bash
python -m venv .venv
.venv/bin/pip install mcp
```

O servidor é registrado em `.claude/settings.json` e executa `mcp/meu-mcp.py` via `.venv/bin/python`. Reinicie o Claude Code após qualquer alteração na configuração.

## Skills disponíveis

| Comando | Uso |
|---------|-----|
| `/resumir <arquivo ou trecho>` | Resume código em português com propósito, I/O e pontos de atenção |
| `/revisar <arquivo>` | Revisão estruturada: bugs, segurança, qualidade |

## Agents/Subagents disponíveis

| Nome | Ferramentas | Quando usar |
|------|-------------|-------------|
| `revisor-codigo` | Read, Grep, Glob, mcp__ide__getDiagnostics | Análise de qualidade, bugs e segurança de código |
| `pesquisador-docs` | Read, Grep, Glob, WebSearch, WebFetch | Pesquisa em documentação local ou web |

O Claude pode invocar esses agents automaticamente ou você pode solicitá-lo explicitamente.

## Ferramentas MCP (servidor `meu-mcp`)

Disponíveis como `mcp__meu-mcp__<nome>`:

| Ferramenta | Parâmetros |
|------------|------------|
| `mcp__meu-mcp__somar` | `a: int`, `b: int` |
| `mcp__meu-mcp__enviar_mensagem` | `mensagem: string` |

O servidor está em `mcp/meu-mcp.py` e usa `FastMCP` da biblioteca `mcp`.

## Documentação detalhada

- [Skills](docs/guia-skills.md)
- [Agents e Subagents](docs/guia-agents-subagents.md)
- [Servidor MCP](docs/guia-mcp.md)
