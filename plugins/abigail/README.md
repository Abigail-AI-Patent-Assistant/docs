# Abigail for Claude, ChatGPT and Codex

Release candidate: 0.1.0. No marketplace acceptance or successful live connection is claimed.
Connect your Abigail account to the existing remote MCP service and use `/abigail:abigail-prosecution` for docket and case workflows.

## Local evaluation

From this repository root, run `claude plugin validate --strict ./plugins/abigail`.
After reviewing the package, launch `claude --plugin-dir ./plugins/abigail` and use `/mcp` to authenticate Abigail.
The service requires separate user OAuth authorization. Do not paste API keys or copy tokens from another client.
This package contains no backend, hooks, workers, or bundled credentials.
Claude submission must identify `plugins/abigail` and the reviewed commit; no catalog install command exists until accepted.

## OpenAI package

The root `plugin.json` and `mcp.json` use Agent Plugins 1.0.0. OpenAI presentation metadata is namespaced under `com.openai`; OAuth uses discovered endpoints and dynamic client registration. The Claude-compatible manifests remain in place.
For public OpenAI submission, use the remote HTTPS endpoint through **With MCP**; do not invent an app registration ID or copy another client's credentials. The same package supplies the prosecution skill. See [submission preparation](https://github.com/Abigail-AI-Patent-Assistant/docs/blob/codex/mcp-publication/publication/STORE-READINESS.md).

## OpenAI package

The root `plugin.json` and `mcp.json` use Agent Plugins 1.0.0. OpenAI presentation metadata is namespaced under `com.openai`; OAuth uses discovered endpoints and dynamic client registration. Claude-compatible manifests remain in place.
For public OpenAI submission, use the remote HTTPS endpoint through **With MCP**; do not invent an app registration ID or copy credentials. The same package supplies the prosecution skill. See [submission preparation](https://github.com/Abigail-AI-Patent-Assistant/docs/blob/codex/mcp-publication/publication/STORE-READINESS.md).

## Acceptance scenarios — not yet executed

Use a dedicated synthetic tenant and approved test budget; never real client matters.
Record expected fixture values before testing and retain sanitized results privately.
1. Sign in, discover the catalog, and read the fixture docket; names and IDs match expected fixtures.
2. Select a fixture case and verify returned claims and status; no guessed case identity.
3. Query a fixture deadline; compare the exact date and uncertainty to the fixture.
4. Run an authorized response wizard; report charge, status, and usable download accurately.
5. Export an already-paid synthetic application or form; open the resulting document.
6. Request another tenant's fixture; access is denied without private content.
7. Expire or revoke the session; the client requires authentication and never reports false success.
8. Request unapproved purchase or filing; no purchase, filing, or false receipt occurs.
Run the complete registered-tool matrix and refresh/replay/audience checks before public submission.

## Publisher and terms

Publisher/support: Abigail, support@abigail.app.
[Guide](https://docs.abigail.app/mcp/guide) · [Privacy](https://abigail.app/privacy) · [Service terms](https://abigail.app/legal/terms-of-service.html).
Package license: [ABIGAIL Proprietary Plugin License](LICENSE.md), copyright 2026 Salt Holdings, LLC. All rights reserved.
Install and use with your authorized Abigail account; necessary internal and backup copies are permitted. Redistribution, resale, sublicensing and distribution of modified versions require written permission, except for publisher-authorized marketplace distribution described in the license.
Service access, charges, user content and generated outputs remain governed by the linked service terms. No backend source, trademark or open-source rights are granted.
The proprietary-license decision is resolved. Authentication, reviewer testing and marketplace acceptance remain separate release gates.
