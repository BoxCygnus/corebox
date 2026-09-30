"""
Automated deployment script for Corebox to Cloudflare Pages via Cloudflare Direct Upload API.
"""
import os
import sys
import mimetypes
import hashlib
import base64
import json
import time
import subprocess
import requests

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

load_env()

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
PROJECT_NAME = os.getenv("CLOUDFLARE_PROJECT_NAME", "corebox-project")
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")

def get_git_info():
    try:
        commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        commit_msg = subprocess.check_output(["git", "log", "-1", "--pretty=%B"], text=True).strip().splitlines()[0]
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
        return branch, commit_hash, commit_msg
    except Exception:
        return "main", "", "Automated deployment"

def deploy():
    print(f"=== [Corebox] Deploying to Cloudflare Pages ({PROJECT_NAME}) ===")
    
    if not ACCOUNT_ID or not API_TOKEN:
        print("Error: CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN must be set in .env file.")
        sys.exit(1)

    if not os.path.exists(PUBLIC_DIR):
        print(f"Error: public directory not found at {PUBLIC_DIR}")
        sys.exit(1)

    # 1. Collect files
    manifest = {}
    files_map = {}
    
    for root, _, files in os.walk(PUBLIC_DIR):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = "/" + os.path.relpath(full_path, PUBLIC_DIR).replace("\\", "/")
            with open(full_path, "rb") as fp:
                data = fp.read()
            
            fhash = hashlib.md5(data).hexdigest()
            manifest[rel_path] = fhash
            content_type, _ = mimetypes.guess_type(full_path)
            if not content_type:
                content_type = "application/octet-stream"
            
            files_map[fhash] = {
                "key": fhash,
                "value": base64.b64encode(data).decode("ascii"),
                "metadata": {"contentType": content_type},
                "base64": True,
                "rel_path": rel_path
            }

    print(f"Found {len(manifest)} asset(s) to deploy.")

    # 2. Get Upload Token (JWT)
    auth_headers = {"Authorization": f"Bearer {API_TOKEN}"}
    token_url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/upload-token"
    res = requests.get(token_url, headers=auth_headers)
    if res.status_code != 200 or not res.json().get("success"):
        print(f"Failed to get upload token: {res.status_code} {res.text}")
        sys.exit(1)
    jwt = res.json()["result"]["jwt"]

    # 3. Check Missing Hashes
    check_url = "https://api.cloudflare.com/client/v4/pages/assets/check-missing"
    jwt_headers = {"Authorization": f"Bearer {jwt}", "Content-Type": "application/json"}
    all_hashes = list(files_map.keys())
    
    res = requests.post(check_url, headers=jwt_headers, json={"hashes": all_hashes})
    missing_hashes = set()
    if res.status_code == 200 and res.json().get("success"):
        missing_hashes = set(res.json().get("result", []))
    else:
        # Default to uploading all if check fails
        missing_hashes = set(all_hashes)

    print(f"Assets to upload: {len(missing_hashes)} / {len(all_hashes)}")

    # 4. Upload missing assets
    if missing_hashes:
        batch = [files_map[h] for h in missing_hashes]
        upload_payload = [{k: v for k, v in item.items() if k != "rel_path"} for item in batch]
        upload_url = "https://api.cloudflare.com/client/v4/pages/assets/upload"
        res = requests.post(upload_url, headers=jwt_headers, json=upload_payload)
        if res.status_code != 200 or not res.json().get("success"):
            print(f"Failed to upload assets: {res.status_code} {res.text}")
            sys.exit(1)
        print("Asset upload completed successfully.")

    # 5. Upsert Hashes
    upsert_url = "https://api.cloudflare.com/client/v4/pages/assets/upsert-hashes"
    res = requests.post(upsert_url, headers=jwt_headers, json={"hashes": all_hashes})
    if res.status_code != 200 or not res.json().get("success"):
        print(f"Warning on upsert hashes: {res.status_code} {res.text}")

    # 6. Trigger Deployment
    deploy_url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/deployments"
    branch, commit_hash, commit_msg = get_git_info()
    
    form_data = {
        "branch": branch,
        "commit_hash": commit_hash,
        "commit_message": commit_msg
    }
    
    files = {
        "manifest": (None, json.dumps(manifest), "application/json")
    }
    
    res = requests.post(deploy_url, headers=auth_headers, data=form_data, files=files)
    if res.status_code != 200 or not res.json().get("success"):
        print(f"Failed to trigger deployment: {res.status_code} {res.text}")
        sys.exit(1)

    deployment_data = res.json()["result"]
    dep_id = deployment_data["id"]
    preview_url = deployment_data.get("url", f"https://{deployment_data['short_id']}.{PROJECT_NAME}.pages.dev")
    print(f"Deployment created! ID: {dep_id}")
    print(f"Preview URL: {preview_url}")

    # 7. Poll status
    print("Waiting for deployment build & deploy to complete...")
    for _ in range(15):
        time.sleep(2)
        status_url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/deployments/{dep_id}"
        s_res = requests.get(status_url, headers=auth_headers)
        if s_res.status_code == 200:
            stage = s_res.json()["result"].get("latest_stage", {})
            status = stage.get("status")
            if status == "success":
                print(f"[SUCCESS] Cloudflare Pages deployment completed!")
                print(f"Live Production URL: https://{PROJECT_NAME}.pages.dev/")
                return
            elif status == "failure":
                print(f"[FAILED] Deployment stage {stage.get('name')} failed.")
                sys.exit(1)

    print(f"Deployment is still processing in background. Check at: https://{PROJECT_NAME}.pages.dev/")

if __name__ == "__main__":
    deploy()
