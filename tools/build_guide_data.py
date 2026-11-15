#!/usr/bin/env python3
"""Build dist/brand.json, the one file the guide in guide/public/ renders (decision 9: data is the source of truth).

  python3 tools/build_guide_data.py           write dist/brand.json
  python3 tools/build_guide_data.py --check   exit 0 if fresh, 1 if stale, 3 if PyYAML is missing (could not check)

It reads data/, tokens/type.yaml, research/color/state.yaml, TRADEMARKS.md and the files in dist/. It never reads
data/words.yaml's franchise lists, because the franchise gate scans dist/ and the built site. Needs PyYAML; the other
tools are stdlib only, so whoever changes a source reruns this in the same PR, as with the art (decision 21).
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "dist", "brand.json")
REPO = "https://github.com/Colorado-Startups/brand"


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


def downloads():
    rows = []
    for sub in ("social", "places"):
        folder = os.path.join(ROOT, "dist", sub)
        for name in sorted(os.listdir(folder)):
            if name.endswith(".jpg"):
                with open(os.path.join(folder, name), "rb") as f:
                    blob = f.read()
                rows.append({"file": f"{sub}/{name}", "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    return rows


def build():
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
        "color": {"source": {k: state["source"][k] for k in ("title", "url", "read")},
                  "primary": [{k: c[k] for k in ("name", "hex", "pms", "rgb", "cmyk")} for c in state["primary"]],
                  "never": state["never"]},
        "type": [{"role": role, **{k: typ[role][k] for k in ("family", "use", "licence")}} for role in ("display", "text")],
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
        "downloads": downloads(),
    }


def dump(data):
    """One top-level key per line: small diffs, few lines."""
    items = [json.dumps(k) + ":" + json.dumps(val, ensure_ascii=False, separators=(",", ":")) for k, val in data.items()]
    return "{\n" + ",\n".join(items) + "\n}\n"


def main(argv):
    try:
        import yaml  # noqa: F401
    except ImportError:
        print("build_guide_data: PyYAML is missing; could not build or check", file=sys.stderr)
        return 3
    out = dump(build())
    if "--check" in argv:
        current = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        print("build_guide_data: dist/brand.json is " + ("fresh" if current == out else "stale; rerun the tool"))
        return 0 if current == out else 1
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"build_guide_data: wrote dist/brand.json ({len(out) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
