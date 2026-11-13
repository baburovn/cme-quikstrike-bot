# -*- coding: utf-8 -*-
"""
CME QuikStrike Options Analytics & Sentiment Engine.
Algorithmic analysis (Option Greeks / Put-Call Dynamics / ITM-OTM Moneyness / Key Levels)
without external third-party APIs.
"""
from typing import Dict, Any, List, Optional


def analyze_quikstrike_options(
    calls: List[Dict[str, Any]],
    puts: List[Dict[str, Any]],
    current_price: float = 0.0,
    symbol: str = "GC"
) -> Dict[str, Any]:
    """
    Analyzes options open interest, moneyness (ITM/OTM), and volume to determine market sentiment,
    key support/resistance levels, and institutional inflows.
    """
    calls = calls or []
    puts = puts or []

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

    resistance_strike = max_call["strike"] if max_call else 0
    resistance_oi = int(max_call["curr_oi"]) if max_call else 0

    # Institutional Smart-Money: maximum daily positive inflow
    all_contracts = calls + puts
    valid_inflow_contracts = [c for c in all_contracts if int(c.get("chg", 0)) > 0]
    top_inflow_contract = max(valid_inflow_contracts, key=lambda x: int(x.get("chg", 0))) if valid_inflow_contracts else None

    # Determine Sentiment
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

    if is_bearish and not is_bullish:
        sentiment = "bearish"
        sentiment_label = "Медвежий (Давление продавцов)"
        sentiment_icon = "🔴"
    elif is_bullish and not is_bearish:
        sentiment = "bullish"
        sentiment_label = "Бычий (Преобладание покупателей)"
        sentiment_icon = "🟢"
    else:
        sentiment = "neutral"
        sentiment_label = "Нейтральный (Баланс спроса и предложения)"
        sentiment_icon = "🟡"

    # Generate explanatory summary text
    if sentiment == "bearish":
        if itm_put_strikes:
            formatted_strikes = ", ".join(f"`{s}`" for s in itm_put_strikes[:3])
            summary = (
                f"На сегодняшний день преобладают опционы **ПУТ**. В топе активности зафиксированы ПУТы на уровнях {formatted_strikes} "
                f"(находятся в деньгах, что говорит о дальнейшем снижении и сохранении давления)."
            )
        else:
            summary = (
                f"На сегодняшний день преобладают опционы **ПУТ** (приток {total_put_inflow:,} контр.). "
                f"Игроки хеджируют риски падения в сторону поддержки ${support_strike}."
            )
    elif sentiment == "bullish":
        if itm_call_strikes:
            formatted_strikes = ", ".join(f"`{s}`" for s in itm_call_strikes[:3])
            summary = (
                f"На сегодняшний день преобладают опционы **КОЛЛ**. В топе активности зафиксированы КОЛЛы на уровнях {formatted_strikes} "
                f"(находятся в деньгах, что подтверждает силу покупателей и восходящий импульс)."
            )
        else:
            summary = (
                f"На сегодняшний день преобладают опционы **КОЛЛ** (приток {total_call_inflow:,} контр.). "
                f"Открытый интерес нарастает выше рынка с целевым ориентиром на сопротивление ${resistance_strike}."
            )
    else:
        summary = (
            f"На рынке наблюдается относительное равновесие между опционами CALL и PUT (PCR по OI: `{pcr_oi}`). "
            f"Котировки зажаты в торговом диапазоне между поддержкой `${support_strike}` и сопротивлением `${resistance_strike}`."
        )

    return {
        "symbol": symbol,
        "current_price": current_price,
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
        "resistance_strike": resistance_strike,
        "resistance_oi": resistance_oi,
        "top_inflow_contract": top_inflow_contract,
        "sentiment": sentiment,
        "sentiment_label": sentiment_label,
        "sentiment_icon": sentiment_icon,
        "summary": summary
    }


def format_analytics_footnote(analysis: Dict[str, Any], instrument_name: str = "Золото (GC)") -> str:
    """Formats algorithmic options analysis into a clean Telegram Markdown section."""
    sup_str = f"`${analysis['support_strike']}` (`{analysis['support_oi']:,}` контр.)" if analysis['support_strike'] else "—"
    res_str = f"`${analysis['resistance_strike']}` (`{analysis['resistance_oi']:,}` контр.)" if analysis['resistance_strike'] else "—"

    lines = [
        f"💡 **ЕЖЕДНЕВНАЯ СНОСКА / АНАЛИТИКА ({instrument_name}):**",
        f"• 🧭 **Сентимент:** {analysis['sentiment_icon']} **{analysis['sentiment_label']}** (PCR OI: `{analysis['pcr_oi']}`)",
        f"• 🔍 **Анализ позиций:** {analysis['summary']}",
        f"• 🛡 **Поддержка (Max Put OI):** {sup_str}",
        f"• 🎯 **Сопротивление (Max Call OI):** {res_str}",
    ]

    top_inflow = analysis.get("top_inflow_contract")
    if top_inflow and int(top_inflow.get("chg", 0)) > 0:
        c_type = "🟢 CALL" if top_inflow.get("type") == "CALL" else "🔴 PUT"
        c_strike = top_inflow.get("strike", "")
        c_chg = int(top_inflow.get("chg", 0))
        lines.append(f"• ⚡️ **Смарт-мани:** макс. суточный приток в {c_type} `{c_strike}` (`+{c_chg:,}` контр.)")

    return "\n".join(lines)
