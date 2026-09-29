import subprocess
import time
import json
import urllib.request
import asyncio
import websockets

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def check():
    proc = subprocess.Popen([
        CHROME_PATH,
        "--headless=new",
        "--remote-debugging-port=9995",
        "--no-sandbox",
        "--disable-gpu",
        "https://corebox-project.pages.dev"
    ])
    await asyncio.sleep(3)
    tabs = json.loads(urllib.request.urlopen("http://localhost:9995/json").read().decode())
    target = [t for t in tabs if "corebox" in t.get("url", "")][0]
    
    with open("chrome_console_dump.txt", "w", encoding="utf-8") as out:
        async with websockets.connect(target["webSocketDebuggerUrl"]) as ws:
            await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Log.enable"}))
            
            start = time.time()
            while time.time() - start < 20:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                    data = json.loads(msg)
                    out.write(json.dumps(data) + "\n")
                    out.flush()
                except asyncio.TimeoutError:
                    pass

    proc.terminate()
    proc.wait()

asyncio.run(check())
