# Code Engine Documentation — Source Citations & Verification Log

Working notes for the rework. Every technical claim in a new page must be traceable here. Any unverifiable claim is marked UNVERIFIED and logged at the bottom.

## Sibling repos (siblings to this repo)

- `~/Documents/GitHub/DomoWeb/DomoWeb/public/javascripts/codeEngine/` — Code Engine UI (TypeScript/React). Authoritative for endpoints, request/response shapes, enums.
- `~/Documents/GitHub/domo.js/` — ryuu.js SDK. Authoritative for `domo.codeEngine(alias, input)`.
- `~/Documents/GitHub/domoapps/` — Ryuu and Odyssey servers. Authoritative for server-side resolution and Workflow integration.

## Endpoint inventory (source: DomoWeb `api/function.api.ts` and `api/permissions.ts`)

| Endpoint | Method | Source file:line | Purpose |
|---|---|---|---|
| `/api/codeengine/v2/packages/{id}/versions/{version}/functions/{name}` | POST | `function.api.ts:142` | Run Function (preview from UI) |
| `/api/codeengine/v2/packages/{id}/executions/{executionId}` | GET | `function.api.ts:148` | Get Execution by ID |
| `/api/codeengine/v2/packages/{id}` | GET | `function.api.ts:30` | Get Package (`?parts=versions`) |
| `/api/codeengine/v2/packages/{id}/versions/{version}` | GET | `function.api.ts:166` | Get Version (`?parts=functions,code,privateFunctions`) |
| `/api/codeengine/v2/packages/{id}/versions/{version}/release` | POST | `function.api.ts:157` | Release Version |
| `/api/codeengine/v2/packages/{id}/share` | POST | `function.api.ts:175` | Share (incremental) |
| `/api/codeengine/v2/packages/{id}/permissions` | GET | `permissions.ts:8` | Get Permissions |
| `/api/codeengine/v2/packages/{id}/permissions` | POST | `permissions.ts:14` | Set Permissions |

**Excluded from public reference** (UI-owned — per spec decision):
- `POST /api/codeengine/v2/packages` (create), `PUT /api/codeengine/v2/packages/{id}` (properties), `DELETE /api/codeengine/v2/packages/{id}` (delete), `DELETE /api/codeengine/v2/packages/{id}/versions/{version}` (delete version).

## Custom App SDK (source: domo.js `src/models/services/codeengine.ts`)

- `domo.codeEngine<T>(alias, input?, options?)` → `POST /domo/codeengine/v2/packages/{alias}` → `Promise<T>`.
- Deprecated variant `/domo/codeengine/v2/packages/{alias}/complex` (2023-06-27) — not on SDK.

## Type system (source: DomoWeb `models/enums.ts` + `workflows/models/enums/DataTypes`)

`TypeEnumV2` / `WorkflowDataType` values available for function inputs/outputs:
- `text`, `number`, `decimal`, `boolean`, `date`, `dateTime`, `time`, `duration`, `object`, `person`, `dataset`, `group`
- `account` (gated on `FeatureFlag.ACCOUNT_ENTITY`)
- `file`, `directory` (gated on `FileSetFeatureAccess.isEnabled()`)
- Excluded from UI pickers: `JSON`, `STRING_BUILDER`

## Execution status (source: `models/enums.ts` ExecutionStatus)

`SUCCESS`, `FAILED`, `RESULT_TYPE_FAILURE`, `RUNNING`, `UNDEFINED`, `OUTPUT_UNDEFINED`.

## Permissions (source: `models/constants.ts` accessLevelToPermissionsMap)

UI label → API value:
- `OWNER` → `OWNER`
- `CAN_EDIT` → `WRITE`
- `CAN_SHARE` → `READ`
- `CAN_EXECUTE` → `EXECUTE`
- `NO_ACCESS` → `NONE`

## Runtime environments (source: `models/enums.ts` Environments)

`LAMBDA` (general-purpose, customer-visible), `ARRAKIS`, `DOMOACTION`, `MODELENDPOINT`, `PYTILE`, `UNDEFINED`.

## Runtimes (source: `models/enums.ts` RuntimesEnumV2)

`JavaScript`, `Python`.

## UNVERIFIED (source needed)

- **JS `codeengine` module method surface.** Current docs list `sendRequest`, `getAccount`, `axios`, `getPersonDetails`, `getExecutionDetails`. Runtime source not located in accessible sibling repos. **Action during plan execution:** search for the Code Engine Lambda/sandbox runtime (likely a separate internal service). If not found, ship pages with "as of 2026-04-23" note and log as followup.
- **JS `require()` allowlist.** Current `javascript-libraries.mdx` lists only 3 libraries. Runtime allowlist not located. **Action:** same as above.
- **Python runtime allowlist** — the list in `python-packages.mdx` has not been verified against runtime source.
- **Python-side `codeengine` equivalent module.** Existence unconfirmed.
- **Account alias configuration model.** `AccountAliasConfiguration` is defined in DomoWeb but the server-side contract (how it's stored, mapped, retrieved) hasn't been traced.
