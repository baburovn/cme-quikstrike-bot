# -*- coding: utf-8 -*-
import unittest
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from cme_analytics import analyze_quikstrike_options, format_analytics_footnote
from cme_fetcher import format_channel_report_message, format_quikstrike_telegram_message


class TestCMEAnalytics(unittest.TestCase):

    def test_empty_options(self):
        analysis = analyze_quikstrike_options([], [], current_price=2750.0, symbol="GC")
        self.assertEqual(analysis["sentiment"], "neutral")
        self.assertEqual(analysis["pcr_oi"], 1.0)
        footnote = format_analytics_footnote(analysis, "Золото (GC)")
        self.assertIn("Золото (GC)", footnote)
        self.assertIn("Сентимент", footnote)

    def test_bearish_scenario_with_itm_puts(self):
        sample_puts = [
            {"strike": 4000, "curr_oi": 3500, "chg": 1200, "vol": 2000, "type": "PUT"},
            {"strike": 4100, "curr_oi": 2800, "chg": 950, "vol": 1500, "type": "PUT"},
        ]
        sample_calls = [
            {"strike": 4500, "curr_oi": 2000, "chg": 200, "vol": 500, "type": "CALL"},
        ]
        analysis = analyze_quikstrike_options(sample_calls, sample_puts, current_price=2750.0, symbol="GC")

        self.assertEqual(analysis["sentiment"], "bearish")
        self.assertIn("🔴", analysis["sentiment_icon"])
        self.assertTrue(len(analysis["itm_put_strikes"]) >= 2)
        self.assertIn(4000, analysis["itm_put_strikes"])
        self.assertIn(4100, analysis["itm_put_strikes"])

        footnote = format_analytics_footnote(analysis, "Золото (GC)")
        self.assertIn("преобладают опционы **ПУТ**", footnote)
        self.assertIn("4000", footnote)
        self.assertIn("4100", footnote)
        self.assertIn("находятся в деньгах", footnote)
        self.assertIn("Поддержка", footnote)
        self.assertIn("Сопротивление", footnote)

    def test_bullish_scenario(self):
        sample_puts = [
            {"strike": 2500, "curr_oi": 1000, "chg": 100, "vol": 500, "type": "PUT"},
        ]
        sample_calls = [
            {"strike": 2600, "curr_oi": 6000, "chg": 2500, "vol": 3000, "type": "CALL"},
            {"strike": 2700, "curr_oi": 5000, "chg": 1800, "vol": 2500, "type": "CALL"},
        ]
        analysis = analyze_quikstrike_options(sample_calls, sample_puts, current_price=2750.0, symbol="GC")

        self.assertEqual(analysis["sentiment"], "bullish")
        self.assertIn("🟢", analysis["sentiment_icon"])
        footnote = format_analytics_footnote(analysis, "Золото (GC)")
        self.assertIn("преобладают опционы **КОЛЛ**", footnote)

    def test_channel_report_contains_footnote(self):
        report = format_channel_report_message()
        self.assertIn("ЕЖЕДНЕВНАЯ СНОСКА / АНАЛИТИКА", report)
        self.assertIn("Сентимент", report)
        self.assertIn("Поддержка", report)
        self.assertIn("Сопротивление", report)

    def test_bot_quikstrike_message_contains_footnote(self):
        msg = format_quikstrike_telegram_message(symbol="GC")
        self.assertIn("ЕЖЕДНЕВНАЯ СНОСКА / АНАЛИТИКА", msg)
        self.assertIn("Золото", msg)
        self.assertIn("Поддержка", msg)
        self.assertIn("Сопротивление", msg)


if __name__ == "__main__":
    unittest.main()
