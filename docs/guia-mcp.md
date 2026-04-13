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
# Registrar o servidor de soma
claude mcp add --scope local mcp-somar python mcp/mcp-somar.py

# Remover o servidor de soma
claude mcp remove mcp-somar --scope local

# Registrar o servidor de mensagem
claude mcp add --scope local mcp-mensagem python mcp/mcp-mensagem.py

# Remover o servidor de mensagem
claude mcp remove mcp-mensagem --scope local
```

O Claude Code inicia o processo automaticamente ao abrir uma sessão no diretório do projeto.

## Servidores neste projeto

Os servidores ficam na pasta `mcp/` e usam `FastMCP` para uma API simplificada.

| Servidor | Arquivo | Ferramenta | Parâmetros |
|----------|---------|------------|------------|
| `mcp-somar` | `mcp/mcp-somar.py` | `somar` | `a: int`, `b: int` |
| `mcp-mensagem` | `mcp/mcp-mensagem.py` | `enviar_mensagem` | `mensagem: str` |

### Uso das ferramentas

```
mcp__mcp-somar__somar          → soma dois inteiros
mcp__mcp-mensagem__enviar_mensagem → envia uma mensagem de texto
```

## Instalação e execução

```bash
# Criar virtualenv e instalar dependência
python -m venv .venv
.venv/bin/pip install mcp

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
