# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Sobre este repositório

Repositório de exemplos práticos para aprender a estender o Claude Code com **skills**, **agents/subagents** e **servidores MCP**. Toda configuração é local (`.claude/`) — nada é instalado globalmente.

## Configuração do servidor MCP

Antes de usar as ferramentas MCP, instale a dependência Python:

```bash
pip install mcp
```

Reinicie o Claude Code após instalar para que o servidor `exemplo` seja carregado.

## Skills disponíveis

| Comando | Uso |
|---------|-----|
| `/resumir <arquivo ou trecho>` | Resume código em português com propósito, I/O e pontos de atenção |
| `/revisar <arquivo>` | Revisão estruturada: bugs, segurança, qualidade |

## Agents/Subagents disponíveis

| Nome | Ferramentas | Quando usar |
|------|-------------|-------------|
| `revisor-codigo` | Read, Grep, Glob | Análise de qualidade, bugs e segurança de código |
| `pesquisador-docs` | Read, Grep, Glob, WebSearch, WebFetch | Pesquisa em documentação local ou web |

O Claude pode invocar esses agents automaticamente ou você pode solicitá-lo explicitamente.

## Ferramentas MCP (servidor `exemplo`)

Após instalar e reiniciar, as ferramentas ficam disponíveis como `mcp__exemplo__<nome>`:

| Ferramenta | Parâmetros |
|------------|------------|
| `mcp__exemplo__saudacao` | `nome: string` |
| `mcp__exemplo__calcular` | `a: number`, `b: number`, `operacao: "+" \| "-" \| "*" \| "/"` |
| `mcp__exemplo__formatar_json` | `entrada: string` |

## Estrutura de configuração local

```
.claude/
├── commands/          # Skills (slash commands)
│   ├── resumir.md
│   └── revisar.md
├── agents/            # Agents e subagents
│   ├── revisor-codigo.md
│   └── pesquisador-docs.md
└── settings.json      # Registro de servidores MCP

mcp-servidor/
├── servidor.py        # Implementação do servidor MCP
└── requirements.txt

docs/
├── guia-skills.md           # Como criar skills
├── guia-agents-subagents.md # Como criar agents e subagents
└── guia-mcp.md              # Como criar servidores MCP
```

## Documentação detalhada

- [Skills](docs/guia-skills.md)
- [Agents e Subagents](docs/guia-agents-subagents.md)
- [Servidor MCP](docs/guia-mcp.md)
