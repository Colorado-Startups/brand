# Art direction v5: Colorado, transformed with magic: Prompts: FIBO 2.0 in VGL

Part 10 of 11 of [`DIRECTION.md`](../DIRECTION.md).

## Prompts: FIBO 2.0 in VGL

FIBO 2.0 reads one JSON caption with a field per concern, in Bria's Visual GenAI Language (VGL guide, Sources). The shipped prompts, for the five places and the three characters, live in `art/render/fibo_cards.py` (`PAINTED`, `STYLE`, `PLACE_STYLE`, `CHARACTERS`, `REFS`). They set `style_medium` and `artistic_style` directly and name the game, the film and the place (decision 44).

The four templates in `art/prompts/` write v4's fixed fields once, for the deferred hero, region, keeper and tile art. Their fixed look is v4's. When that art runs, the fixed `style_medium` and `artistic_style` change to the game look in Part 3.

| Template | Kind | Aspect ratio | Calm area |
|---|---|---|---|
| [`hero.vgl.json`](../prompts/hero.vgl.json) | Home hero | 21:9 at 1MP | Upper-left third |
| [`scene.vgl.json`](../prompts/scene.vgl.json) | Region or town scene | 16:9 at 1MP or 4MP | Top quarter |
| [`keeper.vgl.json`](../prompts/keeper.vgl.json) | Keeper portrait | 3:4 at 1MP or 4MP | Around the head |
| [`tile.vgl.json`](../prompts/tile.vgl.json) | Texture tile | 1:1 at 1MP | All of it |

The ratios and sizes are v3's settings for the Bria node (recorded in v3), kept as starting values. Ratios wider than 16:9 render at 1MP only (same source). The shipped place art and cards render at 1440 × 720 on the Space (`SIZE` in `art/render/fibo_cards.py`).

**How a template works.** Each file wraps the caption in `structured_prompt`. `fixed` lists the fields written once, as JSON Pointers into `structured_prompt`; send them unchanged. `per_image` lists the fields each image writes, and their template values are `{braced}` notes. Send only `structured_prompt` to FIBO, because the model reads every key it receives (VGL guide, "Validate a caption").

**Caption rules** (VGL guide):

1. Always set `style_medium` and `artistic_style`. Without them a caption defaults to a photograph.
2. `artistic_style` holds 3 words at most.
3. `objects` holds 5 entries at most. Everything else goes in `background_setting`.
4. `text_render` stays empty, because the name is composited after the render (decisions 37 and 46).
5. Keep fields consistent: the light, the mood and the background describe the same scene.
6. Record the seed with every render. The same seed and caption recreate an image (recorded in v3). `art/render/out/runs.json` logs each call.

**Edits.** Edits follow Bria's method (decision 41). Write `edit_instruction` as imperative commands that start with a verb, such as "Remove the extra finger from the founder's left hand." Bria's VGL step turns the instruction into a structured edit JSON, and `Fibo-2.0-edit-turbo` runs it. Place art uses one long instruction that repaints the whole photo (decision 43). A mask holds the rest of the picture still, and Bria allows a mask with one source image only, so a creature reference takes a second, unmasked pass (decision 42). Text to image runs 50 steps at guidance 5.0, and edits run 4 steps at guidance 1.0 (`STEPS`, `GUIDANCE`, `EDIT_STEPS` and `EDIT_GUIDANCE` in `art/render/fibo_cards.py`).

## Motion

The LTX-2.5 rules live in [`art/motion.md`](../motion.md): animate only approved stills, muted short loops, the still as poster, a pause control, an AI-made label in the file's metadata and kept provenance.
