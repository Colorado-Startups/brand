# Art direction v4: the Hall, carved in Colorado: Prompts: FIBO 2.0 in VGL

Part 10 of 11 of [`DIRECTION.md`](../DIRECTION.md).

## Prompts: FIBO 2.0 in VGL

FIBO 2.0 reads one JSON caption with a field per concern, in Bria's Visual GenAI Language (VGL guide, Sources). The four templates in `art/prompts/` write the Hall's fixed fields once.

| Template | Kind | Node size | Calm area |
|---|---|---|---|
| [`hero.vgl.json`](../prompts/hero.vgl.json) | Home hero | 21:9 at 1MP | Upper-left third |
| [`scene.vgl.json`](../prompts/scene.vgl.json) | Region or town scene | 16:9 at 1MP or 4MP | Top quarter |
| [`keeper.vgl.json`](../prompts/keeper.vgl.json) | Keeper portrait | 3:4 at 1MP or 4MP | Around the head |
| [`tile.vgl.json`](../prompts/tile.vgl.json) | Texture tile | 1:1 at 1MP | All of it |

Node sizes come from the Bria node's settings (`get_node`, 2026-11-02, recorded in v3). Ratios wider than 16:9 render at 1MP only (same source).

**How a template works.** Each file wraps the caption in `structured_prompt`. `fixed` lists the fields written once, as JSON Pointers into `structured_prompt`; send them unchanged. `per_image` lists the fields each image writes, and their template values are `{braced}` notes. Send only `structured_prompt` to the node, because the model reads every key it receives (VGL guide, "Validate a caption").

**Caption rules** (VGL guide):

1. Describe, don't instruct. Write "founders laughing at a long table", never "make the founders laugh".
2. Always set `style_medium` and `artistic_style`. Without them a caption defaults to a photograph.
3. `artistic_style` holds 3 words at most.
4. `objects` holds 5 entries at most. Everything else goes in `background_setting`.
5. `text_render` stays empty, because the Hall's pictures carry no text.
6. Keep fields consistent: the light, the mood and the background describe the same scene.
7. Record the seed with every render. The same seed and caption recreate an image (the node's tooltip, recorded in v3).

**Edits.** FIBO 2.0 Edit, on `api_bria_image_edit`, fixes one thing at a time. Write `edit_instruction` as one imperative command that starts with a verb, such as "Remove the extra finger from the founder's left hand." The other fields describe the result. A mask holds the rest of the picture still and fixes drift in a keeper's look. The node takes `guidance_scale` from 3 to 5 and `steps` from 20 to 50 (`get_node`, recorded in v3).

## Motion

The LTX-2.5 rules live in [`art/motion.md`](../motion.md): animate only approved stills, muted short loops, the still as poster, a pause control, an AI-made label and kept provenance.
