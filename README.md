# learning-claude-code

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
uv venv        # cria o ambiente virtual em .venv
uv sync        # instala as dependências do pyproject.toml
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
claude mcp add --scope local mcp-oracle python mcp/mcp-oracle.py
claude mcp add --scope local mcp-teams python mcp/mcp-teams.py
```

### Remover

```bash
claude mcp remove mcp-somar --scope local
claude mcp remove mcp-mensagem --scope local
claude mcp remove mcp-oracle --scope local
claude mcp remove mcp-teams --scope local
```

### Ferramentas disponíveis

| Servidor | Ferramenta MCP | Parâmetros |
|----------|----------------|------------|
| `mcp-somar` | `mcp__mcp-somar__somar` | `a: int`, `b: int` |
| `mcp-mensagem` | `mcp__mcp-mensagem__enviar_mensagem` | `mensagem: str` |
| `mcp-oracle` | `mcp__mcp-oracle__executar_query` | `sql: str`, `parametros?: dict` |
| `mcp-oracle` | `mcp__mcp-oracle__executar_dml` | `sql: str`, `parametros?: dict` |
| `mcp-oracle` | `mcp__mcp-oracle__listar_tabelas` | `schema?: str` |
| `mcp-oracle` | `mcp__mcp-oracle__descrever_tabela` | `tabela: str`, `schema?: str` |
| `mcp-oracle` | `mcp__mcp-oracle__executar_procedure` | `nome: str`, `parametros?: dict` |
| `mcp-teams` | `mcp__mcp-teams__listar_equipes` | — |
| `mcp-teams` | `mcp__mcp-teams__listar_canais` | `team_id: str` |
| `mcp-teams` | `mcp__mcp-teams__ler_mensagens_canal` | `team_id: str`, `channel_id: str`, `limite?: int` |
| `mcp-teams` | `mcp__mcp-teams__enviar_mensagem_canal` | `team_id: str`, `channel_id: str`, `mensagem: str`, `formato?: str` |
| `mcp-teams` | `mcp__mcp-teams__responder_mensagem_canal` | `team_id: str`, `channel_id: str`, `message_id: str`, `mensagem: str` |
| `mcp-teams` | `mcp__mcp-teams__listar_chats` | — |
| `mcp-teams` | `mcp__mcp-teams__ler_mensagens_chat` | `chat_id: str`, `limite?: int` |
| `mcp-teams` | `mcp__mcp-teams__enviar_mensagem_chat` | `chat_id: str`, `mensagem: str`, `formato?: str` |

## Exemplo de uso da API Anthropic

```bash
ANTHROPIC_API_KEY=sua-chave .venv/bin/python src/exemplo_claude.py
```

## Documentação

- [Skills e Slash Commands](docs/guia-skills.md)
- [Agents e Subagents](docs/guia-agents-subagents.md)
- [Servidor MCP](docs/guia-mcp.md)
