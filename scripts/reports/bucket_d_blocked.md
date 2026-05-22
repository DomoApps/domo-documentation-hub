# Bucket D — items blocked on source content

Net-new article requests where the Asana ticket either provides only a one-line description, links to external source material (SharePoint/Dojo) that wasn't captured in the export, or asks for content that requires interview / scoping with the submitter.

To unblock any of these for Claude, drop source material (`.docx`, redlined PDF, exported Dojo HTML, screenshots) into `.asana-cache/<task_id>/` and ping me with the task ID.

Of the 12 Bucket D items, 2 were Claude-doable from the description alone and were completed in commit history (Fiscal Calendar Note on Cloud Integrations Overview; Oracle Architectural Overview prose), and 1 was removed from the local to-do list at the submitter's discretion (1211982452048634 — L1 troubleshooting article). The remaining 9 are listed here.

---

## High priority — submitter is engaged or content exists somewhere

### 1206884501713115 — Workflows Cleanup *(High priority)*

- **Submitter:** Aaron Schofield (took over from Karl Altern, who left Domo)
- **Source:** `domosoftware-my.sharepoint.com/.../personal/karl_altern_domo_com/EWS3gRnDr19Og6qkx8Sj1xQBs7Xq3Q_y-lYV_dvnxIefEQ` — likely not accessible now that Karl has left
- **What's needed:** Karl's draft content, or Aaron's notes on what should go into this Workflows Cleanup page
- **Asana:** https://app.asana.com/0/0/1206884501713115/f

### 1210060928091162 — Usage Reporting

- **Submitter:** dan.brinton@domo.com
- **Source:** `domosoftware.sharepoint.com/.../sites/DevProgramManagement/.../ESpB13pE-exPjRjwLSVCwdABme3QCYmPHiU89OImXIcDYA` (draft KB)
- **Status:** On Hold/Blocked in Asana
- **What's needed:** Export of the SharePoint draft as `.docx` into `.asana-cache/1210060928091162/`
- **Asana:** https://app.asana.com/0/0/1210060928091162/f

### 1209805688338018 — Snowflake Pass-Through SQL BETA

- **Submitter:** andrea.henderson@domo.com (same submitter as Query DataSet Tile)
- **Note:** Andrea wrote "I'm attaching the KB documentation template" but no attachment exists in `.asana-cache/`. The Asana export missed it.
- **What's needed:** Re-export the attachment from Asana, or have Andrea resend the template
- **Suggested home:** Linked from `s/article/000005455` (Magic ETL on Snowflake) — Andrea suggested either a linked article or a section within
- **Asana:** https://app.asana.com/0/0/1209805688338018/f

### 1204262218316263 — Window Functions in Beast Mode *(Low priority)*

- **Submitter:** anoosha.medarametla@domo.com
- **Source:** Internal Dojo post `https://dojo.domo.com/internal/discussion/55182/window-functions-in-beast-mode`
- **What's needed:** Copy of the Dojo post content (or a fresh draft summarizing window-function patterns currently supported in Beast Mode)
- **Asana:** https://app.asana.com/0/0/1204262218316263/f

---

## Needs scoping from submitter — description is too thin

### 1211916967943002 — Add Model differences to the DOMO AI section

- **Submitter:** ken.boyer@domo.com
- **Full description:** "Add Model differences to the DOMO AI section" (44 chars total)
- **What's needed:** Which models? Which differences? Where does the "DOMO AI section" live in the KB? Possibly the `s/article/000005544` (AI Prompts in Jupyter) area, or a parent AI/Domo.AI overview.
- **Asana:** https://app.asana.com/0/0/1211916967943002/f

### 1206468170605978 — Beta AI adapters article

- **Submitter:** mckenna.payne@domo.com
- **Description:** "This is a new knowledge article about the Domo.AI Adapters and how to set them up"
- **What's needed:** Either the setup steps themselves (from McKenna) or access to a beta-program doc that already exists
- **Asana:** https://app.asana.com/0/0/1206468170605978/f

### 1209294086210254 — Brand Kit: Remove Email Footer

- **Submitter:** ken.boyer@domo.com
- **Description:** "I have created a document with the necessary steps. We need to add a page/section to Brand Kit to explain how to remove the footer from emails"
- **Target article:** `s/article/5428851518999.mdx` (Brand Kit)
- **What's needed:** Ken's "document with the necessary steps" — not in `.asana-cache/`
- **Asana:** https://app.asana.com/0/0/1209294086210254/f

### 1208975689727859 — Instance Template (Domo Everywhere)

- **Submitter:** ken.boyer@domo.com
- **Description:** "Create a new KB article under Domo Everywhere for Partner expansion"
- **What's needed:** What is an "Instance Template" in this context? Is it the Domo Everywhere partner-onboarding template? Source content needed.
- **Asana:** https://app.asana.com/0/0/1208975689727859/f

### 1208810692509537 — Athena read-only KB

- **Submitter:** felipe.suarez@domo.com
- **Description:** "Please add Athena to the Setup section links and create the Athena KB article"
- **Note:** The Amazon (Redshift, Athena) nav group at `docs.json:139-154` already contains several Athena articles (`s/article/360042931634`, `360042931654`). It's not clear if this asks for a *new* Athena-on-Cloud-Integrations article (matching the Databricks pattern) or for nav-link cleanup.
- **What's needed:** Confirmation from Felipe on whether the request is satisfied by existing Athena articles, or whether a new Cloud Integration-style Athena article (like `s/article/000005289` Databricks) is needed.
- **Asana:** https://app.asana.com/0/0/1208810692509537/f

---

## Summary

| Task ID | Name | Block reason |
|---|---|---|
| 1206884501713115 | Workflows Cleanup | SharePoint draft owned by ex-employee |
| 1210060928091162 | Usage Reporting | SharePoint draft not exported |
| 1209805688338018 | Snowflake Pass-Through SQL BETA | Attachment missing from export |
| 1204262218316263 | Window Functions in Beast Mode | External Dojo post |
| 1211916967943002 | Model differences in DOMO AI | 44-char description |
| 1206468170605978 | Beta AI adapters | No source content |
| 1209294086210254 | Brand Kit remove email footer | Submitter has document not attached |
| 1208975689727859 | Instance Template | Term/scope unclear |
| 1208810692509537 | Athena read-only | Existing Athena articles may already satisfy |
