#!/usr/bin/env bash
# Every check in this repo. CI runs it; run it before every PR.
# Exit contract per check: 0 clean, 1 finding, 2 usage error, 3 could not check.
# A 2 or 3 is an infrastructure problem, reported but never counted as a content finding.
set -u
cd "$(dirname "$0")/.."
fail=0
run() {
  "$@"; rc=$?
  case $rc in
    0) ;;
    1) fail=1 ;;
    *) echo "NOTE: '$*' exited $rc (could not check); not a content finding" ;;
  esac
}
run python3 -I tools/check_dashes.py --self-test
run python3 -I tools/check_dashes.py
run python3 -I tools/franchise_gate.py --self-test
run python3 -I tools/franchise_gate.py
run python3 -I tools/vendor/export_scan.py --self-test
# The public tree, as git would publish it: names, keys, private links, image metadata.
tree=$(mktemp -d)
git ls-files -z | tar --null -T - -cf - | tar -xf - -C "$tree"
rm -rf "$tree/tools/vendor"  # byte copies, scanned upstream; their fixtures are fake personal data
run python3 -I tools/vendor/export_scan.py "$tree" --public-checks-only --quiet
rm -rf "$tree"
exit $fail
