import asyncio
import os
from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright
import httpx

DEVICE_ID = 414
DEVICE_NAME = "GSJ_ANT_ZAW_407"
BASE_URL = "http://gsj-energia.com"

app = FastAPI()

playwright = None
browser = None
context = None
page = None
session_cookies = {}

def load_secrets():
    username = os.environ.get("GSJ_USERNAME")
    password = os.environ.get("GSJ_PASSWORD")
    if not username or not password:
        raise RuntimeError("Brak GSJ_USERNAME lub GSJ_PASSWORD w konfiguracji add-onu")
    return username, password

async def login():
    global playwright, browser, context, page, session_cookies

    username, password = load_secrets()

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True, args=["--no-sandbox"])
    context = await browser.new_context()
    page = await context.new_page()

    await page.goto(f"{BASE_URL}/login", wait_until="networkidle")
    await page.fill('input[name="username"]', username)
    await page.fill('input[name="password"]', password)
    await page.click('button[type="submit"]')
    await page.wait_for_load_state("networkidle")

    cookies = await context.cookies()
    session_cookies = {c["name"]: c["value"] for c in cookies}

    if "gsj_session" not in session_cookies:
        raise RuntimeError("Logowanie nie powiodło się – brak ciasteczka sesji gsj_session")

async def ensure_login():
    if not session_cookies:
        await login()

async def gsj_get(path: str):
    await ensure_login()
    async with httpx.AsyncClient(cookies=session_cookies) as client:
        r = await client.get(f"{BASE_URL}{path}")
        r.raise_for_status()
        return r.json()

async def gsj_post(path: str):
    await ensure_login()
    async with httpx.AsyncClient(cookies=session_cookies) as client:
        r = await client.post(f"{BASE_URL}{path}")
        r.raise_for_status()
        return r.text

@app.on_event("startup")
async def startup_event():
    await login()

@app.get("/health")
async def health():
    return {"status": "ok", "session": "active"}

@app.get("/sensors")
async def sensors():
    data = await gsj_get(f"/get-device-params?deviceName={DEVICE_NAME}")

    def val(key):
        try:
            return float(data.get(key, 0))
        except:
            return 0.0

    return {
        "temperatura_zew": val("TEMPERATURA_ZEW"),
        "temperatura_cwu": val("TEMPERATURA_CWU"),
        "temperatura_bufor": val("TEMPERATURA_BUF"),
        "co_zadana": val("CO_ZADANA"),
        "cwu_zadana": val("CWU_ZADANA"),
        "co_status": int(val("CO_STATUS")),
        "cwu_status": int(val("CWU_STATUS")),
        "temp_parownik": val("TEMP_PAROWNIK"),
        "temp_gaz_parowanie": val("TEMP_GAZ_PAROWANIE"),
    }

@app.post("/set/co/{state}")
async def set_co(state: int):
    if state not in (0, 1):
        raise HTTPException(400, "state must be 0 or 1")
    await gsj_post(f"/set-user-cache?deviceId={DEVICE_ID}&key=CO_STATUS&value={state}")
    return {"co_status": state}

@app.post("/set/cwu/{state}")
async def set_cwu(state: int):
    if state not in (0, 1):
        raise HTTPException(400, "state must be 0 or 1")
    await gsj_post(f"/set-user-cache?deviceId={DEVICE_ID}&key=CWU_STATUS&value={state}")
    return {"cwu_status": state}

@app.post("/set/temperature/co/{value}")
async def set_co_temp(value: float):
    await gsj_post(f"/set-user-cache?deviceId={DEVICE_ID}&key=CO_ZADANA&value={value}")
    return {"co_zadana": value}

@app.post("/set/temperature/cwu/{value}")
async def set_cwu_temp(value: float):
    await gsj_post(f"/set-user-cache?deviceId={DEVICE_ID}&key=CWU_ZADANA&value={value}")
    return {"cwu_zadana": value}
