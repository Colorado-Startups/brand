# Changelog

All notable changes to this repo are in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (`governance/releases.md`). Dates are Mountain Time, as in `decisions.md`. Every release's files and checksums are in its [GitHub release notes](https://github.com/Colorado-Startups/brand/releases).

## [Unreleased]

### Added
- `dist/brand.json`, the guide's data, built by `tools/build_guide_data.py` from `data/`, `tokens/type.yaml`, `research/color/state.yaml` and `TRADEMARKS.md` (#20, decision 47).
- The brand guide: 14 interactive sections at colorado-startups.github.io/brand/, rendered from `dist/brand.json` (#21, decision 47).
- `tools/franchise_gate.py --dir`, which `pages.yml` runs on the built `site/`, and 33 more franchise names in the `never` list of `data/words.yaml` (#22, decision 49).
- The logo in three tiers in `dist/logo/`: the emblem, the wordmark and the icon with its favicon set (#23, decision 50).
- Cards for `photon-mountain`, `space-peak`, `fusion-canyon` and `startup-credits`, composed from the committed place paintings (#23, decision 50).

### Changed
- The Claudius, Linken and Legallas cards are in the game style (#23, decision 50).
- `data/voice.yaml` boilerplates and glossary say "founders" (#20, decision 47).
- `TRADEMARKS.md` names the logo and the characters (#23, decision 50).

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

[Unreleased]: https://github.com/Colorado-Startups/brand/compare/v3.0.0-alpha.4...HEAD
[3.0.0-alpha.4]: https://github.com/Colorado-Startups/brand/compare/v3.0.0-alpha.3...v3.0.0-alpha.4
[3.0.0-alpha.3]: https://github.com/Colorado-Startups/brand/compare/v3.0.0-alpha.2...v3.0.0-alpha.3
[3.0.0-alpha.2]: https://github.com/Colorado-Startups/brand/compare/v3.0.0-alpha.1...v3.0.0-alpha.2
[3.0.0-alpha.1]: https://github.com/Colorado-Startups/brand/releases/tag/v3.0.0-alpha.1
