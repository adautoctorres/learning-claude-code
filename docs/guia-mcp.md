# MCP — Model Context Protocol

MCP é o protocolo que permite ao Claude Code se conectar a servidores externos que expõem **ferramentas**, **recursos** e **prompts** adicionais. Um servidor MCP é um processo separado que se comunica com o Claude via stdio (padrão) ou HTTP/SSE.

## Como funciona

```
Claude Code  ──stdio──►  servidor MCP  ──►  suas ferramentas/dados
```

O Claude chama ferramentas MCP da mesma forma que chama ferramentas nativas (`Read`, `Bash`, etc.), mas o nome segue o padrão `mcp__<servidor>__<ferramenta>`.

**Exemplo:** ferramenta `saudacao` do servidor `exemplo` → `mcp__exemplo__saudacao`

## Registro do servidor

Edite `.claude/settings.json` (configuração local do projeto):

```json
{
  "mcpServers": {
    "nome-do-servidor": {
      "command": "python3",
      "args": ["./caminho/para/servidor.py"],
      "env": {
        "VARIAVEL": "valor"
      }
    }
  }
}
```

### Campos

| Campo | Descrição |
|-------|-----------|
| `command` | Executável (`python3`, `node`, `npx`, etc.) |
| `args` | Lista de argumentos passados ao comando |
| `env` | Variáveis de ambiente adicionais (tokens, configs) |

O Claude Code inicia o processo automaticamente ao abrir uma sessão no diretório do projeto.

## Servidor de exemplo neste projeto

**Arquivo:** `mcp-servidor/servidor.py`  
**Registro:** `.claude/settings.json` → chave `"exemplo"`

### Ferramentas expostas

| Ferramenta | Descrição | Parâmetros |
|------------|-----------|------------|
| `saudacao` | Saudação com data/hora | `nome: string` |
| `calcular` | Operações básicas (+,-,*,/) | `a: number`, `b: number`, `operacao: string` |
| `formatar_json` | Formata JSON com indentação | `entrada: string` |

## Instalação e execução

```bash
# Instalar dependência
pip install mcp

# Testar o servidor isoladamente (opcional)
python3 mcp-servidor/servidor.py
# Aguarda conexão via stdin — Ctrl+C para sair
```

Após instalar, reinicie o Claude Code para que o servidor seja registrado.

## Estrutura de um servidor MCP em Python

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
import asyncio

app = Server("nome-do-servidor")

@app.list_tools()
async def listar_ferramentas() -> list[types.Tool]:
    return [
        types.Tool(
            name="minha_ferramenta",
            description="Descrição clara do que faz.",
            inputSchema={
                "type": "object",
                "properties": {
                    "parametro": {"type": "string", "description": "..."}
                },
                "required": ["parametro"]
            }
        )
    ]

@app.call_tool()
async def executar(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "minha_ferramenta":
        return [types.TextContent(type="text", text=f"Resultado: {arguments['parametro']}")]
    raise ValueError(f"Ferramenta desconhecida: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

## Capacidades além de ferramentas

Um servidor MCP também pode expor:

- **Resources** (`@app.list_resources` / `@app.read_resource`): arquivos ou dados que o Claude pode ler como contexto
- **Prompts** (`@app.list_prompts` / `@app.get_prompt`): templates de prompt reutilizáveis

Consulte a [documentação oficial do MCP](https://modelcontextprotocol.io) para detalhes.

## Escopo: local vs global

| Local (projeto) | Global (usuário) |
|-----------------|------------------|
| `.claude/settings.json` | `~/.claude/settings.json` |
| Só carregado neste projeto | Disponível em qualquer projeto |
