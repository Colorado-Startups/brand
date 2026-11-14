# Art direction v4: the Hall, carved in Colorado: The keepers

Part 9 of 11 of [`DIRECTION.md`](../DIRECTION.md).

## The keepers

Each keeper has one fixed sheet. Paste its `objects_entry` verbatim into every caption that shows it; only `location` and `relationship` change per image.

| Sheet | Kind | Anchor role | Prop |
|---|---|---|---|
| [`keepers/communitas.yaml`](../keepers/communitas.yaml) | Dwarf | `community` | A brass lantern on a short pole, and a ring of brass keys |
| [`keepers/resourcus.yaml`](../keepers/resourcus.yaml) | Gnome | `pine`, with `brass` | A brass surveyor's compass over a painted Front Range map |
| [`keepers/publicus.yaml`](../keepers/publicus.yaml) | Dwarf | `fire` | A blank broadsheet held high, and a satchel of letters |

- **Disclosure.** Every keeper is an AI agent. Its picture ships beside the sheet's `disclosure`, set in HTML and never painted in. Its alt text follows the sheet's `alt_text`, which says so too.
- **Anchors by role.** Each anchor is a token role, and its color words follow that role's value. A render's painted anchor is checked against the role. The shipped Communitas cloak painted near 187 degrees, while the `community` token sat at 212 degrees (website `art/finals.json`).
- **Apart at 64 px.** Each keeper reads apart by color anchor and silhouette at 64 px (a goal). The website's make-finals tool measures the anchor's share, with a goal of 8% (website `art/concepts/batch-1.md`).
- **Two crops.** A large half-body crop at 4:5 and a small head-and-shoulders crop at 1:1. Goal sizes are 960 × 1200 and 320 × 320 (v3, Portrait files).
