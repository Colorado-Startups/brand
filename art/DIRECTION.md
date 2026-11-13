# Art direction v4: the Hall, carved in Colorado

*S7, 2026-11-02. Rebuilt for the brand overhaul from v3 (`baseline/v2/art-DIRECTION.md`, the website's `art/DIRECTION.md` at `18b65a6`).*

**Precedence.** `decisions.md` wins over this file, and the house rules in `~/.claude/rules/` win on Comfy spend and on writing. `art/LICENSES.md` wins on which model route is allowed. `baseline/v2/dwarves.yaml` wins on who each keeper is. `tokens/brand_tokens.yaml` wins on every color value. Once `data/world.yaml` (S2) lands, it wins on towns, outposts and the influence map. If any of them disagree with this file, fix this file in the same session.

## The idea

Colorado's founders build their companies in the Hall, a bright forge-kingdom carved into the Front Range. Inside are carved granite halls, warm hearths, molten-gold channels, brass gnome workshops and round hot-spring terraces lit from below. Outside the open bronze doors are the real towns of the Front Range and the plains. Every picture is painted in a few chunky shapes, warm and bright. Founders and Colorado lead every wide image. Dwarves and gnomes keep the place and never take the headline.

## What changed from v3

| v3 (2026-10-18) | v4 (this file) |
|---|---|
| Colors named by hex | Colors named by token role only. Wave 2 (S12) sets the values |
| The influences stated as a mood | Seven rules from the influence map, each with what to paint and what never to paint |
| Anima prompt files in `.txt` | FIBO 2.0 VGL templates in `art/prompts/*.vgl.json`, with the fixed fields marked |
| Each keeper described anew in each prompt | One fixed sheet per keeper in `art/keepers/`, pasted verbatim into every caption |
| Motion rules dropped by a website merge | Restored and extended in `art/motion.md` |
| The towns in `lore.md` | Those towns plus Golden with the Colorado School of Mines, Fort Collins and Greeley |
| No rule for reference pictures | No borrowed pictures, reference images included |

## The influence map, as rules

The brand mixes three named influences (decision 30). Each gives a mood, a material or a light. None gives a name, emblem, silhouette, iconic item, script, rune, costume or picture. Shipped files use only the generic phrase.

| Influence | Owner | Generic phrase (what ships) | Taken | Never |
|---|---|---|---|---|
| World of Warcraft: Ironforge, its dwarves and gnomes | Blizzard Entertainment | a fantasy MMO's dwarves and gnomes and their forge city | chunky painterly shapes; a hall around a great forge; brass-and-gear tinkering | names, gates, halls, banners, emblems, costumes, machines |
| The Lord of the Rings: the dwarves' mountain halls and mines | the Tolkien Estate | high fantasy's mountain dwarves | straight-line carved ornament; monumental symmetry; gold set in cool stone | runes, scripts, named halls, doors, gates, map style, heraldry |
| The Legend of Zelda: Ocarina of Time, the fire mountain | Nintendo | a classic adventure game's fire mountain and its town | round terraces around a glowing center; ember light from below | the emblem, the rock folk, an erupting volcano, the town's layout |

Each trait below becomes a Colorado translation and a rule a painter can follow.

| Trait, in generic words | Colorado translation | Rule | Lands in |
|---|---|---|---|
| The forge city's few, chunky, painterly shapes | Tilted slabs of red Fountain Formation sandstone; coarse pink Pikes Peak granite | 1 | Every image, every silhouette |
| The forge city's halls carved around a central forge | Mine tunnels, headframes and stamp mills from the 1859 gold rush | 2 | Heroes, region scenes, dividers |
| The gnome city's brass, gears and steam | Mine hoists, cog railways and assay gear, as in Golden and at the School of Mines | 3 | Resourcus, workshops, loading art |
| The fire mountain's round terraces around a glowing center | Terraced hot-spring pools; ember light on red rock | 4 | The mountain's heart, accent light, motion |
| High fantasy dwarves' straight-line carved ornament | Claim-stake ticks and survey cuts | 5 | Door relief, borders, badges |
| High fantasy dwarves' gold set into cool stone | Aspen gold on a granite slope | 6 | Palette, honors, trim |
| All three: grand, warm and lit | The Front Range at golden hour | 7 | Every image |

Sources for the Colorado column: Fountain Formation and Pikes Peak granite (Sources, below); the gold rush from Golden's founding "during the Pike's Peak gold rush" in 1859 (Wikipedia, Golden).

### 1. Chunky, few-shape, painterly

- Build each picture from two or three large shapes, not five small ones (a goal for every image).
- Proportions are sturdy and exaggerated: big hands, broad shoulders, thick beards, heavy boots, wide doors.
- Every main figure reads as a filled silhouette at thumbnail size. For keepers that size is 64 px (a goal).
- Paint with thick confident outlines, visible brush texture and soft cel shading.
- **Never:** fine filigree, thin spikes, photo detail, the gloss of a 3D render, a busy pattern behind a face.

### 2. Carved halls and mining heritage

- Halls are cut from granite and red sandstone: soaring arches, squared pillars, long stairs, stone bridges over lit channels.
- Timber shoring, headframes, ore carts, stamp mills and mine lifts carry the gold rush into the Hall.
- The carving is clean and cared for, and every hall is lit.
- **Never:** a dark mine, a dungeon, a cave, a collapse, a fortress wall, a cage.

### 3. Gnome brass and steam

- Gnomes build with brass and wrought iron: gears, gauges, survey compasses, orreries, small hoists, cog railways.
- Steam shows as thin white threads. It never hides a face.
- The tone is comic and competent: tidy benches, clever gadgets that work.
- **Never:** soot, grime, rust heaps, explosions, weapons, or any game's machines, mounts or vehicles.

### 4. Round terraces and safe underglow

- The mountain's heart is a set of round stepped pools inside the Hall, around a warm glowing center, with brass rails and soft steam.
- Underglow is warm light rising from below. Pools, molten-gold channels and hearths light faces and walls from underneath.
- The glow is always contained and calm, and people rest or work beside it.
- These pools belong to the Hall. Real springs outside the doors are shown as they are, or left out (Real places, below).
- **Never:** a crater, an eruption, a lava flow, danger, hellish red, or a dot-in-a-circle emblem.

### 5. Straight-line carved ornament

- Ornament is straight cuts only: chevrons, stepped bands, parallel grooves, claim-stake ticks and survey crosses.
- It sits in stone lintels, bronze door relief, borders and badges, in mirror symmetry.
- Ornament never forms a letter or a word, or anything that reads as an alphabet, real or invented.
- The brand mark is never painted into a picture. It comes from `logo/` and is set in HTML.
- **Never:** runes, any existing or invented script, the heraldry of any real house.

### 6. Gold set in granite

- Warm gold (the `accent` and `molten` roles) sits inlaid in cool pink-grey granite (the `stone` and `stone-edge` roles), like aspens on a granite slope.
- Stone fills most of a picture. Gold is trim, light and inlay, at most about a tenth of the area (a goal).
- **Never:** gold everywhere, gold as a flat background, chrome or silver as the main metal.

### 7. Composition, value, temperature and room for type

- **Colorado first.** Every wide image shows something a Coloradan recognizes.
- **Founders lead.** In a wide shot the focal point is people building something. Keepers and Hall folk support it, a few per image at most.
- **Grand but welcoming.** Big architecture, open doors, warm light.
- **Value.** Most of each image sits in the light half of the value range. The darkest value is warm bronze (the `text` role), never black or navy. A viewer says "bright" or "glowing" first.
- **Temperature.** Warm key light from a low sun, a lantern or a hearth, with one cool note: Colorado sky (the `community` role). No green or purple cast on faces.
- **Room for type.** Heroes keep the upper-left third calm. Region and town scenes keep the top quarter calm. Keeper portraits keep clear space around the head for a round crop. Texture tiles stay calm throughout.
- **One look.** Every image uses the same fixed VGL fields (Prompts, below).
- **No text, no runes, no weapons.**

## Palette by token role

The art lands in the same colors as the UI, so a picture and the page around it read as one surface. This file names roles only. `tokens/brand_tokens.yaml` sets every value, and Wave 2 (S12) changes values without renaming a role (the plan's S12 row). FIBO 2.0 reads words, not color codes, so the fixed `color_scheme` field carries the palette in plain color words.

**Color words follow the roles.** The templates' `color_scheme` and each keeper's color words describe the roles' current values. Wave 2 picks the v3 values by an evidence-based method, so no hue is fixed here. When those values land, update the words to match, by role, in the same change.

| Role | Where it shows in the art |
|---|---|
| `ground` | Sky near the sun, the brightest lit walls |
| `surface` | Lit stone, paper, pools of lamplight, and the flat ground behind keeper portraits |
| `surface-2` | Carved sandstone in light, warm haze |
| `stone`, `stone-edge` | Granite faces and their carved edges |
| `accent`, `molten` | Lantern flames, molten gold, gilded trim |
| `fire` | Hearths, sparks, underglow, Publicus |
| `link` | Copper fittings, red sandstone in shade |
| `bronze`, `bronze-deep` | Hammered bronze doors, pillars and rails |
| `brass` | Gnome gears, gauges and instruments, Resourcus |
| `text` | The darkest value in any image: deep warm shadow and line art |
| `community` | The one cool note: high sky, Communitas |
| `pine` | Evergreens and Resourcus, used sparingly |
| `night`, `night-ceiling` | The night-stone tile only |

Two art colors have no role: aspen gold (autumn aspens, banners) and alpenglow rose (snow on the high peaks at sunset). The art names them in words. If Wave 2 makes either one a UI color, the file that does so states that it reverses website decision 90.

## Inside the doors: the Hall

The rooms come from `baseline/v2/lore.md`: the Great Hall of the Community, the Map Room, the Leaderboard gallery and the forge. Paint from this list, so every image reads as one place.

| Element | Paint | Never |
|---|---|---|
| Halls | Granite and red sandstone carved into soaring arches, thick timber beams, hammered bronze pillars | A cave, a dungeon, a dark mine |
| Hearths and forges | Huge stone hearths with warm, contained fire | Smoke-black walls, hellish fire |
| Molten gold | Glowing channels in the floor behind brass rails, giving light | Lava flows, danger |
| Doors | Tall hammered bronze doors with straight-line relief, set in a cliff and standing open | Runes, inscriptions, locked gates |
| Banners | Gold, ember and sky blue, with a plain mountain or sun shape at most | Lettering, heraldry from any real house |
| Gnome workshops | Rule 3 | Rule 3 |
| The mountain's heart | Rule 4 | Rule 4 |
| The Leaderboard gallery | Carved plaques for companies, left blank | Names or numbers painted in: a real ranking comes from verified data and is set in HTML |
| Mountain folk | Dwarves and gnomes only: hearty, cheerful, quick to share a meal at long tables | A folk made of living rock, or any game's creature |
| Founders | People of mixed ages and backgrounds in casual Colorado clothes, with laptops, sketches and prototypes | Suits in a boardroom |

## Outside the doors: the towns

The great doors open onto real towns (`lore.md`). The forge is inside; outside is the town square, where founders meet their neighbors. The towns look like Colorado: brick and timber main streets, stone-and-timber cottages with steep roofs for snow, mine headframes, plains windpumps, footbridges over the creeks and aspens in the square. Dwarves and gnomes visit from the Hall. The townsfolk are founders and their neighbors.

| Town | Outpost | What a Coloradan recognizes | Never |
|---|---|---|---|
| Boulder | Photon Mountain | The Flatirons: tilted slabs of red Fountain Formation sandstone above the town; Boulder Creek and its footbridges | The Flatirons drawn as a logo shape |
| Golden | Photon Mountain | Clear Creek running through town at the base of the Front Range, between the two Table Mountains; the Colorado School of Mines; gold-rush storefronts and headframes on the hills | The "M" on Mount Zion. It is a letter, and pictures carry no text, so it lives in the ritual (`data/world.yaml`), not in paint |
| Denver | Photon Mountain | City lights and the skyline on the plain, seen from the foothills; brick warehouses | Readable signs |
| Colorado Springs | Space Peak | Pikes Peak over the city, in coarse pink to brick-red granite; the cog railway | Garden of the Gods as decoration (Real places) |
| Manitou Springs | Space Peak | A Victorian main street at the foot of Pikes Peak; its public mineral springs, as they are | Hall glow, steam or carving added to its springs |
| Fort Collins | Fusion Canyon | Old Town by the Cache la Poudre River; the tooth-shaped granite of Horsetooth Mountain on the western skyline | A canyon setting: Fusion Canyon is "named for the canyon, built on the plain" (Paul's rule, v3) |
| Greeley | Fusion Canyon | A farm town on the High Plains where the Cache la Poudre meets the South Platte; wide sky, windpumps, the Front Range low in the west | Desert |

Arvada, Loveland and Windsor follow the same rules. `data/world.yaml` (S2) lists every town. Facts in this table come from the Sources below.

## Real places

1. Real places are shown as they are, warm and lit, so someone who lives there knows them.
2. Places that matter to the Ute and other tribes are never fantasy decoration. Garden of the Gods is one. Manitou Springs' mineral springs are another: the Ute drank from them for years before visitors came (Wikipedia, Manitou Springs).
3. No Hall door, glow, keeper, banner or carving goes in or on such a place. Show it as it is, or leave it out.
4. Hall doors open in an unnamed cliff near a landform. They are never cut into a named landmark's face.
5. Built places carry no shop names, brands or readable signs, and no real person appears. This is the clearance the LTX Acceptable Use Policy asks for (`art/LICENSES.md`).
6. Each scene picks one real town or region and stays true to it: Pikes Peak never stands behind Boulder.

## No borrowed pictures

1. No picture from a game, film, show or comic is ever an input. That rules out reference images, edit sources, style samples and first or last frames.
2. The rule covers every image input: FIBO 2.0 Inspire and multi-image edits, masked edits, and LTX-2.5 image-to-video, first-and-last-frame and IC-LoRA inputs.
3. The only allowed inputs are the Hall's own approved art and masks drawn for it.
4. No photo of a real person is an input, and no keeper looks like a real person.
5. No franchise, character, artist or studio name appears in a caption, file name, alt text, metadata or negative prompt. The banned list is `data/words.yaml` `never` (S3).

## The keepers

Each keeper has one fixed sheet. Paste its `objects_entry` verbatim into every caption that shows it; only `location` and `relationship` change per image.

| Sheet | Kind | Anchor role | Prop |
|---|---|---|---|
| [`keepers/communitas.yaml`](keepers/communitas.yaml) | Dwarf | `community` | A brass lantern on a short pole, and a ring of brass keys |
| [`keepers/resourcus.yaml`](keepers/resourcus.yaml) | Gnome | `pine`, with `brass` | A brass surveyor's compass over a painted Front Range map |
| [`keepers/publicus.yaml`](keepers/publicus.yaml) | Dwarf | `fire` | A blank broadsheet held high, and a satchel of letters |

- **Disclosure.** Every keeper is an AI agent. Its picture ships beside the sheet's `disclosure`, set in HTML and never painted in. Its alt text follows the sheet's `alt_text`, which says so too.
- **Anchors by role.** Each anchor is a token role, and its color words follow that role's value. A render's painted anchor is checked against the role. The shipped Communitas cloak painted near 187 degrees, while the `community` token sat at 212 degrees (website `art/finals.json`).
- **Apart at 64 px.** Each keeper reads apart by color anchor and silhouette at 64 px (a goal). The website's make-finals tool measures the anchor's share, with a goal of 8% (website `art/concepts/batch-1.md`).
- **Two crops.** A large half-body crop at 4:5 and a small head-and-shoulders crop at 1:1. Goal sizes are 960 × 1200 and 320 × 320 (v3, Portrait files).

## Prompts: FIBO 2.0 in VGL

FIBO 2.0 reads one JSON caption with a field per concern, in Bria's Visual GenAI Language (VGL guide, Sources). The four templates in `art/prompts/` write the Hall's fixed fields once.

| Template | Kind | Node size | Calm area |
|---|---|---|---|
| [`hero.vgl.json`](prompts/hero.vgl.json) | Home hero | 21:9 at 1MP | Upper-left third |
| [`scene.vgl.json`](prompts/scene.vgl.json) | Region or town scene | 16:9 at 1MP or 4MP | Top quarter |
| [`keeper.vgl.json`](prompts/keeper.vgl.json) | Keeper portrait | 3:4 at 1MP or 4MP | Around the head |
| [`tile.vgl.json`](prompts/tile.vgl.json) | Texture tile | 1:1 at 1MP | All of it |

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

The LTX-2.5 rules live in [`art/motion.md`](motion.md): animate only approved stills, muted short loops, the still as poster, a pause control, an AI-made label and kept provenance.

## Renders and runs

- Every render the brand needs is in [`art/render-queue.yaml`](render-queue.yaml). Each runs on the $0 lanes in `art/LICENSES.md` after Paul's yes per batch. FIBO stills also wait for his billing call on Bria's Free plan.
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
