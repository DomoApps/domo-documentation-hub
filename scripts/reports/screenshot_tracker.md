# Screenshot tracker

Outstanding screenshot work surfaced by the Asana backlog execution batches.

For each entry below, the surrounding article text has already been updated and is publishable as-is — the screenshot is supplemental. Drop the image into `images/kb/` using the suggested filename, then replace the matching `{/* TODO[screenshot]: ... */}` marker in the article with a normal `<Frame><img ... /></Frame>` block.

When complete, check the box.

## Format

```
- [ ] **<Task name>** — `<article path>`
  - **Describes:** what the screenshot should depict
  - **Source:** `.asana-cache/<task_id>/<file>` OR "needs new screenshot"
  - **Suggested filename:** `images/kb/<descriptive-name>.png`
  - **Marker in article:** snippet of the TODO comment to find
```

---

## Outstanding

### ✅ Workflows: Design Your Workflow — `s/article/000005331.mdx`

[Asana task](https://app.asana.com/0/0/1212438657897940/f) · Both refreshed screenshots embedded in EN and JA siblings on 2026-05-22.

- [x] **AddingShapeToCanvas** — `images/kb/workflows-adding-shape-to-canvas.png` *(embedded; shows the Add-action menu with Automated Tasks / User Task / Flow Controls / AI Agent Task categories)*
- [x] **ConnectingSteps** — `images/kb/workflows-connecting-steps.png` *(embedded; shows ports and a connecting line being drawn between Forecasting Data and Send Email Notification)*

### ✅ Access Scheduled Reports dropdown — `s/article/360043437773.mdx`

[Asana task](https://app.asana.com/0/0/1211443299710978/f) · Feature is already deployed to all customers. Surrounding prose describes the dropdown generically because the option names were not confirmed in the task body.

- [x] **Scheduled Reports navigation dropdown** — `images/kb/scheduled-reports-navigation-dropdown.png` *(embedded; sourced from .asana-cache/1211443299710978/Screenshot_2025-09-23_at_10.11.47_AM.png — shows the Dashboard/Card/Report dropdown options)*

### ✅ Snowflake Account Identifier — `s/article/4402322966807.mdx`

[Asana task](https://app.asana.com/0/0/1209313933155042/f) · Surfaced because both Snowflake and Domo docs leave users hunting for where to find the account identifier. Body text lists three locations; the screenshot illustrates one of them.

- [x] **Snowflake Account Identifier locations** — `images/kb/snowflake-account-identifier.png` *(embedded; sourced from .asana-cache/1209313933155042/Screenshot_2025-02-03_at_3.36.28_PM.png — shows the Snowsight account details popover with identifier, organization, region, and locator)*

### ⏭️ Properties for Bar Charts — `s/article/360043429813.mdx`

[Asana task](https://app.asana.com/0/0/1206247708235860/f) · **Skipped per user direction on 2026-05-22.** Body prose self-describes Plain vs. Tooltip behavior; TODO markers removed from both EN and JA files. Asana ticket closed.

- [x] ~~Hints Style — Plain~~ (skipped)
- [x] ~~Hints Style — Tooltip~~ (skipped)

### ⏸️ AUDIT | Enable SSO with Okta — `s/article/360043438133.mdx`

[Asana task](https://app.asana.com/0/0/1204480786007423/f) · **On hold pending submitter verification (2026-05-22).** The EN procedure rewrite (commit c9efe77b) and its JA parity port (commit cedb995e) were both done from training-data knowledge of the Okta Admin Console flow — no live Okta access, no docs lookup, and the submitter's offered test instance / Zoom walkthrough was never used. Confirm the field labels, dialog flow, and Directory paths against the live UI **before** capturing screenshots; the captures will lock in whatever wording the article currently uses.

- [ ] **Okta Admin Console home** — `images/kb/okta-sso-admin-console-home.png`
  - Describes: Admin Console home with left-hand navigation, Applications expanded.
  - Source: needs new screenshot.
- [ ] **Applications list with Create App Integration** — `images/kb/okta-sso-create-app-integration.png`
  - Describes: Applications list page with the Create App Integration button highlighted.
  - Source: needs new screenshot.
- [ ] **SAML 2.0 selection dialog** — `images/kb/okta-sso-saml-2-selection.png`
  - Describes: Create a new app integration dialog with SAML 2.0 selected.
  - Source: needs new screenshot.
- [ ] **View SAML setup instructions link** — `images/kb/okta-sso-view-saml-setup-instructions.png`
  - Describes: Sign On tab of the Domo app with the View SAML setup instructions link visible.
  - Source: needs new screenshot.
- [ ] **Assignments tab** — `images/kb/okta-sso-assignments-tab.png`
  - Describes: Assignments tab of the Domo app showing the Assign dropdown.
  - Source: needs new screenshot.
- [ ] **Directory > Groups, Add group** — `images/kb/okta-sso-directory-groups-add.png`
  - Describes: Directory > Groups page with the Add group button visible.
  - Source: needs new screenshot.
- [ ] **Directory > People, Add person** — `images/kb/okta-sso-directory-people-add.png`
  - Describes: Directory > People page with the Add person dialog open.
  - Source: needs new screenshot.
- [ ] **Okta end-user dashboard with Domo tile** — `images/kb/okta-sso-end-user-dashboard-domo-tile.png`
  - Describes: Okta end-user dashboard showing the Domo app tile.
  - Source: needs new screenshot.

### Query DataSet Tile — `s/article/Query-DataSet-Tile.mdx`

[Asana task](https://app.asana.com/0/0/1210394972306471/f) · New Databricks-only Magic ETL tile article. Asana status was **On Hold/Blocked** pending two unresolved items below — call out to Andrea Henderson / Joseph Peterson before publishing.

- [ ] **Query DataSet tile in Actions pane** — `images/kb/query-dataset-tile-action-rail.png`
  - Describes: Magic ETL Actions pane with the **DataSets** section expanded and the **Query DataSet** tile highlighted.
  - Source: needs new screenshot — original draft predated the field rename below.
  - Marker in article: `{/* TODO[screenshot]: Magic ETL Actions pane`
- [ ] **Query DataSet tile configuration panel** — `images/kb/query-dataset-tile-config.png`
  - Describes: Query DataSet tile configuration with **Input DataSet**, **Query partition key**, and **# of Loads** fields populated.
  - Source: needs new screenshot — the original screenshot still shows the old label "# of Parallel Loads"; confirm in-UI label is now "# of Loads" before capturing.
  - Marker in article: `{/* TODO[screenshot]: Query DataSet tile configuration panel`

**Outstanding content items (not screenshot work, but tracked here so they don't fall through):**

- [ ] **Confirm field name** — Source draft used "# of Parallel Loads"; the team planned to rename to "# of Loads". The article currently uses "# of Loads". Verify the live UI matches.
- [ ] **Specimen error messages** — Two error strings were stubbed in the Intro (socket timeout; "Exceeds maximum heap size of 16 GB"). Joseph Peterson was to provide the actual strings. Replace the bullets and remove the `TODO[content]` marker once supplied.

### ✅ Wire an App — `s/article/Wiring-an-App.mdx`

[Asana task](https://app.asana.com/0/0/1204896213998141/f) · All 6 originals extracted from `.asana-cache/1204896213998141/Wiring_an_App.docx` and embedded on 2026-05-22. Note: docx `image4.png` and `image5.png` were swapped relative to article order — image5 (DataSet table) maps to the DataSet display marker; image4 (form + submitted rows) maps to the Collection write/read marker.

- [x] **Wiring screen overview** — `images/kb/wiring-app-screen-overview.png` *(docx image.png)*
- [x] **DataSet dropdown and alias-to-column mapping** — `images/kb/wiring-app-dataset-alias-mapping.png` *(docx image2.png)*
- [x] **Collections tab with create/existing toggle** — `images/kb/wiring-app-collections-toggle.png` *(docx image3.png; shows appDBFormExampleCollection config view)*
- [x] **Example App displaying wired DataSet** — `images/kb/wiring-app-example-dataset-display.png` *(docx image5.png)*
- [x] **Example App writing to and reading from a Collection** — `images/kb/wiring-app-example-collection-form.png` *(docx image4.png)*
- [x] **Sample manifest.json** — `images/kb/wiring-app-manifest-sample.png` *(docx image6.png)*
