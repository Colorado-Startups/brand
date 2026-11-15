---
title: Brand LTX
emoji: 🔥
colorFrom: blue
colorTo: yellow
sdk: gradio
sdk_version: 6.31.0
python_version: "3.12"
app_file: app.py
suggested_hardware: zero-a10g
pinned: false
---

LTX-2.5 distilled image-to-video with Lightricks' Cinemagraph LoRA for the Colorado Startups brand, on ZeroGPU at the
`xlarge` size (2x quota; about 68 GB of weights): the camera stays still and only the named parts move (decision 62).
Both repos are gated and need the owner's licence click; the Space secret `HF_TOKEN` (pushed by `keys.sh` in
`paul-co-startups/api-keys`) carries that access. Source of truth: `Colorado-Startups/brand` `art/render/ltx-space/`;
the client is `art/render/ltx_clips.py cinemagraph`.
