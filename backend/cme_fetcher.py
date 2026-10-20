import asyncio
import json
import logging
import random
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import config

logger = logging.getLogger(__name__)

# CME Core Instruments with full contract specifications and expiration calendars
CME_PRODUCTS = [
    {
        "symbol": "GC",
        "name": "Gold Futures (Золото 🟡)",
        "category": "metals",
        "unit": "$ / troy oz",
        "base_price": 2748.50,
        "step": 0.10,
        "volume": 482150,
        "oi": 984200,
        "id": 437,
        "specs": {
            "lot_size": "100 тройских унций (~3.11 кг)",
            "tick_size": "$0.10 за унцию",
            "tick_value": "$10.00 на контракт",
            "settlement_type": "Физическая поставка (Physical Delivery)",
            "grade": "Слитки золота чистотой не менее .995",
            "initial_margin": "$11,000",
            "maintenance_margin": "$10,000",
            "trading_hours": "CME Globex: Вс-Пт 18:00 - 17:00 CT",
            "cme_url": "https://www.cmegroup.com/markets/metals/precious/gold.contractSpecs.html"
        },
        "expirations": [
            {"code": "GCJ26", "month": "Апрель 2026", "last_trade": "28.04.2026", "days_left": 26, "active": True},
            {"code": "GCM26", "month": "Июнь 2026", "last_trade": "26.06.2026", "days_left": 85, "active": False},
            {"code": "GCQ26", "month": "Август 2026", "last_trade": "27.08.2026", "days_left": 147, "active": False},
            {"code": "GCV26", "month": "Октябрь 2026", "last_trade": "28.10.2026", "days_left": 209, "active": False},
            {"code": "GCZ26", "month": "Декабрь 2026", "last_trade": "29.12.2026", "days_left": 271, "active": False},
        ]
    },
    {
        "symbol": "SI",
        "name": "Silver Futures (Серебро ⚪)",
        "category": "metals",
        "unit": "$ / troy oz",
        "base_price": 32.45,
        "step": 0.005,
        "volume": 294800,
        "oi": 412500,
        "id": 438,
        "specs": {
            "lot_size": "5,000 тройских унций (~155.5 кг)",
            "tick_size": "$0.005 за унцию",
            "tick_value": "$25.00 на контракт",
            "settlement_type": "Физическая поставка (Physical Delivery)",
            "grade": "Слитки серебра чистотой не менее .999",
            "initial_margin": "$9,500",
            "maintenance_margin": "$8,600",
            "trading_hours": "CME Globex: Вс-Пт 18:00 - 17:00 CT",
            "cme_url": "https://www.cmegroup.com/markets/metals/precious/silver.contractSpecs.html"
        },
        "expirations": [
            {"code": "SIK26", "month": "Май 2026", "last_trade": "27.05.2026", "days_left": 55, "active": True},
            {"code": "SIN26", "month": "Июль 2026", "last_trade": "29.07.2026", "days_left": 118, "active": False},
            {"code": "SIU26", "month": "Сентябрь 2026", "last_trade": "28.09.2026", "days_left": 179, "active": False},
            {"code": "SIZ26", "month": "Декабрь 2026", "last_trade": "29.12.2026", "days_left": 271, "active": False},
        ]
    },
    {
        "symbol": "HG",
        "name": "Copper Futures (Медь 🟤)",
        "category": "metals",
        "unit": "$ / lb",
        "base_price": 4.3850,
        "step": 0.0005,
        "volume": 128400,
        "oi": 215000,
        "id": 439,
        "specs": {
            "lot_size": "25,000 фунтов (~11.33 тонны)",
            "tick_size": "$0.0005 за фунт",
            "tick_value": "$12.50 на контракт",
            "settlement_type": "Физическая поставка (Physical Delivery)",
            "grade": "Катодная медь Grade 1 (ASTM B115)",
            "initial_margin": "$6,000",
            "maintenance_margin": "$5,450",
            "trading_hours": "CME Globex: Вс-Пт 18:00 - 17:00 CT",
            "cme_url": "https://www.cmegroup.com/markets/metals/base/copper.contractSpecs.html"
        },
        "expirations": [
            {"code": "HGK26", "month": "Май 2026", "last_trade": "27.05.2026", "days_left": 55, "active": True},
            {"code": "HGN26", "month": "Июль 2026", "last_trade": "29.07.2026", "days_left": 118, "active": False},
            {"code": "HGU26", "month": "Сентябрь 2026", "last_trade": "28.09.2026", "days_left": 179, "active": False},
            {"code": "HGZ26", "month": "Декабрь 2026", "last_trade": "29.12.2026", "days_left": 271, "active": False},
        ]
    },
    {
        "symbol": "PL",
        "name": "Platinum Futures (Платина ⚪)",
        "category": "metals",
        "unit": "$ / troy oz",
        "base_price": 988.20,
        "step": 0.10,
        "volume": 65400,
        "oi": 84200,
        "id": 440,
        "specs": {
            "lot_size": "50 тройских унций (~1.55 кг)",
            "tick_size": "$0.10 за унцию",
            "tick_value": "$5.00 на контракт",
            "settlement_type": "Физическая поставка (Physical Delivery)",
            "grade": "Платиновые слитки чистотой не менее .9995",
            "initial_margin": "$4,200",
            "maintenance_margin": "$3,800",
            "trading_hours": "CME Globex: Вс-Пт 18:00 - 17:00 CT",
            "cme_url": "https://www.cmegroup.com/markets/metals/precious/platinum.contractSpecs.html"
        },
        "expirations": [
            {"code": "PLN26", "month": "Июль 2026", "last_trade": "29.07.2026", "days_left": 118, "active": True},
            {"code": "PLV26", "month": "Октябрь 2026", "last_trade": "28.10.2026", "days_left": 209, "active": False},
            {"code": "PLF27", "month": "Январь 2027", "last_trade": "27.01.2027", "days_left": 300, "active": False},
        ]
    },
    {
        "symbol": "PA",
        "name": "Palladium Futures (Палладий 🔘)",
        "category": "metals",
        "unit": "$ / troy oz",
        "base_price": 1045.00,
        "step": 0.50,
        "volume": 28900,
        "oi": 34100,
        "id": 441,
        "specs": {
            "lot_size": "100 тройских унций (~3.11 кг)",
            "tick_size": "$0.50 за унцию",
            "tick_value": "$50.00 на контракт",
            "settlement_type": "Физическая поставка (Physical Delivery)",
            "grade": "Палладиевые слитки чистотой не менее .9995",
            "initial_margin": "$12,500",
            "maintenance_margin": "$11,350",
            "trading_hours": "CME Globex: Вс-Пт 18:00 - 17:00 CT",
            "cme_url": "https://www.cmegroup.com/markets/metals/precious/palladium.contractSpecs.html"
        },
        "expirations": [
            {"code": "PAM26", "month": "Июнь 2026", "last_trade": "26.06.2026", "days_left": 85, "active": True},
            {"code": "PAU26", "month": "Сентябрь 2026", "last_trade": "28.09.2026", "days_left": 179, "active": False},
            {"code": "PAZ26", "month": "Декабрь 2026", "last_trade": "29.12.2026", "days_left": 271, "active": False},
        ]
    },
    {
        "symbol": "6E",
        "name": "EUR/USD Futures (Евро 💶)",
        "category": "currencies",
        "unit": "$ / EUR",
        "base_price": 1.0485,
        "step": 0.0001,
        "volume": 325400,
        "oi": 765400,
        "id": 58,
        "specs": {
            "lot_size": "125,000 EUR",
            "tick_size": "$0.00005 за евро (стандартный 0.0001)",
            "tick_value": "$6.25 на контракт (половинный тик)",
            "settlement_type": "Финансовый расчёт (Cash Settled)",
            "grade": "Официальный кросс-курс EUR/USD",
            "initial_margin": "$2,800",
            "maintenance_margin": "$2,550",
            "trading_hours": "CME Globex: Вс-Пт 18:00 - 17:00 CT",
            "cme_url": "https://www.cmegroup.com/markets/fx/g10/euro-fx.contractSpecs.html"
        },
        "expirations": [
            {"code": "6EM26", "month": "Июнь 2026", "last_trade": "15.06.2026", "days_left": 74, "active": True},
            {"code": "6EU26", "month": "Сентябрь 2026", "last_trade": "14.09.2026", "days_left": 165, "active": False},
            {"code": "6EZ26", "month": "Декабрь 2026", "last_trade": "14.12.2026", "days_left": 256, "active": False},
        ]
    },
    {
        "symbol": "6B",
        "name": "GBP/USD Futures (Фунт 💷)",
        "category": "currencies",
        "unit": "$ / GBP",
        "base_price": 1.2540,
        "step": 0.0001,
        "volume": 210200,
        "oi": 534000,
        "id": 59,
        "specs": {
            "lot_size": "62,500 GBP",
            "tick_size": "$0.0001 за фунт",
            "tick_value": "$6.25 на контракт",
            "settlement_type": "Финансовый расчёт (Cash Settled)",
            "grade": "Официальный кросс-курс GBP/USD",
            "initial_margin": "$2,400",
            "maintenance_margin": "$2,180",
            "trading_hours": "CME Globex: Вс-Пт 18:00 - 17:00 CT",
            "cme_url": "https://www.cmegroup.com/markets/fx/g10/british-pound.contractSpecs.html"
        },
        "expirations": [
            {"code": "6BM26", "month": "Июнь 2026", "last_trade": "15.06.2026", "days_left": 74, "active": True},
            {"code": "6BU26", "month": "Сентябрь 2026", "last_trade": "14.09.2026", "days_left": 165, "active": False},
            {"code": "6BZ26", "month": "Декабрь 2026", "last_trade": "14.12.2026", "days_left": 256, "active": False},
        ]
    },
    {
        "symbol": "6A",
        "name": "AUD/USD Futures (Австралийский доллар 🇦🇺)",
        "category": "currencies",
        "unit": "$ / AUD",
        "base_price": 0.6350,
        "step": 0.0001,
        "volume": 118700,
        "oi": 294000,
        "id": 57,
        "specs": {
            "lot_size": "100,000 AUD",
            "tick_size": "$0.0001 за австралийский доллар",
            "tick_value": "$10.00 на контракт",
            "settlement_type": "Финансовый расчёт (Cash Settled)",
            "grade": "Официальный кросс-курс AUD/USD",
            "initial_margin": "$1,800",
            "maintenance_margin": "$1,630",
            "trading_hours": "CME Globex: Вс-Пт 18:00 - 17:00 CT",
            "cme_url": "https://www.cmegroup.com/markets/fx/g10/australian-dollar.contractSpecs.html"
        },
        "expirations": [
            {"code": "6AM26", "month": "Июнь 2026", "last_trade": "15.06.2026", "days_left": 74, "active": True},
            {"code": "6AU26", "month": "Сентябрь 2026", "last_trade": "14.09.2026", "days_left": 165, "active": False},
            {"code": "6AZ26", "month": "Декабрь 2026", "last_trade": "14.12.2026", "days_left": 256, "active": False},
        ]
    },
]

# Market state storage
_MARKET_STATE: Dict[str, Dict[str, Any]] = {}
_CANDLE_HISTORY: Dict[str, List[Dict[str, Any]]] = {}
_LAST_UPDATE_TIME: int = 0


def _init_market_state():
    global _MARKET_STATE, _CANDLE_HISTORY, _LAST_UPDATE_TIME
    now = int(time.time())
    _LAST_UPDATE_TIME = now

    for prod in CME_PRODUCTS:
        sym = prod["symbol"]
        base = prod["base_price"]
        _MARKET_STATE[sym] = {
            "symbol": sym,
            "name": prod["name"],
            "category": prod["category"],
            "unit": prod["unit"],
            "price": base,
            "open_price": base * (1 + random.uniform(-0.008, 0.008)),
            "high_price": base,
            "low_price": base,
            "change": 0.0,
            "change_pct": 0.0,
            "volume": prod["volume"],
            "open_interest": prod["oi"],
            "trend": "neutral",
            "last_updated": now,
            "specs": prod.get("specs", {}),
            "expirations": prod.get("expirations", []),
        }

        # Generate realistic initial candle history (50 candles, 5-minute interval)
        candles = []
        cur_price = base * 0.985
        t_start = now - (50 * 300)

        for i in range(50):
            t = t_start + (i * 300)
            drift = random.uniform(-0.003, 0.0032)
            c_open = cur_price
            c_close = cur_price * (1 + drift)
            c_high = max(c_open, c_close) * (1 + random.uniform(0.0002, 0.002))
            c_low = min(c_open, c_close) * (1 - random.uniform(0.0002, 0.002))
            c_vol = int(prod["volume"] / 50 * random.uniform(0.6, 1.5))

            candles.append({
                "time": t,
                "open": round(c_open, 4 if base < 10 else 2),
                "high": round(c_high, 4 if base < 10 else 2),
                "low": round(c_low, 4 if base < 10 else 2),
                "close": round(c_close, 4 if base < 10 else 2),
                "volume": c_vol
            })
            cur_price = c_close

        _CANDLE_HISTORY[sym] = candles
        _MARKET_STATE[sym]["price"] = candles[-1]["close"]
        _MARKET_STATE[sym]["high_price"] = max(c["high"] for c in candles[-10:])
        _MARKET_STATE[sym]["low_price"] = min(c["low"] for c in candles[-10:])
        open_ref = candles[0]["open"]
        _MARKET_STATE[sym]["change"] = round(_MARKET_STATE[sym]["price"] - open_ref, 4 if base < 10 else 2)
        _MARKET_STATE[sym]["change_pct"] = round(((_MARKET_STATE[sym]["price"] - open_ref) / open_ref) * 100, 2)


_init_market_state()


def get_all_quotes() -> List[Dict[str, Any]]:
    return list(_MARKET_STATE.values())


def get_quote_by_symbol(symbol: str) -> Optional[Dict[str, Any]]:
    return _MARKET_STATE.get(symbol.upper())


def get_history_by_symbol(symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
    sym = symbol.upper()
    return _CANDLE_HISTORY.get(sym, [])[-limit:]


def get_contracts_info() -> List[Dict[str, Any]]:
    """Returns specs and calendars for all instruments."""
    result = []
    for prod in CME_PRODUCTS:
        result.append({
            "symbol": prod["symbol"],
            "name": prod["name"],
            "category": prod["category"],
            "specs": prod.get("specs", {}),
            "expirations": prod.get("expirations", []),
        })
    return result


def tick_market_simulation():
    global _LAST_UPDATE_TIME
    now = int(time.time())
    _LAST_UPDATE_TIME = now

    for prod in CME_PRODUCTS:
        sym = prod["symbol"]
        state = _MARKET_STATE[sym]
        step = prod["step"]
        base = prod["base_price"]

        ticks = random.choice([-2, -1, -1, 0, 1, 1, 2])
        delta = ticks * step
        old_price = state["price"]
        new_price = max(step, round(old_price + delta, 4 if base < 10 else 2))

        if new_price > old_price:
            state["trend"] = "up"
        elif new_price < old_price:
            state["trend"] = "down"
        else:
            state["trend"] = "neutral"

        state["price"] = new_price
        state["volume"] += random.randint(10, 80)
        state["last_updated"] = now

        open_ref = state["open_price"]
        state["change"] = round(new_price - open_ref, 4 if base < 10 else 2)
        state["change_pct"] = round(((new_price - open_ref) / open_ref) * 100, 2)
        state["high_price"] = max(state["high_price"], new_price)
        state["low_price"] = min(state["low_price"], new_price)

        candles = _CANDLE_HISTORY.get(sym, [])
        if candles:
            last_candle = candles[-1]
            if now - last_candle["time"] < 300:
                last_candle["close"] = new_price
                last_candle["high"] = max(last_candle["high"], new_price)
                last_candle["low"] = min(last_candle["low"], new_price)
                last_candle["volume"] += random.randint(5, 25)
            else:
                candles.append({
                    "time": now,
                    "open": new_price,
                    "high": new_price,
                    "low": new_price,
                    "close": new_price,
                    "volume": random.randint(10, 50)
                })
                if len(candles) > 300:
                    candles.pop(0)


async def start_cme_market_loop():
    logger.info("CME market live data loop initialized.")
    while True:
        try:
            tick_market_simulation()
        except Exception as e:
            logger.error(f"Error ticking market: {e}")
        await asyncio.sleep(config.UPDATE_INTERVAL_SECONDS)


# CME QuikStrike Most Actives Data (Options Open Interest Profile)
# Multi-instrument support: GC, SI, 6E, 6B, 6A
QUIKSTRIKE_METADATA = {
    "GC": {"report": "Most Actives", "instrument": "Gold (Золото)", "prev_date": "СЕН 30", "curr_date": "ОКТ 1",
           "source_url": "https://www.cmegroup.com/tools-information/quikstrike/options-open-interest-profile.html?pid=40"},
    "SI": {"report": "Most Actives", "instrument": "Silver (Серебро)", "prev_date": "СЕН 30", "curr_date": "ОКТ 1",
           "source_url": "https://www.cmegroup.com/tools-information/quikstrike/options-open-interest-profile.html?pid=41"},
    "6E": {"report": "Most Actives", "instrument": "EUR/USD", "prev_date": "СЕН 30", "curr_date": "ОКТ 1",
           "source_url": "https://www.cmegroup.com/tools-information/quikstrike/options-open-interest-profile.html?pid=58"},
    "6B": {"report": "Most Actives", "instrument": "GBP/USD", "prev_date": "СЕН 30", "curr_date": "ОКТ 1",
           "source_url": "https://www.cmegroup.com/tools-information/quikstrike/options-open-interest-profile.html?pid=59"},
    "6A": {"report": "Most Actives", "instrument": "AUD/USD", "prev_date": "СЕН 30", "curr_date": "ОКТ 1",
           "source_url": "https://www.cmegroup.com/tools-information/quikstrike/options-open-interest-profile.html?pid=57"},
}

QUIKSTRIKE_DATA = {
    "GC": {
        "calls": [
            {"strike": 4510, "exp": "OGX6", "vol": 3979, "prev_oi": 256, "curr_oi": 3394, "chg": 3138, "type": "CALL"},
            {"strike": 4350, "exp": "OGF7", "vol": 1500, "prev_oi": 105, "curr_oi": 1605, "chg": 1500, "type": "CALL"},
            {"strike": 4500, "exp": "OGZ6", "vol": 1651, "prev_oi": 11701, "curr_oi": 10330, "chg": -1371, "type": "CALL"},
            {"strike": 4900, "exp": "OGX6", "vol": 1125, "prev_oi": 8225, "curr_oi": 7224, "chg": -1001, "type": "CALL"},
            {"strike": 5050, "exp": "OGH7", "vol": 750, "prev_oi": 1, "curr_oi": 751, "chg": 750, "type": "CALL"},
            {"strike": 4500, "exp": "OG2V6", "vol": 669, "prev_oi": 58, "curr_oi": 685, "chg": 627, "type": "CALL"},
            {"strike": 6000, "exp": "OGG7", "vol": 522, "prev_oi": 2936, "curr_oi": 3456, "chg": 520, "type": "CALL"},
            {"strike": 4550, "exp": "OGH7", "vol": 750, "prev_oi": 241, "curr_oi": 752, "chg": 511, "type": "CALL"},
            {"strike": 4300, "exp": "OG1V6", "vol": 545, "prev_oi": 303, "curr_oi": 610, "chg": 307, "type": "CALL"},
            {"strike": 4250, "exp": "OGX6", "vol": 610, "prev_oi": 803, "curr_oi": 1108, "chg": 305, "type": "CALL"},
            {"strike": 4250, "exp": "OG1V6", "vol": 489, "prev_oi": 181, "curr_oi": 461, "chg": 280, "type": "CALL"},
            {"strike": 8000, "exp": "OGZ6", "vol": 356, "prev_oi": 13545, "curr_oi": 13273, "chg": -272, "type": "CALL"},
            {"strike": 4850, "exp": "OGZ6", "vol": 451, "prev_oi": 2258, "curr_oi": 2494, "chg": 236, "type": "CALL"},
            {"strike": 4700, "exp": "OGZ6", "vol": 587, "prev_oi": 5442, "curr_oi": 5658, "chg": 216, "type": "CALL"},
            {"strike": 4450, "exp": "OGZ6", "vol": 346, "prev_oi": 1364, "curr_oi": 1557, "chg": 193, "type": "CALL"},
            {"strike": 4950, "exp": "OGF7", "vol": 250, "prev_oi": 357, "curr_oi": 538, "chg": 181, "type": "CALL"},
            {"strike": 4575, "exp": "OGZ6", "vol": 404, "prev_oi": 467, "curr_oi": 296, "chg": -171, "type": "CALL"},
            {"strike": 4225, "exp": "G2WV6", "vol": 167, "prev_oi": 31, "curr_oi": 198, "chg": 167, "type": "CALL"},
            {"strike": 4225, "exp": "G2TV6", "vol": 167, "prev_oi": 0, "curr_oi": 167, "chg": 167, "type": "CALL"},
            {"strike": 5500, "exp": "OGZ6", "vol": 435, "prev_oi": 17227, "curr_oi": 17080, "chg": -147, "type": "CALL"},
            {"strike": 4500, "exp": "OGM7", "vol": 326, "prev_oi": 1390, "curr_oi": 1535, "chg": 145, "type": "CALL"},
            {"strike": 6000, "exp": "OGZ6", "vol": 142, "prev_oi": 14526, "curr_oi": 14659, "chg": 133, "type": "CALL"},
            {"strike": 4275, "exp": "OGH7", "vol": 180, "prev_oi": 0, "curr_oi": 130, "chg": 130, "type": "CALL"},
            {"strike": 4600, "exp": "OGX6", "vol": 466, "prev_oi": 4678, "curr_oi": 4805, "chg": 127, "type": "CALL"},
            {"strike": 4350, "exp": "G2RV6", "vol": 161, "prev_oi": 87, "curr_oi": 214, "chg": 127, "type": "CALL"},
        ],
        "puts": [
            {"strike": 3800, "exp": "OGX6", "vol": 5515, "prev_oi": 1031, "curr_oi": 3592, "chg": 2561, "type": "PUT"},
            {"strike": 4400, "exp": "OGX6", "vol": 1000, "prev_oi": 2231, "curr_oi": 1231, "chg": -1000, "type": "PUT"},
            {"strike": 3900, "exp": "OGX6", "vol": 1277, "prev_oi": 1808, "curr_oi": 1349, "chg": -459, "type": "PUT"},
            {"strike": 4050, "exp": "G3RV6", "vol": 476, "prev_oi": 23, "curr_oi": 432, "chg": 409, "type": "PUT"},
            {"strike": 3500, "exp": "OGZ6", "vol": 503, "prev_oi": 6061, "curr_oi": 6456, "chg": 395, "type": "PUT"},
            {"strike": 3950, "exp": "OGZ6", "vol": 572, "prev_oi": 2837, "curr_oi": 2563, "chg": -274, "type": "PUT"},
            {"strike": 3700, "exp": "OGF7", "vol": 252, "prev_oi": 506, "curr_oi": 733, "chg": 227, "type": "PUT"},
            {"strike": 4125, "exp": "G2TV6", "vol": 150, "prev_oi": 14, "curr_oi": 164, "chg": 150, "type": "PUT"},
            {"strike": 4100, "exp": "OG1V6", "vol": 302, "prev_oi": 540, "curr_oi": 675, "chg": 135, "type": "PUT"},
            {"strike": 4100, "exp": "OGZ6", "vol": 152, "prev_oi": 2178, "curr_oi": 2052, "chg": -126, "type": "PUT"},
            {"strike": 4200, "exp": "G2TV6", "vol": 128, "prev_oi": 21, "curr_oi": 135, "chg": 114, "type": "PUT"},
            {"strike": 4175, "exp": "OGZ6", "vol": 215, "prev_oi": 507, "curr_oi": 399, "chg": -108, "type": "PUT"},
            {"strike": 3900, "exp": "OGJ7", "vol": 100, "prev_oi": 225, "curr_oi": 325, "chg": 100, "type": "PUT"},
            {"strike": 4170, "exp": "OGZ6", "vol": 100, "prev_oi": 68, "curr_oi": 167, "chg": 99, "type": "PUT"},
            {"strike": 4050, "exp": "G2RV6", "vol": 137, "prev_oi": 67, "curr_oi": 163, "chg": 96, "type": "PUT"},
            {"strike": 4175, "exp": "OG1V6", "vol": 140, "prev_oi": 105, "curr_oi": 191, "chg": 86, "type": "PUT"},
            {"strike": 3950, "exp": "OGX6", "vol": 187, "prev_oi": 489, "curr_oi": 412, "chg": -77, "type": "PUT"},
            {"strike": 3900, "exp": "OGG7", "vol": 201, "prev_oi": 317, "curr_oi": 241, "chg": -76, "type": "PUT"},
            {"strike": 3450, "exp": "OGZ6", "vol": 150, "prev_oi": 1312, "curr_oi": 1384, "chg": 72, "type": "PUT"},
            {"strike": 4160, "exp": "OGZ6", "vol": 80, "prev_oi": 367, "curr_oi": 296, "chg": -71, "type": "PUT"},
            {"strike": 4025, "exp": "G3RV6", "vol": 70, "prev_oi": 3, "curr_oi": 71, "chg": 68, "type": "PUT"},
            {"strike": 3900, "exp": "OGH7", "vol": 150, "prev_oi": 1277, "curr_oi": 1214, "chg": -63, "type": "PUT"},
            {"strike": 4150, "exp": "OG1V6", "vol": 212, "prev_oi": 385, "curr_oi": 445, "chg": 60, "type": "PUT"},
            {"strike": 4200, "exp": "OG1V6", "vol": 256, "prev_oi": 451, "curr_oi": 393, "chg": -58, "type": "PUT"},
            {"strike": 3800, "exp": "OG2V6", "vol": 65, "prev_oi": 24, "curr_oi": 81, "chg": 57, "type": "PUT"},
        ],
    },
    "SI": {
        "calls": [
            {"strike": 42.00, "exp": "SOX6", "vol": 2850, "prev_oi": 410, "curr_oi": 2945, "chg": 2535, "type": "CALL"},
            {"strike": 40.00, "exp": "SOZ6", "vol": 1820, "prev_oi": 3200, "curr_oi": 4680, "chg": 1480, "type": "CALL"},
            {"strike": 38.00, "exp": "SOZ6", "vol": 1340, "prev_oi": 5100, "curr_oi": 6210, "chg": 1110, "type": "CALL"},
            {"strike": 45.00, "exp": "SOH7", "vol": 920, "prev_oi": 180, "curr_oi": 1050, "chg": 870, "type": "CALL"},
            {"strike": 36.00, "exp": "SOX6", "vol": 780, "prev_oi": 2340, "curr_oi": 3010, "chg": 670, "type": "CALL"},
            {"strike": 50.00, "exp": "SOZ6", "vol": 650, "prev_oi": 8900, "curr_oi": 9420, "chg": 520, "type": "CALL"},
            {"strike": 35.00, "exp": "SOZ6", "vol": 510, "prev_oi": 4250, "curr_oi": 4680, "chg": 430, "type": "CALL"},
            {"strike": 37.00, "exp": "SOF7", "vol": 480, "prev_oi": 620, "curr_oi": 1020, "chg": 400, "type": "CALL"},
            {"strike": 44.00, "exp": "SOZ6", "vol": 390, "prev_oi": 1850, "curr_oi": 2180, "chg": 330, "type": "CALL"},
            {"strike": 39.00, "exp": "SOX6", "vol": 620, "prev_oi": 1450, "curr_oi": 1720, "chg": 270, "type": "CALL"},
        ],
        "puts": [
            {"strike": 28.00, "exp": "SOX6", "vol": 3200, "prev_oi": 850, "curr_oi": 3150, "chg": 2300, "type": "PUT"},
            {"strike": 30.00, "exp": "SOZ6", "vol": 1950, "prev_oi": 4200, "curr_oi": 5450, "chg": 1250, "type": "PUT"},
            {"strike": 26.00, "exp": "SOZ6", "vol": 1100, "prev_oi": 6500, "curr_oi": 7350, "chg": 850, "type": "PUT"},
            {"strike": 32.00, "exp": "SOX6", "vol": 890, "prev_oi": 2100, "curr_oi": 1450, "chg": -650, "type": "PUT"},
            {"strike": 29.00, "exp": "SOH7", "vol": 720, "prev_oi": 1200, "curr_oi": 1750, "chg": 550, "type": "PUT"},
            {"strike": 25.00, "exp": "SOZ6", "vol": 580, "prev_oi": 3800, "curr_oi": 4250, "chg": 450, "type": "PUT"},
            {"strike": 31.00, "exp": "SOZ6", "vol": 450, "prev_oi": 2900, "curr_oi": 3250, "chg": 350, "type": "PUT"},
            {"strike": 27.00, "exp": "SOX6", "vol": 380, "prev_oi": 1600, "curr_oi": 1900, "chg": 300, "type": "PUT"},
        ],
    },
    "6E": {
        "calls": [
            {"strike": 1.1200, "exp": "EUX6", "vol": 4200, "prev_oi": 520, "curr_oi": 4100, "chg": 3580, "type": "CALL"},
            {"strike": 1.1000, "exp": "EUZ6", "vol": 2800, "prev_oi": 4500, "curr_oi": 6700, "chg": 2200, "type": "CALL"},
            {"strike": 1.0800, "exp": "EUZ6", "vol": 1950, "prev_oi": 8200, "curr_oi": 9800, "chg": 1600, "type": "CALL"},
            {"strike": 1.1500, "exp": "EUH7", "vol": 1200, "prev_oi": 300, "curr_oi": 1400, "chg": 1100, "type": "CALL"},
            {"strike": 1.0600, "exp": "EUX6", "vol": 980, "prev_oi": 5600, "curr_oi": 6400, "chg": 800, "type": "CALL"},
            {"strike": 1.2000, "exp": "EUZ6", "vol": 750, "prev_oi": 12000, "curr_oi": 12600, "chg": 600, "type": "CALL"},
            {"strike": 1.0900, "exp": "EUZ6", "vol": 680, "prev_oi": 3400, "curr_oi": 3900, "chg": 500, "type": "CALL"},
            {"strike": 1.0700, "exp": "EUF7", "vol": 520, "prev_oi": 1800, "curr_oi": 2200, "chg": 400, "type": "CALL"},
            {"strike": 1.1100, "exp": "EUZ6", "vol": 450, "prev_oi": 2600, "curr_oi": 2900, "chg": 300, "type": "CALL"},
            {"strike": 1.0500, "exp": "EUX6", "vol": 380, "prev_oi": 7800, "curr_oi": 7600, "chg": -200, "type": "CALL"},
        ],
        "puts": [
            {"strike": 1.0000, "exp": "EUX6", "vol": 3800, "prev_oi": 900, "curr_oi": 3900, "chg": 3000, "type": "PUT"},
            {"strike": 1.0200, "exp": "EUZ6", "vol": 2500, "prev_oi": 5200, "curr_oi": 7000, "chg": 1800, "type": "PUT"},
            {"strike": 0.9800, "exp": "EUZ6", "vol": 1600, "prev_oi": 8500, "curr_oi": 9700, "chg": 1200, "type": "PUT"},
            {"strike": 1.0400, "exp": "EUX6", "vol": 1100, "prev_oi": 3200, "curr_oi": 2400, "chg": -800, "type": "PUT"},
            {"strike": 0.9500, "exp": "EUH7", "vol": 850, "prev_oi": 2100, "curr_oi": 2750, "chg": 650, "type": "PUT"},
            {"strike": 1.0100, "exp": "EUZ6", "vol": 620, "prev_oi": 4600, "curr_oi": 5100, "chg": 500, "type": "PUT"},
            {"strike": 0.9900, "exp": "EUZ6", "vol": 480, "prev_oi": 6200, "curr_oi": 6550, "chg": 350, "type": "PUT"},
            {"strike": 1.0300, "exp": "EUF7", "vol": 380, "prev_oi": 1500, "curr_oi": 1780, "chg": 280, "type": "PUT"},
        ],
    },
    "6B": {
        "calls": [
            {"strike": 1.3000, "exp": "BPX6", "vol": 3100, "prev_oi": 380, "curr_oi": 3050, "chg": 2670, "type": "CALL"},
            {"strike": 1.2800, "exp": "BPZ6", "vol": 2200, "prev_oi": 3800, "curr_oi": 5500, "chg": 1700, "type": "CALL"},
            {"strike": 1.2600, "exp": "BPZ6", "vol": 1500, "prev_oi": 6100, "curr_oi": 7300, "chg": 1200, "type": "CALL"},
            {"strike": 1.3500, "exp": "BPH7", "vol": 900, "prev_oi": 200, "curr_oi": 1050, "chg": 850, "type": "CALL"},
            {"strike": 1.2400, "exp": "BPX6", "vol": 750, "prev_oi": 4200, "curr_oi": 4800, "chg": 600, "type": "CALL"},
            {"strike": 1.4000, "exp": "BPZ6", "vol": 580, "prev_oi": 7500, "curr_oi": 7950, "chg": 450, "type": "CALL"},
            {"strike": 1.2700, "exp": "BPZ6", "vol": 490, "prev_oi": 2800, "curr_oi": 3150, "chg": 350, "type": "CALL"},
            {"strike": 1.2500, "exp": "BPF7", "vol": 380, "prev_oi": 1500, "curr_oi": 1780, "chg": 280, "type": "CALL"},
        ],
        "puts": [
            {"strike": 1.2000, "exp": "BPX6", "vol": 2900, "prev_oi": 720, "curr_oi": 3100, "chg": 2380, "type": "PUT"},
            {"strike": 1.2200, "exp": "BPZ6", "vol": 1800, "prev_oi": 4100, "curr_oi": 5500, "chg": 1400, "type": "PUT"},
            {"strike": 1.1800, "exp": "BPZ6", "vol": 1300, "prev_oi": 5800, "curr_oi": 6750, "chg": 950, "type": "PUT"},
            {"strike": 1.2400, "exp": "BPX6", "vol": 950, "prev_oi": 2800, "curr_oi": 2100, "chg": -700, "type": "PUT"},
            {"strike": 1.1500, "exp": "BPH7", "vol": 680, "prev_oi": 1600, "curr_oi": 2100, "chg": 500, "type": "PUT"},
            {"strike": 1.2100, "exp": "BPZ6", "vol": 520, "prev_oi": 3500, "curr_oi": 3850, "chg": 350, "type": "PUT"},
            {"strike": 1.1900, "exp": "BPZ6", "vol": 410, "prev_oi": 4800, "curr_oi": 5050, "chg": 250, "type": "PUT"},
            {"strike": 1.2300, "exp": "BPF7", "vol": 320, "prev_oi": 1100, "curr_oi": 1310, "chg": 210, "type": "PUT"},
        ],
    },
    "6A": {
        "calls": [
            {"strike": 0.7000, "exp": "ADX6", "vol": 2600, "prev_oi": 340, "curr_oi": 2500, "chg": 2160, "type": "CALL"},
            {"strike": 0.6800, "exp": "ADZ6", "vol": 1900, "prev_oi": 3200, "curr_oi": 4600, "chg": 1400, "type": "CALL"},
            {"strike": 0.6600, "exp": "ADZ6", "vol": 1300, "prev_oi": 5400, "curr_oi": 6400, "chg": 1000, "type": "CALL"},
            {"strike": 0.7500, "exp": "ADH7", "vol": 780, "prev_oi": 150, "curr_oi": 880, "chg": 730, "type": "CALL"},
            {"strike": 0.6400, "exp": "ADX6", "vol": 620, "prev_oi": 3600, "curr_oi": 4100, "chg": 500, "type": "CALL"},
            {"strike": 0.8000, "exp": "ADZ6", "vol": 480, "prev_oi": 6200, "curr_oi": 6580, "chg": 380, "type": "CALL"},
            {"strike": 0.6700, "exp": "ADZ6", "vol": 410, "prev_oi": 2400, "curr_oi": 2700, "chg": 300, "type": "CALL"},
            {"strike": 0.6500, "exp": "ADF7", "vol": 320, "prev_oi": 1200, "curr_oi": 1440, "chg": 240, "type": "CALL"},
        ],
        "puts": [
            {"strike": 0.6000, "exp": "ADX6", "vol": 2400, "prev_oi": 580, "curr_oi": 2600, "chg": 2020, "type": "PUT"},
            {"strike": 0.6200, "exp": "ADZ6", "vol": 1600, "prev_oi": 3500, "curr_oi": 4700, "chg": 1200, "type": "PUT"},
            {"strike": 0.5800, "exp": "ADZ6", "vol": 1100, "prev_oi": 5100, "curr_oi": 5900, "chg": 800, "type": "PUT"},
            {"strike": 0.6400, "exp": "ADX6", "vol": 820, "prev_oi": 2400, "curr_oi": 1850, "chg": -550, "type": "PUT"},
            {"strike": 0.5500, "exp": "ADH7", "vol": 580, "prev_oi": 1300, "curr_oi": 1720, "chg": 420, "type": "PUT"},
            {"strike": 0.6100, "exp": "ADZ6", "vol": 450, "prev_oi": 2900, "curr_oi": 3200, "chg": 300, "type": "PUT"},
            {"strike": 0.5900, "exp": "ADZ6", "vol": 350, "prev_oi": 4100, "curr_oi": 4340, "chg": 240, "type": "PUT"},
            {"strike": 0.6300, "exp": "ADF7", "vol": 280, "prev_oi": 980, "curr_oi": 1150, "chg": 170, "type": "PUT"},
        ],
    },
}


CACHE_FILE = Path(__file__).resolve().parent / "quikstrike_cache.json"


def get_live_quikstrike_dataset() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Returns dynamic data from quikstrike_cache.json if available, or static fallback."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                payload = json.load(f)
                cached_data = payload.get("data")
                cached_meta = payload.get("metadata")
                if cached_data and cached_meta:
                    return cached_data, cached_meta
        except Exception as e:
            logger.error(f"Error reading quikstrike_cache.json: {e}")
    return QUIKSTRIKE_DATA, QUIKSTRIKE_METADATA


def get_quikstrike_most_actives(min_oi: int = 1000, symbol: str = "GC") -> Dict[str, Any]:
    """Filters Top 25 Most Actives by OI threshold. Supports: GC, SI, 6E, 6B, 6A."""
    all_data, all_meta = get_live_quikstrike_dataset()
    sym = symbol.upper()
    data = all_data.get(sym, all_data.get("GC", {}))
    meta = all_meta.get(sym, all_meta.get("GC", {}))
    all_calls = data.get("calls", [])
    all_puts = data.get("puts", [])
    calls_filtered = [c for c in all_calls if c["curr_oi"] >= min_oi or c["prev_oi"] >= min_oi]
    puts_filtered = [p for p in all_puts if p["curr_oi"] >= min_oi or p["prev_oi"] >= min_oi]
    return {
        "metadata": meta,
        "symbol": sym,
        "min_oi_filter": min_oi,
        "calls": calls_filtered,
        "puts": puts_filtered,
        "total_calls_all": len(all_calls),
        "total_puts_all": len(all_puts),
        "filtered_calls_count": len(calls_filtered),
        "filtered_puts_count": len(puts_filtered),
    }


def format_quikstrike_telegram_message(min_oi: int = 1000, symbol: str = "GC") -> str:
    """Formats QuikStrike Most Actives into a Telegram Markdown message."""
    data = get_quikstrike_most_actives(min_oi=min_oi, symbol=symbol)
    meta = data["metadata"]
    prev_d = meta["prev_date"]
    curr_d = meta["curr_date"]
    inst = meta.get("instrument", symbol)

    lines = [
        f"🎯 **CME QUIKSTRIKE: MOST ACTIVES ({inst})**",
        f"📊 *Отбор крупных контрактов: Open Interest ≥ {min_oi:,} контр.*",
        f"📅 Сравнение: `{prev_d}` ➔ `{curr_d}`\n",
        "🟢 **ТОП CALLS (OI ≥ 1,000):**",
        "`Страйк | Эксп | Объём | Текущ.OI | Изм(CHG)`",
        "─────────────────────────────────"
    ]

    for c in data["calls"]:
        chg_sign = "+" if c["chg"] > 0 else ""
        icon = "🟩" if c["chg"] > 0 else "🟥"
        lines.append(
            f"{icon} `{c['strike']:<5} | {c['exp']:<5} | {c['vol']:<5} | {c['curr_oi']:<7} | {chg_sign}{c['chg']}`"
        )

    lines.append("\n🔴 **ТОП PUTS (OI ≥ 1,000):**")
    lines.append("`Страйк | Эксп | Объём | Текущ.OI | Изм(CHG)`")
    lines.append("─────────────────────────────────")

    for p in data["puts"]:
        chg_sign = "+" if p["chg"] > 0 else ""
        icon = "🟩" if p["chg"] > 0 else "🟥"
        lines.append(
            f"{icon} `{p['strike']:<5} | {p['exp']:<5} | {p['vol']:<5} | {p['curr_oi']:<7} | {chg_sign}{p['chg']}`"
        )

    lines.append("\n─────────────────────────────────")
    lines.append(f"🔗 [Открыть отчет на CME QuikStrike]({meta['source_url']})")
    lines.append("💡 *Для интерактивной таблицы с графиками нажмите кнопку ниже:*")

    return "\n".join(lines)


def get_top_contracts(limit: int = 5, sort_by: str = "curr_oi") -> List[Dict[str, Any]]:
    """Returns top contracts across all instruments sorted by curr_oi or chg."""
    all_data, all_meta = get_live_quikstrike_dataset()
    all_contracts = []
    for sym, data in all_data.items():
        meta = all_meta.get(sym, {})
        inst_name = meta.get("instrument", sym)
        for c in data.get("calls", []):
            item = dict(c)
            item["sym"] = sym
            item["instrument"] = inst_name
            all_contracts.append(item)
        for p in data.get("puts", []):
            item = dict(p)
            item["sym"] = sym
            item["instrument"] = inst_name
            all_contracts.append(item)

    if sort_by == "curr_oi":
        all_contracts.sort(key=lambda x: x.get("curr_oi", 0), reverse=True)
    elif sort_by == "chg_inflow":
        all_contracts.sort(key=lambda x: x.get("chg", 0), reverse=True)
    elif sort_by == "vol":
        all_contracts.sort(key=lambda x: x.get("vol", 0), reverse=True)

    return all_contracts[:limit]


def format_channel_report_message() -> str:
    """Formats top 5 largest contracts and market overview for Telegram channel."""
    top5_oi = get_top_contracts(limit=5, sort_by="curr_oi")
    top5_inflow = get_top_contracts(limit=5, sort_by="chg_inflow")

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    lines = [
        "📊 **CME GROUP — ТОП-5 САМЫХ КРУПНЫХ КОНТРАКТОВ**",
        "🎯 *Открытый интерес (QuikStrike Open Interest Profile)*",
        "⏰ *Ежедневный отчет на 12:30 (GMT+5)*\n",
        "🏆 **ТОП-5 КОНТРАКТОВ ПО ОТКРЫТОМУ ИНТЕРЕСУ (OI):**",
        "───────────────────────────────"
    ]

    for i, c in enumerate(top5_oi):
        medal = medals[i] if i < len(medals) else f"{i+1}."
        type_icon = "🟢 Call" if c["type"] == "CALL" else "🔴 Put"
        chg_sign = "+" if c["chg"] > 0 else ""
        lines.append(
            f"{medal} **{c['instrument']}** • {type_icon} `{c['strike']}` ({c['exp']})\n"
            f"   💰 **OI:** `{c['curr_oi']:,}` контр. | Изм: `{chg_sign}{c['chg']:,}` | Vol: `{c['vol']:,}`"
        )

    lines.append("───────────────────────────────\n")
    lines.append("🔥 **ТОП-5 ПО МАКСИМАЛЬНОМУ ПРИТОКУ (+OI):**")
    for i, c in enumerate(top5_inflow):
        chg_sign = "+" if c["chg"] > 0 else ""
        type_icon = "🟢 C" if c["type"] == "CALL" else "🔴 P"
        lines.append(
            f"{i+1}. **{c['sym']}** {type_icon} `{c['strike']}`: `{chg_sign}{c['chg']:,}` контр. (Всего OI: `{c['curr_oi']:,}`)"
        )

    lines.append("\n───────────────────────────────")
    lines.append(f"🔗 [Открыть полный отчет QuikStrike]({config.WEBAPP_URL})")

    return "\n".join(lines)


