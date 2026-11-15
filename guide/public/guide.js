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
    el("p", { text: p.need }), el("p", { class: "cap", text: `Door: ${p.door}. Best channel: ${p.channel}.` }), el("p", { class: "cap", text: p.proof })));
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

function name(d) {
  const spec = $("#specimen");
  const grounds = [{ label: "On art", bg: "url(dist/places/golden.jpg)", ink: "#fff" }, { label: "White", bg: "#fff", ink: "#001970" }, { label: "Blue", bg: "#001970", ink: "#fff" }];
  chips($("#name-grounds"), grounds, (g) => g.label, (g) => { spec.style.background = g.bg; spec.style.backgroundSize = "cover"; spec.style.color = g.ink;
    spec.style.textShadow = g.label === "On art" ? "0 2px 12px rgba(0,10,40,.7)" : "none"; });
  $("#name-rules").replaceChildren(...d.words.style.filter((r) => /Colorado Startups|Startupers|"Colorado"/.test(r)).map((r) => el("li", { text: r })));
}

function color(d) {
  const pal = d.color.primary, white = { name: "White", hex: "#FFFFFF" };
  $("#swatches").replaceChildren(...pal.map((c) => el("button", { class: "swatch", type: "button", title: `RGB ${c.rgb.join(" ")} · CMYK ${c.cmyk.join(" ")}`,
    "aria-label": `Copy ${c.name} ${c.hex}, PMS ${c.pms}, RGB ${c.rgb.join(" ")}, CMYK ${c.cmyk.join(" ")}`, on: { click: () => copy(c.hex, `${c.name} ${c.hex}`) } },
    el("i", { style: `background:${c.hex}` }), el("span", {}, el("b", { text: c.name }), el("br"), `${c.hex} · PMS ${c.pms}`))));
  const grounds = [white, pal.find((c) => c.name === "Blue"), pal.find((c) => c.name === "Yellow")];
  const inks = [...pal, white], prev = $("#contrast-preview");
  const table = $("#contrast");
  table.replaceChildren(el("tr", {}, el("th", { text: "" }), grounds.map((g) => el("th", { scope: "col", text: g.name }))),
    ...inks.map((ink) => el("tr", {}, el("th", { scope: "row", text: ink.name }), grounds.map((g) => {
      if (g.hex === ink.hex) return el("td", { text: "" });
      const r = ratio(ink.hex, g.hex);
      return el("td", {}, el("button", { type: "button", style: `background:${g.hex};color:${ink.hex}`, "aria-label": `${ink.name} on ${g.name}, ${r.toFixed(1)} to 1, ${grade(r)}`,
        on: { click: () => { prev.style.background = g.hex; prev.style.color = ink.hex;
          prev.textContent = `${ink.name} on ${g.name}: ${r.toFixed(1)}:1, ${grade(r)}. Founders building in Colorado.`; } } },
        `${r.toFixed(1)}:1`, el("small", { text: grade(r) })));
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
  const render = () => box.replaceChildren(...d.type.map((t) => el("div", {}, el("small", { class: "cap", text: `${t.role === "display" ? "Display" : "Text"} · ${t.family}` }),
    el("p", { style: `font-family:${t.role === "display" ? "var(--name);font-size:2.2rem" : "var(--text);font-size:1.15rem"}`, text: input.value || "Colorado Startups" }),
    el("small", { class: "cap", text: `${end(t.use)} ${end(t.licence)}` }))));
  input.addEventListener("input", render);
  render();
}

function voice(d) {
  const v = d.voice, body = $("#pairs tbody"), means = el("p", { class: "cap" });
  $("#traits").after(means);
  chips($("#traits"), v.traits, (t) => t.name, (t) => { means.textContent = t.means;
    body.replaceChildren(...v.pairs.filter((p) => p.trait === t.id).map((p) => el("tr", {}, el("td", { text: p.do }), el("td", { text: p.dont })))); });
  const sel = $("#channel"), dials = $("#dials");
  sel.replaceChildren(...v.channels.map((c, i) => el("option", { value: i, text: c.label })));
  const show = () => { const c = v.channels[sel.value];
    dials.replaceChildren(...v.traits.map((t) => el("div", { class: "dial" }, el("span", { text: t.name }),
      el("b", {}, el("i", { style: `width:${c[t.id]}%` })), el("span", { text: String(c[t.id]) }))),
      el("p", { class: "cap", text: `${c.register === "hall" ? "Community" : "Plain"} register. ${c.note || ""}` })); };
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
  const img = $("#place-img"), cap = $("#place-cap");
  chips($("#place-picks"), d.places, (p) => p.town, (p) => { img.src = `dist/${p.file}`; img.alt = `${p.caption}. AI-made image.`;
    cap.textContent = `${p.town}, ${p.region}. ${p.caption}. ${p.credit}.`; });
  const reg = d.architecture.registers, demo = $("#register-demo");
  chips($("#registers"), ["core", "hall"], (k) => (k === "core" ? "Plain" : "Community"), (k) => {
    demo.className = `register ${k}`;
    demo.style.backgroundImage = k === "hall" ? "url(dist/places/denver.jpg)" : "none";
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
  const nodes = d.architecture.nodes, out = $("#family-detail"), tree = $("#tree");
  const kids = (id) => nodes.filter((n) => n.parent === id);
  const branch = (n) => el("li", {}, el("button", { type: "button", "aria-pressed": "false", text: n.name,
    on: { click: (e) => { press(tree, e.currentTarget); out.replaceChildren(el("b", { text: n.name }), `: ${n.plain}.`); } } }),
  kids(n.id).length ? el("ul", {}, kids(n.id).map(branch)) : null);
  tree.replaceChildren(...kids(null).map(branch));
  tree.querySelector("button").click();
  $("#lockups").textContent = `Outpost lockup: "${d.architecture.outpost}". Projects close with "${d.architecture.endorsement}".`;
}

function use(d) {
  $("#use-fine").replaceChildren(...d.use.fine.map((t) => el("li", { text: t })));
  $("#use-ask").replaceChildren(...d.use.ask.map((t) => el("li", { text: t })));
}

function files(d) {
  $("#files tbody").replaceChildren(...d.downloads.map((f) => el("tr", {}, el("td", {}, el("a", { href: `dist/${f.file}`, download: "", text: f.file })),
    el("td", { text: `${Math.round(f.bytes / 1024)} KB` }),
    el("td", {}, el("button", { type: "button", title: f.sha256, "aria-label": `Copy the sha256 of ${f.file}`, on: { click: () => copy(f.sha256, "the sha256") } }, el("code", { text: f.sha256.slice(0, 16) + "…" }))))));
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
