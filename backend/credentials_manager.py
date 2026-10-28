# -*- coding: utf-8 -*-
"""
CME Credentials Manager.
Centralizes reading and safely persisting CME Group / QuikStrike credentials.
"""
import logging
from pathlib import Path
from typing import Tuple

import config

logger = logging.getLogger(__name__)

CRED_FILE = Path(__file__).resolve().parent / "cme_credentials.py"


def save_cme_credentials(login: str, password: str) -> Tuple[bool, str]:
    """
    Saves CME login and password to cme_credentials.py and updates config in-memory.
    Returns (success: bool, message: str).
    """
    login = login.strip()
    password = password.strip()

    if not login or not password:
        return False, "Логин и пароль не могут быть пустыми."

    # Escape backslashes and double quotes to prevent syntax corruption
    escaped_login = login.replace("\\", "\\\\").replace('"', '\\"')
    escaped_password = password.replace("\\", "\\\\").replace('"', '\\"')

    content = (
        "# =====================================================================\n"
        "# CME GROUP / QUIKSTRIKE УЧЕТНЫЕ ДАННЫЕ\n"
        "# Здесь вы можете менять логин и пароль от аккаунта CME Group.\n"
        "# =====================================================================\n\n"
        f'CME_LOGIN = "{escaped_login}"\n'
        f'CME_PASSWORD = "{escaped_password}"\n'
    )

    try:
        with open(CRED_FILE, "w", encoding="utf-8") as f:
            f.write(content)

        config.CME_LOGIN = login
        config.CME_PASSWORD = password
        logger.info(f"CME credentials successfully updated for login '{login}'.")
        return True, "Учетные данные CME успешно обновлены."
    except Exception as e:
        logger.error(f"Error saving CME credentials: {e}")
        return False, f"Ошибка сохранения данных: {e}"
