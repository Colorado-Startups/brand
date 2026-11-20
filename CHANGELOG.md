# Changelog

All notable changes to this repo are in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (`governance/releases.md`). Dates are Mountain Time, as in `decisions.md`. Every release's files and checksums are in its [GitHub release notes](https://github.com/Colorado-Startups/brand/releases).

## [Unreleased]

## [4.5.0] - 2026-11-20

Linken's repo moved from `Colorado-Startups/link` to `Colorado-Startups/linken`. Checksums for every file in `dist/` are in the GitHub release notes.

### Changed
- `data/world.yaml` `characters`: Linken's `repo` is `Colorado-Startups/linken`, also in `dist/brand.json` (#49). Sites that link a character's repo take the new one; the old URL redirects.
- Pins: Claudius v1.1.1 and Git Crafter v7.0.2 (#44, #45), and plugins, skills and connectors stay on app-wide (#46). Repo upkeep only: nothing in `dist/` changes for these.

## [4.4.0] - 2026-11-16

The brand's calls for the website engagement plan (decision 64), with the regions' new plain labels (decision 63). Checksums for every file in `dist/` are in the GitHub release notes.

### Added
- Region color tokens in `tokens/brand_tokens.yaml`, `dist/tokens.css` and `dist/tokens.json`: `region-photon-mountain`, `region-space-peak`, `region-fusion-canyon` and an `on-region-*` ink for each, with night values and 18 contrast pairs (#42, decision 64).
- `data/voice.yaml` `site_words`: "first steps", "honor card", the AI agents page at `/agents/` and "tallies", each with the words it never uses; four glossary terms and one do and don't pair, also in `dist/brand.json` (#42, decision 64).
- `data/world.yaml` `characters`: a disclosure line and an `agents_page` flag for Claudius, Linken and Legallas, also in `dist/brand.json`; Legallas is `false` until its repo is public (#42, decision 64).
- `data/world.yaml` `regions[].craft` and `art/render-queue.yaml` `places-v2`: place paintings v2, queued and not rendered (#42, decision 64).
- `art/LICENSES.md`: the Rive row (#42, decision 64).

### Changed
- Space Peak's plain label is "the Colorado Startups chapter for Colorado Springs and Fountain", and Fusion Canyon's drops Greeley, in `data/world.yaml`, `data/architecture.yaml`, the `region` glossary entry and `dist/brand.json` (#40, decision 63).
- `data/world.yaml` `regions.colors_status` and the crest `field` rule point to the region tokens (#42, decision 64).

## [4.3.0] - 2026-11-15

Theme clips for Fusion Canyon and Space Peak, with a still camera (decision 62). Checksums for every file in `dist/` are in the GitHub release notes.

### Added
- `dist/clips/fusion.webm`, `fusion.mp4`, `fusion.json`: a 4 s muted loop of the Fort Collins painting, teal cores pulsing and sparks drifting.
- `dist/clips/space.webm`, `space.mp4`, `space.json`: a 4 s muted loop of the Colorado Springs painting, stars and clouds shimmering, gryphon and gyrocopters in place.
- `art/render/ltx-space/`: the own ZeroGPU Space for LTX-2.5 with the Cinemagraph LoRA, and `ltx_clips.py cinemagraph`.

## [4.2.0] - 2026-11-15

The first theme clip for the website's region panels (decision 61). Checksums for every file in `dist/` are in the GitHub release notes.

### Added
- `dist/clips/photonics.webm`, `photonics.mp4`: a 4 s muted loop of the Boulder painting (Photon Mountain), with its provenance record `photonics.json`.
- `dist/brand.json` `downloads` lists `.webm` and `.mp4` files.
- The guide's site serves `dist/clips/`.

## [4.1.0] - 2026-11-15

One crest per region, in the master crest's loud clan style (decision 60). Checksums for every file in `dist/` are in the GitHub release notes.

### Added
- `dist/crests/photon-mountain-1024.png`, `-512.png`: fluorite violet, a white-and-gold light dragon.
- `dist/crests/space-peak-1024.png`, `-512.png`: Pikes Peak granite pink, a golden eagle under a white star.
- `dist/crests/fusion-canyon-1024.png`, `-512.png`: Stout sandstone red, a ring of fire in a canyon (the phoenix did not read at 48 px).

### Changed
- `dist/brand.json` lists the six crest files, and `dist/README.md` describes them.
- The guide's Family section shows the region crests in the region lockup and on the three region nodes.
- `data/world.yaml` `crests`: shipped; each crest keeps the master crest's frame and takes its region's field color and its own charge; the smallest crest is 32 px.

## [4.0.0] - 2026-11-15

No single Hall: the places are equals (decision 58). Checksums for every file in `dist/` are in the GitHub release notes.

### Changed
- **Breaking:** `dist/hall/` is now `dist/website/`, with the same file names.
- **Breaking:** in `dist/brand.json`, the register id `hall` is now `community`, and the lockup key `outpost` is now `region`. Architecture nodes `outpost-*` are now `region-*`, and the keepers sit under `colorado-startups`.
- The region lockup is "Colorado Startups · {Place}", with no "Outpost" (`naming.region-names`).
- Publicus is "Herald of Colorado Startups".

### Removed
- The Hall, as a place, a register name and a brand-tree node (`the-hall`).
- The Hall's rooms: the Great Hall of the Community, the Map Room, the Leaderboard gallery and the forge. Each website page takes its plain name.

## [3.2.0] - 2026-11-15

The logo as a loud clan crest, the banner that flies it, and Claudius's icon (decision 59). Checksums for every file in `dist/` are in the GitHub release notes.

### Added
- `dist/logo/banner-960x1200.png`, `banner-480x600.png`: the crest on a royal-blue war banner.
- `dist/logo/claudius-icon-1024.png`: Claudius's icon for the Claude Code plugin directory.

### Changed
- `dist/logo/emblem-512.png`, `emblem-1024.png` and `dist/templates/square-512.png`: the emblem is a loud winged crest in royal blue and gold, keeping the 2014 shield, the C and its peak.
- `dist/brand.json` and `dist/README.md` list the banner and the Claudius icon, and describe the new emblem.

## [3.1.1] - 2026-11-15

The two renders `v3.0.0` left open. Checksums for every file in `dist/` are in the GitHub release notes.

### Added
- `dist/hall/guides.jpg`: the guides scene, with a picture map that carries no writing (decision 57).

### Fixed
- The `coloradostartups.org` card, which `.github` reuses: the dragons no longer sit on the name, and the sky behind it is open (decision 57).
- Decision 53's spend record: per HF's billing page, 2 min 47 s past the ZeroGPU quota cost $0.28 of the included credit (decision 57).

## [3.1.0] - 2026-11-15

The State's latest guidance (decision 56).

### Added
- `--co-web-*` in `dist/tokens.css` and `palette.web` in `dist/tokens.json`: the State's 22 web color steps from its Digital Guidelines 1.8.
- Atkinson Hyperlegible (SIL OFL 1.1) as the `body` type role, shipped in `guide/public/fonts/` with its licence.

### Changed
- `research/color/state.yaml` cites the State's live brand pages, read 2026-11-15, in place of the 2024 PDF; the primaries are unchanged.
- The guide's body text is set in Atkinson Hyperlegible, with Trebuchet MS as the fallback.

## [3.0.0] - 2026-11-14

The brand overhaul's first full release: the guide, the logo, tokens, the Hall art, templates and every public repo branded. Checksums for every file in `dist/` are in the GitHub release notes.

### Added
- `governance/audit/after.yaml`: the surfaces this work changed, scored on the rubric against `v3.0.0-alpha.5`. Overall 1.77 over 118 scores, against the before-audit's 1.50 (decision 55).
- The emblem beside the name in the guide's header (decision 55).

### Changed
- Every social card has a soft navy fade behind the name, so white type keeps at least 3:1 on a pale sky (decision 55).
- The icon and favicon set are State Blue #001970 (decision 55).
- The guide's control borders, panels and muted text take their colours from `dist/tokens.css` (decision 55).

## [3.0.0-alpha.5] - 2026-11-14

The finish plan's kit.

### Added
- `dist/brand.json`, the guide's data, built by `tools/build_guide_data.py` from `data/`, `tokens/type.yaml`, `research/color/state.yaml` and `TRADEMARKS.md` (#20, decision 47).
- The brand guide: 14 interactive sections at colorado-startups.github.io/brand/, rendered from `dist/brand.json` (#21, decision 47).
- `tools/franchise_gate.py --dir`, which `pages.yml` runs on the built `site/`, and 33 more franchise names in the `never` list of `data/words.yaml` (#22, decision 49).
- The logo in three tiers in `dist/logo/`: the emblem, the wordmark and the icon with its favicon set (#23, decision 50).
- Cards for `photon-mountain`, `space-peak`, `fusion-canyon` and `startup-credits`, composed from the committed place paintings (#23, decision 50).
- Tokens v3: `tokens/brand_tokens.yaml` built into `dist/tokens.css` and `dist/tokens.json`, the State palette in the website's role names (#24, decision 51).
- `dist/hall/`: the three keepers, the passage and founders scenes and the stone tile, for the website (#27, decision 53).
- Four templates in `dist/templates/` by `templates/build.py`; the favicon set and a web manifest on the guide's site (#28, decision 54).
- Each place's people, creature and mount in `data/world.yaml`, shown in the guide's World section (#26, decision 52).
- Org repo branding: custom previews, the `colorado-startups` topic and a guide link on all nine public repos; the org profile shows the emblem (decision 50).

### Changed
- The Claudius, Linken and Legallas cards are in the game style (#23, decision 50).
- `data/voice.yaml` boilerplates and glossary say "founders" (#20, decision 47).
- `TRADEMARKS.md` names the logo and the characters (#23, decision 50).
- The guide meets its word goal, 817 visible words on first load, with detail behind controls (#26, decision 52).
- `dist/tokens.css` styles the guide and its 404 page; the hand-copied `guide/public/tokens.css` is gone (#28, decision 54).
- 25 docs say what decisions 37 to 50 say (#25).

## [3.0.0-alpha.4] - 2026-11-14

The seed-51 places and cards, with no taglines and no text on the images. Supersedes alpha.3's places and every card.

### Changed
- All five `dist/places/*.jpg` and all five `dist/social/*.jpg` are the seed-51 renders (#17, #18, decisions 44 and 45).
- Each image keeps its AI-made label (IPTC `DigitalSourceType`) and its photo credit (`csart:Source`) in its metadata (#19, decision 46).

### Removed
- The text chip on every image, and every tagline: each card shows only its name (#19, decision 46).

## [3.0.0-alpha.3] - 2026-11-14

Game-style place art and the Boulder and Golden cards. Supersedes alpha.2's cards for `coloradostartups.org` and `brand`; the character cards are unchanged.

### Added
- `dist/places/boulder.jpg`, `golden.jpg`, `denver.jpg`, `springs.jpg` and `fortcollins.jpg` (#16, decision 43).

### Changed
- `dist/social/coloradostartups.org.jpg` and `dist/social/brand.jpg` use the Boulder and Golden place art (#16, decision 43).
- Place art starts from scratch on Bria's prompting method, and Bria's free credit stops at $6.00 (#15, decision 42).
- FIBO 2.0 renders on an own ZeroGPU Space first and on Modal second (#14, decision 41).
- Claudius is a gnome, and each place also blends a Middle-earth place (#13, decision 40).

## [3.0.0-alpha.2] - 2026-11-13

FIBO 2.0 art. Supersedes alpha.1's rejected vector cards.

### Added
- `dist/social/claudius.jpg`, `link.jpg` and `legallas.jpg`: one character card for each project repo (#12, decision 39).

### Changed
- `dist/social/coloradostartups.org.jpg` and `brand.jpg` are FIBO 2.0 images, labelled AI-made on the image and in IPTC metadata (#12, decision 39).
- All artwork is FIBO 2.0, video is LTX-2.5 and image motion is Rive (#10, decision 37).
- The brand's own rules are deleted; what binds is Paul's calls, the house rules and the law (#11, decision 38).
- Dependabot pull requests follow the normal merge path (#9, decision 36).
- `anthropics/claude-code-action` is 1.0.265 (#1).

### Removed
- The vector cards `dist/social/brand.png` and `dist/social/coloradostartups.org.png` (#10, decision 37).

## [3.0.0-alpha.1] - 2026-11-13

The first public release (decision 28). A pre-release: the v3 tokens, logo and guide were still to come.

### Added
- Social cards, 1280 × 640: `dist/social/brand.png` and `dist/social/coloradostartups.org.png` (#8).
- The State of Colorado palette reference, `research/color/state.yaml` (#3, decision 29).
- Brand data: strategy, architecture, world, voice and words, in `data/`.
- A guide placeholder on the State tokens (#7).
- FIBO 2.0 on Bria's Free plan, capped at 2,000 calls a month (#5, decision 35).

### Changed
- Long docs are in parts, and READMEs are tables (#6).
- `actions.lock` holds SHA refs, as the workflows pin them (#4).
- Quick wins from the first Quality read (#2).

[Unreleased]: https://github.com/Colorado-Startups/brand/compare/v3.1.1...HEAD
[3.1.1]: https://github.com/Colorado-Startups/brand/compare/v3.1.0...v3.1.1
[3.1.0]: https://github.com/Colorado-Startups/brand/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/Colorado-Startups/brand/compare/v3.0.0-alpha.5...v3.0.0
[3.0.0-alpha.5]: https://github.com/Colorado-Startups/brand/compare/v3.0.0-alpha.4...v3.0.0-alpha.5
[3.0.0-alpha.4]: https://github.com/Colorado-Startups/brand/compare/v3.0.0-alpha.3...v3.0.0-alpha.4
[3.0.0-alpha.3]: https://github.com/Colorado-Startups/brand/compare/v3.0.0-alpha.2...v3.0.0-alpha.3
[3.0.0-alpha.2]: https://github.com/Colorado-Startups/brand/compare/v3.0.0-alpha.1...v3.0.0-alpha.2
[3.0.0-alpha.1]: https://github.com/Colorado-Startups/brand/releases/tag/v3.0.0-alpha.1
