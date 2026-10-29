# -*- coding: utf-8 -*-
"""
CME Market Data Fetcher & Aggregator.
Handles live quote simulation, QuikStrike cache retrieval, and Telegram report formatting.
"""
import asyncio
import json
import logging
import random
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import config
from cme_products import CME_PRODUCTS
from quikstrike_defaults import QUIKSTRIKE_DATA, QUIKSTRIKE_METADATA

logger = logging.getLogger(__name__)

# Cache file path
CACHE_FILE = Path(__file__).resolve().parent / "quikstrike_cache.json"

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
    """Returns current prices and statistics for all CME products."""
    return list(_MARKET_STATE.values())


def get_quote_by_symbol(symbol: str) -> Optional[Dict[str, Any]]:
    """Returns quote data for a single instrument."""
    return _MARKET_STATE.get(symbol.upper())


def get_history_by_symbol(symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Returns candle history for a single instrument."""
    sym = symbol.upper()
    return _CANDLE_HISTORY.get(sym, [])[-limit:]


def get_contracts_info() -> List[Dict[str, Any]]:
    """Returns specs and expiration calendars for all CME products."""
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
    """Generates realistic market price movements and updates candles."""
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
    """Background task to tick market prices at UPDATE_INTERVAL_SECONDS."""
    logger.info("CME market live data loop initialized.")
    while True:
        try:
            tick_market_simulation()
        except Exception as e:
            logger.error(f"Error ticking market: {e}")
        await asyncio.sleep(config.UPDATE_INTERVAL_SECONDS)


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


def get_default_min_oi(symbol: str) -> int:
    """Returns default OI threshold: 500 for Silver (SI), 1000 for Gold and FX."""
    return 500 if symbol.upper() == "SI" else 1000


def get_quikstrike_most_actives(min_oi: Optional[int] = None, symbol: str = "GC") -> Dict[str, Any]:
    """Filters Top 25 Most Actives by OI threshold. Supports: GC, SI, 6E, 6B, 6A."""
    all_data, all_meta = get_live_quikstrike_dataset()
    sym = symbol.upper()
    if min_oi is None:
        min_oi = get_default_min_oi(sym)
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


def format_quikstrike_telegram_message(min_oi: Optional[int] = None, symbol: str = "GC") -> str:
    """Formats QuikStrike Most Actives into a Telegram Markdown message."""
    if min_oi is None:
        min_oi = get_default_min_oi(symbol)
    data = get_quikstrike_most_actives(min_oi=min_oi, symbol=symbol)
    meta = data["metadata"]
    prev_d = meta["prev_date"]
    curr_d = meta["curr_date"]
    inst = meta.get("instrument", symbol)

    lines = [
        f"🎯 **CME QUIKSTRIKE: MOST ACTIVES ({inst})**",
        f"📊 *Отбор крупных контрактов: Open Interest ≥ {min_oi:,} контр.*",
        f"📅 Сравнение: `{prev_d}` ➔ `{curr_d}`\n",
        f"🟢 **ТОП CALLS (OI ≥ {min_oi:,}):**",
        "`Страйк | Эксп | Объём | Текущ.OI | Изм(CHG)`",
        "─────────────────────────────────"
    ]

    for c in data["calls"]:
        chg_sign = "+" if c["chg"] > 0 else ""
        icon = "🟩" if c["chg"] > 0 else "🟥"
        lines.append(
            f"{icon} `{c['strike']:<5} | {c['exp']:<5} | {c['vol']:<5} | {c['curr_oi']:<7} | {chg_sign}{c['chg']}`"
        )

    lines.append(f"\n🔴 **ТОП PUTS (OI ≥ {min_oi:,}):**")
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
        "⏰ *Ежедневный отчет на 09:30 (МСК)*\n",
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
