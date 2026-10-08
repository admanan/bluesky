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
    if "--fitch" in sys.argv: print("Fitch–Cheney ตรวจครบ", check_fitch(), "มือ OK")

if __name__ == "__main__":
    main()
