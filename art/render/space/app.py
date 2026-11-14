"""FIBO 2.0 on ZeroGPU for the Colorado Startups brand (decisions 31, 35, 37, 41).

render mirrors Fibo.render in art/render/fibo_cards.py (Fibo-2.0-dev). edit follows Bria's own editing method: the
client brings a structured edit JSON from Bria's VGL step, and Fibo-2.0-edit-turbo runs it in 4 guidance-free steps.
The client sends the prompt, negative, size, steps and guidance, so the brand's values live in one file. Each image
goes to Bria's attribution API before it is returned. Both pipelines (about 50 GB) need the full GPU: xlarge.
"""
import base64, io, json, os, tempfile
import gradio as gr
import requests
import spaces
import torch
from diffusers import BriaFibo2Pipeline
from huggingface_hub import hf_hub_download
from PIL import Image

MODEL = "briaai/Fibo-2.0-dev"
pipe = BriaFibo2Pipeline.from_pretrained(MODEL, dtype=torch.bfloat16).to("cuda")
edit_pipe = BriaFibo2Pipeline.from_pretrained("briaai/Fibo-2.0-edit-turbo", dtype=torch.bfloat16).to("cuda")
fonts = [hf_hub_download(MODEL, n, subfolder="fonts") for n in ("Aileron-Regular.otf", "DejaVuSans.ttf")]


def gpu_seconds(*a):  # a[-2] is steps; a guess per step plus the load. xlarge doubles what the quota check sees
    return int(a[-2] * 1.2) + 30


@spaces.GPU(duration=gpu_seconds, size="xlarge")
def _run(prompt, negative, seed, image, width, height, steps, guidance):
    kw = {"image": image} if image is not None else {"width": width, "height": height, "fonts": fonts}
    if negative:
        kw["negative_prompt"] = negative  # edit-turbo is guidance-free; Bria sends it no negative
    with torch.inference_mode():
        return (edit_pipe if image is not None else pipe)(prompt=prompt, num_inference_steps=steps, guidance_scale=guidance,
                                                          generator=torch.Generator("cuda").manual_seed(seed), **kw).images[0]


def _attribute(img):  # on CPU, outside the GPU call, so it spends no quota
    buf = io.BytesIO(); img.save(buf, "PNG"); png = buf.getvalue()
    r = requests.post("https://engine.prod.bria-api.com/v2/image/attribution/by_image",
                      headers={"api_token": os.environ["BRIA_API_KEY"], "Content-Type": "application/json"},
                      json={"image": base64.b64encode(png).decode(), "model": "image_fibo:2", "agent": "colorado-startups-brand", "sync": True},
                      timeout=120)
    path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    open(path, "wb").write(png)
    return path, r.status_code, (r.json().get("request_id") if r.ok else r.text[:200])


def render(prompt: str, negative: str, seed: int, width: int, height: int, steps: int, guidance: float):
    return _attribute(_run(prompt, negative, int(seed), None, int(width), int(height), int(steps), float(guidance)))


def edit(photo: str, crop: str, ref: str | None, prompt: str, negative: str, seed: int, width: int, height: int, steps: int, guidance: float):
    src = Image.open(photo).convert("RGB"); w, h = src.size; c = json.loads(crop)
    src = src.crop((int(c[0] * w), int(c[1] * h), int(c[2] * w), int(c[3] * h))).resize((int(width), int(height)), Image.LANCZOS)
    image = [src, Image.open(ref).convert("RGB")] if ref else src  # Bria's own Space: the source first, then references
    return _attribute(_run(prompt, negative, int(seed), image, int(width), int(height), int(steps), float(guidance)))


num = lambda label, v: gr.Number(v, label=label, precision=None if isinstance(v, float) else 0)
out = lambda: [gr.File(label="png"), gr.Number(label="attribution_status", precision=0), gr.Textbox(label="attribution")]
base = lambda: [gr.Textbox(label="prompt"), gr.Textbox(label="negative"), num("seed", 11), num("width", 1440), num("height", 720),
        num("steps", 50), num("guidance", 5.0)]
demo = gr.TabbedInterface(
    [gr.Interface(render, base(), out(), api_name="render"),
     gr.Interface(edit, [gr.File(label="photo", type="filepath"), gr.Textbox(label="crop", value="[0,0,1,1]"),
                         gr.File(label="ref", type="filepath")] + base(), out(), api_name="edit")],
    ["render", "edit"], title="FIBO 2.0 for the Colorado Startups brand")
demo.queue(default_concurrency_limit=1).launch()
