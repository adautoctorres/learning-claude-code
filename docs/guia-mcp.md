# MCP — Model Context Protocol

MCP é o protocolo que permite ao Claude Code se conectar a servidores externos que expõem **ferramentas**, **recursos** e **prompts** adicionais. Um servidor MCP é um processo separado que se comunica com o Claude via stdio (padrão) ou HTTP/SSE.

## Como funciona

```
Claude Code  ──stdio──►  servidor MCP  ──►  suas ferramentas/dados
```

O Claude chama ferramentas MCP da mesma forma que chama ferramentas nativas (`Read`, `Bash`, etc.), mas o nome segue o padrão `mcp__<servidor>__<ferramenta>`.

**Exemplo:** ferramenta `somar` do servidor `mcp-somar` → `mcp__mcp-somar__somar`

## Registro do servidor

Use o CLI do Claude Code para registrar servidores MCP:

```bash
# Registrar um servidor (escopo local ao projeto)
claude mcp add --scope local <nome> <comando> <arquivo>

# Remover um servidor
claude mcp remove <nome> --scope local
```

### Servidores deste projeto

```bash
# Registrar os servidores
claude mcp add --scope local mcp-somar python mcp/mcp-somar.py
claude mcp add --scope local mcp-mensagem python mcp/mcp-mensagem.py
claude mcp add --scope local mcp-oracle python mcp/mcp-oracle.py
claude mcp add --scope local mcp-teams python mcp/mcp-teams.py

# Remover os servidores
claude mcp remove mcp-somar --scope local
claude mcp remove mcp-mensagem --scope local
claude mcp remove mcp-oracle --scope local
claude mcp remove mcp-teams --scope local
```

O Claude Code inicia o processo automaticamente ao abrir uma sessão no diretório do projeto.

## Servidores neste projeto

Os servidores ficam na pasta `mcp/` e usam `FastMCP` para uma API simplificada.

### mcp-somar

Servidor de exemplo. Expõe uma ferramenta de soma.

| Ferramenta | Parâmetros | Retorno |
|------------|------------|---------|
| `somar` | `a: int`, `b: int` | `int` |

### mcp-mensagem

Servidor de exemplo. Simula envio de mensagem.

| Ferramenta | Parâmetros | Retorno |
|------------|------------|---------|
| `enviar_mensagem` | `mensagem: str` | `str` |

### mcp-oracle

Integração com banco de dados Oracle via `oracledb`.

**Variáveis de ambiente:**
```bash
ORACLE_USER=usuario
ORACLE_PASSWORD=senha
ORACLE_DSN=host:1521/service_name
```

| Ferramenta | Parâmetros | Retorno |
|------------|------------|---------|
| `executar_query` | `sql: str`, `parametros?: dict` | `list[dict]` |
| `executar_dml` | `sql: str`, `parametros?: dict` | `dict` |
| `listar_tabelas` | `schema?: str` | `list[dict]` |
| `descrever_tabela` | `tabela: str`, `schema?: str` | `list[dict]` |
| `executar_procedure` | `nome: str`, `parametros?: dict` | `dict` |

### mcp-teams

Integração com Microsoft Teams via Microsoft Graph API.

**Dependências extras:**
```bash
.venv/bin/pip install msal httpx
```

**Variáveis de ambiente:**
```bash
TEAMS_TENANT_ID=seu-tenant-id
TEAMS_CLIENT_ID=seu-client-id
TEAMS_CLIENT_SECRET=seu-client-secret
```

**Permissões necessárias no Azure AD (Application permissions):**
- `ChannelMessage.Read.All`
- `ChannelMessage.Send`
- `Chat.Read.All`
- `Chat.ReadWrite.All`
- `Team.ReadBasic.All`

| Ferramenta | Parâmetros | Retorno |
|------------|------------|---------|
| `listar_equipes` | — | `list[dict]` |
| `listar_canais` | `team_id: str` | `list[dict]` |
| `ler_mensagens_canal` | `team_id: str`, `channel_id: str`, `limite?: int` | `list[dict]` |
| `enviar_mensagem_canal` | `team_id: str`, `channel_id: str`, `mensagem: str`, `formato?: str` | `dict` |
| `responder_mensagem_canal` | `team_id: str`, `channel_id: str`, `message_id: str`, `mensagem: str`, `formato?: str` | `dict` |
| `listar_chats` | — | `list[dict]` |
| `ler_mensagens_chat` | `chat_id: str`, `limite?: int` | `list[dict]` |
| `enviar_mensagem_chat` | `chat_id: str`, `mensagem: str`, `formato?: str` | `dict` |

## Instalação e execução

```bash
# Criar virtualenv e instalar dependências base
python -m venv .venv
.venv/bin/pip install mcp

# Dependências extras por servidor
.venv/bin/pip install oracledb          # mcp-oracle
.venv/bin/pip install msal httpx        # mcp-teams

# Testar um servidor isoladamente (opcional)
.venv/bin/python mcp/mcp-somar.py
# Aguarda conexão via stdin — Ctrl+C para sair
```

Após instalar, reinicie o Claude Code para que os servidores sejam registrados.

## Estrutura de um servidor MCP com FastMCP

FastMCP é a forma mais simples de criar servidores MCP em Python:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("nome-do-servidor")

@mcp.tool()
def minha_ferramenta(parametro: str) -> str:
    """Descrição da ferramenta."""
    return f"Resultado: {parametro}"

if __name__ == "__main__":
    mcp.run()
```

O `FastMCP` infere automaticamente o schema da ferramenta a partir das anotações de tipo Python.

### Exemplo completo: mcp-somar.py

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-somar")

@mcp.tool()
def somar(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    mcp.run()
```

### Exemplo completo: mcp-mensagem.py

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-mensagem")

@mcp.tool()
def enviar_mensagem(mensagem: str) -> str:
    return f"Mensagem enviada: {mensagem}"

if __name__ == "__main__":
    mcp.run()
```

## Capacidades além de ferramentas

Um servidor MCP também pode expor:

- **Resources** (`@mcp.resource`): arquivos ou dados que o Claude pode ler como contexto
- **Prompts** (`@mcp.prompt`): templates de prompt reutilizáveis

Consulte a [documentação oficial do MCP](https://modelcontextprotocol.io) para detalhes.

## Escopo: local vs global

| Local (projeto) | Global (usuário) |
|-----------------|------------------|
| `.claude/settings.json` | `~/.claude/settings.json` |
| Só carregado neste projeto | Disponível em qualquer projeto |
