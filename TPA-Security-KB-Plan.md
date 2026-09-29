# KB Plan: Security Control Evidence Gaps (TPA Assessment)

Sep 29, 2026 · Jared Peterson · Source doc: https://claude.ai/code/artifact/dc0471d1-c387-44eb-8b7a-f3a421db02c5

> **Internal working file.** Contains customer names, a customer hostname, and internal email text. Do not reference it from `docs.json` and do not publish any part of it verbatim.

## Summary

The KB has no page that states Domo's security control posture for encryption in transit, vulnerability remediation, or log retention, so the RFP team had to assemble answers for NAB's Third Party Assessment by email. This plan adds one canonical security reference cluster to the KB so the next assessor, CSM, or proposal manager can cite a public page instead of chasing Information Security.

The core fix is one new reference article, **Security and Compliance Reference** (`s/article/Security-and-Compliance.mdx`). It has one section per control: Encryption in Transit (TLS), including how customers verify TLS on their own instance; Vulnerability and Patch Management; and Security Logging and Log Retention. It also covers certifications and how to request SOC reports. An assessor gets everything from one URL, and the RFP team can deep-link a single control by section anchor. Every statement is taken from Paul Conover's approved wording or the 2025 SOC 1/SOC 2 Type II control text, and nothing publishes without InfoSec sign-off.

**For the executing agent:** the full email thread, the SSL Labs screenshot, and the exact current repo text are in [Reference: email and repo](#reference-email-and-repo) at the end of this file. Work only from that section and InfoSec's written answers to the open questions.

## The request

On 11 September 2026 NAB's Third Party Assessment team asked for more evidence on three controls. Doug Zagami (Senior Proposal Manager) drafted answers, Paul Conover (VP, Information Security & Compliance) resolved the TLS question on 15 September, and on 25 September Doug flagged to Paul and Jared that none of it is in the KB.

| Control | NAB's ask (verbatim) | Domo's approved answer | Evidence source |
| --- | --- | --- | --- |
| TLS 1.3 implementation | "Evidence confirming TLS 1.3 is implemented for data in transit. Examples may include security standards, network/security architecture documentation, configuration screenshots, or other relevant artefacts." | Minimum supported TLS for external customer communications is 1.2. TLS 1.3 is supported where the client and connection path support it. Version is negotiated automatically; customers do not configure or select it per instance. | SSL Labs scan of the customer's instance (e.g. nab-au.domo.com: A+ rating, "This server supports TLS 1.3") |
| Patch management timelines | "Patch Management Policy, Vulnerability Management Standard, or equivalent documentation showing defined remediation timelines for vulnerabilities (e.g., Critical, High, Medium, Low)." | Critical/High with known exploitation: 7 days (highest-exposure assets), 14 days (lower exposure). High without active exploitation: 14 days from patch availability. Medium/Low: routine cadence by asset class. CVSS 7.0+ triggers out-of-band remediation. | 2025 SOC 2 Type II, Control CC7.1 (bi-weekly internal and external scanning; no deviations) |
| Log retention | "Logging and Monitoring Policy or equivalent documentation confirming security logs are retained for a minimum of 12 months." | System logs are retained for one year and record user activity, system events, date/time, and affected objects. | 2025 SOC 2 Type II CC7.2 and PI1.5; 2025 SOC 1 Type II CO6.4 (no deviations) |

Two earlier InfoSec answers read as contradictory: "The floor TLS for Domo is 1.2. It is not configurable to be explicitly 1.3" (8 May 2026) and "Domo does support TLS 1.3 concurrently" (13 August 2026). Paul's 15 September statement reconciles them, and that reconciliation is what the KB is missing. Domo does not distribute internal security policies, so the KB must publish summaries, not the policies themselves.

## Current KB coverage

The KB touches all three controls only in passing, and its one explicit TLS statement is now incomplete. Repo: `~/Documents/GitHub/domo-documentation-hub` (Mintlify; checked at `main` @ `535b1602`). Live pages were confirmed through the Domo documentation index on domo.com/docs.

| Article (repo path) | What it says today | Problem |
| --- | --- | --- |
| [Mobile Enterprise Security](https://domo.com/docs/s/article/1500007028582) · `s/article/1500007028582.mdx` line 49 | "…Domo uses a combination of secure protocols, including TLS… We use TLS 1.2." | States 1.2 as if it were the only version; no mention of 1.3 or negotiation. This is the sentence an assessor finds. |
| [Domo Mobile Security](https://domo.com/docs/s/article/360043428233) · `s/article/360043428233.mdx` line 26 | Same paragraph, ending "We use TLS 1.2." Also says pen tests run "bi-annually". | Same TLS gap. Pen test frequency conflicts with domo.com/platform/security ("annual penetration tests"). |
| `ja/s/article/1500007028582.mdx` line 43 · `ja/s/article/360043428233.mdx` line 26 | Japanese translations of the same paragraph | Must be re-localized after the English fix. No de/es/fr copies exist. |
| [Domo FAQs](https://domo.com/docs/s/article/360043427493) · `s/article/360043427493.mdx` line 24 | "Is there an ISO 27001 certification?" answer | Only compliance mention in the KB; no SOC 1/SOC 2, no report-request path. Also has a ja copy. |
| [Activity Log](https://domo.com/docs/s/article/360042934574) · `s/article/360042934574.mdx` lines 35, 46 | Activity log holds "the rolling one-year period" | Customer-facing log only; says nothing about Domo's internal security/system log retention. |
| Shipping Logs to SIEM · `portal/Security/Integration with SIEM.mdx` | Webhook export of Activity logs to Sentinel | Useful for "keep logs longer yourself"; not linked from any KB security page. |
| [Domo APIs](https://domo.com/docs/s/article/360043439793) `s/article/360043439793.mdx` · [Federated Data](https://domo.com/docs/s/article/360042932974) `s/article/360042932974.mdx` §Data in Transit · [Workbench Encryption](https://domo.com/docs/s/article/000005248) `s/article/000005248.mdx` line 28 | "Encrypted in transit" / "vulnerability assessments" in general terms | No version, timeline, or link to a canonical page. |

Nothing in `s/article/`, `s/topic/`, or `portal/` mentions TLS 1.3, SOC 2, remediation timelines, or CVSS. The nav group **Knowledge Base › Admin › Administrate Domo › Security** (`docs.json` line 2417) holds ten configuration how-tos (MFA, IP allowlist, BYOK, sessions, passwords, tokens) and no reference content. The public [security page](https://www.domo.com/platform/security) lists SOC 1, SOC 2, ISO 27001, ISO 27018, HIPAA, HITRUST, GDPR, and CCPA, but gives no TLS version, retention period, or report-request process.

## Gap analysis

Two of three controls are missing outright, and the third is covered by a sentence that undersells Domo's posture.

| Control | KB status | Specific gap | Fix (see Proposed changes) |
| --- | --- | --- | --- |
| TLS / encryption in transit | Partial, misleading | "We use TLS 1.2" in two mobile articles; no TLS 1.3, no negotiation, no "not configurable per instance" statement; no way for a customer to evidence it | Article §Encryption in Transit (TLS) and its Verify subsection; update B1, B2, B3 |
| Vulnerability and patch management | Missing | No remediation timelines, CVSS threshold, scanning cadence, or SOC 2 CC7.1 reference; pen test frequency inconsistent (bi-annual vs annual) | Article §Vulnerability and Patch Management; fix B2 pen test line |
| Security log retention | Missing (customer log only) | Activity Log's one-year window is documented, but not Domo's system log retention or its SOC control references | Article §Security Logging and Log Retention; update B5, B6 |
| Compliance evidence and reports | Minimal | Only the ISO 27001 FAQ; no SOC 1/SOC 2 page, no report-request path, no "we don't share internal policies" statement | Article §Certifications and Audit Reports; update B4 |
| Discoverability | Missing | Security nav group is config-only; no page an assessor can land on | Add the article first in the Security nav group |

## Proposed changes

One new article (A) and seven edits to existing ones (B1–B7). All copy below is draft, built only from the approved statements in the Reference section; the executing agent must not add claims beyond them. The new file needs `title` and `excerpt` frontmatter (never `description`), starts with `## Intro`, and follows `Domo-KB-Style-Guide.mdx`.

### New article: Security and Compliance Reference

| Field | Value |
| --- | --- |
| File | `s/article/Security-and-Compliance.mdx` |
| URL | `/s/article/Security-and-Compliance` |
| title | Security and Compliance Reference |
| excerpt | "How Domo encrypts data in transit, remediates vulnerabilities, and retains security logs, with the SOC 1 and SOC 2 controls that verify each and how to request audit reports." |
| Diátaxis type | Reference, with one short how-to subsection (Verify TLS) kept inline because assessors ask for the policy and the evidence together |
| Nav | First entry in the Knowledge Base › Admin › Administrate Domo › Security group |

Section anchors are what B1–B7 and the RFP team link to, so keep these headings exactly as written (Mintlify slugs them as shown).

| Heading | Anchor |
| --- | --- |
| Certifications and Audit Reports | `#certifications-and-audit-reports` |
| Encryption in Transit (TLS) | `#encryption-in-transit-tls` |
| Verify TLS Support for Your Instance | `#verify-tls-support-for-your-instance` |
| Vulnerability and Patch Management | `#vulnerability-and-patch-management` |
| Security Logging and Log Retention | `#security-logging-and-log-retention` |

#### Article outline and draft copy

- **## Intro** — This article summarizes Domo's security controls for customers and third-party assessors, with the independent audit controls that verify each one. Include: "Domo does not distribute copies of its internal security policies; the applicable standards are summarized here." (adapted from Doug's approved response). Add a short jump list to the four sections below.
- **## Certifications and Audit Reports**
    - List from domo.com/platform/security: SOC 1, SOC 2, ISO/IEC 27001, ISO/IEC 27018, HIPAA, HITRUST, GDPR, CCPA.
    - SOC 1 and SOC 2 Type II reports are available to customers; the 2025 reports cover 1 January 2025 to 30 November 2025.
    - Request path: **open question Q3**; do not invent one.
    - `<Tip>`: in an assessment, cite this article's section URL plus the matching SOC control ID.
- **## Encryption in Transit (TLS)**
    - Paul Conover's 15 September statement, lightly edited for KB voice, meaning unchanged: "Domo's minimum supported TLS version for external customer communications is TLS 1.2. Domo also supports TLS 1.3 where the client and connection path support it. The TLS version is negotiated automatically when a session is established, so customers do not configure or select a TLS version for their Domo instance. TLS 1.3 is therefore supported concurrently, with TLS 1.2 as the minimum."
    - **### How TLS Version Is Selected** — Client and server agree on the highest mutually supported version; a modern browser or client connecting to `<instance>.domo.com` will typically use TLS 1.3. No cipher lists unless InfoSec supplies them.
    - **### Other Secure Transfer Protocols** — Reuse approved wording from `1500007028582.mdx` line 49: SSH and SFTP supported where appropriate; no clear-text or unencrypted protocols allowed.
    - **### Verify TLS Support for Your Instance** (numbered steps):
        1. Go to [SSL Labs Server Test](https://www.ssllabs.com/ssltest/).
        2. Enter your instance hostname, for example `yourcompany.domo.com`.
        3. (Optional) Select **Do not show the results on the boards**.
        4. Select **Submit** and wait a few minutes for the scan to finish.
        5. Screenshot the **Summary** panel with the address bar visible. It shows the overall rating and the banner "This server supports TLS 1.3." Optionally also capture **Configuration › Protocols**.
    - Screenshot: a NEW capture from a Domo-owned instance (never NAB's `nab-au.domo.com`), saved as `images/kb/Security-and-Compliance-ssllabs-summary.png`, wrapped in `<Frame>`. The NAB image in the Reference section shows the target layout only.
    - `<Note>`: a third-party scan reflects the connection path it tests (the browser-facing endpoint).
    - Optional, KB admin's call: `openssl s_client -connect yourcompany.domo.com:443 -tls1_3` for technical admins.
- **## Vulnerability and Patch Management**
    - Lead: "Domo maintains approved patch and vulnerability management standards that prioritize remediation by severity and exposure, scored using CVSS."
    - **### Remediation Timelines** — Table (Severity · Target), from the approved response:
        - Critical and High, known exploitation · 7 days for highest-exposure assets; 14 days for lower-exposure asset classifications
        - High, no active exploitation · 14 days from patch availability
        - Medium and Low · Routine patch cadence, assigned by asset class and prioritized by exposure and risk tier
        - Any CVSS 7.0 or above · Expedited, out-of-band remediation
    - **### Scanning and Testing** — Internal and external scanning runs bi-weekly (SOC 2 CC7.1 control activity). Third-party penetration testing; frequency pending **Q4**.
    - **### Independent Assurance** — "Domo's 2025 SOC 2 Type II report addresses this process under Control CC7.1. The service auditor reported no deviations."
    - **### Report a Vulnerability** — Link to Domo's responsible disclosure program (from domo.com/platform/security).
    - Gate: the timelines table publishes only with explicit InfoSec approval (**Q1**). If Q1 is "no", ship this section with the lead, scanning, and assurance paragraphs only.
- **## Security Logging and Log Retention**
    - **### Domo System Log Retention** — "System logs are retained for one year. Logs track both user activity and system events and record the date and time of each event and the objects affected." Assurance: SOC 2 Type II CC7.2 (repeated under PI1.5) and SOC 1 Type II CO6.4, no deviations.
    - **### Activity Log in Your Instance** — Rolling one-year window; link `/s/article/360042934574`.
    - **### Keep Activity History Longer** — DomoStats Activity Log report (`/s/article/360043433813`) and SIEM export (`portal/Security/Integration with SIEM.mdx`, permalink `shipping-logs-to-siem`).
- **## Related Security Settings** — Table: Setting · What it controls · Link, for BYOK (`/s/article/360043427593`), MFA (`/s/article/360043439193`), IP allowlisting (`/s/article/360043439173`), Session Settings (`/s/article/000005431`).
- **## FAQ** (`<AccordionGroup>`):
    - "Can I require TLS 1.3 only for my instance?" → No. Version is negotiated automatically and is not configurable per instance.
    - "Does Domo accept TLS 1.0 or 1.1?" → No; 1.2 is the minimum (confirm wording with InfoSec).
    - "Does this apply to connectors, Workbench, and Federated connections?" → **Open question Q2**; omit until answered.
    - "Can I get a copy of Domo's security policies?" → No; Domo summarizes them here and in its SOC reports.

### Edits to existing articles

| ID | File | Change |
| --- | --- | --- |
| B1 | `s/article/1500007028582.mdx` line 49 | Replace "We use TLS 1.2." with: "Domo requires TLS 1.2 at minimum and supports TLS 1.3, negotiated automatically for each connection. See [Encryption in Transit (TLS)](/s/article/Security-and-Compliance#encryption-in-transit-tls)." |
| B2 | `s/article/360043428233.mdx` line 26 (+ §Third-party penetration testing) | Same TLS replacement as B1. Correct pen test frequency once Q4 is answered. |
| B3 | `ja/s/article/1500007028582.mdx` line 43 · `ja/s/article/360043428233.mdx` line 26 | Re-localize the changed paragraph with the `localize` skill (glossary `localization/glossary/ja.csv`); Masaaki reviews. |
| B4 | `s/article/360043427493.mdx` after line 26 (+ ja copy) | Add FAQ "Does Domo have SOC 1 and SOC 2 reports?" → yes, link `/s/article/Security-and-Compliance#certifications-and-audit-reports`. Add a "See also" link to the same anchor in the ISO answer. |
| B5 | `s/article/360042934574.mdx` near line 35 | Add a `<Note>`: "This log shows activity in your instance. For Domo's platform log retention, see [Security Logging and Log Retention](/s/article/Security-and-Compliance#security-logging-and-log-retention)." |
| B6 | `portal/Security/Integration with SIEM.mdx` | Add one line linking `#security-logging-and-log-retention` (no other edits). |
| B7 | `s/article/360043439793.mdx` line 6 · `s/article/360042932974.mdx` §Data in Transit · `s/article/000005248.mdx` line 28 | Link "encrypted in transit" to `#encryption-in-transit-tls` and "vulnerability assessments" to `#vulnerability-and-patch-management`. Text otherwise unchanged. |

## Implementation

This is standard, non-GA content work: base `main`, two PRs (English, then Japanese), each on its own branch. Repo rules come from `CLAUDE.md` at the repo root; read it before starting.

1. **Branch** — `jared.peterson/tpa-security-articles` (already exists) or a fresh `jared.peterson/security-compliance-reference` off current `main`.
2. **Create the article** at `s/article/Security-and-Compliance.mdx` from `New-Article-Template.mdx`, following the outline above. Callouts bold their label (`**Note:**`). Internal links are root-relative (`/s/article/...`). External links use the `icon-arrow-square-out` pattern used elsewhere in the KB.
3. **Add the TLS screenshot** to `images/kb/Security-and-Compliance-ssllabs-summary.png` on the same branch before the article references it.
4. **Navigation (`docs.json`)** — in the group `"group": "Security"` at line 2417 (Knowledge Base › Admin › Administrate Domo › Security), add `"s/article/Security-and-Compliance"` as the FIRST entry of `pages`, ahead of `"s/article/360042934454"`. Validate the JSON parses (a malformed nav entry broke the build in PR #562).
5. **Apply B1, B2, B4–B7** as exact, minimal edits using the anchors in the table above. Change only the sentences named.
6. **PM ownership** — run `python3 scripts/build-pm-ownership.py` so the new file appears in `Article-PM-Ownership-Reference.mdx` and `.github/CODEOWNERS` under Feature "Application Security" (currently "no PM listed"). Never hand-edit CODEOWNERS.
7. **Tables** — run `python3 scripts/pad_md_tables.py s/article/Security-and-Compliance.mdx`.
8. **PR 1 (English)** — title "Add Security and Compliance Reference article"; assign to Jared Peterson; request review from Paul Conover (content accuracy) and Doug Zagami (assessor usefulness). Commit messages present tense, e.g. `Add Security and Compliance Reference article`, `Update mobile security TLS statement`. Leave `TPA-Security-KB-Plan.md` and its screenshot out of the PR.
9. **PR 2 (Japanese)** — after PR 1 merges, run the `localize` skill for ja on the new article, B3, and the B4 ja copy. Translator review by Masaaki. de/es/fr: only if the localization plan already covers the Security group.
10. **Publish** — merged is not live. PRs in by Thursday go out the following Monday; ask the KB Administrator for a mid-week release if NAB needs the link sooner.

### Acceptance checks

- [ ] Every factual sentence traces to a line in the Reference section or to InfoSec's written answer to an open question
- [ ] No customer names or customer hostnames (`nab-au.domo.com`) appear in any published file or image
- [ ] `grep -rn "We use TLS 1.2" s ja` returns nothing
- [ ] Pen test frequency matches across the article, `360043428233.mdx`, and domo.com/platform/security
- [ ] The article renders in `mintlify dev` (or the preview deployment), appears first under Admin › Security, and all five section anchors resolve from the B1–B7 links
- [ ] The new file has `title` + `excerpt`, no `description`
- [ ] Paul Conover has approved the final wording in the PR
- [ ] This plan file and its screenshot are not referenced from `docs.json` and stay out of the merged PR

## Sequencing and open questions

One article means one review and one publish. If Q1 is still open when the rest is approved, ship with the Vulnerability section at summary level and add the timelines table in a follow-up PR.

| Step | What | Owner | Gated by |
| --- | --- | --- | --- |
| 1 | Send open questions Q1–Q5 to Paul Conover | Jared | — |
| 2 | Draft the full article; apply B1, B2 (TLS line), B4–B7 | Executing agent | Q2 (FAQ entry), Q3 (report path), Q5 (screenshot) |
| 3 | Add the timelines table and pen test frequency; apply B2 pen test line | Executing agent | Q1, Q4 |
| 4 | InfoSec wording review | Paul Conover | Draft in PR 1 |
| 5 | Merge PR 1, publish | Jared | Step 4 |
| 6 | Japanese localization (PR 2) | Executing agent, Masaaki | PR 1 merged |
| 7 | Send Doug and the RFP team (rfp@domo.com) the article URL and section anchors | Jared | Step 5 |

### Open questions for InfoSec

- [ ] **Q1** — Can the remediation timelines and SOC control references (sent to NAB privately) be published on the public KB, or should the Vulnerability and Logging sections stay summary-level?
- [ ] **Q2** — Does "external customer communications" cover connector traffic, Workbench, Federated, SFTP, and API calls, or only browser and app traffic to `*.domo.com`?
- [ ] **Q3** — What is the official path for a customer to request SOC 1/SOC 2 reports (account team, NDA, trust portal)?
- [ ] **Q4** — Is third-party penetration testing annual (domo.com/platform/security) or bi-annual (`360043428233.mdx`)?
- [ ] **Q5** — Which Domo-owned instance can be scanned for the article's public TLS screenshot?

---

## Reference: email and repo

Everything the plan relies on, copied verbatim so the agent needs no mailbox or InfoSec access. Treat this section as the only approved source of security claims; anything not here needs InfoSec's written answer first.

### 1. Email thread (verbatim, oldest first)

Subject: **DOMO - Request for Additional Security Control Evidence - TPA Assessment** · Outlook message ID `AAMkADk3NzZmYzliLWIxNGEtNDhkMy05YTcyLWQ4NjEyMzUzMTU0ZgBGAAAAAAAEm1iHSPw4SqSR8-Nz_M7ZBwAfDFgDsFrCQIUnFyI-vu-cAAAAAAEMAAAfDFgDsFrCQIUnFyI-vu-cAAWvB25PAAA=` (Jared's mailbox; flagged).

#### 1a. Doug Zagami → Paul Conover · Tue 15 Sep 2026, 1:39 PM

From: Doug Zagami <doug.zagami@domo.com> · To: Paul Conover <paul.conover@domo.com> · Cc: Wayne Will <wayne.will@domo.com>; Stewart Faith <stewart.faith@domo.com>; RFP & Security Team <rfp@domo.com>

> Paul,
>
> NAB's Third Party Assessment team came back on 11 September asking for additional evidence on three controls where they felt the evidence provided did not validate the requirement.
>
> **NAB's request:**
>
> **"TLS 1.3 Implementation**
> Evidence confirming TLS 1.3 is implemented for data in transit. Examples may include security standards, network/security architecture documentation, configuration screenshots, or other relevant artefacts."
>
> I have two prior responses from you:
>
> **8 May 2026**
> "The floor TLS for Domo is 1.2. It is not configurable to be explicitly 1.3 for a given Domo instance."
>
> **13 August 2026**
> "Domo does support TLS 1.3 concurrently."
>
> **Q1**
> Can you provide a single consolidated statement that accurately explains Domo's TLS posture for NAB and reconciles the two statements above?
> I would rather use your wording directly than risk inferring the intent behind either statement.
>
> **Q2**
> NAB indicated they would accept any of the following evidence types:
>
> - Security standards
> - Network/security architecture documentation
> - Configuration screenshots
> - Other relevant artefacts
>
> Based on the TLS posture described in your consolidated statement above, what do you believe is the best evidence to provide to NAB, and where or from whom can I obtain it?
>
> ---
>
> **@Stewart Faith**
>
> The responses on the other two controls, patch management timelines and log retention, are finished and ready to go to NAB. Both are answered from the 2025 SOC 1 and SOC 2 Type II reports, which NAB already holds, with the control references and the auditor's testing quoted so their assessment team can validate them directly. TLS is the only one outstanding, pending Paul's answer above.
>
> **Additional Security Control Evidence**
> Domo responses: Patch Management Timelines and Log Retention
>
> **1. Patch Management Timelines**
>
> *Customer question, verbatim*
> "Patch Management Policy, Vulnerability Management Standard, or equivalent documentation showing defined remediation timelines for vulnerabilities (e.g., Critical, High, Medium, Low)."
>
> *Domo evidence response*
> Domo maintains approved patch and vulnerability management standards that prioritise remediation by severity and exposure, scored using CVSS. Domo does not distribute copies of its internal security policies; the applicable standards are summarised below.
>
> *Remediation timelines by severity*
>
> - Critical and High severity vulnerabilities associated with known exploitation are targeted for remediation or mitigation within 7 days for the highest exposure assets and within 14 days for lower exposure asset classifications.
> - High risk vulnerabilities without active exploitation are targeted for remediation or mitigation within 14 days of patch availability.
> - Medium and Low severity vulnerabilities are remediated through Domo's routine patch cadence, which is assigned by asset class and prioritised by asset exposure and risk tier.
> - A CVSS score of 7.0 or above triggers expedited, out of band remediation outside the assigned cadence.
>
> **Independent evidence.** The 2025 SOC 2 Type II report addresses Domo's vulnerability management process under **Control CC7.1**.
>
> | Evidence element | Evidence from the 2025 SOC 2 Type II report |
> | --- | --- |
> | Criterion | "To meet its objectives, the entity uses detection and monitoring procedures to identify (1) changes to configurations that result in the introduction of new vulnerabilities, and (2) susceptibilities to newly discovered vulnerabilities." |
> | Control activity | "Internal and external vulnerability scanning is performed on a bi-weekly basis to identify vulnerabilities and management takes action in accordance with the vulnerability management policy, as necessary, based on the results." |
> | Service auditor testing | "Inspected the vulnerability remediation policy and a sample of vulnerability scans and remediation to determine that internal and external vulnerability scanning was performed on a bi-weekly basis to identify vulnerabilities and management took action in accordance with the vulnerability management policy, as necessary, based on the results." |
> | Test result | "No deviations noted." |
>
> The report's System Description also confirms: "The IRP includes levels of response to identified vulnerabilities that define the expected timelines for remediation based on severity and impact to consumer, brand, and company. These response guidelines are carefully mapped to level of severity determined for the reported vulnerability."
>
> The report covers the period 1 January 2025 through 30 November 2025 and was provided to NAB on 18 August 2026.
>
> **2. Log Retention**
>
> *Customer question, verbatim*
> "Logging and Monitoring Policy or equivalent documentation confirming security logs are retained for a minimum of 12 months."
>
> *Domo evidence response*
> Domo's 2025 SOC 1 and SOC 2 Type II reports confirm that system logs are retained for one year. These logs track user activity and system events and record the date and time of each event and the objects affected. In each examination, the service auditor inspected the retention settings and a sample of logs and reported no deviations.
>
> **Independent evidence.** The one year retention control is addressed under **Control CC7.2** of the 2025 SOC 2 Type II report, where it is repeated under **Control PI1.5**, and under **Control CO6.4** of the 2025 SOC 1 Type II report. The control wording and the auditor's testing are identical in each.
>
> | Evidence element | Evidence from the 2025 SOC 1 and SOC 2 Type II reports |
> | --- | --- |
> | Control activity | "System logs are retained for one year. Logs track both user activity and system events and record the date and time of the event and what objects the event impacted." |
> | Service auditor testing | "Inspected the log retention settings and a sample of logs to determine that system logs were retained for one year and that logs tracked both user activity and system events and recorded the date and time of the event and what objects the event impacted." |
> | Test result | "No deviations noted." |
>
> The reports cover the period 1 January 2025 through 30 November 2025. The SOC 2 Type II report was provided to NAB on 18 August 2026.
>
> Thanks,
> Doug Zagami, Senior Proposal Manager

#### 1b. Paul Conover → Doug Zagami · Tue 15 Sep 2026, 6:36 PM

From: Paul Conover <paul.conover@domo.com> (VP, Information Security & Compliance) · To: Doug Zagami · Cc: Wayne Will; Stewart Faith; RFP & Security Team

> Doug,
>
> **Q1 – TLS 1.3 Implementation**
> The two prior statements are both accurate and address different aspects of Domo's TLS posture. Domo's minimum supported TLS version for external customer communications is TLS 1.2. Domo also supports TLS 1.3 where supported by the client and connection path. TLS protocol version selection is negotiated automatically during session establishment, and customers do not configure or select a specific TLS version for a given Domo instance. As a result, Domo supports TLS 1.3 concurrently while maintaining TLS 1.2 as the minimum supported protocol version.
>
> **Q2 – Recommended Evidence**
> Evidence can be a screenshot demonstrating TLS 1.3 support directly on NAB's domo instance(s), such as ssllabs ssl test ( https://www.ssllabs.com/ssltest/analyze.html?d=nab%2dau.domo.com&latest ). See attached screenshot for the example result evidence (note the tls 1.3 support indicated at the bottom).
>
> Thanks,
> Paul Conover

Attached screenshot (inline `image.png`), SSL Labs result for `nab-au.domo.com`: overall rating A+, Certificate and Protocol Support at 100, Key Exchange and Cipher Strength near 90, and the banner "This server supports TLS 1.3." **Customer-identifying: layout reference only, never publish.**

![SSL Labs summary for nab-au.domo.com showing A+ and "This server supports TLS 1.3"](TPA-Security-KB-Plan-ssllabs-example.png)

#### 1c. Doug Zagami → Paul Conover, Jared Peterson · Fri 25 Sep 2026, 1:09 PM PT

To: Paul Conover; Jared Peterson · Cc: Wayne Will

> Hi Paul,
>
> I can't find this info anywhere in the KB and it seems like that would be a good place to put it.
>
> @Jared Peterson

### 2. People

| Name | Role | Part in this work |
| --- | --- | --- |
| Paul Conover | VP, Information Security & Compliance | Source of TLS statement; approves all security wording |
| Doug Zagami | Senior Proposal Manager | Requester; authored patch and log responses |
| Stewart Faith | Cc'd on thread | Receiving the finished NAB responses |
| Wayne Will | Cc'd on thread | — |
| Jared Peterson | KB Administrator | PR reviewer and publisher |
| RFP & Security Team (rfp@domo.com) | Distribution list | Notify when live |

### 3. Current repo text to change (verbatim)

Repo `~/Documents/GitHub/domo-documentation-hub`, `main` @ `535b1602` ("Merge pull request #562 … fix-ai-toolkits-nav-json").

**`s/article/1500007028582.mdx` (Mobile Enterprise Security), line 49**

> To protect our customers' data as it is transmitted across untrusted networks, Domo uses a combination of secure protocols, including TLS, with only a limited number of trusted ciphers supported. SSH and SFTP are also supported, where appropriate, for the secure transfer of data. Domo does not allow clear text or unencrypted data communication protocols. Domo best practice ensures that all Domo customers use at least one of the provided secured services (TLS, SSH, SFTP). We use TLS 1.2.

**`s/article/360043428233.mdx` (Domo Mobile Security), line 26**

> To protect our customers' data as it is transmitted across untrusted networks, Domo uses a combination of secure protocols, including TLS, with only a limited number of trusted ciphers supported. SSH, and SFTP is also supported, where appropriate, for the secure transfer of data. Domo does not allow clear text or unencrypted data communication protocols. Domo's best practice ensures that all Domo customers use at least one of the provided secured services (TLS, SSH, SFTP). We use TLS 1.2.

**Same file, §Third-party penetration testing**

> Domo undergoes independent third-party application, mobile, system, and network penetration tests bi-annually. The executive reports detailing the scope, any findings, and the status of each finding is then made available to customers in our Independent Security Reports (ISR).

**`s/article/360043427493.mdx` (Domo FAQs), lines 24–26**

> ### Is there an ISO 27001 certification?
>
> We have both the ISO/IEC 27001 and ISO/IEC 27018 certificates for information security management. See the press release for more information.

**`s/article/360042934574.mdx` (Activity Log), line 35**

> The Activity log is updated in near real-time and includes activities logged within the rolling one-year period. You can explore the log with filters on the date range and the person who took the action.

**Japanese copies:** `ja/s/article/1500007028582.mdx` line 43, `ja/s/article/360043428233.mdx` line 26, `ja/s/article/360043427493.mdx`. No de/es/fr copies of these three.

**Navigation:** `docs.json` line 2417, `"group": "Security"`, pages `360042934454`, `360043439173`, `360042934514`, `000005831`, `360043439193`, `360043427593`, `360042934494`, `000005431`, `360042934474`, `360042934534`. Feature in `Article-PM-Ownership-Reference.mdx`: "Application Security" (no PM listed). Mobile articles: Feature "Mobile - iOS", PM Chris Wright.

### 4. Public-site facts used

[Enterprise Security and Compliance](https://www.domo.com/platform/security) (opened 29 Sep 2026): certifications "SOC 1, SOC 2, ISO 27001, ISO 27018, HIPAA, HITRUST, GDPR, and CCPA"; "Transport layer encryption and encryption at rest"; "third-party audits, compliance assessments, and annual penetration tests"; a responsible disclosure program. No TLS version, retention period, or report-request process is stated there.
