---
title: Brand FIBO
emoji: 🏔️
colorFrom: blue
colorTo: yellow
sdk: gradio
sdk_version: 6.31.0
python_version: "3.12"
app_file: app.py
suggested_hardware: zero-a10g
pinned: false
---

FIBO 2.0 for the Colorado Startups brand, on ZeroGPU at the `xlarge` size (2x quota): text to image on
`briaai/Fibo-2.0-dev`, edits on `briaai/Fibo-2.0-edit-turbo` from a structured edit JSON written by Bria's VGL step
(the third-party `briaai/Fibo-2.0-editing` Space). `suggested_hardware: zero-a10g` is HF's key for any ZeroGPU Space. Source of truth:
`Colorado-Startups/brand` `art/render/space/`; the client is `art/render/fibo_cards.py`. Every image goes to Bria's
attribution API (Space secrets `HF_TOKEN`, `BRIA_API_KEY`, pushed by `keys.sh` in `paul-co-startups/api-keys`).
