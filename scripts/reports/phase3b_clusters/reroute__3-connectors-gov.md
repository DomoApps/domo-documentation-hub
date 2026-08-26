# Phase 3b RE-ROUTE cluster: reroute__3-connectors-gov

These gaps were correctly skipped by earlier waves because the gap data mislinked them. Each is re-homed to its correct article below. Some target files were already edited in an earlier wave — read current state first and add ONLY the new gap's content.

Follow the shared agent instructions (3 quality gates, [pm-input] deferral, no TODO markers, imperative Title Case, English-only, no Next Steps/Related links).

---

## `s/article/360042931954.mdx`
**Marker PM for this file:** Tasleema Lallmamode

### Gap rank 193 (Medium, score 52.5) — Email connector: subject/attachment regex, CSV encoding, sender identification
- **Routing note:** DataSet via Email connector (was pointed at a Pinterest connector). Add subject/attachment regex, CSV vs CSV-UTF-8 encoding, sender identification.
- **What's missing:** Need documentation on: how subject/attachment-name regex actually works (it filters allow/deny, does NOT extract capture groups into columns), correct regex patterns to avoid dropping all rows, CSV vs CSV-UTF-8 encoding requirements, and the lack of any 'from' sender record. Sender tracking is also a feature request.
- **Original suggested location:** Update the Email connector article: clarify that subject/attachment regex filters (allow/deny) and does not extract capture groups into columns, give safe regex examples, document the CSV vs CSV-UTF-8 encoding requirement, and note that the sender address is not captured (feature request).

---

## `s/article/360042933494.mdx`
**Marker PM for this file:** Tasleema Lallmamode

### Gap rank 314 (Low, score 43.2) — Campaigns app: re-subscribing after unsubscribe
- **Routing note:** Campaigns App User Guide (was pointed at a Campaigns date-format reference). Add re-subscribe-after-unsubscribe / manual removal from unsubscribers list. Likely [pm-input] — mechanic not documented in KB.
- **What's missing:** Documentation of how to re-subscribe a recipient who used a campaign unsubscribe link (e.g. manually removing them from the unsubscribers list), since the email-reply method does not work.
- **Original suggested location:** Update or add to the Campaigns app documentation set: add a short FAQ/section on the unsubscribe list and how to re-subscribe a recipient (manual removal from the unsubscribers list), noting the email-reply method does not work.

---

## `s/article/360042932414.mdx`
**Marker PM for this file:** Tasleema Lallmamode

### Gap rank 234 (Medium, score 49.6) — NetSuite SuiteAnalytics permission changes / migration to JDBC OAuth; UPSERT and writeback enhancements
- **Routing note:** NetSuite Writeback connector — writeback object/transform reference HALF ONLY (the SuiteAnalytics Upsert/date parts were done in 360043433453). Add writeback-specific object/transform reference.
- **What's missing:** Document the SuiteAnalytics permission requirement change and migration path to NetSuite JDBC OAuth; document the now-shipped UPSERT support on SuiteAnalytics Connect; provide a writeback object/transform support reference. Some items (Case object writeback, transform options) are feature requests.
- **Original suggested location:** Update the NetSuite SuiteAnalytics Connect connector article with the permission-change advisory and migration path, plus the now-shipped UPSERT support. Update the NetSuite Writeback connector article with a supported-object/transform reference (note Case object/transform options are feature requests).

---

## `s/article/360043438213.mdx`
**Marker PM for this file:** Dan Brinton

### Gap rank 200 (Medium, score 51.8) — SSO / SCIM onboarding and IdP SSL certificate expiration handling
- **Routing note:** Troubleshoot Single Sign-On Using SAML (the SCIM article 000005241 was the wrong home; the inferred 360042934374 does not exist). Add the two-certificate distinction (IdP-needs vs from-IdP) and which cert expiration affects SAML auth-request signing. Likely [pm-input] for the cert mechanics.
- **What's missing:** Practical SCIM onboarding walkthrough (KB exists but users want more), and clear guidance on 'Information your IdP may need' vs 'Information from your IdP' certificates — which certificate expirations affect SAML auth-request signing and what the customer must do (OIDC and non-signing SAML unaffected).
- **Original suggested location:** Update the SSO configuration article to add an explicit section on the two certificates ('Information your IdP may need' vs 'from your IdP'), which expiration affects SAML auth-request signing, and what the customer must do (OIDC and non-signing SAML unaffected). Optionally expand the SCIM article with a fuller onboarding walkthrough.

---

## `s/article/360043438473.mdx`
**Marker PM for this file:** Jordan Jensen

### Gap rank 179 (Medium, score 53.5) — Domo Course Builder: importing existing cards and YouTube embeds breaking
- **Routing note:** CourseBuilder YouTube-embed portion ONLY (edit/import halves were handled in 360042935714). This 'Best Practices for Using CourseBuilder' article documents Video IDs / provider selection. Correct the guidance: CourseBuilder uses the video ID from a youtube.com/watch?v=ID URL via a provider selector, NOT an /embed/ URL. Flag 'YouTube not showing' as a possible bug via [pm-input].
- **What's missing:** Document Course Builder workflows: locating/editing the project behind a training card, supported YouTube embed URL format (youtube.com/embed/VIDEO_ID), and the download-design / desktop-app import format. Possible bug to surface, but the import/embed expectations need docs.
- **Original suggested location:** Update s/article/360042935714.mdx (Creating and Importing CourseBuilder Apps) to document locating/editing the project behind a published training card, the supported YouTube embed URL format (youtube.com/embed/VIDEO_ID), and the download-design vs desktop-app import format. Flag the YouTube-not-showing behavior to the product team as a possible bug.

---
