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

async def check():
    proc = subprocess.Popen([
        CHROME_PATH,
        "--headless=new",
        "--remote-debugging-port=9996",
        "--no-sandbox",
        "--disable-gpu",
        "--window-size=1440,900",
        "https://corebox-project.pages.dev"
    ])
    await asyncio.sleep(3)
    tabs = json.loads(urllib.request.urlopen("http://localhost:9996/json").read().decode())
    target = [t for t in tabs if "corebox" in t.get("url", "")][0]
    
    async with websockets.connect(target["webSocketDebuggerUrl"]) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
        await ws.send(json.dumps({"id": 2, "method": "Page.enable"}))
        
        # Wait 25 seconds for full Stlite boot & render
        print("Waiting 25 seconds for Stlite Pyodide to finish rendering...", flush=True)
        await asyncio.sleep(25)
        
        # Eval text
        await ws.send(json.dumps({
            "id": 10,
            "method": "Runtime.evaluate",
            "params": {"expression": "document.body.innerText"}
        }))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("id") == 10:
                text = data.get("result", {}).get("result", {}).get("value", "")
                print(f"BODY TEXT ({len(text)} chars):\n{text[:300]}...", flush=True)
                break
        
        # Screenshot
        await ws.send(json.dumps({"id": 20, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("id") == 20:
                b64 = data.get("result", {}).get("data", "")
                out_path = os.path.join(ARTIFACT_DIR, "live_home_verified.png")
                with open(out_path, "wb") as f:
                    f.write(base64.b64decode(b64))
                print(f"Screenshot saved: {out_path} ({os.path.getsize(out_path)} bytes)", flush=True)
                break

        # Now test navigating to users page
        print("\nNavigating to ?page=users ...", flush=True)
        await ws.send(json.dumps({
            "id": 30,
            "method": "Page.navigate",
            "params": {"url": "https://corebox-project.pages.dev/?page=users"}
        }))
        await asyncio.sleep(8)
        
        await ws.send(json.dumps({
            "id": 40,
            "method": "Runtime.evaluate",
            "params": {"expression": "document.body.innerText"}
        }))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("id") == 40:
                text = data.get("result", {}).get("result", {}).get("value", "")
                print(f"USERS BODY TEXT ({len(text)} chars):\n{text[:300]}...", flush=True)
                break

        await ws.send(json.dumps({"id": 50, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("id") == 50:
                b64 = data.get("result", {}).get("data", "")
                out_path = os.path.join(ARTIFACT_DIR, "live_users_verified.png")
                with open(out_path, "wb") as f:
                    f.write(base64.b64decode(b64))
                print(f"Screenshot saved: {out_path} ({os.path.getsize(out_path)} bytes)", flush=True)
                break

    proc.terminate()
    proc.wait()

asyncio.run(check())
