# Both-directory release candidate

Updated October 19, 2026. Candidate artifacts, not submission or approval receipts.
Product parity work: https://github.com/rhahn28/abigail-v3/pull/5697 (OPEN, protected from merge; head 552b05546334264874b0e040489401a3eb4dca9a).
Publication source: https://github.com/Abigail-AI-Patent-Assistant/docs/pull/3 (draft).

## Publisher and listing copy

Name: Abigail. Publisher: Salt Holdings, LLC. Support: support@abigail.app.
Short description: Review your patent docket and draft applications or responses.
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
Build **two distinct artifacts** from the canonical package source:

```sh
python publication/build_package.py --target portable --output /absolute/path/abigail-portable.zip --schema-dir /absolute/path/cached-schemas
python publication/build_package.py --target openai --output /absolute/path/abigail-openai.zip --schema-dir /absolute/path/cached-schemas
PLUGIN_SCHEMA_DIR=/absolute/path/cached-schemas python -m unittest discover -s publication -p test_build_package.py
```

Use the OpenAI artifact for OpenAI preparation. The builder embeds DCR/OAuth
under `mcpServers.abigail.extensions.com.openai.auth` in the actual ZIP's
`mcp.json`. The sidecar JSON is build input, never a substitute for uploaded auth
metadata. The portal reads package settings; it has no advanced OAuth editor.
No client ID, client secret or token is embedded or invented. Discovery supplies
endpoints and DCR registration; the private reviewer account remains separate.

The portable/Claude artifact continues to pass the unchanged published portable
schema. That schema rejects vendor MCP extensions; the OpenAI artifact instead
passes a separate strict local contract derived from the official OpenAI DCR
example. This is **not** an official OpenAI validator or host acceptance. Do not
claim the emitted OpenAI MCP file passes the portable schema. Authenticate the
portal, verify imported settings, and retain actual host scan/OAuth receipts.

October19 repair hypothesis: conflating both host contracts caused auth to be
omitted from the upload. Two reproducible targets preserve the strict portable
contract and carry documented auth in the OpenAI artifact. RED: new package
tests failed because --target and the auth contract were absent. Acceptance:
inspect both actual ZIPs, require embedded DCR in OpenAI, reject missing auth,
credentials and unknown fields, preserve identical proprietary license bytes.

The seven allowlisted files are UTF-8 text. ZIP output normalizes checkout CRLF
to LF so a Windows checkout and committed source produce identical public bytes.
The proprietary license already has the canonical bytes and retains its original
SHA256. RED: the new cross-platform newline test failed before the helper existed;
GREEN requires both equivalent line-ending inputs and actual commit/blob matching.
Earlier Review5 artifacts are retained as superseded checkout-dependent builds.

Public discovery rechecked October19 advertises OAuth resource
`https://mcp.abigail.app` and issuer `https://api.abigail.app/oauth`, with DCR,
S256 PKCE and public-client token authentication. The MCP endpoint remains
`https://mcp.abigail.app/mcp`. Bind `auth.resource` explicitly to the advertised
origin; an endpoint path is not assumed to be the resource identifier. RED:
actual ZIP omitted this binding; GREEN requires its presence and wrong-resource
rejection. No client registration, authorization, token exchange or production
change is performed by this read-only metadata check.

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
| Frozen release | Product and docs merged SHAs, serving MCP/backend/worker/frontend revisions | Incomplete; product PR open, exact-head required CI passed; independent final plan/code review open |
| ROA | Source-faithful case, decisions visible in browser, canonical draft save/reopen, usable latest DOCX, charge/refusal receipts | Local regression only |
| NewApp | Same-session full specification/claims/drawings, scoped persisted references/search log, conflict refusal, inspected full package | Private writes implemented in product PR; real local Storage/SQL/queue/vector/browser readback and exact source download pass. Full generated package/provider acceptance remains open |
| Clients | Browser, Claude and OpenAI each read/edit/readback/reverse continuation/download on same build | Partial local browser readback/download only; native Claude/Codex final-build roundtrips blocked until approved runtime access |
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

## October 18 integrated engineering receipts

Product PR5697 head 552b05546334264874b0e040489401a3eb4dca9a passed all
8 required Agent Gate jobs including Summary in run39166430265:
https://github.com/rhahn28/abigail-v3/actions/runs/39166430265
Full backend CI:33570passed/265skipped. Required frontend typecheck/lint/Jest/build,
Python guards, diff guards and actual PostgreSQL RPC schema smoke all passed.
Skipped optional duplicate CI jobs are not counted as passes.

Exact-head local24module regression714PASS/0skip/0baseline includes the expanded
189case checklist module with valid owned, orphan and foreign-draft links.
Prior d9 CI failure8/33462PASS/265SKIP is retained in the audit; its test fake
rejected strict queries and omitted genuine claim bindings. The repair changes
only test+plan files, leaving runtime byte-identical to real local proofs.
Frontend reference/download suite29PASS; isolated PostgreSQL migration/RLS/RPC1PASS.
Actual local registered save/private Storage/SQL/offline Qdrant and consumer
proof, separate actual Redis/Celery Library delivery, reviewed attribution
manifest and authenticated two-session browser/exact source.txt download passed.
These are not full generated-wizard, hosted native-client or production outcomes.

Production migration dependency hashes and review-only execution sequence are in
the audit's production-release-plan.md and production-migration-file-hashes.json,
and summarized in product PR5697. Historical session ownership is only a candidate
until corroborated or explicitly attributed. Unresolved/conflicting records and
missing original bytes remain explicit; no production attribution was executed.
Independent final plan/code review is UNVERIFIED under no-fan-out.

Current review4 ZIP (seven allowlisted files) SHA256:
`9e01eac0b362e078ea047d8cc22b8ff49cc3b77d7559652a620e1c6ad22b038a`.
Both portable schemas, Claude strict validator, exact-source/integrity/secret
checks and fresh Mintlify build/link checks passed at package source072c4f5.
Proprietary LICENSE SHA256 unchanged:
`761bcbdbcd3f3b09b9736041c9a1bc887c1a6b40e871a98ae0683bb7d9a327f6`.
NewApp is explicit in discovery metadata and acceptance scenarios. Review3 is
historical and retained. This readiness-only update is outside the ZIP.

Fresh public health, protected-resource and authorization-server metadata all
returned HTTPS200 with expected resource/issuer origins. Serving revision and
real user OAuth/client roundtrips were not attested by these reads.

Fresh GitHub inventory also retains27 open dependency alerts:23frontend,
2USPTOFiler,2investor-deck (19high/6medium/2low). All match vulnerable candidate
lock entries; production runtime/build reachability and remediation disposition
remain unverified. Full per-alert table is dependency-alert-triage.md in the
private audit packet. No dependency changed or alert dismissed. Green CI is not
an actual host-scanner or dependency-exposure disposition.

OpenAI's current public-submission guidance requires a stable publicly reachable
HTTPS MCP endpoint; Secure MCP Tunnel alone does not satisfy submission. Verify
production OAuth/domain/auth and actual review-client access on the released
revision. Its public-proxy/private-server guidance describes mTLS; applicability
must be verified for the deployment rather than assumed universally.
https://developers.openai.com/plugins/build/mcp-server

Anthropic's current portal accepts a single remote MCP connector or a GitHub
plugin bundle for developers on paid plans. Validation, review and explicit
publication remain separate receipts. Both portal sessions in this audit are
sign-in gated; no scan, submission or approval is claimed.
https://claude.com/resources/articles/build-plugins-for-claude
