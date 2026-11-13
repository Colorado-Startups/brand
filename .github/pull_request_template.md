<!-- Tables over prose: about 150 words of prose at most. Delete these comments. -->

## What changed

| File or area | Change | Metric: before → after |
| --- | --- | --- |
| `path/or/area` | one line | `metric.id` 0 → 0, or "none" |

**Why:** one line, with its source. A brand call also goes in `decisions.md`.

## Checks run

| Command | Result |
| --- | --- |
| `one test file or lint` | PASS |

## How to reverse

One line: what to revert or delete. 

<!-- Only when the PR cuts or compresses docs: the claims ledger.
| Claim, figure or entity | Kept, relocated (where) or dropped (why) |
| --- | --- |
-->

## Checklist

- [ ] `bash tools/verify.sh` passes
- [ ] No secret, key or personal data in any file
- [ ] Every AI keeper this touches is named as an AI agent
- [ ] Each commit is signed off (`git commit -s`)

Fixes #
