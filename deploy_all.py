"""
One-command script to:
1. Recompile single-page bundle (build_pages.py)
2. Commit and push changes to GitHub
3. Deploy directly to Cloudflare Pages (deploy_cloudflare.py)
"""
import sys
import subprocess
import os

def run(cmd, desc):
    print(f"\n--> {desc}...")
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print(f"[ERROR] Step failed with return code {res.returncode}: {cmd}")
        return False
    return True

def main():
    commit_msg = "Update Corebox application and deploy"
    if len(sys.argv) > 1:
        commit_msg = " ".join(sys.argv[1:])

    # 1. Build pages bundle
    if not run("python build_pages.py", "Building Single-Page Bundle"):
        sys.exit(1)

    # 2. Git add and commit
    run("git add .", "Staging Git changes")
    
    # Check if there are changes to commit
    status = subprocess.check_output("git status --porcelain", shell=True, text=True).strip()
    if status:
        run(f'git commit -m "{commit_msg}"', "Committing Git changes")
    else:
        print("No new Git changes to commit.")

    # 3. Git push
    run("git push origin main", "Pushing to GitHub")

    # 4. Deploy to Cloudflare Pages
    if not run("python deploy_cloudflare.py", "Deploying to Cloudflare Pages"):
        sys.exit(1)

    print("\n[ALL DONE] Build, GitHub Push, and Cloudflare Pages Deployment completed successfully!")

if __name__ == "__main__":
    main()
