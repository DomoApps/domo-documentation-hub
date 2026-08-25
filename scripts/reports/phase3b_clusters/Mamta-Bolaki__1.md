# Phase 3b cluster: Mamta-Bolaki__1

**Owning PM:** Mamta Bolaki
**Files in this cluster:** 3  |  **Gaps:** 8

Edit ONLY the files listed below. Each file gets the forum-gap additions described under it. Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links — that is Phase 5).

---

## `s/article/360043437993.mdx`
*Embed Content Outside of Domo* — area: Domo Everywhere

### Gap rank 124 (Medium, score 58.8) — Embed behaviors: per-user embed IDs, non-universal embed codes, monitoring embed load failures
- **What's missing:** Document that private embed IDs/codes are intentionally user-specific (for security and audit), where to view existing embed IDs in the admin console, and guidance on programmatically monitoring embedded page health (the loading sequence, stack?parts endpoint, TOE codes, and the 401 auth issues users hit when calling it).
- **Suggested location:** Update s/article/360043437993.mdx to clarify whether/why private embed IDs/codes are user-specific and where to view them, and add (or create a new portal/embed/ companion page for) guidance on monitoring embedded-page health: load sequence, the stack?parts endpoint, TOE codes, and the 401 auth pitfalls.

### Gap rank 160 (Medium, score 55.0) — Domo Everywhere publish/share scope and embedded-edit warning
- **What's missing:** Documentation should clarify what 'Public' means for embedded cards (anyone with the link, inside or outside the company), how to scope publication/dataset sharing differently across subscriber sites (including automating dataset re-share for newly added datasets), and explain the 'You are editing content embedded in 1 instance' warning and its implications.
- **Suggested location:** Update s/article/360043437993.mdx to add an FAQ entry explaining the 'You are editing content embedded in N instances' warning, and update s/article/360045120554.mdx to document differential publication/dataset sharing scope across subscriber sites and how newly added datasets get (re)shared.

- **Other referenced articles:** s/article/360045120554.mdx

### Gap rank 166 (Medium, score 54.7) — Embedding Domo content as an iframe (Data Explorer, Salesforce buttons)
- **What's missing:** Embed documentation covering iframe options/permissions for Domo content, and a note/troubleshooting for the Chrome 142 'private network access' change that blocks public-page-to-private-network iframe requests (workaround: open in new tab / access-control headers).
- **Suggested location:** Add a browser-compatibility / troubleshooting note to s/article/360043437993.mdx (or portal/embed/embed-in-sites-and-apps/embedding-into-sites-and-web-portals.mdx) covering Chrome's Private Network Access change that breaks public-page-to-private-network iframes (workarounds: open in new tab, access-control headers), plus clarify which Domo surfaces (e.g. Data Explorer) can/can't be iframed.

- **Other referenced articles:** portal/embed/embed-in-sites-and-apps/embedding-into-sites-and-web-portals.mdx

### Gap rank 303 (Low, score 44.9) — Submitting rich text / inline hyperlinks via Domo Forms
- **What's missing:** Document whether Domo Forms / data-entry support rich text with inline hyperlinks, the HTML-hyperlink approach for table cards and summary numbers, and any workarounds for capturing partial-sentence links.
- **Suggested location:** Update the Forms documentation (portal/Forms/Advanced-Forms/) to state whether form fields support rich text / inline hyperlinks, and cross-link the HTML-hyperlink-in-cards article for the display side. If unsupported, document the limitation and the HTML-in-cell workaround for capturing partial-sentence links.

- **Other referenced articles:** portal/Forms/Advanced-Forms/advanced-form-datasets.mdx

### Gap rank 320 (Low, score 42.8) — Tracking usage/engagement on embedded Domo Everywhere dashboards (iframe analytics)
- **What's missing:** Document how to track embedded-dashboard engagement: Domo Everywhere's built-in interaction tracking and 3rd Party Analytics feature, plus that external iframe-scanning tools can't read inside the embed and what events Domo emits.
- **Suggested location:** Update the '3rd Party Analytics' section of s/article/360043437993.mdx to explicitly note that external page-scanning tools cannot see inside the embed iframe (so DXI integration is required), and list the interaction events Domo captures/emits.

---

## `s/article/4403367344023.mdx`
*Domo Sandbox* — area: App Studio / Migration (Sandbox)

### Gap rank 275 (Medium, score 47.0) — Migrating / duplicating App Studio apps between Domo instances
- **What's missing:** Document how to migrate App Studio apps between instances using Domo Sandbox (enable in source, invite destination, create repository, share) and note that there's no native one-click cross-instance copy.
- **Suggested location:** Update s/article/4403367344023.mdx (Domo Sandbox), or add a short FAQ to the App Studio docs, noting that cross-instance App Studio app migration is done via Sandbox repositories and that there is no native one-click cross-instance copy.

### Gap rank 311 (Low, score 43.4) — Sandbox commit/promotion errors and unsupported items (Forms)
- **What's missing:** Documentation should call out that Forms are unsupported in Sandbox promotion (linking the unsupported-items list) and explain the known defect with non-specific error messaging so users don't chase phantom card errors.
- **Suggested location:** Update s/article/4403367344023.mdx (Domo Sandbox): add a troubleshooting note near the Unsupported Items section mapping the generic dependency/'invalid content entity' error to unsupported items such as Forms, so users stop chasing phantom card errors.

---

## `s/article/4418999855639.mdx`
*Filter Options for the Embedded View Experience* — area: Dashboards / Sharing

### Gap rank 353 (Low, score 37.5) — Deep links / shareable filtered dashboard views
- **What's missing:** Feature request, but an adjacent documentable how-to: pfilter deep-link URL construction and object-ID-based card/page linking patterns (mycompany.domo.com/page/.../kpis/details/...) referenced in comments.
- **Suggested location:** Update or add to a dashboard-sharing article (e.g., s/article/360042932994.mdx) an interim how-to on constructing a filtered-page deep link via pfilter URL parameters and object-ID-based page/card linking for in-app use, distinct from the embed-only pfilter docs. Note auto-generating such links from the UI is a feature request.

- **Other referenced articles:** s/article/360043437993.mdx

---
