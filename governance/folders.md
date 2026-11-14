# Folders and checks

**Precedence.** `CLAUDE.md` wins; it points here for these two tables.

## Folder ownership

| Folder | Owner | What lives there |
|---|---|---|
| `data/strategy.yaml`, `research/strategy/` | S1 Strategy | Purpose, mission, vision, values, promise, positioning, tagline, audiences, personas, messaging |
| `data/architecture.yaml`, `data/world.yaml` | S2 Architecture and world | Brand tree, lockup rules, outposts, towns, crests, influence map |
| `data/voice.yaml`, `data/words.yaml` | S3 Voice and words | Voice, tone by channel, Hall vocabulary, boilerplates, banned words, glossary |
| concepts/a-forged-shield/ (planned) | S4 | Concept A board |
| concepts/b-claim-stake/ (planned) | S5 | Concept B board |
| concepts/c-hearth-ring/ (planned) | S6 | Concept C board |
| `art/` | S7 Art and motion | Art direction, FIBO 2.0 prompt templates, keeper sheets, LTX-2.5 motion rules, licenses |
| `guide/` | S8 Guide engine | The interactive guide on public GitHub Pages |
| `templates/`, .github/workflows/render.yml (planned) | S9 Templates engine | Every application template, rendered in CI |
| `tools/`, `tokens/` (until Wave 2), `.github/workflows/ci.yml`, `.github/workflows/cloud-test.yml`, `.github/cloud-test.json`, root package.json (planned), lockfile and `.nvmrc` | S10 Tooling and gates | Build, checks with self-tests, brand_pull.py (planned), generated skill |
| `governance/`, `data/kpis.yaml` | S11 Governance and measurement | Owners, releases, KPIs, survey, audits |
| `research/color/` | S12c Color research | The category color audit, heritage equity and the color evidence review |
| tokens/brand_tokens.yaml (planned) (Wave 2) | S12 Tokens v3 | The v3 token values |
| `logo/` (Wave 2) | S13 Logo system | Every logo file, lockup, crest and favicon |
| `README.md`, `CLAUDE.md`, `AGENTS.md`, `baseline/`, root community and licence files, `.github/` (except S10's workflows), `.claude/`, `quality/`, `tools/vendor/` | The orchestrator | Only the orchestrator edits these |
| `decisions.md`, `dist/` | Every session | Append your decisions and rebuild `dist/` with `tools/` in your own PR; rebase on conflict (decision 21) |

`baseline/v2/` is a read-only copy of the brand as it stood before the overhaul (public website `682db1b`, 2026-11-13). Read it; never edit it.

## Which checks fire and which wait

| Gate | When | Blocking |
|---|---|---|
| GitHub Actions `ci` (`.github/workflows/ci.yml`, Git Crafter's CI standard running `bash tools/verify.sh`) | **Fires** on every pull request and on push to `main` | Yes. The ruleset requires `ci / ci-ok` |
| GitHub Actions `pages` (`.github/workflows/pages.yml`) | **Fires** on PRs that touch docs, `guide/` or `quality/`; deploys on `main`; daily | No, advisory |
| GitHub Actions `claude-review`, `scorecard`, DCO | `claude-review` on code PRs (needs `CLAUDE_CODE_OAUTH_TOKEN`); `scorecard` on `main`; DCO on every PR | No, advisory |
| GitHub Actions `cloud-test` (`.github/workflows/cloud-test.yml`, a caller of the shared workflow in Colorado-Startups/.github) | **Waits** for a dispatch: `gh workflow run cloud-test.yml --ref <branch> -f script=<name>` runs a name from `.github/cloud-test.json` on a hosted runner. **Fires** on a pull request that changes the caller or the allowlist | No, advisory |
