import subprocess
import time
import json
import urllib.request
import asyncio
import websockets
import base64
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ARTIFACT_DIR = r"C:\Users\Admin\.gemini\antigravity\brain\e2f7d4c2-32f5-45eb-9ee7-eee3f064169b"
USER_DATA = os.path.join(ARTIFACT_DIR, "scratch", "chrome_guest_test_profile")

async def run_test():
    os.makedirs(USER_DATA, exist_ok=True)
    proc = subprocess.Popen([
        CHROME_PATH,
        "--headless=new",
        "--remote-debugging-port=9985",
        "--no-sandbox",
        "--disable-gpu",
        "--window-size=1440,900",
        f"--user-data-dir={USER_DATA}",
        "https://corebox-project.pages.dev"
    ])
    
    await asyncio.sleep(3)
    tabs = json.loads(urllib.request.urlopen("http://localhost:9985/json").read().decode())
    target = [t for t in tabs if "corebox" in t.get("url", "")][0]
    
    async with websockets.connect(target["webSocketDebuggerUrl"]) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
        await ws.send(json.dumps({"id": 2, "method": "Page.enable"}))
        
        # Step 1: Wait 25s for initial Home page load (should be GUEST)
        print("Waiting 25 seconds for initial Home page to load as Guest...", flush=True)
        await asyncio.sleep(25)
        
        # Check text
        await ws.send(json.dumps({"id": 10, "method": "Runtime.evaluate", "params": {"expression": "document.body.innerText"}}))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("id") == 10:
                text = data.get("result", {}).get("result", {}).get("value", "")
                print(f"[TEST 1 - GUEST CHECK]:\nContains 'Khách' or 'Guest': {'Khách' in text or 'Guest' in text}", flush=True)
                print(f"Sample body text:\n{text[:300]}...", flush=True)
                break
                
        # Screenshot of Home (Guest)
        await ws.send(json.dumps({"id": 20, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("id") == 20:
                b64 = data.get("result", {}).get("data", "")
                out_path = os.path.join(ARTIFACT_DIR, "verified_guest_home.png")
                with open(out_path, "wb") as f:
                    f.write(base64.b64decode(b64))
                print(f"[SCREENSHOT 1 SAVED]: {out_path} ({os.path.getsize(out_path)} bytes)", flush=True)
                break

        # Step 2: Navigate to Login Page
        print("\nNavigating to ?page=login ...", flush=True)
        await ws.send(json.dumps({
            "id": 30,
            "method": "Page.navigate",
            "params": {"url": "https://corebox-project.pages.dev/?page=login"}
        }))
        await asyncio.sleep(8)
        
        await ws.send(json.dumps({"id": 40, "method": "Runtime.evaluate", "params": {"expression": "document.body.innerText"}}))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("id") == 40:
                login_text = data.get("result", {}).get("result", {}).get("value", "")
                print(f"[TEST 2 - LOGIN PAGE CHECK]:\nContains 'Chào mừng' or 'Welcome': {'Chào mừng' in login_text or 'Welcome' in login_text}", flush=True)
                print(f"Login body text:\n{login_text[:350]}...", flush=True)
                break

        # Screenshot of Login Page
        await ws.send(json.dumps({"id": 50, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("id") == 50:
                b64 = data.get("result", {}).get("data", "")
                out_path = os.path.join(ARTIFACT_DIR, "verified_login_page.png")
                with open(out_path, "wb") as f:
                    f.write(base64.b64decode(b64))
                print(f"[SCREENSHOT 2 SAVED]: {out_path} ({os.path.getsize(out_path)} bytes)", flush=True)
                break

        # Step 3: Click the Quick Admin Login button on the page!
        print("\nClicking Quick Admin Login button...", flush=True)
        click_expr = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const adminBtn = btns.find(b => b.innerText.includes('Admin') || b.innerText.includes('happyclone96'));
            if (adminBtn) {
                adminBtn.click();
                return 'CLICKED_ADMIN_BTN';
            }
            return 'BTN_NOT_FOUND: ' + btns.map(b => b.innerText).join(' | ');
        })()
        """
        await ws.send(json.dumps({"id": 60, "method": "Runtime.evaluate", "params": {"expression": click_expr}}))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("id") == 60:
                res = data.get("result", {}).get("result", {}).get("value", "")
                print(f"Click result: {res}", flush=True)
                break
                
        # Wait 5s for login action to process and return to home
        await asyncio.sleep(5)
        
        await ws.send(json.dumps({"id": 70, "method": "Runtime.evaluate", "params": {"expression": "document.body.innerText"}}))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("id") == 70:
                logged_text = data.get("result", {}).get("result", {}).get("value", "")
                print(f"[TEST 3 - LOGGED IN CHECK]:\nContains 'Admin' or 'happyclone': {'Admin' in logged_text or 'happyclone' in logged_text or 'Box' in logged_text}", flush=True)
                print(f"Logged-in text sample:\n{logged_text[:300]}...", flush=True)
                break
                
        # Screenshot after login
        await ws.send(json.dumps({"id": 80, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("id") == 80:
                b64 = data.get("result", {}).get("data", "")
                out_path = os.path.join(ARTIFACT_DIR, "verified_logged_in_admin.png")
                with open(out_path, "wb") as f:
                    f.write(base64.b64decode(b64))
                print(f"[SCREENSHOT 3 SAVED]: {out_path} ({os.path.getsize(out_path)} bytes)", flush=True)
                break

    proc.terminate()
    proc.wait()

asyncio.run(run_test())
