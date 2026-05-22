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

### Workflows: Design Your Workflow — `s/article/000005331.mdx`

[Asana task](https://app.asana.com/0/0/1212438657897940/f) · Two refreshed screenshots needed for the Workflows canvas docs. Text and section structure are publishable as-is.

- [ ] **AddingShapeToCanvas** — `images/kb/workflows-adding-shape-to-canvas.png`
  - Describes: The Workflows canvas with the Add-shape action menu open, showing the available shape options.
  - Source: needs new screenshot.
  - Marker in article: `{/* TODO[screenshot]: AddingShapetoCanvas`
- [ ] **ConnectingSteps** — `images/kb/workflows-connecting-steps.png`
  - Describes: Hovering on a workflow step tile to reveal the circular ports, with a connecting line being dragged from one port to another step's port.
  - Source: needs new screenshot.
  - Marker in article: `{/* TODO[screenshot]: ConnectingSteps`

### Access Scheduled Reports dropdown — `s/article/360043437773.mdx`

[Asana task](https://app.asana.com/0/0/1211443299710978/f) · Feature is already deployed to all customers. Surrounding prose describes the dropdown generically because the option names were not confirmed in the task body.

- [ ] **Scheduled Reports navigation dropdown** — `images/kb/scheduled-reports-navigation-dropdown.png`
  - Describes: The Scheduled Reports screen with the new navigation dropdown open, showing the available views (e.g., subscribed reports, owned reports, send history, settings).
  - Source: needs new screenshot.
  - Marker in article: `{/* TODO[screenshot]: Scheduled Reports`

### Snowflake Account Identifier — `s/article/4402322966807.mdx`

[Asana task](https://app.asana.com/0/0/1209313933155042/f) · Surfaced because both Snowflake and Domo docs leave users hunting for where to find the account identifier. Body text now lists three locations; the screenshot is supplemental.

- [ ] **Snowflake Account Identifier locations** — `images/kb/snowflake-account-identifier.png`
  - Describes: Annotated example showing where the Snowflake account identifier appears (in the Snowsight URL and/or the Admin > Accounts page).
  - Source: needs new screenshot.
  - Marker in article: `{/* TODO[screenshot]: Snowflake Account Identifier`

### Properties for Bar Charts — `s/article/360043429813.mdx`

[Asana task](https://app.asana.com/0/0/1206247708235860/f) · Existing PNGs (dated 2024-09-05) showed separator lines between bars that no longer appear in the current Vertical Bar UI. Replace with fresh captures of the **Hints > Style** option.

- [ ] **Hints Style — Plain** — `images/kb/bar-chart-hints-style-plain.png`
  - Describes: A Vertical Bar chart in Details view with **Style = Plain** so value hints appear as bare text on/above each bar.
  - Source: needs new screenshot.
- [ ] **Hints Style — Tooltip** — `images/kb/bar-chart-hints-style-tooltip.png`
  - Describes: The same Vertical Bar chart in Details view with **Style = Tooltip** so each value hint appears inside a callout box with a pointer to the bar.
  - Source: needs new screenshot.

### AUDIT | Enable SSO with Okta — `s/article/360043438133.mdx`

[Asana task](https://app.asana.com/0/0/1204480786007423/f) · Submitter has a test Okta instance available — coordinate via the task.

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

### Wire an App — `s/article/Wiring-an-App.mdx`

[Asana task](https://app.asana.com/0/0/1204896213998141/f) · New article on wiring custom Apps to DataSets and AppDB Collections. The .docx draft embedded six screenshots (`image.png` through `image6.png`) inside `.asana-cache/1204896213998141/Wiring_an_App.docx`. Extract them into `images/kb/` to use; otherwise replace with fresh captures.

- [ ] **Wiring screen overview** — `images/kb/wiring-app-screen-overview.png`
  - Describes: App Wiring screen with the DataSets and Collections tabs visible in the lower half of the page.
  - Source: `.asana-cache/1204896213998141/Wiring_an_App.docx` (embedded image.png) or fresh capture.
  - Marker in article: `{/* TODO[screenshot]: Wiring screen overview`
- [ ] **DataSet dropdown and alias-to-column mapping** — `images/kb/wiring-app-dataset-alias-mapping.png`
  - Describes: Wiring screen DataSets tab showing the alias dropdown open and the field-to-column mapping rows below it.
  - Source: `.asana-cache/1204896213998141/Wiring_an_App.docx` (embedded image2.png) or fresh capture.
  - Marker in article: `{/* TODO[screenshot]: DataSet dropdown and alias-to-column mapping`
- [ ] **Collections tab with create/existing toggle** — `images/kb/wiring-app-collections-toggle.png`
  - Describes: Wiring screen Collections tab showing the toggle between creating a new Collection and selecting an existing one.
  - Source: `.asana-cache/1204896213998141/Wiring_an_App.docx` (embedded image3.png) or fresh capture.
  - Marker in article: `{/* TODO[screenshot]: Collections tab with create/existing toggle`
- [ ] **Example App displaying wired DataSet** — `images/kb/wiring-app-example-dataset-display.png`
  - Describes: Demo App tab showing the rows of the wired DataSet rendered in a table.
  - Source: `.asana-cache/1204896213998141/Wiring_an_App.docx` (embedded image4.png) or fresh capture.
  - Marker in article: `{/* TODO[screenshot]: Example App displaying wired DataSet`
- [ ] **Example App writing to and reading from a Collection** — `images/kb/wiring-app-example-collection-form.png`
  - Describes: Demo App tab showing the product/SKU form, the Submit button, and the table below the form populated with submitted rows.
  - Source: `.asana-cache/1204896213998141/Wiring_an_App.docx` (embedded image5.png) or fresh capture.
  - Marker in article: `{/* TODO[screenshot]: Example App writing to and reading from a Collection`
- [ ] **Sample manifest.json** — `images/kb/wiring-app-manifest-sample.png`
  - Describes: A manifest.json file open in an editor showing the name, version, collections, and datasetsMapping properties.
  - Source: `.asana-cache/1204896213998141/Wiring_an_App.docx` (embedded image6.png) or fresh capture.
  - Marker in article: `{/* TODO[screenshot]: Sample manifest.json`
