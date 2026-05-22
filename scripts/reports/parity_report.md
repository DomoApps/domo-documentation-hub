# EN/JA Parity Sweep Report

Generated: 2026-05-22 21:57 UTC

- **Items processed:** 48
- **Propagated** (sibling-language edits made): 35
- **Parity OK** (no edit needed; sibling already had equivalent content): 13
- **Flagged for re-review:** 1

## Methodology

Source queue: `scripts/reports/parity_queue.json` (48 items derived from 47 unique Asana tasks where one language was edited but the sibling-language file existed in the repo).

Dispatched in three waves to serialize collisions on shared articles. Each item was handled by a fresh general-purpose sub-agent that:
1. Read both EN and JA files in full.
2. Located the change recorded in the manifest's execution.edits summary.
3. Compared semantic equivalence in the sibling file.
4. Either propagated the missing change or marked parity_ok with reasoning.

## Propagated edits

| Task ID | Edited path | What changed |
|---|---|---|
| 1211368593510747 | `s/article/360043429573.mdx` | PILOT — Limit Rows Note added in Understand Row Limits section |
| 1204889600476211 | `ja/s/article/360043437793.mdx` | PILOT — Administer Publications step 2 updated to Features > Slideshows path |
| 1204480786007423 | `ja/s/article/360043438133.mdx` | Okta procedure rewritten to current Okta Admin Console flow; old <Frame> screenshots replaced with TODO[screenshot] markers |
| 1205972488932235 | `ja/s/article/360043438033.mdx` | Added Warning callout before the attribute table requiring Domo Attribute Key to match IdP attribute name exactly |
| 1211917212465281 | `ja/s/article/360043433813.mdx` | Added 3 field-reference tables and 48 placeholder Notes for missing DomoStats reports — mirrors EN structure |
| 1206490314497795 | `ja/s/article/360043429593.mdx` | Added 'テキストボックスのBeast ModeでHTMLを使用する' section with <br> CONCAT example |
| 1212852269509381 | `ja/s/article/360043429313.mdx` | Replaced old guidance with Warning about Optional group by for 300K+ row DataSets; Brand/334K example preserved |
| 1211620872779260 | `ja/s/article/360043630093.mdx` | Added Note covering profile-level IP allowlisting; literal English error preserved |
| 1211975861580461 | `s/article/360043438053.mdx` | Updated EN Entity ID bullet to instruct entering Domo domain starting with https |
| 1205574771945884 | `ja/s/article/360045120554.mdx` | Added 'サンプルデータのDataSet' subsection in Publications Notes; English error string preserved |
| 1212000885805979 | `s/article/000005827.mdx` | Added EN Note inside JIT provisioning row about identifying JIT events in activity log |
| 1212385872300605 | `ja/s/article/4412849158167.mdx` | Corrected swapped JA grant descriptions: Manage Cloud Accounts = per-DataSet; Override Default Cloud = instance-wide |
| 1206247708235860 | `ja/s/article/360043429813.mdx` | Added 'ヒントの重なりを許可' option row; rewrote Style description with TODO[screenshot] markers |
| 1206603202623147 | `ja/s/article/360042933014.mdx` | Renamed all 7 occurrences of パブリケーション to スライドショーパブリケーション across title, headings, body, UI labels, link text |
| 1211430416073921 | `ja/s/article/360042932334.mdx` | Added Warning + example JSON; rewrote Service Token JSON description to require full JSON object |
| 1210124008187309 | `ja/s/article/360043430513.mdx` | Added Note about state-based Alerts omitting card image; threshold/change alerts include it |
| 1207835736009691 | `ja/s/article/360042933614.mdx` | Added Note in step 6 about using Datastore ID to filter FormDefinition search for multi-form instances |
| 1211566520837757 | `ja/s/article/360042924094.mdx` | Rewrote inheritance Note: same-DataSet drills inherit; different-DataSet drills reference parent BMs; recommended not reusing names |
| 1211048253401450 | `ja/s/article/5428851518999.mdx` | Added Amazon SES (各種リージョン) and SocketLabs to SMTP providers list |
| 1205077867012612 | `ja/s/article/360043038714.mdx` | Added FAQ AccordionGroup with 'Upsert DataSetを壊す原因' and the 4 reindex triggers |
| 1212285013117735 | `ja/s/article/000005544.mdx` | Replaced two JA lines with new ${input} placeholder wording; backticks preserved to prevent MDX interpretation |
| 1205077168730952 | `ja/s/article/4407026671767.mdx` | Added FAQ Q&A about Workbench filename-contains via directory-only path with Warning + Note. JA uses bold-text Q&A (no Accordion in this file) |
| 1212438657897940-5331 | `ja/s/article/000005331.mdx` | Updated Multi-element + Pan bullets; swapped AddingShapetoCanvas Frame for TODO[screenshot]; added 既存のステップを接続する H3 with port-hover/connect content |
| 1212438657897940-5797 | `ja/s/article/000005797.mdx` | Added フロー subsection with 4 step-type flow rules (gateways, automated/AI/manual, start, end) |
| 1208404523858557-Databricks | `ja/s/article/000005289.mdx` | Added missing explanatory prose between 構造的な概要 heading and diagram |
| 1208496280343793 | `ja/s/article/4403367344023.mdx` | Added 4 bullets (Enterprise Apps, Pro-Code Editor apps, Form and Dataset Brick, 追加のAppDBコレクションを使用するBrick) under the existing AppDB bullet |
| 1210990706346408 | `ja/s/article/36004740075.mdx` | JA code already correct semantically but had collapsed line breaks; reformatted block to match EN multi-line layout |
| 1209996598240319 | `ja/s/article/360043428433.mdx` | 100 line replacements: ページ→ダッシュボード in matching contexts; preserved Webページ, image filenames, anchor IDs, Domo Stories product name |
| 1211443299710978 | `ja/s/article/360043437773.mdx` | Added JA paragraph about navigation dropdown + TODO[screenshot] marker |
| 1209311915444243 | `ja/s/article/360042926274.mdx` | Rewrote JA step 3 as sub-bulleted Save / Save and New options; Data Centerのレイアウト link preserved |
| 1211082765646442 | `ja/s/article/360043433813.mdx` | Added cross-ref sentence in DataSet フィールド intro linking to /ja/s/article/000005946 |
| 1204474437572884 | `ja/s/article/360043438033.mdx` | Added JA steps 31-33 (close Attributes & Claims pane, assign users/groups, manual SSO test with KB link). Also reordered closing steps and split Test Connection |
| 1209313933155042 | `ja/s/article/4402322966807.mdx` | Added 3 ways to find Snowflake account identifier + TODO[screenshot] marker; SQL queries and URL templates kept verbatim |
| 1212417320201585 | `s/article/4412849158167.mdx` | Updated DataSet Views row from ✅|✅ to △|△ (See note below); added Note explaining same-cloud-connection DSV requirement |
| 1205607412185788 | `ja/s/article/4403367344023.mdx` | Added JA Accordion 'プロモートされないサポート対象外の項目はありますか？' summarizing all unsupported categories with link to サポートされていない項目 section |

## Parity OK (no edit needed)

| Task ID | Reason |
|---|---|
| 1208165611117613 | JA prereqs lines 57-59 already include consumption-contract exemption |
| 1208404523858557-Dremio | JA Dremio article already has 構造的な概要 section with diagram at lines 15-17 |
| 1209829236183039 | JA tip at lines 330-338 already documents both triggers (DataSetスキーマ + 接続されたDataFlowに関連するアカウントへの変更) |
| 1208580085395212 | JA file has equivalent Snowflake-views-0-rows FAQ at lines 384-388 |
| 1208412038346793 | JA file has equivalent row+column PDP FAQ at lines 653-655 |
| 1209540678831600 | JA Warning callout already states the 3,000-partition limit with the 375-day example |
| 1211529720711393 | FLAG: EN file has been restructured (Manage Users/Manage Groups task-oriented headings, no schema bullet list). EN documents `active=false` deletes user (contradicts JA's new Note that says 'active no |
| 1211869216809105 | EN already had service account + Option 1/2 + Roles and Permissions structure; JA was brought up to match |
| 1208012761881833 | JA file already has Command/Windows + click multi-card selection text at line 795 |
| 1208462516023120 | JA Technical FAQ already has locale-support Q&A at lines 216-218 |
| 1208228611537722 | JA already lists App Studioフォーム as first item under サポートされていない項目 (line 277) |
| 1210830058119327 | All 3 items already in EN: Subscription Owner explanation (lines 56,258), Dashboard/App/DataSet step (line 79), Default Filter View / Beast Mode note (line 420) |
| 1208299381056283 | JA Activity Log row at line 31 already has all 4 details: 30-day initial history, incremental up to 30 days prior, daily/every-30-days cadence, See reference link |

## Items flagged for re-review

- **1211529720711393** — FLAG: EN file has been restructured (Manage Users/Manage Groups task-oriented headings, no schema bullet list). EN documents `active=false` deletes user (contradicts JA's new Note that says 'active not supported'). EN may need re-review against ticket intent; agent judged EN as 'already correct'

## Per-batch result files

- `scripts/reports/parity_results/subbatch_1.json`
- `scripts/reports/parity_results/subbatch_2.json`
- `scripts/reports/parity_results/subbatch_3.json`
- `scripts/reports/parity_results/wave_2.json`
- `scripts/reports/parity_results/wave_3.json`