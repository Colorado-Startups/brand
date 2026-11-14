# Motion: LTX-2.5 rules for the Hall's clips: Frame and size math

Part 2 of 4 of [`motion.md`](../motion.md).

## Frame and size math

LTX-2.5 needs a frame count where `frames % 8 == 1`, and a width and height that divide by 32 (LTX-2.5 model card, "Constraints", read 2026-11-02). The numbers below are computed here from those two rules.

| Need | Setting | Why |
|---|---|---|
| 720p frame | Render 1280 × 736, crop 8 px from the top and the bottom to 1280 × 720 | 720 does not divide by 32; 736 is the next size that does |
| A loop of 10 s or less | 233 frames, 9.7 s at 24 fps | 241 frames, the next valid count, runs 10.04 s |
| A loop that repeats cleanly | Drop the last frame when encoding: 232 frames | In a first-and-last-frame loop the last frame repeats the first |
| A clip that plays once and stops | 113 frames or fewer, 4.7 s at 24 fps | It stops within 5 s, so it needs no pause control (WCAG 2.2.2) |
| Under about 1 MB (a goal) | About 800 kbit/s on average for a 9.7 s clip | 1 MB is 8,000 kbit; 8,000 ÷ 9.7 s is about 825 kbit/s |

## A sample prompt

For the home hero's loop, from its approved still:

> The great hall stays still as warm lantern light slowly rises and falls across the carved granite arches. Small embers drift upward from the hearth on the right and fade before they reach the beams. The molten-gold channel in the floor glows a little brighter, then softer, like slow breathing. The founders at the long table lean in and nod as they talk, with small, natural movements. The long banners sway gently in a light draft. The camera holds still at eye level, with no cuts.

## Encoding

Encoding is a light step; generating video never runs on this Mac (`~/.claude/rules/compute.md`). These are starting values. Raise the CRF number until the clip meets the 1 MB goal, then check it by eye.

```sh
# WebM (VP9), no audio, cropped to 1280 x 720
ffmpeg -i ltx-output.mp4 -vf "crop=1280:720:0:8" -frames:v 232 -an \
  -c:v libvpx-vp9 -b:v 0 -crf 40 -row-mt 1 -map_metadata 0 hall.webm
# MP4 (H.264), no audio, for browsers without WebM
ffmpeg -i ltx-output.mp4 -vf "crop=1280:720:0:8" -frames:v 232 -an \
  -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 28 \
  -movflags +faststart -map_metadata 0 hall.mp4
```

**Provenance beats the size goal.** Check the first LTX-2.5 output for embedded provenance: a content-credentials manifest, metadata tags or a watermark. If it carries any, the shipped files must carry it too. If an encode drops it, ship a format that keeps it, and meet the size goal second (LTX-2.x license §6; Attachment A, item 19).
