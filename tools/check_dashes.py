#!/usr/bin/env python3
"""Block em dashes and spaced en dashes in this repo's text files (house rule).

Exit contract: 0 clean, 1 finding, 2 usage error, 3 could not check.
Third-party license texts (root LICENSE and LICENSES/) are not ours to edit,
so they are skipped. --self-test proves both skips, both dash forms, the
case-insensitive extension match and extensionless names such as Makefile.
It also proves unreadable files become notes, deleted files are skipped,
clean samples pass (an unspaced en dash range included), and verdict()
returns 1, 3 and 0.
"""
import os
import subprocess
import sys
import tempfile

EM = "\u2014"
SPACED_EN = " \u2013 "
EXTS = {".md", ".yaml", ".yml", ".html", ".txt", ".mjs", ".js", ".ts", ".py", ".css",
        ".json", ".jsonc", ".svg", ".sh", ".toml", ".xml", ".csv"}
NAMES = {"makefile", ".nvmrc", ".gitignore", ".assetsignore", "dockerfile"}
SKIP_FILES = {"LICENSE"}
SKIP_DIRS = ("LICENSES/",)


def skipped(path):
    return path in SKIP_FILES or path.startswith(SKIP_DIRS)


def scan(root, paths):
    """Return (findings, notes). A note is a file that could not be read."""
    findings, notes = [], []
    for rel in paths:
        base = os.path.basename(rel).lower()
        if skipped(rel) or (os.path.splitext(rel)[1].lower() not in EXTS and base not in NAMES):
            continue
        try:
            with open(os.path.join(root, rel), encoding="utf-8") as fh:
                for n, line in enumerate(fh, 1):
                    if EM in line or SPACED_EN in line:
                        findings.append(f"{rel}:{n}: em dash or spaced en dash")
        except UnicodeDecodeError:
            notes.append(f"NOTE: {rel}: not UTF-8, not checked")
        except FileNotFoundError:
            continue  # deleted in the working tree; git still lists it
        except OSError as exc:
            notes.append(f"NOTE: {rel}: could not read ({exc.strerror}), not checked")
    return findings, notes


def verdict(findings, notes):
    """Exit code: 1 on any finding, else 3 if a file could not be checked, else 0."""
    if findings:
        return 1
    return 3 if notes else 0


def listed(root):
    out = subprocess.run(["git", "-C", root, "ls-files", "-z", "-co", "--exclude-standard"],
                         capture_output=True, check=True)
    return [p for p in out.stdout.decode("utf-8", "surrogateescape").split("\0") if p]


def self_test():
    seeds = {
        "bad-em.md": "one" + EM + "two\n",
        "bad-en.MD": "one" + SPACED_EN + "two\n",
        "clean.md": "one, two; three (four)\n",
        "range.md": "pages 3\u20135\n",
        "LICENSE": "third" + EM + "party\n",
        "LICENSES/x.txt": "third" + EM + "party\n",
        "Makefile": "a" + EM + "b\n",
    }
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "LICENSES"))
        os.makedirs(os.path.join(d, "dir.md"))
        for name, text in seeds.items():
            with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
                fh.write(text)
        with open(os.path.join(d, "latin1.md"), "wb") as fh:
            fh.write(b"caf\xe9\n")
        got, notes = scan(d, list(seeds) + ["dir.md", "latin1.md", "deleted.md"])
    flagged = sorted(f.split(":")[0] for f in got)
    noted = sorted(n.replace("NOTE: ", "", 1).split(":")[0] for n in notes)
    codes = (verdict(got, notes), verdict([], notes), verdict([], []))
    ok = (flagged == ["Makefile", "bad-em.md", "bad-en.MD"] and noted == ["dir.md", "latin1.md"]
          and codes == (1, 3, 0))
    print("check_dashes self-test:", "pass" if ok else f"FAIL findings={got} notes={notes}")
    return 0 if ok else 1


def main(argv):
    if argv[1:] == ["--self-test"]:
        return self_test()
    if argv[1:]:
        print("usage: check_dashes.py [--self-test]", file=sys.stderr)
        return 2
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        paths = listed(root)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"check_dashes: could not list files: {exc}", file=sys.stderr)
        return 3
    findings, notes = scan(root, paths)
    for line in findings + notes:
        print(line)
    print(f"check_dashes: {len(findings)} finding(s), {len(notes)} file(s) not checked")
    return verdict(findings, notes)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
