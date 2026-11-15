"""The brand's clip encoder on the free CPU tier (decisions 37, 46, 61): ffmpeg runs here, never on the brand's Mac.

sheet   a contact sheet (every 8th frame), picked frames at 960 px, and per-frame brightness and change, for flashes
export  the loop (the clip's last `fade` frames dissolved, frame by frame, into its first), WebM (VP9) and MP4 (H.264), no audio, the
        AI-made label in the container's comment tag, and the seam check: the change across the loop's wrap against the
        change between ordinary neighbouring frames
The client, art/render/ltx_clips.py, sends every setting, so the brand's values live in one file.
"""
import json, statistics, subprocess, tempfile
import gradio as gr


def ff(*args):
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", *args], capture_output=True, text=True)
    if r.returncode:
        raise gr.Error(f"ffmpeg exited {r.returncode}: {r.stderr[:1500]}")


def series(path, vf):
    """Mean luma per output frame of a filter chain ending in signalstats."""
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"{vf},metadata=print:key=lavfi.signalstats.YAVG:file=-",
                          "-f", "null", "-"], check=True, capture_output=True, text=True).stdout
    return [float(line.split("=")[1]) for line in out.splitlines() if "YAVG=" in line]


def changes(path):
    """Mean absolute luma change between each frame and the next."""
    return series(path, "tblend=all_mode=difference,signalstats")


def sheet(video: str, picks: str):
    d = tempfile.mkdtemp()
    grid, four = f"{d}/sheet.jpg", f"{d}/picks.jpg"
    ff("-i", video, "-vf", "select='not(mod(n\\,8))',scale=640:-1,tile=4x4", "-frames:v", "1", "-q:v", "3", grid)
    sel = "+".join(f"eq(n\\,{int(p)})" for p in picks.split(","))
    ff("-i", video, "-vf", f"select='{sel}',scale=960:-1,tile=2x2", "-frames:v", "1", "-q:v", "2", four)
    y, dy = series(video, "signalstats"), changes(video)
    return grid, four, json.dumps({"frames": len(y), "luma_min": round(min(y), 1), "luma_max": round(max(y), 1),
                                   "largest_luma_step": round(max(abs(b - a) for a, b in zip(y, y[1:])), 2),
                                   "change_median": round(statistics.median(dy), 2), "change_max": round(max(dy), 2)})


def export(video: str, frames: int, fade: int, fps: int, webm_crf: int, mp4_crf: int, title: str, comment: str, description: str):
    frames, fade, fps = int(frames), int(fade), int(fps)
    d = tempfile.mkdtemp()
    # Frame-exact loop: frames fade..frames-fade-1 play as they are, then frames frames-fade..frames-1 dissolve into
    # frames 0..fade-1 by frame number, ending on pure frame fade-1, which frame fade follows at the wrap.
    z = "setpts=PTS-STARTPTS"
    loop = (f"[0:v]split=3[a][b][c];"
            f"[a]trim=start_frame={fade}:end_frame={frames - fade},{z}[body];"
            f"[b]trim=start_frame={frames - fade}:end_frame={frames},{z}[tail];"
            f"[c]trim=end_frame={fade},{z}[head];"
            f"[tail][head]blend=all_expr='A*(1-(N+1)/{fade})+B*((N+1)/{fade})':shortest=1,{z}[mix];"
            f"[body][mix]concat=n=2:v=1:a=0[v]")
    tags = ["-map_metadata", "-1", "-metadata", f"title={title}", "-metadata", f"comment={comment}",
            "-metadata", f"description={description}"]
    common = ["-i", video, "-filter_complex", loop, "-map", "[v]", "-an", "-r", str(fps), "-pix_fmt", "yuv420p"]
    webm, mp4 = f"{d}/clip.webm", f"{d}/clip.mp4"
    ff(*common, "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", str(int(webm_crf)), "-row-mt", "1", "-deadline", "good",
       "-cpu-used", "2", *tags, webm)
    ff(*common, "-c:v", "libx264", "-profile:v", "high", "-crf", str(int(mp4_crf)), "-preset", "slow",
       "-movflags", "+faststart", *tags, mp4)
    # The seam: decode the loop twice and join the frames (concat filter, frame-exact); the change across the wrap
    # sits between frame n-1 and frame n.
    twice, seam = f"{d}/twice.mkv", f"{d}/seam.jpg"
    ff("-i", mp4, "-i", mp4, "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]", "-map", "[v]", "-c:v", "ffv1", twice)
    dy = changes(twice)
    n = len(dy) // 2 + 1  # dy has 2n - 1 entries
    ordinary = dy[: n - 1]
    ff("-i", twice, "-vf", f"select='between(n\\,{n - 2}\\,{n + 1})',scale=480:-1,tile=4x1", "-frames:v", "1", "-q:v", "2", seam)
    report = {"loop_frames": n, "seam_change": round(dy[n - 1], 2), "ordinary_median": round(statistics.median(ordinary), 2),
              "ordinary_max": round(max(ordinary), 2)}
    return webm, mp4, seam, json.dumps(report)


num = lambda label, v: gr.Number(v, label=label, precision=0)
demo = gr.TabbedInterface(
    [gr.Interface(sheet, [gr.File(label="video", type="filepath"), gr.Textbox(label="picks", value="0,60,96,120")],
                  [gr.File(label="sheet"), gr.File(label="picks"), gr.Textbox(label="stats")], api_name="sheet"),
     gr.Interface(export, [gr.File(label="video", type="filepath"), num("frames", 121), num("fade", 24), num("fps", 24),
                           num("webm_crf", 40), num("mp4_crf", 28), gr.Textbox(label="title"), gr.Textbox(label="comment"),
                           gr.Textbox(label="description")],
                  [gr.File(label="webm"), gr.File(label="mp4"), gr.File(label="seam"), gr.Textbox(label="seam_report")],
                  api_name="export")],
    ["sheet", "export"], title="Colorado Startups brand clips")
demo.queue(default_concurrency_limit=1).launch(show_error=True)
