"""art/render/fibo_cards.py: the brand's FIBO 2.0 art, rendered on Modal (decisions 31, 35, 37, 39).

Lane: Modal's included credit, an L40S. Weights: briaai/Fibo-2.0-dev, gated (Modal Secret fibo-hf). Every image is
sent to Bria's attribution API (Modal Secret fibo-bria), which keeps commercial use covered under the FIBO 2 Free
plan and counts one call. Reserve the calls first: python3 tools/fibo_budget.py reserve N.
  modal run art/render/fibo_cards.py::edit_all --cards boulder,golden --seed 31      place art, edits of real photos
  modal run art/render/fibo_cards.py::character --cards claudius --seed 7            project characters
  modal run art/render/fibo_cards.py::compose_all --seed 31 --cards-only brand       wordmark, label, credit -> dist/social
Raw renders and art/render/out/runs.json (every call's Bria attribution id) land in art/render/out/.
"""
import base64, io, json, pathlib
import modal

app = modal.App("brand-fibo-cards")
weights = modal.Volume.from_name("fibo-weights", create_if_missing=True)
image = (modal.Image.debian_slim(python_version="3.12")
         .pip_install("diffusers>=0.42.0", "torch", "torchvision", "transformers", "accelerate", "requests", "pillow"))

# Bria's recommended text-to-image negative (Fibo-2.0-dev model card) with text, titles and watermarks added.
NEGATIVE = json.dumps({"short_description": "", "objects": [{"description": "the main subject", "texture": "smooth, featureless, plastic-like, airbrushed, no fine surface detail", "appearance_details": "soft blurred edges, simplified shapes, no fine detail"}], "background_setting": "a plain seamless studio backdrop, featureless", "lighting": {}, "aesthetics": {"artifacts": ["visible text", "caption", "title", "letters", "words", "watermark", "logo", "signage", "oversaturated colours", "neon colour cast", "overexposed highlights", "lens flare", "slight blur", "haze"]}, "photographic_characteristics": {"depth_of_field": "shallow, heavy bokeh", "focus": "soft, out of focus"}, "style_medium": "", "context": "", "artistic_style": ""})




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
        import torch
        img = self.pipe(prompt=prompt, negative_prompt=NEGATIVE, width=1440, height=720, num_inference_steps=50, guidance_scale=5.0, fonts=self.fonts,
                        generator=torch.Generator("cuda").manual_seed(seed)).images[0]
        return self._attribute(img)


NEGATIVE_EDIT = json.dumps({"short_description": "", "objects": [], "background_setting": "", "lighting": {}, "aesthetics": {}, "photographic_characteristics": {}, "style_medium": "", "context": "", "artistic_style": ""})

# Place art (Paul, 2026-11-13): each real landmark blended with its paired city from the influences (decision 30),
# so a viewer sees both at once ("that's the Flatirons, and that's the dragon city"). Borrowed and blended, never a
# copy: the archetype's cues, with no crest, emblem, exact building or name from any franchise.
#   Boulder (Photon Mountain)       Flatirons      + Valdrakken  dragons
#   Golden (Photon Mountain)        Table Mountain + Ironforge   dwarves and gnomes, the School of Mines
#   Denver (Photon Mountain)        skyline        + Stormwind   humans
#   Colorado Springs (Space Peak)   Pikes Peak     + Aerie Peak  gryphon-riding dwarves and gnome flying machines
#   Fort Collins (Fusion Canyon)    Poudre Canyon  + Gnomeregan  gnome science
DRAGONS = ("a soaring dragon city built onto the mountain: tall terraces and slender towers of pale stone with gold domes and "
           "teal and crimson roofs climbing between the rock slabs, vast open stone landing platforms and great arched roosts "
           "where huge dragons perch, two great dragons gliding above the slabs, crystal lanterns and beams of warm golden "
           "light, elegant artisans' halls, luminous and majestic; warm and welcoming")
DWARVES = ("a colossal dwarven mountain city carved into the heart of the mountain: a gigantic gate of angular, square-cut "
           "dwarven stonework set deep into the rock, flanked by two colossal stone statues of bearded dwarf warriors leaning "
           "on great war hammers, a broad stone stairway and causeway climbing to it, massive iron-banded doors standing open "
           "with warm molten forge light pouring out, heavy square towers and terraced halls climbing the rock face with rows "
           "of warm golden windows, mine headframes and ore carts, gnome clockwork lifts and brass gears beside the gate, "
           "braziers and small torches, plain crimson and gold banners, light snow on the ledges, all carved from the "
           "mountain's own rock; warm and welcoming, no large fire")
HUMANS = ("a grand white-stone human capital: high white walls and round towers with deep blue slate roofs, a great keep "
          "with tall spires, stone bridges over canals, plain blue and gold banners, warm lamplit windows; majestic and welcoming")
GRYPHONS = ("a high dwarven aerie on the mountain: halls and towers of stone and timber carved into the upper cliffs, great "
            "stone roosts where gryphons nest and launch, gryphons in flight around the peak, small gnome flying machines "
            "and gyrocopters circling, rope lifts and wooden platforms, warm windows and braziers, plain green and gold "
            "banners; adventurous and welcoming")
GNOMES = ("a bright gnome city of science built into both canyon walls: brass and steel workshops with round porthole "
          "windows, great gears and water wheels turned by the river, pipes, catwalks and lifts spanning the canyon, glowing "
          "teal-blue energy cores, small gyrocopters, warm windows; clever, bright and welcoming")


def place(photo, crop, city, where, extra, landmark, background):
    return {"photo": photo, "crop": crop,
            "edit_instruction": f"Blend in {city}, built into {where}. {extra} Change the light to golden hour with a deep navy upper sky fading to gold at the horizon. Keep {landmark} exactly as it is and clearly recognisable. Add no text, letters or signs.",
            "scene": {
                "short_description": f"{background.split(':')[0]} at golden hour, blended with a fantasy city built into the landscape",
                "objects": [{"description": city, "location": where, "relationship": "built into the real place, which stays recognisable", "relative_size": "very large within frame"}],
                "background_setting": background,
                "lighting": {"conditions": "golden hour, warm golden window light from the city", "direction": "low sun from the left, warm light from the windows", "shadows": "long and warm"},
                "aesthetics": {"composition": "wide 2:1 landscape, the landmark and the city centred, calm sky across the top", "color_scheme": "deep navy upper sky (#001970) fading to warm gold (#ffd100), the place's own colours, dark pine green (#245d38), warm golden window light", "mood_atmosphere": "grand, warm, welcoming, inviting"},
                "photographic_characteristics": {"depth_of_field": "deep", "focus": "sharp throughout", "camera_angle": "eye-level", "lens_focal_length": "standard"},
                "style_medium": "photograph, photorealistic", "text_render": [],
                "context": "fantasy place art for a Colorado founders community; the image contains no text",
                "artistic_style": "photorealistic, cinematic"}}


EDITS = {
    "boulder": place("flatirons-2007-pd.jpg", (0.07, 0.22, 1.0, 0.84), DRAGONS,
                     "the mountain between and below the tilted Flatirons slabs, with dragons perched on top of the slabs",
                     "Remove the stadium floodlight tower at the left edge.",
                     "the Flatirons' tilted red-brown rock slabs and the mountain's outline",
                     "the Flatirons above Boulder, Colorado: tilted red-brown sandstone slabs on the forested east face of Green Mountain, with leafy trees in the foreground"),
    "golden": place("table-mountains-golden-ccby.jpg", (0.1, 0.05, 0.9, 0.79), DWARVES,
                    "the steep flank of South Table Mountain on the right, below its basalt cap",
                    "Replace the golf course in the foreground with natural grassland and sandstone.",
                    "both mesas' flat basalt-capped outlines",
                    "North and South Table Mountains above Golden, Colorado: two flat-topped mesas with dark basalt caps and grassy slopes, sandstone outcrops in the foreground"),
    "denver": place("denver-skyline-usfws-pd.jpg", (0.4, 0.25, 1.0, 0.701), HUMANS,
                    "the downtown skyline and the plain in front of it, the keep rising where the tallest towers stand, so the skyline's outline stays recognisable",
                    "Keep the golden cottonwood trees and the grassland in the foreground.",
                    "the Front Range mountains behind the city",
                    "Downtown Denver, Colorado: the city's towers on the plain, with the Front Range mountains rising behind and golden cottonwoods in the foreground"),
    "springs": place("pikes-peak-colorado-springs-ccby.jpg", (0.0, 0.0, 1.0, 0.667), GRYPHONS,
                     "the upper slopes of Pikes Peak below the summit",
                     "Replace the houses in the lower part of the frame with pine forest.",
                     "the summit of Pikes Peak, its pink granite, its snow and its outline",
                     "Pikes Peak above Colorado Springs, Colorado: the broad pink-granite summit with snowfields above forested foothills"),
    "fortcollins": place("poudre-canyon-greyrock-ccby.jpg", (0.0, 0.15, 1.0, 0.8167), GNOMES,
                         "both walls of the canyon, with a clear mountain river running along the canyon floor",
                         "Add the river along the canyon floor.",
                         "the canyon's rocky walls, its ridgelines and its pines",
                         "Poudre Canyon west of Fort Collins, Colorado: steep granite canyon walls with ponderosa pines and a far ridge"),
}


def log_runs(out, entries):
    runs = out / "runs.json"
    rows = (json.loads(runs.read_text()) if runs.exists() else []) + entries
    runs.write_text("[\n" + ",\n".join(json.dumps(r) for r in rows) + "\n]\n")


@app.local_entrypoint()
def edit_all(cards: str = "boulder,golden,denver,springs,fortcollins", seed: int = 11):
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
    log_runs(out, log)


# Each project repo's card is its own character (Paul, 2026-11-13). Borrow and blend: the look of the named
# influences (decision 30) mixed with Colorado, never a copy of one character, emblem or signature item.
CHAR_STYLE = {
    "lighting": {"conditions": "warm golden-hour light with a soft rim light on the character", "direction": "key light from the right, warm fill from below", "shadows": "soft and warm"},
    "photographic_characteristics": {"depth_of_field": "medium, background softly detailed", "focus": "sharp on the character", "camera_angle": "eye-level", "lens_focal_length": "portrait"},
    "style_medium": "cinematic fantasy character key art, highly detailed realistic digital painting", "text_render": [],
    "context": "a social media preview card for an open-source project; text is added later, so the image contains no text, letters, logos, emblems or signage",
    "artistic_style": "epic fantasy, painterly realism, rich detail, warm and heroic",
}
CHARACTERS = {
    "claudius": {
        "short_description": "Claudius, a gnome engineer and loyal companion, in a cosy gnome workshop in a green Colorado river canyon",
        "objects": [{"description": "a small, sturdy, kind-faced gnome engineer and loyal companion with large pointed ears, a big friendly nose, curly sandy-brown hair and a short trimmed beard, brass goggles pushed up on his forehead, a brass mechanical gauntlet on his right hand, rolled-up sleeves and a leather waistcoat, a tool belt of small brass gadgets, a travelling pack with a coil of grey rope and a small cooking pan hanging from it, holding up a thin slate of glowing blue light with lines of light flowing across it, a helpful agent at work, a warm, steady, loyal smile",
                     "location": "right half, waist up", "relationship": "the hero of the frame, in his workshop", "relative_size": "large within frame"}],
        "background_setting": "a cosy gnome workshop built into a green river canyon: a round wooden door and round windows, brass gears, pipes and softly glowing teal energy cores, a small vegetable garden, warm lamplight, the canyon wall and pines beyond",
        "aesthetics": {"composition": "wide 2:1; the gnome in the right half; the left 45 percent is the calm, softly lit depth of the workshop and canyon", "color_scheme": "deep navy shadows (#001970), warm gold lamplight (#ffd100), brass, garden green, the blue glow of the slate and teal cores", "mood_atmosphere": "warm, loyal, clever, homely"},
        **CHAR_STYLE},
    "link": {
        "short_description": "Linken, a small gnome warrior hero, on a trail in the red-rock foothills of Colorado",
        "objects": [{"description": "a small, sturdy gnome warrior hero with large pointed ears, a big friendly nose, bright eyes and tousled sandy-blond hair, a forest-green tunic and a long green pointed cap, a brown leather belt, bracers and boots, a short sword of original design, a round wooden shield with a brass rim and a carved columbine flower, a curved wooden boomerang at his hip, a brass chain-link pendant on his chest, brave and cheerful",
                     "location": "right half, full figure", "relationship": "the hero of the frame, on the trail", "relative_size": "large within frame"}],
        "background_setting": "Colorado's Front Range foothills: tilted red sandstone slabs, golden aspens and dark pines, a winding dirt trail, a wide open sky",
        "aesthetics": {"composition": "wide 2:1; the gnome hero in the right half; the left 45 percent is open sky above soft distant foothills", "color_scheme": "deep navy upper sky (#001970) fading to gold (#ffd100), forest green, red sandstone, aspen gold", "mood_atmosphere": "adventurous, plucky, bright, a little funny"},
        **CHAR_STYLE},
    "legallas": {
        "short_description": "Legallas, an elf ranger, in a golden aspen grove below snowy Colorado peaks",
        "objects": [{"description": "a tall, graceful elf ranger with long straight platinum-blond hair, long elegant swept-back pointed ears and a calm, keen face, fitted crimson-and-gold ranger armour with burnished gold leaf-shaped plates, a grey-green elven travelling cloak fastened with an aspen-leaf clasp, an ornate recurved longbow of pale wood with gold fittings, a quiver of white-fletched arrows, twin long white-handled knives crossed at his back, a slim leather scroll case at the hip",
                     "location": "right half, waist up", "relationship": "the hero of the frame, among the aspens", "relative_size": "large within frame"}],
        "background_setting": "a high Colorado aspen grove in autumn gold, white trunks, snow-capped Front Range peaks beyond",
        "aesthetics": {"composition": "wide 2:1; the ranger in the right half; the left 45 percent is soft gold aspens and sky", "color_scheme": "deep navy upper sky (#001970), aspen gold (#ffd100), crimson and gold armour, grey-green cloak, white aspen bark", "mood_atmosphere": "graceful, vigilant, noble"},
        **CHAR_STYLE},
}


@app.local_entrypoint()
def character(cards: str = "claudius", seed: int = 7):
    """modal run art/render/fibo_cards.py::character --cards claudius,link,legallas --seed 7  (one FIBO call per card)"""
    out = pathlib.Path(__file__).parent / "out"; out.mkdir(exist_ok=True)
    names = cards.split(",")
    log = []
    for c, res in zip(names, Fibo().render.starmap([(json.dumps(CHARACTERS[c], ensure_ascii=False), seed) for c in names])):
        (out / f"{c}-char-{seed}.png").write_bytes(res["png"])
        log.append({"card": c, "seed": seed, "mode": "character", "attribution_status": res["attribution_status"], "attribution": res["attribution"]})
        print(c, seed, "character attribution", res["attribution_status"])
    log_runs(out, log)


# The wordmark, composited after (decision 37: no text inside the art). Aileron ships with FIBO 2.0's own files.
# The third field rides on the card itself: a shared card travels without its README, so the AI-made label
# (decision 8) and the photo credit (CC BY, CC BY-SA) must too. Full credits with links: dist/README.md.
CARD_TEXT = {
    "coloradostartups.org": ("Colorado Startups", "Colorado founders, in good company.", "AI-made image from a public-domain photo by Jimbo Herndan"),
    "brand": ("Colorado Startups", "The open-source brand", "AI-made image from a photo by James St. John, CC BY 2.0"),
    "claudius": ("Claudius", "A Colorado Startups project", "AI-made image"),
    "link": ("Linken", "A Colorado Startups project", "AI-made image"),
    "legallas": ("Legallas", "A Colorado Startups project", "AI-made image"),
}
CARD_ART = {"coloradostartups.org": "boulder-edit", "brand": "golden-edit", "claudius": "claudius-char", "link": "link-char", "legallas": "legallas-char"}


@app.function(image=image, volumes={"/cache": weights}, secrets=[modal.Secret.from_name("fibo-hf")], timeout=600)
def compose(png: bytes, title: str, subtitle: str, credit: str, prov: dict) -> bytes:
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
    return with_provenance(buf.getvalue(), prov)


# Decision 8: model-made images keep their AI-made label in metadata. Only the IPTC AI fields and the art namespace,
# the provenance packet tools/vendor/export_scan.py accepts (#691); no EXIF, no camera or location data.
def with_provenance(jpg: bytes, prov: dict) -> bytes:
    from xml.sax.saxutils import quoteattr
    iptc = "http://cv.iptc.org/newscodes/digitalsourcetype/"
    attrs = {"Iptc4xmpExt:DigitalSourceType": iptc + prov["type"], "Iptc4xmpExt:AISystemUsed": "FIBO 2.0 (Bria), briaai/Fibo-2.0-dev",
             "csart:Seed": str(prov["seed"]), "csart:Source": prov["source"], "csart:ModelLicense": "Bria FIBO 2 Free plan"}
    packet = ('<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
              '<rdf:Description rdf:about="" xmlns:Iptc4xmpExt="http://iptc.org/std/Iptc4xmpExt/2008-02-29/" '
              'xmlns:csart="https://coloradostartups.org/ns/art/1.0/" '
              + " ".join(f"{k}={quoteattr(v)}" for k, v in attrs.items()) + "/></rdf:RDF></x:xmpmeta>").encode()
    seg = b"http://ns.adobe.com/xap/1.0/\x00" + packet
    at = 4 + int.from_bytes(jpg[4:6], "big") if jpg[2:4] == b"\xff\xe0" else 2  # after the JFIF header
    return jpg[:at] + b"\xff\xe1" + (len(seg) + 2).to_bytes(2, "big") + seg + jpg[at:]


@app.local_entrypoint()
def compose_all(seed: int = 11, cards_only: str = ""):
    here = pathlib.Path(__file__).parent
    out = here / "out"; cards = here.parent.parent / "dist" / "social"; cards.mkdir(parents=True, exist_ok=True)
    src = {c: out / f"{CARD_ART[c]}-{seed}.png" for c in (cards_only.split(",") if cards_only else CARD_TEXT)}
    names = [c for c, p in src.items() if p.exists()]
    def prov(c):
        art = CARD_ART[c].rsplit("-", 1)
        if art[1] == "edit":
            return {"type": "compositeWithTrainedAlgorithmicMedia", "seed": seed, "source": f"edit of art/render/src/{EDITS[art[0]]['photo']}"}
        return {"type": "trainedAlgorithmicMedia", "seed": seed, "source": "text to image"}
    for c, jpg in zip(names, compose.starmap([(src[c].read_bytes(), *CARD_TEXT[c], prov(c)) for c in names])):
        (cards / f"{c}.jpg").write_bytes(jpg)
        print(c, len(jpg) // 1024, "KB")
