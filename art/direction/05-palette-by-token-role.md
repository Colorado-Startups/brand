# Art direction v4: the Hall, carved in Colorado: Palette by token role

Part 5 of 11 of [`DIRECTION.md`](../DIRECTION.md).

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
