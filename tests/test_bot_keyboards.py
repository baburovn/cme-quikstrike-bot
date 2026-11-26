# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

# Mock aiogram if running in environment where it is not installed
if "aiogram" not in sys.modules:
    try:
        import aiogram
    except ImportError:
        mock_aiogram = MagicMock()
        mock_types = MagicMock()
        mock_types.InlineKeyboardButton = lambda **kwargs: kwargs
        mock_types.InlineKeyboardMarkup = lambda **kwargs: MagicMock(inline_keyboard=kwargs.get("inline_keyboard", []))
        mock_types.KeyboardButton = lambda **kwargs: kwargs
        mock_types.ReplyKeyboardMarkup = lambda **kwargs: MagicMock(keyboard=kwargs.get("keyboard", []))
        mock_types.WebAppInfo = lambda **kwargs: kwargs
        mock_aiogram.types = mock_types
        sys.modules["aiogram"] = mock_aiogram
        sys.modules["aiogram.types"] = mock_types

backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

import bot_keyboards


class TestBotKeyboards(unittest.TestCase):
    def test_reply_keyboard(self):
        kb = bot_keyboards.get_miniapp_reply_keyboard()
        self.assertIsNotNone(kb)
        self.assertTrue(len(kb.keyboard) >= 3)

    def test_get_share_url(self):
        url = bot_keyboards.get_share_url(text="Test share text", url="https://t.me/cme_daily_info_bot")
        self.assertTrue(url.startswith("https://t.me/share/url?"))
        self.assertIn("url=", url)
        self.assertIn("text=", url)

    def test_inline_keyboards(self):
        miniapp_kb = bot_keyboards.get_miniapp_inline_keyboard()
        self.assertIsNotNone(miniapp_kb)
        oi_kb = bot_keyboards.get_oi_inline_keyboard()
        self.assertIsNotNone(oi_kb)
        ch_kb = bot_keyboards.get_channel_inline_keyboard()
        self.assertIsNotNone(ch_kb)

        # Verify share buttons exist in all keyboards
        def find_share_btn(kb):
            for row in kb.inline_keyboard:
                for btn in row:
                    text = btn.get("text", "") if isinstance(btn, dict) else getattr(btn, "text", "")
                    if "Поделиться" in text:
                        return btn
            return None

        self.assertIsNotNone(find_share_btn(ch_kb), "Share button missing in channel keyboard")
        self.assertIsNotNone(find_share_btn(oi_kb), "Share button missing in OI keyboard")
        self.assertIsNotNone(find_share_btn(miniapp_kb), "Share button missing in Mini App keyboard")

        # Verify refresh button preserves instrument symbol
        si_kb = bot_keyboards.get_oi_inline_keyboard(symbol="SI")
        refresh_callbacks = [
            (btn.get("callback_data", "") if isinstance(btn, dict) else getattr(btn, "callback_data", ""))
            for row in si_kb.inline_keyboard
            for btn in row
            if "Обновить" in (btn.get("text", "") if isinstance(btn, dict) else getattr(btn, "text", ""))
        ]
        self.assertIn("refresh_oi_data:SI", refresh_callbacks)

        # Verify beginner guide button exists in reply and all inline keyboards
        reply_kb = bot_keyboards.get_miniapp_reply_keyboard()
        reply_texts = [
            (btn.get("text", "") if isinstance(btn, dict) else getattr(btn, "text", ""))
            for row in reply_kb.keyboard
            for btn in row
        ]
        self.assertIn("📖 Пояснение терминов", reply_texts)

        for kb in (miniapp_kb, oi_kb, ch_kb):
            guide_btns = [
                btn for row in kb.inline_keyboard for btn in row
                if "Пояснение терминов" in (btn.get("text", "") if isinstance(btn, dict) else getattr(btn, "text", ""))
            ]
            self.assertTrue(len(guide_btns) > 0, "Guide button missing in inline keyboard")


if __name__ == "__main__":
    unittest.main()
