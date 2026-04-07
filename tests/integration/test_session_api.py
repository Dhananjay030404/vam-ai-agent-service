import asyncio

import httpx

from app.main import app


def request(
    method: str,
    path: str,
    headers: dict[str, str] | None = None,
    json: dict | None = None,
) -> httpx.Response:
    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            return await client.request(method, path, headers=headers, json=json)

    return asyncio.run(run())


def test_create_session_success() -> None:
    response = request(
        "POST",
        "/api/v1/session",
        headers={
            "Authorization": (
                "Bearer local:customer-123:oem-456:relation-789:service_advisor"
            )
        },
        json={},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["session"]["customer_id"] == "customer-123"
    assert body["session"]["active_oem_id"] == "oem-456"
    assert body["session"]["customer_oem_relation_id"] == "relation-789"
    assert body["session"]["role"] == "service_advisor"
    assert "orders" in body["session"]["allowed_tools"]
    assert response.headers["X-Request-ID"]


def test_create_session_requires_token() -> None:
    response = request("POST", "/api/v1/session", json={})

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing bearer token"


def test_create_session_rejects_invalid_token() -> None:
    response = request(
        "POST",
        "/api/v1/session",
        headers={"Authorization": "Bearer not-a-valid-token"},
        json={},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_create_session_requires_active_oem_context() -> None:
    response = request(
        "POST",
        "/api/v1/session",
        headers={
            "Authorization": "Bearer local:customer-123::relation-789:service_advisor"
        },
        json={},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Missing active OEM context"


def test_create_session_requires_role() -> None:
    response = request(
        "POST",
        "/api/v1/session",
        headers={"Authorization": "Bearer local:customer-123:oem-456:relation-789:"},
        json={},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Missing role"


def test_create_session_rejects_unsupported_role() -> None:
    response = request(
        "POST",
        "/api/v1/session",
        headers={"Authorization": "Bearer local:customer-123:oem-456:relation-789:bot"},
        json={},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Unsupported role: bot"
