"""LTX-2.5 distilled image-to-video with the Cinemagraph LoRA, on ZeroGPU, for the Colorado Startups brand (decision 62).

Follows Lightricks' own public Space `Lightricks/LTX-2.5` (two-stage distilled: 8 sigmas at half size, x2 latent upsample,
3 sigmas at full size, convolutional decode, unguided) and adds `Lightricks/LTX-2.5-22b-LoRA-Cinemagraph`
(`CINEMAGRAPH_MOTION`, strength 0.5 to 1.5, sweet spot 1.0 to 1.2 on its model card). The client sends the prompt, negative,
size, frames, seed and LoRA strength, so the brand's values live in art/render/ltx_clips.py. Audio is not decoded.
"""
import os
os.environ.setdefault("PYTORCH_ALLOC_CONF", "backend:cudaMallocAsync")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "backend:cudaMallocAsync")
import tempfile
import gradio as gr
import PIL.Image
import spaces
import torch
from huggingface_hub import snapshot_download
from diffusers import LTX2ImageToVideoPipeline, LTX2LatentUpsamplePipeline, LTX2Pipeline
from diffusers.pipelines.ltx2.latent_upsampler import LTX2LatentUpsamplerModel
from diffusers.pipelines.ltx2.utils import DEFAULT_NEGATIVE_PROMPT, DISTILLED_SIGMA_VALUES, STAGE_2_DISTILLED_SIGMA_VALUES
from diffusers.utils import encode_video

HF_TOKEN = os.environ.get("HF_TOKEN")
MODEL_ID = "Lightricks/LTX-2.5-Diffusers"
LORA_ID, LORA_FILE = "Lightricks/LTX-2.5-22b-LoRA-Cinemagraph", "ltx-2.5-22b-lora-cinemagraph-0.9.safetensors"
FPS = 24.0

MODEL_DIR = snapshot_download(MODEL_ID, ignore_patterns=["transformer_full/*", "diffusion_decoder/*"], token=HF_TOKEN, max_workers=8)
base = LTX2Pipeline.from_pretrained(MODEL_DIR, dtype=torch.bfloat16)
base.load_lora_weights(LORA_ID, weight_name=LORA_FILE, adapter_name="cinemagraph", token=HF_TOKEN)  # into the shared transformer
upsampler = LTX2LatentUpsamplerModel.from_pretrained(MODEL_DIR, subfolder="latent_upsampler", dtype=torch.bfloat16)
base.to("cuda"); upsampler.to("cuda")
base.vae.enable_tiling()
pipe = LTX2ImageToVideoPipeline(
    scheduler=base.scheduler, vae=base.vae, audio_vae=base.audio_vae, text_encoder=base.text_encoder, tokenizer=base.tokenizer,
    connectors=base.connectors, transformer=base.transformer, vocoder=base.vocoder, processor=getattr(base, "processor", None),
    prompt_enhancer=getattr(base, "prompt_enhancer", None), duration_head=getattr(base, "duration_head", None))
upsample = LTX2LatentUpsamplePipeline(vae=base.vae, latent_upsampler=upsampler)


def cover(path, w, h):
    img = PIL.Image.open(path).convert("RGB")
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), PIL.Image.LANCZOS)
    l, t = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((l, t, l + w, t + h))


@spaces.GPU(duration=lambda *a: 150, size="xlarge")
def _run(prompt, negative, image, height, width, frames, seed, strength):
    base.set_adapters(["cinemagraph"], [float(strength)])
    gen = torch.Generator("cuda").manual_seed(int(seed))
    shared = dict(prompt=prompt, negative_prompt=negative or DEFAULT_NEGATIVE_PROMPT, frame_rate=FPS, guidance_scale=1.0,
                  audio_guidance_scale=1.0, stg_scale=0.0, audio_stg_scale=0.0, modality_scale=1.0, audio_modality_scale=1.0,
                  guidance_rescale=0.0, audio_guidance_rescale=0.0, spatio_temporal_guidance_blocks=None, generator=gen,
                  return_dict=False, image=cover(image, width, height))
    s1, a1 = pipe(height=height // 2, width=width // 2, num_frames=frames, sigmas=DISTILLED_SIGMA_VALUES, output_type="latent", **shared)
    up = upsample(latents=s1, output_type="latent", return_dict=False)[0]
    video, _ = pipe(num_frames=frames, sigmas=STAGE_2_DISTILLED_SIGMA_VALUES, latents=up, audio_latents=a1,
                    noise_scale=STAGE_2_DISTILLED_SIGMA_VALUES[0], output_type="np", **shared)
    path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    encode_video(video[0], fps=int(FPS), output_path=path)  # silent: no audio kwargs
    return path


def cinemagraph(image: str, prompt: str, negative: str, seed: int, height: int, width: int, frames: int, strength: float):
    if height % 64 or width % 64 or (frames - 1) % 8:
        raise gr.Error("height and width divide by 64, and frames is 8k+1")
    return _run(prompt, negative, image, int(height), int(width), int(frames), int(seed), float(strength))


demo = gr.Interface(cinemagraph, [gr.File(label="image", type="filepath"), gr.Textbox(label="prompt"), gr.Textbox(label="negative"),
                                  gr.Number(11, label="seed", precision=0), gr.Number(640, label="height", precision=0),
                                  gr.Number(1280, label="width", precision=0), gr.Number(121, label="frames", precision=0),
                                  gr.Number(1.1, label="strength")],
                    gr.Video(label="mp4"), api_name="cinemagraph", title="LTX-2.5 Cinemagraph for the Colorado Startups brand")
demo.queue(default_concurrency_limit=1).launch()
