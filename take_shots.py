"""Website ke screenshots leta hai (login + main page) PPT ke liye."""
import time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5000"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    # 1) Login page
    page.goto(f"{BASE}/login")
    page.wait_for_timeout(1500)
    page.screenshot(path="shot_login.png", full_page=False)
    print("login page screenshot ho gaya")

    # 2) Login karke main page
    page.fill("#username", "vikas yadav")
    page.fill("#password", "pit jaunpur")
    page.click("#loginBtn")
    page.wait_for_timeout(2500)  # animations settle hone do
    page.screenshot(path="shot_home.png", full_page=False)
    print("main page screenshot ho gaya")

    # 3) Form bharke + predict karke result page
    page.fill("#tenth_percent", "85")
    page.fill("#twelfth_percent", "80")
    page.fill("#cgpa", "8.2")
    page.fill("#internships", "2")
    page.fill("#projects", "4")
    page.fill("#aptitude_score", "78")
    page.fill("#communication_score", "82")
    page.select_option("#work_experience", "1")
    page.wait_for_timeout(800)
    page.screenshot(path="shot_form.png", full_page=False)
    print("filled form screenshot ho gaya")

    page.click("#submitBtn")
    page.wait_for_timeout(4500)  # scan + result animations
    page.screenshot(path="shot_result.png", full_page=False)
    print("result page screenshot ho gaya")

    browser.close()

print("Sab screenshots taiyar hain!")
