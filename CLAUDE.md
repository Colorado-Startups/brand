# Colorado Startups brand: project instructions

This public, open-source repo is the one source of the Colorado Startups brand: strategy, voice, tokens, logos, art direction, templates and the visual guide. Every other repo pins a release of it and copies from it. The guide is a public GitHub Pages site at `colorado-startups.github.io/brand/`, and never lives on a coloradostartups.org address (decisions 18 and 28). Its private development history is `Colorado-Startups/brand-private` (archived).

## Precedence

- `~/.claude/rules/*.md` (the house rules) win on writing, gates, delegation, keys and Comfy spend.
- On anything brand, this repo wins over every copy elsewhere. A copy that disagrees gets fixed from here, never the other way.
- The approved plan is `~/.claude/plans/can-you-make-a-magical-wren.md` (Paul approved it 2026-11-02). `decisions.md` records every call made since, and wins over the plan where they differ.

## Who decides

Paul is the vision and the community manager. Claude makes every design, research and technical call, then logs it (decision 4). No humans work in production: Claude makes every logo, mark, template and asset (decision 5). Paul is asked only for his queue: money, sign-ins, deletions the bash guard blocks, anything sent as Paul (`~/.claude/rules/delegation.md`), and every outside contributor's PR (decision 34).

## Session start

1. Read this file, then `decisions.md`, then your row below and its folder's `README.md`.
2. Read the plan section for your session (search the plan for your session number, such as `S4`).
3. Work only in the folders your row owns. If you need a change anywhere else, put it in your report as a `REQUEST:` line.

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

## Rules that never bend

- **Original only in what ships.** Anything public borrows no name, emblem, silhouette, iconic item, script, rune, font or picture from a game or film franchise, and passes the website's franchise gate. Never use a franchise picture as an AI reference image (`baseline/v2/lore.md`). The influences are named openly here (decision 30); what ships borrows nothing from them.
- **Every keeper says it is an AI agent** wherever it appears, in words or in a picture. The disclosure text comes from the website's data/team/dwarves.yaml (copy in `baseline/v2/`).
- **Colors come from evidence, not preference** (decision 20): every main color carries a rationale against the six-point method.
- **Real places keep their meaning.** Places that matter to the Ute and other tribes, such as Garden of the Gods, are never fantasy decoration.
- **Accessibility.** WCAG 2.2 AA: 4.5:1 for text, 3:1 for large text and UI parts. Motion that starts on its own stops within 5 s or has a pause control. Nothing flashes more than three times a second.
- **Fonts must be properly licensed.** A font that costs money waits for Paul's spend approval.
- **Nothing heavy runs on this Mac.** Never install Playwright browsers locally; image renders of templates run in GitHub Actions. Run `df -h /` before any install. Renders run only on the free lanes in `art/LICENSES.md` (decision 31), each batch after Paul's yes.
- **Compute:** cloud first, the Mac last and small (Paul, 2026-11-02). CI, test suites, builds, browsers, e2e, renders and GPU jobs run in the cloud (`.github/workflows/cloud-test.yml` here). The MacBook Air runs only rare, seconds-long checks, such as one test file or one lint. House rule: `~/.claude/rules/compute.md` (canonical: Code-OS rules/compute.md), which wins any disagreement.

## Data conventions

- Source of truth is YAML in `data/` and `tokens/`. One file per owner, so parallel sessions never edit the same file.
- `dist/` is generated by `tools/`. Every PR that changes a source rebuilds it, and S10's drift check blocks when it is stale (decision 21).
- Prefer no dependencies. A session that needs Node packages keeps a package.json (planned) inside its own folder; the root one belongs to S10.

## Git and pull requests

- Work in your own worktree on a branch named for your session. Commits are signed.
- Never push to `main`, never force-push, never merge. Open a PR to `main` as soon as `bash tools/verify.sh` passes.
- Outside PRs: before merging, the orchestrator runs `gh pr view <n> --json authorAssociation`. Anyone not `OWNER`, `MEMBER` or `COLLABORATOR` waits for Paul's yes in chat, quoted in the PR (decision 34).
- The PR body lists what changed, the decisions you appended to `decisions.md`, and the commands that prove it.
- End your turn with a short report. Put open questions on `QUESTION:` lines. The orchestrator, the session that started you, answers them.

## Commands

| Task | Command |
|---|---|
| Every check | `bash tools/verify.sh` |
| Every check, on a hosted runner | `gh workflow run cloud-test.yml --ref <branch> -f script=verify` |
| Disk before an install | `df -h /` |

## Which checks fire and which wait

| Gate | When | Blocking |
|---|---|---|
| GitHub Actions `ci` (`.github/workflows/ci.yml`, Git Crafter's CI standard running `bash tools/verify.sh`) | **Fires** on every pull request and on push to `main` | Yes. The ruleset requires `ci / ci-ok` |
| GitHub Actions `pages` (`.github/workflows/pages.yml`) | **Fires** on PRs that touch docs, `guide/` or `quality/`; deploys on `main`; daily | No, advisory |
| GitHub Actions `claude-review`, `scorecard`, DCO | `claude-review` on code PRs (needs `CLAUDE_CODE_OAUTH_TOKEN`); `scorecard` on `main`; DCO on every PR | No, advisory |
| GitHub Actions `cloud-test` (`.github/workflows/cloud-test.yml`, a caller of the shared workflow in Colorado-Startups/.github) | **Waits** for a dispatch: `gh workflow run cloud-test.yml --ref <branch> -f script=<name>` runs a name from `.github/cloud-test.json` on a hosted runner. **Fires** on a pull request that changes the caller or the allowlist | No, advisory |
