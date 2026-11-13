# Releases

**Precedence.** `decisions.md` (decisions 9, 10, 18 and 21) and `CLAUDE.md` win over this page. If they disagree, fix this page in the same session. Only the orchestrator releases, and it reviews and merges every pull request, the release's included (house rule).

The brand follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html). A consumer pins a tag in its `brand.lock.json`, so the version number tells it how much work an upgrade is. `v3.0.0` is the overhaul (decision 10).

## What each bump means

| Bump | When | Examples |
|---|---|---|
| **Major** `4.0.0` | A consumer must change its code, or the public would see a new identity | Removing or renaming a token, data key or `dist/` path; a new primary mark or wordmark; a new type family; a color role moving to a different hue; a new name or tagline |
| **Minor** `3.1.0` | Something is added, or a value changes inside the same identity | A new token, logo variant, outpost crest, template, guide section or data field; a color value that keeps its hue and every contrast pair at its minimum; a deprecation, with the old name kept as an alias until the next major |
| **Patch** `3.0.1` | Nothing is meant to look different | A typo, metadata, a provenance label, a build or checksum fix; an asset brought back to its own spec, such as a drifted color reset to its token |

When a change could fit two rows, take the larger bump.

## Release steps

```mermaid
flowchart LR
  A[main green] --> B[Confirm dist/ is current]
  B --> C[Run the checks]
  C --> D[Changelog entry]
  D --> E[Signed tag and release]
  E --> F[Publish the guide]
  F --> G[Message consumers]
  G --> H[Pull PRs in consumers]
```

1. **Freeze.** Every pull request for the release is merged and CI is green on `main`.
2. **Confirm `dist/` is current.** Every pull request that changes a source rebuilds `dist/` itself, and S10's drift check blocks a stale one (decision 21). On a release branch, run S10's build (its command will be in `tools/README.md`); it must leave no diff. If it does, commit the rebuilt `dist/` there.
3. **Run the checks.** `bash tools/verify.sh` must pass. Once S10 ships them, `python3 -I tools/brand_pull.py --self-test` must pass too, and a dry-run pin into a scratch folder must match the `dist/` checksums. The guide has no word or control limit to check (decision 21).
4. **Write the changelog entry** (format below). It points to the decisions each session appended to `decisions.md`; it does not restate them. Then merge the release branch under the usual review rule.
5. **Tag and release.** `git tag -s vX.Y.Z -m "vX.Y.Z"` on the merge commit, push the tag, then `gh release create vX.Y.Z --notes-file <the entry>`. Attach the checksums that `brand_pull.py` checks.
6. **Publish the guide.** `pages.yml` deploys on merge to `main` (decision 28). Load `colorado-startups.github.io/brand/` and confirm the version it shows.
7. **Message consumers.** Send each consumer's session the tag and the sha256 of every file it pulls.
8. **Open pull PRs in consumers.** In each consumer below, bump `brand.lock.json` to the new tag, pull the files with `brand_pull.py` (it fetches through `gh`, so no key is handled), commit the copies, and open a pull request that quotes the changelog entry. The consumer's CI runs `brand_pull.py --check` (decision 10). A major release lists every "Consumers must" line. Each consumer's own orchestrator merges.

## Consumers

| Consumer | How it takes a release | Session that wires it |
|---|---|---|
| `coloradostartups-site` | `brand.lock.json` and `scripts/brand_pull.py` | W1 |
| `.github`, `.github-private` (org profiles) | Copies its images and links from a tag | S16 |
| `photon-mountain`, `space-peak` | Whatever relationship the orchestrator sets for each; the brand has no fixed sub-brand rule (decision 21) | S17 |
| LinkedIn kit, `Volunteers/Roles`, `AI Initiatives/Pages` (local folders) | A Claude session copies from the tag | S15 |

## Changelog format

The orchestrator keeps `CHANGELOG.md` at the repo root in the [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) shape: newest first, an `Unreleased` section on top, ISO dates. Each line names its pull request and any decision it carries out. Majors add a "Consumers must" section.

```markdown
## [Unreleased]

## [3.1.0] - 2026-12-01
### Added
- Outpost crest for Golden (#41, decision 12).
### Changed
- `color.link` darkened within its hue; every contrast pair still passes (#43).
### Deprecated
- `color.gold` alias; use `color.accent`. Removed in 4.0.0 (#44).
### Fixed
- Favicon set: a real ICO at 16, 32 and 48 px (#45).
```

The other sections are `Removed` and, for a major, `Consumers must`. A section with nothing in it is left out.
