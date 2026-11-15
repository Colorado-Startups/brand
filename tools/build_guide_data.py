#!/usr/bin/env python3
"""Build dist/brand.json, dist/tokens.css and dist/tokens.json (decision 9: data is the source of truth).

  python3 tools/build_guide_data.py           write the three files
  python3 tools/build_guide_data.py --check   exit 0 if all fresh, 1 if any is stale or a token rule fails,
                                              3 if PyYAML is missing (could not check)

brand.json is the one file the guide in guide/public/ renders. It reads data/, templates/kit.yaml, tokens/type.yaml,
research/color/state.yaml, TRADEMARKS.md and the files in dist/. It never reads data/words.yaml's franchise lists,
because the franchise gate scans dist/ and the built site. Its downloads list every file in dist/ but itself.

The tokens come from tokens/brand_tokens.yaml, tokens/type.yaml and the State primaries in research/color/state.yaml.
tokens.css is :root custom properties, a prefers-color-scheme block and a [data-theme="dark"] block. tokens.json is
the same set in the Design Tokens format (DTCG 2025.10). The build fails if a recorded contrast ratio is not the
ratio of its two colors, or is under its min (WCAG 2.2: 4.5 text, 3 large text and UI parts).

Needs PyYAML; the other tools are stdlib only, so whoever changes a source reruns this in the same PR, as with the
art (decision 21).
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DIST = os.path.join(ROOT, "dist")
REPO = "https://github.com/Colorado-Startups/brand"
DOWNLOAD_TYPES = (".jpg", ".png", ".ico", ".css", ".json", ".html")
EXT = "org.coloradostartups.brand"  # reverse-domain key for $extensions in tokens.json
HEX = re.compile(r"#[0-9A-F]{6}")


def load(rel):
    import yaml
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return yaml.safe_load(f)


def url_of(source):
    """The first URL in a source entry, a list of them, or None."""
    for s in source if isinstance(source, list) else [source]:
        if isinstance(s, dict) and s.get("url"):
            return s["url"]
    return None


def bullets(rel, heading):
    """The plain-text bullets under one '## heading' of a Markdown file, links reduced to their text."""
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^## " + re.escape(heading) + r"\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        raise SystemExit(f"build_guide_data: no '## {heading}' in {rel}")
    return [re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line[2:].strip()) for line in m.group(1).splitlines() if line.startswith("- ")]


def downloads(blobs):
    """Every file in dist/ of a download type except brand.json, with its size and sha256. blobs maps a dist/ path to the
    bytes about to be written, so the hashes are those of the new files, not the old ones on disk."""
    found = dict(blobs)
    for folder, _, names in os.walk(DIST):
        for name in names:
            rel = os.path.relpath(os.path.join(folder, name), DIST).replace(os.sep, "/")
            if rel != "brand.json" and rel not in found and name.endswith(DOWNLOAD_TYPES):
                with open(os.path.join(folder, name), "rb") as f:
                    found[rel] = f.read()
    return [{"file": rel, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}
            for rel, blob in sorted(found.items()) if rel != "brand.json" and rel.endswith(DOWNLOAD_TYPES)]


def build(blobs):
    s, v, a, w = (load(f"data/{n}.yaml") for n in ("strategy", "voice", "architecture", "world"))
    state, typ = load("research/color/state.yaml"), load("tokens/type.yaml")
    layers = []
    for key in s["pyramid"]["order"]:
        node = s[key]
        if key == "values":
            layers.append({"id": key, "label": "Values", "statement": ", ".join(x["name"] for x in node),
                           "items": [{"name": x["name"], "means": x["means"], "proof": x["proof_behavior"]} for x in node]})
        else:
            layers.append({"id": key, "label": key.capitalize(), "statement": node["statement"],
                           "proof": [p["text"] for p in node.get("proof", [])][:2]})
    land = s["landscape"]
    return {
        "name": "Colorado Startups",
        "repo": REPO,
        "pyramid": layers,
        "audiences": {
            "rings": [{"ring": r["ring"], "label": r["label"], "segments": [x["label"] for x in r["segments"]]} for r in s["audiences"]["rings"]],
            "personas": [{"label": p["label"], "ring": p["ring"], "need": p["need"], "door": p["door"],
                          "channel": p["best_channel"]["name"], "proof": p["proof_point"]["text"]} for p in s["personas"]],
        },
        "positioning": {
            "statement": s["positioning"]["statement"],
            "descriptor": s["positioning"]["descriptor"],
            "axes": {k: {"label": x["label"], "low": x["low"], "high": x["high"]} for k, x in land["axes"].items()},
            "organizations": [{"name": o["name"], "self": bool(o.get("self")), "kind": o["kind"], "x": o["x"], "y": o["y"],
                               "why": f'{o["x_why"]} {o["y_why"]}', "url": url_of(o.get("source"))} for o in land["organizations"]],
        },
        "voice": {
            "traits": [{"id": t["id"], "name": t["name"], "means": t["means"]} for t in v["traits"]],
            "channels": [{k: c[k] for k in ("label", "register", "warm", "direct", "specific", "bright", "note")} for c in v["tone"]["channels"]],
            "pairs": [{"do": p["do"], "dont": p["dont"], "trait": p["trait"]} for p in v["do_dont"]["pairs"]],
            "greeting": v["greeting"]["text"],
            "closing": v["closing"]["text"],
        },
        "words": {
            "boilerplates": [{"id": b["id"], "text": b["text"]} for b in v["boilerplates"]["items"]],
            "style": [x["rule"] for x in load("data/words.yaml")["style"]],
            "glossary": [{"term": g["term"], "means": g["means"]} for g in v["glossary"]["terms"]],
        },
        "color": {"source": {k: (state["source"][0] if isinstance(state["source"], list) else state["source"])[k] for k in ("title", "url", "read")},
                  "primary": [{k: c[k] for k in ("name", "hex", "pms", "rgb", "cmyk")} for c in state["primary"]],
                  "never": state["never"]},
        "type": [{"role": role, **{k: typ[role][k] for k in ("family", "use", "licence")}} for role in ("display", "body", "text") if role in typ],
        "places": w["place_art"],
        "characters": w["characters"],
        "keepers": [{k: x[k] for k in ("name", "kind", "title", "role", "disclosure")} for x in w["keepers"]["list"]],
        "architecture": {
            "nodes": [{"id": n["id"], "name": n["name"], "plain": n["plain_label"], "parent": n["parent"]} for n in a["nodes"]],
            "registers": {k: {x: a["registers"][k][x] for x in ("plain_label", "holds", "serves")} for k in ("core", "hall")},
            "outpost": a["lockups"]["outpost"]["example"],
            "endorsement": a["lockups"]["endorsement"]["line"],
        },
        "use": {"fine": bullets("TRADEMARKS.md", "Fine without asking"), "ask": bullets("TRADEMARKS.md", "Needs written approval"),
                "contact": "https://coloradostartups.org/contact/"},
        "templates": load("templates/kit.yaml")["templates"],
        "downloads": downloads(blobs),
    }


# ---- Tokens: tokens/brand_tokens.yaml, tokens/type.yaml and the State primaries -> dist/tokens.css and tokens.json ----

GROUPS = (("space", "s"), ("radius", "r"), ("line", "line"), ("size", "size"), ("shadow", "sh"))  # after color, before type


def luminance(hx):
    """WCAG 2.2 relative luminance of #RRGGBB."""
    out = 0.0
    for weight, i in ((0.2126, 1), (0.7152, 3), (0.0722, 5)):
        v = int(hx[i:i + 2], 16) / 255
        out += weight * (v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return out


def contrast_ratio(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def color_value(value, primaries, where):
    """'@Blue' is the State primary of that name; anything else must be #RRGGBB."""
    if value.startswith("@"):
        if value[1:] not in primaries:
            raise SystemExit(f"build_guide_data: {where}: no State primary named '{value[1:]}' in research/color/state.yaml")
        return primaries[value[1:]]
    if not HEX.fullmatch(value):
        raise SystemExit(f"build_guide_data: {where}: '{value}' is not #RRGGBB in capitals or @Name")
    return value


def check_contrast(rows, colors, theme):
    """Every recorded ratio must be the computed ratio to two places, and must meet its min."""
    for r in rows:
        for end in ("fg", "bg"):
            if r[end] not in colors:
                raise SystemExit(f"build_guide_data: contrast ({theme}): '{r[end]}' is not a color role")
        got = contrast_ratio(colors[r["fg"]], colors[r["bg"]])
        if f"{got:.2f}" != f"{r['ratio']:.2f}":
            raise SystemExit(f"build_guide_data: contrast ({theme}) {r['fg']} on {r['bg']}: recorded {r['ratio']}, computed {got:.2f}")
        if got < r["min"]:
            raise SystemExit(f"build_guide_data: contrast ({theme}) {r['fg']} on {r['bg']}: {got:.2f} is under {r['min']}")


def token_model():
    doc, typ, state = load("tokens/brand_tokens.yaml"), load("tokens/type.yaml"), load("research/color/state.yaml")
    primaries = {c["name"]: c["hex"].upper() for c in state["primary"]}
    light, night = {}, {}
    for name, c in doc["color"].items():
        light[name] = color_value(c["light"], primaries, f"color.{name}.light")
        night[name] = color_value(c["night"], primaries, f"color.{name}.night") if "night" in c else light[name]
    for old, new in doc["alias"].items():
        if new not in light:
            raise SystemExit(f"build_guide_data: alias {old} points at unknown color {new}")
    check_contrast(doc["contrast"], light, "light")
    check_contrast(doc["contrast-night"], night, "night")
    return {"doc": doc, "type": typ["scale"], "state": state, "primaries": primaries, "light": light, "night": night}


def css_name(s):
    return str(s).lower().replace(" ", "-")


def tokens_css(m):
    doc = m["doc"]
    lines = ["/* Generated by tools/build_guide_data.py from tokens/brand_tokens.yaml, tokens/type.yaml and research/color/state.yaml. Do not edit. */",
             ":root {", "  color-scheme: light;"]
    lines += [f"  --co-{css_name(n)}: {h};" for n, h in m["primaries"].items()]
    lines += [f"  --co-web-{n}: {h};" for n, h in m["state"].get("web", {}).items()]  # the State's web steps (decision 56)
    lines += [f"  --c-{n}: {h};" for n, h in m["light"].items()]
    for group, prefix in GROUPS:
        lines += [f"  --{prefix}-{n}: {v};" for n, v in doc[group].items()]
    lines += [f"  --t-{n}: {v};" for n, v in m["type"].items()]
    lines += [f"  --c-{old}: var(--c-{new});" for old, new in doc["alias"].items()]
    lines.append("}")
    night = "\n".join(f"    --c-{n}: {h};" for n, h in m["night"].items() if h != m["light"][n])
    lines += ["@media (prefers-color-scheme: dark) {", '  :root:not([data-theme="light"]) {', "    color-scheme: dark;", night, "  }", "}",
              ':root[data-theme="dark"] {', "  color-scheme: dark;", night.replace("    --c-", "  --c-"), "}"]
    return "\n".join(lines) + "\n"


def dtcg_color(hx, alpha=1.0):
    out = {"colorSpace": "srgb", "components": [round(int(hx[i:i + 2], 16) / 255, 5) for i in (1, 3, 5)]}
    if alpha != 1:
        out["alpha"] = alpha
    return {**out, "hex": hx}


def number(text):
    n = float(text)
    return int(n) if n == int(n) else n


def dtcg_length(text):
    m = re.fullmatch(r"(-?[\d.]+)(px|rem)?", text)
    if not m:
        raise SystemExit(f"build_guide_data: '{text}' is not a px or rem length")
    return {"value": number(m.group(1)), "unit": m.group(2) or "px"}


def dtcg_shadow(css):
    """'[inset] x y blur [spread] color' with var(--size-*) lengths and a var(--c-*) or rgb(r g b / a) color."""
    inset = css.startswith("inset ")
    parts = re.findall(r"var\(--[a-z0-9-]+\)|rgb\([^)]*\)|[^\s]+", css[6:] if inset else css)
    *lengths, color = parts
    if len(lengths) not in (3, 4):
        raise SystemExit(f"build_guide_data: shadow '{css}' is not 'x y blur [spread] color'")

    def length(t):
        ref = re.fullmatch(r"var\(--size-([a-z0-9-]+)\)", t)
        return "{size." + ref.group(1) + "}" if ref else dtcg_length(t)

    ref = re.fullmatch(r"var\(--c-([a-z0-9-]+)\)", color)
    rgb = re.fullmatch(r"rgb\((\d+) (\d+) (\d+) / ([\d.]+)\)", color)
    if ref:
        col = "{color." + ref.group(1) + "}"
    elif rgb:
        col = dtcg_color("#%02X%02X%02X" % tuple(int(rgb.group(i)) for i in (1, 2, 3)), float(rgb.group(4)))
    else:
        raise SystemExit(f"build_guide_data: shadow color '{color}' is not var(--c-*) or rgb(r g b / a)")
    x, y, blur, spread = (length(t) for t in (lengths if len(lengths) == 4 else lengths + ["0"]))
    out = {"color": col, "offsetX": x, "offsetY": y, "blur": blur, "spread": spread}
    return {**out, "inset": True} if inset else out


def tokens_json(m):
    doc = m["doc"]
    palette = {"$type": "color", "$description": "The State of Colorado primaries (research/color/state.yaml, decision 29)."}
    for c in m["state"]["primary"]:
        palette[css_name(c["name"])] = {"$value": dtcg_color(c["hex"].upper()), "$description": f"{c['name']}, PMS {c['pms']}"}
    if m["state"].get("web"):
        palette["web"] = {"$description": "The State's web steps (Digital Guidelines 1.8), decision 56.",
                          **{n: {"$value": dtcg_color(h.upper())} for n, h in m["state"]["web"].items()}}
    color = {"$type": "color"}
    for name, c in doc["color"].items():
        tok = {"$value": dtcg_color(m["light"][name]), "$description": c["why"]}
        if m["night"][name] != m["light"][name]:
            tok["$extensions"] = {EXT: {"night": dtcg_color(m["night"][name])}}
        color[name] = tok
    alias = {"$type": "color", "$description": "Old names from the dark v1 palette; each points at a color role."}
    alias.update({old: {"$value": "{color." + new + "}"} for old, new in doc["alias"].items()})
    out = {"$description": "Colorado Startups design tokens, v3, in the Design Tokens format (DTCG 2025.10). "
                           "Each color's night (dark theme) value is under $extensions. Built by tools/build_guide_data.py.",
           "palette": palette, "color": color, "alias": alias}
    for group in ("space", "radius", "line", "size"):
        out[group] = {"$type": "dimension", **{str(n): {"$value": dtcg_length(v)} for n, v in doc[group].items()}}
    out["shadow"] = {"$type": "shadow", **{n: {"$value": dtcg_shadow(v)} for n, v in doc["shadow"].items()}}
    typ = {"$type": "dimension"}
    for n, v in m["type"].items():
        ch = re.fullmatch(r"(\d+)ch", v)
        typ[n] = ({"$type": "number", "$value": int(ch.group(1)), "$description": f"Characters per line (CSS {v})"} if ch
                  else {"$value": dtcg_length(v)})
    out["type"] = typ
    pick = [[{k: r[k] for k in ("fg", "bg", "ratio", "min")} for r in doc[key]] for key in ("contrast", "contrast-night")]
    out["$extensions"] = {EXT: {"contrast": {"light": pick[0], "night": pick[1]}}}
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


def dump(data):
    """One top-level key per line: small diffs, few lines."""
    items = [json.dumps(k) + ":" + json.dumps(val, ensure_ascii=False, separators=(",", ":")) for k, val in data.items()]
    return "{\n" + ",\n".join(items) + "\n}\n"


def outputs():
    """Every file this tool owns, as {path under dist/: text}. The tokens are built first: brand.json hashes them."""
    m = token_model()
    files = {"tokens.css": tokens_css(m), "tokens.json": tokens_json(m)}
    files["brand.json"] = dump(build({k: v.encode("utf-8") for k, v in files.items()}))
    return files


def main(argv):
    try:
        import yaml  # noqa: F401
    except ImportError:
        print("build_guide_data: PyYAML is missing; could not build or check", file=sys.stderr)
        return 3
    files = outputs()
    stale = 0
    for name, text in files.items():
        path = os.path.join(DIST, name)
        if "--check" in argv:
            fresh = os.path.exists(path) and open(path, encoding="utf-8").read() == text
            print(f"build_guide_data: dist/{name} is " + ("fresh" if fresh else "stale; rerun the tool"))
            stale += not fresh
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"build_guide_data: wrote dist/{name} ({len(text) // 1024 + 1} KB)")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
