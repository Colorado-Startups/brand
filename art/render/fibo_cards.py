"""art/render/fibo_cards.py: the brand's FIBO 2.0 art (decisions 31, 35, 37, 39, 41).

Lanes: the ZeroGPU Space paul-co-startups/brand-fibo (art/render/space/, on HF PRO's daily quota) first; Modal's
included credit, an L40S, as the fallback. Weights: briaai/Fibo-2.0-dev, gated. Every image is sent to Bria's
attribution API, which keeps commercial use covered under the FIBO 2 Free plan and counts one call. Reserve the calls
first: python3 tools/fibo_budget.py reserve N. Space (R is uv run --no-project --with modal==1.6.3 --with
gradio_client==2.7.2 --with pillow python3; Modal is the same with `modal run art/render/fibo_cards.py::<entry>`):
  R art/render/fibo_cards.py edit_all --cards boulder,golden --seed 31        place art, edits of real photos
  R art/render/fibo_cards.py character --cards claudius --seed 7              project characters
  R art/render/fibo_cards.py compose_all --seed 31 --cards-only brand         wordmark, label, credit -> dist/social
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
            photo, crop, prompt, seed, ref, keep = a
            src = Image.open(io.BytesIO(photo)).convert("RGB"); w, h = src.size
            src = src.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h))).resize(SIZE, Image.LANCZOS)
            path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name; src.save(path)
            mask = None
            if keep:  # white may change, black (the landmark) is kept; feathered so the seam blends
                from PIL import ImageDraw, ImageFilter
                m = Image.new("L", SIZE, 255); ImageDraw.Draw(m).polygon([(x * SIZE[0], y * SIZE[1]) for x, y in keep], fill=0)
                mask = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name; m.filter(ImageFilter.GaussianBlur(12)).save(mask)
            vgl = Client(VGL)  # Bria's public Space; its /vgl runs on Bria's token and no GPU
            def upload(p):
                r = httpx.post(vgl.upload_url, files=[("files", (pathlib.Path(p).name, open(p, "rb"), "image/png"))], headers=vgl.headers, timeout=60)
                r.raise_for_status(); return r.json()[0]
            edit = vgl.predict(json.loads(prompt)["edit_instruction"], upload(path), upload(ref) if ref else None, None, None,
                               upload(mask) if mask else None, max(seed, 1), api_name="/vgl")["json_instruction"]
            edit = edit if isinstance(edit, str) else json.dumps(edit, ensure_ascii=False)
            png, status, attribution = client.predict(handle_file(path), "[0,0,1,1]", handle_file(ref) if ref else None,
                                                      handle_file(mask) if mask else None, edit, "", seed,
                                                      *SIZE, EDIT_STEPS, EDIT_GUIDANCE, api_name="/edit")
        else:
            prompt, seed = a
            png, status, attribution = client.predict(prompt, NEGATIVE, seed, *SIZE, STEPS, GUIDANCE, api_name="/render")
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
    "film": ("Repaint this whole photo as an epic fantasy matte painting in the grand, naturalistic style of classic fantasy "
             "film concept art: muted earthy colours, soft golden evening light with long shadows, mist in the low ground and "
             "depth haze toward the horizon, painterly brushwork, one consistent light across the whole scene."),
    "game": ("Repaint this whole photo as a hand-painted high-fantasy illustration in a stylized video-game look: bold "
             "saturated colours, chunky slightly exaggerated shapes, painterly hand-painted textures, warm magical evening "
             "light with glowing highlights, one consistent light across the whole scene."),
}
PAINTED = {
    "golden": ("Keep both flat-topped mesas exactly in their shapes and places, with their dark basalt caps. Into the steep face "
               "of the right-hand mesa, carve one colossal dwarven gate rising most of the mesa's height: a towering square-cut "
               "stone portal flanked by two giant statues of helmeted dwarf kings resting on war hammers, warm golden light "
               "glowing from deep inside, a river flowing out from beneath it, and a long stone causeway leading to it. A few "
               "tiny dwarves on the causeway show the immense scale. Replace the golf course, houses and town with wild "
               "grassland, rocks and the river. Add no text, letters or signs.", None),
    "boulder": ("Keep the five tilted Flatirons rock slabs and the mountain's outline exactly in their shapes and places. On "
                "the forested slopes below the slabs, build one grand sanctuary of elves and dragons: pale stone halls with "
                "tall slender arches and towers with gold domes climbing the slope between waterfalls that fall from the "
                "slabs, linked by terraces and bridges. Put the long green serpent dragon from <image_2> coiling through the "
                "sky above the slabs, its horned head and face visible, and one white-and-gold winged dragon perched on the "
                "highest tower, glowing softly. A few tiny elves on the bridges show the scale. Remove the stadium floodlight "
                "tower. Add no text, letters or signs.", "serpent"),
    "denver": ("Keep the downtown skyline's towers and the mountains behind the city exactly in their shapes and places, and "
               "the golden cottonwood trees at the sides. On a green hill on the plain in front of the city, build one grand "
               "citadel of men that blends two styles into a single building: a white stone keep with square towers and blue "
               "slate roofs, whose great central hall is carved timber with a shining golden roof and horse-head gables. A "
               "stone road winds up the hill, with a few tiny riders on horses. Plain blue, green and gold banners. Add no "
               "text, letters or signs.", None),
    "springs": ("Keep Pikes Peak's broad pink-granite summit and its snowfields exactly in their shape and place. On the "
                "forested crags in front of the peak, build one grand dwarven aerie: stone and timber halls and towers carved "
                "into the rocks, wooden walkways and rope bridges, and great stone roosts. Put three gryphons like the "
                "creature in <image_2> flying around the aerie, one giant golden eagle perched on the highest roost, and two "
                "small gnome gyrocopters in the sky. A few tiny dwarves and gnomes on the walkways show the scale. Replace "
                "the houses at the bottom with pine forest. Add no text, letters or signs.", "gryphon"),
    "fortcollins": ("Keep the canyon's rocky walls, its pines and the far ridge exactly in their shapes and places. Along the "
                    "canyon floor, add a clear mountain river and one village of gnome science and hobbit homes: a big brass "
                    "workshop with round porthole windows, a great water wheel turned by the river and softly glowing teal "
                    "energy cores, and beside it round green and yellow doors set into grassy banks, flower gardens and a "
                    "stone bridge over the river. A few tiny gnomes and hobbits on the paths and one small gnome gyrocopter "
                    "in the sky. Add no text, letters or signs.", None),
}


@app.local_entrypoint()
def painted(cards: str = "golden,boulder", leans: str = "film,game", seed: int = 43):
    """One unmasked edit per place and lean: LEANS[lean] + PAINTED[place]; writes out/<place>-<lean>-<seed>.png."""
    here = pathlib.Path(__file__).parent
    out = here / "out"; out.mkdir(exist_ok=True)
    jobs = [(c, l) for c in cards.split(",") for l in leans.split(",")]
    args = [((here / "src" / EDITS[c]["photo"]).read_bytes(), EDITS[c]["crop"],
             json.dumps({"edit_instruction": LEANS[l] + " " + PAINTED[c][0]}, ensure_ascii=False), seed,
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


@app.local_entrypoint()
def character(cards: str = "claudius", seed: int = 7):
    """modal run art/render/fibo_cards.py::character --cards claudius,link,legallas --seed 7  (one FIBO call per card)"""
    out = pathlib.Path(__file__).parent / "out"; out.mkdir(exist_ok=True)
    names = cards.split(",")
    for c, res in zip(names, fibo_map("render", [(json.dumps(CHARACTERS[c], ensure_ascii=False), seed) for c in names])):
        (out / f"{c}-char-{seed}.png").write_bytes(res["png"])
        log_runs(out, [{"card": c, "seed": seed, "mode": "character", "attribution_status": res["attribution_status"], "attribution": res["attribution"]}])
        print(c, seed, "character attribution", res["attribution_status"])


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
CARD_ART = {"coloradostartups.org": "boulder-game", "brand": "golden-game", "claudius": "claudius-char", "link": "link-char", "legallas": "legallas-char"}


@app.function(image=image, volumes={"/cache": weights}, secrets=[modal.Secret.from_name("fibo-hf")], timeout=600)
def compose(png: bytes, title: str, subtitle: str, credit: str, prov: dict) -> bytes:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    from huggingface_hub import hf_hub_download
    font = hf_hub_download("briaai/Fibo-2.0-dev", "Aileron-Regular.otf", subfolder="fonts", cache_dir="/cache" if os.path.isdir("/cache") else None)
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
        if art[1] in ("edit", "game", "film"):  # every place image starts from a real photo
            return {"type": "compositeWithTrainedAlgorithmicMedia", "seed": seed, "source": f"edit of art/render/src/{EDITS[art[0]]['photo']}"}
        return {"type": "trainedAlgorithmicMedia", "seed": seed, "source": "text to image"}
    for c, jpg in zip(names, (compose.starmap if LANE == "modal" else lambda xs: [compose.local(*x) for x in xs])([(src[c].read_bytes(), *CARD_TEXT[c], prov(c)) for c in names])):
        (cards / f"{c}.jpg").write_bytes(jpg)
        print(c, len(jpg) // 1024, "KB")


def places(lean: str = "game", seed: int = 43):
    """dist/places/<place>.jpg: each place's painting (decision 43), 1440x720 JPEG with IPTC provenance, no wordmark.
    Runs locally in seconds (Pillow only); credits for the CC BY photos are in dist/README.md."""
    from PIL import Image
    here = pathlib.Path(__file__).parent
    dest = here.parent.parent / "dist" / "places"; dest.mkdir(parents=True, exist_ok=True)
    for c in EDITS:
        img = Image.open(here / "out" / f"{c}-{lean}-{seed}.png").convert("RGB").resize((1440, 720), Image.LANCZOS)
        buf = io.BytesIO(); img.save(buf, "JPEG", quality=86, optimize=True, progressive=True)
        jpg = with_provenance(buf.getvalue(), {"type": "compositeWithTrainedAlgorithmicMedia", "seed": seed,
                                               "source": f"edit of art/render/src/{EDITS[c]['photo']}"})
        (dest / f"{c}.jpg").write_bytes(jpg)
        print(c, len(jpg) // 1024, "KB")


ENTRIES = {"edit_all": edit_all, "character": character, "compose_all": compose_all, "reference": reference, "painted": painted,
           "places": places}
if __name__ == "__main__" and sys.argv[1:2] and sys.argv[1] in ENTRIES:  # python3 ... <entry> --flag value: the Space lane
    LANE = "space"
    kw = {k.lstrip("-").replace("-", "_"): v for k, v in zip(sys.argv[2::2], sys.argv[3::2])}
    ENTRIES[sys.argv[1]](**{k: int(v) if k == "seed" else v for k, v in kw.items()})
