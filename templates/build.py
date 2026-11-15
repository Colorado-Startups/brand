#!/usr/bin/env python3
"""templates/build.py: the four application templates, composited from shipped files in seconds (decisions 49, 51).

  python3 templates/build.py    writes dist/templates/ (needs Pillow; no network, no model call)

Inputs are committed files only: dist/logo/ (decision 50), dist/places/ (decisions 43 to 45) and the CC0 Aileron in
guide/public/fonts/. AI-made art keeps its IPTC label in the output's metadata (decisions 8 and 46).
"""
import pathlib
import re

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUT = DIST / "templates"
FONT = ROOT / "guide" / "public" / "fonts" / "Aileron-Regular.otf"
BLUE, RED, WHITE = (0, 25, 112), (195, 0, 47), (255, 255, 255)
GUIDE = "https://colorado-startups.github.io/brand/"


def xmp_of(path):
    """The XMP packet already in a shipped image, so a composite keeps its AI-made label and credit."""
    raw = path.read_bytes()
    m = re.search(rb"<x:xmpmeta.*?</x:xmpmeta>", raw, re.S)
    return m.group(0) if m else None


def save_png(img, name, xmp=None):
    from PIL.PngImagePlugin import PngInfo
    info = PngInfo()
    if xmp:
        info.add_itxt("XML:com.adobe.xmp", xmp.decode())
    img.convert("RGB").save(OUT / name, "PNG", optimize=True, pnginfo=info)
    print(name, img.size, (OUT / name).stat().st_size // 1024, "KB")


def name(img, x, y, size, ink=WHITE, shadow=True):
    """The wordmark in the cards' proportions: a red rule 1.58 x the font size wide, then the name."""
    font = ImageFont.truetype(str(FONT), size)
    rule_h, gap = max(2, round(size * 0.08)), round(size * 0.27)
    if shadow:
        s = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(s).text((x, y + rule_h + gap + 3), "Colorado Startups", font=font, fill=(0, 10, 40, 200))
        img.alpha_composite(s.filter(ImageFilter.GaussianBlur(max(2, size // 12))))
    d = ImageDraw.Draw(img)
    d.rectangle((x, y, x + round(size * 1.58), y + rule_h), fill=RED + (255,))
    d.text((x, y + rule_h + gap - font.getbbox("C")[1]), "Colorado Startups", font=font, fill=ink + (255,))


def square():
    """512 square: the emblem at 78% on its own navy, safe for circle crops (Slack, LinkedIn, GitHub)."""
    src = DIST / "logo" / "emblem-1024.png"
    em = Image.open(src).convert("RGB")
    ground = Image.new("RGB", (512, 512), em.getpixel((8, 8)))
    s = round(512 * 0.78)
    ground.paste(em.resize((s, s), Image.LANCZOS), ((512 - s) // 2, (512 - s) // 2))
    save_png(ground, "square-512.png", xmp_of(src))


def linkedin_cover():
    """1128 x 191: the Boulder painting's middle band with the name at left (LinkedIn Page cover)."""
    src = DIST / "places" / "boulder.jpg"
    art = Image.open(src).convert("RGB")
    w = 1128; h = round(art.height * w / art.width)
    art = art.resize((w, h), Image.LANCZOS)
    top = round(h * 0.42) - 95
    img = art.crop((0, top, w, top + 191)).convert("RGBA")
    name(img, 300, 48, 54)
    save_png(img, "linkedin-cover-1128x191.png", xmp_of(src))


def slides():
    """1920 x 1080 backgrounds for a deck in the plain register: State blue, the name, room for a title."""
    for kind in ("title", "closing"):
        img = Image.new("RGBA", (1920, 1080), BLUE + (255,))
        if kind == "title":
            name(img, 120, 900, 56, shadow=False)
        else:
            name(img, 120, 440, 120, shadow=False)
            ImageDraw.Draw(img).text((120, 700), "coloradostartups.org", font=ImageFont.truetype(str(FONT), 48), fill=WHITE + (255,))
        save_png(img, f"slide-{kind}-1920x1080.png")


def email_signature():
    """An HTML email signature in the plain register; the wordmark loads from the guide's site."""
    html = f"""<!-- Colorado Startups email signature. Replace NAME and ROLE; paste into the mail client's signature box. -->
<table cellpadding="0" cellspacing="0" style="font-family:'Trebuchet MS',Arial,sans-serif;font-size:14px;line-height:1.4;color:#001970;max-width:600px">
  <tr><td style="padding:0 0 6px"><strong>NAME</strong><br>ROLE, Colorado Startups</td></tr>
  <tr><td style="padding:6px 0"><img src="{GUIDE}dist/logo/wordmark-blue.png" alt="Colorado Startups" width="200" style="display:block;border:0"></td></tr>
  <tr><td style="padding:4px 0 0"><a href="https://coloradostartups.org" style="color:#c3002f">coloradostartups.org</a></td></tr>
</table>
"""
    (OUT / "email-signature.html").write_text(html, encoding="utf-8")
    print("email-signature.html", len(html), "bytes")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    square(); linkedin_cover(); slides(); email_signature()
