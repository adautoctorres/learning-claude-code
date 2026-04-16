# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Sobre este repositório

Repositório de exemplos práticos para aprender a estender o Claude Code com **skills**, **agents/subagents** e **servidores MCP**. Toda configuração é local (`.claude/`) — nada é instalado globalmente.

## Configuração do servidor MCP

Os servidores MCP usam um virtualenv local. Para configurar:

```bash
python -m venv .venv
.venv/bin/pip install mcp
```

Registre os servidores com o CLI do Claude Code:

```bash
claude mcp add --scope local mcp-somar python mcp/mcp-somar.py
claude mcp add --scope local mcp-mensagem python mcp/mcp-mensagem.py
claude mcp add --scope local mcp-oracle python mcp/mcp-oracle.py
claude mcp add --scope local mcp-teams python mcp/mcp-teams.py
```

O servidor `mcp-oracle` requer a lib `oracledb` e três variáveis de ambiente:

```bash
.venv/bin/pip install oracledb
export ORACLE_USER=usuario
export ORACLE_PASSWORD=senha
export ORACLE_DSN=host:1521/service_name
```

O servidor `mcp-teams` requer as libs `msal` e `httpx` e três variáveis de ambiente:

```bash
.venv/bin/pip install msal httpx
export TEAMS_TENANT_ID=seu-tenant-id
export TEAMS_CLIENT_ID=seu-client-id
export TEAMS_CLIENT_SECRET=seu-client-secret
```

Reinicie o Claude Code após registrar ou alterar servidores MCP.

## Slash commands disponíveis

| Comando | Arquivo | Uso |
|---------|---------|-----|
| `/resumir-cmd` | `.claude/commands/resumir-cmd.md` | Resume código em português com propósito, I/O e pontos de atenção |
| `/revisar-cmd` | `.claude/commands/revisar-cmd.md` | Revisão estruturada: bugs, segurança, qualidade |
| `/gitlab` | `.claude/commands/gitlab.md` | Formata atividades para o GitLab (issue, MR, épico) com templates |

## Skills disponíveis

| Skill | Pasta | Quando é acionada |
|-------|-------|-------------------|
| `gitlab-formatter` | `.claude/skills/gitlab-formatter/` | Ao mencionar issue, MR, épico ou qualquer atividade GitLab |
| `skill-creator` | `.claude/skills/skill-creator/` | Ao criar ou melhorar skills com evals |

## Agents/Subagents disponíveis

| Nome | Arquivo | Ferramentas | Quando usar |
|------|---------|-------------|-------------|
| `revisor-codigo-agent` | `.claude/agents/revisor-codigo-agent.md` | Read, Grep, Glob, mcp__ide__getDiagnostics | Análise de qualidade, bugs e segurança de código |
| `pesquisador-docs-agent` | `.claude/agents/pesquisador-docs-agent.md` | Read, Grep, Glob, WebSearch, WebFetch | Pesquisa em documentação local ou web |

O Claude pode invocar esses agents automaticamente ou você pode solicitá-lo explicitamente.

## Ferramentas MCP disponíveis

| Ferramenta | Parâmetros |
|------------|------------|
| `mcp__mcp-somar__somar` | `a: int`, `b: int` |
| `mcp__mcp-mensagem__enviar_mensagem` | `mensagem: string` |
| `mcp__mcp-oracle__executar_query` | `sql: string`, `parametros?: dict` |
| `mcp__mcp-oracle__executar_dml` | `sql: string`, `parametros?: dict` |
| `mcp__mcp-oracle__listar_tabelas` | `schema?: string` |
| `mcp__mcp-oracle__descrever_tabela` | `tabela: string`, `schema?: string` |
| `mcp__mcp-oracle__executar_procedure` | `nome: string`, `parametros?: dict` |
| `mcp__mcp-teams__listar_equipes` | — |
| `mcp__mcp-teams__listar_canais` | `team_id: string` |
| `mcp__mcp-teams__ler_mensagens_canal` | `team_id: string`, `channel_id: string`, `limite?: int` |
| `mcp__mcp-teams__enviar_mensagem_canal` | `team_id: string`, `channel_id: string`, `mensagem: string`, `formato?: string` |
| `mcp__mcp-teams__responder_mensagem_canal` | `team_id: string`, `channel_id: string`, `message_id: string`, `mensagem: string`, `formato?: string` |
| `mcp__mcp-teams__listar_chats` | — |
| `mcp__mcp-teams__ler_mensagens_chat` | `chat_id: string`, `limite?: int` |
| `mcp__mcp-teams__enviar_mensagem_chat` | `chat_id: string`, `mensagem: string`, `formato?: string` |

## Documentação detalhada

- [Skills e Slash Commands](docs/guia-skills.md)
- [Agents e Subagents](docs/guia-agents-subagents.md)
- [Servidor MCP](docs/guia-mcp.md)
