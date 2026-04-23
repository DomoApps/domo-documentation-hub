# Code Engine Documentation Rework — Design

**Date:** 2026-04-23
**Branch:** `genesis/imp/code-engine-update`
**Author:** Jason Hansen
**Status:** Draft — ready for implementation planning

## Goal

Rework Domo's public Code Engine documentation to reflect the current state of the product and sibling code, with enterprise-grade depth: accurate endpoint coverage, complete calling guides for every supported integration mode, and authoritative conceptual content.

## Success criteria

- A first-time reader can land anywhere in the section and get working (Custom App dev, Workflow builder, external integrator).
- Every technical claim about endpoints, SDK methods, or runtime libraries is traceable to a file in a sibling repo, or flagged as unverified.
- The permalink collision between `Product-APIs/Code-Engine.mdx` and `app-framework-apis/Code-Engine-API.mdx` is resolved.
- The two legacy App-Framework and API-reference calling guides are consolidated into the new `calling/*` hub with redirects from the old paths.

## Reference material

- **Existing docs** — `portal/API-Reference/Product-APIs/Code-Engine.mdx`, `portal/API-Reference/app-framework-apis/Code-Engine-API.mdx`, `portal/Automate-Actions/Code-Engine/*`, `portal/Apps/App-Framework/Guides/hitting-code-engine-from-an-app.mdx`.
- **DomoWeb Code Engine UI** — `DomoWeb/DomoWeb/public/javascripts/codeEngine/` (sibling repo). Source of truth for endpoints, request/response shapes, enums.
  - `api/function.api.ts` — every v2 endpoint the UI calls.
  - `api/permissions.ts` — permissions read/write.
  - `api/accounts.api.ts` — account picker endpoints.
  - `models/interfaces.ts`, `models/enums.ts`, `models/constants.ts` — canonical types.
- **domo.js SDK (ryuu.js)** — `domo.js/src/models/services/codeengine.ts`. Source of truth for `domo.codeEngine(alias, input)`.
- **domoapps / Odyssey** — `domoapps/odyssey-server/.../CodeEngineJobHandler.kt`. Source of truth for the Workflow integration path.

## Decisions (from brainstorm)

- **Scope:** full Code Engine section rework + API references (not just the short Product-APIs page).
- **Endpoint exposure:** execution surface + read-only package introspection. Package authoring endpoints (create / update / delete / save-working-version) remain undocumented as public contract — UI-owned.
- **Structure:** `Automate-Actions/Code-Engine/` is the hub for concepts, UI tasks, and calling guides. `API-Reference/Product-APIs/Code-Engine.mdx` is a pure endpoint reference. The `app-framework-apis/Code-Engine-API.mdx` page is retired; its content is redistributed.

## Page inventory

### Automate-Actions/Code-Engine/ (hub)

**Existing — refresh:**
- `overview.mdx` — rewrite around full mental model (what Code Engine is, packages vs. versions vs. functions, runtimes, how it fits with Workflows/Apps/Bricks). Keep Required Grants.
- `creating-packages.mdx` — split: UI task content stays here; `codeengine` library content moves to `concepts/the-codeengine-library.mdx`.
- `global-vs-custom-packages.mdx` — light refresh, new cross-links.
- `common-use-cases.mdx` — refresh, point at new calling guides.
- `javascript-libraries.mdx` — rewrite against actual runtime allowlist; becomes a two-section page (codeengine module summary + third-party allowlist).
- `python-packages.mdx` — verify package list against actual Python runtime; restructure into stdlib + third-party tables.
- `Packages/Instance-Management.mdx`, `Packages/Cards-to-PDF.mdx` — leave mostly alone; refresh cross-links.

**New — Concepts (`concepts/`):**
- `packages-and-versions.mdx` — object model, working vs. released, semver, availability (GLOBAL/PRIVATE), runtime environments (LAMBDA user-visible; ARRAKIS/DOMOACTION/MODELENDPOINT/PYTILE noted as internal).
- `functions-and-types.mdx` — input/output type system (WorkflowDataType enum), `Variable` shape, account aliasing, type-failure debugging (`RESULT_TYPE_FAILURE`, expected vs. actual).
- `permissions-and-sharing.mdx` — two-layer model (instance grants + package ACLs), permission values (OWNER/EDIT/VIEW/EXECUTE/NONE), UI-to-API mapping, user vs. group sharing, virtual-user model.
- `the-codeengine-library.mdx` — consolidated reference for the `codeengine` runtime module: `sendRequest`, `getAccount`, `axios`, `getPersonDetails`, `getExecutionDetails`. Python equivalents noted if present.

**New — Calling Code Engine (`calling/`):**
- `from-a-custom-app.mdx` — ryuu.js `domo.codeEngine(alias, input)`, manifest `packageMapping`, wiring screen. Replaces `Apps/App-Framework/Guides/hitting-code-engine-from-an-app.mdx`; old page becomes redirect.
- `from-a-workflow.mdx` — Workflow Code Engine action step, virtual-user model, version pinning.
- `from-a-brick.mdx` — short page, cross-links to Workflow or Custom App paths.
- `from-outside-domo.mdx` — external REST path with developer token; curl/Node/Python snippets; links forward to API reference.

### API-Reference/Product-APIs/Code-Engine.mdx

Rewrite as pure endpoint reference. Sections: Authentication, Base URL, Endpoints (grouped: Execute / Introspect / Lifecycle / Permissions), Schemas, Troubleshooting, Operations-not-in-this-reference callout.

### Retired

- `API-Reference/app-framework-apis/Code-Engine-API.mdx` — delete. Content redistributed:
  - Calling-guide sections → `calling/from-a-custom-app.mdx`, `calling/from-a-workflow.mdx`, `calling/from-outside-domo.mdx`.
  - Endpoint-reference sections → consolidated Product-APIs reference.
  - Resolves the permalink collision.

## Information architecture

### Reader paths

- **Admin/developer first-time:** `overview` → `concepts/packages-and-versions` → `creating-packages` → relevant `calling/*`.
- **Custom App developer:** lands on `calling/from-a-custom-app` (self-contained). Deep-link to `concepts/functions-and-types` for type questions. API reference is appendix only.
- **External integrator:** `calling/from-outside-domo` (onboarding) → `API-Reference/Product-APIs/Code-Engine` (contract).

### Cross-linking rules

- Every calling guide ends with Troubleshooting, linked to `concepts/functions-and-types`.
- Every concept page links forward to the relevant calling guide.
- The API reference links back to the recommended calling guide for each endpoint ("Most app developers should use `domo.codeEngine(alias, input)` instead...").

### Nav changes (docs.json)

Under Automate Actions → Code Engine, add two new groups:
- **Concepts** (4 pages)
- **Calling Code Engine** (4 pages)

Keep existing pages where they are; reorder and group. Packages sub-group stays intact.

## External API reference scope

Per-endpoint template: **Method · Path · Auth · Path params · Query params · Request body · Request example · Response example · Response fields · Status values · Errors · Notes**.

### Endpoints

**Execute**

| # | Endpoint |
|---|----------|
| 1 | `POST /api/codeengine/v2/packages/{packageId}/versions/{version}/functions/{functionName}` — Run Function |
| 2 | `GET /api/codeengine/v2/packages/{packageId}/executions/{executionId}` — Get Execution by ID |

**Introspect (read-only)**

| # | Endpoint |
|---|----------|
| 3 | `GET /api/codeengine/v2/packages/{packageId}?parts=versions` — Get Package |
| 4 | `GET /api/codeengine/v2/packages/{packageId}/versions/{version}?parts=functions,code,privateFunctions` — Get Version |

**Lifecycle**

| # | Endpoint |
|---|----------|
| 5 | `POST /api/codeengine/v2/packages/{packageId}/versions/{version}/release` — Release a Version |

**Permissions / sharing**

| # | Endpoint |
|---|----------|
| 6 | `GET /api/codeengine/v2/packages/{packageId}/permissions` — Get Permissions |
| 7 | `POST /api/codeengine/v2/packages/{packageId}/permissions` — Set Permissions |
| 8 | `POST /api/codeengine/v2/packages/{packageId}/share` — Share (incremental) |

### Schemas (documented as tables, not JSON dumps)

`FunctionPackage`, `Version`, `Function`, `Variable` (with full type enum), `FunctionExecution`, `ExecutionStatus` (SUCCESS / FAILED / RESULT_TYPE_FAILURE / RUNNING / OUTPUT_UNDEFINED), `FunctionPackageShareRequest`.

### Excluded (UI-owned)

Package create (`POST /packages`), package update (`PUT /packages/{id}`), package delete, version delete, save-working-version code, run-preview-with-params. Page includes a callout explaining what's intentionally out of scope.

### Troubleshooting section

- 404 on Run Function → version not released, or wrong functionName.
- 200 OK + `status: FAILED` → function-level failure; check `errorInformation.errorMessages` and `stderr.log`.
- 200 OK + `status: RESULT_TYPE_FAILURE` → wrong return type; check `errorInformation.expectedType` vs. `actualType`.
- 403 → token lacks Code Engine execute permission, or package ACL doesn't include the token's owner.

## Concept pages — content outlines

### packages-and-versions.mdx

- Object model: package → versions → functions.
- Working version vs. released version. Only released versions are callable externally.
- Preview runs against working version (UI only).
- Semantic versioning rules (`validRefNameRegex` = `[a-zA-Z0-9\-]+`).
- Copy-from-prior-version workflow.
- Availability: GLOBAL vs. PRIVATE.
- Runtime environments: LAMBDA is user-visible; ARRAKIS/DOMOACTION/MODELENDPOINT/PYTILE noted as internal specializations, not user-selectable.
- Lifecycle diagram: Draft → Working (0.0.0-dev) → Released (1.0.0, 1.0.1…) → Shared.

### functions-and-types.mdx

- Type system from `TypeEnumV2` / `WorkflowDataType`: text, number, decimal, boolean, date, dateTime, time, duration, object, person, dataset, group (+ file / directory when FileSet enabled).
- `Variable` shape: name, displayName, type, isList, nullable, children, defaultValues.
- Account aliasing: how `accountAliasConfiguration` maps account ID → alias for `codeengine.getAccount(alias)`.
- Type/shape failures: `RESULT_TYPE_FAILURE`, `errorInformation.expectedType` vs. `actualType`.
- Side-by-side JS + Python code samples: person input, list-of-number input, object output.

### permissions-and-sharing.mdx

- Layer 1: instance grants (Manage Code Engine Packages, Create Code Engine Packages).
- Layer 2: package ACLs.
- Permission values: `OWNER`, `EDIT` (WRITE), `VIEW` (READ), `EXECUTE`, `NONE`.
- UI → API mapping from `accessLevelToPermissionsMap`: CAN_EDIT → WRITE, CAN_SHARE → READ, CAN_EXECUTE → EXECUTE.
- User vs. group sharing.
- Virtual-user / service-account pattern (Workflows, Bricks).

### the-codeengine-library.mdx

Replaces content scattered across `creating-packages.mdx` and `javascript-libraries.mdx`.

- `codeengine.sendRequest(method, url, body?, headers?, contentType?)` — authenticated internal API calls.
- `codeengine.getAccount(aliasOrId)` — decrypts and returns account properties.
- `codeengine.axios(url, options)` — Axios-backed external HTTP.
- `codeengine.getPersonDetails(personId)` — resolve a `person`-typed input.
- `codeengine.getExecutionDetails(executionId)` — introspect a prior execution.
- Each: signature, params table, example, common errors.
- "Picking the right method" table: internal Domo API → `sendRequest`. External API with stored Domo Account → `getAccount` + `axios`. External API no account → `axios` directly.
- Python equivalents: documented side-by-side if a Python `codeengine` module exists; otherwise explicitly noted as JS-only.

## Calling guide template

Every `calling/*` page uses this section template:

**When to use · Prerequisites · Step-by-step · Full example · Input/output shape · What the server does · Troubleshooting · Related**

### from-a-custom-app.mdx

- When: iframe apps (App Studio, dashboard tile, Pro-code app).
- Prereqs: `proxyId`, ryuu.js.
- Steps: (1) manifest `packageMapping`, (2) wiring screen, (3) `await domo.codeEngine(alias, input)`.
- Full example: React-style component summing two numbers; shows manifest + call site.
- Shape: input keys = alias strings; output wrapped as `{ aliasName: value }`.
- Server: `POST /domo/codeengine/v2/packages/{alias}` → ryuu-server `NebulaResource` → alias resolution → Code Engine execution as virtual user → output re-aliasing. `/complex` variant is deprecated (2023-06-27) and not on the SDK.
- Troubleshooting: alias mismatch, missing wiring, iframe-only, no tokens in iframe.

### from-a-workflow.mdx

- When: Workflow orchestration with server-side code.
- Prereqs: Workflow with Code Engine step, package released, caller has EXECUTE.
- Steps: add action, pick package + version + function, map inputs/outputs.
- Virtual-user model; version pinning (new release does NOT auto-upgrade step).
- Common triggers: App Studio button, schedule, Brick, webhook.
- Troubleshooting: permission failures, SUCCESS at Code Engine but failure at Workflow layer.

### from-a-brick.mdx

Short. Two paths: (a) Brick → Workflow → Code Engine (preferred), (b) Brick as Custom App → ryuu.js. Cross-links rather than duplicates.

### from-outside-domo.mdx

- When: server-to-server, CI, external automation.
- Prereqs: developer token with Code Engine execute scope, released version, token owner has EXECUTE.
- Quickstart: curl + Node + Python snippets for Run Function.
- `getLogs: true` note.
- Re-fetch pattern via Get Execution.
- Security: no tokens in client code; server proxies; rotation.
- "Next: full endpoint reference" link.

## Runtime-reference refresh

### javascript-libraries.mdx

Current page: 3 top-level libraries, 4 `codeengine` methods. Real allowlist is likely larger.

- Verification step in implementation plan: locate the runtime's `require()` allowlist / sandbox manifest. If not available in accessible repos, flag and ship an explicit "as of…" note rather than guessing.
- Rewrite into two sections:
  1. `codeengine` module — brief summary, link to `concepts/the-codeengine-library.mdx`.
  2. Third-party libraries via `require()` — table (name, one-line description, upstream-docs link).
- Remove `sendRequest` documentation from this page (canonical home is `concepts/the-codeengine-library.mdx`).

### python-packages.mdx

- Verify current package list against actual Python runtime allowlist.
- Restructure:
  1. Python standard library — note full stdlib is available (or call out exclusions); link out to Python docs.
  2. Third-party packages — table with name, pinned version if available, upstream-docs link.
- If a Python-side `codeengine` equivalent module exists, document alongside JS in `concepts/the-codeengine-library.mdx`.

### Verification rule for the implementation plan

For each technical claim about the runtime (method signatures, allowed libraries, type system):

- **Either:** cite a file path + line in a sibling repo.
- **Or:** mark the claim `UNVERIFIED — source needed`.

At implementation completion, any remaining `UNVERIFIED` items become a followup list the user can triage.

## Out of scope (for this project)

- Tutorials beyond the existing `Packages/Instance-Management` and `Packages/Cards-to-PDF`. New tutorials can be added in follow-up work.
- OpenAPI spec generation for the Code Engine endpoints (potential future initiative).
- Localization (`de/`, `es/`, `fr/`, `ja/`) updates — the English source is the target; localization will follow its existing process.
- Refactoring `docs.json` beyond the two new groups under Automate Actions → Code Engine.

## Followups (to surface at end of implementation)

- Any `UNVERIFIED` claims from the runtime-reference verification.
- Whether the retired `app-framework-apis/Code-Engine-API.mdx` should hard-redirect (via Mintlify redirect config) or be removed outright.
- Whether existing tutorial pages (`Packages/*`) warrant their own refresh pass after the concept pages land.
- Python-side `codeengine` module, if it exists — may warrant its own standalone page rather than co-habiting with the JS reference.
