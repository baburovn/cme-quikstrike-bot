# 🪙 CME Metals & FX Terminal — Telegram Mini App & Bot

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0.svg)](https://docs.aiogram.dev/)
[![Playwright](https://img.shields.io/badge/Playwright-Headless%20Scraper-2EAD33.svg)](https://playwright.dev/)
[![TradingView](https://img.shields.io/badge/Charts-Lightweight%20Charts-2962FF.svg)](https://www.tradingview.com/lightweight-charts/)

Полнофункциональный финансовый терминал в формате **Telegram Mini App (TMA)** и аналитический Telegram-бот для мониторинга рынка фьючерсов и опционов **CME Group (Chicago Mercantile Exchange)**.

Терминал объединяет интерактивные свечные графики **TradingView Lightweight Charts**, автообновление тиковых котировок по **WebSocket** и автономный парсер опционного профиля **CME QuikStrike Most Actives** (открытый интерес, перераспределение позиций институционалов и топ крупных контрактов).

---

## 🌟 Основные возможности

### 1. 📊 Аналитический отчет QuikStrike Most Actives
* **Парсер CME QuikStrike (Playwright + Stealth bypass):** Автоматический сбор данных с защищенного портала CME Group с поддержкой SSO-авторизации и обхода систем детекции ботов (Akamai).
* **Поддерживаемые активы:**
  * 🥇 **Gold (Золото, GC)**
  * 🥈 **Silver (Серебро, SI)**
  * 💶 **EUR/USD (6E)**
  * 💷 **GBP/USD (6B)**
  * 🇦🇺 **AUD/USD (6A)**
* **Фильтрация и ранжирование:** Отбор институциональных контрактов по объему открытого интереса (OI ≥ 1,000 контрактов), двунаправленная сортировка по страйку, экспирации, объему, текущему/прошлому OI и чистому суточному притоку (`CHG`).
* **Раздельные таблицы Calls / Puts:** Детальный аудит перевеса позиций быков и медведей.

### 2. 📢 Ежедневный автоматический постинг в Telegram-канал
* **Расписание по GMT+5:**
  * `12:15 GMT+5` — запуск фонового парсера и обновление кеша `quikstrike_cache.json`.
  * `12:30 GMT+5` — автоматическая публикация в привязанный канал.
* **Структура поста в канале:**
  * 🏆 **ТОП-5 контрактов по абсолютному открытому интересу (OI)**.
  * 🔥 **ТОП-5 контрактов по максимальному суточному притоку (+OI)**.
  * Кнопка прямого перехода в интерактивный Mini App терминал.
  * Кнопка инлайн-обновления отчета.

### 3. 📈 Интерактивные графики TradingView (Lightweight Charts)
* Свечной график (Candlesticks) + подистограмма торговых объемов (Volume).
* Таймфреймы: `5M`, `15M`, `1H`, `1D`.
* Поддержка зума, скролла и плашки текущих значений OHLC при наведении курсора / тапе на мобильном устройстве.

### 4. ⚡ Real-Time котировки по WebSockets
* Мгновенная рассылка тиков через `/ws` с цветовой индикацией (зеленый/красный флеш при росте/падении цены).
* Автоматический fallback на HTTP Polling при нестабильном мобильном интернете.
* Нативная интеграция Telegram WebApp SDK: полноэкранный режим `expand()`, тактильный виброотклик `HapticFeedback`.

---

## 📁 Структура репозитория

```
cme-metals-miniapp/
├── backend/
│   ├── app.py                 # FastAPI бэкенд (REST API + WebSocket /ws)
│   ├── bot.py                 # aiogram 3 Telegram-бот (команды, инлайн-кнопки, WebApp)
│   ├── channel_manager.py     # Модуль автопостинга в канал и шедулер расписания
│   ├── cme_credentials.py     # Логин и пароль от CME (исключен из git)
│   ├── cme_credentials.example.py # Шаблон конфигурации учетных данных CME
│   ├── cme_fetcher.py         # Модели данных, кэш, генерация отчетов и агрегация
│   ├── cme_scraper.py         # Playwright-парсер CME QuikStrike под xvfb
│   ├── config.py              # Загрузка переменных окружения и настроек
│   ├── run_all.py             # Точка входа: одновременный запуск FastAPI и бота
│   └── requirements.txt       # Python-зависимости бэкенда
├── frontend/
│   ├── index.html             # Разметка Telegram Mini App
│   ├── style.css              # Dark-theme стили в стиле Bloomberg Terminal
│   └── app.js                 # Логика UI, TradingView Charts, WebSocket и таблицы QuikStrike
├── .env.example               # Шаблон переменных окружения
├── .gitignore                 # Исключение конфиденциальных файлов и кэшей
├── cme-miniapp.service        # Systemd-юнит для автозапуска и демонизации
├── nginx-miniapp.conf         # Шаблон конфига Nginx с HTTPS и WebSocket проксированием
├── requirements.txt           # Корневой список зависимостей
└── README.md                  # Документация проекта
```

---

## 🛠 Быстрый старт

### Требования
* Python 3.11+
* Git
* Chromium и Xvfb (для запуска парсера на Linux-сервере)

### 1. Клонирование и установка зависимостей
```bash
git clone https://github.com/your-username/cme-metals-terminal.git
cd cme-metals-terminal

python -m venv venv
# Linux / macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium
```

### 2. Настройка переменных окружения
Скопируйте шаблоны конфигурации:
```bash
cp .env.example .env
cp backend/cme_credentials.example.py backend/cme_credentials.py
```

Отредактируйте `.env`:
```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
WEBAPP_URL=https://your-domain.com
API_HOST=0.0.0.0
API_PORT=8080
UPDATE_INTERVAL_SECONDS=10
```

Укажите учетные данные CME в `backend/cme_credentials.py`:
```python
CME_LOGIN = "your_email@example.com"
CME_PASSWORD = "your_password"
```

### 3. Локальный запуск
```bash
cd backend
python run_all.py
```
Откройте браузер по адресу: `http://localhost:8080`

---

## 🤖 Команды Telegram-бота

| Команда | Описание |
| :--- | :--- |
| `/start` | Запуск бота, главное меню и кнопка открытия Mini App |
| `/oi` | Выгрузка отчета QuikStrike Most Actives (крупные контракты OI ≥ 1,000) |
| `/post` | Принудительная публикация аналитического отчета ТОП-5 в канал |
| `/update_oi` | Запуск парсера Playwright для принудительного обновления данных CME |
| `/channel` | Просмотр текущего привязанного канала и статуса публикаций |
| `/setchannel <id>` | Ручная привязка канала (или просто добавьте бота администратором в канал) |
| `/setcme <login> <pwd>` | Быстрая смена учетных данных CME прямо из переписки с ботом |
| `/quotes` | Текстовый список актуальных котировок металлов и валют |
| `/info` | Информация о сервере, статусе API и расписании |

---

## 🛰 Развертывание на VPS (Ubuntu 22.04 / 24.04)

### 1. Установка системных пакетов
```bash
sudo apt update && sudo apt install -y python3-venv python3-pip xvfb libxi6 libgconf-2-4 libnss3 libxss1 libasound2t64 nginx
```

### 2. Установка браузера Playwright
```bash
/opt/cme-metals-miniapp/venv/bin/playwright install --with-deps chromium
```

### 3. Настройка Systemd Service
Скопируйте `cme-miniapp.service` в `/etc/systemd/system/`:
```bash
sudo systemctl daemon-reload
sudo systemctl enable cme-miniapp
sudo systemctl restart cme-miniapp
sudo systemctl status cme-miniapp
```

### 4. Настройка Nginx и SSL
Используйте `nginx-miniapp.conf` и настройте бесплатный SSL-сертификат от Let's Encrypt через `certbot`:
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🔒 Безопасность

* Файлы с паролями и токенами (`.env`, `cme_credentials.py`, `channel_config.json`, `quikstrike_cache.json`) добавлены в `.gitignore` и никогда не попадают в репозиторий.
* Смена паролей доступна как в коде, так и через Telegram команду администратора.

---

## 📄 Лицензия

MIT License. Свободно для личного и коммерческого использования.
