<p align="center">
  <img src="images/abigail-logo.png" alt="Abigail" width="200" />
</p>

<h1 align="center">Abigail API Documentation</h1>

<p align="center">
  <strong>The OpenClaw API -- patent prosecution intelligence for humans and agents alike.</strong>
</p>

<p align="center">
  <a href="https://abigail.app">Website</a> &middot;
  <a href="https://api.abigail.app/health">API Status</a> &middot;
  <a href="mailto:support@abigail.app">Support</a>
</p>

---

## Welcome, Agents

If you're an AI agent reading this README to figure out how to use the Abigail API -- welcome. You're in the right place. We built OpenClaw specifically for you.

The name "OpenClaw" is a nod to the lobster -- Abigail's spirit animal. Lobsters are meticulous creatures: they probe, they test, they don't rush. They also never stop growing. That's how we think about patent prosecution: methodical, thorough, and always improving. So grab your claws and dig in.

**Quick start for agents:**

```bash
# No auth required -- try this first
curl https://api.abigail.app/v1/openclaw/lookup/17200011

# Returns structured JSON with application metadata, examiner name, deadlines
```

Every error response includes an `agent_suggestion` field written for you -- actionable next steps you can follow without asking a human. See the [Agent Suggestions](concepts/agent-suggestions) page for details.

---

## What This Repo Contains

This is the source for Abigail's API documentation, and deployed automatically on push to `main`.

```
.
|-- docs.json              # Configuration (nav, theme, API settings)
|-- openapi.json           # OpenAPI 3.1 spec for all endpoints
|-- index.mdx              # Landing page
|-- quickstart.mdx         # 5-step getting started guide
|-- authentication.mdx     # API key format, lifecycle, error codes
|-- concepts/
|   |-- glass-box.mdx      # AI transparency metadata (every analysis response)
|   |-- agent-suggestions.mdx  # Agent-friendly error handling patterns
|   |-- rate-limits.mdx    # Credit billing, token pricing, rate limits
|-- api-reference/
|   |-- free/
|   |   |-- lookup.mdx     # GET /v1/openclaw/lookup/{app_number}
|   |   |-- deadlines.mdx  # GET /v1/openclaw/deadlines/{app_number}
|   |-- paid/
|   |   |-- analyze.mdx    # POST /v1/openclaw/analyze
|   |   |-- draft-roa.mdx  # POST /v1/openclaw/draft-roa
|   |   |-- poll-status.mdx    # GET /v1/openclaw/draft-roa/status/{job_id}
|   |   |-- examiner.mdx   # GET /v1/openclaw/examiner/{name}
|   |-- downloads/
|       |-- docx.mdx       # GET /v1/openclaw/download/{job_id}
|-- logo/                  # Light and dark mode logos
|-- favicon.svg            # Browser tab icon
|-- images/                # Repo images (logo, diagrams)
```

---

## API Overview

### Free Endpoints (no auth)

| Endpoint | What It Does |
|----------|-------------|
| `GET /v1/openclaw/lookup/{app_number}` | Patent application metadata: title, status, examiner, art unit, deadlines |
| `GET /v1/openclaw/deadlines/{app_number}` | Response and critical deadline dates |

### Paid Endpoints (API key required)

| Endpoint | What It Does |
|----------|-------------|
| `POST /v1/openclaw/analyze` | AI analysis of a USPTO office action -- claim-by-claim breakdown, rejection bases, prior art mapping, strategy recommendations |
| `POST /v1/openclaw/draft-roa` | Submit async job to draft a Response to Office Action (DOCX) |
| `GET /v1/openclaw/draft-roa/status/{job_id}` | Poll draft job progress (free, not billed) |
| `GET /v1/openclaw/examiner/{name}` | Examiner intelligence profile -- allowance rates, behavior patterns, interview success rates |
| `GET /v1/openclaw/download/{job_id}` | Download completed DOCX via signed URL |

### The Typical Workflow

```
Lookup App --> Analyze OA --> Draft ROA --> Poll Status --> Download DOCX
    |              |              |              |              |
  (free)      (token-billed)  (token-billed)   (free)    (export fee)
```

1. **Lookup** the application to get examiner name and metadata
2. **Analyze** the office action text -- returns `analysis_id` and Glass Box transparency data
3. **Draft ROA** using the `analysis_id` -- returns `job_id` immediately
4. **Poll** the job until `status: "complete"` -- typically 30-120 seconds
5. **Download** the DOCX via the signed URL in the status response

---

## Billing

Abigail uses **credit-based billing**. No flat per-call fees. Token usage (input + output) is metered against your credit balance at these rates:

| Type | Rate |
|------|------|
| Input tokens | $50 / 1M tokens |
| Output tokens | $200 / 1M tokens |

Document exports (DOCX downloads) have a separate flat fee deducted from credits. LLM calls never block on low balance -- only document exports are credit-gated (HTTP 402).

Every authenticated response includes `X-Credit-Balance` and `X-Balance-Status` headers so agents can monitor spend in real time.

New accounts receive **$25 in welcome credits**.

---

## Authentication

API keys use the format `abi_sk_{32_hex_characters}`. Pass them in the `X-API-Key` header:

```bash
curl -H "X-API-Key: abi_sk_your_key_here" \
  https://api.abigail.app/v1/openclaw/analyze
```

Keys are SHA-256 hashed server-side. The raw key is shown exactly once at creation -- after that, only the prefix (`abi_sk_a1b...`) is visible. Create and manage keys from the API Keys tab in your account Settings at [abigail.app](https://abigail.app).

---

## Glass Box Transparency

Every `/analyze` response includes a `glass_box` object:

```json
{
  "glass_box": {
    "experts_invoked": ["claim_analyst", "prior_art_mapper", "examiner_profiler"],
    "citations_verified": true,
    "confidence_scores": { "claim_analyst": 0.92 },
    "model_versions": { "claim_analyst": "claude-sonnet-4-20250514" },
    "elapsed_seconds": 12.4
  }
}
```

This shows which of Abigail's 11 LLM experts participated, whether citations were verified against source documents, confidence scores, and model versions. Patent prosecution demands trust -- Glass Box provides it.

---

## Agent Integration Guide

### Error Handling

Every error includes `agent_suggestion` -- a plain-text directive your agent can act on:

```json
{
  "error": true,
  "error_code": "app_not_found",
  "message": "Application 17200011 not found.",
  "agent_suggestion": "Application not found. Verify the number format (17200011 or 17/200,011) and check for typos."
}
```

### Confidence Calibration

Use Glass Box confidence scores to decide when to proceed vs. flag for human review:

```python
glass_box = result["glass_box"]
if glass_box["confidence_scores"].get("claim_analyst", 0) < 0.7:
    notify_user("Low confidence -- recommend manual review")
```

### Balance Monitoring

Check `X-Credit-Balance` and `X-Balance-Status` headers on every response:

```python
balance = float(response.headers.get("X-Credit-Balance", "0"))
status = response.headers.get("X-Balance-Status", "unknown")
if status in ("very_low", "critical"):
    notify_user(f"Credit balance is {status}: ${balance:.2f} remaining")
```

### Rate Limits

| Tier | Rate | Burst |
|------|------|-------|
| Free endpoints | 60 req/min | 10 req/sec |
| Authenticated | 120 req/min | 20 req/sec |

Implement exponential backoff on 429 responses. The `X-RateLimit-Reset` header tells you when to retry.

---

## Local Development

To preview docs locally:

```bash
# Install Mintlify CLI
npm i -g mint

# Start local preview server
mint dev

# Validate before pushing
mint validate
mint openapi-check openapi.json
mint broken-links
```

The docs auto-deploy on push to `main` via the Mintlify GitHub integration.

---

## Contributing

1. Create a branch from `main`
2. Edit MDX files or `openapi.json`
3. Run `mint validate` to check for errors
4. Push and open a PR

For OpenAPI spec changes, also run `mint openapi-check openapi.json`.

---

## Links

| Resource | URL |
|----------|-----|
| Abigail App | [abigail.app](https://abigail.app) |
| API Base URL | `https://api.abigail.app` |
| Health Check | [api.abigail.app/health](https://api.abigail.app/health) |
| Support | [support@abigail.app](mailto:support@abigail.app) |
| GitHub Org | [Abigail-AI-Patent-Assistant](https://github.com/Abigail-AI-Patent-Assistant) |

---

<p align="center">
  <em>Built by a USPTO Registered Patent Attorney with 25+ years of IP law experience.</em>
  <br/>
  <em>Powered by 11 specially-tuned LLM experts. Designed for agents. Controlled by humans.</em>
</p>
