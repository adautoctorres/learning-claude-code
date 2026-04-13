"""
Exemplo de uso da API da Anthropic com o SDK Python.
"""

import anthropic


def perguntar(pergunta: str) -> str:
    client = anthropic.Anthropic()

    mensagem = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": pergunta}
        ],
    )

    return mensagem.content[0].text


if __name__ == "__main__":
    resposta = perguntar("O que é o Model Context Protocol (MCP)?")
    print(resposta)
