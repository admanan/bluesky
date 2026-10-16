"""ข้อมูลของทุกกลใน wiki (ลำดับในลิสต์ = ลำดับที่แสดง)
แก้ที่นี่แล้วรัน  python3 wiki/tools/build_wiki.py  เพื่อสร้าง Home / หน้ารายการระดับ / ภาพปก / ปุ่มนำทางใหม่"""

TAGS = {
    "shuf": "🔀 ผู้ชมสับสำรับได้",
    "stack": "🔧 ต้องจัดสำรับล่วงหน้า",
    "few": "🎴 ใช้ไพ่ไม่กี่ใบ",
    "help": "👥 ต้องมีผู้ช่วย",
    "mem": "🧠 ต้องท่องจำ",
    "skill": "✋ ต้องฝึกมือ",
    "pred": "📝 เล่นแบบทำนายได้",
    "calc": "🔢 มีการคำนวณ",
}
TRACKS = {"sw": ("🧮", "ไพ่คำนวณ", "Self-Working"), "sl": ("✋", "ไพ่ฝีมือ", "Sleight")}
LEVELS = {1: ("🟢", "ง่าย", "Easy", "#e8f5e9", "#15803d"),
          2: ("🟡", "กลาง", "Medium", "#fff8e1", "#b45309"),
          3: ("🔴", "ยาก", "Hard", "#fdecea", "#c62828")}

# (slug, track, level, ชื่อสั้น, สัญลักษณ์ปก, สรุป 1 บรรทัด, เวลาเรียนโดยประมาณ, แท็ก, กลที่เกี่ยวข้อง)
T = [
 # ---------- ไพ่คำนวณ: ง่าย ----------
 ("sw-easy-key-card", "sw", 1, "ไพ่คีย์", "7♣ → K♦", "ผู้ชมเลือกไพ่ เสียบกลับ ตัดสำรับ — คุณทายได้ว่าใบไหน", "10 นาที", [], ["sl-easy-glimpse", "sw-medium-stebbins", "sw-easy-nine-cards"]),
 ("sw-easy-nine-cards", "sw", 1, "ไพ่ 9 ใบ", "9", "คิดไพ่ในใจจาก 9 ใบ ถามแค่ 2 ครั้งก็หาเจอ", "10 นาที", ["shuf", "few"], ["sw-medium-21-cards", "sw-medium-27-cards"]),
 ("sw-easy-spelling", "sw", 1, "ไพ่สะกดชื่อ", "A-C-E", "สะกด O-N-E เปิดได้ A, T-W-O เปิดได้ 2 … จนถึง 10", "15 นาที", ["stack", "few"], ["sw-easy-four-aces"]),
 ("sw-easy-four-aces", "sw", 1, "เอซ 4 กอง", "A A A A", "ผู้ชมแจก 4 กอง แล้วใบบนสุดของทุกกองเป็นเอซ", "10 นาที", ["stack"], ["sw-medium-poker-deal", "sl-easy-overhand"]),
 ("sw-easy-parity", "sw", 1, "คว่ำ–หงาย (คู่–คี่)", "↑ ↓", "ผู้ชมพลิกไพ่ทีละ 2 ใบโดยคุณไม่มอง แต่คุณทายด้านของไพ่ที่ปิดไว้ได้", "15 นาที", ["few", "calc"], ["sw-easy-missing-card"]),
 ("sw-easy-missing-card", "sw", 1, "ไพ่ที่หายไป", "?", "ผู้ชมซ่อนไพ่ 1 ใบ คุณบวกเลขที่เหลือก็รู้ว่าหายใบไหน", "15 นาที", ["few", "calc"], ["sw-easy-secret-number", "sw-hard-mod9"]),
 ("sw-easy-secret-number", "sw", 1, "เลขลับจากไพ่", "× 5", "ผู้ชมคำนวณเงียบ ๆ แล้วคุณบอกได้ว่าเป็นไพ่ใบไหน", "15 นาที", ["shuf", "calc"], ["sw-medium-1089", "sw-hard-mod9"]),
 ("sw-easy-alternating-deal", "sw", 1, "แยกสีแจกสลับ", "♥ ♠", "ตัดสำรับกี่ครั้งก็ได้ แจก 2 กอง ได้กองแดงล้วนกับดำล้วน", "15 นาที", ["stack"], ["sw-medium-gilbreath"]),
 ("sw-easy-color-balance", "sw", 1, "สมดุลสี", "=", "แดงในกองของผู้ชม = ดำในกองของคุณ เสมอ แม้ผู้ชมสับเอง", "10 นาที", ["shuf", "pred"], ["sw-medium-gilbreath"]),
 ("sw-easy-magic-square", "sw", 1, "สี่เหลี่ยมมหัศจรรย์", "15", "ไพ่ A–9 วาง 3×3 ทุกแถว สดมภ์ แนวทแยงรวม 15", "20 นาที", ["few", "mem"], ["sw-medium-binary-cards"]),
 # ---------- ไพ่คำนวณ: กลาง ----------
 ("sw-medium-21-cards", "sw", 2, "ไพ่ 21 ใบ", "21", "ถามแค่ 3 ครั้ง ไพ่ที่คิดไว้อยู่ใบที่ 11 เสมอ", "20 นาที", ["shuf"], ["sw-easy-nine-cards", "sw-medium-27-cards", "sw-medium-25-cards"]),
 ("sw-medium-gilbreath", "sw", 2, "Gilbreath (สีไพ่)", "♥♠♥♠", "ผู้ชมริฟเฟิลเอง แต่ทุกคู่มีแดง 1 ใบ ดำ 1 ใบ", "30 นาที", ["stack"], ["sw-medium-gilbreath-suit", "sw-easy-alternating-deal"]),
 ("sw-medium-stebbins", "sw", 2, "Si Stebbins Stack", "+3", "สำรับเรียงเลข +3 วนดอก — ทายไพ่ที่เลือกจากไพ่ใบเดียวที่แอบดู", "1–3 วัน", ["stack", "mem", "calc"], ["sw-medium-stebbins-formula", "sw-hard-stebbins-crt", "sw-easy-key-card"]),
 ("sw-medium-kruskal", "sw", 2, "Kruskal Count", "→ →", "ผู้ชมสับเอง กระโดดนับตามค่าไพ่ แล้วไปจบที่ใบเดียวกับคุณ (≈85%)", "20 นาที", ["shuf", "pred", "calc"], []),
 ("sw-medium-binary-cards", "sw", 2, "Binary Cards", "101", "ไพ่ตัวเลข 6 ใบ ทายเลข 1–63 ที่ผู้ชมคิดไว้", "30 นาที", ["few", "calc"], ["sw-easy-magic-square"]),
 ("sw-medium-gilbreath-suit", "sw", 2, "Gilbreath (ดอกไพ่)", "♣♥♠♦", "ทุกกลุ่ม 4 ใบมีครบ 4 ดอกหลังผู้ชมริฟเฟิล", "30 นาที", ["stack"], ["sw-medium-gilbreath", "sw-medium-stebbins"]),
 ("sw-medium-1089", "sw", 2, "เลข 1089", "1089", "ไพ่ 3 ใบ กลับด้านลบบวก ได้ 1089 เสมอ", "15 นาที", ["few", "calc", "pred"], ["sw-easy-secret-number"]),
 ("sw-medium-27-cards", "sw", 2, "ไพ่ 27 ใบ", "27", "ส่งไพ่ที่คิดไว้ไปอยู่ตำแหน่งใดก็ได้ใน 3 รอบ", "1 ชั่วโมง", ["shuf", "calc"], ["sw-medium-21-cards", "sw-medium-25-cards", "sw-hard-base-n"]),
 ("sw-medium-25-cards", "sw", 2, "ไพ่ 25 ใบ", "25", "5 กอง 2 รอบ คุมตำแหน่งของไพ่ที่คิดไว้ได้", "30 นาที", ["shuf", "calc"], ["sw-medium-27-cards", "sw-hard-base-n"]),
 ("sw-medium-stebbins-formula", "sw", 2, "Stebbins: ตำแหน่ง → ไพ่", "n → ?", "ผู้ชมบอกเลข 1–52 คุณบอกไพ่ตำแหน่งนั้นได้ทันที", "1 วัน", ["stack", "mem", "calc"], ["sw-medium-stebbins", "sw-hard-stebbins-crt"]),
 ("sw-medium-poker-deal", "sw", 2, "โป๊กเกอร์ดีล", "A♠ ×4", "แจกไพ่ 4 มือตามปกติ แต่มือของคุณได้เอซครบ 4 ใบ", "10 นาที", ["stack"], ["sw-easy-four-aces"]),
 # ---------- ไพ่คำนวณ: ยาก ----------
 ("sw-hard-fitch-cheney", "sw", 3, "Fitch–Cheney 5 ใบ", "5 → 4", "ผู้ช่วยวางไพ่ 4 ใบ คุณบอกใบที่ 5 ที่ซ่อนอยู่", "2–3 วัน", ["shuf", "help", "calc", "mem"], ["sw-hard-fitch-drill"]),
 ("sw-hard-faro-math", "sw", 3, "Faro: คณิตศาสตร์ตำแหน่ง", "2i", "สูตรตำแหน่งไพ่หลัง In/Out-shuffle และข้อเท็จจริง 8/52/26 รอบ", "1 ชั่วโมง", ["calc"], ["sl-hard-faro-shuffle", "sw-hard-faro-binary"]),
 ("sw-hard-fitch-drill", "sw", 3, "Fitch–Cheney: ฝึกถอดรหัส", "S M L", "แบบฝึกถอดรหัสให้ได้ใน 5 วินาที พร้อมสคริปต์สร้างโจทย์", "1 สัปดาห์", ["help", "mem", "calc"], ["sw-hard-fitch-cheney"]),
 ("sw-hard-mnemonica", "sw", 3, "Mnemonica Stack", "4♣", "สำรับท่องจำ 52 ใบของ Tamariz ใช้เล่นได้หลายกล", "2–4 สัปดาห์", ["stack", "mem"], ["sw-medium-stebbins"]),
 ("sw-hard-monge", "sw", 3, "Monge's Shuffle", "⇄", "สับแบบคำนวณตำแหน่งได้ครบ 12 รอบสำรับกลับเป็นเดิม", "1–3 วัน", ["calc"], ["sw-hard-faro-math"]),
 ("sw-hard-faro-binary", "sw", 3, "Faro Binary", "In Out", "นำไพ่บนสุดไปตำแหน่งใดก็ได้ด้วยเลขฐานสอง", "หลายสัปดาห์", ["skill", "calc", "mem"], ["sl-hard-faro-shuffle", "sw-hard-faro-math"]),
 ("sw-hard-mod9", "sw", 3, "เศษหาร 9", "÷ 9", "ทายเลขที่ผู้ชมปิดไว้จากผลรวมหลักที่เหลือ", "30 นาที", ["few", "calc"], ["sw-easy-missing-card", "sw-medium-1089"]),
 ("sw-hard-josephus", "sw", 3, "Josephus Shuffle", "40", "ทิ้ง-ย้ายไปเรื่อย ๆ ใบสุดท้ายที่เหลือคือไพ่ที่เลือก", "1 ชั่วโมง", ["stack", "calc"], ["sw-hard-faro-binary"]),
 ("sw-hard-base-n", "sw", 3, "สูตร n กอง k รอบ", "nᵏ", "สูตรทั่วไปของไพ่ 9/16/25/27/36/49 ใบ ใช้คุมตำแหน่งไพ่ได้ทุกแบบ", "1 ชั่วโมง", ["shuf", "calc"], ["sw-medium-27-cards", "sw-medium-25-cards"]),
 ("sw-hard-stebbins-crt", "sw", 3, "Stebbins ย้อนกลับ", "mod", "ไพ่ใบไหนก็ได้ → บอกได้ว่าอยู่ตำแหน่งที่เท่าไรในสำรับ", "1–2 วัน", ["stack", "mem", "calc"], ["sw-medium-stebbins-formula", "sw-medium-stebbins"]),
 # ---------- ไพ่ฝีมือ: ง่าย ----------
 ("sl-easy-overhand", "sl", 1, "Overhand Shuffle", "⇅", "สับแบบมือ พร้อมส่งไพ่บนสุด↔ล่างสุดตามต้องการ", "3–7 วัน", ["skill"], ["sl-easy-glimpse", "sw-easy-four-aces"]),
 ("sl-easy-glimpse", "sl", 1, "Glimpse", "◉", "แอบดูไพ่ใบล่างสุดตอนเคาะสำรับให้เรียบ", "1–3 วัน", ["skill"], ["sw-easy-key-card", "sw-medium-stebbins"]),
 ("sl-easy-cross-cut-force", "sl", 1, "Cross-Cut Force", "✚", "ผู้ชมตัดสำรับ 'อย่างอิสระ' แต่ได้ไพ่ที่คุณรู้อยู่แล้ว", "1 สัปดาห์", ["skill"], ["sl-easy-overhand", "sl-easy-glimpse"]),
 # ---------- ไพ่ฝีมือ: กลาง ----------
 ("sl-medium-double-lift", "sl", 2, "Double Lift", "2 → 1", "พลิกไพ่ 2 ใบให้เหมือนใบเดียว", "2–4 สัปดาห์", ["skill"], ["sl-hard-classic-pass"]),
 ("sl-medium-hindu-force", "sl", 2, "Pinky Break & Hindu Force", "⇥", "ให้ผู้ชมสั่งหยุดเองตอนไหนก็ได้ แต่ได้ไพ่ที่คุณรู้", "2–3 สัปดาห์", ["skill"], ["sl-easy-overhand", "sl-easy-glimpse"]),
 ("sl-medium-riffle-bridge", "sl", 2, "Riffle & Bridge", "⌒", "สับริฟเฟิล ดัดสะพาน และคุมใบล่าง/บนสุดได้", "2–4 สัปดาห์", ["skill"], ["sl-hard-faro-shuffle", "sw-medium-gilbreath"]),
 # ---------- ไพ่ฝีมือ: ยาก ----------
 ("sl-hard-classic-pass", "sl", 3, "Classic Pass", "U ⇄ L", "สลับครึ่งสำรับในพริบตา ไพ่ที่เลือกขึ้นมาอยู่บนสุด", "หลายเดือน", ["skill"], ["sl-medium-double-lift", "sl-hard-palm"]),
 ("sl-hard-palm", "sl", 3, "Top-Card Palm", "◐", "ซ่อนไพ่ 1 ใบไว้ในอุ้งมือ", "หลายเดือน", ["skill"], ["sl-hard-classic-pass"]),
 ("sl-hard-faro-shuffle", "sl", 3, "Faro Shuffle (ลงมือจริง)", "26 | 26", "สอดไพ่สองครึ่งสลับทีละใบสมบูรณ์", "หลายเดือน", ["skill"], ["sw-hard-faro-math", "sw-hard-faro-binary", "sl-medium-riffle-bridge"]),
]

KEYS = ("slug", "track", "level", "short", "glyph", "summary", "time", "tags", "related")
TRICKS = [dict(zip(KEYS, t)) for t in T]
BY_SLUG = {t["slug"]: t for t in TRICKS}
