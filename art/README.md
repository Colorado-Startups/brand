# art

Art and motion direction for illustration and video (owner S7). All artwork is FIBO 2.0, video is LTX-2.5 and image motion is Rive (decision 37). The logo ships from `dist/logo/`, made the same way (`logo/README.md`).

| File | What it holds |
|---|---|
| [`DIRECTION.md`](DIRECTION.md) | Art direction v5: the five places, the look, the characters and cards, the palette, the keepers, prompts, renders |
| [`render/`](render/) | The render client `fibo_cards.py` and the ZeroGPU Space's source |
| [`prompts/`](prompts/) | FIBO 2.0 VGL templates for the deferred hero, region, keeper and tile art, with fixed fields marked |
| [`keepers/`](keepers/) | One fixed sheet per keeper: the verbatim `objects` entry, the color anchor by token role, the AI-agent disclosure and craft notes |
| [`motion.md`](motion.md) | LTX-2.5 rules: approved stills only, muted short loops, pause control, an AI-made label in metadata, provenance |
| [`LICENSES.md`](LICENSES.md) | The license register: model, route, verdict and duties, and the $2M and $10M revenue lines |
| [`render-queue.yaml`](render-queue.yaml) | Every render the brand needs, by status: done, in progress or deferred |
| [`fibo-calls.yaml`](fibo-calls.yaml), [`bria-credit.yaml`](bria-credit.yaml) | The FIBO call count by month and the spend on Bria's hosted credit, enforced by `tools/fibo_budget.py` |
