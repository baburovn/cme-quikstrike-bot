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

    def test_inline_keyboards(self):
        miniapp_kb = bot_keyboards.get_miniapp_inline_keyboard()
        self.assertIsNotNone(miniapp_kb)
        oi_kb = bot_keyboards.get_oi_inline_keyboard()
        self.assertIsNotNone(oi_kb)
        ch_kb = bot_keyboards.get_channel_inline_keyboard()
        self.assertIsNotNone(ch_kb)


if __name__ == "__main__":
    unittest.main()
