#!/usr/bin/env python3
"""
PromptHook AI - Fast Google Indexing Submitter
Uses verified Google OAuth2 credentials to dispatch batch URL_UPDATED notifications
directly to Google Indexing API and ping search engines.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.parse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# Find token files
TOKEN_PATHS = [
    os.path.join(os.path.dirname(__file__), "google_tokens.json"),
    r"C:\Users\er\Desktop\ozsponsorjobs.site\google_tokens.json",
    os.path.expanduser(r"~\Desktop\ozsponsorjobs.site\google_tokens.json"),
]

SECRET_PATHS = [
    os.path.join(os.path.dirname(__file__), "google_client_secret.json"),
    r"C:\Users\er\Desktop\ozsponsorjobs.site\google_client_secret.json",
    os.path.expanduser(r"~\Desktop\ozsponsorjobs.site\google_client_secret.json"),
]

def find_file(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def get_access_token():
    token_file = find_file(TOKEN_PATHS)
    secret_file = find_file(SECRET_PATHS)
    if not token_file or not secret_file:
        raise FileNotFoundError("Google credentials files not found.")
    
    with open(token_file, "r", encoding="utf-8") as f:
        tokens = json.load(f)
    with open(secret_file, "r", encoding="utf-8") as f:
        secrets = json.load(f)

    client_id = secrets.get("installed", {}).get("client_id")
    client_secret = secrets.get("installed", {}).get("client_secret")
    refresh_token = tokens.get("refresh_token")

    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }).encode("utf-8")

    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res["access_token"]

def submit_url(url, access_token):
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    payload = {
        "url": url,
        "type": "URL_UPDATED"
    }
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except Exception as e:
        return 500, str(e)

def ping_search_engines(sitemap_url):
    results = {}
    pings = [
        ("Google Ping", f"https://www.google.com/ping?sitemap={urllib.parse.quote(sitemap_url)}"),
        ("Bing Ping", f"https://www.bing.com/ping?sitemap={urllib.parse.quote(sitemap_url)}")
    ]
    for name, p_url in pings:
        try:
            req = urllib.request.Request(p_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                results[name] = resp.getcode()
        except Exception as e:
            results[name] = str(e)
    return results

def main():
    print("[+] Authenticating with Google OAuth 2.0...")
    access_token = get_access_token()
    print("[✓] Access token acquired successfully!")

    # Priority URLs
    priority_urls = [
        "https://www.prompthookai.com/",
        # 4 Flagship Late 2026 Blueprints
        "https://www.prompthookai.com/2026/10/grok-3-deepsearch-realtime-intelligence.html",
        "https://www.prompthookai.com/2026/10/cursorrules-claude-codebase-directive.html",
        "https://www.prompthookai.com/2026/10/hybrid-reasoning-thinking-budget-controller.html",
        "https://www.prompthookai.com/2026/10/mcp-server-tool-orchestrator.html",
        # Top-performing GSC & Traffic Articles
        "https://www.prompthookai.com/2025/09/grok-customize.html",
        "https://www.prompthookai.com/2026/08/handle-the-bug-in-feature.html",
        "https://www.prompthookai.com/2025/06/white-box-web-application-security-audit-penetration-testing-prompt-for-ai-code-editors-cursor-windsurf-antigravity.html",
        "https://www.prompthookai.com/2025/07/personal-growth-plan-for-bnwo-enthusiasts.html",
        "https://www.prompthookai.com/2025/09/stripe-payment-builder.html",
        "https://www.prompthookai.com/2025/01/psychologist.html",
        "https://www.prompthookai.com/2025/01/chess-player.html",
        "https://www.prompthookai.com/2025/07/literature-reading-and-analysis-assistant.html",
        "https://www.prompthookai.com/2025/08/train-waiter.html",
        # Hub & Category Pages
        "https://www.prompthookai.com/categories/frontier-models.html",
        "https://www.prompthookai.com/models/grok-3.html",
        "https://www.prompthookai.com/categories/coding-agents.html",
        "https://www.prompthookai.com/models/claude-3-7-sonnet.html",
        "https://www.prompthookai.com/models/deepseek-r1.html",
        "https://www.prompthookai.com/models/gemini-2-5-pro.html",
        "https://www.prompthookai.com/models/gpt-4o.html",
    ]

    print(f"\n[+] Submitting {len(priority_urls)} URLs to Google Indexing API...")
    success_count = 0
    for i, u in enumerate(priority_urls, 1):
        code, res = submit_url(u, access_token)
        if code == 200:
            success_count += 1
            print(f"  [{i}/{len(priority_urls)}] [200 OK] {u}")
        else:
            print(f"  [{i}/{len(priority_urls)}] [{code}] {u} -> {res}")
        time.sleep(0.3)

    print(f"\n[✓] Finished Google Indexing submission: {success_count}/{len(priority_urls)} succeeded!")

    sitemap_url = "https://www.prompthookai.com/sitemap.xml"
    print(f"\n[+] Pinging search engines with sitemap: {sitemap_url}...")
    ping_res = ping_search_engines(sitemap_url)
    for name, res in ping_res.items():
        print(f"  - {name}: {res}")

if __name__ == "__main__":
    main()
