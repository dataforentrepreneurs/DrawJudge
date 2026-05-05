from playwright.sync_api import sync_playwright
import time
import os

artifact_dir = r"C:\Users\sahai\.gemini\antigravity\brain\23e276e4-eaa4-43f1-b5cb-73fea4f4e787"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    # Launcher
    page.goto("http://localhost:3001/")
    time.sleep(2)
    page.screenshot(path=os.path.join(artifact_dir, "before_launcher.png"))

    # Draw Judge
    page.goto("http://localhost:3001/drawjudge/index.html")
    time.sleep(2)
    page.screenshot(path=os.path.join(artifact_dir, "before_drawjudge.png"))

    # Couple Clash
    page.goto("http://localhost:3001/coupleclash/index.html")
    time.sleep(2)
    page.screenshot(path=os.path.join(artifact_dir, "before_coupleclash.png"))

    browser.close()
