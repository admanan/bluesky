#!/usr/bin/env python3
"""สร้างหน้า Home, หน้ารายการระดับ, ภาพปกของแต่ละกล และปุ่มนำทางในทุกหน้ากลใหม่
รัน:  python3 wiki/tools/build_wiki.py
เนื้อหาของแต่ละกลอยู่ใน wiki/tricks/*.md ระหว่างบรรทัด <!-- body:start --> ... <!-- body:end --> (แก้ได้ตามปกติ)
ข้อมูลกล (ชื่อ/สรุป/แท็ก) อยู่ใน tricks_meta.py"""
import os, re
from xml.sax.saxutils import escape
from tricks_meta import TRICKS, BY_SLUG, TAGS, TRACKS, LEVELS

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FONT = "'Sarabun','Noto Sans Thai','Tahoma',sans-serif"


def level_page(track, level):
    return f"{TRACKS[track][2]}-{LEVELS[level][2]}.md"


def read_trick(slug):
    t = open(os.path.join(ROOT, "tricks", slug + ".md"), encoding="utf-8").read()
    title = re.search(r"<!-- title:(.*?) -->", t).group(1)
    body = re.search(r"<!-- body:start -->\n(.*)<!-- body:end -->", t, re.S).group(1)
    return title, body


# ------------------------------------------------------------------ ภาพปก
def thumb(t):
    em, lvname, _, bg, fg = LEVELS[t["level"]]
    tem, trname, _ = TRACKS[t["track"]]
    glyph = escape(t["glyph"])
    size = 54 if len(t["glyph"]) <= 4 else 40 if len(t["glyph"]) <= 7 else 30
    title = escape(t["short"])
    tsize = 19 if len(t["short"]) <= 18 else 16
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180" width="320" height="180" font-family="{FONT}">
<rect width="320" height="180" rx="14" fill="{bg}" stroke="{fg}" stroke-width="2"/>
<rect x="14" y="14" width="{86 + len(trname) * 6}" height="24" rx="12" fill="#fff" stroke="{fg}"/>
<text x="26" y="31" font-size="13" font-weight="700" fill="{fg}">{escape(trname)} · {lvname}</text>
<text x="160" y="104" font-size="{size}" font-weight="700" text-anchor="middle" fill="#1f2937">{glyph}</text>
<text x="160" y="156" font-size="{tsize}" font-weight="700" text-anchor="middle" fill="{fg}">{title}</text>
</svg>'''
    d = os.path.join(ROOT, "images", "thumbs")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, t["slug"] + ".svg"), "w", encoding="utf-8").write(svg)


# ------------------------------------------------------------------ การ์ด
def badges(t):
    return " · ".join([f"⏱ {t['time']}"] + [TAGS[g] for g in t["tags"]])


def badges_short(t):
    """ในการ์ดใช้เฉพาะอีโมจิ (ความหมายดูที่คำอธิบายสัญลักษณ์ในหน้า Home)"""
    return f"⏱ {t['time']}" + ("  " + " ".join(TAGS[g].split()[0] for g in t["tags"]) if t["tags"] else "")


def card_grid(items, prefix, cols=3):
    """prefix = พาธจากหน้าปัจจุบันไปยัง tricks/ และ images/ ('' หรือ '../')"""
    rows = []
    for i in range(0, len(items), cols):
        cells = []
        for t in items[i:i + cols]:
            href = f"{prefix}tricks/{t['slug']}.md"
            cells.append(
                f'<td width="{100 // cols}%" valign="top">'
                f'<a href="{href}"><img src="{prefix}images/thumbs/{t["slug"]}.svg" alt="{escape(t["short"])}" width="100%"></a><br>'
                f'<b><a href="{href}">{escape(t["short"])}</a></b><br>{escape(t["summary"])}<br>'
                f'<sub>{badges_short(t)}</sub></td>')
        cells += ['<td width="%d%%"></td>' % (100 // cols)] * (cols - len(items[i:i + cols]))
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>\n"


def group(track, level):
    return [t for t in TRICKS if t["track"] == track and t["level"] == level]


# ------------------------------------------------------------------ หน้ากล
def build_trick(t):
    title, body = read_trick(t["slug"])
    tem, trname, _ = TRACKS[t["track"]]
    lem, lvname, _, _, _ = LEVELS[t["level"]]
    seq = [x for x in TRICKS if x["track"] == t["track"]]
    i = seq.index(t)
    prev, nxt = (seq[i - 1] if i else None), (seq[i + 1] if i + 1 < len(seq) else None)
    lp = "../" + level_page(t["track"], t["level"])
    nav = []
    nav.append(f"⬅️ [{LEVELS[prev['level']][0]} {prev['short']}]({prev['slug']}.md)" if prev else "")
    nav.append(f"[📋 {trname} · ระดับ{lvname} ทั้งหมด]({lp})")
    nav.append(f"[{LEVELS[nxt['level']][0]} {nxt['short']}]({nxt['slug']}.md) ➡️" if nxt else "")
    rel = " · ".join(f"[{LEVELS[BY_SLUG[r]['level']][0]} {BY_SLUG[r]['short']}]({r}.md)" for r in t["related"])
    out = (f"[🏠 หน้าแรก](../Home.md) › [{tem} {trname}]({lp}) › {t['short']}\n\n"
           f"# {title}\n\n"
           f"> {lem} **ระดับ{lvname}** · {tem} {trname} · {badges(t)}\n\n"
           f"<!-- title:{title} -->\n<!-- body:start -->\n{body}<!-- body:end -->\n\n"
           f"---\n\n" + "  ·  ".join(x for x in nav if x) + "\n" +
           (f"\n**กลที่เกี่ยวข้อง:** {rel}\n" if rel else ""))
    open(os.path.join(ROOT, "tricks", t["slug"] + ".md"), "w", encoding="utf-8").write(out)


# ------------------------------------------------------------------ หน้ารายการระดับ
def build_level(track, level):
    tem, trname, _ = TRACKS[track]
    lem, lvname, _, _, _ = LEVELS[level]
    items = group(track, level)
    other = [(l, level_page(track, l)) for l in (1, 2, 3) if l != level]
    nav = "  ·  ".join(f"[{LEVELS[l][0]} ระดับ{LEVELS[l][1]}]({p})" for l, p in other)
    out = (f"[🏠 หน้าแรก](Home.md) › {tem} {trname} › ระดับ{lvname}\n\n"
           f"# {tem} {trname} — {lem} ระดับ{lvname} ({len(items)} กล)\n\n"
           f"คลิกที่การ์ดเพื่อเปิดอ่านทีละกล\n\n" + card_grid(items, "") +
           f"\n---\n\nดูระดับอื่น: {nav}\n")
    open(os.path.join(ROOT, level_page(track, level)), "w", encoding="utf-8").write(out)


# ------------------------------------------------------------------ Home
def build_home():
    n_sw = sum(t["track"] == "sw" for t in TRICKS); n_sl = len(TRICKS) - n_sw
    L = []
    L.append("# 🃏 Wiki มายากลไพ่ (Card Magic Wiki)\n")
    L.append("![cover](images/cover.svg)\n")
    L.append(f"**{len(TRICKS)} กล** · ไพ่คำนวณ {n_sw} กล · ไพ่ฝีมือ {n_sl} กล · ทุกกลมีภาพประกอบ และเปิดอ่านได้ทีละกล\n")
    L.append("| 🚀 เริ่มต้น | คำอธิบาย |\n|---|---|\n"
             "| 📖 [พื้นฐานและศัพท์](Basics.md) | อุปกรณ์ ศัพท์ หลักการแสดง วิธีฝึก (อ่าน 10 นาที) |\n"
             "| 🗺 [เส้นทางการเรียน 8 สัปดาห์](Learning-Path.md) | แผนฝึกเป็นสัปดาห์ ไล่ง่าย → ยาก |\n"
             "| 🔎 [หากลตามเงื่อนไข](#filter) | ผู้ชมสับได้ / ไม่ต้องจัดสำรับ / ต้องมีผู้ช่วย … |\n")
    legend = " · ".join(["⏱ เวลาเรียนโดยประมาณ"] + [v for v in TAGS.values()])
    L.append(f"<sub>สัญลักษณ์ในการ์ด: {legend}</sub>\n")
    L.append('| ไปที่ | 🟢 ง่าย | 🟡 กลาง | 🔴 ยาก |\n|---|---|---|---|\n'
             + "\n".join(f"| **{TRACKS[tr][0]} {TRACKS[tr][1]}** | " +
                         " | ".join(f"[{len(group(tr, lv))} กล](#{tr}-{lv})" for lv in (1, 2, 3)) + " |" for tr in ("sw", "sl")) + "\n")
    for tr in ("sw", "sl"):
        tem, trname, tenname = TRACKS[tr]
        desc = ("ผลลัพธ์เกิดจากหลักการ/การจัดสำรับ ไม่ต้องใช้ฝีมือ" if tr == "sw" else "ใช้เทคนิคมือควบคุมไพ่ ต้องฝึกหน้ากระจก")
        L.append(f"\n---\n\n## {tem} {trname} ({tenname})\n\n{desc}\n")
        for lv in (1, 2, 3):
            lem, lvname, _, _, _ = LEVELS[lv]
            items = group(tr, lv)
            L.append(f'\n<a id="{tr}-{lv}"></a>\n\n### {lem} ระดับ{lvname} — {len(items)} กล\n')
            L.append(card_grid(items, ""))
            L.append(f"\n[📋 ดูแบบรายการ: {trname} ระดับ{lvname}]({level_page(tr, lv)})\n")
    L.append('\n---\n\n<a id="filter"></a>\n\n## 🔎 หากลตามเงื่อนไข\n')
    L.append("| อยากได้กลที่… | กล |\n|---|---|")
    for key, label in TAGS.items():
        ts = [t for t in TRICKS if key in t["tags"]]
        L.append(f"| {label} | " + " · ".join(f"[{t['short']}](tricks/{t['slug']}.md)" for t in ts) + " |")
    L.append("\n## ⚖️ ไพ่คำนวณ vs ไพ่ฝีมือ\n")
    L.append("| | ไพ่คำนวณ | ไพ่ฝีมือ |\n|---|---|---|\n| หลักการ | คณิตศาสตร์ / การจัดสำรับ / หลักการสับ | การควบคุมไพ่ด้วยมือ |\n"
             "| ต้องฝึกมือ | น้อย–ปานกลาง | มาก |\n| ต้องฝึกพูด/จังหวะ | **มาก** (วิธีเรียบง่าย ต้องใช้ศิลปะการแสดง) | **มาก** |\n"
             "| ข้อดี | เริ่มเล่นได้ในวันเดียว สำรับยืมได้ | ผลลัพธ์ดูเหลือเชื่อ ยืดหยุ่น |\n| ข้อควรระวัง | เล่นซ้ำคนจับทางได้ง่าย | ฝึกไม่พอ = เห็นเทคนิค |\n")
    L.append("> ⚠️ **จริยธรรมนักมายากล:** ความสนุกอยู่ที่ \"ความอัศจรรย์ใจ\" ไม่ใช่การหลอกลวงเอาประโยชน์ อย่านำไปใช้กับการพนัน/การโกงเงิน และอย่าเฉลยวิธีให้ผู้ชมระหว่างการแสดง\n")
    L.append("## 🧪 เครื่องมือตรวจสอบและฝึกซ้อม (`wiki/tools/`)\n")
    L.append("| สคริปต์ | หน้าที่ |\n|---|---|\n"
             "| `verify_tricks.py [--fitch]` | ตรวจความถูกต้องของกลไพ่คำนวณทุกกลด้วยการจำลอง (`--fitch` ตรวจครบทุก 2.6 ล้านมือ) |\n"
             "| `fitch_drill.py` | สร้างโจทย์ฝึกถอดรหัส Fitch–Cheney |\n| `mnemonica_drill.py` | ฝึกท่องตำแหน่ง Mnemonica / Si Stebbins |\n"
             "| `generate_images.py` | สร้างภาพประกอบ SVG ของแต่ละกล |\n| `build_wiki.py` | สร้างหน้า Home / รายการระดับ / ภาพปก / ปุ่มนำทางจาก `tricks_meta.py` |\n")
    open(os.path.join(ROOT, "Home.md"), "w", encoding="utf-8").write("\n".join(L))


def main():
    for t in TRICKS:
        thumb(t)
        build_trick(t)
    for tr in ("sw", "sl"):
        for lv in (1, 2, 3):
            build_level(tr, lv)
    build_home()
    print("สร้างแล้ว: หน้ากล", len(TRICKS), "· ภาพปก", len(TRICKS), "· หน้ารายการระดับ 6 · Home")


if __name__ == "__main__":
    main()
