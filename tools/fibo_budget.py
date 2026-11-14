#!/usr/bin/env python3
"""fibo_budget.py: the guard on Bria's FIBO 2 Free plan (decision 35).

  reserve N   add N calls to this month in art/fibo-calls.yaml, or exit 1 if the
              month would pass the limit (1,950 of the 2,000 free calls)
  check       exit 1 if any month in the ledger is over the limit
  reserve-bria N  add N hosted calls to art/bria-credit.yaml, or exit 1 past its cap
              ($6.00 of Bria's $7.00 free credit; Bria bills the card at $0, decision 42)
  --self-test

Run `reserve` before every FIBO batch; commit the ledger with the batch's PR.
"""
import datetime, json, os, re, sys, tempfile

LEDGER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art", "fibo-calls.yaml")
CREDIT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art", "bria-credit.yaml")


def load(path):
    text = open(path).read()
    limit = int(re.search(r"^limit:\s*(\d+)", text, re.M).group(1))
    months = json.loads(re.search(r"^months:\s*(\{.*\})\s*$", text, re.M).group(1))
    return text, limit, months


def save(path, text, months):
    open(path, "w").write(re.sub(r"^months:.*$", "months: " + json.dumps(months, sort_keys=True), text, flags=re.M))


def reserve(path, n, month):
    text, limit, months = load(path)
    used = months.get(month, 0)
    if used + n > limit:
        print(f"fibo_budget: refused: {month} has {used}, +{n} passes {limit}")
        return 1
    months[month] = used + n
    save(path, text, months)
    print(f"fibo_budget: {month} {used} -> {used + n} of {limit}")
    return 0


def reserve_bria(path, n):
    text = open(path).read()
    cap, price, spent = (int(re.search(rf"^{k}:\s*(\d+)", text, re.M).group(1)) for k in ("cap_mills", "price_mills", "spent_mills"))
    if spent + n * price > cap:
        print(f"fibo_budget: refused: Bria credit spent ${spent / 1000:.3f}, +{n} calls passes ${cap / 1000:.2f}")
        return 1
    open(path, "w").write(re.sub(r"^spent_mills:.*$", f"spent_mills: {spent + n * price}", text, flags=re.M))
    print(f"fibo_budget: Bria credit ${spent / 1000:.3f} -> ${(spent + n * price) / 1000:.3f} of ${cap / 1000:.2f}")
    return 0


def check(path):
    _, limit, months = load(path)
    over = {m: c for m, c in months.items() if c > limit}
    print(f"fibo_budget: {len(over)} month(s) over {limit}")
    return 1 if over else 0


def self_test():
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        f.write("limit: 10\nmonths: {}\n")
    assert reserve(f.name, 6, "2026-11") == 0
    assert reserve(f.name, 5, "2026-11") == 1, "passed the limit"
    assert reserve(f.name, 4, "2026-11") == 0 and check(f.name) == 0
    os.unlink(f.name)
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        f.write("cap_mills: 100\nprice_mills: 32\nspent_mills: 0\n")
    assert reserve_bria(f.name, 3) == 0, "3 calls fit in $0.10"
    assert reserve_bria(f.name, 1) == 1, "the fourth call passes the cap"
    os.unlink(f.name)
    print("fibo_budget self-test: pass")
    return 0


def main(a):
    if a == ["--self-test"]:
        return self_test()
    if a == ["check"]:
        return check(LEDGER)
    if len(a) == 2 and a[0] == "reserve" and a[1].isdigit():
        return reserve(LEDGER, int(a[1]), datetime.date.today().strftime("%Y-%m"))
    if len(a) == 2 and a[0] == "reserve-bria" and a[1].isdigit():
        return reserve_bria(CREDIT, int(a[1]))
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
