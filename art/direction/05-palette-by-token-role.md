# Art direction v5: Colorado, transformed with magic: Palette by token role

Part 5 of 11 of [`DIRECTION.md`](../DIRECTION.md).

## Palette by token role

The art lands in the same colors as the UI, so a picture and the page around it read as one surface. This file names roles only. `tokens/brand_tokens.yaml` sets every value from the State of Colorado's palette (decision 29), and keeps the role names. The forge glow and the fantasy twist stay in the art (decision 29). Each place also has its own colors (Part 3). The prompts' `color_scheme` field carries the palette in plain color words, and the characters' prompts add the State's navy and gold by hex beside the words (`CHARACTERS` in `art/render/fibo_cards.py`).

**Color words follow the roles.** No hue is fixed here. When `tokens/brand_tokens.yaml` changes a role's value, the words that name it in the prompts change to match, by role, in the same change. The keepers' sheets keep their older words until their restyle (decision 48).

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

Two art colors have no role: aspen gold (autumn aspens, banners) and alpenglow rose (snow on the high peaks at sunset). The art names them in words. If tokens v3 makes either one a UI color, the file that does so states that it reverses website decision 90.
