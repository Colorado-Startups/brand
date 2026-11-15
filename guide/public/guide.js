// The brand guide, rendered from dist/brand.json (tools/build_guide_data.py builds it from data/). No libraries.
"use strict";
const $ = (s) => document.querySelector(s);
const NS = "http://www.w3.org/2000/svg";

function make(doc, tag, props, kids) {
  const n = doc(tag);
  for (const [k, v] of Object.entries(props || {})) {
    if (k === "on") for (const [ev, fn] of Object.entries(v)) n.addEventListener(ev, fn);
    else if (k === "text") n.textContent = v;
    else if (v !== false && v != null) n.setAttribute(k, v === true ? "" : v);
  }
  n.append(...kids.flat().filter((x) => x != null && x !== false));
  return n;
}
const el = (tag, props, ...kids) => make((t) => document.createElement(t), tag, props, kids);
const sv = (tag, props, ...kids) => make((t) => document.createElementNS(NS, t), tag, props, kids);

function toast(msg) {
  const t = el("div", { class: "toast", role: "status", text: msg });
  document.body.append(t);
  setTimeout(() => t.remove(), 1600);
}
function copy(text, label) {
  const done = () => toast(`Copied ${label || text}`);
  if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, () => toast("Copy blocked; select the text instead"));
  else toast("Copy blocked; select the text instead");
}
// One pressed button per group; every control here is a button, so keyboard and screen readers work without extra code.
function press(group, btn, attr = "aria-pressed") {
  group.querySelectorAll(`[${attr}]`).forEach((b) => b.setAttribute(attr, "false"));
  btn.setAttribute(attr, "true");
}
// An SVG shape that acts as a button: focusable, Enter or Space activates it.
function hit(node, label, fn) {
  node.setAttribute("tabindex", "0");
  node.setAttribute("role", "button");
  node.setAttribute("aria-label", label);
  node.classList.add("hit");
  node.addEventListener("click", fn);
  node.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); fn(); } });
  return node;
}
function chips(box, items, label, onPick, attr = "aria-pressed", pick = true) {
  box.replaceChildren(...items.map((it, i) => el("button", { class: "chip", type: "button", [attr]: "false",
    role: attr === "aria-selected" ? "tab" : null, text: label(it), on: { click: (e) => { press(box, e.currentTarget, attr); onPick(it, i); } } })));
  if (pick) box.firstChild.click();
}
// Tabs written in the page: each tab's aria-controls names its panel, one panel shows, arrow keys move along the row.
function tabs(list) {
  const btns = [...list.querySelectorAll('[role="tab"]')];
  const show = (b) => btns.forEach((x) => { const on = x === b; x.setAttribute("aria-selected", String(on)); x.tabIndex = on ? 0 : -1;
    document.getElementById(x.getAttribute("aria-controls")).hidden = !on; });
  btns.forEach((b, i) => {
    b.addEventListener("click", () => show(b));
    b.addEventListener("keydown", (e) => { const step = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
      if (step) { const n = btns[(i + step + btns.length) % btns.length]; e.preventDefault(); show(n); n.focus(); } });
  });
  show(btns.find((b) => b.getAttribute("aria-selected") === "true") || btns[0]);
}

// A file path from dist/brand.json as the built site serves it: paths are relative to dist/, which pages.yml serves at dist/.
const href = (f) => (/^(https?:|\/|dist\/)/.test(f) ? f : `dist/${f}`);
const filesOf = (x) => [].concat(x.files || x.file || []).map((f) => (typeof f === "string" ? f : f && f.file)).filter(Boolean);
// The rows of a key a later package adds (logo, templates), read defensively: a list, a map keyed by id,
// or either one under a wrapper key such as "tiers" or "items". Anything else reads as no rows.
function rowsOf(v, wrappers = []) {
  if (!v || typeof v !== "object") return [];
  const w = !Array.isArray(v) && wrappers.find((k) => v[k] && typeof v[k] === "object");
  if (w) v = v[w];
  return Array.isArray(v) ? v.filter((r) => r && typeof r === "object")
    : Object.entries(v).filter(([, r]) => r && typeof r === "object" && !Array.isArray(r)).map(([id, r]) => ({ id, ...r }));
}
const sizeOf = (r) => { const s = r.size; return s && typeof s === "object" ? [s.width, s.height].filter(Boolean).join(" × ") : s || (r.width && r.height ? `${r.width} × ${r.height}` : ""); };

// WCAG 2.2 relative luminance and contrast ratio.
function lum(hex) {
  const c = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255).map((v) => (v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
}
function ratio(a, b) { const [x, y] = [lum(a), lum(b)].sort((m, n) => n - m); return (x + 0.05) / (y + 0.05); }
const end = (s) => (/[.!?]$/.test(s) ? s : s + ".");
const cap1 = (s) => s.charAt(0).toUpperCase() + s.slice(1);
const grade = (r) => (r >= 4.5 ? "AA" : r >= 3 ? "AA large" : "Below AA");

function theme() {
  const btn = $("#theme");
  const dark = () => document.documentElement.dataset.theme === "dark" ||
    (!document.documentElement.dataset.theme && matchMedia("(prefers-color-scheme: dark)").matches);
  const sync = () => { btn.setAttribute("aria-pressed", String(dark())); btn.textContent = dark() ? "Day" : "Night"; };
  btn.addEventListener("click", () => {
    const next = dark() ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem("cs-theme", next); } catch (e) { /* private mode: the choice lasts this visit */ }
    sync();
  });
  sync();
}

function why(d) {
  const svg = $("#pyramid"), out = $("#why-detail");
  const colors = ["#001970", "#35647E", "#245D38", "#7A853B", "#6D3A5D", "#C3002F"];
  const n = d.pyramid.length, h = 56, gap = 4, base = 580, peak = 120;
  const width = (i) => base - (i * (base - peak)) / n;
  d.pyramid.forEach((layer, i) => {
    const yb = 370 - i * (h + gap), yt = yb - h, wb = width(i), wt = width(i + 1);
    const g = sv("g", {}, sv("polygon", { points: `${300 - wb / 2},${yb} ${300 + wb / 2},${yb} ${300 + wt / 2},${yt} ${300 - wt / 2},${yt}`, fill: colors[i % colors.length], stroke: "rgba(255,255,255,.35)", "stroke-width": 1 }),
      sv("text", { x: 300, y: yt + h / 2 + 7, "text-anchor": "middle", fill: "#fff", "font-size": 19, "font-weight": 700, text: layer.label }));
    svg.append(hit(g, layer.label, () => {
      svg.querySelectorAll("polygon").forEach((p) => { p.setAttribute("stroke", "rgba(255,255,255,.35)"); p.setAttribute("stroke-width", "1"); });
      g.firstChild.setAttribute("stroke", "#FFD100"); g.firstChild.setAttribute("stroke-width", "5");
      out.replaceChildren(el("h3", { text: layer.label }), el("p", { text: layer.statement }),
        layer.items ? el("ul", { class: "list" }, layer.items.map((v) => el("li", {}, el("b", { text: v.name + ". " }), v.means))) :
          layer.proof.length ? el("p", { class: "cap", text: "Proof: " + layer.proof[0] }) : null);
    }));
  });
  svg.querySelector("g").dispatchEvent(new Event("click"));
}

function who(d) {
  const svg = $("#rings"), out = $("#who-detail"), rings = d.audiences.rings;
  const radius = [62, 112, 162], fill = ["#001970", "#35647E", "#7A853B"];
  [...rings].reverse().forEach((r) => {
    const i = r.ring - 1;
    const g = sv("g", {}, sv("circle", { cx: 170, cy: 170, r: radius[i], fill: fill[i] }),
      sv("text", { x: 170, y: i === 0 ? 176 : 170 - radius[i] + 30, "text-anchor": "middle", fill: "#fff", "font-size": i === 0 ? 18 : 14, "font-weight": 700, text: i === 0 ? r.label : r.segments.join(" · ") }));
    svg.append(hit(g, r.label, () => out.replaceChildren(el("h3", { text: `Ring ${r.ring}: ${r.label}` }), el("p", { text: r.segments.join(", ") }))));
  });
  chips($("#personas"), d.audiences.personas, (p) => p.label, (p) => out.replaceChildren(el("h3", { text: p.label }),
    el("p", { text: p.need }), el("p", { class: "cap", text: `Door: ${p.door}. Best channel: ${p.channel}.` }), el("p", { class: "cap", text: p.proof })),
    "aria-pressed", false);
}

function where(d) {
  const p = d.positioning, svg = $("#map"), out = $("#where-detail");
  $("#positioning").textContent = p.statement;
  const X = (v) => 60 + v * 5.2, Y = (v) => 390 - v * 3.6, short = (s) => s.split(":")[0];
  svg.append(sv("line", { x1: X(50), y1: Y(0), x2: X(50), y2: Y(100), stroke: "currentColor", "stroke-opacity": 0.3 }),
    sv("line", { x1: X(0), y1: Y(50), x2: X(100), y2: Y(50), stroke: "currentColor", "stroke-opacity": 0.3 }),
    sv("text", { x: X(0), y: 425, fill: "currentColor", "font-size": 13, text: "← " + short(p.axes.x.low) }),
    sv("text", { x: X(100), y: 425, fill: "currentColor", "font-size": 13, "text-anchor": "end", text: short(p.axes.x.high) + " →" }),
    sv("text", { x: 14, y: Y(100) + 4, fill: "currentColor", "font-size": 13, text: "↑ " + short(p.axes.y.high) }),
    sv("text", { x: 14, y: Y(0), fill: "currentColor", "font-size": 13, text: "↓ " + short(p.axes.y.low) }));
  const show = (o) => out.replaceChildren(el("h3", { text: o.name }), el("p", { class: "cap", text: o.kind }), el("p", { text: o.why }),
    o.url ? el("a", { href: o.url, text: "Source" }) : null);
  p.organizations.forEach((o) => {
    const dot = sv("circle", { cx: X(o.x), cy: Y(o.y), r: o.self ? 11 : 7, fill: o.self ? "#C3002F" : "#35647E", stroke: "#fff", "stroke-width": 2 });
    svg.append(hit(dot, o.name, () => show(o)));
    if (o.self) svg.append(sv("text", { x: X(o.x) - 14, y: Y(o.y) - 16, "text-anchor": "end", fill: "currentColor", "font-size": 14, "font-weight": 700, text: o.name }));
  });
  out.textContent = "Pick a dot.";
}

// The logo's three tiers (decisions 48 and 50). A `logo` key in dist/brand.json wins when a later package adds it.
// Until then the tiers come from decision 50's files in dist/logo/ (dist/README.md, Logo), each listed only when
// `downloads` shows the file exists. With neither, the section shows the wordmark set in type, as on the cards.
const TIERS = ["emblem", "banner", "wordmark", "icon"];
const SHIPPED = {
  emblem: { files: ["logo/emblem-512.png"], use: "Avatars (GitHub org, LinkedIn, Slack) and the website's cards" },
  wordmark: { files: ["logo/wordmark-blue.png", "logo/wordmark-white.png"], use: "Decks, sponsor, State and press pieces, any width" },
  icon: { files: ["logo/icon-512.png"], use: "Favicon, app icons and tiny avatars" },
  banner: { files: ["logo/banner-480x600.png"], use: "Event roll-ups, covers and the guide; it flies the crest (decision 59)" },
};
function logoTiers(d) {
  const keyed = rowsOf(d.logo, ["tiers"]).map((t) => ({ id: String(t.id || t.tier || "").toLowerCase(), use: t.use, size: sizeOf(t), files: filesOf(t) }));
  const have = new Set((d.downloads || []).map((f) => f.file));
  const shipped = TIERS.map((id) => ({ id, use: SHIPPED[id].use, size: "", files: SHIPPED[id].files.filter((f) => have.has(f)) }));
  return (keyed.length ? keyed : shipped).map((t) => ({ ...t, name: cap1(t.id) })).filter((t) => TIERS.includes(t.id) && t.files.length)
    .sort((a, b) => TIERS.indexOf(a.id) - TIERS.indexOf(b.id));
}

function name(d) {
  const spec = $("#specimen"), detail = $("#tier-detail"), typeset = [...spec.childNodes], tiers = logoTiers(d);
  const grounds = [{ label: "On art", bg: "url(dist/places/golden.jpg)", ink: "#fff", dark: true }, { label: "White", bg: "#fff", ink: "#001970" }, { label: "Blue", bg: "#001970", ink: "#fff", dark: true }];
  let ground = grounds[0], tier = null;
  const draw = () => {
    spec.style.background = ground.bg; spec.style.backgroundSize = "cover"; spec.style.color = ground.ink;
    spec.style.textShadow = ground.label === "On art" && !tier ? "0 2px 12px rgba(0,10,40,.7)" : "none";
    spec.classList.toggle("tiered", !!tier);
    if (!tier) return spec.replaceChildren(...typeset);
    // A tier may ship one file per ground (blue ink for light grounds, white for dark); the icon shows at three sizes.
    const art = tier.files.filter((f) => !/\.ico$/i.test(f)), want = ground.dark ? /white|light|reverse/i : /blue|dark|colou?r/i;
    const file = art.find((f) => want.test(f)) || art[0] || tier.files[0], src = href(file.includes("/") ? file : `logo/${file}`);
    spec.replaceChildren(...(tier.id === "icon" ? [64, 32, 16] : [0]).map((px) => {
      const img = el("img", { src, class: `tier-${tier.id}`, width: px || null, height: px || null,
        alt: px ? `The Colorado Startups icon at ${px} px` : `The Colorado Startups ${tier.id}` });
      // A file the site does not serve yet (pages.yml copies dist/logo/ in a later package): fall back to the type.
      img.addEventListener("error", () => { spec.replaceChildren(...typeset); spec.classList.remove("tiered");
        spec.style.textShadow = ground.label === "On art" ? "0 2px 12px rgba(0,10,40,.7)" : "none"; detail.textContent = `${file} is not on this site yet.`; });
      return img;
    }));
  };
  if (tiers.length) {
    $("#name-cap").textContent = "Pick a tier, then a ground. No tagline.";
    $("#name-tiers").hidden = false;
    // No tier is picked on load: the type wordmark shows first, and a file loads only when asked for, so a site
    // that does not serve dist/logo/ yet logs nothing on load.
    chips($("#name-tiers"), tiers, (t) => t.name, (t) => { tier = t; detail.textContent = [t.use, t.size].filter(Boolean).map((s) => end(cap1(String(s)))).join(" "); draw(); },
      "aria-pressed", false);
  } else detail.textContent = "Emblem and icon: in the works.";
  chips($("#name-grounds"), grounds, (g) => g.label, (g) => { ground = g; draw(); });
  $("#name-rules").replaceChildren(...d.words.style.filter((r) => /Colorado Startups|Startupers|"Colorado"/.test(r)).map((r) => el("li", { text: r })));
}

function color(d) {
  const pal = d.color.primary, white = { name: "White", hex: "#FFFFFF" }, box = $("#swatches"), spec = $("#swatch-detail");
  // The swatch shows name and hex; a pick copies the hex and shows the print values below.
  box.replaceChildren(...pal.map((c) => el("button", { class: "swatch", type: "button", "aria-pressed": "false",
    "aria-label": `Copy ${c.name} ${c.hex}, PMS ${c.pms}, RGB ${c.rgb.join(" ")}, CMYK ${c.cmyk.join(" ")}`,
    on: { click: (e) => { press(box, e.currentTarget); copy(c.hex, `${c.name} ${c.hex}`);
      spec.textContent = `${c.name} ${c.hex} · PMS ${c.pms} · RGB ${c.rgb.join(" ")} · CMYK ${c.cmyk.join(" ")}`; } } },
    el("i", { style: `background:${c.hex}` }), el("span", {}, el("b", { text: c.name }), el("br"), c.hex))));
  const grounds = [white, pal.find((c) => c.name === "Blue"), pal.find((c) => c.name === "Yellow")];
  const inks = [...pal, white], prev = $("#contrast-preview");
  const table = $("#contrast");
  table.replaceChildren(el("tr", {}, el("th", { text: "" }), grounds.map((g) => el("th", { scope: "col", text: g.name }))),
    ...inks.map((ink) => el("tr", {}, el("th", { scope: "row", text: ink.name }), grounds.map((g) => {
      if (g.hex === ink.hex) return el("td", { text: "" });
      const r = ratio(ink.hex, g.hex);
      // The grade is drawn, not written: dashed passes for large text only, struck through fails. The preview and label name it.
      return el("td", {}, el("button", { type: "button", class: r >= 4.5 ? "aa" : r >= 3 ? "large" : "fail", style: `background:${g.hex};color:${ink.hex}`,
        "aria-label": `${ink.name} on ${g.name}, ${r.toFixed(1)} to 1, ${grade(r)}`,
        on: { click: () => { prev.style.background = g.hex; prev.style.color = ink.hex;
          prev.textContent = `${ink.name} on ${g.name}: ${r.toFixed(1)}:1, ${grade(r)}. Founders building in Colorado.`; } } },
        `${r.toFixed(1)}:1`));
    }))));
  table.querySelector("td button").click();
  $("#vision").addEventListener("change", (e) => {
    const f = e.target.value ? `url(#cv-${e.target.value})` : "";
    ["#swatches", "#contrast", "#contrast-preview"].forEach((s) => { $(s).style.filter = f; });
  });
  $("#color-never").replaceChildren(...d.color.never.map((t) => el("li", { text: `Never ${t}.` })));
}

function type(d) {
  const box = $("#type-specimens"), input = $("#headline");
  const face = (t) => (t.role === "display" ? "var(--name);font-size:2.2rem" : `"${t.family}", var(--text);font-size:1.15rem`);
  const render = () => box.replaceChildren(...d.type.map((t) => el("div", {}, el("small", { class: "cap", text: `${cap1(t.role)} · ${t.family}` }),
    el("p", { style: `font-family:${face(t)}`, text: input.value || "Colorado Startups" }),
    el("small", { class: "cap", text: `${end(t.use)} ${end(t.licence)}` }))));
  input.addEventListener("input", render);
  render();
}

function voice(d) {
  const v = d.voice, body = $("#pairs tbody"), means = el("p", { class: "cap" }), more = $("#pairs-more");
  $("#traits").after(means);
  // Two pairs per trait show; the rest open with the button under the table.
  let trait = null;
  const pairs = () => {
    const rows = v.pairs.filter((p) => p.trait === trait.id), all = more.getAttribute("aria-expanded") === "true";
    body.replaceChildren(...(all ? rows : rows.slice(0, 2)).map((p) => el("tr", {}, el("td", { text: p.do }), el("td", { text: p.dont }))));
    more.hidden = rows.length <= 2;
    more.textContent = all ? "Fewer examples" : `${rows.length - 2} more examples`;
  };
  more.addEventListener("click", () => { more.setAttribute("aria-expanded", String(more.getAttribute("aria-expanded") !== "true")); pairs(); });
  chips($("#traits"), v.traits, (t) => t.name, (t) => { trait = t; means.textContent = t.means; more.setAttribute("aria-expanded", "false"); pairs(); });
  const sel = $("#channel"), dials = $("#dials");
  sel.replaceChildren(...v.channels.map((c, i) => el("option", { value: i, text: c.label })));
  const show = () => { const c = v.channels[sel.value];
    dials.replaceChildren(...v.traits.map((t) => el("div", { class: "dial" }, el("span", { text: t.name }),
      el("b", {}, el("i", { style: `width:${c[t.id]}%` })), el("span", { text: String(c[t.id]) }))),
      el("p", { class: "cap", text: `${c.register === "community" ? "Community" : "Plain"} register. ${c.note || ""}` })); };
  sel.addEventListener("change", show);
  show();
}

function words(d) {
  const w = d.words, text = $("#boiler");
  chips($("#boiler-tabs"), w.boilerplates, (b) => b.id[0].toUpperCase() + b.id.slice(1), (b) => {
    text.textContent = b.text; $("#boiler-count").textContent = `${b.text.split(/\s+/).length} words`; }, "aria-selected");
  $("#boiler-copy").addEventListener("click", () => copy(text.textContent, "the boilerplate"));
  $("#greeting").textContent = `Newsletters open with "${d.voice.greeting}" Big moments close with "${d.voice.closing}"`;
  $("#style").replaceChildren(...w.style.map((r) => el("li", { text: r })));
  const q = $("#gloss-q"), list = $("#glossary");
  const show = () => { const s = q.value.trim().toLowerCase();
    const hits = w.glossary.filter((g) => !s || g.term.toLowerCase().includes(s) || g.means.toLowerCase().includes(s)).slice(0, s ? 8 : 0);
    list.replaceChildren(...hits.flatMap((g) => [el("dt", { text: g.term }), el("dd", { text: g.means })])); };
  q.addEventListener("input", show);
  show();
}

function world(d) {
  const img = $("#place-img"), cap = $("#place-cap"), kin = $("#place-kin");
  // Each place's one blended people, its wild creature and its mount (decision 44), in generic words.
  chips($("#place-picks"), d.places, (p) => p.town, (p) => { img.src = `dist/${p.file}`; img.alt = `${p.caption}. AI-made image.`;
    cap.textContent = `${p.town}, ${p.region}. ${p.caption}. ${p.credit}.`;
    kin.replaceChildren(...[["People", p.people], ["Creature", p.creature], ["Mount", p.mount]].filter(([, x]) => x)
      .map(([k, x]) => el("div", {}, el("dt", { text: k }), el("dd", { text: cap1(x) })))); });
  const reg = d.architecture.registers, demo = $("#register-demo");
  chips($("#registers"), ["core", "community"], (k) => (k === "core" ? "Plain" : "Community"), (k) => {
    demo.className = `register ${k}`;
    demo.style.backgroundImage = k === "community" ? "url(dist/places/denver.jpg)" : "none";
    demo.replaceChildren(el("strong", { text: d.name }), el("small", { text: `${cap1(reg[k].holds)}. For ${reg[k].serves.join(", ")}.` }));
  });
}

function characters(d) {
  $("#cards").replaceChildren(...d.characters.map((c) => el("figure", {}, el("img", { src: `dist/${c.card}`, alt: `${c.name}, ${c.what.toLowerCase()}. AI-made image.`, loading: "lazy", width: 1280, height: 640 }),
    el("figcaption", {}, el("b", { text: c.name }), `. ${c.what}. `, el("a", { href: `https://github.com/${c.repo}`, text: c.repo.split("/")[1] })))));
  const out = $("#keeper-detail");
  out.textContent = "Pick a keeper.";
  chips($("#keepers"), d.keepers, (k) => k.name, (k) => { out.textContent = `${k.name}, ${k.title}. ${end(k.role)} ${k.disclosure}`; }, "aria-pressed", false);
}

function family(d) {
  const a = d.architecture, nodes = a.nodes, out = $("#family-detail"), tree = $("#tree");
  const kids = (id) => nodes.filter((n) => n.parent === id);
  // The master and its first branches show; a deeper branch opens with the toggle beside its name.
  const branch = (n, depth) => {
    const sub = kids(n.id), open = depth === 0;
    const list = sub.length ? el("ul", { id: `branch-${n.id}`, hidden: !open }, sub.map((k) => branch(k, depth + 1))) : null;
    const toggle = sub.length && !open ? el("button", { type: "button", class: "twist", "aria-expanded": "false", "aria-controls": `branch-${n.id}`,
      "aria-label": `Branches under ${n.name}`, on: { click: (e) => { const now = e.currentTarget.getAttribute("aria-expanded") !== "true";
        e.currentTarget.setAttribute("aria-expanded", String(now)); list.hidden = !now; } } }) : null;
    return el("li", { class: toggle ? "has-kids" : null }, toggle, el("button", { type: "button", class: "node", "aria-pressed": "false", text: n.name,
      on: { click: (e) => { press(tree, e.currentTarget); out.replaceChildren(el("b", { text: n.name }), `: ${n.plain}.`); } } }), list);
  };
  tree.replaceChildren(...kids(null).map((n) => branch(n, 0)));
  tree.querySelector(".node").click();
  // The two lockups as type specimens. The region lockup's crest waits on the logo (decision 48), so it is type only.
  const [lead, ...place] = a.region.split(" · ");
  $("#lockup-region").replaceChildren(el("span", { class: "rule", "aria-hidden": "true" }),
    el("span", { class: "lockup-line" }, lead, place.length ? el("span", { class: "place" }, el("span", { class: "sep", text: " · " }), place.join(" · ")) : null));
  const project = nodes.find((n) => n.parent === "projects");
  $("#lockup-endorse").replaceChildren(project ? el("b", { text: project.name }) : null, el("small", { text: a.endorsement }));
}

function use(d) {
  $("#use-fine").replaceChildren(...d.use.fine.map((t) => el("li", { text: t })));
  $("#use-ask").replaceChildren(...d.use.ask.map((t) => el("li", { text: t })));
  tabs($("#use-tabs"));
}

// Files by folder. When dist/brand.json has a `templates` key (a later package adds it), Applications comes first:
// each template's name, size and use, linked to its files.
const FOLDERS = { social: "Cards", places: "Places", templates: "Templates" };
function templateRows(t) {
  return rowsOf(t, ["items", "list", "templates"]).map((r) => ({ name: r.name || r.label || r.title || r.id, use: r.use, size: sizeOf(r), files: filesOf(r) }))
    .filter((r) => r.name);
}

function files(d) {
  const body = $("#files tbody"), table = $("#files-box"), apps = $("#apps");
  const folder = (f) => (f.includes("/") ? f.split("/")[0] : "");
  const rows = d.downloads.map((f) => [folder(f.file), el("tr", {}, el("td", {}, el("a", { href: `dist/${f.file}`, download: "", text: f.file })),
    el("td", { text: `${Math.round(f.bytes / 1024)} KB` }),
    el("td", {}, el("button", { type: "button", title: f.sha256, "aria-label": `Copy the sha256 of ${f.file}`, on: { click: () => copy(f.sha256, "the sha256") } }, el("code", { text: f.sha256.slice(0, 16) + "…" }))))]);
  const groups = [...new Set(rows.map(([g]) => g))].map((g) => ({ id: g, label: FOLDERS[g] || (g ? cap1(g) : "Data") }));
  const tpl = templateRows(d.templates);
  if (tpl.length) {
    apps.replaceChildren(...tpl.map((t) => el("li", {}, t.files.length === 1 ? el("a", { href: href(t.files[0]), text: t.name }) : el("b", { text: t.name }),
      t.size ? el("span", { class: "cap", text: ` ${t.size}` }) : null, t.use ? el("span", { class: "cap", text: ` · ${cap1(String(t.use))}` }) : null,
      t.files.length > 1 ? t.files.flatMap((f) => [" ", el("a", { href: href(f), text: f.split("/").pop() })]) : null)));
    groups.unshift({ id: null, label: "Applications" });
  }
  chips($("#file-picks"), groups, (g) => g.label, (g) => { apps.hidden = g.id !== null; table.hidden = g.id === null;
    body.replaceChildren(...rows.filter(([id]) => id === g.id).map(([, tr]) => tr)); });
}

function sources(d) {
  document.querySelectorAll("a.src").forEach((a) => { a.href = `${d.repo}/blob/main/${a.dataset.src}`; });
}

theme();
fetch("dist/brand.json").then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); }).then((d) => {
  [sources, why, who, where, name, color, type, voice, words, world, characters, family, use, files].forEach((fn) => {
    try { fn(d); } catch (e) { console.error(fn.name, e); }
  });
  const target = location.hash && document.querySelector(location.hash);
  if (target) target.scrollIntoView({ behavior: "instant" });
}).catch((e) => { $("#start").append(el("p", { class: "panel", text: `The guide's data did not load (${e.message}). The source is on GitHub.` })); });
