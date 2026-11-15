"""art/render/fibo_cards.py: the brand's FIBO 2.0 art (decisions 31, 35, 37, 39, 41).

Lanes: the ZeroGPU Space paul-co-startups/brand-fibo (art/render/space/, on HF PRO's daily quota) first; Modal's
included credit, an L40S, as the fallback. Weights: briaai/Fibo-2.0-dev, gated. Every image is sent to Bria's
attribution API, which keeps commercial use covered under the FIBO 2 Free plan and counts one call. Reserve the calls
first: python3 tools/fibo_budget.py reserve N. Space (R is uv run --no-project --with modal==1.6.3 --with
gradio_client==2.7.2 --with pillow python3; Modal is the same with `modal run art/render/fibo_cards.py::<entry>`):
  R art/render/fibo_cards.py edit_all --cards boulder,golden --seed 31        place art, edits of real photos
  R art/render/fibo_cards.py character --cards claudius --seed 7              project characters
  R art/render/fibo_cards.py compose_all --cards-only brand                   wordmark only -> dist/social
Place art since decision 43: R ... painted --cards golden --leans game --seed 43, then R ... places.
Raw renders and art/render/out/runs.json (every call's Bria attribution id) land in art/render/out/.
"""
import base64, io, json, os, pathlib, sys, tempfile
import modal

app = modal.App("brand-fibo-cards")
SPACE, SIZE, STEPS, GUIDANCE = "paul-co-startups/brand-fibo", (1440, 720), 50, 5.0
VGL, EDIT_STEPS, EDIT_GUIDANCE = "briaai/Fibo-2.0-editing", 4, 1.0  # Bria's editing method (decision 41)
LANE = "modal"  # "space" when run with python3, below
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
        src = src.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h))).resize(SIZE, Image.LANCZOS)
        img = self.pipe(prompt=prompt, negative_prompt=NEGATIVE_EDIT, image=src, num_inference_steps=STEPS, guidance_scale=GUIDANCE,
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
        img = self.pipe(prompt=prompt, negative_prompt=NEGATIVE, width=SIZE[0], height=SIZE[1], num_inference_steps=STEPS, guidance_scale=GUIDANCE, fonts=self.fonts,
                        generator=torch.Generator("cuda").manual_seed(seed)).images[0]
        return self._attribute(img)


NEGATIVE_EDIT = json.dumps({"short_description": "", "objects": [], "background_setting": "", "lighting": {}, "aesthetics": {}, "photographic_characteristics": {}, "style_medium": "", "context": "", "artistic_style": ""})

# Place art (Paul, 2026-11-13): each real landmark blended with its paired city from the influences (decision 30),
# so a viewer sees both at once ("that's the Flatirons, and that's the dragon city"). Borrowed and blended, never a
# copy: the archetype's cues, with no crest, emblem, exact building or name from any franchise.
#   Boulder (Photon Mountain)       Flatirons      + Valdrakken + Rivendell          dragons and elves
#   Golden (Photon Mountain)        Table Mountain + Ironforge  + Erebor             dwarves and gnomes, the School of Mines
#   Denver (Photon Mountain)        skyline        + Stormwind  + Edoras             men
#   Colorado Springs (Space Peak)   Pikes Peak     + Aerie Peak + the Eagles' eyrie  gryphons, eagles, gnome flying machines
#   Fort Collins (Fusion Canyon)    Poudre Canyon  + Gnomeregan + the Shire          gnomes and hobbits
# (decisions 39 and 40)
DRAGONS = ("a single luminous city of elves and dragon-folk built onto the mountain in one shared style: pale stone and "
           "gold, flowing leaf-like arches, slender towers with gold domes and teal and crimson roofs, elven halls and slender "
           "bridges over small waterfalls, wide stone terraces and landing platforms; high elves with long fair hair in flowing "
           "robes and dragon-folk (upright, horned, scaled humanoids with small wings) walking the terraces and bridges; and "
           "only three massive dragons: a huge long serpentine green dragon without wings flying in a great S-curve through "
           "the sky above the slabs, its horned, bearded head and face clearly visible and its tail tapering to a fine tip, a "
           "great winged dragon with scales the red-brown and ochre of the Flatirons sandstone perched on a slab, and a "
           "white-and-gold winged dragon glowing softly with light; a refuge of learning, majestic, warm and welcoming")
DWARVES = ("a colossal dwarven mountain kingdom carved into the heart of the mountain: a gigantic gate of angular, square-cut "
           "dwarven stonework set deep into the rock, flanked by two colossal stone statues of bearded dwarf kings leaning "
           "on great war hammers, a clear stream flowing out from beneath the gate, a broad stone stairway and causeway "
           "climbing to it, massive iron-banded doors standing open with warm golden light and glints of gold pouring out, "
           "heavy square towers and terraced halls climbing the rock face with rows of warm golden windows, mine headframes "
           "and ore carts, gnome clockwork lifts and brass gears beside the gate, braziers and small torches, plain crimson "
           "and gold banners, light snow on the ledges, all carved from the mountain's own rock; warm and welcoming, no large fire")
HUMANS = ("one grand citadel of men that blends two styles into a single building: a white stone keep with square towers "
          "and deep blue slate roofs, whose great central hall is built of carved timber with a shining golden roof and "
          "horse-head gables, standing on a green hill on the plain in front of the city, with stone bridges, horses and "
          "riders on the open plain, plain blue, green and gold banners and warm lamplit windows; majestic, sturdy and welcoming")
GRYPHONS = ("a high dwarven aerie on the mountain: halls and towers of stone and timber carved into the upper cliffs, great "
            "stone roosts where gryphons nest and launch; dwarves with braided beards and gnomes in goggles walking the timber "
            "walkways, terraces and rope bridges, clearly visible; four gryphons in flight, each a four-legged beast with the "
            "head, wings and front talons of an eagle and the tawny body, hind legs and tufted tail of a lion, and two giant "
            "golden eagles with all-dark-brown plumage and golden napes; no other birds; small gnome flying machines and "
            "gyrocopters circling, rope lifts and wooden platforms, warm windows and braziers, plain green and gold banners; "
            "adventurous and welcoming")
GNOMES = ("a bright village of gnome science and hobbit homes along both canyon walls: brass and steel workshops with round "
          "porthole windows, great gears and water wheels turned by the river, pipes, catwalks and lifts spanning the canyon, "
          "glowing teal-blue energy cores, small gyrocopters, and lower down round green and yellow doors set into grassy "
          "banks, flower and vegetable gardens, a stone bridge over the river and a cosy inn with warm windows; clever, "
          "homely and welcoming")


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
                     "Remove the stadium floodlight tower at the left edge. Show only three dragons, none black; the green serpent dragon flies in the sky with its whole body, head and face visible, like the creature in the second reference image.",
                     "the Flatirons' tilted red-brown rock slabs and the mountain's outline",
                     "the Flatirons above Boulder, Colorado: tilted red-brown sandstone slabs on the forested east face of Green Mountain, with leafy trees in the foreground"),
    "golden": place("table-mountains-golden-ccby.jpg", (0.1, 0.05, 0.9, 0.79), DWARVES,
                    "the steep flank of South Table Mountain on the right, below its basalt cap",
                    "Replace the golf course in the foreground with natural grassland and sandstone.",
                    "both mesas' flat basalt-capped outlines",
                    "North and South Table Mountains above Golden, Colorado: two flat-topped mesas with dark basalt caps and grassy slopes, sandstone outcrops in the foreground"),
    "denver": place("denver-skyline-usfws-pd.jpg", (0.4, 0.25, 1.0, 0.701), HUMANS,
                    "the green plain in front of the downtown skyline, so the city's towers stay clearly visible behind it",
                    "Build one citadel only, never two separate castles, and keep the downtown towers clearly visible behind it. Keep the golden cottonwood trees and the grassland in the foreground.",
                    "the Front Range mountains behind the city",
                    "Downtown Denver, Colorado: the city's towers on the plain, with the Front Range mountains rising behind and golden cottonwoods in the foreground"),
    "springs": place("pikes-peak-colorado-springs-ccby.jpg", (0.0, 0.0, 1.0, 0.667), GRYPHONS,
                     "the upper slopes of Pikes Peak below the summit",
                     "Replace the houses in the lower part of the frame with pine forest. Every flying creature is either a four-legged gryphon like the creature in the second reference image or a giant golden eagle; no other birds. Show dwarves and gnomes walking the walkways, and gnome gyrocopters in the air.",
                     "the summit of Pikes Peak, its pink granite, its snow and its outline",
                     "Pikes Peak above Colorado Springs, Colorado: the broad pink-granite summit with snowfields above forested foothills"),
    "fortcollins": place("poudre-canyon-greyrock-ccby.jpg", (0.0, 0.15, 1.0, 0.8167), GNOMES,
                         "both walls of the canyon, with a clear mountain river running along the canyon floor",
                         "Add the river along the canyon floor.",
                         "the canyon's rocky walls, its ridgelines and its pines",
                         "Poudre Canyon west of Fort Collins, Colorado: steep granite canyon walls with ponderosa pines and a far ridge"),
}
# From scratch (decision 42), following Bria's FIBO 2.0 prompting guidance (docs.bria.ai/vgl, Bria-AI/vgl best
# practices): each element named with its look and action, counts stated, "keep everything else unchanged". A mask
# freezes the real landmark: `keep` is the landmark's outline as fractions of the crop (black, kept exactly); the
# rest is white and may change. Creatures the model cannot draw from words get a second, unmasked pass from an
# original reference image (`creatures`), the way Bria's own editing Space takes references as <image_2>.
SCRATCH = {
    "boulder": "In the masked areas, add a luminous city of high elves and dragon-folk on the forested slopes and meadow below the Flatirons: terraces of pale stone with gold domes and slender towers with teal and crimson roofs, graceful elven halls with tall pointed arches and leaf-like carvings, arched stone bridges over small waterfalls, and wide landing platforms. On the bridges and terraces, add a few high elves with long fair hair in flowing ivory and green robes, walking, and a few dragon-folk, upright horned scaled humanoids with small folded wings, walking among them. Add one great winged dragon with red-brown and ochre scales like the sandstone, perched on a platform at the right, and one white-and-gold winged dragon glowing softly with light, gliding in the sky. Turn the sky to warm late-afternoon gold fading to deep navy at the top. Keep everything else unchanged, especially the Flatirons rock slabs and the mountain.",
    "golden": "In the masked areas, carve a colossal dwarven kingdom into the lower flank of South Table Mountain on the right: a gigantic gate of angular, square-cut stone with iron-banded doors standing open and warm golden light inside, flanked by two colossal stone statues of helmeted dwarf kings with braided beards, each leaning on a great war hammer, a broad stone stairway climbing to the gate, a clear stream flowing out from beneath it, terraced halls with rows of warm windows, mine headframes, ore carts on rails and brass gnome lifts beside the gate, and plain crimson and gold banners. Add a few dwarves with braided beards and a few gnomes in goggles working by the carts. Replace the golf course and houses in the foreground with natural grassland and sandstone. Turn the sky to warm late-afternoon gold fading to deep navy at the top. Keep everything else unchanged, especially both flat-topped mesas and their basalt caps.",
    "denver": "In the masked areas, on a green hill in the right foreground in front of the city, add one grand citadel that blends two styles into a single building: a white stone keep with square towers and deep blue slate roofs, whose great central hall is carved timber with a shining golden roof and horse-head gables. Add a stone road winding up to it, plain blue, green and gold banners, and a few riders on horses on the open grassland in the foreground. Keep the downtown towers, the mountains and the golden cottonwood at the left exactly as they are and clearly visible. Keep everything else unchanged.",
    "springs": "In the masked areas, on the forested crags in the foreground below Pikes Peak, add a high dwarven aerie: halls and towers of stone and timber carved into the rocks, wooden walkways and rope bridges between them, great stone roosts, warm windows and braziers, and plain green and gold banners. On the walkways, add a few stout dwarves with braided beards and a few small gnomes in goggles, walking. Add two giant golden eagles, all dark brown with golden napes, one perched on a high roost and one flying, and three small gnome gyrocopters in the sky. Replace the houses at the bottom with pine forest. Turn the sky to warm late-afternoon gold fading to deep navy at the top. Keep everything else unchanged, especially Pikes Peak and its snowfields.",
    "fortcollins": "In the masked areas, add a village of gnome science and hobbit homes along the canyon floor and lower slopes: brass and steel workshops with round porthole windows, great gears and a water wheel turned by a clear mountain river running down the canyon floor, pipes, catwalks and a small lift, softly glowing teal energy cores, and among them round green and yellow doors set into grassy banks, flower and vegetable gardens, a stone bridge over the river and a cosy inn with warm windows. Add a few gnomes in goggles and a few barefoot hobbits with curly hair walking the paths, and two small gnome gyrocopters in the sky. Turn the sky to warm late-afternoon gold fading to deep navy at the top. Keep everything else unchanged, especially the canyon walls and the far ridge.",
}
KEEP = {"boulder": [[0, 0.58], [0.1, 0.56], [0.2, 0.48], [0.3, 0.42], [0.42, 0.36], [0.5, 0.33], [0.62, 0.32], [0.7, 0.34], [0.78, 0.4], [0.8, 0.55], [0.8, 0.66], [0.6, 0.68], [0.4, 0.68], [0.2, 0.7], [0, 0.7]], "golden": [[0, 0.37], [0.15, 0.35], [0.4, 0.37], [0.58, 0.42], [0.65, 0.36], [0.7, 0.35], [1.0, 0.37], [1.0, 0.46], [0.62, 0.46], [0.58, 0.56], [0, 0.56]], "denver": [[0, 0.05], [1.0, 0.05], [1.0, 0.45], [0.72, 0.45], [0.72, 0.8], [0, 0.8]], "springs": [[0, 0.25], [0.15, 0.2], [0.3, 0.15], [0.42, 0.1], [0.5, 0.08], [0.6, 0.12], [0.75, 0.18], [0.9, 0.22], [1, 0.26], [1, 0.48], [0, 0.48]], "fortcollins": [[0, 0], [0.12, 0.02], [0.2, 0.2], [0.3, 0.35], [0.4, 0.48], [0.55, 0.48], [0.65, 0.55], [0.75, 0.42], [0.9, 0.38], [1, 0.38], [1, 0.6], [0, 0.6]]}
CREATURES = {
    "boulder": ("serpent", "Put the long green serpent dragon from <image_2> into the sky of <image_1>, flying in a great S-curve above the Flatirons with its horned head and face clearly visible and its tail tapering to a fine tip. Keep everything else in <image_1> unchanged."),
    "springs": ("gryphon", "Put four gryphons like the creature in <image_2> into the sky of <image_1>, flying around the aerie: each has the head, wings and front talons of an eagle and the tawny body, hind legs and tufted tail of a lion. Keep everything else in <image_1> unchanged."),
}
for c in EDITS:
    EDITS[c]["edit_instruction"], EDITS[c]["keep"] = SCRATCH[c], KEEP[c]
REFS = {
    "stonewyrm": ("A colossal legless stone serpent, no legs and no claws: its body is a single line of about ten huge rounded "
                  "grey boulders, each as big as a house, joined one after another like beads on a string and tapering to the "
                  "tail, with thin slivers of glowing gold ore running through every boulder; its head is one great blocky "
                  "boulder with a wide jaw and small glowing gold eyes. It arcs up out of rocky ground. Hand-painted "
                  "high-fantasy illustration, bold warm colours, plain golden-hour sky background.", 29),
    "serpent": ("A colossal long serpentine green dragon without wings flying in a sweeping S-curve across a golden-hour sky, its "
                "horned, bearded head and fierce face clearly visible in three-quarter view, mossy green scales with a pale gold "
                "belly, four small clawed legs, the long body tapering to a fine tail tip. Photorealistic epic fantasy, sharp "
                "detail, plain sky background.", 11),
    "gryphon": ("A majestic gryphon in flight against a clear golden-hour sky, full body side view: a four-legged creature with "
                "the head, feathered neck, broad wings and front talons of a golden eagle, and the tawny furred body, muscular "
                "hind legs with paws and long tufted tail of a lion. Photorealistic wildlife photograph, sharp detail, plain sky "
                "background.", 7),
}


def fibo_map(method, args):
    """Fibo.<method> over args: Modal under `modal run`, else the ZeroGPU Space, which returns the same dict."""
    if LANE == "modal":  # Modal's Fibo.edit takes no reference
        return getattr(Fibo(), method).starmap([a[:4] for a in args] if method == "edit" else args)
    import httpx
    from gradio_client import Client, handle_file
    from PIL import Image
    client = Client(SPACE)  # the hf CLI's signed-in account, so its PRO quota
    def call(a):
        if method == "edit":  # Bria's method: its VGL step writes the edit JSON from the instruction, then edit-turbo
            photo, crop, prompt, seed, ref, keep, *rest = a
            size = rest[0] if rest else SIZE
            src = Image.open(io.BytesIO(photo))
            if src.mode in ("RGBA", "LA", "P"):  # a transparent logo: flatten onto white so the edit sees its shapes
                src = src.convert("RGBA"); ground = Image.new("RGB", src.size, (255, 255, 255))
                ground.paste(src, mask=src.split()[-1]); src = ground
            src = src.convert("RGB"); w, h = src.size
            src = src.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h))).resize(size, Image.LANCZOS)
            path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name; src.save(path)
            mask = None
            if keep:  # white may change, black (the landmark) is kept; feathered so the seam blends
                from PIL import ImageDraw, ImageFilter
                m = Image.new("L", size, 255); ImageDraw.Draw(m).polygon([(x * size[0], y * size[1]) for x, y in keep], fill=0)
                mask = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name; m.filter(ImageFilter.GaussianBlur(12)).save(mask)
            vgl = Client(VGL)  # Bria's public Space; its /vgl runs on Bria's token and no GPU
            def upload(p):
                r = httpx.post(vgl.upload_url, files=[("files", (pathlib.Path(p).name, open(p, "rb"), "image/png"))], headers=vgl.headers, timeout=60)
                r.raise_for_status(); return r.json()[0]
            edit = vgl.predict(json.loads(prompt)["edit_instruction"], upload(path), upload(ref) if ref else None, None, None,
                               upload(mask) if mask else None, max(seed, 1), api_name="/vgl")["json_instruction"]
            style = json.loads(prompt).get("style")
            if style:  # set the style fields directly rather than leaving them to the VGL step's paraphrase
                edit = json.loads(edit) if isinstance(edit, str) else dict(edit)
                for k, v in style.items():
                    edit[k] = {**edit[k], **v} if isinstance(v, dict) and isinstance(edit.get(k), dict) else v
            edit = edit if isinstance(edit, str) else json.dumps(edit, ensure_ascii=False)
            png, status, attribution = client.predict(handle_file(path), "[0,0,1,1]", handle_file(ref) if ref else None,
                                                      handle_file(mask) if mask else None, edit, "", seed,
                                                      *size, EDIT_STEPS, EDIT_GUIDANCE, api_name="/edit")
        else:
            prompt, seed, *rest = a
            png, status, attribution = client.predict(prompt, NEGATIVE, seed, *(rest[0] if rest else SIZE), STEPS, GUIDANCE, api_name="/render")
        return {"png": pathlib.Path(png).read_bytes(), "attribution_status": int(status), "attribution": attribution}
    return map(call, args)


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
             json.dumps({**EDITS[c]["scene"], "edit_instruction": EDITS[c]["edit_instruction"]}, ensure_ascii=False), seed,
             None, EDITS[c].get("keep")) for c in names]
    for c, res in zip(names, fibo_map("edit", args)):  # each row logged as it lands, so a failed later call loses none
        (out / f"{c}-edit-{seed}.png").write_bytes(res["png"])
        log_runs(out, [{"card": c, "seed": seed, "mode": "edit", "photo": EDITS[c]["photo"], "attribution_status": res["attribution_status"], "attribution": res["attribution"]}])
        print(c, seed, "edit attribution", res["attribution_status"])
        if c in CREATURES and LANE != "modal":  # pass 2: the referenced creatures, on pass 1's image
            (out / f"{c}-edit-{seed}-pass1.png").write_bytes(res["png"])  # kept, so a weak pass 2 reruns alone
            ref, instruction = CREATURES[c]
            res = next(iter(fibo_map("edit", [(res["png"], [0, 0, 1, 1], json.dumps({"edit_instruction": instruction}), seed,
                                                str(here / "refs" / f"{ref}.png"), None)])))
            (out / f"{c}-edit-{seed}.png").write_bytes(res["png"])
            log_runs(out, [{"card": c, "seed": seed, "mode": "edit-creatures", "ref": ref, "attribution_status": res["attribution_status"], "attribution": res["attribution"]}])
            print(c, seed, "creatures attribution", res["attribution_status"])


# Painted (decision 43, test): the whole photo repainted in one light, no mask, so the landmark and the fantasy share
# one style. One hero structure at huge scale carved into the landmark, a few tiny figures for scale, and the
# atmosphere spelled out. Two leans per place: "film" (grand, misty, naturalistic) and "game" (hand-painted,
# bold, stylized). Styles are described, never named.
LEANS = {
    "wow": "",

    "wowlike": ("Repaint this whole photo as hand-painted MMO game concept art in a stylized, heroic, slightly cartoony look: "
                "chunky exaggerated proportions, massive oversized architecture with thick stone walls, giant rivets, huge "
                "ornamental trims and bold geometric carvings, bold saturated jewel-tone colours, painterly hand-painted "
                "textures with soft highlights, stylized foliage in big leaf clumps, and warm glowing magical light, one "
                "consistent light across the whole scene."),
    "film": ("Repaint this whole photo as an epic fantasy matte painting in the grand, naturalistic style of classic fantasy "
             "film concept art: muted earthy colours, soft golden evening light with long shadows, mist in the low ground and "
             "depth haze toward the horizon, painterly brushwork, one consistent light across the whole scene."),
    "game": ("Repaint this whole photo as a hand-painted high-fantasy illustration in a stylized video-game look: bold "
             "saturated colours, chunky slightly exaggerated shapes, painterly hand-painted textures, warm magical evening "
             "light with glowing highlights, one consistent light across the whole scene."),
}
STYLE = {
    "wow": {"style_medium": "digital illustration", "artistic_style": "World of Warcraft, hand-painted, stylized"},
}
PLACE_STYLE = {  # context names the game and the transformation; aesthetics merges into the VGL step's own
    "boulder": {"context": "World of Warcraft game environment concept art: Boulder's Flatirons transformed into a night elf "
                           "and Rivendell elven city",
                "aesthetics": {"color_scheme": "night elf purples and teals with moonlit silver, golden leaves and red-brown "
                                               "sandstone", "mood_atmosphere": "epic, magical, serene"}},
    "golden": {"context": "World of Warcraft game environment concept art: Golden's Table Mountain transformed into an "
                          "Ironforge and Erebor dwarven kingdom",
               "aesthetics": {"color_scheme": "warm stone greys, bronze, gold and forge orange with crimson banners",
                              "mood_atmosphere": "epic, mighty, bustling"}},
    "denver": {"context": "World of Warcraft game environment concept art: Denver transformed into a Stromgarde and Edoras "
                          "kingdom of men",
               "aesthetics": {"color_scheme": "white stone, royal blue and gold with green fields and golden trees",
                              "mood_atmosphere": "epic, noble, lively"}},
    "springs": {"context": "World of Warcraft game environment concept art: Pikes Peak transformed into an Aerie Peak and "
                           "Eagles' Eyrie dwarven aerie",
                "aesthetics": {"color_scheme": "pink granite, forest green and gold with warm firelight",
                               "mood_atmosphere": "epic, adventurous, wild"}},
    "fortcollins": {"context": "World of Warcraft game environment concept art: Poudre Canyon transformed into a New "
                               "Tinkertown and Shire village",
                    "aesthetics": {"color_scheme": "brass, copper and glowing teal with garden greens and bright flowers",
                                   "mood_atmosphere": "epic, whimsical, cheerful"}},
}
# Named models (decision 44): with the "wow" lean, each place's prompt also names what it blends, so the model lands
# on the games' look instead of generic fantasy. Names stay in art/ prompts; nothing shipped carries them.
NAMES = {}  # superseded: the names now live in the body of each PAINTED prompt
PAINTED = {  # place, then people, then two small accents (decisions 43 and 44); heroes are kept for later
    "boulder": ("Transform this into World of Warcraft game art: the Flatirons above Boulder become a night elf and Rivendell "
                "elven city. Keep the five huge flat red-brown sandstone slabs tilted steeply back against the forested "
                "mountain exactly in their shapes and places, and keep the mountain's outline. Build a grand World of "
                "Warcraft night elf city in the style of Darnassus and Mount Hyjal, blended with The Lord of the Rings' "
                "Rivendell: curved organic halls with sweeping purple and teal roofs, carved wood and pale stone arches, "
                "moonwells glowing silver-blue, lantern-lit bridges and waterfalls between the slabs, and one colossal World "
                "Tree with silver bark and golden leaves on the ridge behind. Fill it with dozens of elves, World of Warcraft "
                "night elves blended with The Lord of the Rings' Noldor: tall, long swept-back ears, lavender-tinted skin, "
                "silver or midnight-blue hair, night elf armour and flowing Rivendell robes, bare heads. Small in the sky: two "
                "dragons of World of Warcraft's green dragonflight and two hippogryphs with golden-eagle heads and antlers. "
                "Golden evening light with the first stars. Remove the stadium floodlight tower.", None),
    "golden": ("Transform this into World of Warcraft game art: Table Mountain above Golden becomes an Ironforge and Erebor "
               "dwarven kingdom. Keep both flat-topped mesas with their dark basalt caps exactly in their shapes and places. "
               "Carve into the right-hand mesa's cliff a colossal World of Warcraft Ironforge gate blended with The Lord of "
               "the Rings' Erebor: massive square-cut stone, two giant dwarf king statues with war hammers, bronze and gold "
               "trim, tiers of halls with forge-orange windows, a river flowing from the gate and a busy stone causeway. "
               "Fill it with dozens of World of Warcraft Ironforge dwarves blended with The Lord of the Rings' dwarves: "
               "stocky, huge braided beards, oversized armoured shoulders and hands, with a few gnomes, hauling ore carts "
               "and trading at market stalls. Small accents: far off on a slope one legless stone wyrm like the creature in "
               "<image_2>, made of rounded grey boulders with slivers of gold, and two dwarven steam tanks with spinning "
               "drill heads on the causeway. Replace the golf course and town with wild grassland, rocks and the river. "
               "Crimson and gold dwarven banners.", "stonewyrm"),
    "denver": ("Transform this into World of Warcraft game art: downtown Denver becomes a Stromgarde and Edoras kingdom of "
               "men. Keep downtown Denver's skyscrapers clearly visible behind, and the mountains and the golden cottonwood "
               "trees, exactly in their shapes and places. On a green hill in front of the city build a World of Warcraft "
               "human city in the style of Stromgarde and Stormwind, blended with The Lord of the Rings' Edoras: white stone "
               "walls and round towers with blue slate roofs and gold trim around one great golden-roofed timber hall with "
               "horse-head gables, timber-framed houses and a busy market. Fill it with dozens of World of Warcraft humans "
               "blended with The Lord of the Rings' Rohirrim: knights in heavy plate with big pauldrons and blue and gold "
               "tabards, townsfolk with braided hair and green cloaks, and a few dwarves. Small accents: knights riding "
               "white horses whose barding glows with golden Light up the road, and two white gryphons with bald-eagle heads "
               "in the sky. Blue and gold banners.", None),
    "springs": ("Transform this into World of Warcraft game art: Pikes Peak becomes an Aerie Peak and Eagles' Eyrie dwarven "
                "aerie. Keep Pikes Peak's broad pink-granite summit and its snowfields exactly in their shape and place. On "
                "the forested crags in front build a World of Warcraft Wildhammer dwarf town in the style of Aerie Peak, "
                "blended with The Lord of the Rings' Eagles' Eyrie: stone towers on tall rock spires, gryphon roosts, wooden "
                "walkways and rope bridges, warm windows and green and gold banners. Fill it with dozens of World of Warcraft "
                "Wildhammer dwarves: stocky, wild braided hair and beards, blue tattoos, feathered leather armour and big "
                "shoulders. Small accents: two golden-eagle-style gryphons like the creature in <image_2> and two Warcraft "
                "III dwarven gyrocopters flying between the towers. Replace the houses at the bottom with pine forest.", "gryphon"),
    "fortcollins": ("Transform this into World of Warcraft game art: Poudre Canyon becomes a New Tinkertown and Shire village. "
                    "Keep the canyon's rocky walls, its pines and the far ridge exactly in their shapes and places. Along "
                    "the canyon floor build a World of Warcraft gnome town in the style of New Tinkertown and Gnomeregan, "
                    "blended with The Lord of the Rings' Shire: brass and copper workshops with cogs, pipes, rockets and "
                    "glowing teal energy cores, a big water wheel on a clear river, and round green and yellow hobbit doors "
                    "in grassy banks, gardens and stone bridges. Fill it with dozens of World of Warcraft gnomes blended "
                    "with The Lord of the Rings' hobbits: tiny, big pointed ears and noses, wild colourful hair, goggles, "
                    "bare furry feet and bright waistcoats. Small accents: a few World of Warcraft mechanical dragonlings in "
                    "the air and two gnome mechanostriders ridden along the path.", None),
}


@app.local_entrypoint()
def painted(cards: str = "golden,boulder", leans: str = "film,game", seed: int = 43):
    """One unmasked edit per place and lean: LEANS[lean] + PAINTED[place]; writes out/<place>-<lean>-<seed>.png."""
    here = pathlib.Path(__file__).parent
    out = here / "out"; out.mkdir(exist_ok=True)
    jobs = [(c, l) for c in cards.split(",") for l in leans.split(",")]
    args = [((here / "src" / EDITS[c]["photo"]).read_bytes(), EDITS[c]["crop"],
             json.dumps({"edit_instruction": LEANS[l] + " " + PAINTED[c][0] + (" " + NAMES[c] if c in NAMES and l == "wow" else ""),
                         "style": {**STYLE[l], **PLACE_STYLE.get(c, {})} if l in STYLE else None}, ensure_ascii=False), seed,
             str(here / "refs" / f"{PAINTED[c][1]}.png") if PAINTED[c][1] else None, None) for c, l in jobs]
    for (c, l), res in zip(jobs, fibo_map("edit", args)):
        (out / f"{c}-{l}-{seed}.png").write_bytes(res["png"])
        log_runs(out, [{"card": c, "seed": seed, "mode": f"painted-{l}", "photo": EDITS[c]["photo"], "attribution_status": res["attribution_status"], "attribution": res["attribution"]}])
        print(c, l, seed, "painted attribution", res["attribution_status"])


@app.local_entrypoint()
def reference(names: str = "serpent,gryphon"):
    """Render REFS (text to image, attributed) into art/render/refs/<name>.png; edit_all reads them from there."""
    here = pathlib.Path(__file__).parent
    out, refs = here / "out", here / "refs"; out.mkdir(exist_ok=True); refs.mkdir(exist_ok=True)
    picked = names.split(",")
    scenes = [json.dumps({"short_description": REFS[n][0], "objects": [], "background_setting": "a plain golden-hour sky",
                          **{k: CHAR_STYLE[k] for k in ("lighting", "photographic_characteristics", "text_render")},
                          "style_medium": "photograph, photorealistic", "context": "a reference image of one creature; no text",
                          "artistic_style": "photorealistic"}, ensure_ascii=False) for n in picked]
    for n, res in zip(picked, fibo_map("render", [(sc, REFS[n][1]) for n, sc in zip(picked, scenes)])):
        (refs / f"{n}.png").write_bytes(res["png"])
        log_runs(out, [{"card": f"ref-{n}", "seed": REFS[n][1], "mode": "reference", "attribution_status": res["attribution_status"], "attribution": res["attribution"]}])
        print(n, "reference attribution", res["attribution_status"])


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


# Decision 48: the characters join the places' bright, hand-painted game look (decisions 43 to 45).
CHAR_GAME = {**STYLE["wow"], "context": "World of Warcraft game character key art for a social media preview card; text is added "
             "later, so the image contains no text, letters, logos, emblems or signage"}


@app.local_entrypoint()
def character(cards: str = "claudius", seed: int = 7, look: str = "game"):
    """python3 art/render/fibo_cards.py character --cards claudius,link,legallas --seed 7  (one FIBO call per card).
    look "game" (decision 48) or "char" (the first, realistic look); writes out/<card>-<look>-<seed>.png."""
    out = pathlib.Path(__file__).parent / "out"; out.mkdir(exist_ok=True)
    names = cards.split(",")
    body = lambda c: {**CHARACTERS[c], **(CHAR_GAME if look == "game" else {})}
    for c, res in zip(names, fibo_map("render", [(json.dumps(body(c), ensure_ascii=False), seed) for c in names])):
        (out / f"{c}-{look}-{seed}.png").write_bytes(res["png"])
        log_runs(out, [{"card": c, "seed": seed, "mode": f"character-{look}", "attribution_status": res["attribution_status"], "attribution": res["attribution"]}])
        print(c, look, seed, "character attribution", res["attribution_status"])


# Decision 48: the emblem tier evolves the 2014 shield, our own file, so no outside art is an input. Symbol only: the
# text band goes (the wordmark is its own tier). The C keeps its violet and silver, never the flag's red around a gold
# disc, which would read as the State "C" logo (research/color/state.yaml).
SHIELD = "baseline/v2/cs-logo-1500.png"
LOGO_SIZE = (1024, 1024)
EMBLEM_STYLE = {**STYLE["wow"], "context": "World of Warcraft game emblem for a community's avatar; no text, no letters"}
EMBLEM_KEEP = ("Keep the shield's outline, the two snow-capped mountains rising behind it and the round C with the small "
               "snowy peak inside its disc. Remove the white text band and every word and letter. The C is never red and its "
               "disc is never gold. Centre the whole emblem with even margins on the plain background.")
EMBLEM = {
    "a": "Transform this logo into a World of Warcraft game emblem: a forged shield of burnished gold and dark steel with "
         "riveted rims, the C in polished violet-silver metal, its disc a pale blue sky, warm forge light glowing behind the "
         "mountains, on a plain deep navy background.",
    "b": "Transform this logo into a World of Warcraft game emblem: the shield carved from grey granite like a dwarven gate, "
         "the mountains carved in relief with snow on the peaks, the C carved in deep violet stone with warm forge light "
         "glowing from its disc, on a plain deep navy background.",
    "c": "Transform this logo into a World of Warcraft game crest: the shield in deep blue enamel with a bright gold rim, the "
         "mountains in white and slate blue, the C in polished silver with the small snowy peak in its disc, on a plain white "
         "background.",
}
ICON_STYLE = {"style_medium": "flat vector illustration", "artistic_style": "flat, minimal, bold, two-tone",
              "context": "A favicon and app icon that must stay readable at 16 pixels; no text"}
ICON = {
    "i1": "Simplify this logo into a flat app icon: one bold shield silhouette in solid deep blue #001970 with a thick white "
          "rim, a single bold white C with one white mountain peak inside it, no gradients, no texture, no thin lines, no "
          "text, centred on plain white.",
    "i2": "Simplify this logo into a flat app icon: a bold white shield silhouette with a deep blue #001970 C and one deep "
          "blue mountain peak inside it, on a solid deep blue #001970 square, no gradients, no texture, no thin lines, no "
          "text, centred.",
}


@app.local_entrypoint()
def logo(kinds: str = "a,b,c", seed: int = 5):
    """Emblem (a, b, c) or icon (i1, i2) candidates, each a FIBO edit of the 2014 shield; writes out/logo-<kind>-<seed>.png."""
    here = pathlib.Path(__file__).parent
    out = here / "out"; out.mkdir(exist_ok=True)
    shield = (here.parent.parent / SHIELD).read_bytes()
    picked = kinds.split(",")
    def prompt(k):
        icon = k.startswith("i")
        return json.dumps({"edit_instruction": ICON[k] if icon else EMBLEM[k] + " " + EMBLEM_KEEP,
                           "style": ICON_STYLE if icon else EMBLEM_STYLE}, ensure_ascii=False)
    for k, res in zip(picked, fibo_map("edit", [(shield, (0, 0, 1, 1), prompt(k), seed, None, None, LOGO_SIZE) for k in picked])):
        (out / f"logo-{k}-{seed}.png").write_bytes(res["png"])
        log_runs(out, [{"card": f"logo-{k}", "seed": seed, "mode": "logo", "photo": SHIELD, "attribution_status": res["attribution_status"], "attribution": res["attribution"]}])
        print("logo", k, seed, "attribution", res["attribution_status"])


# The name alone, composited after (decision 37: no text inside the art; decision 46: no tagline, no on-image chip).
# Aileron ships with FIBO 2.0's own files. The AI-made label and the photo credit travel in the IPTC packet
# (with_provenance); full credits with links: dist/README.md.
CARD_TITLE = {"coloradostartups.org": "Colorado Startups", "brand": "Colorado Startups", "claudius": "Claudius",
              "link": "Linken", "legallas": "Legallas"}
CARD_ART = {"coloradostartups.org": "boulder-wow-51", "brand": "golden-wow-51", "claudius": "claudius-game-7",
            "link": "link-game-13", "legallas": "legallas-game-13"}  # <source>-<kind>-<seed> in art/render/out/; decision 50
PLACE_ART = {"boulder": "boulder-wow-51", "golden": "golden-wow-51", "denver": "denver-wow-51",
             "springs": "springs-wow-51", "fortcollins": "fortcollins-wow-51"}  # <place>-<lean>-<seed> in art/render/out/
PHOTO_CREDIT = {  # rides in csart:Source; CC BY 2.0 and 2.5 4(b) allow credit "in any reasonable manner"
    "boulder": "public-domain photo by Jimbo Herndan",
    "golden": "photo by James St. John, CC BY 2.0",
    "denver": "public-domain photo by USFWS Mountain-Prairie",
    "springs": "photo by Huttarl, CC BY 2.5",
    "fortcollins": "photo by Charles Willgren, CC BY 2.0",
}


def photo_source(place: str) -> str:
    return f"edit of a {PHOTO_CREDIT[place]} (art/render/src/{EDITS[place]['photo']})"


@app.function(image=image, volumes={"/cache": weights}, secrets=[modal.Secret.from_name("fibo-hf")], timeout=600)
def compose(png: bytes, title: str, prov: dict) -> bytes:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    font = aileron()
    img = Image.open(io.BytesIO(png)).convert("RGB").resize((1280, 640), Image.LANCZOS)
    big = ImageFont.truetype(font, 76)
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((76, 75), title, font=big, fill=(0, 10, 40, 200))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    img = Image.alpha_composite(img.convert("RGBA"), shadow); d = ImageDraw.Draw(img)
    d.rectangle((76, 56, 196, 62), fill=(195, 0, 47, 255))
    d.text((76, 72), title, font=big, fill=(255, 255, 255, 255))
    buf = io.BytesIO(); img.convert("RGB").save(buf, "JPEG", quality=88, optimize=True, progressive=True)
    return with_provenance(buf.getvalue(), prov)


def aileron() -> str:
    """Aileron Regular (CC0): the copy in guide/public/fonts, or FIBO 2.0's own file where the repo is absent (Modal)."""
    local = pathlib.Path(__file__).resolve().parents[2] / "guide" / "public" / "fonts" / "Aileron-Regular.otf"
    if local.exists():
        return str(local)
    from huggingface_hub import hf_hub_download
    return hf_hub_download("briaai/Fibo-2.0-dev", "Aileron-Regular.otf", subfolder="fonts", cache_dir="/cache" if os.path.isdir("/cache") else None)


# Decisions 8 and 46: model-made images carry their AI-made label (DigitalSourceType) and photo credit (csart:Source)
# in metadata. Only the IPTC AI fields and the art namespace, the provenance packet tools/vendor/export_scan.py
# accepts (#691); no EXIF, no camera or location data.
def xmp_packet(prov: dict) -> bytes:
    from xml.sax.saxutils import quoteattr
    iptc = "http://cv.iptc.org/newscodes/digitalsourcetype/"
    attrs = {"Iptc4xmpExt:DigitalSourceType": iptc + prov["type"], "Iptc4xmpExt:AISystemUsed": "FIBO 2.0 (Bria), briaai/Fibo-2.0-dev",
             "csart:Seed": str(prov["seed"]), "csart:Source": prov["source"], "csart:ModelLicense": "Bria FIBO 2 Free plan"}
    packet = ('<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
              '<rdf:Description rdf:about="" xmlns:Iptc4xmpExt="http://iptc.org/std/Iptc4xmpExt/2008-02-29/" '
              'xmlns:csart="https://coloradostartups.org/ns/art/1.0/" '
              + " ".join(f"{k}={quoteattr(v)}" for k, v in attrs.items()) + "/></rdf:RDF></x:xmpmeta>").encode()
    return packet


def with_provenance(jpg: bytes, prov: dict) -> bytes:
    seg = b"http://ns.adobe.com/xap/1.0/\x00" + xmp_packet(prov)
    at = 4 + int.from_bytes(jpg[4:6], "big") if jpg[2:4] == b"\xff\xe0" else 2  # after the JFIF header
    return jpg[:at] + b"\xff\xe1" + (len(seg) + 2).to_bytes(2, "big") + seg + jpg[at:]


@app.local_entrypoint()
def compose_all(cards_only: str = ""):
    here = pathlib.Path(__file__).parent
    out = here / "out"; cards = here.parent.parent / "dist" / "social"; cards.mkdir(parents=True, exist_ok=True)
    names = cards_only.split(",") if cards_only else list(CARD_TITLE)
    src = {c: out / f"{CARD_ART[c]}.png" for c in names}
    missing = [str(p) for p in src.values() if not p.exists()]
    if missing:
        raise SystemExit("compose_all: missing source render(s): " + ", ".join(missing))
    def prov(c):
        source, kind, seed = CARD_ART[c].rsplit("-", 2)
        if kind in ("edit", "game", "film", "wow") and source in EDITS:  # every place image starts from a real photo
            return {"type": "compositeWithTrainedAlgorithmicMedia", "seed": int(seed), "source": photo_source(source)}
        return {"type": "trainedAlgorithmicMedia", "seed": int(seed), "source": "text to image"}
    for c, jpg in zip(names, (compose.starmap if LANE == "modal" else lambda xs: [compose.local(*x) for x in xs])([(src[c].read_bytes(), CARD_TITLE[c], prov(c)) for c in names])):
        (cards / f"{c}.jpg").write_bytes(jpg)
        print(c, len(jpg) // 1024, "KB")


def places():
    """dist/places/<place>.jpg: each place's painting (decision 43), 1440x720 JPEG, no text on the image (decision 46).
    The AI-made label and photo credit ride in the IPTC packet; full credits in dist/README.md. Pillow only, seconds."""
    from PIL import Image
    here = pathlib.Path(__file__).parent
    dest = here.parent.parent / "dist" / "places"; dest.mkdir(parents=True, exist_ok=True)
    for c in EDITS:
        img = Image.open(here / "out" / f"{PLACE_ART[c]}.png").convert("RGB").resize((1440, 720), Image.LANCZOS)
        buf = io.BytesIO(); img.save(buf, "JPEG", quality=86, optimize=True, progressive=True)
        jpg = with_provenance(buf.getvalue(), {"type": "compositeWithTrainedAlgorithmicMedia", "seed": int(PLACE_ART[c].rsplit("-", 1)[1]),
                                               "source": photo_source(c)})
        (dest / f"{c}.jpg").write_bytes(jpg)
        print(c, len(jpg) // 1024, "KB")


# The website's Hall art (Paul, 2026-11-14: "Yes, render all 7"): its three keepers, the 404 passage, founders and
# guides scenes and the Hall's stone texture, in the game look. The keepers replace Anima art whose licence allows only
# non-commercial use; the scenes keep the website's picks' subjects (coloradostartups.org art/finals.json).
HALL_LOOK = {
    "lighting": {"conditions": "warm, bright, magical light", "direction": "key light from the upper left, warm fill", "shadows": "soft"},
    "photographic_characteristics": {"depth_of_field": "deep", "focus": "sharp throughout", "camera_angle": "eye-level", "lens_focal_length": "standard"},
    "text_render": [], **STYLE["wow"],
}
KEEPER = ("plain flat warm cream background with nothing else in it", "4:5 portrait, the keeper from the waist up, centred, "
          "head in the upper third, generous cream margin on every side")
HALL = {
    "communitas": ((960, 1200), {
        "short_description": "Communitas, Keeper of the Doors, a warm dwarf woman who welcomes newcomers",
        "objects": [{"description": "a sturdy, kind dwarf woman with long copper-red braids, rosy cheeks and a welcoming smile, a sky-blue "
                     "hooded cloak over a brown leather tunic, a ring of brass keys at her belt, holding up a glowing brass lantern on a "
                     "tall wooden pole", "location": "centre", "relationship": "the only subject", "relative_size": "large within frame"}],
        "background_setting": KEEPER[0],
        "aesthetics": {"composition": KEEPER[1], "color_scheme": "sky blue cloak, copper hair, warm brass and leather on cream", "mood_atmosphere": "welcoming, warm, kind"},
        "context": "World of Warcraft game character portrait of a community's AI guide for a website; no text, no letters, no logo",
        **HALL_LOOK}),
    "resourcus": ((960, 1200), {
        "short_description": "Resourcus, an elder gnome mapkeeper who knows every startup resource",
        "objects": [{"description": "a small, wise elder gnome with a long white beard and bright eyes, brass goggles on a tall pointed brass "
                     "hat, a pine-green coat with brass buttons, holding a brass compass over a blank hand-painted map with drawn "
                     "mountains and rivers and no writing", "location": "centre", "relationship": "the only subject", "relative_size": "large within frame"}],
        "background_setting": KEEPER[0],
        "aesthetics": {"composition": KEEPER[1], "color_scheme": "pine green coat, white beard, polished brass on cream", "mood_atmosphere": "wise, helpful, curious"},
        "context": "World of Warcraft game character portrait of a community's AI guide for a website; no text, no letters, no logo",
        **HALL_LOOK}),
    "publicus": ((960, 1200), {
        "short_description": "Publicus, Herald of the Hall, a cheerful dwarf herald",
        "objects": [{"description": "a stocky, cheerful dwarf herald with a long copper-red braided beard, a red cap with a white feather, an "
                     "ember-red tabard over chain mail, holding a large blank broadsheet high in one hand, with no writing on it, and a "
                     "leather satchel of rolled scrolls", "location": "centre", "relationship": "the only subject", "relative_size": "large within frame"}],
        "background_setting": KEEPER[0],
        "aesthetics": {"composition": KEEPER[1], "color_scheme": "ember red tabard and cap, copper beard, steel and leather on cream", "mood_atmosphere": "cheerful, bold, newsy"},
        "context": "World of Warcraft game character portrait of a community's AI guide for a website; no text, no letters, no logo",
        **HALL_LOOK}),
    "passage": ((1344, 768), {
        "short_description": "A lantern-lit passage carved through pink Pikes Peak granite, where a cog railway ends at a blank stone wall",
        "objects": [{"description": "a brass steam cog-railway engine on a small cart, on toothed rails that run down the passage", "location": "centre left", "relationship": "on the rails", "relative_size": "medium"},
                    {"description": "a smooth, blank, unfinished stone wall where the rails end, with scaffolding and tools beside it, no writing, no signs", "location": "centre right", "relationship": "the end of the passage", "relative_size": "medium"}],
        "background_setting": "a tunnel of pink and rose granite with hanging lanterns, opening at the far left onto a snowy Colorado peak under a gold sky",
        "aesthetics": {"composition": "wide 16:9, the rails leading the eye to the blank wall", "color_scheme": "pink granite, warm lantern gold, brass, a cool blue sky", "mood_atmosphere": "a build still in progress, curious, inviting"},
        "context": "World of Warcraft game environment concept art for a website's page-not-found scene; no text, no letters, no signs",
        **HALL_LOOK}),
    "founders": ((1344, 768), {
        "short_description": "Founders build a glowing fusion core in a red sandstone workshop below the Flatirons",
        "objects": [{"description": "a small team of founders, a dwarf, a gnome, an elf and a human, building a glowing teal fusion core held in a large brass ring on a workbench", "location": "centre", "relationship": "working together", "relative_size": "large"}],
        "background_setting": "a warm red sandstone workshop with brass tools and gears, a big arched window showing Boulder's tilted red Flatirons in sunlight",
        "aesthetics": {"composition": "wide 16:9, the team and the core in the centre, the window behind", "color_scheme": "red sandstone, glowing teal, brass gold, green pines", "mood_atmosphere": "focused, hopeful, inventive"},
        "context": "World of Warcraft game environment concept art for a website scene about founders; no text, no letters, no signs",
        **HALL_LOOK}),
    "guides": ((1344, 768), {
        "short_description": "Two founders plan a route on a hand-drawn map of the Front Range above Denver",
        "objects": [{"description": "two founders, a gnome and a human, leaning over a table and marking a picture map drawn only with little painted peaks, blue rivers and green forests: no writing anywhere on it, no labels, no letters, no script, no numbers", "location": "centre", "relationship": "planning together", "relative_size": "large"},
                    {"description": "a polished copper rocket model and a small brass satellite on the table", "location": "right", "relationship": "beside the map", "relative_size": "small"}],
        "background_setting": "a high study with tall windows showing snowy Front Range peaks above the Denver skyline at golden hour",
        "aesthetics": {"composition": "wide 16:9, the table in the foreground, the view behind", "color_scheme": "copper and brass, warm wood, snowy peaks, gold sky", "mood_atmosphere": "guiding, ambitious, friendly"},
        "context": "World of Warcraft game environment concept art for a website scene about guides; no text, no letters, no signs",
        **HALL_LOOK}),
    "stone": ((1024, 1024), {
        "short_description": "A seamless, tileable texture swatch of smooth carved warm sandstone",
        "objects": [], "background_setting": "the whole frame is the stone surface, seen straight on",
        "aesthetics": {"composition": "an even all-over pattern like a sample swatch, no focal point, no edges, no lighting gradient, no light falloff, no banding", "color_scheme": "warm sand and soft ochre", "mood_atmosphere": "calm"},
        "lighting": {"conditions": "flat, even light", "direction": "none", "shadows": "none"},
        "photographic_characteristics": {"depth_of_field": "deep", "focus": "sharp throughout", "camera_angle": "top-down", "lens_focal_length": "standard"},
        "text_render": [], "style_medium": "digital painting", "artistic_style": "hand-painted game texture, soft mottling, fine grain",
        "context": "A seamless tile for a website's background texture; no text"}),
}


@app.local_entrypoint()
def hall(names: str = "communitas,resourcus,publicus,passage,founders,guides,stone", seed: int = 3):
    """The website's Hall art: text to image at each item's size; writes out/hall-<name>-<seed>.png."""
    out = pathlib.Path(__file__).parent / "out"; out.mkdir(exist_ok=True)
    picked = names.split(",")
    for n, res in zip(picked, fibo_map("render", [(json.dumps(HALL[n][1], ensure_ascii=False), seed, HALL[n][0]) for n in picked])):
        (out / f"hall-{n}-{seed}.png").write_bytes(res["png"])
        log_runs(out, [{"card": f"hall-{n}", "seed": seed, "mode": "hall", "attribution_status": res["attribution_status"], "attribution": res["attribution"]}])
        print("hall", n, seed, "attribution", res["attribution_status"])


def hall_export(picks: str = ""):
    """dist/hall/: the chosen Hall renders at the website's sizes (coloradostartups.org art/concepts/finals.md).
    picks: name=seed pairs, e.g. communitas=3,resourcus=8. Keepers 960 x 1200 and a 320 head crop; scenes 1344 x 756
    JPEG; the stone tile 1024 PNG. Every file keeps the AI-made label in its XMP."""
    from PIL import Image
    from PIL.PngImagePlugin import PngInfo
    here = pathlib.Path(__file__).parent
    dest = here.parent.parent / "dist" / "hall"; dest.mkdir(parents=True, exist_ok=True)
    for pair in picks.split(","):
        n, seed = pair.split("=")
        img = Image.open(here / "out" / f"hall-{n}-{seed}.png").convert("RGB")
        prov = {"type": "trainedAlgorithmicMedia", "seed": int(seed), "source": "text to image"}
        info = PngInfo(); info.add_itxt("XML:com.adobe.xmp", xmp_packet(prov).decode())
        if HALL[n][0] == (960, 1200):  # a keeper
            img.save(dest / f"{n}.png", "PNG", optimize=True, pnginfo=info)
            side = 576; left = (960 - side) // 2
            img.crop((left, 90, left + side, 90 + side)).resize((320, 320), Image.LANCZOS).save(dest / f"{n}-small.png", "PNG", optimize=True, pnginfo=info)
            print(n, "960x1200 and 320x320")
        elif n == "stone":
            img.save(dest / "stone.png", "PNG", optimize=True, pnginfo=info)
            print(n, img.size)
        else:  # a scene: the website's 1344 x 756 crop
            buf = io.BytesIO(); img.crop((0, 6, 1344, 762)).save(buf, "JPEG", quality=86, optimize=True, progressive=True)
            (dest / f"{n}.jpg").write_bytes(with_provenance(buf.getvalue(), prov))
            print(n, "1344x756")


# Cards for the region and project repos (finish plan, package G), from the shipped place paintings committed in
# dist/places/: the raw renders in out/ are gitignored, so nothing here depends on them.
REPO_CARDS = {"photon-mountain": ("denver", "Photon Mountain"), "space-peak": ("springs", "Space Peak"),
              "fusion-canyon": ("fortcollins", "Fusion Canyon"), "startup-credits": ("golden", "Startup Credits")}


def repo_cards():
    dist = pathlib.Path(__file__).parent.parent.parent / "dist"
    for repo, (place, title) in REPO_CARDS.items():
        prov = {"type": "compositeWithTrainedAlgorithmicMedia", "seed": int(PLACE_ART[place].rsplit("-", 1)[1]), "source": photo_source(place)}
        jpg = compose.local((dist / "places" / f"{place}.jpg").read_bytes(), title, prov)
        (dist / "social" / f"{repo}.jpg").write_bytes(jpg)
        print(repo, len(jpg) // 1024, "KB")


def logo_export(emblem: str = "logo-a-9", icon: str = "logo-i2-5"):  # decision 50's blind-judged winners
    """dist/logo/: decision 48's three tiers from the chosen candidates in out/, and the favicon set
    (32 px ICO with 16 and 48, 180 apple-touch with 20 px padding, 192 and 512; Evil Martians, 2026)."""
    from PIL import Image, ImageDraw, ImageFont
    from PIL.PngImagePlugin import PngInfo
    here = pathlib.Path(__file__).parent
    dest = here.parent.parent / "dist" / "logo"; dest.mkdir(parents=True, exist_ok=True)
    def save(img, name, prov=None):
        info = PngInfo()
        if prov:  # the AI-made label rides in an XMP iTXt chunk, the packet export_scan accepts
            info.add_itxt("XML:com.adobe.xmp", xmp_packet(prov).decode())
        img.save(dest / name, "PNG", optimize=True, pnginfo=info)
        print(name, (dest / name).stat().st_size // 1024, "KB")
    seed_of = lambda n: int(n.rsplit("-", 1)[1])
    em = Image.open(here / "out" / f"{emblem}.png").convert("RGB")
    prov = {"type": "compositeWithTrainedAlgorithmicMedia", "seed": seed_of(emblem), "source": f"edit of {SHIELD}, the 2014 shield"}
    for s in (1024, 512):
        save(em.resize((s, s), Image.LANCZOS), f"emblem-{s}.png", prov)
    ic = Image.open(here / "out" / f"{icon}.png").convert("RGB")
    prov = {**prov, "seed": seed_of(icon)}
    for s in (512, 192):
        save(ic.resize((s, s), Image.LANCZOS), f"icon-{s}.png", prov)
    touch = Image.new("RGB", (180, 180), ic.getpixel((4, 4)))
    touch.paste(ic.resize((140, 140), Image.LANCZOS), (20, 20))
    save(touch, "apple-touch-icon.png", prov)
    ic.resize((256, 256), Image.LANCZOS).save(dest / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("favicon.ico", (dest / "favicon.ico").stat().st_size // 1024, "KB")
    # The wordmark tier is type, not a model's image: Aileron under the State red rule, in the cards' proportions.
    font, text = ImageFont.truetype(aileron(), 200), "Colorado Startups"
    x0, y0, x1, y1 = font.getbbox(text)
    for name, ink in (("wordmark-blue.png", (0, 25, 112, 255)), ("wordmark-white.png", (255, 255, 255, 255))):
        img = Image.new("RGBA", (x1 - x0 + 40, y1 - y0 + 110), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        d.rectangle((20, 20, 336, 36), fill=(195, 0, 47, 255))  # the cards' rule: 1.58 x the font size wide, 0.08 tall
        d.text((20 - x0, 90 - y0), text, font=font, fill=ink)   # and a gap of 0.27 x the font size below it
        img.save(dest / name, "PNG", optimize=True)
        print(name, img.size)


ENTRIES = {"edit_all": edit_all, "character": character, "compose_all": compose_all, "reference": reference, "painted": painted,
           "places": places, "logo": logo, "repo_cards": repo_cards, "logo_export": logo_export, "hall": hall, "hall_export": hall_export}
if __name__ == "__main__" and sys.argv[1:2] and sys.argv[1] in ENTRIES:  # python3 ... <entry> --flag value: the Space lane
    LANE = "space"
    kw = {k.lstrip("-").replace("-", "_"): v for k, v in zip(sys.argv[2::2], sys.argv[3::2])}
    ENTRIES[sys.argv[1]](**{k: int(v) if k == "seed" else v for k, v in kw.items()})
