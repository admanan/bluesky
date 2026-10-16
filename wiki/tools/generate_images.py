#!/usr/bin/env python3
"""สร้างภาพประกอบ SVG ทั้งหมดของ wiki  (รัน: python3 wiki/tools/generate_images.py)"""
import os, random
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "images")
FONT = "'Sarabun','Noto Sans Thai','Tahoma',sans-serif"
INK, MUTE, BG, PAPER = "#1f2937", "#6b7280", "#faf8f3", "#ffffff"
RED, BLUE, GREEN, GOLD, GRAY = "#c62828", "#1d4ed8", "#15803d", "#f59e0b", "#d1d5db"


class Svg:
    def __init__(self, w, h, title):
        self.w, self.h, self.parts = w, h, []
        self.parts.append(f'<rect width="{w}" height="{h}" rx="14" fill="{BG}" stroke="#e5e0d3"/>')
        self.text(w / 2, 30, title, 20, "middle", 700)

    def text(self, x, y, s, size=13, anchor="start", weight=400, fill=INK):
        self.parts.append(
            f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" '
            f'fill="{fill}">{escape(str(s))}</text>')

    def rect(self, x, y, w, h, fill=PAPER, stroke="#9ca3af", sw=1.2, rx=6, extra=""):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
                          f'stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def line(self, x1, y1, x2, y2, stroke=MUTE, sw=2, dash=None, arrow=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = ' marker-end="url(#ar)"' if arrow else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}{m}/>')

    def circle(self, x, y, r, fill=GOLD, stroke="none"):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}"/>')

    def step(self, x, y, n):
        self.circle(x, y, 13, BLUE)
        self.text(x, y + 5, n, 14, "middle", 700, "#fff")

    def card(self, x, y, label=None, w=48, h=68, hl=False, back=False):
        stroke = GOLD if hl else "#6b7280"
        sw = 3.5 if hl else 1.3
        if back or label is None:
            self.rect(x, y, w, h, "#2f4b8f", stroke, sw, 6)
            self.rect(x + 5, y + 5, w - 10, h - 10, "none", "#9db4e8", 1, 3)
            return
        self.rect(x, y, w, h, PAPER, stroke, sw, 6)
        col = RED if label[-1] in "♥♦" else INK
        self.text(x + 6, y + 19, label, 16, "start", 700, col)
        self.text(x + w / 2, y + h - 14, label[-1], 28, "middle", 400, col)

    def strip(self, x, y, label, w=96, h=24, fill=PAPER, hl=False, color=None):
        self.rect(x, y, w, h, fill, GOLD if hl else "#9ca3af", 3 if hl else 1.2, 5)
        self.text(x + w / 2, y + h / 2 + 5, label, 14, "middle", 600,
                  color or (RED if str(label)[-1:] in "♥♦" else INK))

    def save(self, name):
        defs = (f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
                f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTE}"/></marker></defs>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
               f'height="{self.h}" font-family="{FONT}">{defs}{"".join(self.parts)}</svg>')
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)


def stack(s, x, y, labels, hl=(), w=96, gap=26):
    for i, lb in enumerate(labels):
        s.strip(x, y + i * gap, lb, w, 24, hl=i in hl,
                fill="#e8eefc" if lb == "…" else PAPER)


# ---------------------------------------------------------------- self-working
def keycard():
    s = Svg(760, 330, "ไพ่คีย์ (Key Card): ไพ่ใบที่คนดูเลือก จะอยู่ติดหลังไพ่คีย์เสมอ")
    cols = [("① แอบดูไพ่ใบล่างสุด", ["?", "?", "…", "?", "7♣"], (4,)),
            ("② คนดูหยิบไพ่ X มาวางบนสุด", ["K♦", "?", "…", "?", "7♣"], (0, 4)),
            ("③ ตัดสำรับกี่ครั้งก็ได้", ["?", "…", "7♣", "K♦", "?", "?"], (2, 3))]
    for i, (t, labs, hl) in enumerate(cols):
        x = 40 + i * 245
        s.step(x + 12, 62, i + 1)
        s.text(x + 32, 67, t[2:], 14, "start", 600)
        stack(s, x + 10, 90, labs, hl)
        if i < 2:
            s.line(x + 130, 170, x + 195, 170, arrow=True)
    s.text(380, 290, "ไพ่คีย์ = 7♣ (ใบที่แอบดู)   ไพ่ที่คนดูเลือก = ใบถัดจากไพ่คีย์ = K♦", 15, "middle", 700, GREEN)
    s.text(380, 312, "สำรับต้องไม่ถูก 'สับ' หลังขั้นตอน ② ตัดได้อย่างเดียว", 13, "middle", 400, MUTE)
    s.save("keycard.svg")


def nine_cards():
    s = Svg(760, 360, "ไพ่ 9 ใบ: คนดูเลือกไพ่ในใจ  →  ถามแค่ 2 ครั้ง  →  ใบที่ 5 เสมอ")
    # round grid
    def grid(x, title, nums, hl_rows=None, hl_cells=()):
        s.text(x + 90, 62, title, 14, "middle", 600)
        for p in range(3):
            s.text(x + 30 + p * 62, 84, "กอง " + "ABC"[p], 12, "middle", 400, MUTE)
            for r in range(3):
                n = nums[r * 3 + p]
                s.rect(x + 8 + p * 62, 92 + r * 40, 44, 32, "#fff3cd" if n in hl_cells else PAPER,
                       GOLD if n in hl_cells else "#9ca3af", 2.5 if n in hl_cells else 1.2, 5)
                s.text(x + 30 + p * 62, 113 + r * 40, n, 15, "middle", 700)
    grid(20, "รอบที่ 1: แจก 9 ใบ (หงายหน้า)", list(range(1, 10)))
    s.text(390, 175, "คนดูบอกว่าอยู่กองไหน →", 12, "middle", 400, MUTE)
    s.line(215, 100, 275, 100, arrow=True)
    # gather
    s.text(375, 62, "เก็บ: กองที่ถูกเลือกไว้ 'ตรงกลาง'", 14, "middle", 600)
    for i, (lb, hl) in enumerate([("กองอื่น (ใบ 1–3)", False), ("กองที่เลือก (ใบ 4–6)", True), ("กองอื่น (ใบ 7–9)", False)]):
        s.strip(285, 85 + i * 40, lb, 180, 30, fill="#fff3cd" if hl else PAPER, hl=hl)
    s.text(375, 215, "ไพ่ในใจอยู่ตำแหน่ง 4, 5 หรือ 6", 13, "middle", 700, BLUE)
    s.line(475, 130, 530, 130, arrow=True)
    # round 2
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    s.text(645, 62, "รอบที่ 2: แจกอีกครั้ง", 14, "middle", 600)
    for p in range(3):
        s.text(570 + p * 62 + 22, 84, "กอง " + "ABC"[p], 12, "middle", 400, MUTE)
        for r in range(3):
            n = nums[r * 3 + p]
            hl = r == 1
            s.rect(550 + p * 62, 92 + r * 40, 44, 32, "#fff3cd" if hl else PAPER, GOLD if hl else "#9ca3af",
                   2.5 if hl else 1.2, 5)
            s.text(572 + p * 62, 113 + r * 40, "4 5 6".split()[p] if hl else "·", 15, "middle", 700)
    s.text(645, 232, "ใบที่ 4,5,6 ไปอยู่แถวกลางของแต่ละกอง", 12, "middle", 400, MUTE)
    s.rect(40, 262, 680, 76, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 290, "คนดูบอกกองที่ 2  →  ไพ่ในใจคือ 'แถวกลาง' ของกองนั้น", 15, "middle", 700, GREEN)
    s.text(380, 316, "(เก็บกองนั้นไว้ตรงกลางอีกครั้ง → ไพ่ในใจคือใบที่ 5 ของสำรับ 9 ใบ)", 13, "middle", 400, INK)
    s.save("nine-cards.svg")


def twentyone():
    s = Svg(760, 380, "ไพ่ 21 ใบ: 3 รอบ → ไพ่ในใจคือ 'ใบที่ 11' เสมอ")
    s.text(130, 62, "แจกหงายหน้า 3 กอง × 7 ใบ", 14, "middle", 600)
    for p in range(3):
        s.text(60 + p * 60, 82, "กอง " + "ABC"[p], 12, "middle", 400, MUTE)
        for r in range(7):
            n = r * 3 + p + 1
            mid = 8 <= n <= 14
            s.rect(38 + p * 60, 90 + r * 30, 44, 25, "#fff3cd" if mid else PAPER, GOLD if mid else "#9ca3af",
                   2 if mid else 1.1, 4)
            s.text(60 + p * 60, 108 + r * 30, n, 13, "middle", 600)
    s.text(130, 320, "เลข = ลำดับตอนแจก (แถบเหลือง = ใบที่ 8–14)", 11, "middle", 400, MUTE)
    # ranges
    s.text(555, 62, "ตำแหน่งที่ไพ่ในใจ 'เป็นไปได้' ในสำรับ 21 ใบ", 14, "middle", 600)
    rounds = [("เริ่มต้น", 1, 21), ("หลังรอบ 1", 8, 14), ("หลังรอบ 2", 10, 12), ("หลังรอบ 3", 11, 11)]
    x0, bw = 290, 12
    for i, (lb, a, b) in enumerate(rounds):
        y = 90 + i * 52
        s.text(x0 - 10, y + 15, lb, 12, "end", 600)
        for n in range(1, 22):
            on = a <= n <= b
            s.rect(x0 + (n - 1) * (bw + 2), y, bw, 24, GOLD if on else "#eef0f3", "#9ca3af" if not on else "#b45309", 0.8, 2)
        s.text(x0 + (a - 1) * (bw + 2), y + 40, f"ใบที่ {a}" + (f"–{b}" if b != a else ""), 11, "start", 400, MUTE)
    s.rect(290, 305, 440, 52, "#ecfdf5", GREEN, 1.5, 10)
    s.text(510, 328, "ทุกรอบ: เก็บกองที่ถูกเลือกไว้ 'ตรงกลาง' (ระหว่างอีก 2 กอง)", 13, "middle", 700, GREEN)
    s.text(510, 347, "จบรอบ 3 นับจากบน → ใบที่ 11 คือไพ่ที่คนดูคิดไว้", 13, "middle", 400)
    s.save("twentyone.svg")


def gilbreath():
    random.seed(7)
    stack_ = list("RBRBRBRB")
    table = list(reversed(stack_[:4]))  # แจกลงโต๊ะ 4 ใบ → กลับลำดับ
    hand = stack_[4:]
    a, b = table[:], hand[:]
    merged = []
    while a or b:
        if a and (not b or random.random() < .5):
            merged.append(a.pop(0))
        else:
            merged.append(b.pop(0))
    s = Svg(760, 400, "หลักการ Gilbreath: สลับแดง–ดำ → แจกกลับ → ริฟเฟิล = ทุกคู่มีแดง 1 ดำ 1")
    def col(c): return ("#fecaca", RED) if c == "R" else ("#d1d5db", INK)
    def column(x, y, seq, title, pairs=False):
        s.text(x + 30, y - 12, title, 13, "middle", 600)
        for i, c in enumerate(seq):
            f, t = col(c)
            s.rect(x, y + i * 30, 60, 24, f, "#6b7280", 1.2, 4)
            s.text(x + 30, y + i * 30 + 17, "แดง" if c == "R" else "ดำ", 13, "middle", 700, t)
        if pairs:
            for k in range(0, len(seq), 2):
                s.parts.append(f'<path d="M{x+68},{y+k*30} q10,0 10,10 v28 q0,10 -10,10" fill="none" stroke="{GREEN}" stroke-width="2.5"/>')
                s.text(x + 90, y + k * 30 + 33, "1 แดง + 1 ดำ", 12, "start", 700, GREEN)
    column(60, 80, stack_, "① จัดสลับสี")
    s.text(165, 130, "แจก 4 ใบ", 12, "middle", 400, MUTE); s.text(165, 148, "จากบนลงโต๊ะ", 12, "middle", 400, MUTE)
    s.line(130, 160, 200, 160, arrow=True)
    column(225, 80, table, "② กองโต๊ะ")
    column(325, 80, hand, "ในมือ")
    s.line(385, 160, 455, 160, arrow=True)
    s.text(420, 138, "ริฟเฟิล", 12, "middle", 400, MUTE); s.text(420, 154, "สับสลับ", 12, "middle", 400, MUTE)
    column(470, 80, merged, "③ หลังริฟเฟิล", pairs=True)
    s.rect(30, 340, 700, 44, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 368, "แจกไพ่ทีละ 2 ใบ → ทุกคู่ได้ 'แดง 1 ดำ 1' แม้ผู้ชมริฟเฟิลเองจนไม่รู้ลำดับ (ห้ามตัดเพิ่ม)", 13, "middle", 700, GREEN)
    # verify principle
    for i in range(0, 8, 2):
        assert set(merged[i:i + 2]) == {"R", "B"}
    s.save("gilbreath.svg")


SUITS = "♣♥♠♦"
RANKS = "A 2 3 4 5 6 7 8 9 10 J Q K".split()


def stebbins_seq(n=52):
    seq, v, su = [], 1, 0
    for _ in range(n):
        seq.append(RANKS[v - 1] + SUITS[su % 4])
        v = (v + 3 - 1) % 13 + 1
        su += 1
    return seq


def stebbins():
    seq = stebbins_seq()
    assert len(set(seq)) == 52
    s = Svg(760, 360, "Si Stebbins Stack: เลขเพิ่มทีละ 3 + ดอกวนรอบ ♣ ♥ ♠ ♦ (CHaSeD)")
    for i in range(13):
        x = 24 + (i % 7) * 104
        y = 56 + (i // 7) * 100
        s.card(x, y, seq[i], 56, 78)
        s.text(x + 28, y + 94, f"ใบที่ {i+1}", 11, "middle", 400, MUTE)
        if i % 7 != 6 and i < 12:
            s.text(x + 80, y + 44, "+3", 12, "middle", 700, BLUE)
            s.line(x + 60, y + 52, x + 98, y + 52, arrow=True)
    s.text(380, 276, "สูตร: ใบถัดไป = เลข +3 (K→A วนรอบ: K+3 = 3)  และ  ดอกถัดไปตามลำดับ ♣→♥→♠→♦→♣", 14, "middle", 700)
    s.rect(40, 292, 680, 50, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 313, "ตัวอย่าง: ไพ่คีย์ที่แอบดู = 10♦  →  ไพ่ที่คนดูหยิบ = เลข 10+3 = K, ดอกต่อจาก ♦ = ♣  →  K♣", 14, "middle", 700, GREEN)
    s.text(380, 332, "(สำรับ 52 ใบเรียงวนไม่ซ้ำ จึงตัดกี่ครั้งก็ยังเรียงต่อกันเสมอ)", 12, "middle", 400, MUTE)
    s.save("stebbins.svg")


def fitch():
    s = Svg(760, 450, "Fitch–Cheney 5 ใบ: ผู้ช่วยวาง 4 ใบ  →  นักมายากลบอกใบที่ 5")
    five = ["K♥", "3♥", "9♠", "7♣", "2♦"]
    s.text(30, 62, "① คนดูเลือก 5 ใบ  →  ผู้ช่วยหา 'ไพ่ดอกเดียวกัน 2 ใบ' (♥ ♥)", 14, "start", 600)
    for i, c in enumerate(five):
        s.card(40 + i * 70, 76, c, 54, 76, hl=c in ("K♥", "3♥"))
    s.text(30, 184, "② ระยะ K→A→2→3 = 3 (ไม่เกิน 6)  →  วาง K♥ เป็นใบแรก", 14, "start", 600)
    s.text(48, 204, "ใบที่ซ่อน = 3♥  และ d = 3", 14, "start", 600)
    s.text(30, 230, "③ ใบที่เหลือ 2♦ 7♣ 9♠ = เล็ก S / กลาง M / ใหญ่ L", 14, "start", 600)
    s.text(48, 250, "d = 3 ต้องวางเรียง M S L  (7♣, 2♦, 9♠)", 14, "start", 600)
    shown = ["K♥", "7♣", "2♦", "9♠"]
    for i, c in enumerate(shown):
        s.card(40 + i * 70, 266, c, 54, 76, hl=i == 0)
        s.text(67 + i * 70, 358, ["ดอก+จุดเริ่ม", "M กลาง", "S เล็ก", "L ใหญ่"][i], 11, "middle", 600, MUTE)
    s.text(350, 300, "นักมายากลเห็น K♥ 7♣ 2♦ 9♠", 14, "start", 700, BLUE)
    s.text(350, 324, "ดอก = ♥  ·  M S L = 3  ·  K + 3 = 3  →  3♥", 14, "start", 700, GREEN)
    s.text(540, 62, "ตารางรหัสระยะ d", 13, "start", 700)
    codes = ["S M L", "S L M", "M S L", "M L S", "L S M", "L M S"]
    for i, c in enumerate(codes):
        s.rect(540, 72 + i * 22, 190, 20, "#fff3cd" if i == 2 else PAPER, GOLD if i == 2 else "#9ca3af", 1.5 if i == 2 else 1, 4)
        s.text(552, 87 + i * 22, f"d = {i+1}", 13, "start", 700)
        s.text(718, 87 + i * 22, c, 13, "end", 600)
    s.rect(30, 378, 700, 60, "#eff6ff", BLUE, 1.2, 10)
    s.text(380, 400, "ลำดับขนาด: A<2<…<K  ถ้าเลขเท่ากันเทียบดอก ♣ < ♦ < ♥ < ♠", 13, "middle", 600)
    s.text(380, 422, "ใบแรก = บอกดอกของใบซ่อน  ·  ใบซ่อน = ใบแรก + d (K→A วนรอบ)", 13, "middle", 600)
    s.save("fitch-cheney.svg")


def faro_math():
    s = Svg(760, 400, "Faro Shuffle: คณิตศาสตร์ตำแหน่งไพ่ (ตัวอย่าง 8 ใบ → สูตรสำหรับ 52 ใบ)")
    orig = list(range(1, 9))
    inn = [5, 1, 6, 2, 7, 3, 8, 4]
    out = [1, 5, 2, 6, 3, 7, 4, 8]
    def col(x, y, seq, title, hl=None):
        s.text(x + 22, y - 10, title, 12, "middle", 600)
        for i, n in enumerate(seq):
            s.rect(x, y + i * 28, 44, 24, "#fff3cd" if n == hl else PAPER, GOLD if n == hl else "#9ca3af", 2 if n == hl else 1.1, 4)
            s.text(x + 22, y + i * 28 + 17, n, 14, "middle", 700)
    col(40, 70, orig, "ก่อนสับ", 1)
    s.line(100, 180, 150, 180, arrow=True)
    col(165, 70, inn, "In-shuffle", 1)
    col(285, 70, out, "Out-shuffle", 1)
    s.text(187, 322, "In: ใบ 1 ไปตำแหน่ง 2", 11, "middle", 400, MUTE)
    s.text(307, 322, "Out: ใบ 1 อยู่ที่เดิม", 11, "middle", 400, MUTE)
    s.rect(360, 56, 372, 150, PAPER, "#9ca3af", 1.2, 10)
    s.text(372, 80, "สำรับ 52 ใบ (ตำแหน่งนับจากบน = p)", 13, "start", 700)
    s.text(372, 106, "In-shuffle :  p  →  (2·p) mod 53", 14, "start", 600, BLUE)
    s.text(372, 128, "Out-shuffle :  p  →  (2·p − 1) mod 51   (ใบล่างสุดอยู่ที่เดิม)", 14, "start", 600, BLUE)
    s.text(372, 156, "ตัวอย่าง In: p=27 → 54 mod 53 = 1  (ใบที่ 27 ขึ้นบนสุด)", 13, "start")
    s.text(372, 178, "ตัวอย่าง Out: p=27 → 53 mod 51 = 2", 13, "start")
    s.rect(360, 218, 372, 130, "#ecfdf5", GREEN, 1.5, 10)
    s.text(372, 242, "ข้อเท็จจริงที่ใช้โชว์", 13, "start", 700, GREEN)
    for i, t in enumerate(["• Out-shuffle สมบูรณ์ 8 ครั้ง → สำรับกลับเป็นลำดับเดิม",
                           "• In-shuffle สมบูรณ์ 52 ครั้ง → กลับเป็นลำดับเดิม",
                           "• In-shuffle 26 ครั้ง → สำรับกลับหัวทั้งสำรับ"]):
        s.text(372, 268 + i * 26, t, 13, "start")
    s.save("faro-math.svg")
    # ตรวจสูตร
    inpos = lambda p: (2 * p) % 53
    assert inpos(1) == 2 and inpos(27) == 1 and inpos(52) == 51
    d = list(range(52)); ref = d[:]
    def faro(deck, inshuf):
        a, b = deck[:26], deck[26:]
        r = []
        for x, y in zip(a, b):
            r += [y, x] if inshuf else [x, y]
        return r
    x = ref[:]
    for _ in range(8): x = faro(x, False)
    assert x == ref
    x = ref[:]
    for _ in range(52): x = faro(x, True)
    assert x == ref
    x = ref[:]
    for _ in range(26): x = faro(x, True)
    assert x == ref[::-1]


# ---------------------------------------------------------------- sleight of hand
def overhand():
    s = Svg(760, 360, "Overhand Shuffle: ใบบนสุดลงไปล่างสุด / ใบล่างสุดขึ้นมาบนสุด")
    steps = [
        ("เริ่มต้น", [1, 2, 3, 4, 5, 6], [], "มือขวาถือสำรับ"),
        ("ดึงใบแรก 'ทีละใบ'", [2, 3, 4, 5, 6], [1], "นิ้วโป้งซ้ายดึง 1 ออกมา"),
        ("ดึงเป็นกอง 2–3 ใบ", [4, 5, 6], [2, 3, 1], "กองใหม่วาง 'ทับ' ด้านบน"),
        ("ใบสุดท้ายหย่อนทีละใบ", [], [6, 4, 5, 2, 3, 1], "6 (ใบล่างเดิม) ขึ้นบนสุด"),
    ]
    for i, (t, right, left, note) in enumerate(steps):
        x = 30 + i * 180
        s.step(x + 12, 62, i + 1)
        s.text(x + 30, 67, t, 13, "start", 600)
        s.text(x, 98, "มือขวา" if True else "", 12, "start", 400, MUTE)
        for k, n in enumerate(right):
            s.strip(x, 106 + k * 26, n, 70, 22, hl=False, fill="#eef2ff")
        s.text(x, 262, "มือซ้าย", 12, "start", 400, MUTE) if False else None
        for k, n in enumerate(left):
            s.strip(x + 84, 106 + k * 26, n, 70, 22, fill="#fff3cd" if (i == 3 and n == 6) or (i == 1 and n == 1) else PAPER)
        s.text(x + 84, 98, "มือซ้าย", 12, "start", 400, MUTE)
        s.text(x, 290, note, 12, "start", 400, MUTE)
    s.rect(30, 308, 700, 38, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 332, "แถบบนสุดของคอลัมน์ = ไพ่ใบบนสุดของกอง   ·   ตัวเลข = ลำดับไพ่เดิม (1 อยู่บน … 6 อยู่ล่าง)", 13, "middle", 600, GREEN)
    s.save("overhand.svg")


def glimpse():
    s = Svg(760, 300, "Glimpse: แอบดูไพ่ใบล่างสุดตอนเคาะสำรับให้เรียบ")
    # side view
    s.text(190, 62, "มองจากด้านข้าง", 14, "middle", 600)
    s.rect(60, 150, 260, 14, "#2f4b8f", "#1e2f5c", 1.2, 3)
    for i in range(6):
        s.line(60, 148 - i * 0, 320, 148, "#1e2f5c", 0.6)
    s.parts.append('<polygon points="60,150 320,150 300,164 40,164" fill="#2f4b8f" stroke="#1e2f5c"/>')
    s.parts.append('<polygon points="60,164 130,164 130,184 60,184" fill="#fff" stroke="#6b7280"/>')
    s.text(66, 180, "7♣", 14, "start", 700)
    s.text(190, 210, "ปลายสำรับฝั่งนิ้วหัวแม่มือยกขึ้นเล็กน้อย", 12, "middle", 400, MUTE)
    s.text(190, 228, "ดัชนีมุมของใบล่างสุดจะโผล่ให้เห็น", 12, "middle", 400, MUTE)
    s.line(190, 118, 100, 160, GOLD, 3, arrow=True)
    s.text(215, 112, "สายตา", 12, "start", 600)
    s.step(36, 62, 1)
    # top view
    s.text(560, 62, "ท่าเคาะสำรับ (มองจากด้านบน)", 14, "middle", 600)
    s.card(470, 80, None, 90, 128, back=True)
    s.card(486, 96, None, 90, 128, back=True)
    s.card(470, 80, "7♣", 90, 128) if False else None
    s.rect(470, 180, 22, 28, PAPER, GOLD, 3, 3)
    s.text(481, 200, "7♣", 11, "middle", 700)
    s.text(570, 150, "← มุมล่างซ้ายโผล่", 12, "start", 700, BLUE)
    s.text(380, 270, "เคล็ดลับ: ทำระหว่างที่พูดคุย / จัดสำรับให้เรียบ ห้ามหยุดมือหรือมองนาน", 13, "middle", 700, GREEN)
    s.save("glimpse.svg")


def crosscut():
    s = Svg(760, 330, "Cross-Cut Force: บังคับให้คนดูได้ไพ่ใบที่เรารู้ (F)")
    # step1
    s.step(40, 62, 1); s.text(62, 67, "ไพ่ F อยู่บนสุด", 13, "start", 600)
    stack(s, 40, 90, ["F", "?", "…", "?"], (0,), w=90)
    s.text(85, 214, "คนดูตัดสำรับ", 12, "middle", 400, MUTE)
    s.line(140, 140, 215, 140, arrow=True)
    # step2
    s.step(230, 62, 2); s.text(252, 67, "กอง A ลงโต๊ะ", 13, "start", 600)
    stack(s, 235, 90, ["F", "?", "…"], (0,), w=80)
    s.text(275, 190, "กอง A (บนมี F)", 12, "middle", 400, MUTE)
    stack(s, 235, 215, ["?", "…", "?"], (), w=80)
    s.text(275, 305, "กอง B (ที่เหลือในมือ)", 12, "middle", 400, MUTE)
    s.line(330, 250, 405, 200, arrow=True)
    # step3
    s.step(430, 62, 3); s.text(452, 67, "วางกอง B 'ไขว้' ทับ A", 13, "start", 600)
    s.rect(440, 120, 120, 22, PAPER, "#9ca3af", 1.2, 5); s.text(452, 136, "A", 12, "start", 700)
    s.rect(500, 82, 24, 100, "#e8eefc", "#6b7280", 1.5, 5)
    s.text(512, 108, "B", 14, "middle", 700)
    s.text(540, 136, "F", 12, "start", 700, GREEN)
    s.text(495, 200, "คุยต่ออีกสักพัก…", 12, "middle", 400, MUTE)
    s.line(580, 140, 640, 140, arrow=True)
    s.step(655, 62, 4); s.text(677, 67, "ยก B ออก", 13, "start", 600)
    s.strip(640, 100, "F", 90, 26, hl=True)
    s.text(685, 150, "ใบที่อยู่ใต้ B", 12, "middle", 600, GREEN)
    s.text(685, 168, "คือ F เสมอ", 12, "middle", 600, GREEN)
    s.rect(430, 250, 300, 56, "#ecfdf5", GREEN, 1.5, 10)
    s.text(580, 274, "ยกกอง B ออก → 'เลือก' ใบบนสุดของกอง A", 13, "middle", 700, GREEN)
    s.text(580, 294, "ปล่อยเวลาพอให้คนลืมว่าตัดตรงไหน", 12, "middle", 400)
    s.save("cross-cut-force.svg")


def double_lift():
    s = Svg(760, 330, "Double Lift: พลิกไพ่ 2 ใบให้เหมือนใบเดียว")
    # side views
    def side(x, y, n_off, label):
        s.text(x + 90, y - 16, label, 13, "middle", 600)
        s.parts.append(f'<rect x="{x}" y="{y+40}" width="180" height="10" rx="3" fill="#2f4b8f" stroke="#1e2f5c"/>')
        for i in range(2):
            off = 0 if n_off else 0
            s.parts.append(f'<rect x="{x+10+off}" y="{y+22-i*10}" width="160" height="9" rx="3" fill="#fff" stroke="#6b7280"/>')
    s.step(40, 62, 1); s.text(62, 67, "จับไพ่ 2 ใบบนสุดเป็นก้อนเดียว", 13, "start", 600)
    stack(s, 60, 100, ["A+B = 'ใบเดียว'", "ใบที่ 3", "…"], (0,), w=150)
    s.line(230, 130, 290, 130, arrow=True)
    s.step(305, 62, 2); s.text(327, 67, "จับด้วยนิ้วโป้ง+นิ้วชี้ขวา", 13, "start", 600)
    s.rect(300, 100, 150, 24, "#fff3cd", GOLD, 3, 5); s.text(375, 117, "A (บน) ซ้อน B (ล่าง)", 13, "middle", 700)
    s.text(375, 150, "พลิกขึ้นเหมือนพลิกใบเดียว", 12, "middle", 400, MUTE)
    s.line(470, 130, 520, 130, arrow=True)
    s.step(530, 62, 3); s.text(552, 67, "หงายหน้า = เห็นหน้า B", 13, "start", 600)
    s.card(540, 90, "Q♥", 60, 84, hl=True)
    s.text(570, 195, "คนดูคิดว่านี่คือใบบนสุด", 12, "middle", 400, MUTE)
    s.rect(30, 230, 700, 76, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 254, "คว่ำกลับทั้งก้อน → คนดูเชื่อว่าใบบนสุดคือ B  แต่ความจริงใบบนสุดคือ A", 14, "middle", 700, GREEN)
    s.text(380, 276, "(พลิกก้อน 2 ใบขึ้น → เห็น B  ·  คว่ำลง → A กลับขึ้นบน, B ซ่อนใต้ A)", 13, "middle")
    s.text(380, 296, "จุดตายคือ 'สองใบเหลื่อมกัน' → ฝึกให้ขอบเรียบสนิท", 12, "middle", 400, MUTE)
    s.save("double-lift.svg")


def hindu_force():
    s = Svg(760, 320, "Hindu Shuffle Force: ใบ F อยู่ล่างสุด คนดูสั่ง 'หยุด' เมื่อไรก็ได้")
    s.step(40, 62, 1); s.text(62, 67, "มือขวาถือสำรับ", 13, "start", 600)
    stack(s, 40, 90, ["?", "?", "…", "?", "F"], (4,), w=110)
    s.text(95, 232, "F อยู่ล่างสุด", 12, "middle", 700, GREEN)
    s.step(230, 62, 2); s.text(252, 67, "มือซ้ายดึงกองเล็กออกจากด้านบน", 13, "start", 600)
    stack(s, 230, 90, ["?", "?"], (), w=80); s.text(270, 160, "มือซ้าย (กองที่ดึง)", 11, "middle", 400, MUTE)
    stack(s, 330, 90, ["?", "…", "F"], (2,), w=80); s.text(370, 188, "มือขวา", 11, "middle", 400, MUTE)
    s.text(300, 240, "ดึงต่อเรื่อย ๆ ด้วยจังหวะสม่ำเสมอ", 12, "middle", 400, MUTE)
    s.step(460, 62, 3); s.text(482, 67, "คนดูพูด 'หยุด'", 13, "start", 600)
    s.text(580, 95, "หยุดทันที ยกกองที่เหลือในมือขวา", 12, "middle", 400, MUTE)
    s.text(580, 112, "ขึ้นมาเปิดหน้า 'ใบล่างสุด'", 12, "middle", 400, MUTE)
    s.card(550, 128, "F", 60, 84, hl=True)
    s.text(580, 232, "= ใบที่ 'ตัดสินใจเอง'", 12, "middle", 700, GREEN)
    s.rect(30, 262, 700, 40, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 287, "กุญแจ: ไพ่ล่างสุดไม่ถูกดึงออกเลย จึงอยู่ใน 'มือขวา' จนวินาทีสุดท้าย", 13, "middle", 700, GREEN)
    s.save("hindu-force.svg")


def riffle():
    s = Svg(760, 330, "Riffle Shuffle & Bridge: สับแบบไพ่สลับ แล้วดัดสะพาน")
    s.step(40, 62, 1); s.text(62, 67, "แบ่งครึ่ง", 13, "start", 600)
    stack(s, 40, 90, ["A", "A", "A"], w=80); stack(s, 140, 90, ["B", "B", "B"], w=80)
    s.line(230, 118, 270, 118, arrow=True)
    s.step(285, 62, 2); s.text(307, 67, "ปล่อยสลับนิ้วโป้ง", 13, "start", 600)
    stack(s, 290, 90, ["A", "B", "A", "B", "B", "A"], w=90, gap=26)
    s.line(395, 118, 435, 118, arrow=True)
    s.step(450, 62, 3); s.text(472, 67, "ดัดสะพาน (Bridge)", 13, "start", 600)
    s.parts.append('<path d="M455,170 Q515,90 575,170" fill="none" stroke="#2f4b8f" stroke-width="10" stroke-linecap="round"/>')
    s.parts.append('<path d="M455,170 Q515,90 575,170" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>')
    s.text(515, 200, "ใช้นิ้วโป้งงอ 2 ครึ่งขึ้น แล้วดันเข้าหากัน", 12, "middle", 400, MUTE)
    s.text(515, 218, "เสียงซ่าให้ไพ่ลงมาต่อกันเอง", 12, "middle", 400, MUTE)
    s.rect(30, 256, 700, 56, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 280, "ฝึกให้ 'ใบล่างสุด / บนสุด' อยู่ที่เดิมได้ เพื่อใช้ควบคุมไพ่ (ปล่อยใบแรกจากกองใดก็ได้ตามต้องการ)", 13, "middle", 700, GREEN)
    s.text(380, 300, "เริ่มจากสับช้า ๆ  ปล่อยทีละ 1–2 ใบ  แล้วค่อยเร่งความเร็ว", 12, "middle", 400)
    s.save("riffle-bridge.svg")


def classic_pass():
    s = Svg(760, 330, "Classic Pass: สลับครึ่งบน–ล่างในพริบตา → ไพ่ที่เลือกขึ้นมาอยู่บนสุด")
    s.step(40, 62, 1); s.text(62, 67, "มี 'รอยแยก' ด้วยนิ้วก้อย", 13, "start", 600)
    s.rect(40, 92, 110, 36, "#e8eefc", "#6b7280", 1.5, 6); s.text(95, 115, "ครึ่งบน U", 12, "middle", 700)
    s.line(36, 134, 154, 134, RED, 3, dash="6 4")
    s.text(95, 150, "รอยแยก (นิ้วก้อย)", 11, "middle", 700, RED)
    s.rect(40, 158, 110, 30, "#fff3cd", GOLD, 2.5, 6); s.text(95, 178, "ไพ่ที่เลือก", 12, "middle", 700)
    s.rect(40, 188, 110, 36, "#e8eefc", "#6b7280", 1.5, 6); s.text(95, 211, "ครึ่งล่าง L", 12, "middle", 700)
    s.line(170, 150, 235, 150, arrow=True)
    s.step(255, 62, 2); s.text(277, 67, "มือขวาปิดบัง สลับครึ่ง", 13, "start", 600)
    s.rect(255, 92, 100, 36, "#e8eefc", "#6b7280", 1.5, 6); s.text(305, 115, "U", 12, "middle", 700)
    s.rect(385, 150, 100, 60, "#fff3cd", GOLD, 2.5, 6); s.text(435, 185, "L + ไพ่ที่เลือก", 12, "middle", 700)
    s.parts.append('<path d="M360,112 C410,112 400,140 385,160" fill="none" stroke="#6b7280" stroke-width="2.5" marker-end="url(#ar)"/>')
    s.parts.append('<path d="M385,200 C320,215 270,190 290,138" fill="none" stroke="#6b7280" stroke-width="2.5" marker-end="url(#ar)" stroke-dasharray="5 4"/>')
    s.text(370, 240, "L ถูกยกขึ้นไปบนสุด  ·  U ลงไปล่าง", 12, "middle", 400, MUTE)
    s.line(505, 150, 565, 150, arrow=True)
    s.step(590, 62, 3); s.text(612, 67, "ผลลัพธ์", 13, "start", 600)
    s.rect(590, 92, 110, 30, "#fff3cd", GOLD, 2.5, 6); s.text(645, 112, "ไพ่ที่เลือก (บนสุด)", 11, "middle", 700)
    s.rect(590, 122, 110, 36, "#e8eefc", "#6b7280", 1.5, 6); s.text(645, 145, "ครึ่งล่าง L", 12, "middle", 700)
    s.rect(590, 158, 110, 36, "#e8eefc", "#6b7280", 1.5, 6); s.text(645, 181, "ครึ่งบน U", 12, "middle", 700)
    s.rect(30, 262, 700, 54, "#fef2f2", RED, 1.5, 10)
    s.text(380, 284, "ทำตอน 'มีจังหวะบังสายตา' เช่น คนดูกำลังมองหน้าคุณ หรือคุณพลิกมือเปลี่ยนเรื่อง", 13, "middle", 700, RED)
    s.text(380, 304, "ฝึกกับสำรับเก่าช้า ๆ ก่อนค่อยเร็ว · ต้องเงียบที่สุด", 12, "middle", 400)
    s.save("classic-pass.svg")


def palm():
    s = Svg(760, 320, "Top-Card Palm: ซ่อนไพ่ 1 ใบไว้ในอุ้งมือ")
    s.text(200, 62, "มองด้านหลังมือ", 13, "middle", 600)
    s.parts.append('<path d="M110,240 C95,160 110,110 150,92 C170,82 190,92 190,115 L190,95 C190,80 215,80 215,100 L215,115 C215,80 245,82 245,105 L245,125 C245,100 275,105 275,130 L275,170 C285,215 270,250 240,262 L150,262 Z" fill="#f5d5b8" stroke="#a16207" stroke-width="2"/>')
    s.text(200, 292, "สำรับอยู่ใต้ฝ่ามือ นิ้วงอเล็กน้อยเป็นธรรมชาติ", 11, "middle", 400, MUTE)
    s.text(550, 62, "มองด้านฝ่ามือ", 13, "middle", 600)
    s.parts.append('<path d="M450,240 C435,170 450,120 490,102 C510,92 530,102 530,125 L530,105 C530,90 555,90 555,110 L555,125 C555,90 585,92 585,115 L585,135 C585,110 615,115 615,140 L615,180 C625,225 610,250 580,262 L490,262 Z" fill="#f5d5b8" stroke="#a16207" stroke-width="2"/>')
    s.parts.append('<rect x="480" y="150" width="90" height="60" rx="5" fill="#fff" stroke="#6b7280" stroke-width="2" transform="rotate(-18 525 180)"/>')
    s.text(525, 186, "ไพ่", 14, "middle", 700)
    s.circle(488, 190, 6, RED); s.text(442, 188, "①", 13, "end", 700, RED)
    s.circle(566, 160, 6, RED); s.text(578, 156, "②", 13, "start", 700, RED)
    s.text(550, 292, "① โคนนิ้วหัวแม่มือ  ② ข้อนิ้วนางกับนิ้วก้อย  — ไพ่ถูกหนีบเฉียง", 11, "middle", 400, MUTE)
    s.rect(30, 218, 190, 70, "#ecfdf5", GREEN, 1.5, 10) if False else None
    s.save("palm.svg")


def faro_physical():
    s = Svg(760, 330, "Faro Shuffle (ลงมือจริง): สอดไพ่สองครึ่งให้สลับกันทีละใบ")
    s.step(40, 62, 1); s.text(62, 67, "แบ่งครึ่ง 26 + 26 ถือมุมแนบกัน", 13, "start", 600)
    s.parts.append('<g transform="rotate(-8 130 140)"><rect x="40" y="110" width="110" height="70" rx="6" fill="#2f4b8f" stroke="#1e2f5c"/></g>')
    s.parts.append('<g transform="rotate(8 230 140)"><rect x="170" y="110" width="110" height="70" rx="6" fill="#2f4b8f" stroke="#1e2f5c"/></g>')
    s.text(95, 210, "มือซ้าย", 12, "middle", 400, MUTE); s.text(225, 210, "มือขวา", 12, "middle", 400, MUTE)
    s.text(160, 235, "นิ้วโป้งยกมุมด้านใน", 12, "middle", 400, MUTE)
    s.line(300, 145, 360, 145, arrow=True)
    s.step(380, 62, 2); s.text(402, 67, "ดันเข้าหากัน ให้มุมไพ่ซ้อน", 13, "start", 600)
    for i in range(8):
        y = 100 + i * 10
        s.rect(380 + (0 if i % 2 == 0 else 20), y, 110, 8, "#2f4b8f" if i % 2 == 0 else "#4f6fb5", "#1e2f5c", 1, 2)
    s.text(450, 200, "ไพ่สองกองสอดสลับทีละใบ", 12, "middle", 400, MUTE)
    s.line(510, 145, 570, 145, arrow=True)
    s.step(590, 62, 3); s.text(612, 67, "ผลลัพธ์", 13, "start", 600)
    for i in range(8):
        s.rect(590, 100 + i * 10, 120, 8, "#2f4b8f" if i % 2 == 0 else "#4f6fb5", "#1e2f5c", 1, 2)
    s.text(650, 210, "สลับสนิททีละใบ: ใบบนสุดอยู่ที่เดิม = Out", 11, "middle", 400, MUTE)
    s.text(650, 228, "ใบบนสุดลงมาเป็นใบที่ 2 = In", 11, "middle", 400, MUTE)
    s.rect(30, 252, 700, 56, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 276, "ถ้าตัดได้ 26/26 พอดีแล้วสอดสลับสมบูรณ์ จะนำสูตรในหน้า Faro (คณิต) ไปใช้ได้ทันที", 13, "middle", 700, GREEN)
    s.text(380, 296, "ฝึกกับสำรับใหม่ ๆ เพราะต้องการขอบไพ่คม  ใช้เวลาฝึกหลายสัปดาห์", 12, "middle", 400)
    s.save("faro-physical.svg")


# ---------------------------------------------------------------- เพิ่มเติม: ไพ่คำนวณ
from verify_tricks import (spelling_arrangement, kval, kruskal_final, binary_cards, monge)


def spelling():
    arr = spelling_arrangement()
    s = Svg(760, 330, "ไพ่สะกดชื่อ: สะกด O-N-E แล้วไพ่ที่เปิดคือ A, T-W-O → 2 …")
    s.text(30, 62, "① จัดไพ่ 10 ใบ (บน → ล่าง) ล่วงหน้า  (A = 1)", 14, "start", 600)
    for i, n in enumerate(arr):
        s.strip(30 + i * 70, 76, "A♠" if n == 1 else f"{n}♠", 62, 34)
        s.text(61 + i * 70, 128, f"ใบที่ {i+1}", 10, "middle", 400, MUTE)
    s.text(30, 160, "② สะกด ONE: ย้ายไพ่จาก 'บน → ล่าง' ทีละใบ ตามจำนวนตัวอักษร (3 ตัว = 3 ใบ)", 14, "start", 600)
    q = arr[:]
    row = lambda y, cards, hl=None, lab="": ([s.strip(30 + i * 70, y, "A♠" if n == 1 else f"{n}♠", 62, 30, hl=(n == hl)) for i, n in enumerate(cards)], s.text(30, y - 6, lab, 11, "start", 400, MUTE))
    row(182, q, None, "ก่อนสะกด")
    for _ in "ONE": q.append(q.pop(0))
    row(238, q, 1, "หลังย้าย 3 ใบ → ใบบนสุดคือ A  (เปิดทิ้งออกไป แล้วสะกดคำต่อไป)")
    s.rect(30, 282, 700, 36, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 305, "ทำซ้ำ: TWO(3) → 2, THREE(5) → 3 … TEN(3) → 10 (ตรวจด้วยโค้ดแล้ว)", 13, "middle", 700, GREEN)
    s.save("spelling.svg")


def four_aces_deal():
    s = Svg(760, 330, "เอซ 4 ใบจากการแจก 4 กอง: เอซอยู่ 4 ใบล่างสุด (ใบที่ 49–52)")
    s.text(30, 62, "① สำรับ 52 ใบ: เอซ 4 ใบอยู่ล่างสุด", 14, "start", 600)
    for i in range(6):
        s.strip(30 + i * 40, 76, "?", 36, 26)
    s.text(30 + 6 * 40 + 6, 94, "…", 16, "start", 700)
    for i, c in enumerate(["A♠", "A♥", "A♦", "A♣"]):
        s.strip(300 + i * 52, 76, c, 48, 26, hl=True)
    s.text(300, 122, "ใบที่ 49 50 51 52", 11, "start", 400, MUTE)
    s.text(30, 156, "② แจกหงายหน้า/คว่ำหน้าทีละใบ วนซ้าย→ขวา 4 กอง จนหมดสำรับ (กองละ 13 ใบ)", 14, "start", 600)
    for p in range(4):
        x = 90 + p * 160
        s.text(x + 48, 182, f"กอง {p+1}", 12, "middle", 600, MUTE)
        for k, lab in enumerate(["?", "?", "…"]):
            s.strip(x, 190 + k * 20, lab, 96, 18)
        s.strip(x, 250, ["A♠", "A♥", "A♦", "A♣"][p], 96, 26, hl=True)
    s.text(380, 300, "ใบสุดท้ายที่แจกของแต่ละกอง (บนสุด) = เอซ ครบ 4 กอง", 13, "middle", 700, GREEN)
    s.text(380, 320, "ต้องแจกครบทั้ง 52 ใบ และสำรับห้ามถูกตัดก่อนแจก", 12, "middle", 400, MUTE)
    s.save("four-aces-deal.svg")


def parity():
    s = Svg(760, 360, "ทายด้านไพ่ด้วยหลักคู่–คี่ (Parity): พลิกคู่ ๆ จำนวนหงายยังเป็นเลขคู่เสมอ")
    up = [1, 0, 1, 1, 0, 0, 1, 0, 0, 0]
    def row(y, ups, hide=None, title=""):
        s.text(30, y - 8, title, 13, "start", 600)
        for i, u in enumerate(ups):
            x = 30 + i * 70
            if i == hide:
                s.rect(x, y, 56, 70, "#e5e7eb", "#6b7280", 1.5, 6); s.text(x + 28, y + 42, "ปิดไว้", 12, "middle", 700, MUTE)
            elif u:
                s.rect(x, y, 56, 70, PAPER, "#6b7280", 1.5, 6); s.text(x + 28, y + 43, "หงาย", 12, "middle", 700)
            else:
                s.card(x, y, None, 56, 70, back=True)
    row(80, up, None, "① เริ่มต้น: หงาย 4 ใบ (เลขคู่) — ผู้ชมพลิกไพ่ 'ทีละ 2 ใบ' กี่ครั้งก็ได้ (ผมไม่มอง)")
    up2 = [1, 0, 1, 1, 0, 0, 1, 0, 0, 0]
    row(200, up2, hide=2, title="② ผู้ชมเอามือปิดไพ่ 1 ใบ (ใบที่ 3)  → ผมนับหงายที่เห็น = 3 ใบ (คี่)")
    s.rect(30, 290, 700, 56, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 314, "หงายที่เห็นเป็นเลขคี่ → ใบที่ปิดอยู่ต้อง 'หงาย' (ให้รวมเป็นเลขคู่)", 14, "middle", 700, GREEN)
    s.text(380, 334, "หงายที่เห็นเป็นเลขคู่ → ใบที่ปิดอยู่ 'คว่ำ'", 13, "middle", 400)
    s.save("parity.svg")


def kruskal():
    # หาสำรับตัวอย่างที่เส้นทางจากใบที่ 1 กับใบที่ 3 ไปบรรจบกันภายใน 24 ใบแรก
    rnd = random.Random(11)
    base = [r for r in range(1, 14) for _ in range(4)]
    while True:
        d = base[:]; rnd.shuffle(d)
        def path(st):
            i, ps = st, [st]
            while i + kval(d[i]) < len(d): i += kval(d[i]); ps.append(i)
            return ps
        pa, pb = path(0), path(2)
        com = [i for i in pa if i in pb]
        if com and com[0] < 24 and kruskal_final(d, 0) == kruskal_final(d, 2):
            break
    s = Svg(760, 330, "Kruskal Count: เริ่มต่างกัน แต่เส้นทางมักไปบรรจบกัน")
    face = lambda r: {1: "A", 11: "J", 12: "Q", 13: "K"}.get(r, str(r))
    for i in range(24):
        x, y = 22 + (i % 12) * 60, 60 + (i // 12) * 90
        inA, inB = i in pa, i in pb
        col = GOLD if (inA and inB) else (BLUE if inA else (GREEN if inB else "#9ca3af"))
        s.rect(x, y, 52, 66, "#fff7ed" if col == GOLD else PAPER, col, 3.2 if col != "#9ca3af" else 1.2, 6)
        s.text(x + 26, y + 40, face(d[i]), 20, "middle", 700)
        s.text(x + 26, y + 60, f"#{i+1}", 10, "middle", 400, MUTE)
    s.text(30, 252, "● น้ำเงิน = เส้นทางเริ่มที่ใบ #1   ● เขียว = เริ่มที่ใบ #3   ● ทอง = ตกใบเดียวกัน (เดินต่อไปด้วยกันเสมอ)", 12, "start", 600)
    s.text(30, 274, "นับตามค่าไพ่: A=1 … 10=10, J Q K = 5  → ไปหยุดที่ใบสุดท้ายที่นับต่อไม่ได้อีก", 12, "start", 400, MUTE)
    s.rect(30, 288, 700, 30, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 308, "จำลอง 20,000 สำรับ: เริ่ม #1 กับจุดเริ่มใด ๆ ใน 10 ใบแรก ได้ใบสุดท้ายเดียวกัน ≈ 85%", 13, "middle", 700, GREEN)
    s.save("kruskal.svg")


def binary_cards_img():
    cards = binary_cards()
    s = Svg(760, 440, "Binary Cards: ไพ่ตัวเลข 6 ใบ ทายเลข 1–63 ที่ผู้ชมคิดไว้")
    for b, nums in enumerate(cards):
        ox, oy = 18 + (b % 3) * 245, 52 + (b // 3) * 190
        s.rect(ox, oy, 230, 176, PAPER, "#6b7280", 1.5, 8)
        s.text(ox + 115, oy + 18, f"ใบที่ {b+1}  (เลขแรก = {1 << b})", 12, "middle", 700, BLUE)
        for k, n in enumerate(nums):
            cx, cy = ox + 14 + (k % 8) * 26.5, oy + 38 + (k // 8) * 33
            hl = n == 37
            if hl: s.rect(cx - 3, cy - 14, 24, 20, "#fff3cd", GOLD, 2, 4)
            s.text(cx + 9, cy, n, 12, "middle", 700 if hl else 400)
    s.text(380, 428, "ตัวอย่าง: 37 อยู่ในใบ 1, 3, 6  →  1 + 4 + 32 = 37", 14, "middle", 700, GREEN)
    s.save("binary-cards.svg")


def gilbreath_suit():
    random.seed(3)
    suits = "♣♥♠♦"
    deck = [i % 4 for i in range(12)]
    n = 5
    table, hand = list(reversed(deck[:n])), deck[n:]
    a, b, merged = table[:], hand[:], []
    while a or b:
        if a and (not b or random.random() < .5): merged.append(a.pop(0))
        else: merged.append(b.pop(0))
    for i in range(0, 12, 4): assert sorted(merged[i:i + 4]) == [0, 1, 2, 3]
    s = Svg(760, 470, "Gilbreath หลักการที่ 2: จัดดอกวน ♣♥♠♦ → ทุกกลุ่ม 4 ใบมีครบ 4 ดอก")
    def col(x, y, seq, title, groups=False):
        s.text(x + 30, y - 12, title, 12, "middle", 600)
        for i, c in enumerate(seq):
            s.strip(x, y + i * 28, suits[c], 60, 24, color=RED if c in (1, 3) else INK)
        if groups:
            for k in range(0, len(seq), 4):
                s.parts.append(f'<path d="M{x+68},{y+k*28} q10,0 10,10 v76 q0,10 -10,10" fill="none" stroke="{GREEN}" stroke-width="2.5"/>')
                s.text(x + 90, y + k * 28 + 60, "ครบ 4 ดอก", 12, "start", 700, GREEN)
    col(40, 80, deck, "① จัดดอกวน")
    s.line(115, 200, 190, 200, arrow=True); s.text(152, 182, "แจก 5 ใบ", 11, "middle", 400, MUTE)
    col(205, 80, table, "② กองโต๊ะ (กลับ)")
    col(305, 80, hand, "ในมือ (7)")
    s.line(385, 200, 455, 200, arrow=True); s.text(420, 182, "ริฟเฟิล", 11, "middle", 400, MUTE)
    col(470, 80, merged, "③ หลังริฟเฟิล", True)
    s.text(380, 452, "ใช้ได้กับทุกจำนวนที่แจกออก (ตรวจ 0–52 ใบ × 100 รูปแบบ) · ดอกที่ใช้แทนสีได้ · ริฟเฟิลแค่ 1 ครั้ง", 12, "middle", 600, GREEN)
    s.save("gilbreath-suit.svg")


MNEMONICA = "4♣ 2♥ 7♦ 3♣ 4♥ 6♦ A♠ 5♥ 9♠ 2♠ Q♥ 3♦ Q♣ 8♥ 6♠ 5♠ 9♥ K♣ 2♦ J♥ 3♠ 8♠ 6♥ 10♣ 5♦ K♦ 2♣ 3♥ 8♦ 5♣ K♠ J♦ 8♣ 10♠ K♥ J♣ 7♠ 10♥ A♦ 4♠ 7♥ 4♦ A♣ 9♣ J♠ Q♦ 7♣ Q♠ 10♦ 6♣ A♥ 9♦".split()


def mnemonica():
    assert len(set(MNEMONICA)) == 52
    s = Svg(760, 330, "Mnemonica Stack (Juan Tamariz): 52 ใบเรียงบน → ล่าง")
    for i, c in enumerate(MNEMONICA):
        x, y = 16 + (i % 13) * 56.5, 52 + (i // 13) * 64
        s.rect(x, y, 52, 56, PAPER, "#9ca3af", 1.2, 5)
        s.text(x + 5, y + 14, i + 1, 10, "start", 400, MUTE)
        s.text(x + 26, y + 40, c, 17, "middle", 700, RED if c[-1] in "♥♦" else INK)
    s.text(380, 318, "อ่านจากซ้ายไปขวา แถวบนไปล่าง (ใบที่ 1 = 4♣ … ใบที่ 52 = 9♦)", 13, "middle", 600, MUTE)
    s.save("mnemonica.svg")


def monge_img():
    s = Svg(760, 360, "Monge's Shuffle: ไพ่ใบที่ 1 วางก่อน ใบถัดไปสลับ 'วางทับ / วางใต้'")
    d = list(range(1, 11)); t = []; steps = []
    for i, c in enumerate(d):
        t = [c] + t if i % 2 else t + [c]; steps.append(t[:])
    s.text(30, 60, "ตัวอย่าง 10 ใบ — สถานะกองใหม่หลังวางแต่ละใบ", 13, "start", 600)
    for k in (1, 2, 3, 4, 5):
        x = 30 + (k - 1) * 140
        s.text(x, 84, f"วางใบ {k} " + ("" if k == 1 else ("ทับ" if k % 2 == 0 else "ใต้")), 12, "start", 700, BLUE)
        for r, c in enumerate(steps[k - 1]):
            s.strip(x, 94 + r * 26, c, 70, 22, hl=(c == k))
    s.text(30, 242, "ผลสุดท้าย (บน → ล่าง) — ใบคู่เรียงย้อนกลับก่อน แล้วตามด้วยใบคี่เรียงปกติ:", 13, "start", 600)
    fin = steps[-1]
    for i, c in enumerate(fin):
        s.strip(30 + i * 70, 252, c, 62, 26)
    s.rect(30, 296, 700, 50, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 318, "สำรับ 52 ใบ: ใบคี่ i → ตำแหน่ง 26 + (i+1)/2   ·   ใบคู่ i → ตำแหน่ง 27 − i/2", 13, "middle", 700, GREEN)
    s.text(380, 337, "ทำซ้ำ 12 รอบ สำรับ 52 ใบกลับเป็นลำดับเดิมพอดี (ตรวจด้วยโค้ดแล้ว)", 12, "middle", 400)
    s.save("monge.svg")


def fitch_flow():
    s = Svg(760, 300, "Fitch–Cheney ถอดรหัสเร็ว: 3 ขั้นตอนใน 5 วินาที")
    boxes = [("① ใบแรก", "ดู 'ดอก' → ดอกของใบซ่อน\nจำ 'เลข' เป็นจุดเริ่ม", BLUE),
             ("② ใบที่เหลือ 3 ใบ", "เรียงเล็ก–กลาง–ใหญ่\n→ อ่านรหัส d (1–6)", GOLD),
             ("③ บวก", "ใบซ่อน = เลขใบแรก + d\n(เกิน K ให้วนกลับ A)", GREEN)]
    for i, (h, b, c) in enumerate(boxes):
        x = 30 + i * 240
        s.rect(x, 60, 220, 120, PAPER, c, 3, 12)
        s.text(x + 110, 90, h, 16, "middle", 700, c)
        for k, ln in enumerate(b.split("\n")): s.text(x + 110, 124 + k * 24, ln, 13, "middle", 400)
        if i < 2: s.line(x + 224, 120, x + 236, 120, MUTE, 2, arrow=True)
    s.rect(30, 204, 700, 74, "#eff6ff", BLUE, 1.2, 10)
    s.text(380, 230, "เทคนิคช่วยจำ: d = ตำแหน่งในลิสต์ SML, SLM, MSL, MLS, LSM, LMS", 13, "middle", 700)
    s.text(380, 252, "เล็ก–กลาง–ใหญ่ ใช้ A<2<…<K ก่อน ถ้าเลขเท่ากันใช้ ♣<♦<♥<♠", 13, "middle")
    s.text(380, 270, "กฎนี้ตรวจแล้วครบทุก 2,598,960 มือ", 12, "middle", 700, GREEN)
    s.save("fitch-flow.svg")


# ---------------------------------------------------------------- ชุดที่ 2 (ง่าย/กลาง/ยาก อย่างละ 5)
from verify_tricks import digits_of, josephus_top


def box(s, x, y, w, h, title, lines, color=BLUE):
    s.rect(x, y, w, h, PAPER, color, 2.5, 10)
    s.text(x + w / 2, y + 24, title, 14, "middle", 700, color)
    for i, ln in enumerate(lines):
        s.text(x + w / 2, y + 50 + i * 22, ln, 13, "middle", 400 if i else 600)


def missing_card():
    s = Svg(760, 300, "ไพ่ที่หายไป (Missing Card): A–K ดอกเดียวกัน รวมกัน = 91")
    names = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    for i, n in enumerate(names):
        x = 22 + i * 56
        if n == "6":
            s.rect(x, 60, 50, 70, "#fff3cd", RED, 2.5, 6, 'stroke-dasharray="6 4"')
            s.text(x + 25, 102, "?", 26, "middle", 700, RED)
        else:
            s.card(x, 60, n + "♠", 50, 70)
    s.text(30, 156, "① ผู้ชมแอบหยิบไพ่ 1 ใบ (ที่ซ่อน)   ·   ทั้งชุดรวม 1+2+…+13 = 91", 14, "start", 600)
    s.text(30, 182, "② บวกค่าไพ่ที่เหลือบนโต๊ะ (A=1, J=11, Q=12, K=13) = 85", 14, "start", 600)
    s.rect(30, 214, 700, 62, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 240, "ไพ่ที่หาย = 91 − 85 = 6", 20, "middle", 700, GREEN)
    s.text(380, 264, "ฝึกบวกเป็นคู่ที่รวม 13 (A+Q, 2+J, 3+10, 4+9, 5+8, 6+7) จะไวขึ้นมาก", 12, "middle", 400, MUTE)
    s.save("missing-card.svg")


def secret_number():
    s = Svg(760, 340, "เลขลับจากไพ่: ผู้ชมคำนวณเงียบ ๆ คุณบอกไพ่ได้จากผลลัพธ์")
    steps = [("เลือกไพ่ 1 ใบ", "7♥ (ค่า 7)"), ("× 2", "14"), ("+ 3", "17"), ("× 5", "85"), ("+ เลขดอก (♥ = 3)", "88")]
    for i, (a, b) in enumerate(steps):
        x = 24 + i * 146
        s.rect(x, 56, 136, 70, PAPER, BLUE, 2, 10)
        s.text(x + 68, 82, a, 12, "middle", 600)
        s.text(x + 68, 110, b, 18, "middle", 700, BLUE)
        if i < 4: s.line(x + 138, 91, x + 146, 91, MUTE, 2, arrow=True)
    s.text(30, 156, "ผู้ชมบอกผลลัพธ์สุดท้าย = 88", 15, "start", 700)
    s.rect(30, 172, 700, 52, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 196, "คุณลบ 15 → 88 − 15 = 73   →   หลักสิบ = ค่าไพ่ (7)   หลักหน่วย = เลขดอก (3 = ♥)", 14, "middle", 700, GREEN)
    s.text(380, 214, "ได้ 7♥", 14, "middle", 700, GREEN)
    s.text(30, 252, "เลขดอก:", 14, "start", 700)
    for i, (n, c) in enumerate([("1", "♣"), ("2", "♦"), ("3", "♥"), ("4", "♠")]):
        s.rect(120 + i * 110, 234, 100, 28, PAPER, "#9ca3af", 1.2, 6)
        s.text(170 + i * 110, 254, f"{c} = {n}", 15, "middle", 700, RED if c in "♥♦" else INK)
    s.text(380, 296, "สูตร: ((ค่า × 2) + 3) × 5 + ดอก = 10 × ค่า + 15 + ดอก  (J Q K ใช้ 11, 12, 13 ก็ได้ ผลสิบหลักเป็น 11–13)", 12, "middle", 400, MUTE)
    s.text(380, 316, "ตรวจครบทุกค่า A–10 × 4 ดอกแล้ว", 12, "middle", 700, GREEN)
    s.save("secret-number.svg")


def alt_color_deal():
    s = Svg(760, 340, "แยกสีด้วยการแจกสลับ: สำรับสลับ แดง–ดำ แล้วแจกเป็น 2 กอง")
    deck = ["R", "B"] * 4
    cut = 3
    d2 = deck[cut:] + deck[:cut]
    def col(x, y, seq, title, cut_at=None):
        s.text(x + 30, y - 10, title, 12, "middle", 600)
        for i, c in enumerate(seq):
            s.rect(x, y + i * 24, 60, 20, "#fecaca" if c == "R" else "#d1d5db", "#6b7280", 1.2, 4)
            s.text(x + 30, y + i * 24 + 15, "แดง" if c == "R" else "ดำ", 12, "middle", 700, RED if c == "R" else INK)
        if cut_at:
            s.line(x - 6, y + cut_at * 24 - 2, x + 66, y + cut_at * 24 - 2, RED, 3, dash="6 4")
    col(40, 70, deck, "① จัดสลับ (8 ใบตัวอย่าง)", cut)
    s.text(135, 130, "ผู้ชมตัด", 12, "start", 700, RED); s.text(135, 148, "ตรงไหนก็ได้", 12, "start", 700, RED)
    s.line(220, 200, 270, 200, arrow=True)
    col(285, 70, d2, "② หลังตัดยังสลับสีอยู่")
    s.line(360, 200, 410, 200, arrow=True)
    s.text(500, 80, "③ แจกสลับ ไปกอง A / กอง B", 12, "middle", 600)
    for p, lab in enumerate(["กอง A", "กอง B"]):
        x = 420 + p * 150
        s.text(x + 30, 104, lab, 12, "middle", 600, MUTE)
        for i, c in enumerate(d2[p::2]):
            s.rect(x, 112 + i * 24, 60, 20, "#fecaca" if c == "R" else "#d1d5db", "#6b7280", 1.2, 4)
            s.text(x + 30, 112 + i * 24 + 15, "แดง" if c == "R" else "ดำ", 12, "middle", 700, RED if c == "R" else INK)
    s.rect(30, 280, 700, 44, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 308, "กอง A = แดงล้วน, กอง B = ดำล้วน  (สำรับ 52 ใบ ตัดกี่ครั้งก็ได้ แต่ห้ามสับ)", 14, "middle", 700, GREEN)
    s.save("alt-color-deal.svg")


def color_balance():
    s = Svg(760, 330, "สมดุลสี: แจกครึ่งสำรับ → แดงในกอง A = ดำในกอง B เสมอ")
    for k, (lab, red, blk) in enumerate([("กอง A (26 ใบ)", 15, 11), ("กอง B (26 ใบ)", 11, 15)]):
        x = 60 + k * 340
        s.text(x + 130, 66, lab, 14, "middle", 700)
        s.rect(x, 80, 260 * red / 26, 40, "#fecaca", RED, 1.5, 4); s.text(x + 130 * red / 26, 106, f"แดง {red}", 14, "middle", 700, RED)
        s.rect(x + 260 * red / 26, 80, 260 * blk / 26, 40, "#d1d5db", INK, 1.5, 4); s.text(x + 260 * red / 26 + 130 * blk / 26, 106, f"ดำ {blk}", 14, "middle", 700)
    s.text(130, 156, "แดง 15", 20, "middle", 700, RED); s.text(470, 156, "ดำ 15", 20, "middle", 700)
    s.text(300, 156, "=", 22, "middle", 700, GREEN)
    s.rect(30, 190, 700, 110, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 218, "ทำไม? ทั้งสำรับมีแดง 26 ใบ", 14, "middle", 700, GREEN)
    s.text(380, 244, "แดงที่ไม่ได้อยู่กอง A ต้องอยู่กอง B  →  แดงกอง B = 26 − แดงกอง A", 13, "middle")
    s.text(380, 268, "และกอง B มี 26 ใบ  →  ดำกอง B = 26 − แดงกอง B = แดงกอง A", 13, "middle")
    s.text(380, 290, "(ตัวเลขในภาพเป็นตัวอย่าง: ผลจริงจะเป็นเท่าไรก็ได้ แต่สองค่านี้เท่ากันเสมอ)", 11, "middle", 400, MUTE)
    s.save("color-balance.svg")


def magic_square():
    s = Svg(760, 340, "สี่เหลี่ยมมหัศจรรย์ 3×3: ไพ่ A–9 เรียงให้ทุกแถว/สดมภ์/แนวทแยง = 15")
    sq = [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
    for r in range(3):
        for c in range(3):
            n = sq[r][c]
            s.card(60 + c * 70, 56 + r * 86, ("A" if n == 1 else str(n)) + "♠", 60, 76, hl=(r == 1 and c == 1))
    for r in range(3):
        s.text(280, 100 + r * 86, "= 15", 16, "start", 700, GREEN)
    for c in range(3):
        s.text(90 + c * 70, 326, "= 15", 13, "middle", 700, GREEN)
    s.text(300, 96, "", 12)
    box(s, 380, 56, 340, 120, "วิธีเล่น", ["ท่องตำแหน่งไว้ แล้ววางไพ่ 9 ใบให้ผู้ชมดู", "หมุน/กลับด้านได้รวม 8 แบบ (ยังรวม 15 เหมือนเดิม)", "ใบกลางต้องเป็น 5 เสมอ"], BLUE)
    box(s, 380, 192, 340, 100, "จำง่าย", ["มุมทั้ง 4 = เลขคู่ (2 4 6 8)", "ขอบ = เลขคี่ (1 3 7 9), กลาง = 5"], GOLD)
    s.save("magic-square.svg")


def reverse_1089():
    s = Svg(760, 340, "เลข 1089 ด้วยไพ่ 3 ใบ: ผลลัพธ์ 1089 เสมอ")
    steps = [("① ไพ่ 3 ใบ เรียงเป็นเลข", "7  3  2  →  732", "(ไพ่ใบแรกกับใบสุดท้ายต้องต่างกัน; A=1…9)"),
             ("② กลับด้านเป็น", "237", ""),
             ("③ ลบ (ใหญ่ − เล็ก)", "732 − 237 = 495", "ถ้าได้ 2 หลัก ให้เติม 0 หน้า เช่น 099"),
             ("④ กลับด้านผลลบ แล้วบวก", "495 + 594 = 1089", "")]
    for i, (a, b, c) in enumerate(steps):
        x, y = 30 + (i % 2) * 360, 56 + (i // 2) * 120
        s.rect(x, y, 340, 104, PAPER, BLUE, 2, 10)
        s.text(x + 170, y + 26, a, 13, "middle", 700, BLUE)
        s.text(x + 170, y + 62, b, 20, "middle", 700)
        s.text(x + 170, y + 88, c, 11, "middle", 400, MUTE)
    s.rect(30, 300, 700, 30, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 321, "เพิ่มลูกเล่น: ให้บอกแค่ 'หลักร้อย' ของผลลบ (4) → คุณรู้ทั้งหมด 4 9 5 (หลักสิบเป็น 9 เสมอ, หลักหน่วย = 9 − หลักร้อย)", 12, "middle", 700, GREEN)
    s.save("reverse-1089.svg")


def ternary27():
    s = Svg(760, 400, "ไพ่ 27 ใบ: คุมตำแหน่งปลายทางได้ทุกใบ (เลขฐาน 3)")
    s.text(30, 62, "แต่ละรอบ: ผู้ชมบอกกองที่ไพ่อยู่ → คุณวางกองนั้นไว้ช่อง บน (0) / กลาง (1) / ล่าง (2)", 14, "start", 600)
    s.text(30, 86, "ตำแหน่งปลายทาง t (นับจาก 0) = 9·ช่องรอบ3 + 3·ช่องรอบ2 + ช่องรอบ1", 14, "start", 700, BLUE)
    heads = ["อยากให้ไพ่อยู่ใบที่", "รอบ 1", "รอบ 2", "รอบ 3"]
    xs = [40, 300, 440, 580]
    for x, h in zip(xs, heads): s.text(x, 122, h, 13, "start", 700, MUTE)
    names = ["บน", "กลาง", "ล่าง"]
    for i, pos in enumerate([1, 14, 21, 27]):
        y = 134 + i * 44
        s.rect(30, y, 700, 36, PAPER, "#9ca3af", 1.2, 6)
        s.text(40, y + 24, f"ใบที่ {pos}" + ("  (บนสุด)" if pos == 1 else "  (กลางพอดี)" if pos == 14 else "  (ล่างสุด)" if pos == 27 else ""), 14, "start", 700)
        d = digits_of(pos - 1, 3, 3)
        for k in range(3):
            s.text(xs[k + 1], y + 24, names[d[k]], 14, "start", 700, GREEN)
    s.rect(30, 320, 700, 66, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 346, "ตรวจครบทุกตำแหน่งเริ่มต้น × ทุกตำแหน่งปลายทาง (27 × 27) แล้ว", 13, "middle", 700, GREEN)
    s.text(380, 368, "แจกหงายทีละใบเป็น 3 กอง → พลิกแต่ละกองคว่ำทั้งก้อน → ซ้อนตามช่องที่ต้องการ", 12, "middle", 400)
    s.save("ternary-27.svg")


def five_piles():
    s = Svg(760, 380, "ไพ่ 25 ใบ: 5 กอง × 5 ใบ แค่ 2 รอบ")
    s.text(30, 62, "แจกหงาย 5 กอง (กองละ 5)  →  ผู้ชมบอกกอง  →  ซ้อนกองนั้นไว้ช่อง (บน=0 … ล่าง=4)", 14, "start", 600)
    for p in range(5):
        s.text(60 + p * 56, 92, "ABCDE"[p], 12, "middle", 700, MUTE)
        for r in range(5):
            n = r * 5 + p + 1
            mid = n == 13
            s.rect(38 + p * 56, 98 + r * 34, 44, 28, "#fff3cd" if mid else PAPER, GOLD if mid else "#9ca3af", 2.5 if mid else 1.2, 4)
            s.text(60 + p * 56, 118 + r * 34, n, 14, "middle", 700)
    s.text(350, 112, "ตำแหน่งปลายทาง t = 5 × ช่องรอบ2 + ช่องรอบ1", 14, "start", 700, BLUE)
    for i, pos in enumerate([1, 8, 13, 25]):
        d = digits_of(pos - 1, 5, 2)
        y = 134 + i * 38
        s.rect(350, y, 380, 30, PAPER, "#9ca3af", 1.2, 6)
        s.text(360, y + 21, f"ใบที่ {pos}", 13, "start", 700)
        s.text(470, y + 21, f"รอบ1 = ช่อง {d[0]}", 13, "start", 700, GREEN)
        s.text(600, y + 21, f"รอบ2 = ช่อง {d[1]}", 13, "start", 700, GREEN)
    s.rect(350, 296, 380, 56, "#ecfdf5", GREEN, 1.5, 10)
    s.text(540, 320, "ใบที่ 13 (กลางพอดี) = ช่อง 2 ทั้งสองรอบ", 13, "middle", 700, GREEN)
    s.text(540, 340, "ตรวจทุกตำแหน่งเริ่ม × ปลายทางแล้ว", 12, "middle", 400)
    s.save("five-piles-25.svg")


def stebbins_formula():
    seq = stebbins_seq()
    s = Svg(760, 340, "Si Stebbins: ตำแหน่ง n → ไพ่ ได้ทันทีด้วยสูตร")
    s.text(30, 66, "เลข = (3n − 2) mod 13   (ได้ 0 ให้ใช้ K)", 15, "start", 700, BLUE)
    s.text(30, 92, "ดอก = ลำดับที่ (n − 1) mod 4  ในวงรอบ ♣ ♥ ♠ ♦", 15, "start", 700, BLUE)
    for i, n in enumerate([20, 33, 52]):
        x = 40 + i * 235
        v = (3 * n - 2) % 13 or 13
        card = seq[n - 1]
        assert card[:-1] == {1: "A", 11: "J", 12: "Q", 13: "K"}.get(v, str(v))
        s.rect(x, 116, 215, 160, PAPER, "#9ca3af", 1.5, 10)
        s.text(x + 107, 142, f"ตำแหน่ง n = {n}", 14, "middle", 700)
        s.text(x + 107, 168, f"เลข: 3·{n} − 2 = {3*n-2}", 12, "middle")
        s.text(x + 107, 186, f"{3*n-2} mod 13 = {v}", 12, "middle")
        s.text(x + 107, 208, f"ดอก: ({n}−1) mod 4 = {(n-1)%4}", 12, "middle")
        s.card(x + 78, 220, card, 40, 50)
    s.rect(30, 288, 700, 44, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 316, "ให้ผู้ชมบอกเลขตำแหน่ง 1–52 → คุณบอกไพ่ในตำแหน่งนั้นได้ทันที (ตรวจครบ 52 ตำแหน่ง)", 13, "middle", 700, GREEN)
    s.save("stebbins-formula.svg")


def poker_deal():
    s = Svg(760, 360, "โป๊กเกอร์ดีล: เอซ 4 ใบอยู่ใบที่ 4, 8, 12, 16 → ตกกับผู้เล่นคนที่ 4 (คุณ)")
    for p in range(4):
        x = 40 + p * 175
        s.text(x + 60, 66, f"ผู้เล่น {p+1}" + (" (คุณ)" if p == 3 else ""), 14, "middle", 700, GREEN if p == 3 else INK)
        for r in range(5):
            n = r * 4 + p + 1
            ace = p == 3 and r < 4
            s.rect(x, 78 + r * 40, 120, 32, "#fff3cd" if ace else PAPER, GOLD if ace else "#9ca3af", 2.5 if ace else 1.2, 6)
            s.text(x + 14, 99 + r * 40, f"ใบที่ {n}", 12, "start", 400, MUTE)
            s.text(x + 106, 99 + r * 40, "A" if ace else "?", 16, "end", 700, RED if ace else INK)
    s.rect(30, 290, 700, 56, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 314, "แจกวนทีละใบให้ผู้เล่น 1 → 2 → 3 → 4 (คุณเป็นคนสุดท้าย) คนละ 5 ใบ", 13, "middle", 700, GREEN)
    s.text(380, 334, "สำรับต้องไม่ถูกสับ/ตัดก่อนแจก  ·  เอซอยู่ใบที่ 4, 8, 12, 16 ของสำรับ", 12, "middle", 400)
    s.save("poker-deal.svg")


def faro_binary():
    s = Svg(760, 380, "Faro Binary: นำไพ่บนสุดไปตำแหน่งใดก็ได้ ด้วย In/Out ตามเลขฐานสอง")
    s.text(30, 62, "กฎ: In-shuffle = ตำแหน่ง → 2i + 1   ·   Out-shuffle = ตำแหน่ง → 2i   (i นับจาก 0, เมื่อ i < 26)", 13, "start", 700, BLUE)
    s.text(30, 86, "เขียนตำแหน่งปลายทาง t (นับจาก 0) เป็นเลขฐานสอง  → บิต 1 = In, บิต 0 = Out (อ่านจากซ้ายไปขวา)", 13, "start", 600)
    rows = [(27, "ใบที่ 27"), (12, "ใบที่ 12"), (40, "ใบที่ 40")]
    for i, (pos, lab) in enumerate(rows):
        tt = pos - 1; bits = bin(tt)[2:]
        idx, path = 0, [0]
        for ch in bits: idx = 2 * idx + int(ch); path.append(idx)
        assert idx == tt
        y = 112 + i * 62
        s.rect(30, y, 700, 52, PAPER, "#9ca3af", 1.2, 8)
        s.text(42, y + 22, f"{lab}  (t = {tt} = {bits}₂)", 14, "start", 700)
        s.text(42, y + 42, "  →  ".join(("In" if c == "1" else "Out") for c in bits), 13, "start", 700, GREEN)
        s.text(724, y + 42, "ตำแหน่งที่เปลี่ยน: " + " → ".join(str(x + 1) for x in path), 12, "end", 400, MUTE)
    s.rect(30, 304, 700, 62, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 328, "ไพ่อยู่ตำแหน่ง p ไม่ใช่บนสุด? ตัดสำรับ (ย้ายบน p−1 ใบไปล่าง) ให้ไพ่ขึ้นบนก่อน แล้วค่อย Faro", 13, "middle", 700, GREEN)
    s.text(380, 350, "ตรวจครบทุกตำแหน่ง 1–52 ด้วยการจำลอง Faro จริงบนสำรับ 52 ใบ", 12, "middle", 400)
    s.save("faro-binary.svg")


def mod9():
    s = Svg(760, 360, "เศษหาร 9: ทายเลขที่ผู้ชมปิดไว้ จากผลรวมเลขที่เหลือ")
    steps = [("① ไพ่ 5 ใบ (A=1…9) เรียงเป็นเลข", "5 3 8 2 1  →  53821"), ("② สลับลำดับไพ่ใหม่", "1 2 3 5 8  →  12358"),
             ("③ ลบ (ใหญ่ − เล็ก)", "53821 − 12358 = 41463"), ("④ ผู้ชมปิดเลข 1 หลักที่ไม่ใช่ 0 (ตัวอย่าง: 6)", "บอกที่เหลือ: 4 1 4 3")]
    for i, (a, b) in enumerate(steps):
        x, y = 30 + (i % 2) * 360, 56 + (i // 2) * 96
        s.rect(x, y, 340, 84, PAPER, BLUE, 2, 10)
        s.text(x + 170, y + 26, a, 12, "middle", 700, BLUE)
        s.text(x + 170, y + 62, b, 17, "middle", 700)
    s.rect(30, 256, 700, 92, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 282, "คุณบวกเลขที่เหลือ: 4 + 1 + 4 + 3 = 12  →  12 หาร 9 เหลือเศษ 3", 14, "middle", 700, GREEN)
    s.text(380, 308, "เลขที่ปิด = 9 − 3 = 6  (ถ้าเศษเป็น 0 เลขที่ปิดคือ 9)", 14, "middle", 700, GREEN)
    s.text(380, 332, "เหตุผล: เลขที่สลับหลักกัน มีผลรวมหลักเท่ากัน → ผลต่างหารด้วย 9 ลงตัวเสมอ", 12, "middle", 400)
    assert 53821 - 12358 == 41463 and (9 - (4 + 1 + 4 + 3) % 9) % 9 == 6
    s.save("mod9.svg")


def josephus():
    s = Svg(760, 360, "Josephus Shuffle: ทิ้งใบบนสุด ย้ายใบถัดไปไปล่าง ทำซ้ำ → เหลือใบเดียว")
    q = list(range(1, 11)); order = []
    while len(q) > 1:
        order.append(q.pop(0))
        if len(q) > 1: q.append(q.pop(0))
    surv = q[0]
    assert surv == josephus_top(10) == 4
    s.text(30, 62, "ตัวอย่าง 10 ใบ (เลข = ตำแหน่งเดิมนับจากบน) ลำดับที่ถูกทิ้ง:", 14, "start", 600)
    for i, n in enumerate(range(1, 11)):
        x = 30 + i * 70
        k = order.index(n) + 1 if n in order else None
        s.rect(x, 80, 62, 64, "#fff3cd" if n == surv else PAPER, GOLD if n == surv else "#9ca3af", 3 if n == surv else 1.2, 6)
        s.text(x + 31, 108, n, 18, "middle", 700)
        s.text(x + 31, 134, f"ทิ้งที่ {k}" if k else "รอด!", 11, "middle", 700, MUTE if k else GREEN)
    s.rect(30, 170, 700, 64, "#eff6ff", BLUE, 1.2, 10)
    s.text(380, 196, "สูตร (สำหรับ n ใบ, n > 1): ให้ m = 2 ยกกำลังสูงสุดที่ ≤ n − 1", 13, "middle", 600)
    s.text(380, 220, "ใบที่รอด = 2 × (n − 1 − m) + 2  (นับจากบนสุดก่อนเริ่ม)", 16, "middle", 700, BLUE)
    s.text(380, 262, "ตัวอย่าง: n = 10 → m = 8 → 2 × (9 − 8) + 2 = 4   ✓ (ภาพบน)", 14, "middle", 600)
    s.rect(30, 280, 700, 64, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 306, "n = 52 → m = 32 → 2 × (51 − 32) + 2 = 40", 15, "middle", 700, GREEN)
    s.text(380, 328, "ไพ่ใบที่ 40 จากบนสุดคือใบที่เหลือรอดเสมอ (ตรวจ n = 1–52 ด้วยการจำลองแล้ว)", 12, "middle", 400)
    s.save("josephus.svg")


def base_n():
    s = Svg(760, 340, "สูตรทั่วไป: n กอง k รอบ = ไพ่ nᵏ ใบ  →  ตำแหน่งปลายทางเป็นเลขฐาน n")
    heads = ["จำนวนไพ่", "กอง × รอบ", "ตำแหน่งปลายทาง t (จาก 0)", "ใบกลางพอดี = ช่อง"]
    xs = [40, 190, 340, 580]
    for x, h in zip(xs, heads): s.text(x, 66, h, 13, "start", 700, MUTE)
    rows = [("9", "3 × 2", "3·ช่องรอบ2 + ช่องรอบ1", "กลาง, กลาง → ใบที่ 5"),
            ("16", "4 × 2", "4·ช่องรอบ2 + ช่องรอบ1", "(ไม่มีช่องกลางตรง)"),
            ("25", "5 × 2", "5·ช่องรอบ2 + ช่องรอบ1", "กลาง, กลาง → ใบที่ 13"),
            ("27", "3 × 3", "9·ช่องรอบ3 + 3·ช่อง2 + ช่อง1", "กลาง ×3 → ใบที่ 14"),
            ("36", "6 × 2", "6·ช่องรอบ2 + ช่องรอบ1", "(ไม่มีช่องกลางตรง)"),
            ("49", "7 × 2", "7·ช่องรอบ2 + ช่องรอบ1", "กลาง, กลาง → ใบที่ 25")]
    for i, r in enumerate(rows):
        y = 76 + i * 38
        s.rect(30, y, 700, 32, PAPER, "#9ca3af", 1.2, 6)
        for x, v in zip(xs, r): s.text(x, y + 22, v, 13, "start", 600)
    s.rect(30, 312 - 8, 700, 30, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 331 - 8, "ตรวจด้วยการจำลองจริง: (3,2) (4,2) (5,2) (3,3) — ทุกตำแหน่งเริ่ม × ทุกตำแหน่งปลายทาง", 12, "middle", 700, GREEN)
    s.save("base-n.svg")


def stebbins_crt():
    seq = stebbins_seq()
    n = seq.index("8♦") + 1
    assert n == 12
    s = Svg(760, 360, "Stebbins ย้อนกลับ: ไพ่ → ตำแหน่ง (Chinese Remainder)")
    s.text(30, 62, "ตัวอย่าง: ผู้ชมหยิบ 8♦  → ไพ่นี้อยู่ตำแหน่งที่เท่าไร?", 15, "start", 700)
    box(s, 30, 78, 340, 126, "① เลข → ตำแหน่งแบบวนรอบ 13", ["n ≡ 9 × (ค่า + 2)  (mod 13)", "ค่า = 8:  9 × 10 = 90  →  90 mod 13 = 12", "ตัวเลือก: n = 12, 25, 38, 51"], BLUE)
    box(s, 390, 78, 340, 126, "② ดอก → ตำแหน่งแบบวนรอบ 4", ["ลำดับดอก ♣=0 ♥=1 ♠=2 ♦=3", "n ≡ ลำดับดอก + 1  (mod 4)", "♦: n ≡ 4 ≡ 0  (mod 4)"], GOLD)
    s.rect(30, 216, 700, 56, PAPER, "#9ca3af", 1.2, 8)
    for i, c in enumerate([12, 25, 38, 51]):
        x = 60 + i * 170
        ok = c % 4 == 0
        s.text(x, 240, f"{c}  mod 4 = {c % 4}", 14, "start", 700, GREEN if ok else MUTE)
        s.text(x, 260, "✓ ตรง" if ok else "✗", 12, "start", 700, GREEN if ok else MUTE)
    s.rect(30, 288, 700, 52, "#ecfdf5", GREEN, 1.5, 10)
    s.text(380, 312, "8♦ = ตำแหน่งที่ 12 ของสำรับ", 16, "middle", 700, GREEN)
    s.text(380, 332, "ตรวจครบทุกใบ (52 ใบ) แล้ว: มีตัวเลือกเดียวเสมอ", 12, "middle", 400)
    s.save("stebbins-crt.svg")


# ---------------------------------------------------------------- overview
def learning_path():
    s = Svg(760, 500, "เส้นทางการเรียน: ไต่ระดับจากง่ายไปยาก")
    levels = [("ง่าย", GREEN, ["ไพ่คีย์", "ไพ่ 9 ใบ", "ไพ่สะกดชื่อ", "เอซ 4 กอง", "คู่–คี่ คว่ำ/หงาย", "ไพ่ที่หายไป / เลขลับ", "แยกสี / สมดุลสี", "สี่เหลี่ยมมหัศจรรย์", "Overhand Shuffle", "Glimpse", "Cross-Cut Force"]),
              ("กลาง", GOLD, ["ไพ่ 21 ใบ", "Gilbreath (สี/ดอก)", "Si Stebbins", "Kruskal Count", "Binary Cards", "เลข 1089 / ไพ่ 27, 25 ใบ", "โป๊กเกอร์ดีล", "Double Lift", "Hindu Shuffle Force", "Riffle + Bridge"]),
              ("ยาก", RED, ["Fitch–Cheney 5 ใบ", "Mnemonica Stack", "Monge's Shuffle", "Faro คณิต + Faro Binary", "เศษหาร 9, Josephus", "n กอง k รอบ / Stebbins ย้อน", "Classic Pass", "Top-Card Palm", "Faro Shuffle จริง"])]
    for i, (name, c, items) in enumerate(levels):
        x = 30 + i * 240
        h = 62 + len(items) * 28
        y = 480 - h
        s.rect(x, y, 220, h, "#fff", c, 2.5, 12)
        s.text(x + 110, y + 28, f"ระดับ{name}", 17, "middle", 700, c)
        for k, it in enumerate(items):
            s.rect(x + 16, y + 42 + k * 28, 188, 22, "#f8fafc", "#cbd5e1", 1, 5)
            s.text(x + 110, y + 58 + k * 28, it, 13, "middle", 600)
        if i < 2:
            s.line(x + 224, 440, x + 236, 440, MUTE, 2, arrow=True)
    s.save("learning-path.svg")


def cover():
    s = Svg(760, 220, "Wiki มายากลไพ่: ไพ่คำนวณ  &  ไพ่ฝีมือ")
    xs = [("A♠", 60), ("K♥", 160), ("Q♦", 260), ("J♣", 360), ("10♥", 460), ("9♠", 560)]
    for i, (c, x) in enumerate(xs):
        s.parts.append(f'<g transform="rotate({-18 + i*7} {x+30} 160)">')
        s.card(x, 60, c, 70, 98)
        s.parts.append('</g>')
    s.text(380, 200, "ง่าย  →  กลาง  →  ยาก", 16, "middle", 700, BLUE)
    s.save("cover.svg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (keycard, nine_cards, twentyone, gilbreath, stebbins, fitch, faro_math, overhand, glimpse,
               crosscut, double_lift, hindu_force, riffle, classic_pass, palm, faro_physical,
               learning_path, cover, spelling, four_aces_deal, parity, kruskal, binary_cards_img,
               gilbreath_suit, mnemonica, monge_img, fitch_flow,
               missing_card, secret_number, alt_color_deal, color_balance, magic_square, reverse_1089,
               ternary27, five_piles, stebbins_formula, poker_deal, faro_binary, mod9, josephus, base_n,
               stebbins_crt):
        fn()
    print("สร้างภาพครบ", len(os.listdir(OUT)), "ไฟล์")
