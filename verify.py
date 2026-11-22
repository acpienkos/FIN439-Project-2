"""Check the frozen decision, point-in-time gate, and interactive entry point."""
import hashlib
import json
import unittest
from dataclasses import replace
from pathlib import Path
from statistics import stdev
from tempfile import TemporaryDirectory
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

import engine

ROOT = Path(__file__).resolve().parent


class ReadinessChecks(unittest.TestCase):
    def test_grid_is_complete(self):
        grid = set(engine.grid())
        self.assertEqual(len(grid), 1771)
        self.assertTrue(all(abs(sum(weights) - 1) < 1e-12 for weights in grid))

    def test_vintage_refuses_same_day_and_current_file(self):
        self.assertEqual(engine.credit_snapshot()["yield_pct"], 6.32)
        with self.assertRaises(ValueError):
            engine.credit_snapshot(decision=engine.VINTAGE)
        with self.assertRaises(FileNotFoundError):
            engine.credit_snapshot(vintage=engine.VINTAGE.replace(day=29))

    def test_known_base_and_break_even(self):
        base = engine.evaluate()
        self.assertEqual(base["feasible_count"], 1)
        candidate = base["rows"]["Lowest-risk qualifying mix"]
        self.assertEqual(candidate["weights"], (.9, 0, 0, .1))
        bill, _, _, equity = base["gross_estimates_pct"]
        self.assertAlmostEqual(candidate["net_pct"], .9 * bill + .1 * equity - .20, 12)
        self.assertAlmostEqual(candidate["net_pct"], 4.196694207744123, 12)
        self.assertAlmostEqual(candidate["vol_pct"], 1.6615110978430472, 12)
        self.assertEqual(base["rows"]["BIL benchmark"]["failures"], ["4% net objective"])
        self.assertEqual(engine.evaluate(replace(engine.Inputs(), cost_bps=39))["feasible_count"], 1)
        self.assertEqual(engine.evaluate(replace(engine.Inputs(), cost_bps=40))["feasible_count"], 0)

    def test_report_and_independent_stresses(self):
        with (ROOT / "docs/visible-output.json").open(encoding="utf-8") as file:
            saved = json.load(file)
        current = engine.research()
        self.assertEqual(saved, json.loads(json.dumps(current)))
        base = saved["base"]["inputs"]
        for result in saved["AI-assisted stress runs"].values():
            self.assertEqual(sum(result["inputs"][key] != value for key, value in base.items()), 1)
        self.assertEqual(engine.evaluate(), current["base"])

    def test_streamlit_control_changes_verdict(self):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
        self.assertFalse(app.exception)
        self.assertIn("4.20%", app.table[0].value["Net estimate"].tolist())
        app.number_input[0].set_value(50).run()
        self.assertFalse(app.exception)
        self.assertIn("FAIL: no feasible mix", str(app.table[0].value))

    def test_portfolio_risk_against_weighted_monthly_returns(self):
        base = engine.evaluate()
        candidate = base["rows"]["Lowest-risk qualifying mix"]
        bills, _, _, equity = engine.price_returns(59)
        returns = [0.9 * bill + 0.1 * stock for bill, stock in zip(bills, equity)]
        self.assertAlmostEqual(candidate["vol_pct"], 100 * (12 ** .5) * stdev(returns), 11)
        self.assertTrue(all(candidate["rules"].values()))
        self.assertEqual(base["authorized_allocation_pct"], 0)
        self.assertTrue(all(status == "Open" for status in base["implementation_gates"].values()))

    def test_bad_inputs_and_missing_data_fail_closed(self):
        for changes in ({"months": 2.5}, {"cost_bps": -1}, {"reserve_pct": 19},
                        {"years_remaining": 6}, {"equity_shock_pp": float("nan")}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                engine.evaluate(replace(engine.Inputs(), **changes))
        with TemporaryDirectory() as directory, patch.object(engine, "DATA", Path(directory)):
            with self.assertRaises(FileNotFoundError):
                engine.evaluate()
            (Path(directory) / "prices.csv").write_text("date,wrong\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "price columns"):
                engine.evaluate()

    def test_frozen_data_hashes(self):
        for line in (ROOT / "data/SHA256SUMS").read_text(encoding="utf-8").splitlines():
            digest, filename = line.split()
            canonical = (ROOT / "data" / filename).read_text(encoding="utf-8").encode("utf-8")
            self.assertEqual(hashlib.sha256(canonical).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
