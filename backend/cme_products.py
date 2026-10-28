# -*- coding: utf-8 -*-
"""
CME Core Instruments with full contract specifications and expiration calendars.
"""

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
