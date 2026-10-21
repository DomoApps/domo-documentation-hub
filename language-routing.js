(function () {
  // Three-letter codes are ISO 639-2; "jp", "sp", and "esp" are non-standard but common.
  const PARAM_TO_FOLDER = {
    en: "",
    de: "de",
    deu: "de",
    ger: "de",
    es: "es",
    spa: "es",
    sp: "es",
    esp: "es",
    fr: "fr",
    fra: "fr",
    fre: "fr",
    ja: "ja",
    jpn: "ja",
    jp: "ja",
  };
  const LANGUAGE_PARAMS = ["language", "lang", "locale", "lng", "hl"];
  const LOCALIZED_FOLDERS = ["de", "es", "fr", "ja"];
  const base = /^\/docs(\/|$)/.test(location.pathname) ? "/docs" : "";

  function parse(pathname) {
    const rest = pathname.slice(base.length) || "/";
    const first = rest.split("/")[1];
    if (LOCALIZED_FOLDERS.includes(first)) {
      return { lang: first, rest: rest.slice(first.length + 1) || "/" };
    }
    return { lang: "", rest };
  }

  function pathFor(lang, rest) {
    return base + (lang ? "/" + lang : "") + rest;
  }

  async function exists(path) {
    try {
      const res = await fetch(path, {
        method: "HEAD",
        credentials: "same-origin",
      });
      return res.ok;
    } catch {
      return false;
    }
  }

  function go(path, params) {
    const search = params.toString();
    location.replace(path + (search ? "?" + search : "") + location.hash);
  }

  async function isMissing(initialLoad) {
    const status =
      initialLoad &&
      performance.getEntriesByType("navigation")[0]?.responseStatus;
    if (status) return status === 404;
    return !(await exists(location.pathname));
  }

  async function route(initialLoad) {
    const params = new URLSearchParams(location.search);
    const { lang, rest } = parse(location.pathname);

    if (lang) {
      if (await isMissing(initialLoad)) go(pathFor("", rest), params);
      return;
    }

    const name = LANGUAGE_PARAMS.find((p) => params.has(p));
    const requested = (name ? params.get(name) : "")
      .toLowerCase()
      .split(/[-_]/)[0];
    const target =
      Object.hasOwn(PARAM_TO_FOLDER, requested) && PARAM_TO_FOLDER[requested];
    if (target && (await exists(pathFor(target, rest)))) {
      LANGUAGE_PARAMS.forEach((p) => params.delete(p));
      go(pathFor(target, rest), params);
    }
  }

  route(true);
  window.addEventListener("mintlify:navigate", () => route(false));
})();
