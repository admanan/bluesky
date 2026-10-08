#!/usr/bin/env python3
"""แบบฝึกจำ Mnemonica / Si Stebbins: python3 wiki/tools/mnemonica_drill.py [mnemonica|stebbins] [จำนวนข้อ]
ถามสลับระหว่าง 'ตำแหน่ง → ไพ่' และ 'ไพ่ → ตำแหน่ง'"""
import random, sys
from generate_images import MNEMONICA, stebbins_seq

def main():
    kind = next((a for a in sys.argv[1:] if a in ("mnemonica", "stebbins")), "mnemonica")
    n = int(next((a for a in sys.argv[1:] if a.isdigit()), 10))
    stack = MNEMONICA if kind == "mnemonica" else stebbins_seq()
    score = 0
    for _ in range(n):
        i = random.randrange(52)
        if random.random() < .5:
            ans = input(f"ตำแหน่งที่ {i+1} คือไพ่อะไร? ").strip().upper().replace("S", "♠").replace("H", "♥").replace("D", "♦").replace("C", "♣")
            ok = ans == stack[i]
        else:
            ans = input(f"{stack[i]} อยู่ตำแหน่งที่เท่าไร? ").strip()
            ok = ans == str(i + 1)
        score += ok
        print("✓" if ok else f"✗ เฉลย: {stack[i]} = ตำแหน่ง {i+1}")
    print(f"ได้ {score}/{n}")

if __name__ == "__main__":
    main()
