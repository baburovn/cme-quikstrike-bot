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

    def test_format_qs_date(self):
        self.assertEqual(cme_fetcher.format_qs_date("NOV 5"), "НОЯ 5")
        self.assertEqual(cme_fetcher.format_qs_date("OCT 1"), "ОКТ 1")
        self.assertEqual(cme_fetcher.format_qs_date(""), "")

    def test_format_channel_report_message(self):
        report = cme_fetcher.format_channel_report_message()
        self.assertIsInstance(report, str)
        self.assertIn("CME GROUP", report)
        self.assertIn("ТОП-5 КОНТРАКТОВ ПО ОТКРЫТОМУ ИНТЕРЕСУ", report)
        self.assertIn("ТОП-5 ПО МАКСИМАЛЬНОМУ ПРИТОКУ", report)
        self.assertIn("09:30 (МСК)", report)
        self.assertIn("Срез биржи:", report)
        self.assertNotIn("12:30", report)
        self.assertNotIn("Актуальные котировки рынка CME", report)

    def test_dynamic_expirations_midnight_msk_rollover(self):
        from datetime import datetime
        from cme_products import compute_dynamic_expirations, TZ_MSK

        sample = [
            {"code": "OLD", "month": "Окт 2026", "last_trade": "28.10.2026", "days_left": 99, "active": True},
            {"code": "CURR", "month": "Дек 2026", "last_trade": "29.12.2026", "days_left": 99, "active": False},
            {"code": "NEXT", "month": "Фев 2027", "last_trade": "24.02.2027", "days_left": 99, "active": False},
        ]
        day1 = datetime(2026, 11, 26, 23, 59, 0, tzinfo=TZ_MSK)
        day2 = datetime(2026, 11, 27, 0, 0, 1, tzinfo=TZ_MSK)

        res1 = compute_dynamic_expirations(sample, now_msk=day1)
        res2 = compute_dynamic_expirations(sample, now_msk=day2)

        self.assertEqual([x["code"] for x in res1], ["CURR", "NEXT"])
        self.assertTrue(res1[0]["active"])
        self.assertFalse(res1[1]["active"])
        self.assertEqual(res1[0]["days_left"], 33)
        self.assertEqual(res2[0]["days_left"], 32)


if __name__ == "__main__":
    unittest.main()
