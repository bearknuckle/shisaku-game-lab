"""ホームの「関連サービス」に並べるバナー画像（1200x630, Xのリンクカードと同じ比率）を作る。

KUMA MUSIC ジュークボックスは自前のリンクプレビュー画像（jukebox ブランチの jukebox/og.png）があるので、
それを lab/services/jukebox.jpg にコピーして使う。PLAYABLE LAB と BOARD GAME PLAYGROUND は
プレビュー画像を持っていないので、ジュークボックスと同じレイアウトでここで描く。
必要なもの: pip install cairosvg fonttools / Noto Sans CJK フォント（fonts-noto-cjk）
使い方: python3 tools/make_service_banners.py
"""
import io
from pathlib import Path

import cairosvg
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTCollection
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "lab" / "services"
FONT_DIR = Path("/usr/share/fonts/opentype/noto")


def jp_font(name):
    col = TTCollection(str(FONT_DIR / name))
    return next(t for t in col.fonts if "JP" in t["name"].getDebugName(1))


def text_path(font, text):
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    pen, x = SVGPathPen(gs), 0
    for ch in text:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
        x += gs[g].width
    return x, pen.getCommands()


# PLAYABLE LAB のアイコン（stack-lab リポジトリの public/icon.svg と同じ絵。文字は輪郭にして描く）
def playable_icon(black):
    w1, p1 = text_path(black, "PLAYABLE")
    w2, p2 = text_path(black, "LAB")
    s1, s2 = 390 / w1, 0.115
    return (
        '<defs><linearGradient id="pbg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#06134f"/>'
        '<stop offset=".55" stop-color="#071b68"/><stop offset="1" stop-color="#0756d8"/></linearGradient>'
        '<radialGradient id="pglow"><stop stop-color="#087cff" stop-opacity=".75"/>'
        '<stop offset="1" stop-color="#071b59" stop-opacity="0"/></radialGradient></defs>'
        '<rect width="512" height="512" rx="112" fill="url(#pbg)"/>'
        '<ellipse cx="410" cy="95" rx="190" ry="150" fill="url(#pglow)"/>'
        '<ellipse cx="90" cy="420" rx="180" ry="140" fill="url(#pglow)"/>'
        f'<path transform="translate({256 - w1 * s1 / 2:.1f} 238) scale({s1:.5f})" fill="#fff" d="{p1}"/>'
        f'<path transform="translate({256 - w2 * s2 / 2:.1f} 345) scale({s2:.5f})" fill="#ffe600" d="{p2}"/>'
    )


# BOARD GAME PLAYGROUND のアイコン（サイトの色に合わせたサイコロとコマ）
def playground_icon():
    pips = "".join(f'<circle cx="{x}" cy="{y}" r="17" fill="#075b67"/>'
                   for x, y in [(178, 222), (268, 222), (178, 312), (268, 312), (223, 267)])
    return (
        '<defs><linearGradient id="gbg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0b9aa8"/>'
        '<stop offset="1" stop-color="#064b55"/></linearGradient></defs>'
        '<rect width="512" height="512" rx="112" fill="url(#gbg)"/>'
        '<g transform="rotate(-12 223 267)"><rect x="133" y="177" width="180" height="180" rx="34" fill="#f3f7f6"/>'
        f'{pips}</g>'
        '<path d="M296 392 Q300 306 352 268 Q404 306 408 392 Z" fill="#e7ae45"/>'
        '<circle cx="352" cy="236" r="38" fill="#e7ae45"/>'
        '<rect x="96" y="398" width="320" height="18" rx="9" fill="#ffffff" opacity=".25"/>'
    )


SERVICES = [
    {
        "file": "playable-lab.jpg",
        "bg": ("#0b1f78", "#050a26"),
        "icon": "playable",
        "title": ["PLAYABLE", "LAB"],
        "title_color": "#fff8e6",
        "bars": ["#ffe600", "#4fa3ff", "#ffffff"],
        "sub": ["遊びながらルールを覚える", "「遊べる説明書」"],
        "sub_color": "#d6dcff",
    },
    {
        "file": "board-game-playground.jpg",
        "bg": ("#0a7480", "#04363d"),
        "icon": "playground",
        "title": ["BOARD GAME", "PLAYGROUND"],
        "title_color": "#fffaf0",
        "bars": ["#e7ae45", "#ffffff", "#8fe3d6"],
        "sub": ["ボードゲームのルールを", "遊びながら確認できる"],
        "sub_color": "#d4eeea",
    },
]


def banner(svc, black, bold):
    icon = playable_icon(black) if svc["icon"] == "playable" else playground_icon()
    top, bottom = svc["bg"]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">',
        f'<defs><radialGradient id="bgg" cx=".3" cy="0" r="1.1"><stop stop-color="{top}"/>'
        f'<stop offset="1" stop-color="{bottom}"/></radialGradient>'
        '<filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="14" '
        'stdDeviation="22" flood-color="#000" flood-opacity=".45"/></filter></defs>',
        '<rect width="1200" height="630" fill="url(#bgg)"/>',
        f'<g filter="url(#sh)" transform="translate(90 115) scale(0.78)">{icon}</g>',
    ]
    # タイトル（2行）。いちばん長い行が 540px に収まる大きさで、2行とも同じ大きさにする
    paths = [text_path(black, t) for t in svc["title"]]
    sc = min(0.088, 540 / max(w for w, _ in paths))
    for i, (_, d) in enumerate(paths):
        parts.append(f'<path transform="translate(556 {212 + i * 92}) scale({sc:.5f})" '
                     f'fill="{svc["title_color"]}" d="{d}"/>')
    for i, (color, x, w) in enumerate(zip(svc["bars"], (556, 586, 616), (378, 318, 258))):
        parts.append(f'<rect x="{x}" y="{330 + i * 17 + 0}" width="{w}" height="8" rx="4" fill="{color}"/>')
    for i, line in enumerate(svc["sub"]):
        _, d = text_path(bold, line)
        parts.append(f'<path transform="translate(556 {442 + i * 50}) scale(0.034)" '
                     f'fill="{svc["sub_color"]}" d="{d}"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    OUT.mkdir(exist_ok=True)
    black, bold = jp_font("NotoSansCJK-Black.ttc"), jp_font("NotoSansCJK-Bold.ttc")
    for svc in SERVICES:
        png = cairosvg.svg2png(bytestring=banner(svc, black, bold).encode(),
                               output_width=1200, output_height=630)
        dest = OUT / svc["file"]
        Image.open(io.BytesIO(png)).convert("RGB").save(dest, quality=86, optimize=True, progressive=True)
        print("wrote", dest)


if __name__ == "__main__":
    main()
