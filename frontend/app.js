// Default fallback initial dataset (Instant render on page load)
const INITIAL_DATA = [
  {
    symbol: "GC",
    name: "Gold Futures (Золото 🟡)",
    category: "metals",
    unit: "$ / troy oz",
    price: 2748.50,
    change_pct: 0.42,
    volume: 482150,
    open_interest: 984200,
    trend: "up",
    specs: {
      lot_size: "100 тройских унций (~3.11 кг)",
      tick_size: "$0.10 за унцию",
      tick_value: "$10.00 на контракт",
      settlement_type: "Физическая поставка (Physical Delivery)",
      grade: "Слитки золота чистотой не менее .995",
      initial_margin: "$11,000",
      maintenance_margin: "$10,000",
      trading_hours: "CME Globex: Вс-Пт 18:00 - 17:00 CT",
      cme_url: "https://www.cmegroup.com/markets/metals/precious/gold.contractSpecs.html"
    },
    expirations: [
      { code: "GCJ26", month: "Апрель 2026", last_trade: "28.04.2026", days_left: 26, active: true },
      { code: "GCM26", month: "Июнь 2026", last_trade: "26.06.2026", days_left: 85, active: false },
      { code: "GCQ26", month: "Август 2026", last_trade: "27.08.2026", days_left: 147, active: false },
      { code: "GCV26", month: "Октябрь 2026", last_trade: "28.10.2026", days_left: 209, active: false },
      { code: "GCZ26", month: "Декабрь 2026", last_trade: "29.12.2026", days_left: 271, active: false },
    ]
  },
  {
    symbol: "SI",
    name: "Silver Futures (Серебро ⚪)",
    category: "metals",
    unit: "$ / troy oz",
    price: 32.45,
    change_pct: -0.15,
    volume: 294800,
    open_interest: 412500,
    trend: "down",
    specs: {
      lot_size: "5,000 тройских унций (~155.5 кг)",
      tick_size: "$0.005 за унцию",
      tick_value: "$25.00 на контракт",
      settlement_type: "Физическая поставка (Physical Delivery)",
      grade: "Слитки серебра чистотой не менее .999",
      initial_margin: "$9,500",
      maintenance_margin: "$8,600",
      trading_hours: "CME Globex: Вс-Пт 18:00 - 17:00 CT",
      cme_url: "https://www.cmegroup.com/markets/metals/precious/silver.contractSpecs.html"
    },
    expirations: [
      { code: "SIK26", month: "Май 2026", last_trade: "27.05.2026", days_left: 55, active: true },
      { code: "SIN26", month: "Июль 2026", last_trade: "29.07.2026", days_left: 118, active: false },
      { code: "SIU26", month: "Сентябрь 2026", last_trade: "28.09.2026", days_left: 179, active: false },
      { code: "SIZ26", month: "Декабрь 2026", last_trade: "29.12.2026", days_left: 271, active: false },
    ]
  },
  {
    symbol: "HG",
    name: "Copper Futures (Медь 🟤)",
    category: "metals",
    unit: "$ / lb",
    price: 4.3850,
    change_pct: 0.28,
    volume: 128400,
    open_interest: 215000,
    trend: "up",
    specs: {
      lot_size: "25,000 фунтов (~11.33 тонны)",
      tick_size: "$0.0005 за фунт",
      tick_value: "$12.50 на контракт",
      settlement_type: "Физическая поставка (Physical Delivery)",
      grade: "Катодная медь Grade 1 (ASTM B115)",
      initial_margin: "$6,000",
      maintenance_margin: "$5,450",
      trading_hours: "CME Globex: Вс-Пт 18:00 - 17:00 CT",
      cme_url: "https://www.cmegroup.com/markets/metals/base/copper.contractSpecs.html"
    },
    expirations: [
      { code: "HGK26", month: "Май 2026", last_trade: "27.05.2026", days_left: 55, active: true },
      { code: "HGN26", month: "Июль 2026", last_trade: "29.07.2026", days_left: 118, active: false },
      { code: "HGU26", month: "Сентябрь 2026", last_trade: "28.09.2026", days_left: 179, active: false },
      { code: "HGZ26", month: "Декабрь 2026", last_trade: "29.12.2026", days_left: 271, active: false },
    ]
  },
  {
    symbol: "PL",
    name: "Platinum Futures (Платина ⚪)",
    category: "metals",
    unit: "$ / troy oz",
    price: 988.20,
    change_pct: -0.54,
    volume: 65400,
    open_interest: 84200,
    trend: "down",
    specs: {
      lot_size: "50 тройских унций (~1.55 кг)",
      tick_size: "$0.10 за унцию",
      tick_value: "$5.00 на контракт",
      settlement_type: "Физическая поставка (Physical Delivery)",
      grade: "Платиновые слитки чистотой не менее .9995",
      initial_margin: "$4,200",
      maintenance_margin: "$3,800",
      trading_hours: "CME Globex: Вс-Пт 18:00 - 17:00 CT",
      cme_url: "https://www.cmegroup.com/markets/metals/precious/platinum.contractSpecs.html"
    },
    expirations: [
      { code: "PLN26", month: "Июль 2026", last_trade: "29.07.2026", days_left: 118, active: true },
      { code: "PLV26", month: "Октябрь 2026", last_trade: "28.10.2026", days_left: 209, active: false },
      { code: "PLF27", month: "Январь 2027", last_trade: "27.01.2027", days_left: 300, active: false },
    ]
  },
  {
    symbol: "PA",
    name: "Palladium Futures (Палладий 🔘)",
    category: "metals",
    unit: "$ / troy oz",
    price: 1045.00,
    change_pct: 1.12,
    volume: 28900,
    open_interest: 34100,
    trend: "up",
    specs: {
      lot_size: "100 тройских унций (~3.11 кг)",
      tick_size: "$0.50 за унцию",
      tick_value: "$50.00 на контракт",
      settlement_type: "Физическая поставка (Physical Delivery)",
      grade: "Палладиевые слитки чистотой не менее .9995",
      initial_margin: "$12,500",
      maintenance_margin: "$11,350",
      trading_hours: "CME Globex: Вс-Пт 18:00 - 17:00 CT",
      cme_url: "https://www.cmegroup.com/markets/metals/precious/palladium.contractSpecs.html"
    },
    expirations: [
      { code: "PAM26", month: "Июнь 2026", last_trade: "26.06.2026", days_left: 85, active: true },
      { code: "PAU26", month: "Сентябрь 2026", last_trade: "28.09.2026", days_left: 179, active: false },
      { code: "PAZ26", month: "Декабрь 2026", last_trade: "29.12.2026", days_left: 271, active: false },
    ]
  },
  {
    symbol: "6E",
    name: "EUR/USD Futures (Евро 💶)",
    category: "currencies",
    unit: "$ / EUR",
    price: 1.0485,
    change_pct: -0.05,
    volume: 325400,
    open_interest: 765400,
    trend: "down",
    specs: {
      lot_size: "125,000 EUR",
      tick_size: "$0.00005 за евро (половинный тик)",
      tick_value: "$6.25 на контракт",
      settlement_type: "Финансовый расчёт (Cash Settled)",
      grade: "Официальный кросс-курс EUR/USD",
      initial_margin: "$2,800",
      maintenance_margin: "$2,550",
      trading_hours: "CME Globex: Вс-Пт 18:00 - 17:00 CT",
      cme_url: "https://www.cmegroup.com/markets/fx/g10/euro-fx.contractSpecs.html"
    },
    expirations: [
      { code: "6EM26", month: "Июнь 2026", last_trade: "15.06.2026", days_left: 74, active: true },
      { code: "6EU26", month: "Сентябрь 2026", last_trade: "14.09.2026", days_left: 165, active: false },
      { code: "6EZ26", month: "Декабрь 2026", last_trade: "14.12.2026", days_left: 256, active: false },
    ]
  },
  {
    symbol: "6B",
    name: "GBP/USD Futures (Фунт 💷)",
    category: "currencies",
    unit: "$ / GBP",
    price: 1.2540,
    change_pct: 0.18,
    volume: 210200,
    open_interest: 534000,
    trend: "up",
    specs: {
      lot_size: "62,500 GBP",
      tick_size: "$0.0001 за фунт",
      tick_value: "$6.25 на контракт",
      settlement_type: "Финансовый расчёт (Cash Settled)",
      grade: "Официальный кросс-курс GBP/USD",
      initial_margin: "$2,400",
      maintenance_margin: "$2,180",
      trading_hours: "CME Globex: Вс-Пт 18:00 - 17:00 CT",
      cme_url: "https://www.cmegroup.com/markets/fx/g10/british-pound.contractSpecs.html"
    },
    expirations: [
      { code: "6BM26", month: "Июнь 2026", last_trade: "15.06.2026", days_left: 74, active: true },
      { code: "6BU26", month: "Сентябрь 2026", last_trade: "14.09.2026", days_left: 165, active: false },
      { code: "6BZ26", month: "Декабрь 2026", last_trade: "14.12.2026", days_left: 256, active: false },
    ]
  },
  {
    symbol: "6A",
    name: "AUD/USD Futures (Австралийский доллар 🇦🇺)",
    category: "currencies",
    unit: "$ / AUD",
    price: 0.6350,
    change_pct: -0.12,
    volume: 118700,
    open_interest: 294000,
    trend: "down",
    specs: {
      lot_size: "100,000 AUD",
      tick_size: "$0.0001 за австралийский доллар",
      tick_value: "$10.00 на контракт",
      settlement_type: "Финансовый расчёт (Cash Settled)",
      grade: "Официальный кросс-курс AUD/USD",
      initial_margin: "$1,800",
      maintenance_margin: "$1,630",
      trading_hours: "CME Globex: Вс-Пт 18:00 - 17:00 CT",
      cme_url: "https://www.cmegroup.com/markets/fx/g10/australian-dollar.contractSpecs.html"
    },
    expirations: [
      { code: "6AM26", month: "Июнь 2026", last_trade: "15.06.2026", days_left: 74, active: true },
      { code: "6AU26", month: "Сентябрь 2026", last_trade: "14.09.2026", days_left: 165, active: false },
      { code: "6AZ26", month: "Декабрь 2026", last_trade: "14.12.2026", days_left: 256, active: false },
    ]
  }
];

// State
let selectedSymbol = "GC";
let quotesData = [...INITIAL_DATA];
let currentCategory = "all";
let currentViewMode = "chart"; // 'chart', 'specs', 'calendar'
let chart = null;
let candleSeries = null;
let volumeSeries = null;
let ws = null;
let lastKnownPrices = {};

// Telegram WebApp Init
const tg = window.Telegram?.WebApp;
if (tg) {
  try {
    tg.ready();
    tg.expand();
    if (tg.setHeaderColor) tg.setHeaderColor("#0e1117");
    if (tg.setBackgroundColor) tg.setBackgroundColor("#0e1117");
    document.body.classList.add("tg-theme");
  } catch (e) {
    console.warn("Telegram WebApp init warning:", e);
  }
}

function tgHaptic(type = "light") {
  try {
    if (tg?.HapticFeedback) {
      if (type === "medium") tg.HapticFeedback.impactOccurred("medium");
      else if (type === "success") tg.HapticFeedback.notificationOccurred("success");
      else tg.HapticFeedback.impactOccurred("light");
    }
  } catch (e) {}
}

// Format numbers
function formatPrice(val, decimals = 2) {
  if (val === undefined || val === null || isNaN(val)) return "--";
  if (Number(val) < 10) decimals = 4;
  return Number(val).toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  });
}

function formatCompact(val) {
  return Number(val || 0).toLocaleString("en-US");
}

// CME Market Clock
function updateClock() {
  const clockEl = document.getElementById("cmeClock");
  if (clockEl) {
    const now = new Date();
    clockEl.textContent = now.toLocaleTimeString("ru-RU", { hour12: false }) + " UTC";
  }
}
setInterval(updateClock, 1000);
updateClock();

// Initialize TradingView Lightweight Charts (v4 and v5 compatible)
function initChart() {
  const container = document.getElementById("chartContainer");
  if (!container || !window.LightweightCharts) {
    console.warn("Chart container or LightweightCharts not found");
    return;
  }

  container.innerHTML = "";

  try {
    chart = LightweightCharts.createChart(container, {
      width: container.clientWidth || 340,
      height: 240,
      layout: {
        background: { color: "#161b22" },
        textColor: "#8b949e",
        fontSize: 11,
        fontFamily: "'JetBrains Mono', monospace",
      },
      grid: {
        vertLines: { color: "#21262d" },
        horzLines: { color: "#21262d" },
      },
      crosshair: {
        mode: LightweightCharts.CrosshairMode?.Normal ?? 1,
      },
      rightPriceScale: {
        borderColor: "#2d333b",
      },
      timeScale: {
        borderColor: "#2d333b",
        timeVisible: true,
        secondsVisible: false,
      },
    });

    const candleOpts = {
      upColor: "#10b981",
      downColor: "#ef4444",
      borderVisible: false,
      wickUpColor: "#10b981",
      wickDownColor: "#ef4444",
    };

    if (typeof chart.addCandlestickSeries === "function") {
      candleSeries = chart.addCandlestickSeries(candleOpts);
    } else if (typeof chart.addSeries === "function" && window.LightweightCharts?.CandlestickSeries) {
      candleSeries = chart.addSeries(LightweightCharts.CandlestickSeries, candleOpts);
    }

    const volOpts = {
      color: "#26a69a",
      priceFormat: { type: "volume" },
      priceScaleId: "",
    };

    if (typeof chart.addHistogramSeries === "function") {
      volumeSeries = chart.addHistogramSeries(volOpts);
    } else if (typeof chart.addSeries === "function" && window.LightweightCharts?.HistogramSeries) {
      volumeSeries = chart.addSeries(LightweightCharts.HistogramSeries, volOpts);
    }

    const ro = new ResizeObserver(entries => {
      if (!entries || entries.length === 0 || !entries[0].contentRect) return;
      const { width, height } = entries[0].contentRect;
      if (chart && width > 0 && height > 0) {
        chart.applyOptions({ width, height });
      }
    });
    ro.observe(container);

    chart.subscribeCrosshairMove(param => {
      if (!param || !candleSeries) return;
      const bar = param.seriesData ? param.seriesData.get(candleSeries) : null;
      const vol = (param.seriesData && volumeSeries) ? param.seriesData.get(volumeSeries) : null;
      if (bar) {
        if (bar.open !== undefined) document.getElementById("barOpen").textContent = formatPrice(bar.open);
        if (bar.high !== undefined) document.getElementById("barHigh").textContent = formatPrice(bar.high);
        if (bar.low !== undefined) document.getElementById("barLow").textContent = formatPrice(bar.low);
        if (bar.close !== undefined) document.getElementById("barClose").textContent = formatPrice(bar.close);
      }
      if (vol && vol.value !== undefined) {
        document.getElementById("barVol").textContent = formatCompact(vol.value);
      }
    });
  } catch (err) {
    console.error("Failed to initialize chart:", err);
  }
}

// Fetch candle history for active instrument
async function loadChartHistory(symbol) {
  if (!candleSeries) return;
  try {
    const res = await fetch(`/api/history/${symbol}`);
    const data = await res.json();
    if (data.status === "ok" && data.candles && candleSeries) {
      const formattedCandles = data.candles.map(c => ({
        time: c.time,
        open: c.open,
        high: c.high,
        low: c.low,
        close: c.close
      }));

      const formattedVolumes = data.candles.map(c => ({
        time: c.time,
        value: c.volume,
        color: c.close >= c.open ? "rgba(16, 185, 129, 0.4)" : "rgba(239, 68, 68, 0.4)"
      }));

      candleSeries.setData(formattedCandles);
      if (volumeSeries) volumeSeries.setData(formattedVolumes);
      if (chart) chart.timeScale().fitContent();

      const last = data.candles[data.candles.length - 1];
      if (last) {
        document.getElementById("barOpen").textContent = formatPrice(last.open);
        document.getElementById("barHigh").textContent = formatPrice(last.high);
        document.getElementById("barLow").textContent = formatPrice(last.low);
        document.getElementById("barClose").textContent = formatPrice(last.close);
        document.getElementById("barVol").textContent = formatCompact(last.volume);
      }
    }
  } catch (err) {
    console.error("Error loading chart history:", err);
  }
}

// Render Contract Specifications View
function renderSpecs(symbol) {
  const grid = document.getElementById("specsGrid");
  if (!grid) return;

  const quote = quotesData.find(q => q.symbol === symbol) || INITIAL_DATA.find(q => q.symbol === symbol);
  const specs = quote?.specs || {};

  grid.innerHTML = `
    <div class="spec-card">
      <div class="spec-title">📦 Размер контракта (Lot Size)</div>
      <div class="spec-val">${specs.lot_size || 'N/A'}</div>
    </div>
    <div class="spec-card">
      <div class="spec-title">🎯 Шаг цены (Tick Size)</div>
      <div class="spec-val">${specs.tick_size || 'N/A'}</div>
    </div>
    <div class="spec-card">
      <div class="spec-title">💵 Стоимость 1 тика (Tick Value)</div>
      <div class="spec-val" style="color: var(--accent-gold);">${specs.tick_value || 'N/A'}</div>
    </div>
    <div class="spec-card">
      <div class="spec-title">🚚 Тип расчёта (Settlement)</div>
      <div class="spec-val">${specs.settlement_type || 'N/A'}</div>
    </div>
    <div class="spec-card">
      <div class="spec-title">🛡 Начальная маржа (Initial Margin)</div>
      <div class="spec-val" style="color: var(--color-green);">${specs.initial_margin || 'N/A'}</div>
    </div>
    <div class="spec-card">
      <div class="spec-title">⚠️ Поддерживающая маржа (Maint.)</div>
      <div class="spec-val">${specs.maintenance_margin || 'N/A'}</div>
    </div>
    <div class="spec-card">
      <div class="spec-title">🔍 Стандарт качества / Базис</div>
      <div class="spec-val" style="font-size: 11px;">${specs.grade || 'N/A'}</div>
    </div>
    <div class="spec-card">
      <div class="spec-title">⏰ Часы торговли (Globex)</div>
      <div class="spec-val" style="font-size: 11px;">${specs.trading_hours || 'N/A'}</div>
    </div>
    <div class="cme-link-box">
      <a href="${specs.cme_url || 'https://www.cmegroup.com'}" target="_blank" class="cme-link-btn">
        <span>📄 Официальная спецификация на CME Group</span> ↗
      </a>
    </div>
  `;
}

// Render Expiration Calendar View
function renderCalendar(symbol) {
  const container = document.getElementById("calendarList");
  if (!container) return;

  const quote = quotesData.find(q => q.symbol === symbol) || INITIAL_DATA.find(q => q.symbol === symbol);
  const expirations = quote?.expirations || [];

  if (expirations.length === 0) {
    container.innerHTML = `<div style="text-align:center; padding: 20px; color: var(--text-muted);">Календарь обновляется...</div>`;
    return;
  }

  container.innerHTML = expirations.map(exp => `
    <div class="calendar-card">
      <div class="cal-left">
        <span class="cal-code">${exp.code}</span>
        <span class="cal-month">${exp.month}</span>
        ${exp.active ? '<span class="cal-badge active">🔥 Активный контракт</span>' : ''}
      </div>
      <div class="cal-right">
        <span class="cal-date">Экспирация: <b>${exp.last_trade}</b></span>
        <span class="cal-days">Осталось: ${exp.days_left} дн.</span>
      </div>
    </div>
  `).join("");
}

// Render Cards
function renderCards() {
  const grid = document.getElementById("tickerGrid");
  if (!grid) return;

  const filtered = quotesData.filter(q => {
    if (currentCategory === "all") return true;
    return q.category === currentCategory;
  });

  grid.innerHTML = filtered.map(q => {
    const isSelected = q.symbol === selectedSymbol;
    const isPos = (q.change_pct || 0) >= 0;
    const chgClass = isPos ? "positive" : "negative";
    const chgSign = isPos ? "+" : "";

    return `
      <div class="ticker-card ${isSelected ? 'active-card' : ''}" id="card-${q.symbol}" onclick="selectSymbol('${q.symbol}')">
        <div class="card-top">
          <div class="card-sym-group">
            <span class="card-sym">${q.symbol}</span>
            <span class="card-name">${(q.name || '').split('(')[0]}</span>
          </div>
          <span class="card-change ${chgClass}">${chgSign}${(q.change_pct || 0).toFixed(2)}%</span>
        </div>
        <div class="card-middle">
          <span class="card-price" id="price-${q.symbol}">$${formatPrice(q.price)}</span>
          <span class="card-unit">${q.unit || ''}</span>
        </div>
        <div class="card-bottom">
          <span>Объем: <b>${formatCompact(q.volume)}</b></span>
          <span>OI: <b>${formatCompact(q.open_interest)}</b></span>
        </div>
      </div>
    `;
  }).join("");
}

// Select active symbol
window.selectSymbol = function(symbol) {
  selectedSymbol = symbol;
  tgHaptic("light");

  const quote = quotesData.find(q => q.symbol === symbol) || INITIAL_DATA.find(q => q.symbol === symbol);
  if (quote) {
    document.getElementById("chartSymbol").textContent = quote.symbol;
    document.getElementById("chartAssetName").textContent = quote.name;
    document.getElementById("chartPrice").textContent = `$${formatPrice(quote.price)}`;

    const chgEl = document.getElementById("chartChange");
    const isPos = (quote.change_pct || 0) >= 0;
    chgEl.className = `price-change ${isPos ? 'positive' : 'negative'}`;
    chgEl.textContent = `${isPos ? '+' : ''}${(quote.change_pct || 0).toFixed(2)}%`;
  }

  document.querySelectorAll(".ticker-card").forEach(c => c.classList.remove("active-card"));
  const activeCard = document.getElementById(`card-${symbol}`);
  if (activeCard) activeCard.classList.add("active-card");

  // Update views
  loadChartHistory(symbol);
  renderSpecs(symbol);
  renderCalendar(symbol);
};

// Switch view mode tabs (Chart vs Specs vs Calendar)
function setupViewSwitchTabs() {
  document.querySelectorAll(".view-tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".view-tab-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentViewMode = btn.dataset.view;
      tgHaptic("medium");

      document.querySelectorAll(".view-panel").forEach(p => p.classList.remove("active"));
      if (currentViewMode === "chart") {
        document.getElementById("chartViewWrapper").classList.add("active");
        if (chart) {
          const container = document.getElementById("chartContainer");
          chart.applyOptions({ width: container.clientWidth, height: 240 });
          chart.timeScale().fitContent();
        }
      } else if (currentViewMode === "specs") {
        document.getElementById("specsViewWrapper").classList.add("active");
        renderSpecs(selectedSymbol);
      } else if (currentViewMode === "calendar") {
        document.getElementById("calendarViewWrapper").classList.add("active");
        renderCalendar(selectedSymbol);
      }
    });
  });
}

// Handle Real-Time Updates
function handleQuotesUpdate(newQuotes) {
  if (!Array.isArray(newQuotes) || newQuotes.length === 0) return;

  newQuotes.forEach(q => {
    const prev = lastKnownPrices[q.symbol];
    if (prev !== undefined && prev !== q.price) {
      const card = document.getElementById(`card-${q.symbol}`);
      if (card) {
        card.classList.remove("flash-up", "flash-down");
        void card.offsetWidth;
        card.classList.add(q.price > prev ? "flash-up" : "flash-down");
      }
    }
    lastKnownPrices[q.symbol] = q.price;
  });

  quotesData = newQuotes;
  renderCards();

  const activeQuote = quotesData.find(q => q.symbol === selectedSymbol);
  if (activeQuote) {
    document.getElementById("chartPrice").textContent = `$${formatPrice(activeQuote.price)}`;
    const chgEl = document.getElementById("chartChange");
    const isPos = (activeQuote.change_pct || 0) >= 0;
    chgEl.className = `price-change ${isPos ? 'positive' : 'negative'}`;
    chgEl.textContent = `${isPos ? '+' : ''}${(activeQuote.change_pct || 0).toFixed(2)}%`;

    if (candleSeries && activeQuote.last_updated) {
      try {
        candleSeries.update({
          time: activeQuote.last_updated,
          open: activeQuote.price,
          high: activeQuote.high_price || activeQuote.price,
          low: activeQuote.low_price || activeQuote.price,
          close: activeQuote.price
        });
      } catch (e) {}
    }
  }

  const d = new Date();
  const lastUpdatedEl = document.getElementById("lastUpdated");
  if (lastUpdatedEl) lastUpdatedEl.textContent = d.toLocaleTimeString("ru-RU");
}

// WebSocket Connection
function connectWebSocket() {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws`;

  const statusPill = document.getElementById("connectionStatus");

  try {
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      if (statusPill) {
        statusPill.className = "status-pill connected";
        statusPill.querySelector(".status-text").textContent = "LIVE 10s";
      }
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg.type === "initial_snapshot" || msg.type === "quotes_update") {
          handleQuotesUpdate(msg.data);
        }
      } catch (e) {
        console.error("WS Parse error:", e);
      }
    };

    ws.onclose = () => {
      if (statusPill) {
        statusPill.className = "status-pill disconnected";
        statusPill.querySelector(".status-text").textContent = "Reconnecting";
      }
      setTimeout(connectWebSocket, 3000);
    };

    ws.onerror = () => {
      try { ws.close(); } catch (e) {}
    };
  } catch (err) {
    console.error("WS Init error, falling back to polling", err);
    setInterval(pollQuotes, 10000);
  }
}

async function pollQuotes() {
  try {
    const res = await fetch("/api/quotes");
    const data = await res.json();
    if (data.status === "ok" && Array.isArray(data.quotes)) {
      handleQuotesUpdate(data.quotes);
    }
  } catch (e) {
    console.error("Polling error:", e);
  }
}

// Category Tabs
document.querySelectorAll(".tab-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    currentCategory = btn.dataset.cat;
    tgHaptic("light");
    renderCards();
  });
});

// Timeframe Buttons
document.querySelectorAll(".tf-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tf-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    tgHaptic("medium");
    loadChartHistory(selectedSymbol);
  });
});

// QuikStrike Most Actives State & Logic
let currentMinOi = 1000;
let currentQsSymbol = "GC";
let lastCallsData = [];
let lastPutsData = [];
let sortState = { calls: { key: null, dir: 'desc' }, puts: { key: null, dir: 'desc' } };

const QS_INSTRUMENT_NAMES = {
  "GC": "Золото (Gold)",
  "SI": "Серебро (Silver)",
  "6E": "EUR/USD",
  "6B": "GBP/USD",
  "6A": "AUD/USD"
};

function sortDataByKey(data, key, dir) {
  return [...data].sort((a, b) => {
    let va = a[key], vb = b[key];
    if (typeof va === 'string') {
      return dir === 'asc' ? va.localeCompare(vb) : vb.localeCompare(va);
    }
    return dir === 'asc' ? va - vb : vb - va;
  });
}

function rerenderTableBody(tableType) {
  const data = tableType === 'calls' ? lastCallsData : lastPutsData;
  const state = sortState[tableType];
  const sorted = state.key ? sortDataByKey(data, state.key, state.dir) : data;
  const allChg = [...lastCallsData, ...lastPutsData].map(x => Math.abs(x.chg));
  const maxChg = Math.max(...allChg, 1);
  const bodyEl = document.getElementById(tableType === 'calls' ? 'callsTableBody' : 'putsTableBody');
  if (bodyEl) {
    if (sorted.length === 0) {
      bodyEl.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:20px; color:var(--text-muted);">Нет контрактов с OI ≥ ${formatCompact(currentMinOi)}</td></tr>`;
    } else {
      bodyEl.innerHTML = sorted.map(c => buildTableRow(c, maxChg)).join("");
    }
  }
  // Update sort indicators in headers
  const table = document.getElementById(tableType === 'calls' ? 'callsTable' : 'putsTable');
  if (table) {
    table.querySelectorAll('.sortable-th').forEach(th => {
      const baseText = th.textContent.replace(/ [⇅↑↓]$/, '');
      if (th.dataset.sort === state.key) {
        th.textContent = baseText + (state.dir === 'asc' ? ' ↑' : ' ↓');
        th.classList.add('sort-active');
      } else {
        th.textContent = baseText + ' ⇅';
        th.classList.remove('sort-active');
      }
    });
  }
}

function setupSortableHeaders() {
  document.querySelectorAll('.sortable-th').forEach(th => {
    th.addEventListener('click', () => {
      const key = th.dataset.sort;
      const tableType = th.dataset.table;
      const state = sortState[tableType];
      if (state.key === key) {
        state.dir = state.dir === 'desc' ? 'asc' : 'desc';
      } else {
        state.key = key;
        state.dir = 'desc';
      }
      tgHaptic("light");
      rerenderTableBody(tableType);
    });
  });
}

function switchMainPage(page) {
  tgHaptic("medium");
  document.querySelectorAll(".nav-tab").forEach(t => t.classList.remove("active"));
  const activeTab = document.querySelector(`.nav-tab[data-nav="${page}"]`);
  if (activeTab) activeTab.classList.add("active");

  document.querySelectorAll(".page-content").forEach(p => p.classList.remove("active"));
  if (page === "futures") {
    document.getElementById("pageFutures").classList.add("active");
    if (chart) {
      const container = document.getElementById("chartContainer");
      chart.applyOptions({ width: container.clientWidth, height: 240 });
      chart.timeScale().fitContent();
    }
  } else if (page === "quikstrike") {
    document.getElementById("pageQuikstrike").classList.add("active");
    renderQuikstrikeTables(currentMinOi, currentQsSymbol);
  }
}

function setupMainNav() {
  document.querySelectorAll(".nav-tab").forEach(tab => {
    tab.addEventListener("click", () => {
      switchMainPage(tab.dataset.nav);
    });
  });

  // Filter Pills for QuikStrike
  document.querySelectorAll(".filter-pill").forEach(pill => {
    pill.addEventListener("click", () => {
      document.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      currentMinOi = parseInt(pill.dataset.minoi, 10);
      tgHaptic("light");
      renderQuikstrikeTables(currentMinOi, currentQsSymbol);
    });
  });

  // Instrument Selector Pills for QuikStrike
  document.querySelectorAll(".instrument-pill").forEach(pill => {
    pill.addEventListener("click", () => {
      document.querySelectorAll(".instrument-pill").forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      currentQsSymbol = pill.dataset.qsSymbol;
      tgHaptic("medium");
      // Update subtitle
      const subtitle = document.getElementById("qsSubtitle");
      if (subtitle) {
        subtitle.textContent = `CME QuikStrike™ Options Open Interest Profile • ${QS_INSTRUMENT_NAMES[currentQsSymbol] || currentQsSymbol}`;
      }
      // Reset sort state when switching instrument
      sortState = { calls: { key: null, dir: 'desc' }, puts: { key: null, dir: 'desc' } };
      renderQuikstrikeTables(currentMinOi, currentQsSymbol);
    });
  });
}

function buildTableRow(item, maxChg) {
  const isPos = item.chg > 0;
  const chgClass = isPos ? "chg-positive" : "chg-negative";
  const chgSign = isPos ? "+" : "";
  const barClass = isPos ? "mini-bar-fill-green" : "mini-bar-fill-red";
  const barWidth = Math.min(100, Math.max(12, Math.round((Math.abs(item.chg) / maxChg) * 100)));

  return `
    <tr>
      <td class="strike-val">${item.strike}</td>
      <td class="exp-code">${item.exp}</td>
      <td>${formatCompact(item.vol)}</td>
      <td>${formatCompact(item.prev_oi)}</td>
      <td style="font-weight:600;">${formatCompact(item.curr_oi)}</td>
      <td class="${chgClass}">${chgSign}${formatCompact(item.chg)}</td>
      <td class="chg-bar-cell">
        <div class="mini-bar-track">
          <div class="${barClass}" style="width: ${barWidth}%;"></div>
        </div>
      </td>
    </tr>
  `;
}

async function renderQuikstrikeTables(minOi = 1000, symbol = "GC") {
  try {
    const res = await fetch(`/api/options/most-actives?min_oi=${minOi}&symbol=${symbol}`);
    const resData = await res.json();
    if (resData.status === "ok" && resData.data) {
      const { calls, puts } = resData.data;

      // Store data for sorting
      lastCallsData = calls;
      lastPutsData = puts;

      // Find max change for visual bar scaling
      const allChg = [...calls, ...puts].map(x => Math.abs(x.chg));
      const maxChg = Math.max(...allChg, 1);

      // Apply current sort if any
      const sortedCalls = sortState.calls.key ? sortDataByKey(calls, sortState.calls.key, sortState.calls.dir) : calls;
      const sortedPuts = sortState.puts.key ? sortDataByKey(puts, sortState.puts.key, sortState.puts.dir) : puts;

      // Render Calls
      const callsBody = document.getElementById("callsTableBody");
      if (callsBody) {
        if (sortedCalls.length === 0) {
          callsBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:20px; color:var(--text-muted);">Нет контрактов с OI ≥ ${formatCompact(minOi)}</td></tr>`;
        } else {
          callsBody.innerHTML = sortedCalls.map(c => buildTableRow(c, maxChg)).join("");
        }
      }

      // Render Puts
      const putsBody = document.getElementById("putsTableBody");
      if (putsBody) {
        if (sortedPuts.length === 0) {
          putsBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:20px; color:var(--text-muted);">Нет контрактов с OI ≥ ${formatCompact(minOi)}</td></tr>`;
        } else {
          putsBody.innerHTML = sortedPuts.map(p => buildTableRow(p, maxChg)).join("");
        }
      }

      // Update counters
      const callsCountEl = document.getElementById("callsCount");
      if (callsCountEl) callsCountEl.textContent = calls.length;

      const putsCountEl = document.getElementById("putsCount");
      if (putsCountEl) putsCountEl.textContent = puts.length;

      const maxInflowEl = document.getElementById("maxInflow");
      if (maxInflowEl) {
        const topCall = calls.slice().sort((a,b) => b.chg - a.chg)[0];
        if (topCall && topCall.chg > 0) {
          maxInflowEl.textContent = `+${formatCompact(topCall.chg)} (${topCall.strike} C)`;
        }
      }
    }
  } catch (err) {
    console.error("Error loading QuikStrike tables:", err);
  }
}

// Start App immediately
window.addEventListener("DOMContentLoaded", () => {
  renderCards();
  setupViewSwitchTabs();
  setupMainNav();
  setupSortableHeaders();

  try {
    initChart();
    selectSymbol("GC");
  } catch (e) {
    console.error("initChart error:", e);
  }

  pollQuotes();
  connectWebSocket();

  // Default: open QuikStrike tab
  if (window.location.hash === "#futures") {
    switchMainPage("futures");
  } else {
    // Load QuikStrike as default page
    renderQuikstrikeTables(1000, currentQsSymbol);
  }
});

