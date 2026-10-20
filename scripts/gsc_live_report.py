#!/usr/bin/env python3
"""
PromptHook AI - Live Google Search Console Monitor
Fetches real-time organic search analytics (clicks, impressions, queries, positions)
directly from the Google Search Console API.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

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

def query_gsc(access_token, property_id, start_date, end_date, dimensions=None, row_limit=10):
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(property_id, safe='')}/searchAnalytics/query"
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "rowLimit": row_limit
    }
    if dimensions:
        body["dimensions"] = dimensions
    
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    print("=" * 60)
    print("      PROMPTHOOK AI - GOOGLE SEARCH CONSOLE LIVE REPORT      ")
    print("=" * 60)
    
    try:
        token = get_access_token()
    except Exception as e:
        print(f"[!] Authentication failed: {e}")
        return

    prop = "sc-domain:prompthookai.com"
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

    print(f"\n[+] Property: {prop}")
    print(f"[+] Date Range: {start_date} to {end_date} (90 Days)")

    # 1. Total Metrics
    totals = query_gsc(token, prop, start_date, end_date)
    rows = totals.get("rows", [])
    if rows:
        r = rows[0]
        clicks = r.get("clicks", 0)
        impressions = r.get("impressions", 0)
        ctr = r.get("ctr", 0) * 100
        pos = r.get("position", 0)
        print("\n--- OVERALL TOTALS ---")
        print(f"  • Total Organic Clicks:      {clicks}")
        print(f"  • Total Search Impressions:  {impressions}")
        print(f"  • Average CTR:               {ctr:.2f}%")
        print(f"  • Average Position:          {pos:.1f}")
    else:
        print("\n[!] No overall totals recorded for this range.")

    # 2. Top Search Queries
    q_data = query_gsc(token, prop, start_date, end_date, dimensions=["query"], row_limit=10)
    print("\n--- TOP SEARCH QUERIES ---")
    if "rows" in q_data:
        for idx, row in enumerate(q_data["rows"], 1):
            q_name = row["keys"][0]
            print(f"  {idx:2d}. '{q_name}' | Clicks: {row.get('clicks', 0)} | Imp: {row.get('impressions', 0)} | Pos: {row.get('position', 0):.1f}")
    else:
        print("  No queries data available yet.")

    # 3. Top Pages
    p_data = query_gsc(token, prop, start_date, end_date, dimensions=["page"], row_limit=8)
    print("\n--- TOP PAGES IN GOOGLE ---")
    if "rows" in p_data:
        for idx, row in enumerate(p_data["rows"], 1):
            p_name = row["keys"][0]
            print(f"  {idx:2d}. {p_name}")
            print(f"      Clicks: {row.get('clicks', 0)} | Impressions: {row.get('impressions', 0)} | CTR: {row.get('ctr', 0)*100:.1f}% | Avg Pos: {row.get('position', 0):.1f}")
    else:
        print("  No pages data available yet.")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
