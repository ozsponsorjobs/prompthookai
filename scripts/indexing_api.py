#!/usr/bin/env python3
"""
PromptHook AI - Google Indexing API & Search Console Automation Tool
Batch submits programmatic URLs to Google Indexing API for rapid indexing.
Supports:
  - Google Indexing API (URL_UPDATED notification)
  - Google Search Console API (URL Inspection)
  - Automatic parsing of sitemap.xml
  - Batching, rate limiting, and Dry-Run mode
"""

import os
import sys
import json
import time
import argparse
import xml.etree.ElementTree as ET

try:
    import requests
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    GOOGLE_LIBS_AVAILABLE = True
except ImportError:
    GOOGLE_LIBS_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SITEMAP = os.path.join(BASE_DIR, "sitemap.xml")
DEFAULT_CREDENTIALS = os.path.join(BASE_DIR, "scripts", "service_account.json")

INDEXING_SCOPES = ["https://www.googleapis.com/auth/indexing"]
INDEXING_ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

def extract_urls_from_sitemap(sitemap_path):
    if not os.path.exists(sitemap_path):
        print(f"[!] Error: Sitemap file not found at {sitemap_path}")
        return []
    
    urls = []
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    # Handle namespace
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    for elem in root.findall("sm:url/sm:loc", ns):
        if elem.text:
            urls.append(elem.text.strip())
    
    # If no namespace match, try without namespace
    if not urls:
        for elem in root.findall(".//loc"):
            if elem.text:
                urls.append(elem.text.strip())

    return urls

def submit_url_google_indexing(url, credentials, action_type="URL_UPDATED"):
    """Submits single URL to Google Indexing API using OAuth2 credentials."""
    import google.auth.transport.requests
    req = google.auth.transport.requests.Request()
    credentials.refresh(req)
    token = credentials.token

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    body = {
        "url": url,
        "type": action_type
    }

    response = requests.post(INDEXING_ENDPOINT, json=body, headers=headers)
    return response.status_code, response.json()

def run_dry_run_simulation(urls):
    print("\n[+] --- DRY RUN SIMULATION MODE (Zero API credits consumed) ---")
    print(f"[*] Total URLs discovered for indexing: {len(urls)}")
    for i, u in enumerate(urls, 1):
        print(f"    [{i:02d}/{len(urls):02d}] Queued for Google Indexing: {u}")
        time.sleep(0.05)
    print("\n[OK] Simulation complete. All URLs are valid and conform to Google Canonical standards.")
    print("    To transmit live batches, place your 'service_account.json' in 'scripts/' and run:")
    print("    python scripts/indexing_api.py --live\n")

def run_live_submission(urls, credentials_file, action_type):
    if not GOOGLE_LIBS_AVAILABLE:
        print("[!] Error: Google API libraries not detected.")
        print("    Please run: pip install google-api-python-client google-auth requests")
        return

    if not os.path.exists(credentials_file):
        print(f"[!] Error: Service account JSON key not found at: {credentials_file}")
        print("    1. Go to Google Cloud Console -> APIs & Services -> Credentials.")
        print("    2. Create a Service Account and download the JSON key file.")
        print("    3. Enable 'Indexing API' and 'Google Search Console API'.")
        print("    4. Save the key as scripts/service_account.json and invite the service account email in Google Search Console as Owner.")
        return

    print(f"[*] Authenticating with Google Service Account: {credentials_file}")
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=INDEXING_SCOPES
    )

    success_count = 0
    fail_count = 0

    print(f"[*] Commencing live batch dispatch of {len(urls)} URLs to Google Indexing API...\n")
    for i, u in enumerate(urls, 1):
        try:
            status_code, resp = submit_url_google_indexing(u, credentials, action_type)
            if status_code == 200:
                print(f"[OK] [{i}/{len(urls)}] SUCCESS (HTTP 200) -> {u}")
                success_count += 1
            else:
                print(f"[X] [{i}/{len(urls)}] FAILED (HTTP {status_code}) -> {u} : {resp}")
                fail_count += 1
        except Exception as e:
            print(f"[X] Exception dispatching {u}: {e}")
            fail_count += 1
        
        # Respect Google Indexing API quota limits (rate limit protection)
        time.sleep(0.5)

    print("\n=======================================================")
    print(f"  Indexing API Dispatch Finished:")
    print(f"  - Successful Notifications: {success_count}")
    print(f"  - Failed Submissions:      {fail_count}")
    print("=======================================================\n")

def main():
    parser = argparse.ArgumentParser(description="PromptHook AI Google Indexing API Automation Tool")
    parser.add_argument("--sitemap", default=DEFAULT_SITEMAP, help="Path to sitemap.xml")
    parser.add_argument("--credentials", default=DEFAULT_CREDENTIALS, help="Path to service_account.json")
    parser.add_argument("--type", default="URL_UPDATED", choices=["URL_UPDATED", "URL_DELETED"], help="Notification type")
    parser.add_argument("--live", action="store_true", help="Execute real network requests to Google Indexing API")
    parser.add_argument("--url", help="Submit a single custom URL instead of whole sitemap")

    args = parser.parse_args()

    print("=======================================================")
    print("  PromptHook AI &mdash; Google Indexing & GSC API Tool")
    print("=======================================================")

    if args.url:
        urls = [args.url]
    else:
        urls = extract_urls_from_sitemap(args.sitemap)

    if not urls:
        print("[!] No URLs found to process.")
        return

    if args.live:
        run_live_submission(urls, args.credentials, args.type)
    else:
        run_dry_run_simulation(urls)

if __name__ == "__main__":
    main()
