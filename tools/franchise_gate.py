#!/usr/bin/env python3
"""franchise_gate.py: no franchise name in a file that ships (decision 30).

Runs the website's franchise-name rule (tools/vendor/franchise_rule.json) over
data/ (except data/words.yaml, the banned list), dist/, guide/, templates/ and
logo/. art/DIRECTION.md and NOTICE may name the influences; they never ship.

Usage: python3 tools/franchise_gate.py [ROOT] | --self-test
Exit: 0 clean, 1 a finding, 2 usage error.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHIPS = ("data", "dist", "guide", "templates", "logo")
EXEMPT = {os.path.join("data", "words.yaml")}
TEXT = (".yaml", ".yml", ".json", ".md", ".html", ".css", ".js", ".mjs", ".svg", ".txt")


def rule():
    r = json.load(open(os.path.join(HERE, "vendor", "franchise_rule.json")))["rule"]
    return re.compile(r["regex"])


def scan(root, rx):
    found = []
    for top in SHIPS:
        for d, _, files in os.walk(os.path.join(root, top)):
            for f in files:
                p = os.path.join(d, f)
                rel = os.path.relpath(p, root)
                if rel in EXEMPT or not f.endswith(TEXT):
                    continue
                for n, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
                    m = rx.search(line)
                    if m:
                        found.append("%s:%d: %s" % (rel, n, m.group(0)))
    return found


def self_test(rx):
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, "data"))
        open(os.path.join(t, "data", "words.yaml"), "w").write("Ironforge\n")
        open(os.path.join(t, "data", "ok.yaml"), "w").write("a mountain forge city\n")
        assert scan(t, rx) == [], "exempt or clean file flagged"
        open(os.path.join(t, "data", "bad.yaml"), "w").write("the halls of Moria\n")
        assert len(scan(t, rx)) == 1, "a franchise name was missed"
    print("franchise_gate self-test: pass")


def main(argv):
    rx = rule()
    if argv[1:] == ["--self-test"]:
        self_test(rx)
        return 0
    if len(argv) > 2:
        print(__doc__)
        return 2
    found = scan(argv[1] if len(argv) == 2 else ".", rx)
    for f in found:
        print(f)
    print("franchise_gate: %d finding(s)" % len(found))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
