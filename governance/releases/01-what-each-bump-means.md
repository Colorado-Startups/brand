# Releases: What each bump means

Part 1 of 3 of [`releases.md`](../releases.md).

## What each bump means

| Bump | When | Examples |
|---|---|---|
| **Major** `4.0.0` | A consumer must change its code, or the public would see a new identity | Removing or renaming a token, data key or `dist/` path; a new primary mark or wordmark; a new type family; a color role moving to a different hue; a new name or tagline |
| **Minor** `3.1.0` | Something is added, or a value changes inside the same identity | A new token, logo variant, outpost crest, template, guide section or data field; a color value that keeps its hue and every contrast pair at its minimum; a deprecation, with the old name kept as an alias until the next major |
| **Patch** `3.0.1` | Nothing is meant to look different | A typo, metadata, a provenance label, a build or checksum fix; an asset brought back to its own spec, such as a drifted color reset to its token |

When a change could fit two rows, take the larger bump.
