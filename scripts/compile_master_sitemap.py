#!/usr/bin/env python3
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://www.prompthookai.com"
today = datetime.now().strftime("%Y-%m-%d")

with open(os.path.join(BASE_DIR, "data", "upgraded_urls.json"), "r", encoding="utf-8") as f:
    upgraded = json.load(f)

core_urls = [
    "/",
    "/about.html",
    "/contact.html",
    "/privacy.html",
    "/terms.html",
    "/categories/code-engineering.html",
    "/categories/autonomous-agents.html",
    "/categories/data-analytics.html",
    "/categories/seo-content-strategy.html",
    "/categories/growth-marketing.html",
    "/categories/customer-support.html",
    "/models/claude-sonnet-3-7.html",
    "/models/gpt-4o.html",
    "/models/deepseek-r1.html",
    "/models/gemini-2-flash.html",
    "/blueprints/enterprise-codebase-refactor-security-auditor.html",
    "/blueprints/autonomous-react-agent-tool-orchestrator.html",
    "/blueprints/zero-hallucination-json-extractor.html",
    "/blueprints/programmatic-seo-silo-content-architect.html",
    "/blueprints/b2b-saas-cold-outreach-sequence-engine.html",
    "/blueprints/multiturn-customer-support-triage-arbiter.html"
]

all_urls = core_urls + upgraded

print(f"[*] Compiling Master XML Sitemap for {len(all_urls)} URLs...")

lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

for u in all_urls:
    if u == "/":
        prio = "1.0"
        freq = "daily"
    elif u.startswith("/categories/") or u.startswith("/models/"):
        prio = "0.9"
        freq = "weekly"
    elif u.startswith("/blueprints/"):
        prio = "0.85"
        freq = "weekly"
    elif any(u.startswith(f"/{y}/") for y in ["2025", "2026"]):
        prio = "0.8"
        freq = "monthly"
    else:
        prio = "0.5"
        freq = "monthly"

    lines.append("  <url>")
    lines.append(f"    <loc>{DOMAIN}{u}</loc>")
    lines.append(f"    <lastmod>{today}</lastmod>")
    lines.append(f"    <changefreq>{freq}</changefreq>")
    lines.append(f"    <priority>{prio}</priority>")
    lines.append("  </url>")

lines.append("</urlset>")

sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"[+] Master sitemap.xml generated with {len(all_urls)} URLs! Size: {os.path.getsize(sitemap_path) / 1024:.1f} KB")
