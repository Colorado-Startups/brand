# Art direction v4: the Hall, carved in Colorado: Renders and runs

Part 11 of 11 of [`DIRECTION.md`](../DIRECTION.md).

## Renders and runs

- Every render the brand needs is in [`art/render-queue.yaml`](../render-queue.yaml). Each runs on the $0 lanes in `art/LICENSES.md` after Paul's yes per batch. FIBO stills also wait for his billing call on Bria's Free plan.
- Until both clear, the brand uses the shipped art, regraded, plus SVG and CSS (decision 14).
- Run tiers follow `~/.claude/rules/compute-detail.md`. Stills on the Bria nodes are tier 3; clips and upscales are tier 2. Nothing renders on this Mac.
- Each render keeps a provenance record: model, route, node or template, seed, caption, date, who approved it, and `comfy cloud status` before and after.
- Every shipped image and clip carries an AI-made label and keeps its provenance (decision 8).

## Texture tiles

The tiles are `stone`, `parchment` and `night-stone`: 512 × 512 WebP files that repeat with no visible seam (v3, Texture tiles). The token file's `texture` block sets each tile's floor and ceiling roles. The website's `make-tiles.mjs` maps each tile's luminance between those roles. So a new palette regrades a tile without a new render. A new tile uses `tile.vgl.json`.

## Files

| Path | What it holds |
|---|---|
| `art/DIRECTION.md` | This file |
| `art/prompts/*.vgl.json` | FIBO 2.0 VGL templates, with fixed and per-image fields marked |
| `art/keepers/*.yaml` | One fixed sheet per keeper, with its disclosure |
| `art/motion.md` | LTX-2.5 motion and video rules |
| `art/LICENSES.md` | The license register: model, route, verdict and duties |
| `art/render-queue.yaml` | Every render the brand needs, with route, tier, estimate and status |
| `art/renders/` | Approved renders and their provenance, if Wave 2's S14 runs |

## Sources

Read 2026-11-02 unless noted.

| Source | Used for |
|---|---|
| `baseline/v2/art-DIRECTION.md` (v3), `baseline/v2/lore.md`, `baseline/v2/dwarves.yaml` | Vocabulary, rooms, towns, keepers, node settings, tile contract |
| The website's `art/DIRECTION.md` at commits `13c6b52` and `e628748` | Motion rules and the reference-image rule |
| The website's `art/concepts/batch-1.md` (`origin/main` `c6f10bc`) | Shipped keeper picks and their 64 px measurements |
| [FIBO 2.0 VGL guide](https://huggingface.co/briaai/Fibo-2.0-dev/blob/main/vgl/README.md) | Caption fields and rules |
| [Fountain Formation](https://en.wikipedia.org/wiki/Fountain_Formation), Wikipedia | Red sandstone of the Flatirons, Red Rocks and Garden of the Gods |
| [Pikes Peak granite](https://en.wikipedia.org/wiki/Pikes_Peak_granite), Wikipedia | Coarse pink to brick-red granite of Pikes Peak |
| [Golden, Colorado](https://en.wikipedia.org/wiki/Golden,_Colorado), Wikipedia | Clear Creek, the Table Mountains, the School of Mines, the 1859 gold rush |
| [Mount Zion (Colorado)](https://en.wikipedia.org/wiki/Mount_Zion_(Colorado)), Wikipedia | The "M" and the freshman rock ritual |
| [Manitou Springs, Colorado](https://en.wikipedia.org/wiki/Manitou_Springs,_Colorado), Wikipedia | The mineral springs and the Ute |
| [Fort Collins, Colorado](https://en.wikipedia.org/wiki/Fort_Collins,_Colorado), Wikipedia | The Cache la Poudre, Old Town, Horsetooth Mountain |
| [Greeley, Colorado](https://en.wikipedia.org/wiki/Greeley,_Colorado), Wikipedia | The High Plains and the two rivers' confluence |
