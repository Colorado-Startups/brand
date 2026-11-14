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
                   "mood_atmosphere": "grand, warm, welcoming, inviting"},
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
    def edit(self, photo: bytes, crop: tuple, prompt: str, seed: int) -> dict:
        import os, requests, torch
        from PIL import Image
        src = Image.open(io.BytesIO(photo)).convert("RGB")
        w, h = src.size
        src = src.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h))).resize((1440, 720), Image.LANCZOS)
        img = self.pipe(prompt=prompt, negative_prompt=NEGATIVE_EDIT, image=src, num_inference_steps=50, guidance_scale=5.0,
                        fonts=self.fonts, generator=torch.Generator("cuda").manual_seed(seed)).images[0]
        return self._attribute(img)

    def _attribute(self, img) -> dict:
        import os, requests
        buf = io.BytesIO(); img.save(buf, "PNG"); png = buf.getvalue()
        r = requests.post("https://engine.prod.bria-api.com/v2/image/attribution/by_image",
                          headers={"api_token": os.environ["BRIA_API_KEY"], "Content-Type": "application/json"},
                          json={"image": base64.b64encode(png).decode(), "model": "image_fibo:2", "agent": "colorado-startups-brand", "sync": True},
                          timeout=120)
        return {"png": png, "attribution_status": r.status_code, "attribution": r.json().get("request_id") if r.ok else r.text[:200]}

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


NEGATIVE_EDIT = json.dumps({"short_description": "", "objects": [], "background_setting": "", "lighting": {}, "aesthetics": {}, "photographic_characteristics": {}, "style_medium": "", "context": "", "artistic_style": ""})

# Edits of real public-domain photos (decision 38). The caption describes the result; edit_instruction states the change.
EDITS = {
    "coloradostartups.org": {
        "photo": "flatirons-2007-pd.jpg", "crop": (0.07, 0.22, 1.0, 0.84),
        "edit_instruction": "Carve a massive, original mountain fortress carved into the heart of the mountain: a monumental stone facade with tall columns and a great arched doorway, towers, halls and terraces rising out of the cliffs at many levels and spread across the whole mountainside, carved from the same weathered rock so they look grown from the mountain, with rows of warm golden glowing windows, small torches and braziers along a winding stone road, the hall clearly vast and cavernous inside; warm, welcoming light, no large fire, spanning a large part of the mountain face, into the mountain below and between the tilted rock slabs. Change the light to golden hour with a deep navy upper sky fading to gold at the ridge. Remove the stadium floodlight tower at the left edge. Keep the Flatirons rock slabs and the mountain's shape exactly as they are. Add no text, letters or signs.",
        "scene": {
            "short_description": "The Flatirons above Boulder, Colorado, at golden hour, with a massive fortress carved into the mountain, rows of warm golden windows climbing the rock",
            "objects": [{"description": "a massive, original mountain fortress carved into the heart of the mountain: a monumental stone facade with tall columns and a great arched doorway, towers, halls and terraces rising out of the cliffs at many levels and spread across the whole mountainside, carved from the same weathered rock so they look grown from the mountain, with rows of warm golden glowing windows, small torches and braziers along a winding stone road, the hall clearly vast and cavernous inside; warm, welcoming light, no large fire", "location": "center, at the forested base of the mountain below the rock slabs", "relationship": "carved into the mountain itself, beneath the Flatirons", "relative_size": "very large within frame"}],
            "background_setting": "the Flatirons, tilted red-brown sandstone slabs on the forested east face of Green Mountain above Boulder, Colorado, exactly as they are, with leafy trees in the foreground",
            "lighting": {"conditions": "golden hour, warm golden window light from the fortress", "direction": "low sun from the left, soft warm light from the windows", "shadows": "long and warm"},
            "aesthetics": {"composition": "wide 2:1 landscape, the mountain and gateway centered, calm sky across the top", "color_scheme": "deep navy upper sky (#001970) fading to warm gold (#ffd100), red-brown sandstone, dark pine green (#245d38), warm golden window light", "mood_atmosphere": "grand, warm, welcoming, inviting"},
            "photographic_characteristics": {"depth_of_field": "deep", "focus": "sharp throughout", "camera_angle": "eye-level", "lens_focal_length": "standard"},
            "style_medium": "photograph, photorealistic", "text_render": [],
            "context": "a social media preview card background for a Colorado founders community; the image contains no text",
            "artistic_style": "photorealistic, cinematic"},
    },
}

EDITS_BASE = {k: v for k, v in EDITS["coloradostartups.org"]["scene"].items() if k not in ("background_setting", "objects")}
EDITS_BASE["short_description"] = "a real Colorado mountain at golden hour with a massive fortress carved into the mountain, rows of warm golden windows climbing the rock"
EDITS.update({
    "brand": {
        "photo": "table-mountains-golden-ccby.jpg", "crop": (0.1, 0.05, 0.9, 0.79),
        "edit_instruction": "Carve a massive, original mountain fortress carved into the heart of the mountain: a monumental stone facade with tall columns and a great arched doorway, towers, halls and terraces rising out of the cliffs at many levels and spread across the whole mountainside, carved from the same weathered rock so they look grown from the mountain, with rows of warm golden glowing windows, small torches and braziers along a winding stone road, the hall clearly vast and cavernous inside; warm, welcoming light, no large fire, spanning a large part of the mountain face, into the steep flank of South Table Mountain on the right, below its basalt cap. Replace the golf course in the foreground with natural grassland and sandstone. Change the light to golden hour with a deep navy upper sky fading to gold at the horizon. Keep the real mountains' shapes exactly as they are. Add no text, letters or signs.",
        "scene": {**EDITS_BASE, "background_setting": 'North and South Table Mountains above Golden, Colorado: two flat-topped mesas with dark basalt caps and grassy slopes, exactly as they are, with sandstone outcrops in the foreground',
                   "objects": [{"description": 'a massive, original mountain fortress carved into the heart of the mountain: a monumental stone facade with tall columns and a great arched doorway, towers, halls and terraces rising out of the cliffs at many levels and spread across the whole mountainside, carved from the same weathered rock so they look grown from the mountain, with rows of warm golden glowing windows, small torches and braziers along a winding stone road, the hall clearly vast and cavernous inside; warm, welcoming light, no large fire', "location": 'the steep flank of South Table Mountain on the right, below its basalt cap', "relationship": "carved into the mountain itself", "relative_size": "very large within frame"}]},
    },
    "claudius": {
        "photo": "horsetooth-mountain-view-ccbysa.jpg", "crop": (0.0, 0.0, 1.0, 0.75),
        "edit_instruction": "Carve a massive, original mountain fortress carved into the heart of the mountain: a monumental stone facade with tall columns and a great arched doorway, towers, halls and terraces rising out of the cliffs at many levels and spread across the whole mountainside, carved from the same weathered rock so they look grown from the mountain, with rows of warm golden glowing windows, small torches and braziers along a winding stone road, the hall clearly vast and cavernous inside; warm, welcoming light, no large fire, spanning a large part of the mountain face, into the rocky slope of the near ridge on the right. Change the light to golden hour with a deep navy upper sky fading to gold at the horizon. Keep the real mountains' shapes exactly as they are. Add no text, letters or signs.",
        "scene": {**EDITS_BASE, "background_setting": 'the foothills and ridges west of Fort Collins, Colorado, seen from Horsetooth Mountain Open Space, exactly as they are, pine trees and boulders in the foreground',
                   "objects": [{"description": 'a massive, original mountain fortress carved into the heart of the mountain: a monumental stone facade with tall columns and a great arched doorway, towers, halls and terraces rising out of the cliffs at many levels and spread across the whole mountainside, carved from the same weathered rock so they look grown from the mountain, with rows of warm golden glowing windows, small torches and braziers along a winding stone road, the hall clearly vast and cavernous inside; warm, welcoming light, no large fire', "location": 'the rocky slope of the near ridge on the right', "relationship": "carved into the mountain itself", "relative_size": "very large within frame"}]},
    },
    "link": {
        "photo": "pikes-peak-colorado-springs-ccby.jpg", "crop": (0.0, 0.0, 1.0, 0.667),
        "edit_instruction": "Carve a massive, original mountain fortress carved into the heart of the mountain: a monumental stone facade with tall columns and a great arched doorway, towers, halls and terraces rising out of the cliffs at many levels and spread across the whole mountainside, carved from the same weathered rock so they look grown from the mountain, with rows of warm golden glowing windows, small torches and braziers along a winding stone road, the hall clearly vast and cavernous inside; warm, welcoming light, no large fire, spanning a large part of the mountain face, into the forested foothill ridge in the middle distance, far below the peak. Replace the houses in the lower part of the frame with pine forest. Change the light to golden hour with a deep navy upper sky fading to gold at the horizon. Keep the real mountains' shapes exactly as they are. Add no text, letters or signs.",
        "scene": {**EDITS_BASE, "background_setting": 'Pikes Peak, the pink-granite summit seen from Colorado Springs, Colorado, exactly as it is, above forested foothills',
                   "objects": [{"description": 'a massive, original mountain fortress carved into the heart of the mountain: a monumental stone facade with tall columns and a great arched doorway, towers, halls and terraces rising out of the cliffs at many levels and spread across the whole mountainside, carved from the same weathered rock so they look grown from the mountain, with rows of warm golden glowing windows, small torches and braziers along a winding stone road, the hall clearly vast and cavernous inside; warm, welcoming light, no large fire', "location": 'the forested foothill ridge in the middle distance, far below the peak', "relationship": "carved into the mountain itself", "relative_size": "very large within frame"}]},
    },
    "legallas": {
        "photo": "longs-peak-meeker-pd.jpg", "crop": (0.0, 0.1, 1.0, 0.767),
        "edit_instruction": "Carve a massive, original mountain fortress carved into the heart of the mountain: a monumental stone facade with tall columns and a great arched doorway, towers, halls and terraces rising out of the cliffs at many levels and spread across the whole mountainside, carved from the same weathered rock so they look grown from the mountain, with rows of warm golden glowing windows, small torches and braziers along a winding stone road, the hall clearly vast and cavernous inside; warm, welcoming light, no large fire, spanning a large part of the mountain face, into the base of the dark forested ridge in the lower third of the frame, small against the peaks behind it. Remove the rooftop and any buildings. Change the light to golden hour with a deep navy upper sky fading to gold at the horizon. Leave Longs Peak, with its flat summit and sheer east face, and Mount Meeker beside it, completely unchanged in shape and position; the gateway must not touch either peak. Add no text, letters or signs.",
        "scene": {**EDITS_BASE, "background_setting": 'Longs Peak and Mount Meeker on the Colorado Front Range, exactly as they are, above a dark forested ridge',
                   "objects": [{"description": 'a massive, original mountain fortress carved into the heart of the mountain: a monumental stone facade with tall columns and a great arched doorway, towers, halls and terraces rising out of the cliffs at many levels and spread across the whole mountainside, carved from the same weathered rock so they look grown from the mountain, with rows of warm golden glowing windows, small torches and braziers along a winding stone road, the hall clearly vast and cavernous inside; warm, welcoming light, no large fire', "location": 'the base of the dark forested ridge in the lower third, far below the peaks', "relationship": "carved into the mountain itself", "relative_size": "very large within frame"}]},
    },
})


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


@app.local_entrypoint()
def edit_all(cards: str = "brand,claudius,link,legallas", seed: int = 11):
    here = pathlib.Path(__file__).parent
    out = here / "out"; out.mkdir(exist_ok=True)
    names = cards.split(",")
    args = [((here / "src" / EDITS[c]["photo"]).read_bytes(), EDITS[c]["crop"],
             json.dumps({**EDITS[c]["scene"], "edit_instruction": EDITS[c]["edit_instruction"]}, ensure_ascii=False), seed) for c in names]
    log = []
    for c, res in zip(names, Fibo().edit.starmap(args)):
        (out / f"{c}-edit-{seed}.png").write_bytes(res["png"])
        log.append({"card": c, "seed": seed, "mode": "edit", "photo": EDITS[c]["photo"], "attribution_status": res["attribution_status"], "attribution": res["attribution"]})
        print(c, seed, "edit attribution", res["attribution_status"])
    runs = out / "runs.json"
    old = json.loads(runs.read_text()) if runs.exists() else []
    runs.write_text(json.dumps(old + log, indent=1) + "\n")


@app.local_entrypoint()
def edit_main(card: str = "coloradostartups.org", seed: int = 11):
    e = EDITS[card]
    here = pathlib.Path(__file__).parent
    out = here / "out"; out.mkdir(exist_ok=True)
    prompt = json.dumps({**e["scene"], "edit_instruction": e["edit_instruction"]}, ensure_ascii=False)
    res = Fibo().edit.remote((here / "src" / e["photo"]).read_bytes(), e["crop"], prompt, seed)
    (out / f"{card}-edit-{seed}.png").write_bytes(res["png"])
    runs = out / "runs.json"
    old = json.loads(runs.read_text()) if runs.exists() else []
    runs.write_text(json.dumps(old + [{"card": card, "seed": seed, "mode": "edit", "photo": e["photo"], "attribution_status": res["attribution_status"], "attribution": res["attribution"]}], indent=1) + "\n")
    print(card, seed, "edit attribution", res["attribution_status"])


# The wordmark, composited after (decision 37: no text inside the art). Aileron ships with FIBO 2.0's own files.
# The third field rides on the card itself: a shared card travels without its README, so the AI-made label
# (decision 8) and the photo credit (CC BY, CC BY-SA) must too. Full credits with links: dist/README.md.
CARD_TEXT = {
    "coloradostartups.org": ("Colorado Startups", "Colorado founders, in good company.", "AI-made image from a public-domain photo by Jimbo Herndan"),
    "brand": ("Colorado Startups", "The open-source brand", "AI-made image from a photo by James St. John, CC BY 2.0"),
    "claudius": ("Claudius", "A Colorado Startups project", "AI-made image from a photo by KimonBerlin. Photo and card: CC BY-SA 2.0"),
    "link": ("Link", "A Colorado Startups project", "AI-made image from a photo by Huttarl, CC BY 2.5"),
    "legallas": ("Legallas", "A Colorado Startups project", "AI-made image from a public-domain photo"),
}


@app.function(image=image, volumes={"/cache": weights}, secrets=[modal.Secret.from_name("fibo-hf")], timeout=600)
def compose(png: bytes, title: str, subtitle: str, credit: str) -> bytes:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    from huggingface_hub import hf_hub_download
    font = hf_hub_download("briaai/Fibo-2.0-dev", "Aileron-Regular.otf", subfolder="fonts", cache_dir="/cache")
    img = Image.open(io.BytesIO(png)).convert("RGB").resize((1280, 640), Image.LANCZOS)
    big, small = ImageFont.truetype(font, 76), ImageFont.truetype(font, 34)
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(shadow)
    for f, y, t in ((big, 72, title), (small, 168, subtitle)):
        d.text((76, y + 3), t, font=f, fill=(0, 10, 40, 200))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    img = Image.alpha_composite(img.convert("RGBA"), shadow); d = ImageDraw.Draw(img)
    d.rectangle((76, 56, 196, 62), fill=(195, 0, 47, 255))
    d.text((76, 72), title, font=big, fill=(255, 255, 255, 255))
    d.text((76, 168), subtitle, font=small, fill=(255, 238, 190, 255))
    # Credit chip, bottom right: navy at 72% keeps cream text above 4.5:1 even over the brightest gold sky.
    tiny = ImageFont.truetype(font, 17)
    x0, y0, x1, y1 = d.textbbox((0, 0), credit, font=tiny)
    w, h = x1 - x0 + 24, y1 - y0 + 14
    chip = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(chip).rounded_rectangle((1280 - 20 - w, 640 - 18 - h, 1280 - 20, 640 - 18), radius=8, fill=(0, 10, 40, 184))
    img = Image.alpha_composite(img, chip); d = ImageDraw.Draw(img)
    d.text((1280 - 20 - w + 12 - x0, 640 - 18 - h + 7 - y0), credit, font=tiny, fill=(255, 238, 190, 255))
    buf = io.BytesIO(); img.convert("RGB").save(buf, "JPEG", quality=88, optimize=True, progressive=True)
    return buf.getvalue()


@app.local_entrypoint()
def compose_all(seed: int = 11):
    here = pathlib.Path(__file__).parent
    out = here / "out"; cards = here.parent.parent / "dist" / "social"; cards.mkdir(parents=True, exist_ok=True)
    names = [c for c in CARD_TEXT if (out / f"{c}-edit-{seed}.png").exists()]
    for c, jpg in zip(names, compose.starmap([((out / f"{c}-edit-{seed}.png").read_bytes(), *CARD_TEXT[c]) for c in names])):
        (cards / f"{c}.jpg").write_bytes(jpg)
        print(c, len(jpg) // 1024, "KB")
