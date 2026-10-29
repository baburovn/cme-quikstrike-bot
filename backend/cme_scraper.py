import asyncio
import json
import logging
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Any, Tuple

# Ensure backend directory is in sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from playwright.async_api import async_playwright

try:
    import config
except ImportError:
    from backend import config

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("cme-scraper")

CACHE_FILE = Path(__file__).resolve().parent / "quikstrike_cache.json"
TZ_MSK = timezone(timedelta(hours=3))

PRODUCTS = [
    {"sym": "GC", "pid": 40, "name": "Gold (Золото)"},
    {"sym": "SI", "pid": 41, "name": "Silver (Серебро)"},
    {"sym": "6E", "pid": 350, "name": "EUR/USD"},
    {"sym": "6B", "pid": 354, "name": "GBP/USD"},
    {"sym": "6A", "pid": 351, "name": "AUD/USD"},
]


def parse_numeric(v: str):
    """Converts strings like '4,500', '(197)', '-' to float or int."""
    if not v:
        return 0
    v = v.replace(",", "").strip()
    if v.startswith("(") and v.endswith(")"):
        inner = v[1:-1].strip()
        try:
            return -int(float(inner))
        except ValueError:
            return -1
    if v == "-" or v == "":
        return 0
    try:
        f = float(v)
        return int(f) if f.is_integer() else f
    except ValueError:
        return v


def parse_table_rows(table_data: list, option_type: str) -> Tuple[list, str, str]:
    """
    Parses table data from QuikStrike Most Actives.
    Row 0: Column headers
    Row 1: Date headers (e.g. OCT 16 | OCT 19 | CHG)
    Row 2+: Data rows
    """
    if len(table_data) < 3:
        return [], "", ""

    # Parse dates from Row 1
    date_row = table_data[1]
    prev_date = date_row[0] if len(date_row) > 0 else "ПРОШЛ"
    curr_date = date_row[1] if len(date_row) > 1 else "ТЕКУЩ"

    items = []
    for r in table_data[2:]:
        if len(r) < 6:
            continue
        try:
            strike = parse_numeric(r[0])
            exp = str(r[1]).strip()
            vol = int(parse_numeric(r[2]))
            prev_oi = int(parse_numeric(r[3]))
            curr_oi = int(parse_numeric(r[4]))
            chg = int(parse_numeric(r[5]))

            items.append({
                "strike": strike,
                "exp": exp,
                "vol": vol,
                "prev_oi": prev_oi,
                "curr_oi": curr_oi,
                "chg": chg,
                "type": option_type
            })
        except Exception as e:
            logger.debug(f"Row parse error: {e} for row {r}")

    return items, prev_date, curr_date


async def run_scraper() -> Tuple[bool, str]:
    """
    Performs CME Group login and scrapes QuikStrike Most Actives for all 5 products.
    Saves parsed results to quikstrike_cache.json.
    """
    login = config.CME_LOGIN
    password = config.CME_PASSWORD

    if not login or not password:
        msg = "CME_LOGIN or CME_PASSWORD not set in cme_credentials.py"
        logger.error(msg)
        return False, msg

    logger.info(f"Starting CME QuikStrike scraper with account: {login}")
    scraped_data = {}
    scraped_meta = {}

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            # 1. Login to CME
            logger.info("Step 1: Navigating to CME SSO login...")
            await page.goto("https://login.cmegroup.com/sso/ssologin.action")
            await page.wait_for_selector("#user", state="attached", timeout=25000)
            await page.type("#user", login, delay=35)
            await page.type("#pwd", password, delay=35)
            await page.click("#loginBtn")

            # Wait for SAML authentication to complete
            logger.info("Waiting for login redirect to complete...")
            logged_in = False
            for _ in range(20):
                await asyncio.sleep(1)
                u = page.url
                if "cmegroup.com" in u and "login" not in u and "auth" not in u:
                    logged_in = True
                    break

            if not logged_in:
                logger.warning(f"Did not detect final cmegroup.com URL, current URL: {page.url}. Continuing anyway...")

            # 2. Scrape each product
            for prod in PRODUCTS:
                sym = prod["sym"]
                pid = prod["pid"]
                pname = prod["name"]
                url = f"https://www.cmegroup.com/tools-information/quikstrike/options-open-interest-profile.html?pid={pid}"
                logger.info(f"Scraping product {sym} ({pname}) from {url}...")

                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=30000)

                    # Locate the QuikStrike iframe (with retry wait)
                    qs_frame = None
                    for _ in range(15):
                        for f in page.frames:
                            if "quikstrike.net" in f.url and "ErrorPage" not in f.url:
                                qs_frame = f
                                break
                        if qs_frame:
                            break
                        await asyncio.sleep(1)

                    if not qs_frame:
                        logger.error(f"QuikStrike iframe not found for {sym}")
                        continue

                    # Click 'Most Actives' link
                    link_sel = "#MainContent_ucViewControl_IntegratedOpenInterestTool_lbMostActives"
                    await qs_frame.wait_for_selector(link_sel, timeout=20000)
                    await qs_frame.click(link_sel)
                    await asyncio.sleep(6)

                    # Extract all grid-thm tables
                    table_rows = await qs_frame.eval_on_selector_all(
                        "table.grid-thm",
                        """els => els.map(e => Array.from(e.rows).map(r => Array.from(r.cells).map(c => c.innerText.trim())))"""
                    )

                    # Filter only the tables with actual strike data (>= 10 rows)
                    data_tables = [t for t in table_rows if len(t) >= 10]
                    if len(data_tables) < 2:
                        logger.warning(f"Expected at least 2 data tables for {sym}, found {len(data_tables)} (total grid tables: {len(table_rows)})")
                        continue

                    calls, prev_d, curr_d = parse_table_rows(data_tables[0], "CALL")
                    puts, _, _ = parse_table_rows(data_tables[1], "PUT")

                    logger.info(f"Parsed {sym}: {len(calls)} calls, {len(puts)} puts (Dates: {prev_d} -> {curr_d})")

                    scraped_data[sym] = {
                        "calls": calls,
                        "puts": puts
                    }
                    scraped_meta[sym] = {
                        "report": "Most Actives (Top 25 by Open Interest Change)",
                        "instrument": pname,
                        "prev_date": prev_d,
                        "curr_date": curr_d,
                        "source_url": url
                    }

                except Exception as e:
                    logger.error(f"Error scraping {sym}: {e}")

            await browser.close()

    except Exception as e:
        msg = f"Browser error during scraping: {e}"
        logger.error(msg)
        return False, msg

    if not scraped_data:
        msg = "Scraper ran but failed to extract any data."
        logger.warning(msg)
        return False, msg

    # Save to cache file
    cache_payload = {
        "updated_at": datetime.now(TZ_MSK).strftime("%Y-%m-%d %H:%M:%S (МСК)"),
        "date_key": datetime.now(TZ_MSK).strftime("%Y-%m-%d"),
        "metadata": scraped_meta,
        "data": scraped_data
    }

    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_payload, f, ensure_ascii=False, indent=2)
        logger.info(f"Successfully saved scraped data to {CACHE_FILE}")
        return True, f"Успешно спарсены данные по {len(scraped_data)} инструментам!"
    except Exception as e:
        msg = f"Error saving cache: {e}"
        logger.error(msg)
        return False, msg


if __name__ == "__main__":
    success, msg = asyncio.run(run_scraper())
    print(f"Result: {success} | {msg}")
