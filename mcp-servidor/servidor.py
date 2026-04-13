"""
Servidor MCP de exemplo — expõe três ferramentas simples via protocolo stdio.

Instalação:
    pip install mcp

Uso direto (teste manual):
    python servidor.py

Registro no Claude Code: veja .claude/settings.json
"""

import asyncio
import json
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# ── Inicialização do servidor ─────────────────────────────────────────────────

app = Server("exemplo-mcp")


# ── Definição das ferramentas disponíveis ─────────────────────────────────────

@app.list_tools()
async def listar_ferramentas() -> list[types.Tool]:
    return [
        types.Tool(
            name="saudacao",
            description="Retorna uma saudação personalizada com data e hora atual.",
            inputSchema={
                "type": "object",
                "properties": {
                    "nome": {
                        "type": "string",
                        "description": "Nome da pessoa a ser saudada."
                    }
                },
                "required": ["nome"]
            }
        ),
        types.Tool(
            name="calcular",
            description="Realiza operações matemáticas básicas (+, -, *, /).",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "Primeiro operando."},
                    "b": {"type": "number", "description": "Segundo operando."},
                    "operacao": {
                        "type": "string",
                        "enum": ["+", "-", "*", "/"],
                        "description": "Operação a realizar."
                    }
                },
                "required": ["a", "b", "operacao"]
            }
        ),
        types.Tool(
            name="formatar_json",
            description="Recebe uma string JSON e retorna formatada com indentação.",
            inputSchema={
                "type": "object",
                "properties": {
                    "entrada": {
                        "type": "string",
                        "description": "String JSON a ser formatada."
                    }
                },
                "required": ["entrada"]
            }
        )
    ]


# ── Implementação das ferramentas ─────────────────────────────────────────────

@app.call_tool()
async def executar_ferramenta(
    name: str,
    arguments: dict
) -> list[types.TextContent]:

    if name == "saudacao":
        nome = arguments["nome"]
        agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
        texto = f"Olá, {nome}! São {agora}. Bem-vindo ao servidor MCP de exemplo."
        return [types.TextContent(type="text", text=texto)]

    if name == "calcular":
        a = arguments["a"]
        b = arguments["b"]
        op = arguments["operacao"]

        if op == "+" :
            resultado = a + b
        elif op == "-":
            resultado = a - b
        elif op == "*":
            resultado = a * b
        elif op == "/":
            if b == 0:
                return [types.TextContent(type="text", text="Erro: divisão por zero.")]
            resultado = a / b
        else:
            raise ValueError(f"Operação desconhecida: {op}")

        return [types.TextContent(type="text", text=f"{a} {op} {b} = {resultado}")]

    if name == "formatar_json":
        entrada = arguments["entrada"]
        try:
            parsed = json.loads(entrada)
            formatado = json.dumps(parsed, indent=2, ensure_ascii=False)
            return [types.TextContent(type="text", text=formatado)]
        except json.JSONDecodeError as e:
            return [types.TextContent(type="text", text=f"JSON inválido: {e}")]

    raise ValueError(f"Ferramenta desconhecida: {name}")


# ── Entrypoint ────────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
