# Security

| Way | Use it for |
| --- | --- |
| [Report a vulnerability](https://github.com/Colorado-Startups/brand/security/advisories/new) (GitHub private reporting) | Anything in this repo |
| Email info@coloradostartups.org | When you cannot use GitHub |

Please do not open a public issue. A person replies.

| Control | Where |
| --- | --- |
| Secret scanning with push protection, CodeQL, Dependabot | Repo settings |
| Leak scan (emails, keys, private links, image metadata) on every PR and on the built site | [`tools/vendor/export_scan.py`](tools/vendor/export_scan.py), [`tools/verify.sh`](tools/verify.sh), [`pages.yml`](.github/workflows/pages.yml) |
| Every action pinned by full SHA; read-only default token; fork PRs get no secrets | [`.github/workflows/`](.github/workflows/) |
| Outside PRs merge only after the owner's yes | [`GOVERNANCE.md`](GOVERNANCE.md) |
| Threats and answers | [`THREAT-MODEL.md`](THREAT-MODEL.md) |
