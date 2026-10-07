import unittest
from breakeven import Sku, calculate


class T(unittest.TestCase):
    def test_single_sku(self):
        r = calculate([Sku("a", 100, 60, 1)], fixed=4000)
        self.assertAlmostEqual(r["bep_units"], 100)
        self.assertAlmostEqual(r["bep_revenue"], 10000)

    def test_multi_sku_mix(self):
        # mix 50/50: wacm = (40+20)/2 = 30 -> 3000/30 = 100 units, 50 each
        r = calculate([Sku("a", 100, 60, 1), Sku("b", 50, 30, 1)], fixed=3000)
        self.assertAlmostEqual(r["bep_units"], 100)
        self.assertAlmostEqual(r["rows"][0]["bep_units"], 50)
        self.assertAlmostEqual(r["bep_revenue"], 50 * 100 + 50 * 50)

    def test_target_and_mos(self):
        r = calculate([Sku("a", 100, 60, 1)], 4000, 2000, expected_units=200)
        self.assertAlmostEqual(r["target_units"], 150)
        self.assertAlmostEqual(r["margin_of_safety_pct"], 0.5)
        self.assertAlmostEqual(r["expected_profit"], 4000)

    def test_infeasible(self):
        self.assertFalse(calculate([Sku("a", 50, 60, 1)], 1000)["feasible"])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            calculate([Sku("a", 0, 1, 1)], 1)


if __name__ == "__main__":
    unittest.main()
