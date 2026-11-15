# Art direction v5: Colorado, transformed with magic: Renders and runs

Part 11 of 11 of [`DIRECTION.md`](../DIRECTION.md).

## Renders and runs

Every render the brand needs is in [`art/render-queue.yaml`](../render-queue.yaml), by status: done, in progress or deferred.

| Route | How | Limit |
|---|---|---|
| 1. The own ZeroGPU Space `paul-co-startups/brand-fibo` | `python3 art/render/fibo_cards.py <entry>` (decision 41) | HF PRO's 40 daily minutes, then the included $2.00 credit, then stop |
| 2. Modal | `modal run art/render/fibo_cards.py::<entry>` | The included monthly credit |
| 3. Bria's hosted credit | Not wired yet (decision 42) | $6.00 of the $7.00 free credit, enforced by `tools/fibo_budget.py reserve-bria` |

- Money and lanes are in `art/LICENSES.md`. Run `python3 tools/fibo_budget.py reserve N` before each batch. The calls count against 1,950 a month.
- The finish plan renders on one standing yes (decision 48): at most 60 FIBO calls on route 1, then stop, with $0 billed. Any other batch waits for Paul's yes in chat, with its estimate. Balances are read before and after each batch.
- Nothing renders on this Mac. `~/.claude/rules/compute.md` sets cloud first.
- Each render keeps a provenance record: model, route, seed, caption, date, who approved it, and the lane's balances before and after. `art/render/out/runs.json` logs every call.
- Every shipped image and clip carries an AI-made label in its metadata and keeps its provenance (decisions 8 and 46).

## Texture tiles

The tiles are `stone`, `parchment` and `night-stone`: 512 × 512 WebP files that repeat with no visible seam (v3, Texture tiles). The token file's `texture` block sets each tile's floor and ceiling roles. The website's `make-tiles.mjs` maps each tile's luminance between those roles. So a new palette regrades a tile without a new render. A new tile uses `tile.vgl.json`.

## Files

| Path | What it holds |
|---|---|
| `art/DIRECTION.md` | This file |
| `art/prompts/*.vgl.json` | FIBO 2.0 VGL templates for the deferred art, with fixed and per-image fields marked |
| `art/keepers/*.yaml` | One fixed sheet per keeper, with its disclosure |
| `art/motion.md` | LTX-2.5 motion and video rules |
| `art/LICENSES.md` | The license register: model, route, verdict and duties |
| `art/render-queue.yaml` | Every render the brand needs, by status |
| `art/render/` | The render client, the Space's source and the run log |
| `dist/places/`, `dist/social/`, `dist/logo/` | The shipped place art, cards and logo |

## Sources

Read 2026-11-02 unless noted.

| Source | Used for |
|---|---|
| `baseline/v2/art-DIRECTION.md` (v3), `baseline/v2/lore.md`, `baseline/v2/dwarves.yaml` | Vocabulary, rooms, towns, keepers, node settings, tile contract |
| The website's `art/DIRECTION.md` at commits `13c6b52` and `e628748` | Motion rules and the reference-image rule |
| The website's `art/concepts/batch-1.md` (`origin/main` `c6f10bc`) | Shipped keeper picks and their 64 px measurements |
| [FIBO 2.0 VGL guide](https://huggingface.co/briaai/Fibo-2.0-dev/blob/main/vgl/README.md) | Caption fields and rules |
| [Bria's VGL docs](https://docs.bria.ai/vgl), `Bria-AI/vgl` best practices, and the `briaai/Fibo-2.0-dev` and `-edit-turbo` model cards (read 2026-11-14) | The prompting and edit method (decision 42) |
| [Fountain Formation](https://en.wikipedia.org/wiki/Fountain_Formation), Wikipedia | Red sandstone of the Flatirons, Red Rocks and Garden of the Gods |
| [Pikes Peak granite](https://en.wikipedia.org/wiki/Pikes_Peak_granite), Wikipedia | Coarse pink to brick-red granite of Pikes Peak |
| [Golden, Colorado](https://en.wikipedia.org/wiki/Golden,_Colorado), Wikipedia | Clear Creek, the Table Mountains, the School of Mines, the 1859 gold rush |
| [Mount Zion (Colorado)](https://en.wikipedia.org/wiki/Mount_Zion_(Colorado)), Wikipedia | The "M" and the freshman rock ritual |
| [Manitou Springs, Colorado](https://en.wikipedia.org/wiki/Manitou_Springs,_Colorado), Wikipedia | The mineral springs and the Ute |
| [Fort Collins, Colorado](https://en.wikipedia.org/wiki/Fort_Collins,_Colorado), Wikipedia | The Cache la Poudre, Old Town, Horsetooth Mountain |
| [Greeley, Colorado](https://en.wikipedia.org/wiki/Greeley,_Colorado), Wikipedia | The High Plains and the two rivers' confluence |
