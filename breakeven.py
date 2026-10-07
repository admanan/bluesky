#!/usr/bin/env python3
"""โปรแกรมคำนวณจุดคุ้มทุน (Break-even) สินค้าหลาย SKU

วิธีคำนวณ (Sales-mix method):
  กำไรส่วนเกินต่อหน่วย (CM)  = ราคาขาย - ต้นทุนผันแปร
  สัดส่วนยอดขาย (mix)        = จำนวนที่ขายของ SKU / จำนวนรวม (ปรับให้รวมเป็น 100%)
  CM เฉลี่ยถ่วงน้ำหนัก       = Σ (CM_i * mix_i)
  จุดคุ้มทุนรวม (หน่วย)      = ต้นทุนคงที่ / CM เฉลี่ยถ่วงน้ำหนัก
  จุดคุ้มทุนของแต่ละ SKU     = จุดคุ้มทุนรวม * mix_i

ตัวอย่าง:
  python3 breakeven.py sample.csv --fixed 50000
  python3 breakeven.py sample.csv --fixed 50000 --target-profit 20000
  python3 breakeven.py --interactive
"""
import argparse
import csv
import sys
from dataclasses import dataclass


@dataclass
class Sku:
    name: str
    price: float
    var_cost: float
    mix: float  # น้ำหนักสัดส่วนยอดขาย (หน่วยใดก็ได้ จะถูก normalize)

    @property
    def cm(self):
        return self.price - self.var_cost

    @property
    def cm_ratio(self):
        return self.cm / self.price if self.price else 0.0


def load_csv(path):
    """อ่าน CSV คอลัมน์: sku,price,variable_cost,mix"""
    skus = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            try:
                skus.append(Sku(row["sku"].strip(), float(row["price"]),
                                float(row["variable_cost"]), float(row["mix"])))
            except (KeyError, ValueError, AttributeError) as e:
                raise ValueError(f"บรรทัด {i} ในไฟล์ไม่ถูกต้อง: {e!r}")
    return skus


def validate(skus):
    if not skus:
        raise ValueError("ไม่มีข้อมูลสินค้า")
    for s in skus:
        if s.price <= 0:
            raise ValueError(f"{s.name}: ราคาขายต้องมากกว่า 0")
        if s.var_cost < 0 or s.mix < 0:
            raise ValueError(f"{s.name}: ต้นทุนผันแปร/สัดส่วน ต้องไม่ติดลบ")
    if sum(s.mix for s in skus) <= 0:
        raise ValueError("ผลรวมสัดส่วนยอดขาย (mix) ต้องมากกว่า 0")


def calculate(skus, fixed, target_profit=0.0, expected_units=None):
    """คืน dict ผลลัพธ์ รวมต่อ SKU"""
    validate(skus)
    total_mix = sum(s.mix for s in skus)
    shares = [s.mix / total_mix for s in skus]
    wacm = sum(s.cm * w for s, w in zip(skus, shares))
    avg_price = sum(s.price * w for s, w in zip(skus, shares))
    res = {"fixed": fixed, "target_profit": target_profit, "wacm": wacm,
           "avg_price": avg_price, "rows": [], "feasible": wacm > 0}
    if wacm <= 0:
        return res  # ขายเท่าไรก็ไม่คุ้มทุน

    def units_for(profit):
        return (fixed + profit) / wacm

    bep = units_for(0)
    tgt = units_for(target_profit)
    for s, w in zip(skus, shares):
        res["rows"].append({
            "sku": s.name, "price": s.price, "var_cost": s.var_cost,
            "cm": s.cm, "cm_ratio": s.cm_ratio, "share": w,
            "bep_units": bep * w, "bep_revenue": bep * w * s.price,
            "target_units": tgt * w, "target_revenue": tgt * w * s.price,
        })
    res["bep_units"] = bep
    res["bep_revenue"] = sum(r["bep_revenue"] for r in res["rows"])
    res["target_units"] = tgt
    res["target_revenue"] = sum(r["target_revenue"] for r in res["rows"])
    if expected_units:
        mos_units = expected_units - bep
        res["margin_of_safety_units"] = mos_units
        res["margin_of_safety_pct"] = mos_units / expected_units
        res["expected_profit"] = expected_units * wacm - fixed
    return res


def ceil_int(x):
    n = int(x)
    return n if n == x else n + 1


def render(res):
    out = []
    if not res["feasible"]:
        return ("⚠ CM เฉลี่ยถ่วงน้ำหนัก ≤ 0 : ราคาขายไม่เพียงพอครอบคลุมต้นทุนผันแปร "
                "ไม่มีจุดคุ้มทุน กรุณาปรับราคา/ต้นทุน/สัดส่วนสินค้า")
    show_t = res["target_profit"] > 0
    hdr = ["SKU", "ราคา", "ต้นทุนผันแปร", "CM/หน่วย", "CM%", "สัดส่วน",
           "BEP(หน่วย)", "BEP(บาท)"]
    if show_t:
        hdr += ["เป้าหมาย(หน่วย)", "เป้าหมาย(บาท)"]
    rows = [hdr]
    for r in res["rows"]:
        line = [r["sku"], f"{r['price']:,.2f}", f"{r['var_cost']:,.2f}",
                f"{r['cm']:,.2f}", f"{r['cm_ratio']:.1%}", f"{r['share']:.1%}",
                f"{ceil_int(round(r['bep_units'], 6)):,}", f"{r['bep_revenue']:,.2f}"]
        if show_t:
            line += [f"{ceil_int(round(r['target_units'], 6)):,}", f"{r['target_revenue']:,.2f}"]
        rows.append(line)
    widths = [max(len(row[i]) for row in rows) for i in range(len(hdr))]
    for k, row in enumerate(rows):
        out.append("  ".join(c.ljust(widths[i]) if i == 0 else c.rjust(widths[i])
                             for i, c in enumerate(row)))
        if k == 0:
            out.append("-" * (sum(widths) + 2 * (len(widths) - 1)))
    out.append("")
    out.append(f"ต้นทุนคงที่รวม            : {res['fixed']:,.2f} บาท")
    out.append(f"ราคาขายเฉลี่ยถ่วงน้ำหนัก   : {res['avg_price']:,.2f} บาท/หน่วย")
    out.append(f"CM เฉลี่ยถ่วงน้ำหนัก       : {res['wacm']:,.2f} บาท/หน่วย")
    out.append(f"จุดคุ้มทุนรวม             : {ceil_int(round(res['bep_units'], 6)):,} หน่วย "
               f"/ {res['bep_revenue']:,.2f} บาท")
    if show_t:
        out.append(f"ถึงกำไรเป้าหมาย {res['target_profit']:,.2f} บาท : "
                   f"{ceil_int(round(res['target_units'], 6)):,} หน่วย / {res['target_revenue']:,.2f} บาท")
    if "margin_of_safety_pct" in res:
        out.append(f"ยอดขายคาดการณ์ → กำไรคาดการณ์ {res['expected_profit']:,.2f} บาท, "
                   f"Margin of Safety {res['margin_of_safety_pct']:.1%} "
                   f"({res['margin_of_safety_units']:,.1f} หน่วย)")
    out.append("หมายเหตุ: ตัวเลข BEP ต่อ SKU ปัดขึ้นเป็นจำนวนเต็ม โดยสมมติว่าสัดส่วนยอดขายคงที่")
    return "\n".join(out)


def interactive():
    def ask(msg, cast=float, default=None):
        while True:
            raw = input(msg).strip()
            if not raw and default is not None:
                return default
            try:
                return cast(raw.replace(",", ""))
            except ValueError:
                print("  กรุณากรอกตัวเลขให้ถูกต้อง")

    fixed = ask("ต้นทุนคงที่รวมต่อเดือน (บาท): ")
    skus = []
    print("กรอกข้อมูล SKU (เว้นชื่อว่างเพื่อจบ)")
    while True:
        name = input(f"ชื่อ SKU #{len(skus) + 1}: ").strip()
        if not name:
            break
        skus.append(Sku(name, ask("  ราคาขาย/หน่วย: "), ask("  ต้นทุนผันแปร/หน่วย: "),
                        ask("  สัดส่วนยอดขาย (เช่น จำนวนที่คาดว่าจะขาย): ")))
    target = ask("กำไรเป้าหมาย (บาท, Enter = 0): ", default=0.0)
    return skus, fixed, target


def main(argv=None):
    p = argparse.ArgumentParser(description="คำนวณจุดคุ้มทุนสินค้าหลาย SKU")
    p.add_argument("csv", nargs="?", help="ไฟล์ CSV: sku,price,variable_cost,mix")
    p.add_argument("--fixed", type=float, help="ต้นทุนคงที่รวม (บาท)")
    p.add_argument("--target-profit", type=float, default=0.0, help="กำไรเป้าหมาย (บาท)")
    p.add_argument("--expected-units", type=float, help="ยอดขายคาดการณ์รวม (หน่วย) เพื่อคำนวณ Margin of Safety")
    p.add_argument("-i", "--interactive", action="store_true", help="โหมดถาม-ตอบ")
    a = p.parse_args(argv)
    try:
        if a.interactive:
            skus, fixed, target = interactive()
        elif a.csv and a.fixed is not None:
            skus, fixed, target = load_csv(a.csv), a.fixed, a.target_profit
        else:
            p.error("ระบุไฟล์ CSV และ --fixed หรือใช้ --interactive")
        print(render(calculate(skus, fixed, target, a.expected_units)))
    except (ValueError, OSError) as e:
        print(f"ข้อผิดพลาด: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
