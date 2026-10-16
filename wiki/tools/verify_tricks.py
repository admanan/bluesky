#!/usr/bin/env python3
"""ตรวจความถูกต้องของกลไพ่คำนวณใน wiki  (รัน: python3 wiki/tools/verify_tricks.py [--fitch])
--fitch : ตรวจ Fitch–Cheney ครบทุกมือ C(52,5)=2,598,960 มือ (ใช้เวลาราว 1–2 นาที)"""
import random, sys, itertools

# ---------- ไพ่สะกดชื่อ ----------
WORDS = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN"]

def spelling_arrangement():
    q, res = list(range(10)), {}
    for k, w in enumerate(WORDS, 1):
        for _ in w: q.append(q.pop(0))
        res[q.pop(0)] = k
    return [res[i] for i in range(10)]          # บน -> ล่าง

# ---------- Kruskal ----------
def kval(r): return r if r <= 10 else 5
def kruskal_final(deck, s):
    i = s
    while i + kval(deck[i]) < len(deck): i += kval(deck[i])
    return i

# ---------- Binary ----------
def binary_cards():
    return [[n for n in range(1, 64) if n >> b & 1] for b in range(6)]

# ---------- Monge ----------
def monge(d):
    t = []
    for i, c in enumerate(d): t = [c] + t if i % 2 else t + [c]
    return t

# ---------- Fitch–Cheney ----------
RANK = {r: i for i, r in enumerate("A 2 3 4 5 6 7 8 9 10 J Q K".split(), 1)}
SUITRANK = {"C": 0, "D": 1, "H": 2, "S": 3}
CODES = {1: "SML", 2: "SLM", 3: "MSL", 4: "MLS", 5: "LSM", 6: "LMS"}
DECODE = {v: k for k, v in CODES.items()}

def key(c): return (c[0], SUITRANK[c[1]])       # c = (เลข 1..13, ดอก)

def fc_encode(hand):
    for a, b in itertools.combinations(hand, 2):
        if a[1] == b[1]:
            for first, hid in ((a, b), (b, a)):
                d = (hid[0] - first[0]) % 13
                if 1 <= d <= 6:
                    rest = sorted((c for c in hand if c not in (first, hid)), key=key)
                    S, M, L = rest
                    m = {"S": S, "M": M, "L": L}
                    return [first] + [m[ch] for ch in CODES[d]], hid
    raise AssertionError(hand)

def fc_decode(shown):
    first, rest = shown[0], shown[1:]
    srt = sorted(rest, key=key)
    name = {srt[0]: "S", srt[1]: "M", srt[2]: "L"}
    d = DECODE["".join(name[c] for c in rest)]
    return ((first[0] - 1 + d) % 13 + 1, first[1])

def check_fitch():
    deck = [(r, s) for r in range(1, 14) for s in "CDHS"]
    n = 0
    for hand in itertools.combinations(deck, 5):
        shown, hid = fc_encode(hand)
        assert fc_decode(shown) == hid, hand
        n += 1
    return n


# =====================================================================
#  ชุดที่ 2: กลเพิ่มเติม (ง่าย/กลาง/ยาก อย่างละ 5)
# =====================================================================
SUIT_ORDER = "CHSD"            # Si Stebbins: ♣ ♥ ♠ ♦


def deal_gather(deck, n, order):
    """แจกหงายทีละใบเป็น n กอง แล้วพลิกแต่ละกองคว่ำทั้งก้อน (ใบที่แจกก่อนขึ้นบน)
    วางซ้อนตามลำดับกอง `order` (กองแรกอยู่บนสุด)"""
    piles = [[] for _ in range(n)]
    for k, c in enumerate(deck): piles[k % n].append(c)
    return [c for i in order for c in piles[i]]


def locate_rounds(n, rounds, slots):
    """จำลองการหาตำแหน่ง: เริ่มทุกตำแหน่ง p0 ให้ผู้ชมบอกกองที่ไพ่อยู่
    แล้ววางกองนั้นไว้ช่อง slots[r] (0=บนสุด) คืนตำแหน่งสุดท้ายของไพ่ (นับจาก 0) ทุกค่า p0"""
    size = n ** rounds
    out = set()
    for p0 in range(size):
        deck, pos = list(range(size)), p0
        for r in range(rounds):
            chosen = deck.index(p0) % n       # กองที่ไพ่อยู่ (ผู้ชมบอก)
            others = [i for i in range(n) if i != chosen]
            order = others[:slots[r]] + [chosen] + others[slots[r]:]
            deck = deal_gather(deck, n, order)
        out.add(deck.index(p0))
    return out


def digits_of(t, n, k):
    return [(t // n ** i) % n for i in range(k)]            # ตัวแรก = รอบแรก (หลักน้อยสุด)


def josephus_top(n):
    """ทิ้งใบบนสุด แล้วย้ายใบถัดไปไปล่างสุด ทำซ้ำจนเหลือใบเดียว → ตำแหน่ง (นับจากบน) ของใบที่รอด"""
    if n == 1: return 1
    m = 1 << ((n - 1).bit_length() - 1)
    return 2 * (n - 1 - m) + 2


def check_extra():
    # ---------- ง่าย ----------
    for m in range(1, 14): assert sum(range(1, 14)) - (sum(range(1, 14)) - m) == m
    for v in range(1, 11):
        for s in range(1, 5):
            r = ((2 * v + 3) * 5 + s) - 15
            assert r == 10 * v + s
    for k in range(52):                                      # แจกสลับสี (ตัดสำรับได้)
        d = ["R", "B"] * 26; d = d[k:] + d[:k]
        a, b = d[0::2], d[1::2]
        assert len(set(a)) == 1 and len(set(b)) == 1 and a[0] != b[0]
    for _ in range(2000):                                    # สมดุลสี
        d = ["R"] * 26 + ["B"] * 26; random.shuffle(d)
        A, B = d[:26], d[26:]
        assert A.count("R") == B.count("B")
    sq = [[2, 7, 6], [9, 5, 1], [4, 3, 8]]
    assert all(sum(r) == 15 for r in sq) and all(sum(c) == 15 for c in zip(*sq))
    assert sq[0][0] + sq[1][1] + sq[2][2] == 15 and sq[0][2] + sq[1][1] + sq[2][0] == 15
    print("ชุดง่าย 5 กล OK")
    # ---------- กลาง ----------
    for a in range(1, 10):
        for b in range(1, 10):
            for c in range(1, 10):
                if a == c: continue
                big, small = max(100 * a + 10 * b + c, 100 * c + 10 * b + a), min(100 * a + 10 * b + c, 100 * c + 10 * b + a)
                d = big - small; s = f"{d:03d}"
                assert s[1] == "9" and int(s[0]) + int(s[2]) == 9
                assert d + int(s[::-1]) == 1089
    for (n, k) in ((3, 3), (5, 2), (3, 2), (4, 2)):          # ตำแหน่งปลายทางตามเลขฐาน n
        size = n ** k
        for t in range(size):
            digs = digits_of(t, n, k)
            res = set()
            for p0 in range(size):
                deck = list(range(size))
                for r in range(k):
                    chosen = deck.index(p0) % n
                    others = [i for i in range(n) if i != chosen]
                    order = others[:digs[r]] + [chosen] + others[digs[r]:]
                    deck = deal_gather(deck, n, order)
                res.add(deck.index(p0))
            assert res == {t}, (n, k, t, res)
    stk = []
    v, s = 1, 0
    for _ in range(52):
        stk.append((v, SUIT_ORDER[s % 4])); v = (v + 2) % 13 + 1; s += 1
    assert len(set(stk)) == 52
    for n in range(1, 53):
        v = (3 * n - 2) % 13 or 13
        assert stk[n - 1] == (v, SUIT_ORDER[(n - 1) % 4])
    for n in range(1, 53):                                   # ย้อนกลับ (CRT)
        v, su = stk[n - 1]; si = SUIT_ORDER.index(su)
        cands = [x for x in range(1, 53) if x % 13 == (9 * (v + 2)) % 13 and x % 4 == (si + 1) % 4]
        assert cands == [n]
    for n in range(1, 53):                                   # สูตรปิด: n = c0 + 13·((ดอก+1 − c0) mod 4)
        v, su = stk[n - 1]; si = SUIT_ORDER.index(su)
        c0 = (9 * (v + 2)) % 13 or 13
        assert c0 + 13 * (((si + 1) % 4 - c0) % 4) == n
    deck = list(range(52)); aces = {3, 7, 11, 15}             # โป๊กเกอร์ดีล: ใบที่ 4,8,12,16
    hands = [[] for _ in range(4)]
    for i in range(20): hands[i % 4].append(i)
    assert aces <= set(hands[3])
    print("ชุดกลาง 5 กล OK")
    # ---------- ยาก ----------
    def faro(d, in_):
        a, b = d[:26], d[26:]; r = []
        for x, y in zip(a, b): r += [y, x] if in_ else [x, y]
        return r
    for t in range(52):
        d = list(range(52)); bits = bin(t)[2:] if t else ""
        for ch in bits: d = faro(d, ch == "1")
        assert d.index(0) == t, t
    for p in range(52):                                      # ไพ่อยู่ตำแหน่ง p ตัดขึ้นบนก่อน
        d = list(range(52)); d = d[p:] + d[:p]; assert d[0] == p
    for _ in range(3000):                                    # เศษหาร 9
        L = random.randint(3, 7); digs = [random.randint(0, 9) for _ in range(L)]
        a = int("".join(map(str, digs))); random.shuffle(digs); b = int("".join(map(str, digs)))
        diff = abs(a - b)
        if diff == 0: continue
        ds = [int(c) for c in str(diff) if c != "0"]
        i = random.randrange(len(ds)); hidden = ds[i]; rest = sum(ds) - hidden
        guess = (9 - rest % 9) % 9 or 9
        assert guess == hidden
    for n in range(1, 53):                                   # Josephus
        q = list(range(1, n + 1))
        while len(q) > 1: q.pop(0); q.append(q.pop(0)) if len(q) > 1 else None
        assert q[0] == josephus_top(n), n
    print("ชุดยาก 5 กล OK")


def main():
    random.seed(1)
    arr = spelling_arrangement()
    q, out = arr[:], []
    for w in WORDS:
        for _ in w: q.append(q.pop(0))
        out.append(q.pop(0))
    assert out == list(range(1, 11)); print("สะกดชื่อ OK", arr)
    for _ in range(3000):                        # คว่ำ-หงาย (คู่/คี่)
        n = random.choice([10, 12, 13]); up = [False] * n
        for i in random.sample(range(n), random.randrange(0, n + 1, 2)): up[i] = True
        for _ in range(random.randrange(1, 30)):
            a, b = random.sample(range(n), 2); up[a] ^= True; up[b] ^= True
        h = random.randrange(n); assert ((sum(up) - up[h]) % 2 == 1) == up[h]
    print("คว่ำ-หงาย OK")
    ranks = [r for r in range(1, 14) for _ in range(4)]; T = 20000; ok = 0
    for _ in range(T):
        d = ranks[:]; random.shuffle(d); ok += kruskal_final(d, random.randrange(10)) == kruskal_final(d, 0)
    print(f"Kruskal: ตรงกัน {ok/T:.1%}")
    for n in range(1, 64): assert sum(c[0] for c in [] ) == 0 and sum(1 << b for b in range(6) if n >> b & 1) == n
    cards = binary_cards(); assert all(sum(1 << b for b in range(6) if n in cards[b]) == n for n in range(1, 64))
    print("Binary OK", [len(c) for c in cards])
    for n in range(53):                          # Gilbreath แบบดอก
        for _ in range(100):
            deck = [i % 4 for i in range(52)]
            a, b, r = list(reversed(deck[:n])), deck[n:], []
            while a or b:
                if a and (not b or random.random() < .5): r.append(a.pop(0))
                else: r.append(b.pop(0))
            assert all(sorted(r[i:i + 4]) == [0, 1, 2, 3] for i in range(0, 52, 4))
    print("Gilbreath แบบดอก OK")
    d = list(range(1, 53)); x = d[:]; k = 0
    while True:
        x = monge(x); k += 1
        if x == d: break
    assert k == 12; print("Monge วนครบ", k, "รอบ")
    check_extra()
    if "--fitch" in sys.argv: print("Fitch–Cheney ตรวจครบ", check_fitch(), "มือ OK")

if __name__ == "__main__":
    main()
