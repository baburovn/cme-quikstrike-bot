# -*- coding: utf-8 -*-
import sys
import unittest
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

import config
import credentials_manager


class TestCredentialsManager(unittest.TestCase):
    def setUp(self):
        self.orig_login = config.CME_LOGIN
        self.orig_password = config.CME_PASSWORD

    def tearDown(self):
        # Restore original credentials so test is idempotent
        credentials_manager.save_cme_credentials(self.orig_login, self.orig_password)

    def test_save_cme_credentials_function_exists(self):
        self.assertTrue(callable(credentials_manager.save_cme_credentials))

    def test_save_and_read_credentials(self):
        success, msg = credentials_manager.save_cme_credentials("test@example.com", "Secret123!")
        self.assertTrue(success)
        self.assertEqual(config.CME_LOGIN, "test@example.com")
        self.assertEqual(config.CME_PASSWORD, "Secret123!")

    def test_empty_credentials_rejected(self):
        success, msg = credentials_manager.save_cme_credentials("", "")
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
