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

# =====================================================================
#  ชุดที่ 3: กลเพิ่มเติมอีก 15 กล
# =====================================================================
import functools

GL_SQUARE = [["A♠", "K♥", "Q♦", "J♣"], ["Q♣", "J♦", "A♥", "K♠"], ["J♥", "Q♠", "K♣", "A♦"], ["K♦", "A♣", "J♠", "Q♥"]]
HAMMING_GROUPS = {1: (1, 3, 5, 7), 2: (2, 3, 6, 7), 4: (4, 5, 6, 7)}
FANO_LINES = [(1, 2, 3), (1, 4, 5), (1, 6, 7), (2, 4, 6), (2, 5, 7), (3, 4, 7), (3, 5, 6)]


def de_bruijn(k=2, n=5):
    a = [0] * k * n; seq = []
    def db(t, p):
        if t > n:
            if n % p == 0: seq.extend(a[1:p + 1])
        else:
            a[t] = a[t - p]; db(t + 1, p)
            for j in range(a[t - p] + 1, k): a[t] = j; db(t + 1, t)
    db(1, 1)
    return seq


def pile_to_ten(deck):
    """คืน (จำนวนแถว P, ผลรวมไพ่หงาย S, จำนวนไพ่ที่เหลือ L)"""
    val = lambda r: min(r, 10)
    hand, P, S = list(deck), 0, 0
    while hand:
        c = hand.pop(0); need = 10 - val(c)
        if len(hand) < need: return P, S, len(hand) + 1
        del hand[:need]; P += 1; S += val(c)
    return P, S, 0


def nim_losing(n, misere=False):
    @functools.lru_cache(None)
    def win(k):                                  # ผู้ที่ถึงตาเดินเมื่อเหลือ k ใบ ชนะไหม
        if k == 0: return misere                 # ปกติ: คนที่ถึงตาตอน 0 = แพ้ (อีกฝ่ายหยิบหมดแล้ว); misère: ชนะ
        return any(not win(k - m) for m in (1, 2, 3) if m <= k)
    return not win(n)


def nim_sum_win(piles):
    @functools.lru_cache(None)
    def win(st):
        if sum(st) == 0: return False
        for i, p in enumerate(st):
            for m in range(1, p + 1):
                ns = list(st); ns[i] -= m
                if not win(tuple(sorted(ns))): return True
        return False
    return win(tuple(sorted(piles)))


def cross_gf2(a, b):
    a1, a2, a3 = a >> 2 & 1, a >> 1 & 1, a & 1; b1, b2, b3 = b >> 2 & 1, b >> 1 & 1, b & 1
    return (a2 & b3 ^ a3 & b2) << 2 | (a3 & b1 ^ a1 & b3) << 1 | (a1 & b2 ^ a2 & b1)


def check_extra2():
    random.seed(7)
    # ---------- ง่าย ----------
    for n in range(10, 40):                                   # ผลรวมหลัก: เหลือ 9a ใบ ใบบนสุดคือใบที่ 9a
        deck = list(range(52)); P = deck[:n][::-1]; d = sum(map(int, str(n)))
        rem = P[d:]; a = n // 10
        assert len(rem) == 9 * a and rem[0] == 9 * a - 1 and rem[-1] == 0      # บนสุด = ใบที่ 9a, ล่างสุด = ใบที่ 1 เดิม
    for _ in range(3000):                                     # หงายเท่ากัน
        N = random.randint(6, 20); h = random.randint(0, N); up = [True] * h + [False] * (N - h); random.shuffle(up)
        idx = set(random.sample(range(N), h)); A = [not up[i] for i in idx]; B = [up[i] for i in range(N) if i not in idx]
        assert sum(A) == sum(B)
    for t_ in range(16):                                      # 16 ใบ 2 กอง 4 รอบ → ไพ่ไปตำแหน่ง t
        for p0 in range(16):
            deck = list(range(16))
            for r in range(4):
                chosen = deck.index(p0) % 2; slot = t_ >> r & 1
                order = [chosen, 1 - chosen] if slot == 0 else [1 - chosen, chosen]
                deck = deal_gather(deck, 2, order)
            assert deck.index(p0) == t_
    rows = GL_SQUARE; cells = [[(r[c][:-1], r[c][-1]) for c in range(4)] for r in rows]
    def ok(group): return len({g[0] for g in group}) == 4 and len({g[1] for g in group}) == 4
    for i in range(4):
        assert ok(cells[i]) and ok([cells[r][i] for r in range(4)])
    assert ok([cells[i][i] for i in range(4)]) and ok([cells[i][3 - i] for i in range(4)])
    assert ok([cells[0][0], cells[0][3], cells[3][0], cells[3][3]])
    for r, c in ((0, 0), (0, 2), (2, 0), (2, 2), (1, 1)):       # บล็อก 2×2: มี 5 บล็อกที่ครบ (4 มุมใหญ่ + กลาง)
        assert ok([cells[r][c], cells[r][c + 1], cells[r + 1][c], cells[r + 1][c + 1]])
    assert not ok([cells[0][1], cells[0][2], cells[1][1], cells[1][2]])          # บล็อก 2×2 อื่นไม่ครบ
    flat = {(r, c): cells[r][c] for r in range(4) for c in range(4)}
    good = [g for g in itertools.combinations(flat, 4) if len({flat[x][0] for x in g}) == 4 and len({flat[x][1] for x in g}) == 4]
    assert len(good) == 24                                                     # ทั้งหมด 24 กลุ่ม (ใน 1,820 แบบ)
    assert len({x for row in rows for x in row}) == 16
    for _ in range(2000):                                     # คูณ 11
        L = random.randint(1, 6); n = random.randint(10 ** (L - 1), 10 ** L - 1); ds = [0] + [int(c) for c in str(n)] + [0]
        carry, out = 0, []
        for i in range(len(ds) - 1, 0, -1):
            s = ds[i] + ds[i - 1] + carry; out.append(s % 10); carry = s // 10
        if carry: out.append(carry)
        assert int("".join(map(str, out[::-1]))) == n * 11
    print("ชุดง่ายใหม่ 5 กล OK")
    # ---------- กลาง ----------
    for n in range(0, 61):
        assert nim_losing(n) == (n % 4 == 0)
        assert nim_losing(n, misere=True) == (n % 4 == 1)
    for n in range(100, 1000):
        assert int(f"{n}{n}") % 1001 == 0 and int(f"{n}{n}") // 7 // 11 // 13 == n
    for a in range(1, 11):
        for b in range(1, 11):
            s = [a, b]
            for _ in range(8): s.append(s[-1] + s[-2])
            assert sum(s) == 11 * s[6] == 55 * a + 88 * b
    for _ in range(3000):                                     # ตารางคู่–คี่ 5×5
        g = [[random.random() < .5 for _ in range(5)] for _ in range(5)]
        for i in range(4): g[i][4] = sum(g[i][:4]) % 2 == 1
        for j in range(5): g[4][j] = sum(g[i][j] for i in range(4)) % 2 == 1
        assert all(sum(r) % 2 == 0 for r in g) and all(sum(g[i][j] for i in range(5)) % 2 == 0 for j in range(5))
        i, j = random.randrange(5), random.randrange(5); g[i][j] = not g[i][j]
        odd_r = [r for r in range(5) if sum(g[r]) % 2]; odd_c = [c for c in range(5) if sum(g[r][c] for r in range(5)) % 2]
        assert odd_r == [i] and odd_c == [j]
    for _ in range(3000):                                     # กองถึง 10
        d = [r for r in range(1, 14) for _ in range(4)]; random.shuffle(d)
        P, S, L = pile_to_ten(d); assert L == 52 - 11 * P + S
    print("ชุดกลางใหม่ 5 กล OK")
    # ---------- ยาก ----------
    seq = de_bruijn(); assert len(seq) == 32 and sum(seq) == 16
    wins = {tuple(seq[(i + j) % 32] for j in range(5)) for i in range(32)}; assert len(wins) == 32
    for data in range(16):                                    # Hamming 7 ใบ
        bits = {3: data & 1, 5: data >> 1 & 1, 6: data >> 2 & 1, 7: data >> 3 & 1}
        bits[1] = (bits[3] + bits[5] + bits[7]) % 2; bits[2] = (bits[3] + bits[6] + bits[7]) % 2; bits[4] = (bits[5] + bits[6] + bits[7]) % 2
        for flip in range(0, 8):
            b = dict(bits)
            if flip: b[flip] ^= 1
            syn = sum(g for g, mem in HAMMING_GROUPS.items() if sum(b[m] for m in mem) % 2)
            assert syn == flip
            xor = 0                                              # มุมมอง XOR: ตำแหน่งของไพ่หงายรวมกัน (XOR) = ตำแหน่งที่ถูกพลิก
            for pos_, v_ in b.items():
                if v_: xor ^= pos_
            assert xor == flip
    for _ in range(3000):                                     # เดาสีไพ่บนหน้าผาก
        n = random.randint(2, 26); col = [random.randint(0, 1) for _ in range(n)]   # คนที่ 0 พูดก่อน เห็นทุกคนข้างหน้า
        call0 = sum(col[1:]) % 2; said = [call0]
        for i in range(1, n):
            ahead = sum(col[i + 1:]); heard = sum(said[1:i])
            said.append((call0 - ahead - heard) % 2)
        assert said[1:] == col[1:]
    for a in range(0, 8):                                     # Nim สามกอง
        for b in range(a, 8):
            for c in range(b, 8): assert nim_sum_win((a, b, c)) == (a ^ b ^ c != 0)
    for x, y, z in FANO_LINES: assert x ^ y ^ z == 0
    for i in range(7):
        for j in range(i + 1, 7): assert len(set(FANO_LINES[i]) & set(FANO_LINES[j])) == 1
    cards = {k: {s for s in range(1, 8) if bin(s & k).count("1") % 2 == 0} for k in range(1, 8)}
    for a in range(1, 8):
        for b in range(a + 1, 8): assert cards[a] & cards[b] == {cross_gf2(a, b)}
    print("ชุดยากใหม่ 5 กล OK")


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
    check_extra2()
    if "--fitch" in sys.argv: print("Fitch–Cheney ตรวจครบ", check_fitch(), "มือ OK")

if __name__ == "__main__":
    main()
