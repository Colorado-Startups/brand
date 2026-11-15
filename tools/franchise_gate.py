#!/usr/bin/env python3
"""franchise_gate.py: no franchise name in a file that ships (decisions 30 and 50).

One rule, two sources joined: the website's franchise-name rule
(tools/vendor/franchise_rule.json) and the `never` list in data/words.yaml,
which adds the names decision 44's places, peoples and heroes and decision
39's characters came from. It scans data/ (except data/words.yaml, the banned
list), dist/, guide/, templates/ and logo/. art/ and decisions.md may name the
influences (decision 44); they never ship.

Usage: python3 tools/franchise_gate.py [ROOT] | --dir PATH | --self-test
  --dir PATH   scan every text file under PATH, such as the built site/
Exit: 0 clean, 1 a finding, 2 usage error, 3 could not read a rule file.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
WORDS = os.path.join(ROOT, "data", "words.yaml")
SHIPS = ("data", "dist", "guide", "templates", "logo")
EXEMPT = {os.path.join("data", "words.yaml")}
TEXT = (".yaml", ".yml", ".json", ".md", ".html", ".css", ".js", ".mjs", ".svg", ".txt")


def block(text, key):
    """The lines of one top-level YAML key, read without PyYAML (tools stay stdlib only)."""
    m = re.search(r"^%s:\n(.*?)(?=^\S|\Z)" % re.escape(key), text, re.M | re.S)
    return m.group(1).splitlines() if m else []


def words_list():
    """(case-insensitive patterns, case-sensitive patterns, hit samples, miss samples) from data/words.yaml."""
    text = open(WORDS, encoding="utf-8").read()
    ci, cs, pat = [], [], None
    for line in block(text, "never"):
        m = re.match(r"\s+pattern: '(.*)'$", line)
        if m:
            pat = m.group(1).replace("''", "'")
        m = re.match(r"\s+case_sensitive: (true|false)$", line)
        if m and pat is not None:
            (cs if m.group(1) == "true" else ci).append(pat)
            pat = None
    hits, misses, into = [], [], None
    for line in block(text, "never_samples"):
        if re.match(r"\s+hit:$", line):
            into = hits
        elif re.match(r"\s+miss:$", line):
            into = misses
        elif into is not None and re.match(r"\s+- ", line):
            into.append(line.split("- ", 1)[1].strip())
    return ci, cs, hits, misses


def rule():
    vendored = json.load(open(os.path.join(HERE, "vendor", "franchise_rule.json")))["rule"]["regex"]
    ci, cs, _, _ = words_list()
    parts = [vendored] + (["(?i:" + "|".join(ci) + ")"] if ci else []) + cs
    return re.compile("|".join("(?:%s)" % p for p in parts))


def scan_files(paths, root, rx):
    found = []
    for p in paths:
        rel = os.path.relpath(p, root)
        if rel in EXEMPT or not p.endswith(TEXT):
            continue
        for n, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
            m = rx.search(line)
            if m:
                found.append("%s:%d: %s" % (rel, n, m.group(0)))
    return found


def walk(top):
    return [os.path.join(d, f) for d, _, fs in os.walk(top) for f in fs]


def scan(root, rx):
    return scan_files([p for top in SHIPS for p in walk(os.path.join(root, top))], root, rx)


def self_test(rx):
    import tempfile
    _, _, hits, misses = words_list()
    assert len(hits) > 50 and len(misses) > 20, "samples not read from data/words.yaml"
    missed = [s for s in hits if not rx.search(s)]
    wrong = [s for s in misses if rx.search(s)]
    assert not missed, "names not caught: %s" % missed
    assert not wrong, "ordinary words flagged: %s" % wrong
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, "data"))
        open(os.path.join(t, "data", "words.yaml"), "w").write("Ironforge\n")
        open(os.path.join(t, "data", "ok.yaml"), "w").write("a mountain forge city\n")
        assert scan(t, rx) == [], "exempt or clean file flagged"
        open(os.path.join(t, "data", "bad.yaml"), "w").write("the halls of Moria\n")
        assert len(scan(t, rx)) == 1, "a franchise name was missed"
        os.makedirs(os.path.join(t, "site"))
        open(os.path.join(t, "site", "index.html"), "w").write("<p>Dragons over Valdrakken</p>\n")
        assert len(scan_files(walk(os.path.join(t, "site")), t, rx)) == 1, "--dir missed a built page"
    print("franchise_gate self-test: pass (%d hits caught, %d misses passed)" % (len(hits), len(misses)))


def main(argv):
    try:
        rx = rule()
    except (OSError, ValueError, KeyError, re.error) as e:
        print("franchise_gate: could not read a rule file (%s)" % e)
        return 3
    args = argv[1:]
    if args == ["--self-test"]:
        self_test(rx)
        return 0
    if len(args) == 2 and args[0] == "--dir":
        found = scan_files(walk(args[1]), args[1], rx)
    elif len(args) <= 1 and not (args and args[0].startswith("-")):
        found = scan(args[0] if args else ".", rx)
    else:
        print(__doc__)
        return 2
    for f in found:
        print(f)
    print("franchise_gate: %d finding(s)" % len(found))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
