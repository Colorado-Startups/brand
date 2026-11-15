# Colorado Startups brand

The open source of the Colorado Startups brand: strategy, voice, world, tokens, logos, art direction and templates. Colorado first, with the State of Colorado's palette and real Front Range places transformed with magic, painted bright in a video-game style. All artwork is FIBO 2.0, video is LTX-2.5 and image motion is Rive (decision 37).

```mermaid
flowchart LR
  D[data/*.yaml<br/>strategy · voice · world] --> B[tools/ build]
  T[tokens/*.yaml] --> B
  B --> X[dist/<br/>tokens CSS and JSON · brand.json · logo · place and card images]
  A[art/render/<br/>FIBO 2.0 on a ZeroGPU Space] --> X
  X --> G[Guide on GitHub Pages]
  X --> P[Templates]
  X --> C[Every other repo<br/>pins a release]
```

| Need | Go to |
|---|---|
| See the brand | [The guide](https://colorado-startups.github.io/brand/) |
| See how healthy the repo is | [Quality, Speed, Consumption](https://colorado-startups.github.io/brand/quality/) · [Process](https://colorado-startups.github.io/brand/quality/process.html) |
| Use it in a repo | From `v3.0.0`: pin a release in `brand.lock.json`, pull with `tools/brand_pull.py`, commit the copies |
| Why something is the way it is | [`decisions.md`](decisions.md) |
| Contribute | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Reuse it | Code: [Apache-2.0](LICENSE). Writing and data: [CC BY 4.0](LICENSES/CC-BY-4.0.txt). Name, marks and keepers: [`TRADEMARKS.md`](TRADEMARKS.md) |
