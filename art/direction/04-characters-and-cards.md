# Art direction v5: Colorado, transformed with magic: Characters and cards

Part 4 of 11 of [`DIRECTION.md`](../DIRECTION.md).

## Characters and cards

Each project card is a character (decision 39). The master-brand cards and the four region and project repo cards use place art. Every card shows only its name, set in Aileron after the render (decisions 37 and 46).

| Card | Image | Blends |
|---|---|---|
| `coloradostartups.org` | Boulder place art | Part 2 |
| `brand` | Golden place art | Part 2 |
| `claudius` | Claudius, a gnome engineer and loyal companion | Samwise (the loyal companion) and Mimiron (the titan-forged master engineer) (decision 40) |
| `link` | Linken, a gnome hero | Ocarina of Time's Link and World of Warcraft's gnome Linken; the name also reads as short for LinkedIn (decision 39) |
| `legallas` | Legallas, an elf ranger | The Lord of the Rings' Legolas and Silvermoon's Ranger-General, Halduron Brightwing (decision 39) |
| `photon-mountain`, `space-peak`, `fusion-canyon`, `startup-credits` | The Denver, Colorado Springs, Fort Collins and Golden paintings | Part 2 (decision 50) |

The characters borrow costume cues and carry their own gear (decision 39):

| Character | Gear and cues |
|---|---|
| Linken | A green cap and tunic, a sword, a shield and a boomerang |
| Legallas | Platinum hair, a longbow and twin knives |
| Claudius | Brass goggles and gauntlet, a tool belt of gadgets, and a thin slate of glowing light for the agent's work |

## Status

| Item | State |
|---|---|
| The three character cards in `v3.0.0-alpha.4` | A first pass in a cinematic, realistic style, replaced in the next release |
| Characters in the game style | Done (decision 50): Claudius, Linken and Legallas, re-rendered like the places, with their cards recomposed |
| Region art, place heroes and the keepers | Deferred (decisions 44 and 48) |

## Layout

| Element | Value | Source |
|---|---|---|
| Card | 1280 × 640 JPEG | `dist/README.md` |
| Render size | 1440 × 720, 2:1 | `SIZE` in `art/render/fibo_cards.py` |
| Character | In the right half; the left 45 percent stays calm | `CHARACTERS` in `art/render/fibo_cards.py` |
| Name | Composited after, in Aileron (CC0) | Decisions 37 and 46 |
| AI-made label and photo credit | In the image's IPTC metadata, not on the picture | Decision 46 |
