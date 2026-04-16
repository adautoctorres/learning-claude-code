"""
MCP Server para integração com Microsoft Teams via Microsoft Graph API.

Dependências:
    pip install mcp msal httpx

Variáveis de ambiente necessárias:
    TEAMS_TENANT_ID     - ID do tenant Azure AD (encontrado no Entra ID)
    TEAMS_CLIENT_ID     - ID do app registrado no Azure AD
    TEAMS_CLIENT_SECRET - Secret gerado para o app no Azure AD

Permissões necessárias no Azure AD (Application permissions):
    ChannelMessage.Read.All  - ler mensagens de canais
    Chat.Read.All            - ler mensagens de chats
    Chat.ReadWrite.All       - enviar mensagens em chats
    ChannelMessage.Send      - enviar mensagens em canais (requer permissão delegada)
    Team.ReadBasic.All       - listar equipes

Registro no Claude Code:
    claude mcp add --scope local mcp-teams python mcp/mcp-teams.py
"""

import os
from pathlib import Path
from typing import Any

import httpx
import msal
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv(Path(__file__).parent.parent / ".env")

mcp = FastMCP("mcp-teams")

GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"


def _get_token() -> str:
    """Obtém token de acesso via client credentials flow (permissão de aplicativo)."""
    tenant_id = os.environ.get("TEAMS_TENANT_ID")
    client_id = os.environ.get("TEAMS_CLIENT_ID")
    client_secret = os.environ.get("TEAMS_CLIENT_SECRET")

    if not all([tenant_id, client_id, client_secret]):
        raise ValueError(
            "Variáveis de ambiente ausentes. Defina TEAMS_TENANT_ID, "
            "TEAMS_CLIENT_ID e TEAMS_CLIENT_SECRET."
        )

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority,
    )

    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )

    if "access_token" not in result:
        error = result.get("error_description", result.get("error", "Erro desconhecido"))
        raise RuntimeError(f"Falha ao obter token: {error}")

    return result["access_token"]


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_get_token()}",
        "Content-Type": "application/json",
    }


def _raise_for_status(response: httpx.Response) -> None:
    if response.is_error:
        try:
            detail = response.json().get("error", {}).get("message", response.text)
        except Exception:
            detail = response.text
        raise RuntimeError(f"Graph API erro {response.status_code}: {detail}")


@mcp.tool()
def listar_equipes() -> list[dict[str, str]]:
    """
    Lista todas as equipes (teams) disponíveis para o app.

    Returns:
        Lista de dicionários com {"id": str, "nome": str, "descricao": str}.
    """
    with httpx.Client() as client:
        response = client.get(f"{GRAPH_BASE_URL}/teams", headers=_headers())
        _raise_for_status(response)
        items = response.json().get("value", [])
        return [
            {
                "id": t["id"],
                "nome": t.get("displayName", ""),
                "descricao": t.get("description", ""),
            }
            for t in items
        ]


@mcp.tool()
def listar_canais(team_id: str) -> list[dict[str, str]]:
    """
    Lista os canais de uma equipe.

    Args:
        team_id: ID da equipe (obtido via listar_equipes).

    Returns:
        Lista de dicionários com {"id": str, "nome": str, "descricao": str}.
    """
    with httpx.Client() as client:
        response = client.get(
            f"{GRAPH_BASE_URL}/teams/{team_id}/channels",
            headers=_headers(),
        )
        _raise_for_status(response)
        items = response.json().get("value", [])
        return [
            {
                "id": c["id"],
                "nome": c.get("displayName", ""),
                "descricao": c.get("description", ""),
            }
            for c in items
        ]


@mcp.tool()
def ler_mensagens_canal(
    team_id: str,
    channel_id: str,
    limite: int = 20,
) -> list[dict[str, Any]]:
    """
    Lê as mensagens mais recentes de um canal.

    Args:
        team_id:    ID da equipe.
        channel_id: ID do canal (obtido via listar_canais).
        limite:     Número máximo de mensagens a retornar (padrão: 20, máx: 50).

    Returns:
        Lista de dicionários com {"id", "autor", "conteudo", "criado_em", "tipo"}.
    """
    limite = min(limite, 50)
    url = f"{GRAPH_BASE_URL}/teams/{team_id}/channels/{channel_id}/messages"
    params = {"$top": limite, "$orderby": "createdDateTime desc"}

    with httpx.Client() as client:
        response = client.get(url, headers=_headers(), params=params)
        _raise_for_status(response)
        items = response.json().get("value", [])
        return [
            {
                "id": m["id"],
                "autor": m.get("from", {}).get("user", {}).get("displayName", "Desconhecido"),
                "conteudo": m.get("body", {}).get("content", ""),
                "criado_em": m.get("createdDateTime", ""),
                "tipo": m.get("messageType", ""),
            }
            for m in items
        ]


@mcp.tool()
def enviar_mensagem_canal(
    team_id: str,
    channel_id: str,
    mensagem: str,
    formato: str = "text",
) -> dict[str, str]:
    """
    Envia uma mensagem em um canal de equipe.

    Args:
        team_id:    ID da equipe.
        channel_id: ID do canal.
        mensagem:   Conteúdo da mensagem.
        formato:    "text" para texto simples ou "html" para HTML (padrão: "text").

    Returns:
        Dicionário com {"id": str, "status": str, "criado_em": str}.

    Nota:
        Esta operação requer permissão delegada (usuário autenticado) em ambientes
        de produção. Em sandboxes e apps com consentimento de admin, pode funcionar
        com client credentials.
    """
    url = f"{GRAPH_BASE_URL}/teams/{team_id}/channels/{channel_id}/messages"
    payload = {"body": {"contentType": formato, "content": mensagem}}

    with httpx.Client() as client:
        response = client.post(url, headers=_headers(), json=payload)
        _raise_for_status(response)
        data = response.json()
        return {
            "id": data.get("id", ""),
            "status": "enviada",
            "criado_em": data.get("createdDateTime", ""),
        }


@mcp.tool()
def responder_mensagem_canal(
    team_id: str,
    channel_id: str,
    message_id: str,
    mensagem: str,
    formato: str = "text",
) -> dict[str, str]:
    """
    Responde a uma mensagem existente em um canal (reply em thread).

    Args:
        team_id:    ID da equipe.
        channel_id: ID do canal.
        message_id: ID da mensagem a ser respondida.
        mensagem:   Conteúdo da resposta.
        formato:    "text" ou "html" (padrão: "text").

    Returns:
        Dicionário com {"id": str, "status": str, "criado_em": str}.
    """
    url = (
        f"{GRAPH_BASE_URL}/teams/{team_id}/channels/{channel_id}"
        f"/messages/{message_id}/replies"
    )
    payload = {"body": {"contentType": formato, "content": mensagem}}

    with httpx.Client() as client:
        response = client.post(url, headers=_headers(), json=payload)
        _raise_for_status(response)
        data = response.json()
        return {
            "id": data.get("id", ""),
            "status": "enviada",
            "criado_em": data.get("createdDateTime", ""),
        }


@mcp.tool()
def listar_chats() -> list[dict[str, Any]]:
    """
    Lista os chats (diretos e em grupo) disponíveis para o app.

    Returns:
        Lista de dicionários com {"id", "tipo", "topico", "atualizado_em"}.
    """
    with httpx.Client() as client:
        response = client.get(f"{GRAPH_BASE_URL}/chats", headers=_headers())
        _raise_for_status(response)
        items = response.json().get("value", [])
        return [
            {
                "id": c["id"],
                "tipo": c.get("chatType", ""),
                "topico": c.get("topic", ""),
                "atualizado_em": c.get("lastUpdatedDateTime", ""),
            }
            for c in items
        ]


@mcp.tool()
def ler_mensagens_chat(chat_id: str, limite: int = 20) -> list[dict[str, Any]]:
    """
    Lê as mensagens mais recentes de um chat direto ou em grupo.

    Args:
        chat_id: ID do chat (obtido via listar_chats).
        limite:  Número máximo de mensagens (padrão: 20, máx: 50).

    Returns:
        Lista de dicionários com {"id", "autor", "conteudo", "criado_em"}.
    """
    limite = min(limite, 50)
    url = f"{GRAPH_BASE_URL}/chats/{chat_id}/messages"
    params = {"$top": limite, "$orderby": "createdDateTime desc"}

    with httpx.Client() as client:
        response = client.get(url, headers=_headers(), params=params)
        _raise_for_status(response)
        items = response.json().get("value", [])
        return [
            {
                "id": m["id"],
                "autor": m.get("from", {}).get("user", {}).get("displayName", "Desconhecido"),
                "conteudo": m.get("body", {}).get("content", ""),
                "criado_em": m.get("createdDateTime", ""),
            }
            for m in items
        ]


@mcp.tool()
def enviar_mensagem_chat(
    chat_id: str,
    mensagem: str,
    formato: str = "text",
) -> dict[str, str]:
    """
    Envia uma mensagem em um chat direto ou em grupo.

    Args:
        chat_id:  ID do chat.
        mensagem: Conteúdo da mensagem.
        formato:  "text" ou "html" (padrão: "text").

    Returns:
        Dicionário com {"id": str, "status": str, "criado_em": str}.
    """
    url = f"{GRAPH_BASE_URL}/chats/{chat_id}/messages"
    payload = {"body": {"contentType": formato, "content": mensagem}}

    with httpx.Client() as client:
        response = client.post(url, headers=_headers(), json=payload)
        _raise_for_status(response)
        data = response.json()
        return {
            "id": data.get("id", ""),
            "status": "enviada",
            "criado_em": data.get("createdDateTime", ""),
        }


if __name__ == "__main__":
    mcp.run()
