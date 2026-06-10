# Inline icon image → icon font mapping (FULL)

Mapping of every inline-icon `<img>` reference (images embedded in articles with `style={{display: 'inline'}}`) to its corresponding Domo icon font glyph.

**Goal:** replace each `<img>` with `<i className="icon-{name}" aria-hidden="true" />` (phosphor, current Domo UI) or `<i className="legacy-icon-{name}" aria-hidden="true" />` (legacy Workbench / pre-refresh Domo UI). Pick the font based on the UI surface the article depicts. Both fonts ship the same glyph set. See [Domo-KB-Style-Guide.mdx](../Domo-KB-Style-Guide.mdx) › **Icons**.

**Companion file:** [inline-icon-mapping.json](inline-icon-mapping.json) — machine-readable mapping with every src path, hash, alt text, locale set, and chosen target. A replacement script should consume this.

**Locales column** — derived per entry from the locale folder of each src in `all_srcs`. `/images/kb/ja/...` → `ja`, `/images/kb/de/...` → `de`, `/images/kb/es/...` → `es`, `/images/kb/fr/...` → `fr`, anything else under `/images/kb/` → `en`. An entry may carry multiple locales when the same image content (md5) is referenced from multiple locale folders.

**Maps to column** — usually an icon-font class like `` `icon-pencil` ``. A few entries use `` `X` (text) `` to indicate the inline `<img>` should be replaced with a literal character instead (look for `text_replacement` in the JSON).

**Excluded:**
- Chart-type thumbnails under `/images/charts/` — known not-icons used by chart-catalog articles.
- Release-notes articles (titles starting with `"YYYY Release N"` or containing `"Release Notes"`) — both file types are out of scope for this migration. `refs` counts and `all_srcs` lists only reflect non-release-notes usages.

## Coverage

- **1,076 distinct image contents** identified (deduplicated by md5 hash; charts and release-notes-only refs excluded)
- **2,250 inline-icon references** in non-release-notes articles resolve to images on disk
- (the original scan found 3,815 total inline-icon refs across all articles; ~1,203 broken refs to missing files are tracked separately)

## Confidence tally

| Confidence | Entries | Refs covered |
|---|---:|---:|
| `high` | 647 | 1603 |
| `medium` | 146 | 222 |
| `low` | 1 | 2 |
| `not-icon` | 273 | 412 |
| `needs-review` | 9 | 11 |
| **Total** | **1076** | **2250** |

- `high` / `medium` / `low` — mapped to a font glyph (or literal-character replacement) at that level of certainty
- `not-icon` — not actually an icon (full UI screenshot, table, labeled button caught by `style={{display: 'inline'}}`, or tile illustration)
- `needs-review` — visually clear but no good font equivalent (status-color dots, brand logos, composite glyphs)

## Glyph consolidation (workhorse mappings)

Many image hashes converge on the same target glyph. Replacing one logical mapping covers many image-path references — these are the highest-leverage targets for a replacement script:

| Target | Total refs | Distinct image contents |
|---|---:|---:|
| `icon-wrench` | 136 | 31 |
| `icon-trash` | 99 | 37 |
| `icon-pencil` | 94 | 23 |
| `icon-dots-vertical` | 85 | 30 |
| `icon-arrow-square-out` | 77 | 6 |
| `icon-plus` | 60 | 26 |
| `icon-gear` | 49 | 23 |
| `icon-dots-horizontal` | 42 | 17 |
| `icon-check-square-fill text-green-600` | 36 | 2 |
| `icon-x` | 29 | 19 |
| `legacy-icon-wrench` | 27 | 8 |
| `icon-megaphone` | 26 | 1 |
| `icon-cube-outlined` | 22 | 7 |
| `icon-funnel` | 22 | 11 |
| `icon-lines-horizontal` | 22 | 10 |
| `icon-eye` | 19 | 11 |
| `icon-chevron-down` | 18 | 13 |
| `icon-plus-circle` | 18 | 4 |
| `icon-search` | 18 | 6 |
| `icon-chevron-up` | 17 | 4 |
| `legacy-icon-badge-layout-small` | 17 | 1 |
| `icon-bell` | 15 | 3 |
| `icon-duplicate` | 15 | 12 |
| `icon-arrows-diagonal-in` | 14 | 11 |
| `icon-database` | 14 | 8 |
| `icon-funnel-plus` | 14 | 4 |
| `legacy-icon-database` | 14 | 4 |
| `icon-arrow-box` | 13 | 2 |
| `icon-pencil-box` | 13 | 7 |
| `icon-play` | 13 | 5 |
| `icon-play-circle-outline` | 13 | 4 |
| `icon-upload` | 13 | 7 |
| `legacy-icon-save` | 13 | 5 |
| `icon-key` | 12 | 7 |
| `icon-arrow-curved-right` | 11 | 3 |
| `icon-chart-bar-vertical` | 11 | 7 |
| `icon-chat-bubbles` | 11 | 2 |
| `icon-list-bulleted` | 11 | 6 |
| `icon-person-plus` | 11 | 5 |
| `icon-question-circle` | 11 | 6 |
| `icon-reset` | 11 | 2 |
| `icon-x text-red-600` | 11 | 1 |
| `icon-caret-down` | 9 | 4 |
| `icon-save` | 9 | 5 |
| `legacy-icon-arrow-up` | 9 | 2 |
| `icon-chart-line` | 8 | 3 |
| `icon-check` | 8 | 5 |
| `icon-chevron-right` | 8 | 4 |
| `icon-expand` | 8 | 5 |
| `icon-plus-circle-fill` | 8 | 4 |

_(274 distinct target glyphs total)_

## Top 100 entries (detailed)

| Rank | Refs | Locales | Srcs | Glyph | Maps to | Confidence | Notes |
|---:|---:|---|---|---|---|---|---|
| 1 | 48 | de, en, es, ja | [ja/0EMVq000005scBu.jpg](../images/kb/ja/0EMVq000005scBu.jpg)<br />[ja/0EMVq000003k2I2.jpg](../images/kb/ja/0EMVq000003k2I2.jpg)<br />[de/0EMVq000005scBu.jpg](../images/kb/de/0EMVq000005scBu.jpg)<br />[es/0EMVq000005scBu.jpg](../images/kb/es/0EMVq000005scBu.jpg)<br />[0EMVq000008gSmT.jpg](../images/kb/0EMVq000008gSmT.jpg)<br />[ja/0EMVq0000043wLJ.jpg](../images/kb/ja/0EMVq0000043wLJ.jpg)<br />[ja/0EMVq000002cL77.jpg](../images/kb/ja/0EMVq000002cL77.jpg)<br />[0EMVq000008fzSj.jpg](../images/kb/0EMVq000008fzSj.jpg)<br />[0EMVq000002cL77.jpg](../images/kb/0EMVq000002cL77.jpg)<br />[ja/0EMVq000005Ww7d.jpg](../images/kb/ja/0EMVq000005Ww7d.jpg)<br />[ja/0EMVq000001ctMH.jpg](../images/kb/ja/0EMVq000001ctMH.jpg)<br />[ja/0EMVq000003FPAr.jpg](../images/kb/ja/0EMVq000003FPAr.jpg)<br />[ja/0EMVq000006wbdF.jpg](../images/kb/ja/0EMVq000006wbdF.jpg)<br />[ja/0EMVq0000026ObB.jpg](../images/kb/ja/0EMVq0000026ObB.jpg)<br />[ja/0EMVq000000KYTl.jpg](../images/kb/ja/0EMVq000000KYTl.jpg)<br />[ja/0EMVq000000KZ85.jpg](../images/kb/ja/0EMVq000000KZ85.jpg)<br />[ja/0EMVq000003fnKn.jpg](../images/kb/ja/0EMVq000003fnKn.jpg)<br />[ja/0EMVq000000KZo1.jpg](../images/kb/ja/0EMVq000000KZo1.jpg)<br />[ja/0EMVq000000oyqb.jpg](../images/kb/ja/0EMVq000000oyqb.jpg)<br />[ja/0EMVq000002YFjR.jpg](../images/kb/ja/0EMVq000002YFjR.jpg)<br />[ja/0EMVq000000KtRl.jpg](../images/kb/ja/0EMVq000000KtRl.jpg)<br />[ja/0EMVq0000023r6f.jpg](../images/kb/ja/0EMVq0000023r6f.jpg)<br />[0EMVq000008gOvl.jpg](../images/kb/0EMVq000008gOvl.jpg)<br />[0EMVq000003FPAr.jpg](../images/kb/0EMVq000003FPAr.jpg)<br />[0EMVq000000Buen.jpg](../images/kb/0EMVq000000Buen.jpg)<br />[0EMVq000000KYTl.jpg](../images/kb/0EMVq000000KYTl.jpg)<br />[0EMVq000000KZ85.jpg](../images/kb/0EMVq000000KZ85.jpg)<br />[0EMVq000000KZo1.jpg](../images/kb/0EMVq000000KZo1.jpg)<br />[0EMVq000005kLBR.jpg](../images/kb/0EMVq000005kLBR.jpg)<br />[0EMVq000005kPJt.jpg](../images/kb/0EMVq000005kPJt.jpg)<br />[0EMVq00000DTPJi.jpg](../images/kb/0EMVq00000DTPJi.jpg)<br />[0EMVq00000DT9wU.jpg](../images/kb/0EMVq00000DT9wU.jpg)<br />[0EMVq000000T2OD.jpg](../images/kb/0EMVq000000T2OD.jpg)<br />[0EMVq000005Ys4j.jpg](../images/kb/0EMVq000005Ys4j.jpg) | external link square+arrow-out | `icon-arrow-square-out` | high |  |
| 2 | 26 | de, en, es, ja | [ka0Vq0000000qbJ-00N5w00000Ri7BU-0EMVq000000Mcmc.jpg](../images/kb/ka0Vq0000000qbJ-00N5w00000Ri7BU-0EMVq000000Mcmc.jpg)<br />[es/0EMVq000000Mcmc.jpg](../images/kb/es/0EMVq000000Mcmc.jpg)<br />[ja/0EMVq000000Mcmc.jpg](../images/kb/ja/0EMVq000000Mcmc.jpg)<br />[de/0EMVq000000Mcmc.jpg](../images/kb/de/0EMVq000000Mcmc.jpg) |  | `icon-megaphone` | high |  |
| 3 | 25 | en, ja | [ja/0EMVq000000MdYz.jpg](../images/kb/ja/0EMVq000000MdYz.jpg)<br />[ja/0EMVq000000Mddp.jpg](../images/kb/ja/0EMVq000000Mddp.jpg)<br />[ja/0EMVq000000Mdh3.jpg](../images/kb/ja/0EMVq000000Mdh3.jpg)<br />[ja/0EMVq000000MdkH.jpg](../images/kb/ja/0EMVq000000MdkH.jpg)<br />[0EMVq000003qUpu.jpg](../images/kb/0EMVq000003qUpu.jpg)<br />[ja/0EMVq000004oUwf.jpg](../images/kb/ja/0EMVq000004oUwf.jpg)<br />[0EMVq000004oUwf.jpg](../images/kb/0EMVq000004oUwf.jpg)<br />[0EMVq000003tbbW.jpg](../images/kb/0EMVq000003tbbW.jpg) | external link variant | `icon-arrow-square-out` | high |  |
| 4 | 22 | en, ja | [ja/0EMVq000001luvq.jpg](../images/kb/ja/0EMVq000001luvq.jpg)<br />[ja/0EMVq000000J38g.jpg](../images/kb/ja/0EMVq000000J38g.jpg)<br />[0EMVq000001luvq.jpg](../images/kb/0EMVq000001luvq.jpg)<br />[ja/0EMVq000000JC0f.jpg](../images/kb/ja/0EMVq000000JC0f.jpg)<br />[ka0Vq0000007KoP-00N5w00000Ri7BU-0EMVq000000SmMf.jpg](../images/kb/ka0Vq0000007KoP-00N5w00000Ri7BU-0EMVq000000SmMf.jpg)<br />[ja/0EMVq000000SmMf.jpg](../images/kb/ja/0EMVq000000SmMf.jpg)<br />[ja/0EMVq000001Fbcz.jpg](../images/kb/ja/0EMVq000001Fbcz.jpg)<br />[ja/0EMVq000001pd6n.jpg](../images/kb/ja/0EMVq000001pd6n.jpg)<br />[ja/0EMVq000000J7CH.jpg](../images/kb/ja/0EMVq000000J7CH.jpg)<br />[ja/0EMVq000000J5VT.jpg](../images/kb/ja/0EMVq000000J5VT.jpg)<br />[ja/0EMVq000000x3I1.jpg](../images/kb/ja/0EMVq000000x3I1.jpg)<br />[ja/0EMVq000000yxmn.jpg](../images/kb/ja/0EMVq000000yxmn.jpg)<br />[ja/0EMVq000000yy2v.jpg](../images/kb/ja/0EMVq000000yy2v.jpg)<br />[0EMVq000001Fbcz.jpg](../images/kb/0EMVq000001Fbcz.jpg) | trash can | `icon-trash` | high |  |
| 5 | 20 | de, en, es | [ka05w00000123Qn-00N5w00000Ri7BU-0EM5w000005vOAb.png](../images/kb/ka05w00000123Qn-00N5w00000Ri7BU-0EM5w000005vOAb.png)<br />[de/0EM5w000005wJXq.png](../images/kb/de/0EM5w000005wJXq.png)<br />[de/0EM5w000005wJa8.png](../images/kb/de/0EM5w000005wJa8.png)<br />[es/0EM5w000005wKOG.png](../images/kb/es/0EM5w000005wKOG.png) |  | `icon-wrench` | high |  |
| 6 | 20 | en, ja | [ja/0EMVq000004rbAP.jpg](../images/kb/ja/0EMVq000004rbAP.jpg)<br />[0EMVq000004rbAP.jpg](../images/kb/0EMVq000004rbAP.jpg)<br />[ja/0EMVq0000096wli.jpg](../images/kb/ja/0EMVq0000096wli.jpg)<br />[0EMVq0000096wli.jpg](../images/kb/0EMVq0000096wli.jpg) |  | `icon-check-square-fill text-green-600` | high |  |
| 7 | 19 | en, ja | [ja/0EMVq000000Ht3J.jpg](../images/kb/ja/0EMVq000000Ht3J.jpg)<br />[ja/0EMVq000000yxYH.jpg](../images/kb/ja/0EMVq000000yxYH.jpg)<br />[ja/0EMVq000001ltN4.jpg](../images/kb/ja/0EMVq000001ltN4.jpg)<br />[ja/0EMVq000000J6bB.jpg](../images/kb/ja/0EMVq000000J6bB.jpg)<br />[ja/0EMVq000000HvrV.jpg](../images/kb/ja/0EMVq000000HvrV.jpg)<br />[0EMVq000001ltN4.jpg](../images/kb/0EMVq000001ltN4.jpg)<br />[ja/0EMVq000003nMor.jpg](../images/kb/ja/0EMVq000003nMor.jpg)<br />[ja/0EMVq000000J8mf.jpg](../images/kb/ja/0EMVq000000J8mf.jpg)<br />[ja/0EMVq0000026Iih.jpg](../images/kb/ja/0EMVq0000026Iih.jpg)<br />[ja/0EMVq000001gwIN.jpg](../images/kb/ja/0EMVq000001gwIN.jpg) |  | `icon-pencil` | high |  |
| 8 | 17 | en, ja | [ja/0EMVq0000060Lqd.jpg](../images/kb/ja/0EMVq0000060Lqd.jpg)<br />[0EMVq0000060Lqd.jpg](../images/kb/0EMVq0000060Lqd.jpg)<br />[ja/0EMVq000008R1xt.jpg](../images/kb/ja/0EMVq000008R1xt.jpg)<br />[ja/0EMVq0000060G2y.jpg](../images/kb/ja/0EMVq0000060G2y.jpg)<br />[ja/0EMVq0000060jJS.jpg](../images/kb/ja/0EMVq0000060jJS.jpg)<br />[0EMVq0000060G2y.jpg](../images/kb/0EMVq0000060G2y.jpg)<br />[0EMVq000008iUU1.jpg](../images/kb/0EMVq000008iUU1.jpg)<br />[0EMVq0000060jJS.jpg](../images/kb/0EMVq0000060jJS.jpg) | pencil outlined | `icon-pencil` | high |  |
| 9 | 17 | de, es | [de/0EM5w000005wJZO.png](../images/kb/de/0EM5w000005wJZO.png)<br />[es/0EM5w000005wKNa.png](../images/kb/es/0EM5w000005wKNa.png)<br />[es/0EM5w000005wKLC.png](../images/kb/es/0EM5w000005wKLC.png) |  | `legacy-icon-badge-layout-small` | high |  |
| 10 | 16 | en | [ka05w00000123sv-00N5w00000Ri7BU-0EM5w000005vPOn.png](../images/kb/ka05w00000123sv-00N5w00000Ri7BU-0EM5w000005vPOn.png) | plus | `icon-plus` | high |  |
| 11 | 16 | en | [Integration-Account-Table-Indicator-Dot.png](../images/kb/Integration-Account-Table-Indicator-Dot.png) |  | `icon-check-square-fill text-green-600` | high |  |
| 12 | 15 | en | [0EM5w000005vXkS.png](../images/kb/0EM5w000005vXkS.png) |  | `icon-wrench` | high |  |
| 13 | 14 | en, ja | [ja/0EM5w000005wLHe.png](../images/kb/ja/0EM5w000005wLHe.png)<br />[ja/0EM5w000005vNik.png](../images/kb/ja/0EM5w000005vNik.png)<br />[ka0Vq000000FmNh-00N5w00000Ri7BU-0EM5w000005vNjp-1.png](../images/kb/ka0Vq000000FmNh-00N5w00000Ri7BU-0EM5w000005vNjp-1.png)<br />[ka0Vq000000FmNh-00N5w00000Ri7BU-0EM5w000005vNjp-2.png](../images/kb/ka0Vq000000FmNh-00N5w00000Ri7BU-0EM5w000005vNjp-2.png)<br />[ka0Vq000000FmNh-00N5w00000Ri7BU-0EM5w000005vNjp-3.png](../images/kb/ka0Vq000000FmNh-00N5w00000Ri7BU-0EM5w000005vNjp-3.png)<br />[ka0Vq000000FmNh-00N5w00000Ri7BU-0EM5w000005vNjp-4.png](../images/kb/ka0Vq000000FmNh-00N5w00000Ri7BU-0EM5w000005vNjp-4.png) | pencil light gray small | `icon-pencil` | high |  |
| 14 | 14 | ja | [ja/0EM5w000005vXkS.png](../images/kb/ja/0EM5w000005vXkS.png) |  | `icon-wrench` | high |  |
| 15 | 13 | en | [ka05w00000123rQ-00N5w00000Ri7BU-0EM5w000005vPKu.png](../images/kb/ka05w00000123rQ-00N5w00000Ri7BU-0EM5w000005vPKu.png) | chevron up | `icon-chevron-up` | high |  |
| 16 | 12 | en, ja | [ja/0EMVq000006vBxm.jpg](../images/kb/ja/0EMVq000006vBxm.jpg)<br />[0EMVq000006vBxm.jpg](../images/kb/0EMVq000006vBxm.jpg) | three vertical dots | `icon-dots-vertical` | high |  |
| 17 | 11 | en, ja | [ka0Vq0000001Fg9-00N5w00000Ri7BU-0EM5w000005wybX.jpg](../images/kb/ka0Vq0000001Fg9-00N5w00000Ri7BU-0EM5w000005wybX.jpg)<br />[ja/0EMVq000004rbIT.jpg](../images/kb/ja/0EMVq000004rbIT.jpg)<br />[0EMVq000004rbIT.jpg](../images/kb/0EMVq000004rbIT.jpg) |  | `icon-x text-red-600` | high |  |
| 18 | 11 | ja | [ja/0EM5w000005vOEr.png](../images/kb/ja/0EM5w000005vOEr.png) |  | — | not-icon |  |
| 19 | 11 | en | [ka05w00000124mU-00N5w00000Ri7BU-0EM5w000005vOGc.png](../images/kb/ka05w00000124mU-00N5w00000Ri7BU-0EM5w000005vOGc.png) | labeled SMART TEXT button | — | not-icon | Full button screenshot, not a glyph |
| 20 | 10 | en, ja | [0EM5w000005vPW6.png](../images/kb/0EM5w000005vPW6.png)<br />[ja/0EM5w000005vPW6.png](../images/kb/ja/0EM5w000005vPW6.png) |  | `icon-wrench` | high |  |
| 21 | 10 | en, ja | [ka0Vq0000000oMb-00N5w00000Ri7BU-0EMVq000000i27l.jpg](../images/kb/ka0Vq0000000oMb-00N5w00000Ri7BU-0EMVq000000i27l.jpg)<br />[ja/0EMVq000000Ht4v.jpg](../images/kb/ja/0EMVq000000Ht4v.jpg)<br />[ja/0EMVq000000i27l.jpg](../images/kb/ja/0EMVq000000i27l.jpg) |  | `icon-reset` | high |  |
| 22 | 10 | en, ja | [ka05w00000124S5-00N5w00000Ri7BU-0EM5w000005vOAW.png](../images/kb/ka05w00000124S5-00N5w00000Ri7BU-0EM5w000005vOAW.png)<br />[0EM5w000005vOVd.png](../images/kb/0EM5w000005vOVd.png)<br />[ja/0EM5w000005wLFb.png](../images/kb/ja/0EM5w000005wLFb.png) |  | `icon-arrow-box` | high |  |
| 23 | 9 | de, en, es | [es/0EM5w000005wKNq.png](../images/kb/es/0EM5w000005wKNq.png)<br />[ka05w00000123au-00N5w00000Ri7BU-0EM5w000005vOcV.png](../images/kb/ka05w00000123au-00N5w00000Ri7BU-0EM5w000005vOcV.png)<br />[de/0EM5w000005wJaC.png](../images/kb/de/0EM5w000005wJaC.png)<br />[0EM5w000005vObp.png](../images/kb/0EM5w000005vObp.png) | bell (alert) | `icon-bell` | high |  |
| 24 | 9 | en, ja | [0EMVq000008QaWI.jpg](../images/kb/0EMVq000008QaWI.jpg)<br />[ja/0EMVq000008QaWI.jpg](../images/kb/ja/0EMVq000008QaWI.jpg) |  | `icon-wrench` | high |  |
| 26 | 9 | en, ja | [ja/0EM5w000005vOXY.png](../images/kb/ja/0EM5w000005vOXY.png)<br />[0EM5w000005vOXY.png](../images/kb/0EM5w000005vOXY.png)<br />[ka0Vq0000000wgj-00N5w00000Ri7BU-0EM5w000005vOXj.png](../images/kb/ka0Vq0000000wgj-00N5w00000Ri7BU-0EM5w000005vOXj.png) |  | `icon-chat-bubbles` | high |  |
| 27 | 8 | en, ja | [ka0Vq0000004ZAT-00N5w00000Ri7BU-0EM5w000006u434.png](../images/kb/ka0Vq0000004ZAT-00N5w00000Ri7BU-0EM5w000006u434.png)<br />[ja/0EM5w000006u434.png](../images/kb/ja/0EM5w000006u434.png)<br />[ja/0EM5w000006u43o.png](../images/kb/ja/0EM5w000006u43o.png)<br />[ja/0EM5w000006u43p.png](../images/kb/ja/0EM5w000006u43p.png)<br />[ja/0EM5w000006u43r.png](../images/kb/ja/0EM5w000006u43r.png) | funnel+plus (filter add) | `icon-funnel-plus` | high |  |
| 28 | 8 | en, ja | [ja/0EMVq0000058BEk.jpg](../images/kb/ja/0EMVq0000058BEk.jpg)<br />[0EMVq0000058BEk.jpg](../images/kb/0EMVq0000058BEk.jpg) |  | `icon-wrench` | high |  |
| 29 | 8 | en, ja | [ka05w00000123tG-00N5w00000Ri7BU-0EM5w000005vPPk.png](../images/kb/ka05w00000123tG-00N5w00000Ri7BU-0EM5w000005vPPk.png)<br />[ja/0EM5w000005wLED.png](../images/kb/ja/0EM5w000005wLED.png)<br />[0EM5w000005vPMo.png](../images/kb/0EM5w000005vPMo.png) |  | `icon-play-circle-outline` | high |  |
| 30 | 8 | en | [ka0Vq000000C3gT-00N5w00000Ri7BU-0EMVq000000J38g.jpg](../images/kb/ka0Vq000000C3gT-00N5w00000Ri7BU-0EMVq000000J38g.jpg)<br />[ka0Vq000000C3gT-00N5w00000Ri7BU-0EMVq000000JC0f.jpg](../images/kb/ka0Vq000000C3gT-00N5w00000Ri7BU-0EMVq000000JC0f.jpg)<br />[ka0Vq000000C3gT-00N5w00000Ri7BU-0EMVq000001pd6n.jpg](../images/kb/ka0Vq000000C3gT-00N5w00000Ri7BU-0EMVq000001pd6n.jpg) | trash can | `icon-trash` | high |  |
| 31 | 8 | en, ja | [ka05w00000123tU-00N5w00000Ri7BU-0EM5w000005vPQj.png](../images/kb/ka05w00000123tU-00N5w00000Ri7BU-0EM5w000005vPQj.png)<br />[ja/0EM5w000005wLEP.png](../images/kb/ja/0EM5w000005wLEP.png) |  | `icon-lines-horizontal` | high |  |
| 32 | 8 | en, ja | [ka05w0000012Aam-00N5w00000Ri7BU-0EM5w000006vrB8.jpg](../images/kb/ka05w0000012Aam-00N5w00000Ri7BU-0EM5w000006vrB8.jpg)<br />[ja/0EM5w000006uVxG.jpg](../images/kb/ja/0EM5w000006uVxG.jpg)<br />[ja/0EMVq000001FbbN.jpg](../images/kb/ja/0EMVq000001FbbN.jpg)<br />[0EM5w000006uVxG.jpg](../images/kb/0EM5w000006uVxG.jpg)<br />[0EMVq000001FbbN.jpg](../images/kb/0EMVq000001FbbN.jpg) |  | `icon-wrench` | high |  |
| 33 | 8 | en, ja | [ka05w00000123RF-00N5w00000Ri7BU-0EM5w000005vOCU.png](../images/kb/ka05w00000123RF-00N5w00000Ri7BU-0EM5w000005vOCU.png)<br />[ja/0EM5w000005vXl9.png](../images/kb/ja/0EM5w000005vXl9.png)<br />[0EM5w000005vXl9.png](../images/kb/0EM5w000005vXl9.png) |  | `icon-wrench` | high |  |
| 34 | 7 | ja | [ja/0EM5w000005vOVX.png](../images/kb/ja/0EM5w000005vOVX.png) | KPI cards screenshot | — | not-icon | False positive |
| 35 | 7 | en | [ka05w00000126DW-00N5w00000Ri7BU-0EM5w000005vZ3P.png](../images/kb/ka05w00000126DW-00N5w00000Ri7BU-0EM5w000005vZ3P.png) | trash can | `icon-trash` | high |  |
| 36 | 7 | en, ja | [ka0Vq000000BCNd-00N5w00000Ri7BU-0EMVq000000uSeO.jpg](../images/kb/ka0Vq000000BCNd-00N5w00000Ri7BU-0EMVq000000uSeO.jpg)<br />[ja/0EMVq000004SfHF.jpg](../images/kb/ja/0EMVq000004SfHF.jpg)<br />[ja/0EMVq000000uSeO.jpg](../images/kb/ja/0EMVq000000uSeO.jpg)<br />[ja/0EMVq000000p1LR.jpg](../images/kb/ja/0EMVq000000p1LR.jpg)<br />[ja/0EMVq000004NTF7.jpg](../images/kb/ja/0EMVq000004NTF7.jpg)<br />[0EMVq000004NTF7.jpg](../images/kb/0EMVq000004NTF7.jpg) |  | `icon-plus-circle` | high |  |
| 37 | 7 | en, ja | [ka0Vq000000FnBh-00N5w00000Ri7BU-0EM5w000005vPMz.png](../images/kb/ka0Vq000000FnBh-00N5w00000Ri7BU-0EM5w000005vPMz.png)<br />[0EM5w000005vPMz.png](../images/kb/0EM5w000005vPMz.png)<br />[ja/0EM5w000005wLDx.png](../images/kb/ja/0EM5w000005wLDx.png) | trash | `icon-trash` | high |  |
| 38 | 7 | en, ja | [ka05w00000125lS-00N5w00000Ri7BU-0EM5w000005wtzY.jpg](../images/kb/ka05w00000125lS-00N5w00000Ri7BU-0EM5w000005wtzY.jpg)<br />[ja/0EM5w000006vsvl.jpg](../images/kb/ja/0EM5w000006vsvl.jpg)<br />[0EM5w000006vwtj.jpg](../images/kb/0EM5w000006vwtj.jpg)<br />[0EM5w000006vsvl.jpg](../images/kb/0EM5w000006vsvl.jpg) | pencil (edit) | `icon-pencil` | high | alt 'edit.png' |
| 39 | 7 | en, ja | [0EM5w000005vOXO.png](../images/kb/0EM5w000005vOXO.png)<br />[ja/0EM5w000005vOXO.png](../images/kb/ja/0EM5w000005vOXO.png) | thumbs up | `icon-thumbs-up` | high |  |
| 40 | 7 | en | [0EM5w000005vOVX.png](../images/kb/0EM5w000005vOVX.png) | full screenshot of Selecting Constraint dataflow tile and Select Columns config | — | not-icon | Not an icon - full UI screenshot |
| 41 | 7 | en, ja | [ka05w00000123tU-00N5w00000Ri7BU-0EM5w000005vPQ5.png](../images/kb/ka05w00000123tU-00N5w00000Ri7BU-0EM5w000005vPQ5.png)<br />[ja/0EM5w000005wLER.png](../images/kb/ja/0EM5w000005wLER.png) |  | `legacy-icon-key` | high |  |
| 42 | 7 | en, ja | [ka0Vq00000013Ld-00N5w00000Ri7BU-0EMVq000001Q2f7.jpg](../images/kb/ka0Vq00000013Ld-00N5w00000Ri7BU-0EMVq000001Q2f7.jpg)<br />[ja/0EMVq000002Hc4Z.jpg](../images/kb/ja/0EMVq000002Hc4Z.jpg)<br />[ja/0EMVq0000026oDt.jpg](../images/kb/ja/0EMVq0000026oDt.jpg)<br />[ja/0EMVq000002BZEF.jpg](../images/kb/ja/0EMVq000002BZEF.jpg)<br />[0EMVq000002Hc4Z.jpg](../images/kb/0EMVq000002Hc4Z.jpg)<br />[0EMVq0000026oDt.jpg](../images/kb/0EMVq0000026oDt.jpg) | three vertical dots | `icon-dots-vertical` | high |  |
| 43 | 7 | en, ja | [ja/0EM5w000005wLoC.png](../images/kb/ja/0EM5w000005wLoC.png)<br />[ja/0EM5w000005vO5u.png](../images/kb/ja/0EM5w000005vO5u.png)<br />[ja/0EM5w000005wLoB.png](../images/kb/ja/0EM5w000005wLoB.png)<br />[ja/0EM5w000005vO5c.png](../images/kb/ja/0EM5w000005vO5c.png)<br />[ja/0EM5w000005vO5q.png](../images/kb/ja/0EM5w000005vO5q.png)<br />[0EM5w000005vO5c.png](../images/kb/0EM5w000005vO5c.png)<br />[0EM5w000005vO5q.png](../images/kb/0EM5w000005vO5q.png) | cloud-region table screenshot | — | not-icon | False positive — inline-styled table |
| 44 | 7 | en, ja | [ka05w00000124SK-00N5w00000Ri7BU-0EM5w000005vOsq.png](../images/kb/ka05w00000124SK-00N5w00000Ri7BU-0EM5w000005vOsq.png)<br />[ja/0EM5w000005vPVn.png](../images/kb/ja/0EM5w000005vPVn.png)<br />[0EM5w000005vPVn.png](../images/kb/0EM5w000005vPVn.png) | white gear on blue background (Data Center bulk gear) | `icon-gear` | high | alt 'data_center_bulk_gear_icon.png' |
| 45 | 6 | en, ja | [ka05w00000129wP-00N5w00000Ri7BU-0EM5w000006vSrA.jpg](../images/kb/ka05w00000129wP-00N5w00000Ri7BU-0EM5w000006vSrA.jpg)<br />[ja/0EM5w000006uRFK.jpg](../images/kb/ja/0EM5w000006uRFK.jpg)<br />[ja/0EM5w000006vr1X.jpg](../images/kb/ja/0EM5w000006vr1X.jpg)<br />[ja/0EM5w000006wB3E.jpg](../images/kb/ja/0EM5w000006wB3E.jpg)<br />[0EM5w000006vr1X.jpg](../images/kb/0EM5w000006vr1X.jpg) | trash can | `icon-trash` | high | alt 'delete 1.png' |
| 46 | 6 | en, ja | [ka0Vq000000BCNd-00N5w00000Ri7BU-0EMVq000000uR3y.jpg](../images/kb/ka0Vq000000BCNd-00N5w00000Ri7BU-0EMVq000000uR3y.jpg)<br />[ja/0EMVq000000uR3y.jpg](../images/kb/ja/0EMVq000000uR3y.jpg)<br />[0EMVq000000uR3y.jpg](../images/kb/0EMVq000000uR3y.jpg) |  | `icon-cube-outlined` | high |  |
| 47 | 6 | ja | [ja/img/rte_broken_image.png](../images/kb/ja/img/rte_broken_image.png) | RTE 'Image Not Available' notice | — | not-icon | Broken/missing-image placeholder; not a real icon |
| 48 | 6 | en | [ka05w00000123tU-00N5w00000Ri7BU-0EM5w000005vPQz.png](../images/kb/ka05w00000123tU-00N5w00000Ri7BU-0EM5w000005vPQz.png)<br />[0EM5w000005vPN0.png](../images/kb/0EM5w000005vPN0.png) | curved return/revert arrow | `legacy-icon-arrow-curved-back` | medium | alt 'wb5_revert_icon.png' - legacy Workbench revert glyph |
| 49 | 6 | en, ja | [ja/0EM5w000005wLDf.png](../images/kb/ja/0EM5w000005wLDf.png)<br />[ja/0EM5w000005vPNz.png](../images/kb/ja/0EM5w000005vPNz.png)<br />[0EM5w000005vPMw.png](../images/kb/0EM5w000005vPMw.png) | database/jobs cylinder (Workbench jobs) | `legacy-icon-database` | medium | alt 'wb5_jobs_icon.png' - legacy Workbench jobs icon (stacked cylinders) |
| 50 | 6 | en, ja | [ja/0EM5w000005vOXZ.png](../images/kb/ja/0EM5w000005vOXZ.png)<br />[0EM5w000005vOXZ.png](../images/kb/0EM5w000005vOXZ.png)<br />[ka05w00000124CW-00N5w00000Ri7BU-0EM5w000005vOXZ.png](../images/kb/ka05w00000124CW-00N5w00000Ri7BU-0EM5w000005vOXZ.png) | three horizontal dots | `icon-dots-horizontal` | high |  |
| 51 | 6 | en, ja | [ja/0EM5w000005vXk8.png](../images/kb/ja/0EM5w000005vXk8.png)<br />[0EM5w000005vXk8.png](../images/kb/0EM5w000005vXk8.png) | three horizontal dots (Options menu) | `icon-dots-horizontal` | high | alt 'Options_Menu.png' |
| 52 | 6 | en, ja | [ja/0EM5w000005vNm2.png](../images/kb/ja/0EM5w000005vNm2.png)<br />[ka05w00000129vy-00N5w00000Ri7BU-0EM5w000005vNm2.png](../images/kb/ka05w00000129vy-00N5w00000Ri7BU-0EM5w000005vNm2.png) | three vertical dots inside a small white box (kebab button) | `icon-dots-vertical` | high |  |
| 53 | 6 | en, ja | [ja/0EM5w000005vOXD.png](../images/kb/ja/0EM5w000005vOXD.png)<br />[0EM5w000005vOXD.png](../images/kb/0EM5w000005vOXD.png) | square with pencil (Buzz new message) | `icon-pencil-box` | high | alt 'buzz_highnoon_new_message.png' - compose/new-message glyph |
| 54 | 6 | en, ja | [ja/0EMVq000008RDsb.jpg](../images/kb/ja/0EMVq000008RDsb.jpg)<br />[0EMVq000008RDsb.jpg](../images/kb/0EMVq000008RDsb.jpg)<br />[ja/0EMVq000008RCrh.jpg](../images/kb/ja/0EMVq000008RCrh.jpg)<br />[0EMVq000008RCrh.jpg](../images/kb/0EMVq000008RCrh.jpg) |  | `icon-wrench` | high |  |
| 55 | 6 | en, ja | [ja/0EMVq000000IKxx.jpg](../images/kb/ja/0EMVq000000IKxx.jpg)<br />[ja/0EMVq000000J4G1.jpg](../images/kb/ja/0EMVq000000J4G1.jpg)<br />[ja/0EMVq00000232FR.jpg](../images/kb/ja/0EMVq00000232FR.jpg)<br />[ka0Vq0000001e53-00N5w00000Ri7BU-0EMVq000000HkeL.jpg](../images/kb/ka0Vq0000001e53-00N5w00000Ri7BU-0EMVq000000HkeL.jpg)<br />[0EMVq00000232FR.jpg](../images/kb/0EMVq00000232FR.jpg) | gear (settings) | `icon-gear` | high | alt 'settings.png' |
| 56 | 6 | de | [de/0EM5w000005wJXj.png](../images/kb/de/0EM5w000005wJXj.png) | play triangle in a square button | `icon-play` | medium | alt 'page_gear_icon.png' but glyph is a play button |
| 57 | 6 | en | [ka05w00000123aO-00N5w00000Ri7BU-0EM5w000005vOaD.png](../images/kb/ka05w00000123aO-00N5w00000Ri7BU-0EM5w000005vOaD.png) | three vertical dots (kebab menu) | `icon-dots-vertical` | high |  |
| 58 | 6 | en, ja | [ja/0EM5w000005vOCM.png](../images/kb/ja/0EM5w000005vOCM.png)<br />[0EM5w000005vOCM.png](../images/kb/0EM5w000005vOCM.png) | three vertical dots (kebab menu) | `icon-dots-vertical` | high | alt 'group_management_triple_dots.png' |
| 59 | 6 | en | [0EM5w000005vYzC.png](../images/kb/0EM5w000005vYzC.png) | clipboard (copy embed code) | `icon-clipboard-copy` | high | alt 'domo_embed_copy.png' |
| 60 | 6 | en, ja | [ka0Vq000000A23l-00N5w00000Ri7BU-0EMVq000005xN0v.jpg](../images/kb/ka0Vq000000A23l-00N5w00000Ri7BU-0EMVq000005xN0v.jpg)<br />[ja/0EMVq000005Nj9d.jpg](../images/kb/ja/0EMVq000005Nj9d.jpg)<br />[ja/0EMVq000005GWnR.jpg](../images/kb/ja/0EMVq000005GWnR.jpg)<br />[0EMVq000005Nj9d.jpg](../images/kb/0EMVq000005Nj9d.jpg) |  | `icon-cube-outlined` | high |  |
| 61 | 6 | en | [0EM5w000005vPNz.png](../images/kb/0EM5w000005vPNz.png)<br />[ka0Vq000000FnBh-00N5w00000Ri7BU-0EM5w000005vPNZ.png](../images/kb/ka0Vq000000FnBh-00N5w00000Ri7BU-0EM5w000005vPNZ.png) | up arrow (Workbench jobs) | `legacy-icon-arrow-up` | medium | alt 'wb5_jobs_icon.png' but glyph is a plain up-arrow - likely an upload/jobs marker; legacy Workbench context |
| 62 | 5 | en, ja | [ka0Vq000000BENp-00N5w00000Ri7BU-0EMVq000004mhMv.jpg](../images/kb/ka0Vq000000BENp-00N5w00000Ri7BU-0EMVq000004mhMv.jpg)<br />[ja/0EMVq000004mjVB.jpg](../images/kb/ja/0EMVq000004mjVB.jpg)<br />[ja/0EMVq000004mula.jpg](../images/kb/ja/0EMVq000004mula.jpg)<br />[0EMVq000004mula.jpg](../images/kb/0EMVq000004mula.jpg) |  | `icon-cube-outlined` | high |  |
| 63 | 5 | en, ja | [ja/0EMVq000001ZIeD.jpg](../images/kb/ja/0EMVq000001ZIeD.jpg)<br />[ja/0EMVq000000J7gw.jpg](../images/kb/ja/0EMVq000000J7gw.jpg)<br />[ja/0EMVq000000J8oH.jpg](../images/kb/ja/0EMVq000000J8oH.jpg)<br />[0EMVq000001ZIeD.jpg](../images/kb/0EMVq000001ZIeD.jpg)<br />[ka0Vq0000001Fg9-00N5w00000Ri7BU-0EMVq000001b4Lq.jpg](../images/kb/ka0Vq0000001Fg9-00N5w00000Ri7BU-0EMVq000001b4Lq.jpg) | X (close) | `icon-x` | high | alt 'close.jpg' |
| 64 | 5 | ja | [ja/0EM5w000005vOEn.png](../images/kb/ja/0EM5w000005vOEn.png) | full screenshot of 'Apply logic to this text' modal with Prefix/Suffix fields and Remove/Cancel/Apply buttons | — | not-icon | Not an icon - full UI screenshot |
| 65 | 5 | en | [ka05w00000123c6-00N5w00000Ri7BU-0EM5w000005vOeu.png](../images/kb/ka05w00000123c6-00N5w00000Ri7BU-0EM5w000005vOeu.png) | curved forward/share arrow pointing right | `icon-arrow-curved-right` | high |  |
| 66 | 5 | en, ja | [ja/0EMVq000001mnU7.jpg](../images/kb/ja/0EMVq000001mnU7.jpg)<br />[ka0Vq0000004oHZ-00N5w00000Ri7BU-0EMVq000001mnU7.jpg](../images/kb/ka0Vq0000004oHZ-00N5w00000Ri7BU-0EMVq000001mnU7.jpg) |  | `icon-right-rail-fill` | high |  |
| 67 | 5 | en | [ka05w00000124mU-00N5w00000Ri7BU-0EM5w000005vOGX.png](../images/kb/ka05w00000124mU-00N5w00000Ri7BU-0EM5w000005vOGX.png) | three vertical dots (kebab menu) | `icon-dots-vertical` | high |  |
| 68 | 5 | en, ja | [ka0Vq000000BCKP-00N5w00000Ri7BU-0EM5w000005vNtv.png](../images/kb/ka0Vq000000BCKP-00N5w00000Ri7BU-0EM5w000005vNtv.png)<br />[ja/0EM5w000005vNtv.png](../images/kb/ja/0EM5w000005vNtv.png) | plus inside circle (add new) | `icon-plus-circle` | high | alt 'add_new_cloud.png' |
| 69 | 5 | en | [ka05w00000123aG-00N5w00000Ri7BU-0EM5w000005vOZk.png](../images/kb/ka05w00000123aG-00N5w00000Ri7BU-0EM5w000005vOZk.png) | pencil (edit) | `icon-pencil` | high |  |
| 70 | 5 | en | [ka05w00000123c6-00N5w00000Ri7BU-0EM5w000005vOet.png](../images/kb/ka05w00000123c6-00N5w00000Ri7BU-0EM5w000005vOet.png) |  | `icon-arrow-curved-right` | high |  |
| 71 | 5 | en, ja | [ja/0EM5w000005vOCw.png](../images/kb/ja/0EM5w000005vOCw.png)<br />[0EM5w000005vOCw.png](../images/kb/0EM5w000005vOCw.png) | small downward caret/chevron | `icon-caret-down` | high | alt 'group_management_snowman_nose.png' - small caret indicator |
| 72 | 5 | en | [ka05w00000123kQ-00N5w00000Ri7BU-0EM5w000005vOyu.png](../images/kb/ka05w00000123kQ-00N5w00000Ri7BU-0EM5w000005vOyu.png) |  | `icon-analyzer` | high |  |
| 73 | 5 | en, ja | [ka05w00000128SJ-00N5w00000Ri7BU-0EM5w000005vOcQ.png](../images/kb/ka05w00000128SJ-00N5w00000Ri7BU-0EM5w000005vOcQ.png)<br />[ja/0EM5w000005vOc8.png](../images/kb/ja/0EM5w000005vOc8.png)<br />[0EM5w000005vOc8.png](../images/kb/0EM5w000005vOc8.png) | bell (notifications/alerts) | `icon-bell` | high |  |
| 74 | 5 | en | [ka0Vq0000005UQT-00N5w00000Ri7BU-0EM5w000005vNtu.png](../images/kb/ka0Vq0000005UQT-00N5w00000Ri7BU-0EM5w000005vNtu.png) | wrench | `icon-wrench` | high |  |
| 75 | 5 | en, ja | [ja/0EM5w000005vXkP.png](../images/kb/ja/0EM5w000005vXkP.png)<br />[0EM5w000005vXkP.png](../images/kb/0EM5w000005vXkP.png)<br />[ka0Vq00000051WX-00N5w00000Ri7BU-0EM5w000005vXkP.png](../images/kb/ka0Vq00000051WX-00N5w00000Ri7BU-0EM5w000005vXkP.png) | three horizontal dots inside a tile/box | `icon-dots-horizontal` | high |  |
| 76 | 5 | en, ja | [ka05w00000126DW-00N5w00000Ri7BU-0EM5w000005vZ3K.png](../images/kb/ka05w00000126DW-00N5w00000Ri7BU-0EM5w000005vZ3K.png)<br />[ja/0EM5w000005vOVV.png](../images/kb/ja/0EM5w000005vOVV.png)<br />[ja/0EM5w000005wLFd.png](../images/kb/ja/0EM5w000005wLFd.png)<br />[0EM5w000005vObn.png](../images/kb/0EM5w000005vObn.png) |  | `icon-wrench` | high |  |
| 77 | 5 | ja | [ja/0EM5w000005vNjp.png](../images/kb/ja/0EM5w000005vNjp.png) | full screenshot of a Product Container table column listing pack/box sizes with red circles around Jumbo Box rows | — | not-icon | Not an icon - full UI screenshot |
| 78 | 4 | en | [ka05w00000123tG-00N5w00000Ri7BU-0EM5w000005vPPb.png](../images/kb/ka05w00000123tG-00N5w00000Ri7BU-0EM5w000005vPPb.png) |  | `legacy-icon-pencil-fill` | high |  |
| 79 | 4 | en, ja | [ja/0EM5w000005vPW5.png](../images/kb/ja/0EM5w000005vPW5.png)<br />[0EM5w000005vPW5.png](../images/kb/0EM5w000005vPW5.png) | tag with arrow (bulk tag) | `icon-tag` | high | alt: data_center_bulk_tag_icon.png |
| 80 | 4 | en, ja | [ja/0EM5w000006vr00.jpg](../images/kb/ja/0EM5w000006vr00.jpg)<br />[0EM5w000006vr00.jpg](../images/kb/0EM5w000006vr00.jpg) | eye outline (unhide) | `icon-eye` | high | alt: unhide.jpg |
| 81 | 4 | en | [ka05w0000012Aef-00N5w00000Ri7BU-0EM5w000005wEqf.jpg](../images/kb/ka05w0000012Aef-00N5w00000Ri7BU-0EM5w000005wEqf.jpg) | flag/bookmark outline shape | `icon-flag-outline` | medium | Appears to be a flag or bookmark icon |
| 82 | 4 | en | [ka05w00000128TW-00N5w00000Ri7BU-0EM5w000006ufdc.jpg](../images/kb/ka05w00000128TW-00N5w00000Ri7BU-0EM5w000006ufdc.jpg) |  | `legacy-icon-save` | high |  |
| 83 | 4 | en, ja | [ja/0EM5w000005vODJ.png](../images/kb/ja/0EM5w000005vODJ.png)<br />[0EM5w000005vODJ.png](../images/kb/0EM5w000005vODJ.png) | Share Card or Page dialog screenshot | — | not-icon | False positive - 'Share Card or Page' dialog screenshot (card search results), not an icon; remove from articles, do not convert |
| 84 | 4 | en, ja | [ja/0EMVq000005KDFx.jpg](../images/kb/ja/0EMVq000005KDFx.jpg)<br />[ja/0EMVq000005KDW5.jpg](../images/kb/ja/0EMVq000005KDW5.jpg)<br />[0EMVq000005KDFx.jpg](../images/kb/0EMVq000005KDFx.jpg)<br />[0EMVq000005KDW5.jpg](../images/kb/0EMVq000005KDW5.jpg) | wrench (legacy card edit) | `legacy-icon-wrench` | high | Legacy card-edit wrench icon |
| 85 | 4 | en, ja | [ka05w00000128SJ-00N5w00000Ri7BU-0EM5w000005vOch.png](../images/kb/ka05w00000128SJ-00N5w00000Ri7BU-0EM5w000005vOch.png)<br />[ja/0EM5w000005vObp.png](../images/kb/ja/0EM5w000005vObp.png) | small zigzag line chart (alert icon) | `icon-chart-line` | medium | alt: alert_icon.png - appears to be a small line chart used as an alert indicator |
| 86 | 4 | en | [ka0Vq00000010qn-00N5w00000Ri7BU-0EM5w000005vOFT.png](../images/kb/ka0Vq00000010qn-00N5w00000Ri7BU-0EM5w000005vOFT.png) | closed padlock | `legacy-icon-lock-closed` | high | Lock icon |
| 87 | 4 | ja | [ja/0EMVq000000wNdl.jpg](../images/kb/ja/0EMVq000000wNdl.jpg)<br />[ja/0EMVq0000011js9.jpg](../images/kb/ja/0EMVq0000011js9.jpg)<br />[ja/0EMVq000000ws9h.jpg](../images/kb/ja/0EMVq000000ws9h.jpg)<br />[ja/0EMVq000000ywxB.jpg](../images/kb/ja/0EMVq000000ywxB.jpg) | person with plus (add groups/people) | `icon-person-plus` | high | alt: add groups and people.jpg |
| 88 | 4 | en, ja | [ja/0EMVq000000IJDt.jpg](../images/kb/ja/0EMVq000000IJDt.jpg)<br />[ka0Vq0000002n4f-00N5w00000Ri7BU-0EMVq000000IJDt.jpg](../images/kb/ka0Vq0000002n4f-00N5w00000Ri7BU-0EMVq000000IJDt.jpg) | plus sign | `icon-plus` | high |  |
| 89 | 4 | en | [use-writeback-connectors.png](../images/kb/use-writeback-connectors.png) | tile graphic with check-square icon and caption | — | not-icon | Tile graphic with text label, not a single UI icon |
| 90 | 4 | en, ja | [ja/0EM5w000005vOXe.png](../images/kb/ja/0EM5w000005vOXe.png)<br />[0EM5w000005vOXe.png](../images/kb/0EM5w000005vOXe.png) |  | `icon-paperclip` | high |  |
| 91 | 4 | en, ja | [ka05w00000123tU-00N5w00000Ri7BU-0EM5w000005vPQG.png](../images/kb/ka05w00000123tU-00N5w00000Ri7BU-0EM5w000005vPQG.png)<br />[ja/0EM5w000005wLEV.png](../images/kb/ja/0EM5w000005wLEV.png)<br />[0EM5w000005vPNS.png](../images/kb/0EM5w000005vPNS.png) | dark help/question circle icon | `legacy-icon-question-circle` | high | Workbench 5 help icon (alt: wb5_help_icon.png) |
| 92 | 4 | en, ja | [ja/0EMVq000005s5np.jpg](../images/kb/ja/0EMVq000005s5np.jpg)<br />[ja/0EMVq000005sEeD.jpg](../images/kb/ja/0EMVq000005sEeD.jpg)<br />[0EMVq000005s5np.jpg](../images/kb/0EMVq000005s5np.jpg)<br />[0EMVq000005sEeD.jpg](../images/kb/0EMVq000005sEeD.jpg) | pencil (edit) | `icon-pencil` | high |  |
| 93 | 4 | en, ja | [ja/0EMVq0000037r13.jpg](../images/kb/ja/0EMVq0000037r13.jpg)<br />[0EMVq0000037r13.jpg](../images/kb/0EMVq0000037r13.jpg) | three vertical dots (kebab menu) | `icon-dots-vertical` | high |  |
| 94 | 4 | en | [ka05w00000123q1-00N5w00000Ri7BU-0EM5w000005vPJH.png](../images/kb/ka05w00000123q1-00N5w00000Ri7BU-0EM5w000005vPJH.png) | pie chart | `icon-chart-pie` | high |  |
| 95 | 4 | en | [ka05w00000123l5-00N5w00000Ri7BU-0EM5w000005vP0C.png](../images/kb/ka05w00000123l5-00N5w00000Ri7BU-0EM5w000005vP0C.png) | database stack with chevron dropdown | `icon-database` | high | Database picker with dropdown |
| 96 | 4 | de, es | [de/0EM5w000005wJQt.png](../images/kb/de/0EM5w000005wJQt.png)<br />[es/0EM5w000005wKF3.png](../images/kb/es/0EM5w000005wKF3.png) | person silhouette (pdp users icon) | `icon-person` | high | alt: pdp_users_icon.png |
| 97 | 4 | en, ja | [ja/0EM5w000005vOD9.png](../images/kb/ja/0EM5w000005vOD9.png)<br />[0EM5w000005vOD9.png](../images/kb/0EM5w000005vOD9.png) | share/upload box with up arrow | `icon-arrow-box` | high | alt: group_management_share.png - share icon as upload-style box-with-arrow |
| 98 | 4 | en, ja | [ja/0EM5w000006vqzC.jpg](../images/kb/ja/0EM5w000006vqzC.jpg)<br />[0EM5w000006vqzC.jpg](../images/kb/0EM5w000006vqzC.jpg) | eye with pupil (preview) | `icon-eye-observed` | high | alt: preview eye.jpg |
| 99 | 4 | en, ja | [ja/0EM5w000005vOG6.png](../images/kb/ja/0EM5w000005vOG6.png)<br />[0EM5w000005vOG6.png](../images/kb/0EM5w000005vOG6.png) | right-pointing chevron (show subpages) | `icon-chevron-right` | high | alt: show_subpages.png |
| 100 | 4 | en | [ka05w00000124TS-00N5w00000Ri7BU-0EM5w000005vPJJ.png](../images/kb/ka05w00000124TS-00N5w00000Ri7BU-0EM5w000005vPJJ.png) | funnel with plus (add filter) | `icon-funnel-plus` | medium | Funnel with a small plus icon |

_(For ranks 101–1,077, see `inline-icon-mapping.json`.)_

## Needs review (9 entries)

These were visually clear but had no good font equivalent or required a judgment call. Worth a human pass:

| Rank | Refs | Locales | Srcs | Glyph | Notes |
|---:|---:|---|---|---|---|
| 312 | 2 | en | [ka0Vq000000FnBh-00N5w00000Ri7BU-0EM5w000005vPNY.png](../images/kb/ka0Vq000000FnBh-00N5w00000Ri7BU-0EM5w000005vPNY.png) | search with badge | Magnifying glass over document with red notification badge - composite UI, no exact font match |
| 388 | 2 | en | [ka0Vq00000055bl-00N5w00000Ri7BU-0EM5w000005wbeB.jpg](../images/kb/ka0Vq00000055bl-00N5w00000Ri7BU-0EM5w000005wbeB.jpg) | database with plus - add database/job | Workbench composite icon - database with plus sign; closest single glyph would be legacy-icon-database-plus |
| 836 | 1 | en | [ka05w00000123aO-00N5w00000Ri7BU-0EM5w000005vOaL.png](../images/kb/ka05w00000123aO-00N5w00000Ri7BU-0EM5w000005vOaL.png) | toggle switch on with checkmark | UI control (toggle switch), no direct icon font equivalent |
| 857 | 1 | en | [ka05w00000123Yu-00N5w00000Ri7BU-0EM5w000005vOY3.png](../images/kb/ka05w00000123Yu-00N5w00000Ri7BU-0EM5w000005vOY3.png) | two icons (gear+star?) | Composite of two small icons |
| 906 | 1 | en | [ka05w00000123vE-00N5w00000Ri7BU-0EM5w000005vPVj.png](../images/kb/ka05w00000123vE-00N5w00000Ri7BU-0EM5w000005vPVj.png) | parallel gateway + arrow combination | Composite workflow element (gateway plus right-arrow); not a single glyph |
| 941 | 1 | ja | [ja/0EM5w000006uKYY.jpg](../images/kb/ja/0EM5w000006uKYY.jpg) | unclear black square thumbnail | Image appears to be a tiny black square - glyph not visible/recognizable |
| 970 | 1 | en | [ka05w00000123Zh-00N5w00000Ri7BU-0EM5w000005vOYe.png](../images/kb/ka05w00000123Zh-00N5w00000Ri7BU-0EM5w000005vOYe.png) | globe + gear combo | Two icons in one image: globe and gear |
| 1033 | 1 | en | [ka05w00000123vE-00N5w00000Ri7BU-0EM5w000005vPWc.png](../images/kb/ka05w00000123vE-00N5w00000Ri7BU-0EM5w000005vPWc.png) | rotate arrows + arrow combination | Composite workflow element (rotate plus right-arrow); not a single glyph |
| 1058 | 1 | en | [ka05w00000124T8-00N5w00000Ri7BU-0EM5w000005vNgJ.png](../images/kb/ka05w00000124T8-00N5w00000Ri7BU-0EM5w000005vNgJ.png) | Mastercard-style logo | Logo/brand mark, not in icon font |

## Not icons (272 entries, 408 refs)

Caught by the scanner because they use `style={{display: 'inline'}}` but aren't single-glyph icons. Most are:
- **Full UI screenshots** that were inlined at small dimensions (Workbench dialogs, App Studio panels, OAuth screens, etc.)
- **Labeled buttons** captured as a full image rather than a glyph
- **Tile illustrations** (SVG marketing/landing-page graphics)
- **Status-indicator dots** or other tiny pixel patterns
- **6 oversized screenshots** (>2000px) flagged separately because they exceed the multimodal image-size limit

These don't need replacement — but the scanner pattern should be tightened to exclude images with reasonable width/height attributes. See top 25 by ref count:

| Rank | Refs | Locales | Srcs | Notes |
|---:|---:|---|---|---|
| 18 | 11 | ja | [ja/0EM5w000005vOEr.png](../images/kb/ja/0EM5w000005vOEr.png) |  |
| 19 | 11 | en | [ka05w00000124mU-00N5w00000Ri7BU-0EM5w000005vOGc.png](../images/kb/ka05w00000124mU-00N5w00000Ri7BU-0EM5w000005vOGc.png) | Full button screenshot, not a glyph |
| 34 | 7 | ja | [ja/0EM5w000005vOVX.png](../images/kb/ja/0EM5w000005vOVX.png) | False positive |
| 40 | 7 | en | [0EM5w000005vOVX.png](../images/kb/0EM5w000005vOVX.png) | Not an icon - full UI screenshot |
| 43 | 7 | en, ja | [ja/0EM5w000005wLoC.png](../images/kb/ja/0EM5w000005wLoC.png)<br />[ja/0EM5w000005vO5u.png](../images/kb/ja/0EM5w000005vO5u.png)<br />[ja/0EM5w000005wLoB.png](../images/kb/ja/0EM5w000005wLoB.png)<br />[ja/0EM5w000005vO5c.png](../images/kb/ja/0EM5w000005vO5c.png)<br />[ja/0EM5w000005vO5q.png](../images/kb/ja/0EM5w000005vO5q.png)<br />[0EM5w000005vO5c.png](../images/kb/0EM5w000005vO5c.png)<br />[0EM5w000005vO5q.png](../images/kb/0EM5w000005vO5q.png) | False positive — inline-styled table |
| 47 | 6 | ja | [ja/img/rte_broken_image.png](../images/kb/ja/img/rte_broken_image.png) | Broken/missing-image placeholder; not a real icon |
| 64 | 5 | ja | [ja/0EM5w000005vOEn.png](../images/kb/ja/0EM5w000005vOEn.png) | Not an icon - full UI screenshot |
| 77 | 5 | ja | [ja/0EM5w000005vNjp.png](../images/kb/ja/0EM5w000005vNjp.png) | Not an icon - full UI screenshot |
| 89 | 4 | en | [use-writeback-connectors.png](../images/kb/use-writeback-connectors.png) | Tile graphic with text label, not a single UI icon |
| 104 | 4 | en | [0EM5w000005vPNu.png](../images/kb/0EM5w000005vPNu.png) | alt: wb5_more_icon.png but actually a full screenshot of Plugin Editor properties panel |
| 115 | 4 | en, ja | [ka0Vq0000004ZAT-00N5w00000Ri7BU-0EM5w000006u2sZ.png](../images/kb/ka0Vq0000004ZAT-00N5w00000Ri7BU-0EM5w000006u2sZ.png)<br />[ja/0EM5w000006u2sZ.png](../images/kb/ja/0EM5w000006u2sZ.png)<br />[ja/0EM5w000006u43q.png](../images/kb/ja/0EM5w000006u43q.png) |  |
| 117 | 4 | en, ja | [ja/0EMVq000002lgib.jpg](../images/kb/ja/0EMVq000002lgib.jpg)<br />[0EMVq000002lgib.jpg](../images/kb/0EMVq000002lgib.jpg) |  |
| 118 | 4 | en, ja | [ja/0EM5w000005vO8h.png](../images/kb/ja/0EM5w000005vO8h.png)<br />[ja/0EM5w000005vO8p.png](../images/kb/ja/0EM5w000005vO8p.png)<br />[0EM5w000005vO8h.png](../images/kb/0EM5w000005vO8h.png)<br />[0EM5w000005vO8p.png](../images/kb/0EM5w000005vO8p.png) | Full screenshot of a data table, not an icon |
| 138 | 3 | en, ja | [ja/0EM5w000005wLE8.png](../images/kb/ja/0EM5w000005wLE8.png)<br />[ja/0EM5w000005vPMU.png](../images/kb/ja/0EM5w000005vPMU.png)<br />[0EM5w000005vPMu.png](../images/kb/0EM5w000005vPMu.png) | Full Workbench window screenshot - mistakenly tagged with WB5 icon alts |
| 145 | 3 | en | [ka0Vq000000FV1t-00N5w00000Ri7BU-0EM5w000005vO5s.png](../images/kb/ka0Vq000000FV1t-00N5w00000Ri7BU-0EM5w000005vO5s.png)<br />[0EM5w000005vO6B.png](../images/kb/0EM5w000005vO6B.png) | Full panel screenshot with form fields, not a UI icon |
| 157 | 3 | en | [ka0Vq0000000Rcv-00N5w00000Ri7BU-0EM5w000006vME1.jpg](../images/kb/ka0Vq0000000Rcv-00N5w00000Ri7BU-0EM5w000006vME1.jpg) | Third-party logo banner, not a Domo UI icon |
| 177 | 2 | en | [0EM5w000005vOVv.png](../images/kb/0EM5w000005vOVv.png) | Full ETL canvas screenshot; alt text 'page_gear_icon.png' is misleading — the image is a screenshot, not a glyph |
| 179 | 2 | en, ja | [ja/0EM5w000005vODI.png](../images/kb/ja/0EM5w000005vODI.png)<br />[0EM5w000005vODI.png](../images/kb/0EM5w000005vODI.png) | Alt 'group_management_new_members.png' - full member selection table screenshot |
| 191 | 2 | en, ja | [ja/0EM5w000005wLGw.png](../images/kb/ja/0EM5w000005wLGw.png)<br />[0EM5w000005vPU8.png](../images/kb/0EM5w000005vPU8.png) | Workbench 'Select DataSet' picker dialog screenshot - not an icon. |
| 199 | 2 | en, ja | [ja/0EM5w000005vOVu.png](../images/kb/ja/0EM5w000005vOVu.png)<br />[0EM5w000005vOVu.png](../images/kb/0EM5w000005vOVu.png) | Full UI screenshot of a Magic ETL/Dataflow region, not an icon |
| 210 | 2 | ja | [ja/0EM5w000005wLEE.png](../images/kb/ja/0EM5w000005wLEE.png) | Alt name wb5_revert_icon.png is misleading — actual image is a full Workbench dialog screenshot, not an icon |
| 216 | 2 | ja | [ja/0EM5w000005vObm.png](../images/kb/ja/0EM5w000005vObm.png) | Full Discover topics screenshot with annotations - not an icon |
| 230 | 2 | ja | [ja/0EM5w000005vOUq.png](../images/kb/ja/0EM5w000005vOUq.png) | Full Domo side panel screenshot, not an icon. |
| 231 | 2 | en, ja | [ja/0EM5w000005vODD.png](../images/kb/ja/0EM5w000005vODD.png)<br />[0EM5w000005vODD.png](../images/kb/0EM5w000005vODD.png) | Alt 'group_management_new_group_button.png' - full screenshot with New Group button highlighted |
| 232 | 2 | en, ja | [ja/0EM5w000005vOto.png](../images/kb/ja/0EM5w000005vOto.png)<br />[0EM5w000005vOto.png](../images/kb/0EM5w000005vOto.png) | Full screenshot of ETL append rows configuration, not a single icon. |

_(Full list in `inline-icon-mapping.json` — filter by `confidence == "not-icon"`.)_

## Next steps

1. **Spot-check the `medium`/`needs-review` entries.** ~148 medium-confidence mappings and 9 needs-review entries cover 246 references combined. A 30-minute eyeball pass would catch most miscalls.
2. **Audit the 1,203 missing-file references.** These are broken image refs in the source, separate from the mapping problem.
3. **Tighten the scanner** to filter out images with width/height > ~40px before generating future inline-icon audits. ~272 of the 1,077 entries here are false positives (full screenshots caught because they used `style={{display: 'inline'}}`).
4. **Build a replacement script** that consumes `inline-icon-mapping.json` and walks `.mdx` files, proposing per-article diffs for review. Should:
   - Skip release-notes articles (titles containing "Release Notes" or matching `YYYY Release N | Month`)
   - Look up each `<img src="...">` by src path → find the matching entry by hash
   - Only auto-replace `high` confidence entries; flag `medium`/`low` for human review
   - For entries with `text_replacement`, substitute the literal character instead of an icon-font tag
   - Skip `not-icon` and `needs-review` entries entirely
   - Preserve any surrounding `<p>` or `<Frame>` wrappers
