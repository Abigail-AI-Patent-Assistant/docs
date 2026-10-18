# Both-directory release candidate

Prepared October 17, 2026. Candidate artifacts, not submission or approval receipts.
Product parity work: https://github.com/rhahn28/abigail-v3/pull/5697 (draft).
Publication source: https://github.com/Abigail-AI-Patent-Assistant/docs/pull/3 (draft).

## Publisher and listing copy

Name: Abigail. Publisher: Salt Holdings, LLC. Support: support@abigail.app.
Short description: Review your patent docket and draft prosecution documents.
Long description and suggested prompts: `plugins/abigail/plugin.json`.
Endpoint: https://mcp.abigail.app/mcp (Streamable HTTP; per-user OAuth).
Website: https://abigail.app. Privacy: https://abigail.app/privacy.
Service terms: https://abigail.app/legal/terms-of-service.html.
Package license: `plugins/abigail/LICENSE.md` (proprietary candidate preserved from original owner).
An Abigail account and sufficient entitlement/credits are required for billed work.
No guaranteed patent outcome, autonomous filing, directory acceptance, or free export claim.

## Package preparation

`plugins/abigail` contains one shared prosecution skill, portable Agent Plugins
1.0.0 `plugin.json` / `mcp.json`, and the existing Claude-compatible manifests.
No credentials, backend, hooks, or workers are bundled. Build an allowlisted ZIP:

```sh
python publication/build_package.py --output /absolute/path/abigail-0.1.0.zip --schema-dir /absolute/path/cached-schemas
claude plugin validate --strict ./plugins/abigail
```

The schema directory must contain `plugin.schema.json` and `mcp.schema.json` fetched
from https://agent-plugins.org/schemas/1.0.0/ . Record the ZIP SHA256 and source
commit with the reviewer packet. Rebuild after any package change.

## OpenAI public directory

Current official path: https://platform.openai.com/plugins ; submit the remote
HTTPS endpoint through **With MCP**. Public plugins are shared by ChatGPT and
Codex. A local package install or workspace publication is not public listing.
Set OAuth in the portal from `openai-auth-settings.json` using discovery and DCR.
No registered app ID or client secret has been invented or embedded.

Compatibility issue to verify in portal: OpenAI's packaging guide describes
server `extensions.com.openai.auth`, but the published Agent Plugins 1.0.0 MCP
schema rejects all server `extensions` (`additionalProperties: false`). This
candidate keeps portable `mcp.json` schema-valid and records OAuth separately.
Do not treat portable-schema validation as OpenAI scanner acceptance. If portal
requires an auth extension in an uploaded package, use its validated export or
resolve the schema discrepancy before submission; never silently disable OAuth.

Pending: authenticated publisher/role; issued domain challenge and actual
verification; endpoint registration; account/credit fixture for reviewers;
scanner warnings; accurate screenshots/demo from accepted runtime; submission
ID; review decision; explicit publication; fresh-user installation proof.
Portal inspected in this audit redirects to sign-in. No submission exists from
this preparation and no verification token was fabricated.

## Anthropic directory

Current portal: https://claude.ai/admin-settings/directory/submissions/new .
Use its MCP connector flow or the repository plugin source as the actual portal
requires. Claude's plugin manifest uses HTTP type; portable manifest uses
streamable-http. Both target the same endpoint. Point reviewers to the exact
reviewed commit and `plugins/abigail`, not a moving development tree.
Pending: authenticated entitlement/publisher, connector/plugin route selection,
reviewer fixture, client authentication and tool behavior, scanner/review result,
submission ID, approval, explicit publication and fresh-user install.
Do not promise editorial promotion or assume old Team-plan-only requirements.

## Required acceptance evidence before either submission

| Gate | Required evidence | Current state |
|---|---|---|
| Frozen release | Product and docs merged SHAs, serving MCP/backend/worker/frontend revisions | Incomplete; product PR draft |
| ROA | Source-faithful case, decisions visible in browser, canonical draft save/reopen, usable latest DOCX, charge/refusal receipts | Local regression only |
| NewApp | Same-session full specification/claims/drawings, scoped persisted references/search log, conflict refusal, inspected full package | Incomplete; private-reference writes deferred on current main |
| Clients | Browser, Claude and OpenAI each read/edit/readback/reverse continuation/download on same build | Not accepted |
| Security | Private owner/other-user/cross-tenant negatives, wrong job/resource, expired/revoked auth, prompt injection | Local controls only; live matrix open |
| Tools | Registered catalog vs actual positive/negative/readback matrix, no fake queued/completed/filing receipts | Matrix open |
| Billing | Consent, credit refusal, actual ledger/provider/export/download reconciliation | Runtime reconciliation open |
| Quality | All E1-E6 assertions and 120 source/UI cases, every final artifact page inspected, Roger attorney acceptance | Open |
| Legal | Exact package clauses and marketplace distribution compatibility reviewed; public entity/terms/support consistent | Proprietary direction authorized; acceptance not established |
| Directory | Submission/reference, review approval, publication and fresh-user install on both platforms | Not submitted |

Use synthetic matters only for reviewer demonstrations. Never put client case
content, tokens, or shared credentials in public issues, packages or videos.
Run billed tests only within a specifically approved budget. Check job status and
charge references before retries. Keep filing and purchases separately authorized.

## Primary requirements checked

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/deploy/submission
- https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
- https://agent-plugins.org/schemas/1.0.0/mcp.schema.json
- https://claude.com/resources/articles/build-plugins-for-claude

A locally valid package is a review candidate. Submission, approval, publication,
and the intended fresh-user outcome each require their own retained receipt.
