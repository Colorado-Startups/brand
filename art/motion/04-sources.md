# Motion: LTX-2.5 rules for the Hall's clips: Sources

Part 4 of 4 of [`motion.md`](../motion.md).

## Sources

Read 2026-11-02.

| Source | Used for |
|---|---|
| The website's `art/DIRECTION.md` at `13c6b52` and `e628748`; the merge `b1378dd` | Rules 1 to 7, and where they were lost |
| [LTX-2.5 model card](https://huggingface.co/Lightricks/LTX-2.5) | Frame and size constraints; CFG 1 on the distilled checkpoint |
| [LTX-2 prompting guide](https://docs.ltx.io/open-source-model/usage-guides/prompting-guide), via the research digest | One present-tense paragraph of 4 to 8 sentences; CFG about 4 or less; audio on by default |
| [LTX-2.x Community License](https://github.com/Lightricks/LTX-2/blob/main/LICENSE-2_x) | Labels, watermarks and provenance (§6; Attachment A, items 5 and 19) |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | 1.2.2 captions, 2.2.2 pause, 2.3.1 three flashes, 2.5.8 target size |
| [web.dev, "Replace animated GIFs with video"](https://web.dev/articles/replace-gifs-with-videos) | `autoplay muted loop playsinline`, WebM first, poster, `preload` |

## Rive (decision 31)

| Rule | Value |
|---|---|
| Use | Interactive marks, keepers and UI motion: one `.riv` per mark or keeper, driven by a state machine |
| Autoplay | Stops within 5 s, or has a pause control; nothing flashes more than 3 times a second |
| Reduced motion | `prefers-reduced-motion: reduce` shows the still first frame |
| Build | Scenes live in `art/rive/<name>/` (`rive create`); `rive <dir> --verify` checks one locally in seconds; nothing renders video on this Mac |
| Account | Pushing to a Rive account waits for Paul's `rive login` |
| Licence | Rive's runtimes are open source; S7 reads Rive's terms of service and adds a row to `art/LICENSES.md` before the first shipped `.riv` |
