#!/usr/bin/env python3
"""แบบฝึกหัด Fitch–Cheney: python3 wiki/tools/fitch_drill.py [จำนวนข้อ] [--answer]
แสดงไพ่ 4 ใบที่ผู้ช่วยวาง ให้ถอดรหัสใบที่ 5  (ใส่ --answer เพื่อดูเฉลย)"""
import random, sys
from verify_tricks import fc_encode, fc_decode

SYM = {"C": "♣", "D": "♦", "H": "♥", "S": "♠"}
NAME = {1: "A", 11: "J", 12: "Q", 13: "K"}
fmt = lambda c: f"{NAME.get(c[0], c[0])}{SYM[c[1]]}"

def main():
    n = int(next((a for a in sys.argv[1:] if a.isdigit()), 5))
    deck = [(r, s) for r in range(1, 14) for s in "CDHS"]
    for i in range(1, n + 1):
        hand = random.sample(deck, 5)
        shown, hid = fc_encode(hand)
        assert fc_decode(shown) == hid
        print(f"ข้อ {i}: ", "  ".join(fmt(c) for c in shown), end="")
        print(f"   → เฉลย {fmt(hid)}" if "--answer" in sys.argv else "")

if __name__ == "__main__":
    main()
