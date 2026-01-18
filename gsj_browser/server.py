from fastapi import FastAPI
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
import os

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(req: LoginRequest):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context()
        page = context.new_page()

        page.goto("http://gsj-energia.com/login", wait_until="networkidle")

        page.fill('input[name="username"]', req.username)
        page.fill('input[name="password"]', req.password)
        page.click('button[type="submit"]')

        page.wait_for_load_state("networkidle")

        cookies = context.cookies()
        browser.close()

        result = {}
        for c in cookies:
            if c["name"] in ("gsj_session", "XSRF-TOKEN"):
                result[c["name"]] = c["value"]

        if "gsj_session" not in result:
            return {"error": "Login failed", "cookies": result}

        return {"cookies": result}
