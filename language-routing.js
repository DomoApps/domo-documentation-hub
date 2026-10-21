(function () {
  // docs.json calls Japanese "jp", but the content folder and URLs use "ja".
  const PARAM_TO_FOLDER = { en: "", de: "de", es: "es", fr: "fr", ja: "ja", jp: "ja" };
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
      const res = await fetch(path, { method: "HEAD", credentials: "same-origin" });
      return res.ok;
    } catch {
      return false;
    }
  }

  function go(path, params) {
    const search = params.toString();
    location.replace(path + (search ? "?" + search : "") + location.hash);
  }

  async function route() {
    const params = new URLSearchParams(location.search);
    const requested = (params.get("language") || "").toLowerCase();
    const { lang, rest } = parse(location.pathname);

    if (requested in PARAM_TO_FOLDER) {
      const target = PARAM_TO_FOLDER[requested];
      if (target !== lang && (await exists(pathFor(target, rest)))) {
        params.delete("language");
        return go(pathFor(target, rest), params);
      }
    }

    if (lang && !(await exists(location.pathname))) {
      const english = pathFor("", rest);
      if (await exists(english)) go(english, params);
    }
  }

  route();
  window.addEventListener("mintlify:navigate", route);
})();
