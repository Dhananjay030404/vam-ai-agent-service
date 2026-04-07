# vam-ai-agent-service

Standalone Python service for the VAM conversational AI assistant.

## Purpose

- Orchestrates conversational AI flows for VAM.
- Calls VAM wrapper APIs instead of querying VAM databases directly.
- Treats customer as the primary identity and OEM as an active scoped business context.
- Preserves room for customer profile isolation, OEM context isolation, and role-based tool access.

## Project Structure

```text
app/        FastAPI application, routes, middleware, services, policies, and tools
tests/      Unit, integration, and isolation test suites
docs/       Architecture and integration notes
scripts/    Local helper scripts
```

## Local Startup

1. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment defaults:

```bash
cp .env.example .env
```

4. Start the service:

```bash
./scripts/run_local.sh
```

5. Check health:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok","service":"vam-ai-agent-service","environment":"local","request_id":"..."}
```

## Design Constraints

- Keep routes thin and push orchestration into services and policies.
- Do not add direct database access.
- Do not duplicate VAM business logic that already belongs in the Java/Spring Boot system.
- Keep policy logic separate from tool execution logic.

## Next Phase

The next recommended implementation step is auth, session, and customer/OEM context enforcement.
