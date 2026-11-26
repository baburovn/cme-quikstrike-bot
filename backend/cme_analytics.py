# -*- coding: utf-8 -*-
"""
CME QuikStrike Options Analytics & Sentiment Engine.
Algorithmic analysis (Option Greeks / Put-Call Dynamics / ITM-OTM Moneyness / Key Levels)
without external third-party APIs.
"""
from datetime import datetime, timezone, timedelta
import re
from typing import Dict, Any, List, Optional, Tuple

TZ_MSK = timezone(timedelta(hours=3))

CME_MONTH_CODES = {
    "F": 1, "G": 2, "H": 3, "J": 4, "K": 5, "M": 6,
    "N": 7, "Q": 8, "U": 9, "V": 10, "X": 11, "Z": 12,
}


def parse_cme_exp_months_ahead(exp: str, now_msk: Optional[datetime] = None) -> int:
    """
    Decodes CME expiration code (e.g. 'G5MX6', 'OG1Z6', 'OGF7') into months ahead
    from the current Moscow month. Returns 0 if exp is missing/unparseable.
    """
    exp_str = str(exp or "").strip().upper()
    m = re.search(r"([FGHJKMNQUVXZ])(\d)$", exp_str)
    if not m:
        return 0

    month = CME_MONTH_CODES[m.group(1)]
    year_digit = int(m.group(2))
    now = now_msk or datetime.now(TZ_MSK)
    decade = (now.year // 10) * 10
    year = decade + year_digit
    if year < now.year - 2:
        year += 10

    return (year - now.year) * 12 + (month - now.month)


def filter_near_term_contracts(
    contracts: List[Dict[str, Any]],
    now_msk: Optional[datetime] = None,
) -> Tuple[List[Dict[str, Any]], bool]:
    """
    Filters contracts to near-term expirations (0..1 months ahead, or 0..2 if <2 found),
    ignoring far-dated long-term contracts (e.g. 2027+).
    Returns (filtered_list, is_near_term_filtered).
    """
    if not contracts:
        return [], False

    has_exp = any(bool(c.get("exp")) for c in contracts)
    if not has_exp:
        return contracts, False

    for max_months in (1, 2):
        near = [
            c for c in contracts
            if 0 <= parse_cme_exp_months_ahead(c.get("exp", ""), now_msk=now_msk) <= max_months
        ]
        if len(near) >= 2:
            return near, True

    # Fallback: take contracts with the smallest non-negative months_ahead
    valid = [
        (parse_cme_exp_months_ahead(c.get("exp", ""), now_msk=now_msk), c)
        for c in contracts
    ]
    non_neg = [pair for pair in valid if pair[0] >= 0]
    if non_neg:
        min_m = min(pair[0] for pair in non_neg)
        return [pair[1] for pair in non_neg if pair[0] <= min_m + 1], True

    return contracts, False


def analyze_quikstrike_options(
    calls: List[Dict[str, Any]],
    puts: List[Dict[str, Any]],
    current_price: float = 0.0,
    symbol: str = "GC",
    now_msk: Optional[datetime] = None,
) -> Dict[str, Any]:
    """
    Analyzes near-term options open interest, moneyness (ITM/OTM), and volume to determine
    expected short-term market movement, key support/resistance levels, and inflows.
    """
    raw_calls = calls or []
    raw_puts = puts or []

    calls, calls_near = filter_near_term_contracts(raw_calls, now_msk=now_msk)
    puts, puts_near = filter_near_term_contracts(raw_puts, now_msk=now_msk)
    is_near_term = calls_near or puts_near

    total_call_oi = sum(int(c.get("curr_oi", 0)) for c in calls)
    total_put_oi = sum(int(p.get("curr_oi", 0)) for p in puts)
    total_call_vol = sum(int(c.get("vol", 0)) for c in calls)
    total_put_vol = sum(int(p.get("vol", 0)) for p in puts)
    total_call_inflow = sum(max(0, int(c.get("chg", 0))) for c in calls)
    total_put_inflow = sum(max(0, int(p.get("chg", 0))) for p in puts)

    pcr_oi = round(total_put_oi / total_call_oi, 2) if total_call_oi > 0 else 1.0
    pcr_vol = round(total_put_vol / total_call_vol, 2) if total_call_vol > 0 else 1.0
    pcr_inflow = round(total_put_inflow / total_call_inflow, 2) if total_call_inflow > 0 else 1.0

    # Classify Moneyness (ITM / ATM / OTM)
    itm_puts: List[Dict[str, Any]] = []
    itm_calls: List[Dict[str, Any]] = []

    if current_price > 0:
        for p in puts:
            strike = float(p.get("strike", 0))
            # Put is In-The-Money when strike > current price
            if strike > current_price * 1.005:
                itm_puts.append(p)

        for c in calls:
            strike = float(c.get("strike", 0))
            # Call is In-The-Money when strike < current price
            if strike < current_price * 0.995:
                itm_calls.append(c)

    itm_put_strikes = sorted(list({p["strike"] for p in itm_puts}))
    itm_call_strikes = sorted(list({c["strike"] for c in itm_calls}))

    # Key Levels: Support (Max Put OI) & Resistance (Max Call OI)
    max_put = max(puts, key=lambda x: int(x.get("curr_oi", 0))) if puts else None
    max_call = max(calls, key=lambda x: int(x.get("curr_oi", 0))) if calls else None

    support_strike = max_put["strike"] if max_put else 0
    support_oi = int(max_put["curr_oi"]) if max_put else 0
    support_exp = str(max_put.get("exp", "")).strip() if max_put else ""

    resistance_strike = max_call["strike"] if max_call else 0
    resistance_oi = int(max_call["curr_oi"]) if max_call else 0
    resistance_exp = str(max_call.get("exp", "")).strip() if max_call else ""

    # Institutional Smart-Money: maximum daily positive inflow (near-term)
    all_contracts = calls + puts
    valid_inflow_contracts = [c for c in all_contracts if int(c.get("chg", 0)) > 0]
    top_inflow_contract = max(valid_inflow_contracts, key=lambda x: int(x.get("chg", 0))) if valid_inflow_contracts else None

    # Determine Short-Term Movement Direction from Nearest Call & Put
    is_bearish = (
        pcr_inflow >= 1.20
        or (pcr_oi >= 1.15 and len(itm_put_strikes) > 0)
        or (len(itm_put_strikes) >= 2 and total_put_inflow > total_call_inflow)
    )
    is_bullish = (
        pcr_inflow <= 0.80
        or (pcr_oi <= 0.85 and len(itm_call_strikes) > 0)
        or (len(itm_call_strikes) >= 2 and total_call_inflow > total_put_inflow)
    )

    sup_exp_note = f" ({support_exp})" if support_exp else ""
    res_exp_note = f" ({resistance_exp})" if resistance_exp else ""

    if is_bearish and not is_bullish:
        sentiment = "bearish"
        sentiment_label = "Медвежий (Давление продавцов)"
        sentiment_icon = "🔴"
        movement_icon = "📉"
        movement_label = f"Вниз к ближнему PUT ${support_strike}"
        if itm_put_strikes:
            formatted_strikes = ", ".join(f"`{s}`" for s in itm_put_strikes[:3])
            summary = (
                f"По ближнему сроку преобладают опционы **ПУТ**. В топе активности зафиксированы ПУТы на уровнях {formatted_strikes} "
                f"(находятся в деньгах, что говорит о дальнейшем снижении к ближнему PUT `${support_strike}`{sup_exp_note})."
            )
        else:
            summary = (
                f"По ближнему сроку преобладают опционы **ПУТ** (приток {total_put_inflow:,} контр.). "
                f"Ожидается движение вниз к ближнему PUT `${support_strike}`{sup_exp_note}, потолок — CALL `${resistance_strike}`{res_exp_note}."
            )
    elif is_bullish and not is_bearish:
        sentiment = "bullish"
        sentiment_label = "Бычий (Преобладание покупателей)"
        sentiment_icon = "🟢"
        movement_icon = "📈"
        movement_label = f"Вверх к ближнему CALL ${resistance_strike}"
        if itm_call_strikes:
            formatted_strikes = ", ".join(f"`{s}`" for s in itm_call_strikes[:3])
            summary = (
                f"По ближнему сроку преобладают опционы **КОЛЛ**. В топе активности зафиксированы КОЛЛы на уровнях {formatted_strikes} "
                f"(находятся в деньгах, что подтверждает движение вверх к `${resistance_strike}`{res_exp_note})."
            )
        else:
            summary = (
                f"По ближнему сроку преобладают опционы **КОЛЛ** (приток {total_call_inflow:,} контр.). "
                f"Основной ориентир движения — вверх к ближнему CALL `${resistance_strike}`{res_exp_note}, поддержка — PUT `${support_strike}`{sup_exp_note}."
            )
    else:
        sentiment = "neutral"
        sentiment_label = "Нейтральный (Баланс спроса и предложения)"
        sentiment_icon = "🟡"
        movement_icon = "↔️"
        movement_label = f"Диапазон ${support_strike} – ${resistance_strike}"
        summary = (
            f"Ближний интерес распределён между **PUT** `${support_strike}`{sup_exp_note} и **CALL** `${resistance_strike}`{res_exp_note}. "
            f"Ожидается движение внутри этого коридора до пробоя одной из границ."
        )

    return {
        "symbol": symbol,
        "current_price": current_price,
        "is_near_term": is_near_term,
        "total_call_oi": total_call_oi,
        "total_put_oi": total_put_oi,
        "total_call_vol": total_call_vol,
        "total_put_vol": total_put_vol,
        "total_call_inflow": total_call_inflow,
        "total_put_inflow": total_put_inflow,
        "pcr_oi": pcr_oi,
        "pcr_vol": pcr_vol,
        "pcr_inflow": pcr_inflow,
        "itm_put_strikes": itm_put_strikes,
        "itm_call_strikes": itm_call_strikes,
        "support_strike": support_strike,
        "support_oi": support_oi,
        "support_exp": support_exp,
        "resistance_strike": resistance_strike,
        "resistance_oi": resistance_oi,
        "resistance_exp": resistance_exp,
        "top_inflow_contract": top_inflow_contract,
        "sentiment": sentiment,
        "sentiment_label": sentiment_label,
        "sentiment_icon": sentiment_icon,
        "movement_icon": movement_icon,
        "movement_label": movement_label,
        "summary": summary
    }


def format_analytics_footnote(analysis: Dict[str, Any], instrument_name: str = "Золото (GC)") -> str:
    """Formats near-term algorithmic options analysis into a clean Telegram Markdown section."""
    sup_exp = f"{analysis['support_exp']} • " if analysis.get("support_exp") else ""
    res_exp = f"{analysis['resistance_exp']} • " if analysis.get("resistance_exp") else ""
    sup_str = f"`${analysis['support_strike']}` ({sup_exp}`{analysis['support_oi']:,}` контр.)" if analysis['support_strike'] else "—"
    res_str = f"`${analysis['resistance_strike']}` ({res_exp}`{analysis['resistance_oi']:,}` контр.)" if analysis['resistance_strike'] else "—"
    horizon = " • Ближний срок" if analysis.get("is_near_term") else ""

    lines = [
        f"💡 **ЕЖЕДНЕВНАЯ СНОСКА / АНАЛИТИКА ({instrument_name}{horizon}):**",
        f"• 🧭 **Движение:** {analysis.get('movement_icon', analysis['sentiment_icon'])} **{analysis.get('movement_label', analysis['sentiment_label'])}**",
        f"• 🔍 **По ближним Call и Put:** {analysis['summary']}",
        f"• 🛡 **Ближний PUT (Поддержка):** {sup_str}",
        f"• 🎯 **Ближний CALL (Цель/Сопрот.):** {res_str}",
    ]

    top_inflow = analysis.get("top_inflow_contract")
    if top_inflow and int(top_inflow.get("chg", 0)) > 0:
        c_type = "🟢 CALL" if top_inflow.get("type") == "CALL" else "🔴 PUT"
        c_strike = top_inflow.get("strike", "")
        c_exp = str(top_inflow.get("exp", "")).strip()
        exp_part = f", {c_exp}" if c_exp else ""
        c_chg = int(top_inflow.get("chg", 0))
        lines.append(f"• ⚡️ **Ближний приток (Смарт-мани):** в {c_type} `{c_strike}` (`+{c_chg:,}` контр.{exp_part})")

    lines.append("\n📢 *Детальный анализ у нас в канале, ссылка в шапке профиля*")

    return "\n".join(lines)


def format_cme_guide_message() -> str:
    """Returns a beginner-friendly glossary matching the Mini App 'Пояснение терминов' page."""
    return (
        "📖 **ПОЯСНЕНИЕ ТЕРМИНОВ (ГИД ДЛЯ НОВИЧКА)**\n"
        "*Простым языком о том, что значат все кнопки, колонки и цифры в терминале и отчётах бота:*\n\n"
        "1️⃣ 🏦 **CME Group и QuikStrike — что это за данные?**\n"
        "• **CME Group** — крупнейшая биржа мира (Чикаго), где банки, фонды и корпорации торгуют золотом, серебром и валютами.\n"
        "• **QuikStrike (Most Actives OI)** — это «рентген» биржи: показывает, на каких ценах прямо сейчас лежат самые крупные деньги.\n\n"
        "2️⃣ 🟢 **CALL и 🔴 PUT — куда смотрят игроки**\n"
        "• **🟢 CALL (Колл)** — ставка (или страховка) на **РОСТ** цены. Например, много CALL на `4500` — рынок ждёт движения к этому уровню.\n"
        "• **🔴 PUT (Пут)** — ставка (или страховка) на **ПАДЕНИЕ** цены. Крупный объём PUT на `3500` — там крупняк страхуется от снижения.\n\n"
        "3️⃣ 📊 **STRIKE и EXP — колонки таблицы**\n"
        "• **STRIKE (Страйк)** — конкретная **цена-уровень**, на которую заключён контракт (например, `$3750` за унцию золота).\n"
        "• **EXP (Экспирация)** — **срок жизни** контракта: код месяца и года, когда он закончится (например, `OGG7` — февраль 2027).\n\n"
        "4️⃣ 💰 **VOL, даты (OI) и CHG — объёмы и деньги**\n"
        "• **VOL (Объём)** — сколько контрактов купили и продали **за один день**. Показывает активность торгов сегодня.\n"
        "• **Даты (напр. НОЯ 24 / НОЯ 25)** — это **OI (Открытый интерес)**: сколько действующих контрактов *уже открыто* на этом уровне вчера и сегодня. Чем больше число — тем сильнее уровень.\n"
        "• **CHG (Изменение)** — главная колонка! `+1,052` (зелёный) — зашли *новые* деньги. `-373` (красный) — часть старых позиций закрыли.\n\n"
        "5️⃣ 🎯 **Фильтр OI, Поддержка и Сопротивление**\n"
        "• **Фильтр (OI ≥ 500 / 1,000 / 2,000)** — убирает мелкий шум и оставляет только крупные сделки.\n"
        "• 🛡 **Поддержка (Max Put OI)** — «пол» рынка, где больше всего PUT. Крупным игрокам часто невыгодно падение сильно ниже.\n"
        "• 🎯 **Сопротивление (Max Call OI)** — «потолок» / ориентир роста, где накоплено больше всего CALL.\n\n"
        "6️⃣ ⚡️ **Смарт-мани, ITM и OTM**\n"
        "• ⚡️ **Смарт-мани («Умные деньги»)** — уровень с самым большим суточным притоком `+CHG`. Подсказка, куда крупный капитал зашёл прямо сейчас.\n"
        "• **В деньгах (ITM)** — цена уже зашла за этот страйк (у контракта уже есть реальная прибыль).\n"
        "• **Вне денег (OTM)** — цена ещё не дошла до этого уровня.\n\n"
        "✅ **КАК ПОЛЬЗОВАТЬСЯ ОТЧЁТОМ НОВИЧКУ (3 ШАГА):**\n"
        "1. **Посмотри направление:** выбери инструмент (Gold, Silver и др.) и проверь, где больше зелёных цифр `+CHG` — в **CALL** (рост) или в **PUT** (снижение/защита).\n"
        "2. **Найди важные цены:** выпиши страйки с самым большим **OI** и максимальным притоком `+CHG` — это ориентиры границ рынка.\n"
        "3. **Не торопись:** данные CME показывают среднесрочные ожидания фондов, а не сигнал «входить в эту секунду». Всегда торгуй со стоп-лоссом."
    )
