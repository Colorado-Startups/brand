# Art direction v5: Colorado, transformed with magic: The keepers

Part 9 of 11 of [`DIRECTION.md`](../DIRECTION.md).

## The keepers

The keepers carry over as the community's world (decision 2). Their game-style restyle is deferred (decision 48), so each sheet keeps the look of the pick that shipped on the website. Each sheet is fixed: paste its `objects_entry` verbatim into every caption that shows the keeper, and change only `location` and `relationship` per image.

| Sheet | Kind | Anchor role | Prop |
|---|---|---|---|
| [`keepers/communitas.yaml`](../keepers/communitas.yaml) | Dwarf | `community` | A brass lantern on a short pole, and a ring of brass keys |
| [`keepers/resourcus.yaml`](../keepers/resourcus.yaml) | Gnome | `pine`, with `brass` | A brass surveyor's compass over a painted Front Range map |
| [`keepers/publicus.yaml`](../keepers/publicus.yaml) | Dwarf | `fire` | A blank broadsheet held high, and a satchel of letters |

| Craft | Value |
|---|---|
| Disclosure | Every keeper is an AI agent. Its picture ships beside the sheet's `disclosure`, set in HTML. Its alt text follows the sheet's `alt_text`, which says so too |
| Anchors by role | Each anchor is a token role, and its color words follow that role's value in `tokens/brand_tokens.yaml`. The restyle sets the new words |
| Apart at 64 px | Each keeper reads apart by color anchor and silhouette at 64 px (a goal). The website's make-finals tool measures the anchor's share, with a goal of 8% (website `art/concepts/batch-1.md`) |
| Two crops | A large half-body crop at 4:5 and a small head-and-shoulders crop at 1:1. Goal sizes are 960 × 1200 and 320 × 320 (v3, Portrait files) |
| Craft notes | Each sheet's `craft_notes` list what keeps the picture reading as that keeper |
