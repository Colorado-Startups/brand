"""art/render/ltx_clips.py: the website's theme clips, LTX-2.5 image-to-video of the place paintings (decisions 37, 61).

Lane: Lightricks' own public ZeroGPU Space Lightricks/LTX-2.5 (the distilled 22B, two stages), called with the hf CLI's
signed-in account, so its HF PRO daily quota, the way the FIBO edit step calls Bria's public Space (decision 41). Read
huggingface.co/settings/billing before and after every call; past the quota HF bills the included credit (decision 57).
R is uv run --no-project --with gradio_client==2.7.2 python3:
  R art/render/ltx_clips.py render photonics --seed 11       one GPU call: raw clip and runs row in art/render/out/clips/
  R art/render/ltx_clips.py frames photonics --seed 11        contact sheet, picked frames, brightness and change
  R art/render/ltx_clips.py export photonics --seed 11        loop, WebM and MP4 with no audio -> dist/clips/
frames and export run ffmpeg on the clip Space paul-co-startups/brand-clips (art/render/clip-space/, free CPU tier),
because the bash guard keeps ffmpeg off the Mac (rules/compute.md).
The Space has no first-and-last-frame mode and stops at 5 s (121 frames), so export makes the loop: it dissolves the
clip's last second into its first. The loop opens 1 s after the painting, so the painting still works as the poster.
"""
import argparse, datetime, hashlib, json, pathlib, shutil, subprocess

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
OUT = HERE / "out" / "clips"
DIST = ROOT / "dist" / "clips"
SPACE = "Lightricks/LTX-2.5"
ENCODER = "paul-co-startups/brand-clips"  # art/render/clip-space/, free CPU: ffmpeg never runs on the Mac
# The Space's grid: both sides divide by 64. 1280 x 640 keeps the paintings' 2:1 and the 720p class's 1280 width.
WIDTH, HEIGHT, SECONDS, FPS, DECODER = 1280, 640, 5.0, 24, "conv"
FRAMES = int(SECONDS * FPS) // 8 * 8 + 1  # 121, the Space's own snap to the 8k+1 grid
FADE = 24  # frames crossfaded at the seam: 1 s
LABEL = "AI-made: LTX-2.5 image-to-video of a FIBO 2.0 painting (Colorado Startups brand)"

# One present-tense paragraph each (art/motion.md rule 8): what moves, how, and what the camera does. Places are named
# in the generic words of dist/README.md; the painting already carries the look.
CLIPS = {
    "photonics": {
        "still": "dist/places/boulder.jpg", "place": "Boulder (Photon Mountain)",
        "source_photo": "Photo by Jimbo Herndan, public domain (commons.wikimedia.org/wiki/File:Flatirons_2007.jpg)",
        "prompt": "Boulder's Flatirons stand still as an elven city of light at dusk, in a bright, hand-painted fantasy "
                  "game style. The round crystal portals set in the red rock glow pale blue and white, and their light "
                  "ripples slowly inward like a calm pulse. Faint, steady threads of blue light shimmer between the "
                  "portals like quiet lasers, never flashing. The waterfalls pour down between the rocks, the stars "
                  "twinkle softly, and small motes of light drift up from the lanterns along the bridges. The robed "
                  "elves stand in place, and only their capes and hair stir in a light breeze. The dragons stay where "
                  "they are in the sky, their wings slowly rising and falling. The camera holds completely still, with "
                  "no cuts."},
    "fusion": {
        "still": "dist/places/fortcollins.jpg", "place": "Fort Collins (Fusion Canyon)",
        "source_photo": "Photo by Charles Willgren, CC BY 2.0 (commons.wikimedia.org/wiki/File:Poudre_Canyon,_Greyrock_trail.jpg), edited",
        "prompt": "A cinemagraph of a bright, hand-painted fantasy game painting of Poudre Canyon as a gnome workshop "
                  "village. The picture stays frozen like a painting: the camera, the houses, the gnomes, the riders, the "
                  "metal striders and the two bronze dragonlings do not move at all. Only a few small things are alive. "
                  "The big water wheel turns slowly, the waterfall and the creek flow, and soft white steam rises from "
                  "the chimneys. The round teal energy cores in the workshop windows glow and pulse gently, and thin "
                  "lines of teal light flow along the brass pipes like a small power grid."},
    "space": {
        "still": "dist/places/springs.jpg", "place": "Colorado Springs (Space Peak)",
        "source_photo": "Photo by Huttarl, CC BY 2.5 (commons.wikimedia.org/wiki/File:Pikes_Peak_from_CO_Springs.jpg), edited",
        "prompt": "A cinemagraph of a bright, hand-painted fantasy game painting of Pikes Peak behind tall stone tower "
                  "aeries. The picture stays frozen like a painting: the camera, the towers, the golden gryphon and the "
                  "bodies of the gyrocopters do not move at all. Only a few small things are alive. The rotors on the "
                  "brass gyrocopters spin, and thin white exhaust drifts up from them like a launch about to begin. The "
                  "green banners on the towers sway gently, warm lantern light glows softly in the windows, and mist "
                  "drifts slowly through the valley."},
}


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def raw(clip, seed):
    return OUT / f"{clip}-{seed}.mp4"


def log(row):
    runs = OUT / "runs.json"
    rows = (json.loads(runs.read_text()) if runs.exists() else []) + [row]
    runs.write_text("[\n" + ",\n".join(json.dumps(r) for r in rows) + "\n]\n")


def render(clip, seed):
    from gradio_client import Client, handle_file
    OUT.mkdir(parents=True, exist_ok=True)
    c = CLIPS[clip]
    started = datetime.datetime.now(datetime.timezone.utc)
    client = Client(SPACE)  # the hf CLI's signed-in account, so its PRO quota
    video, used, _, length = client.predict(
        c["prompt"], handle_file(str(ROOT / c["still"])), HEIGHT, WIDTH, SECONDS, seed, DECODER,
        False, False, False, api_name="/run")  # auto length, random seed and the prompt enhancer all off
    path = video["video"] if isinstance(video, dict) else video
    shutil.copyfile(path, raw(clip, seed))
    secs = (datetime.datetime.now(datetime.timezone.utc) - started).total_seconds()
    log({"clip": clip, "seed": seed, "prompt": c["prompt"], "still": c["still"], "still_sha256": sha(ROOT / c["still"]), "space": SPACE,
         "width": WIDTH, "height": HEIGHT, "frames": FRAMES, "decoder": DECODER, "length": length,
         "prompt_sent_matches": used.strip() == c["prompt"].strip(), "wall_seconds": round(secs, 1),
         "at": started.isoformat(timespec="seconds"), "sha256": sha(raw(clip, seed))})
    print(clip, seed, length, f"{secs:.0f} s wall", raw(clip, seed))


def ffprobe(path, entries):
    return json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", entries, "-of", "json", str(path)],
                                     check=True, capture_output=True, text=True).stdout)


def frames(clip, seed, picks="0,60,96,120"):
    """A contact sheet of every 8th frame, picked frames at 960 px, and per-frame brightness and change (for flashes),
    made on the clip Space."""
    from gradio_client import Client, handle_file
    grid, four, stats = Client(ENCODER).predict(handle_file(str(raw(clip, seed))), picks, api_name="/sheet")
    for got, name in ((grid, "sheet"), (four, "picks")):
        shutil.copyfile(got, OUT / f"{clip}-{seed}-{name}.jpg")
    print(stats, OUT / f"{clip}-{seed}-sheet.jpg", OUT / f"{clip}-{seed}-picks.jpg")


def export(clip, seed, webm_crf, mp4_crf, approved, billing):
    """Loop and encode on the clip Space, then write dist/clips/<clip>.webm, .mp4 and the provenance record."""
    from gradio_client import Client, handle_file
    c, src = CLIPS[clip], raw(clip, seed)
    run = [r for r in json.loads((OUT / "runs.json").read_text()) if r["clip"] == clip and r["seed"] == seed][-1]
    DIST.mkdir(parents=True, exist_ok=True)
    description = f"{c['place']}, animated from the painting in dist/places. Source photo: {c['source_photo']}."
    got_webm, got_mp4, got_seam, seam = Client(ENCODER).predict(
        handle_file(str(src)), FRAMES, FADE, FPS, webm_crf, mp4_crf, f"Colorado Startups: {clip}", LABEL, description,
        api_name="/export")
    webm, mp4 = DIST / f"{clip}.webm", DIST / f"{clip}.mp4"
    shutil.copyfile(got_webm, webm); shutil.copyfile(got_mp4, mp4); shutil.copyfile(got_seam, OUT / f"{clip}-{seed}-seam.jpg")
    files = {}
    for f in (webm, mp4):
        info = ffprobe(f, "format=duration:format_tags:stream=codec_type,width,height")
        tags = {k.lower(): v for k, v in info["format"].get("tags", {}).items()}
        v = next(s for s in info["streams"] if s["codec_type"] == "video")
        files[f.name] = {"bytes": f.stat().st_size, "seconds": round(float(info["format"]["duration"]), 2),
                         "size": f"{v['width']}x{v['height']}", "streams": [s["codec_type"] for s in info["streams"]],
                         "comment": tags.get("comment"), "sha256": sha(f)}
    record = {"clip": clip, "still": c["still"], "still_sha256": sha(ROOT / c["still"]), "place": c["place"],
              "source_photo": c["source_photo"], "model": "LTX-2.5 distilled 22B (Lightricks/LTX-2.5-Diffusers)",
              "lane": f"huggingface.co/spaces/{SPACE}, ZeroGPU on the HF PRO quota; encoded on {ENCODER} (free CPU)",
              "mode": "image-to-video", "prompt": run["prompt"], "prompt_enhancer": False, "seed": seed,
              "render": f"{WIDTH}x{HEIGHT}, {FRAMES} frames, {FPS} fps", "guidance": "1.0 (distilled, unguided)",
              "decoder": DECODER, "loop": f"last {FADE} frames dissolved frame by frame into the first {FADE}; {FRAMES - FADE} frames",
              "seam": json.loads(seam), "audio": "dropped", "label": LABEL, "raw_sha256": sha(src),
              "approved": approved, "billing": billing, "files": files}
    (DIST / f"{clip}.json").write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({"seam": json.loads(seam), "files": files}, indent=1))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("step", choices=["render", "frames", "export"])
    p.add_argument("clip", choices=sorted(CLIPS))
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--webm-crf", type=int, default=40)
    p.add_argument("--mp4-crf", type=int, default=28)
    p.add_argument("--approved", default="")
    p.add_argument("--billing", default="")
    a = p.parse_args()
    if a.step == "render":
        render(a.clip, a.seed)
    elif a.step == "frames":
        frames(a.clip, a.seed)
    else:
        export(a.clip, a.seed, a.webm_crf, a.mp4_crf, a.approved, a.billing)
