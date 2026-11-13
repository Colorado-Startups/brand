# Threat model

Read 2026-11-13. The repo holds brand data, docs, small Python tools and workflows; it serves a static Pages site.

| Threat | Answer | Where |
| --- | --- | --- |
| A fork PR runs code with secrets | Fork PRs get no secrets; approval required for outside runs; `pull_request` only, never `pull_request_target` | `.github/workflows/` |
| A compromised action | Full-SHA pins, `sha_pinning_required`, Dependabot with a 14-day cooldown | `ci.yml`, `dependabot.yml` |
| A leaked key or personal data | Push protection; the leak scan in `verify.sh` and on the built site | `tools/vendor/export_scan.py` |
| A franchise name ships | The franchise gate on `data/`, `dist/`, `guide/`, `templates/`, `logo/` and the built site | `tools/franchise_gate.py` |
| A brand change sneaks in from outside | Outside PRs wait for Paul (decision 34) | `GOVERNANCE.md` |
| A tampered release | Immutable releases, protected `v*` tags | Repo settings |
