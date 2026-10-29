# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

import cme_fetcher


class TestCMEDomain(unittest.TestCase):
    def test_get_all_quotes(self):
        quotes = cme_fetcher.get_all_quotes()
        self.assertIsInstance(quotes, list)
        self.assertGreater(len(quotes), 0)
        symbols = [q["symbol"] for q in quotes]
        self.assertIn("GC", symbols)
        self.assertIn("SI", symbols)
        for q in quotes:
            self.assertIn("price", q)
            self.assertIn("symbol", q)
            self.assertIn("volume", q)

    def test_quikstrike_most_actives_shape(self):
        data = cme_fetcher.get_quikstrike_most_actives(min_oi=1000, symbol="GC")
        self.assertIsInstance(data, dict)
        self.assertIn("calls", data)
        self.assertIn("puts", data)
        self.assertIn("metadata", data)
        self.assertIn("total_calls_all", data)
        self.assertIn("total_puts_all", data)

    def test_silver_default_min_oi_is_500(self):
        data = cme_fetcher.get_quikstrike_most_actives(symbol="SI")
        self.assertEqual(data["min_oi_filter"], 500)

    def test_gold_default_min_oi_is_1000(self):
        data = cme_fetcher.get_quikstrike_most_actives(symbol="GC")
        self.assertEqual(data["min_oi_filter"], 1000)

    def test_format_quikstrike_telegram_message(self):
        msg = cme_fetcher.format_quikstrike_telegram_message(symbol="GC")
        self.assertIsInstance(msg, str)
        self.assertIn("CME QUIKSTRIKE", msg)
        self.assertIn("CALLS", msg)
        self.assertIn("PUTS", msg)

    def test_format_channel_report_message(self):
        report = cme_fetcher.format_channel_report_message()
        self.assertIsInstance(report, str)
        self.assertIn("CME GROUP", report)
        self.assertIn("ТОП-5 КОНТРАКТОВ ПО ОТКРЫТОМУ ИНТЕРЕСУ", report)
        self.assertIn("ТОП-5 ПО МАКСИМАЛЬНОМУ ПРИТОКУ", report)
        self.assertIn("09:30 (МСК)", report)
        self.assertNotIn("12:30", report)
        self.assertNotIn("Актуальные котировки рынка CME", report)


if __name__ == "__main__":
    unittest.main()
