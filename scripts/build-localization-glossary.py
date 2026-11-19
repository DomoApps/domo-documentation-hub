#!/usr/bin/env python3
"""Build the deterministic localization glossaries.

Generates one CSV per target language under ``localization/glossary/`` from three
sources, in descending order of authority:

1. **style-guide**  — the per-language term tables, callout labels, and section
   headers hand-encoded from ``localization/Localization-Style-Guide.mdx`` (which
   was itself reverse-engineered from approved translator work). Authoritative.
2. **branded-terms** — the PMM branded-terms glossary
   (``localization/sources/Domo_BrandedTerms_PMMupdates_092425 1.csv``). Supplies
   the universal "never translate" (keep-in-English) rules for all languages.
3. **mined-tm** (Japanese only) — high-agreement term pairs mined from the approved
   entries of the XTM translation memory
   (``localization/sources/JA-XTM-TM.csv``, gitignored). Only augments Japanese
   with Domo/technical terms not already covered by the style guide.

Output schema (identical for every language):

    english_term,translation,keep_in_english,context,notes,source,last_updated

Re-running is safe: rows whose ``source`` begins with ``retrospective:`` or
``manual`` are preserved verbatim (these are the learning-loop / hand-curated
rows), while ``style-guide`` / ``branded-terms`` / ``mined-tm`` rows are
regenerated.

Usage:
    python3 scripts/build-localization-glossary.py            # regenerate all CSVs
    python3 scripts/build-localization-glossary.py --report   # also print mining report
"""

import argparse
import csv
import collections
import datetime
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDED_CSV = os.path.join(REPO_ROOT, "localization", "sources",
                           "Domo_BrandedTerms_PMMupdates_092425 1.csv")
JA_TM_CSV = os.path.join(REPO_ROOT, "localization", "sources", "JA-XTM-TM.csv")
OUT_DIR = os.path.join(REPO_ROOT, "localization", "glossary")

LANGS = ["es", "fr", "de", "ja"]
TODAY = datetime.date.today().isoformat()
FIELDS = ["english_term", "translation", "keep_in_english",
          "context", "notes", "source", "last_updated"]

PRESERVE_SOURCE_PREFIXES = ("retrospective:", "manual")

# --------------------------------------------------------------------------- #
# 1. Universal keep-in-English terms (apply to ALL languages).
#    Sourced from Localization-Style-Guide.mdx "What is NEVER translated".
#    An entry may carry an ``except`` set of language codes that DO translate it
#    (only Magic ETL, expanded in Spanish).
# --------------------------------------------------------------------------- #
UNIVERSAL_KEEP_EN = [
    # Domo brand and product names
    ("Domo", ""), ("DataSet", "Singular/plural identical in EN"),
    ("DataSets", ""), ("DataFlow", ""), ("DataFlows", ""), ("DataFusion", ""),
    ("Beast Mode", ""), ("Analyzer", ""), ("Buzz", ""), ("Cloud Amplifier", ""),
    ("Jupyter Notebook", ""), ("Jupyter Workspace", ""), ("Embed", ""),
    ("Appstore", ""), ("Workbench", ""), ("DomoStats", ""), ("Domo Bricks", ""),
    ("DDX Bricks", ""), ("AppDB", ""), ("Domo AI", ""), ("Domo Documents", ""),
    ("Domo Schema", ""), ("Flex Table", ""),
    # Technical acronyms and standards
    ("ETL", ""), ("OAuth", ""), ("SQL", ""), ("API", ""), ("SAML", ""),
    ("SSO", ""), ("MFA", ""), ("2FA", ""), ("JSON", ""), ("XML", ""),
    ("CSV", ""), ("YAML", ""), ("MDX", ""), ("SDK", ""), ("CLI", ""),
    ("REST", ""), ("HTTP", ""), ("HTTPS", ""), ("PDP", "Personalized Data Permissions"),
    ("M2M", "Machine to Machine"),
    # Third-party product and brand names
    ("Snowflake", ""), ("BigQuery", ""), ("Azure", ""), ("AWS", ""),
    ("Google", ""), ("Microsoft", ""), ("Databricks", ""), ("Salesforce", ""),
    ("MySQL", ""), ("PostgreSQL", ""), ("Slack", ""), ("GitHub", ""),
]
# Magic ETL is kept in EN everywhere EXCEPT Spanish (which expands it).
MAGIC_ETL = ("Magic ETL", "Kept in English (see Spanish glossary for the ES expansion)", {"es"})

# --------------------------------------------------------------------------- #
# 2. Per-language translation glossary, encoded from the style guide.
#    Each row: (english_term, translation, context, notes)
# --------------------------------------------------------------------------- #
GLOSSARY = {
    "es": [
        ("Magic ETL", "Magic - Extracción, transformación y carga", "", "Spanish uniquely expands Magic ETL on first mention; 'Magic ETL' acceptable on later mentions in the same section"),
        ("Workflows", "Flujos de trabajo", "", "Always translated"),
        ("workflow", "flujo de trabajo", "generic", "Lowercase when not a product reference"),
        ("Connector", "Conector", "", ""),
        ("Connectors", "Conectores", "", ""),
        ("Cloud Integration", "Integración en la nube", "", "Always translated"),
        ("Dashboard", "Tablero", "", "Translated in most contexts; 'dashboard' acceptable as a modifier"),
        ("Alert", "Alerta", "", ""),
        ("Alerts", "Alertas", "", ""),
        ("Chart", "Gráfico", "", ""),
        ("Table", "Tabla", "UI", "UI element"),
        ("Database table", "tabla de base de datos", "database", "Lowercase"),
        ("Filter", "Filtro", "", ""),
        ("Group", "Grupo", "", ""),
        ("Card", "Tarjeta", "", ""),
        ("Page", "Página", "", ""),
        ("Query", "Consulta", "", ""),
        ("Section", "Sección", "", ""),
        ("Report", "Informe", "", ""),
        ("Role", "Función", "", "'Función' preferred; 'Rol' accepted"),
        ("Permission", "Permiso", "", ""),
        ("Grant", "Concesión", "", "Context-dependent: 'Concesión' or 'Permiso'"),
        ("Setting", "Configuración", "", "Or 'Ajuste'"),
        ("Update", "Actualización", "", "As noun; 'actualizar' as verb"),
        ("Enhancement", "Mejora", "", ""),
        ("Feature", "Función", "", "'Función' preferred in release notes; 'Característica' accepted"),
        ("User", "Usuario", "", ""),
        ("Admin", "Administrador", "", ""),
        ("Instance", "Instancia", "", ""),
        ("Account", "Cuenta", "", ""),
        ("Dataset tile", "Icono de DataSet", "Magic ETL", "tile = icono in ETL context; DataSet stays EN"),
        ("Workspace", "Espacio de trabajo", "", ""),
        ("Template", "Plantilla", "", ""),
        ("Widget", "Widget", "", "Kept in English"),
        ("Read-only", "Solo lectura", "", ""),
        ("Pushdown", "En pushdown", "", "Technical term kept with Spanish article"),
    ],
    "fr": [
        ("Workflows", "Flux de travail", "", "Lowercase in body ('flux de travail'); capitalize in headings"),
        ("workflow", "flux de travail", "generic", ""),
        ("Connector", "connecteur", "", "Lowercase"),
        ("Connectors", "connecteurs", "", "Lowercase"),
        ("Cloud Integration", "Intégration dans le cloud", "", "'dans le cloud' not 'en nuage'"),
        ("Dashboard", "tableau de bord", "", "Always translated"),
        ("Alert", "alerte", "", "Lowercase"),
        ("Alerts", "alertes", "", "Lowercase"),
        ("Chart", "graphique", "", ""),
        ("Table", "tableau", "UI", "UI element; 'tableau' also = spreadsheet"),
        ("Database table", "table", "database", "Keep 'table' for database context"),
        ("Filter", "filtre", "", ""),
        ("Group", "groupe", "", ""),
        ("Card", "carte", "", ""),
        ("Page", "page", "", ""),
        ("Query", "requête", "", ""),
        ("Section", "section", "", ""),
        ("Report", "rapport", "", ""),
        ("Role", "rôle", "", ""),
        ("Permission", "autorisation", "", ""),
        ("Permissions", "autorisations", "", ""),
        ("Grant", "droit", "", "Context-dependent: 'droit' or 'autorisation'"),
        ("Setting", "paramètre", "", ""),
        ("Update", "mise à jour", "", "As noun; 'mettre à jour' as verb"),
        ("Enhancement", "optimisation", "", "'amélioration' also acceptable; 'optimisations' in RN headers"),
        ("Feature", "fonctionnalité", "", ""),
        ("User", "utilisateur", "", ""),
        ("Admin", "administrateur", "", ""),
        ("Instance", "instance", "", ""),
        ("Account", "compte", "", ""),
        ("App Studio", "Studio d'applications", "", "Translated in French"),
        ("Jupyter Notebook", "bloc-notes Jupyter", "generic", "When translating 'notebook' generically; 'Jupyter Notebook' when it is the tool name"),
        ("Workspace", "espace de travail", "", ""),
        ("Template", "modèle", "", ""),
        ("Widget", "widget", "", "Kept in English"),
        ("Read-only", "lecture seule", "", ""),
        ("Tile", "mosaïque", "Magic ETL", ""),
        ("Pushdown", "pushdown", "", "Technical term kept in English"),
        ("AI Chat", "Conversation par IA", "", ""),
    ],
    "de": [
        ("Workflows", "Arbeitsabläufe", "", "Always translated"),
        ("workflow", "Arbeitsablauf", "generic", "Singular"),
        ("Connector", "Konnektor", "", "German technical term"),
        ("Connectors", "Konnektoren", "", ""),
        ("Cloud Integration", "Cloud-Integration", "", "Hyphenated compound"),
        ("Dashboard", "Dashboard", "", "Kept in English (widely understood in German tech)"),
        ("Alert", "Mitteilung", "", "'Benachrichtigung' also acceptable"),
        ("Alerts", "Mitteilungen", "", ""),
        ("Chart", "Diagramm", "", ""),
        ("Table", "Tabelle", "UI", ""),
        ("Database table", "Tabelle", "database", "Same word; context clarifies"),
        ("Filter", "Filter", "", "Kept in English"),
        ("Group", "Gruppe", "", ""),
        ("Card", "Karte", "", ""),
        ("Page", "Seite", "", ""),
        ("Query", "Abfrage", "", ""),
        ("Section", "Abschnitt", "", ""),
        ("Report", "Bericht", "", ""),
        ("Role", "Rolle", "", ""),
        ("Permission", "Berechtigung", "", ""),
        ("Permissions", "Berechtigungen", "", ""),
        ("Grant", "Zugriffsrecht", "", "Context-dependent: 'Zugriffsrecht' or 'Berechtigung'"),
        ("Setting", "Einstellung", "", ""),
        ("Update", "Aktualisierung", "", "As noun; 'aktualisieren' as verb"),
        ("Enhancement", "Verbesserung", "", ""),
        ("Feature", "Funktion", "", ""),
        ("User", "Benutzer", "", ""),
        ("Admin", "Administrator", "", ""),
        ("Instance", "Instanz", "", ""),
        ("Account", "Konto", "", ""),
        ("App Studio", "App Studio", "", "Kept in English in German"),
        ("Workspace", "Arbeitsbereich", "", ""),
        ("Template", "Vorlage", "", ""),
        ("Widget", "Widget", "", "Kept in English"),
        ("Read-only", "schreibgeschützt", "", "Adjective; 'schreibgeschützter Zugriff' = read-only access"),
        ("Tile", "Kachel", "Magic ETL", ""),
        ("Pushdown", "Pushdown", "", "Technical term kept in English"),
        ("AI", "KI", "", "'KI' as acronym; 'Künstliche Intelligenz' spelled out; 'KI-Chat' = AI Chat"),
        ("Artificial Intelligence", "Künstliche Intelligenz", "", ""),
        ("Pass-Through", "Pass-Through", "", "Kept with hyphen"),
        ("Drag-and-drop", "Drag-and-Drop", "", "Kept, capitalized as noun"),
    ],
    "ja": [
        ("Connector", "コネクター", "", "Katakana; singular and plural identical"),
        ("Connectors", "コネクター", "", "Katakana; singular and plural identical"),
        ("Dashboard", "ダッシュボード", "", "Katakana"),
        ("Alert", "アラート", "", "Katakana"),
        ("Alerts", "アラート", "", "Katakana"),
        ("Chart", "グラフ", "", "Kanji (style guide); TM often uses チャート — style guide wins"),
        ("Table", "表", "UI", "Kanji; preferred over テーブル in UI context"),
        ("Table", "テーブル", "database", "Katakana; database or ETL context"),
        ("Filter", "フィルター", "", "Katakana"),
        ("Group", "グループ", "", "Katakana"),
        ("Card", "カード", "", "Katakana"),
        ("Page", "ページ", "", "Katakana"),
        ("Query", "クエリ", "", "Katakana"),
        ("Section", "セクション", "", "Katakana"),
        ("Report", "レポート", "", "Katakana"),
        ("Role", "ロール", "user", "Katakana; user role"),
        ("Role", "権限", "agent-field", "Kanji; the agent 'Role' configuration field"),
        ("Permission", "許可", "", "許可 = a specific grant/permission"),
        ("Grant", "権限", "", "権限 = authority/access broadly"),
        ("Setting", "設定", "", "Kanji"),
        ("Settings", "設定", "", "Kanji"),
        ("Update", "更新", "", "Kanji; '更新する' as verb"),
        ("Enhancement", "機能拡張", "", "Kanji; preferred in feature/product context"),
        ("Feature", "機能", "", "Kanji"),
        ("User", "ユーザー", "", "Katakana"),
        ("Admin", "管理者", "", "Kanji"),
        ("Administrator", "管理者", "", "Kanji"),
        ("Admin Settings", "管理者設定", "", "Kanji compound"),
        ("Instance", "インスタンス", "", "Katakana"),
        ("Account", "アカウント", "", "Katakana"),
        ("App Studio", "App Studio", "", "Kept in English"),
        ("Workspace", "ワークスペース", "", "Katakana"),
        ("Workflow", "ワークフロー", "", "Katakana"),
        ("Workflows", "ワークフロー", "", "Katakana"),
        ("Template", "テンプレート", "", "Katakana"),
        ("Widget", "ウィジェット", "", "Katakana"),
        ("Read-only", "読み取り専用", "", "Kanji compound"),
        ("Tile", "タイル", "Magic ETL", "Katakana"),
        ("Pushdown", "プッシュダウン", "", "Katakana"),
        ("AI", "AI", "", "'AI' kept in EN as acronym; '人工知能' when spelled out"),
        ("Artificial Intelligence", "人工知能", "", ""),
        ("AI Chat", "AIチャット", "", "Mixed; AI kept in English"),
        ("Cloud Integration", "クラウド統合", "", "Katakana + kanji compound"),
        ("Data Center", "Data Center", "", "Kept in English when referring to the Domo UI element"),
        ("Dataset tile", "DataSetアイコン", "Magic ETL", "DataSet kept in English; アイコン (icon) in ETL context"),
    ],
}

# --------------------------------------------------------------------------- #
# 3. Callout labels and standard section headers — highly deterministic,
#    directly checkable. Encoded from the style guide.
# --------------------------------------------------------------------------- #
CALLOUTS = {  # english -> {lang: label}
    "Note":      {"es": "Nota",       "fr": "Remarque", "de": "Hinweis", "ja": "注"},
    "Important": {"es": "Importante",  "fr": "Important", "de": "Wichtig", "ja": "重要"},
    "Tip":       {"es": "Sugerencia",  "fr": "Conseil",   "de": "Tipp",    "ja": "ヒント"},
}
SECTION_HEADERS = {  # english -> {lang: header}
    "New Features and Enhancements": {"es": "Nuevas funciones y mejoras",
                                      "fr": "Nouvelles fonctionnalités et optimisations",
                                      "de": "Neue Funktionen und Verbesserungen",
                                      "ja": "新機能と機能拡張"},
    "Support & Feedback": {"es": "Soporte y comentarios",
                           "fr": "Support technique et commentaires",
                           "de": "Unterstützung und Feedback",
                           "ja": "サポート"},
    "Intro":           {"ja": "はじめに"},
    "Beta Features":   {"ja": "ベータ機能"},
    "Required Grants": {"ja": "必要な許可"},
    "FAQ":             {"ja": "よくある質問"},
}


def load_branded_terms():
    """Return (keep_en_terms, ok_to_translate_terms) from the PMM branded glossary."""
    keep_en, ok_translate = [], []
    with open(BRANDED_CSV, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            term = (row.get("Term") or "").strip()
            if not term:
                continue
            ok = (row.get("OK to Translate?") or "").strip().lower()
            note = (row.get("Notes") or "").strip()
            if ok == "no":
                keep_en.append((term, note))
            elif ok == "yes":
                ok_translate.append((term, note))
    return keep_en, ok_translate


def mine_ja_tm(interest_terms, min_count=5, min_agreement=0.70):
    """Mine high-agreement EN->JA term pairs from approved TM entries.

    Only exact standalone matches (en_US cell == term) are considered, and only
    for terms in ``interest_terms``. Returns {term_lower: (english, ja, count, total, pct)}.
    """
    if not os.path.exists(JA_TM_CSV):
        return {}, "TM file not present (gitignored); skipping JA mining."
    csv.field_size_limit(10 ** 8)
    agg = collections.defaultdict(collections.Counter)
    canonical = {}  # lower -> original casing seen
    interest_lower = {t.lower() for t in interest_terms}
    with open(JA_TM_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (row.get("status") or "") != "approved":
                continue
            en = (row.get("en_US") or "").strip()
            ja = (row.get("ja_JP") or "").strip()
            if not en or not ja:
                continue
            key = en.lower()
            if key in interest_lower:
                agg[key][ja] += 1
                canonical.setdefault(key, en)
    mined = {}
    for key, counter in agg.items():
        total = sum(counter.values())
        ja, cnt = counter.most_common(1)[0]
        pct = cnt / total
        if total >= min_count and pct >= min_agreement:
            mined[key] = (canonical[key], ja, cnt, total, round(pct * 100))
    note = f"Mined {len(mined)} high-agreement terms from approved TM entries."
    return mined, note


def read_existing_preserved(path):
    """Return rows from an existing CSV whose source must be preserved on rebuild."""
    if not os.path.exists(path):
        return []
    preserved = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            src = (row.get("source") or "")
            if src.startswith(PRESERVE_SOURCE_PREFIXES):
                preserved.append({k: row.get(k, "") for k in FIELDS})
    return preserved


def build_language(lang, branded_keep_en, branded_ok, mined_ja):
    """Return the list of glossary rows for one language."""
    rows = []
    seen = set()  # (english_term.lower(), context)

    def add(english, translation, keep_en, context, notes, source):
        k = (english.lower(), context)
        if k in seen:
            return
        seen.add(k)
        rows.append({
            "english_term": english, "translation": translation,
            "keep_in_english": "yes" if keep_en else "no",
            "context": context, "notes": notes,
            "source": source, "last_updated": TODAY,
        })

    def lemmas(term):
        """Case-insensitive term key plus a naive singular/plural variant."""
        t = term.lower()
        variants = {t}
        if t.endswith("s"):
            variants.add(t[:-1])
        else:
            variants.add(t + "s")
        return variants

    def already_seen_term(term):
        return any(e in lemmas(term) for e, _c in seen)

    # a) Universal keep-in-English (style guide "never translated")
    for term, note in UNIVERSAL_KEEP_EN:
        add(term, "", True, "", note, "style-guide")
    met_term, met_note, met_except = MAGIC_ETL
    if lang not in met_except:
        add(met_term, "", True, "", met_note, "style-guide")

    # b) Per-language translation glossary (authoritative)
    for english, translation, context, notes in GLOSSARY.get(lang, []):
        add(english, translation, False, context, notes, "style-guide")

    # c) Callout labels and section headers
    for english, labels in CALLOUTS.items():
        if lang in labels:
            add(english, labels[lang], False, "callout-label",
                f"<{english}> callout label", "style-guide")
    for english, headers in SECTION_HEADERS.items():
        if lang in headers:
            add(english, headers[lang], False, "section-header", "", "style-guide")

    # Terms the per-language guide already translates (keep_in_english=no).
    # The guide is authoritative: a branded "keep in English" row must NOT
    # contradict it, so we skip branded keep-EN for these lemmas.
    translated_lemmas = set()
    for r in rows:
        if r["keep_in_english"] == "no" and r["translation"]:
            translated_lemmas |= lemmas(r["english_term"])

    # d) Branded-terms keep-in-English (universal brand policy).
    #    Skip where the per-language guide already gives a translation.
    for term, note in branded_keep_en:
        if term.lower() in translated_lemmas:
            continue  # guide translates this term — guide wins
        add(term, "", True, "", note or "Branded term — keep in English", "branded-terms")

    # e) JA mining augmentation (new terms only; baseline wins on conflicts).
    #    Runs BEFORE the empty branded OK-to-translate slots so a mined
    #    translation fills the term instead of an empty placeholder.
    if lang == "ja":
        for key, (english, ja, cnt, total, pct) in sorted(mined_ja.items()):
            if already_seen_term(english):
                continue  # already covered by baseline/branded in some context
            add(english, ja, False, "",
                f"Mined from XTM TM: {cnt}/{total} approved ({pct}% agreement)",
                "mined-tm")

    # f) Branded OK-to-translate terms still without any target: documented slot
    #    for the translator / retrospective learning loop to fill.
    for term, note in branded_ok:
        if already_seen_term(term):
            continue
        add(term, "", False, "",
            (note + " " if note else "") + "OK to translate per PMM glossary; "
            "no fixed target yet — fill via translator/retrospective",
            "branded-terms")

    return rows


def write_csv(path, rows, preserved):
    """Write rows + preserved rows to a CSV, sorted for stable diffs."""
    all_rows = rows + preserved
    # stable order: keep-in-English first, then by english_term, then context
    all_rows.sort(key=lambda r: (r["keep_in_english"] != "yes",
                                 r["english_term"].lower(), r["context"]))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in all_rows:
            w.writerow(r)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", action="store_true",
                    help="print the JA TM mining report")
    args = ap.parse_args()

    branded_keep_en, branded_ok = load_branded_terms()

    # interest set for JA mining = all glossary keys + branded terms
    interest = set()
    for lang_rows in GLOSSARY.values():
        interest.update(r[0] for r in lang_rows)
    interest.update(t for t, _ in branded_keep_en)
    interest.update(t for t, _ in branded_ok)
    mined_ja, mine_note = mine_ja_tm(interest)

    print(mine_note)
    if args.report and mined_ja:
        print("\nJA TM mining report (term -> dominant JA, agreement):")
        for key in sorted(mined_ja):
            english, ja, cnt, total, pct = mined_ja[key]
            print(f"  {english:22} -> {ja}  ({cnt}/{total}, {pct}%)")
        print()

    for lang in LANGS:
        path = os.path.join(OUT_DIR, f"{lang}.csv")
        preserved = read_existing_preserved(path)
        rows = build_language(lang, branded_keep_en, branded_ok, mined_ja)
        write_csv(path, rows, preserved)
        kept = sum(1 for r in rows if r["keep_in_english"] == "yes")
        print(f"  {lang}.csv: {len(rows)} generated "
              f"({kept} keep-in-EN) + {len(preserved)} preserved")

    print(f"\nDone. Wrote {len(LANGS)} glossaries to {OUT_DIR}/")


if __name__ == "__main__":
    sys.exit(main())
