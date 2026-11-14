"""art/render/fibo_cards.py: the five social cards, rendered with FIBO 2.0 on Modal (decisions 31, 35, 37).

Lane: Modal's included credit, an L40S. Weights: briaai/Fibo-2.0-dev, gated (Modal Secret fibo-hf). Every image is
sent to Bria's attribution API (Modal Secret fibo-bria), which keeps commercial use covered under the FIBO 2 Free
plan and counts one call. Reserve the calls first: python3 tools/fibo_budget.py reserve N.
Run: modal run art/render/fibo_cards.py [--limit N] [--skip N]   (writes art/render/out/<card>-<seed>.png, raw art, no text)
"""
import base64, io, json, pathlib
import modal

app = modal.App("brand-fibo-cards")
weights = modal.Volume.from_name("fibo-weights", create_if_missing=True)
image = (modal.Image.debian_slim(python_version="3.12")
         .pip_install("diffusers>=0.42.0", "torch", "torchvision", "transformers", "accelerate", "requests", "pillow"))

# The State palette (research/color/state.yaml) with the forge glow; real places as they are (data/world.yaml).
COMMON = {
    "lighting": {"conditions": "golden hour, a low warm sun, with a warm ember glow from a carved stone forge hall in the foreground foothill",
                 "direction": "low sun from the right, ember light from below in the foreground", "shadows": "long, soft, warm shadows"},
    "aesthetics": {"composition": "wide 2:1 landscape; the left 45 percent of the frame is calm, empty, open sky over a soft distant ridge; the landmark and the glowing forge doorway sit in the right half",
                   "color_scheme": "deep navy blue upper sky (#001970) fading through blue to warm gold (#ffd100) at the horizon, red sandstone (#c3002f tones), dark pine green (#245d38), blue-teal mountain haze (#35647e), and a warm ember-orange forge glow",
                   "mood_atmosphere": "grand, warm, welcoming, quietly magical"},
    "photographic_characteristics": {"depth_of_field": "deep", "focus": "sharp throughout", "camera_angle": "eye-level, slightly low", "lens_focal_length": "wide-angle"},
    "style_medium": "cinematic photorealistic landscape photograph with a subtle fantasy touch",
    "text_render": [],
    "context": "a social media preview card background for a Colorado founders community; text is added later, so the image contains no text, letters, logos, flags, emblems or signage",
    "artistic_style": "photorealistic, cinematic, natural",
}
FORGE = ("a tall arched doorway carved directly into a weathered rock face of an unnamed foothill in the right foreground, warm orange "
         "forge light glowing from deep inside, two iron lanterns beside it, worn stone steps; no building, no people, no characters, no symbols")
CARDS = {
    "coloradostartups.org": ("The Flatirons above Boulder, Colorado, at golden hour, with a small glowing forge hall in an unnamed foothill nearby",
                             "the Flatirons above Boulder, Colorado: three huge flat triangular slabs of red-brown sandstone tilted steeply back against the east face of Green Mountain, rising out of dark pine forest above a green meadow, exactly as seen from Chautauqua Park"),
    "brand": ("North Table Mountain and Lookout Mountain above Golden, Colorado, at golden hour, with a glowing forge hall in a nearby foothill",
              "North Table Mountain above Golden, Colorado: a long flat-topped mesa with a dark basalt cap and steep grassy slopes, with forested Lookout Mountain beyond, exactly as they are"),
    "claudius": ("Horsetooth Rock above Fort Collins, Colorado, at golden hour, with a glowing forge hall in a nearby foothill",
                 "Horsetooth Rock west of Fort Collins, Colorado: a rocky summit with two blunt granite knobs like a horse's molar on a long forested ridge above the blue water of Horsetooth Reservoir, exactly as it is"),
    "link": ("Pikes Peak seen from Colorado Springs at golden hour, with a glowing forge hall in an unnamed foothill far from the peak",
             "Pikes Peak, the pink-granite summit seen from Colorado Springs, Colorado, shown exactly as it is, untouched, distant"),
    "legallas": ("The Colorado Front Range at dawn seen from the plains, with a glowing forge hall in a nearby foothill",
                 "the snow-capped Colorado Front Range at dawn seen across the high plains, shown exactly as it is"),
}
SEEDS = (11, 23, 37)
# Bria's recommended text-to-image negative (Fibo-2.0-dev model card) with text, titles and watermarks added.
NEGATIVE = json.dumps({"short_description": "", "objects": [{"description": "the main subject", "texture": "smooth, featureless, plastic-like, airbrushed, no fine surface detail", "appearance_details": "soft blurred edges, simplified shapes, no fine detail"}], "background_setting": "a plain seamless studio backdrop, featureless", "lighting": {}, "aesthetics": {"artifacts": ["visible text", "caption", "title", "letters", "words", "watermark", "logo", "signage", "oversaturated colours", "neon colour cast", "overexposed highlights", "lens flare", "slight blur", "haze"]}, "photographic_characteristics": {"depth_of_field": "shallow, heavy bokeh", "focus": "soft, out of focus"}, "style_medium": "", "context": "", "artistic_style": ""})


def scene(card):
    short, landmark = CARDS[card]
    return json.dumps({"short_description": short,
                       "objects": [{"description": FORGE, "location": "right foreground, lower third", "relationship": "a small warm accent below the real landmark", "relative_size": "small within frame"}],
                       "background_setting": landmark, **COMMON}, ensure_ascii=False)


@app.cls(image=image, gpu="L40S", timeout=1800, volumes={"/cache": weights},
         secrets=[modal.Secret.from_name("fibo-hf"), modal.Secret.from_name("fibo-bria")])
class Fibo:
    @modal.enter()
    def load(self):
        import os, torch
        from diffusers import BriaFibo2Pipeline
        from huggingface_hub import hf_hub_download
        os.environ["HF_HOME"] = "/cache"
        self.pipe = BriaFibo2Pipeline.from_pretrained("briaai/Fibo-2.0-dev", dtype=torch.bfloat16, cache_dir="/cache").to("cuda")
        self.fonts = [hf_hub_download("briaai/Fibo-2.0-dev", n, subfolder="fonts", cache_dir="/cache") for n in ("Aileron-Regular.otf", "DejaVuSans.ttf")]
        weights.commit()

    @modal.method()
    def render(self, prompt: str, seed: int) -> dict:
        import os, requests, torch
        img = self.pipe(prompt=prompt, negative_prompt=NEGATIVE, width=1440, height=720, num_inference_steps=50, guidance_scale=5.0, fonts=self.fonts,
                        generator=torch.Generator("cuda").manual_seed(seed)).images[0]
        buf = io.BytesIO(); img.save(buf, "PNG"); png = buf.getvalue()
        r = requests.post("https://engine.prod.bria-api.com/v2/image/attribution/by_image",
                          headers={"api_token": os.environ["BRIA_API_KEY"], "Content-Type": "application/json"},
                          json={"image": base64.b64encode(png).decode(), "model": "image_fibo:2", "agent": "colorado-startups-brand", "sync": True},
                          timeout=120)
        return {"png": png, "attribution_status": r.status_code, "attribution": r.json().get("request_id") if r.ok else r.text[:200]}


@app.local_entrypoint()
def main(limit: int = 0, skip: int = 0):
    out = pathlib.Path(__file__).parent / "out"; out.mkdir(exist_ok=True)
    jobs = [(c, s) for c in CARDS for s in SEEDS][skip:]
    jobs = jobs[:limit] if limit else jobs
    log = []
    for (card, seed), res in zip(jobs, Fibo().render.starmap([(scene(c), s) for c, s in jobs])):
        (out / f"{card}-{seed}.png").write_bytes(res["png"])
        log.append({"card": card, "seed": seed, "attribution_status": res["attribution_status"], "attribution": res["attribution"]})
        print(card, seed, "attribution", res["attribution_status"])
    runs = out / "runs.json"
    old = json.loads(runs.read_text()) if runs.exists() else []
    runs.write_text(json.dumps(old + log, indent=1) + "\n")
