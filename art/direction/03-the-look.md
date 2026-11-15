# Art direction v5: Colorado, transformed with magic: The look

Part 3 of 11 of [`DIRECTION.md`](../DIRECTION.md).

## The look

A bright, hand-painted video-game painting of the real photo (decision 43). Paul chose it over a film look: "I like this style the best because it's brighter."

| Trait | What the render does | Set in |
|---|---|---|
| Bright and hand-painted | Bold saturated colors, chunky slightly exaggerated shapes, painterly textures, warm magical light with glowing highlights. The style fields read "digital illustration" and "World of Warcraft, hand-painted, stylized" | `STYLE["wow"]` in `art/render/fibo_cards.py`; decision 43's `LEANS["game"]` first set the look |
| One light | The whole real photo is repainted in one consistent light, so nothing looks pasted on (decision 43) | `painted()`, one unmasked edit per place |
| Recognisable | The landmark's shapes and colors are named in the prompt, so it stays recognisable | `PAINTED[place]` |
| One hero structure | A single structure stands at huge scale: an elven city on the Flatirons, a dwarven gate in the Table Mountain mesa, a keep on a hill before Denver, an aerie on Pikes Peak's crags, a gnome town on the Poudre Canyon floor | `PAINTED[place]` |
| A crowd | Dozens of the place's own people fill the city, small in the frame (decision 44) | `PAINTED[place]` |
| Two accents | One wild creature and one mount, small, in the sky or on the road | `PAINTED[place]` and `REFS` |
| Named influences | The prompt names the game, the film and the place outright, and sets `style_medium` and `artistic_style` directly (decision 44) | `STYLE`, `PLACE_STYLE` and `PAINTED[place]` |

## Each place's colors

| Place | Color scheme in the prompt | Mood |
|---|---|---|
| Boulder | Night-elf purples and teals with moonlit silver, golden leaves, red-brown sandstone | Epic, magical, serene |
| Golden | Warm stone greys, bronze, gold and forge orange, with crimson banners | Epic, mighty, bustling |
| Denver | White stone, royal blue and gold, with green fields and golden trees | Epic, noble, lively |
| Colorado Springs | Pink granite, forest green and gold, with warm firelight | Epic, adventurous, wild |
| Fort Collins | Brass, copper and glowing teal, with garden greens and bright flowers | Epic, whimsical, cheerful |

Source: `PLACE_STYLE` in `art/render/fibo_cards.py`.

## How a place is made

| Step | What happens | Source |
|---|---|---|
| 1 | Start from a public-domain or CC BY photo of the landmark (`art/render/src/SOURCES.md`) | Decisions 38 and 44 |
| 2 | Render a reference image for any creature the model cannot draw from words (`REFS`), through the same attributed lane | Decisions 42 and 43 |
| 3 | Run one unmasked FIBO 2.0 edit that repaints the whole photo. Bria's VGL step writes the structured edit from the instruction; `Fibo-2.0-edit-turbo` runs it | Decisions 41 and 43 |
| 4 | Send the image to Bria's attribution call and log it in `art/render/out/runs.json` | Decisions 35 and 41 |
| 5 | Composite the name and write the IPTC provenance, with the AI-made label and the photo credit | Decisions 37 and 46 |

The shipped renders use seed 51 (decision 45). They are `dist/places/*.jpg`.
