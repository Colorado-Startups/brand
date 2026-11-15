# dist

| Item | Value |
|---|---|
| Built by | `tools/` |
| Rebuilt | In every PR that changes a source |
| Guard | The drift check blocks a stale `dist/` (decision 21) |
| Pulled by | Consumers, at a release tag (decision 10) |

## Guide data (`brand.json`)

Everything the [brand guide](https://colorado-startups.github.io/brand/) shows, one top-level key per line, with each image's sha256. Built by `tools/build_guide_data.py` (decision 47).

## Tokens (`tokens.css`, `tokens.json`)

The design tokens, built by `tools/build_guide_data.py` from `tokens/` (decision 51). The State of Colorado palette leads; every role name, space, radius, line and size value is the website's v2.

| File | Holds |
|---|---|
| `tokens.css` | `:root` custom properties (`--co-*` State primaries, `--co-web-*` the State's 22 web steps (decision 56), `--c-*` roles, `--s-*`, `--r-*`, `--line-*`, `--size-*`, `--sh-*`, `--t-*`), then the night set under `prefers-color-scheme: dark` and `[data-theme="dark"]` |
| `tokens.json` | The same tokens in the Design Tokens format (DTCG 2025.10), with each role's night value and contrast records in `$extensions` |

## Social cards (`social/`, 1280×640 JPEG)

Every card is AI-made with FIBO 2.0 (decision 37) and shows only its name: no tagline (decision 46). The AI-made label and photo credit are in its IPTC metadata (decisions 8 and 46). Built by `art/render/fibo_cards.py` (decision 39); photo sources in `art/render/src/SOURCES.md`.

| Card | Image | Credit |
|---|---|---|
| `coloradostartups.org.jpg` | Boulder: the Flatirons transformed into an elven city of waterfalls, moon portals and a great tree, with dragons; open sky behind the name (decision 57) | Photo by Jimbo Herndan, [public domain](https://commons.wikimedia.org/wiki/File:Flatirons_2007.jpg) |
| `brand.jpg` | Golden: Table Mountain transformed into a dwarven kingdom's forge gate, with steam carts and a boulder wyrm | Photo by James St. John, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) ([source](https://commons.wikimedia.org/wiki/File:Lava_flows_capping_North_Table_Mountain_%26_South_Table_Mountain_(Denver_Formation,_Upper_Cretaceous;_Golden,_Colorado,_USA).jpg)), edited |
| `claudius.jpg` | Claudius, a gnome engineer and loyal companion, in the game style (decision 50) | AI-made, no photo |
| `link.jpg` | Linken, a gnome hero, in the game style | AI-made, no photo |
| `legallas.jpg` | Legallas, an elf ranger, in the game style | AI-made, no photo |
| `photon-mountain.jpg` | The Denver painting, for the photon-mountain repo | Photo by USFWS Mountain-Prairie, [public domain](https://commons.wikimedia.org/wiki/File:Denver_Skyline_(15242286069).jpg) |
| `space-peak.jpg` | The Colorado Springs painting, for the space-peak repo | Photo by Huttarl, [CC BY 2.5](https://creativecommons.org/licenses/by/2.5/) ([source](https://commons.wikimedia.org/wiki/File:Pikes_Peak_from_CO_Springs.jpg)), edited |
| `fusion-canyon.jpg` | The Fort Collins painting, for the fusion-canyon repo | Photo by Charles Willgren, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) ([source](https://commons.wikimedia.org/wiki/File:Poudre_Canyon,_Greyrock_trail.jpg)), edited |
| `startup-credits.jpg` | The Golden painting, for the startup-credits repo | Photo by James St. John, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/), edited |

## Logo (`logo/`, decisions 50 and 59)

Three tiers and the banner, built by `art/render/fibo_cards.py` (`crest`, `banner` and `logo`, then `logo_export`). The emblem, banner and icon are FIBO 2.0 edits of the 2014 shield, labelled AI-made in each PNG's XMP; the wordmark is type. Reserved marks (`TRADEMARKS.md`).

| File | Tier | Use |
|---|---|---|
| `emblem-512.png`, `emblem-1024.png` | Emblem: the 2014 shield as a loud winged crest in royal-blue enamel and gold, no text | Avatars (GitHub org, LinkedIn, Slack), the website's cards |
| `banner-960x1200.png`, `banner-480x600.png` | Banner: the crest on a royal-blue war banner, as a game faction flies its crest | Event roll-ups, covers and the guide |
| `wordmark-blue.png`, `wordmark-white.png` | Wordmark: Aileron under the State red rule, transparent | Decks, sponsor, State and press pieces, any width |
| `favicon.ico` (16, 32, 48), `apple-touch-icon.png` (180), `icon-192.png`, `icon-512.png` | Icon: white shield on State blue | Favicon, app icons, tiny avatars |
| `claudius-icon-1024.png` | Claudius's icon: his head and shoulders from his card art (decision 50), on navy | The Claudius plugin's directory listing |

## Region crests (`crests/`, decision 60)

One crest per region, as each race in the game carries its own crest under the faction's banner. Each is a FIBO 2.0 edit of the master crest (`logo/emblem-1024.png`), built by `art/render/fibo_cards.py` (`region_crest`, then `crest_export`) and labelled AI-made in its XMP. The gold rim, wings and shield outline stay the same; the field takes the region's stone color and the charge is the region's own symbol. No letters, no project mark. Reserved marks (`TRADEMARKS.md`).

| File | Field | Charge |
|---|---|---|
| `photon-mountain-1024.png`, `-512.png` | Fluorite violet | A crystal prism casting rainbow light over the Flatirons |
| `space-peak-1024.png`, `-512.png` | Pikes Peak granite pink | A bright star over Pikes Peak |
| `fusion-canyon-1024.png`, `-512.png` | Stout sandstone red | A ring of fire in a red canyon |

Use: the region lockup "Colorado Startups · {Place}" (`data/architecture.yaml`), region event cards and channel headers, at 32 px and up. Below 32 px, use the logo's icon.

## Website art (`website/`, decisions 53, 57 and 58)

The website's art in the game look, text to image with FIBO 2.0 (`art/render/fibo_cards.py`, `hall` then `hall_export`), each labelled AI-made in its XMP. Sizes follow the website's finals (coloradostartups.org `art/concepts/finals.md`).

| File | What | Size |
|---|---|---|
| `communitas.png`, `communitas-small.png` | Communitas, Keeper of the Doors: a dwarf woman, copper braids, sky-blue cloak, keys, lantern on a pole | 960 × 1200; 320 × 320 |
| `resourcus.png`, `resourcus-small.png` | Resourcus: an elder gnome mapkeeper, white beard, tall brass hat with goggles, pine-green coat, compass and blank map | 960 × 1200; 320 × 320 |
| `publicus.png`, `publicus-small.png` | Publicus, Herald of Colorado Startups: a dwarf herald, copper braided beard, feathered red cap, ember tabard, blank broadsheet | 960 × 1200; 320 × 320 |
| `passage.jpg` | The 404 scene: a cog railway in a pink-granite passage ends at a blank wall | 1344 × 756 |
| `founders.jpg` | Founders build a glowing fusion core in a red sandstone workshop below red rock spires | 1344 × 756 |
| `guides.jpg` | Two founders plan a route on a picture map with no writing, in a study above Denver and the Front Range | 1344 × 756 |
| `stone.png` | A warm sandstone texture tile | 1024 × 1024 |

The keepers are AI agents: every surface that shows one also shows its disclosure line (`data/world.yaml` `keepers`).

## Templates (`templates/`, decision 54)

Built by `templates/build.py` from committed files in seconds (no model call). The guide's Files section lists them from `templates/kit.yaml`.

| File | Size | Where it goes |
|---|---|---|
| `square-512.png` | 512 × 512 | Slack workspace icon, LinkedIn Page logo, GitHub org avatar |
| `linkedin-cover-1128x191.png` | 1128 × 191 | LinkedIn Page cover |
| `slide-title-1920x1080.png`, `slide-closing-1920x1080.png` | 1920 × 1080 | Deck backgrounds |
| `email-signature.html` | 600 px wide | Mail client signature; replace NAME and ROLE |

## Places (`places/`, 1440×720 JPEG)

Each real Colorado place transformed with magic into one bright, hand-painted fantasy-game scene, repainted from a photo (decisions 43 to 46). AI-made with FIBO 2.0, with no text on the image; the AI-made label and photo credit are in its IPTC metadata (decision 46). Built by `art/render/fibo_cards.py` (`painted`, then `places`).

| File | Place | Credit |
|---|---|---|
| `boulder.jpg` | Boulder (Photon Mountain): the Flatirons as an elven city of waterfalls, moon portals and a great tree, with dragons | Photo by Jimbo Herndan, [public domain](https://commons.wikimedia.org/wiki/File:Flatirons_2007.jpg) |
| `golden.jpg` | Golden (Photon Mountain): Table Mountain as a dwarven kingdom's forge gate, with steam carts and a boulder wyrm | Photo by James St. John, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) ([source](https://commons.wikimedia.org/wiki/File:Lava_flows_capping_North_Table_Mountain_%26_South_Table_Mountain_(Denver_Formation,_Upper_Cretaceous;_Golden,_Colorado,_USA).jpg)), edited |
| `denver.jpg` | Denver (Photon Mountain): the skyline behind a walled castle town, with knights on white horses and white gryphons | Photo by USFWS Mountain-Prairie, [public domain](https://commons.wikimedia.org/wiki/File:Denver_Skyline_(15242286069).jpg) |
| `springs.jpg` | Colorado Springs (Space Peak): Pikes Peak's rock spires as tower aeries, with gyrocopters and a gryphon | Photo by Huttarl, [CC BY 2.5](https://creativecommons.org/licenses/by/2.5/) ([source](https://commons.wikimedia.org/wiki/File:Pikes_Peak_from_CO_Springs.jpg)), edited |
| `fortcollins.jpg` | Fort Collins (Fusion Canyon): Poudre Canyon as a gnome workshop village of water wheels and round-door burrow homes, with small dragons and mechanical striders | Photo by Charles Willgren, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) ([source](https://commons.wikimedia.org/wiki/File:Poudre_Canyon,_Greyrock_trail.jpg)), edited |
