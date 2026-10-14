#!/usr/bin/env python3
"""
PromptHook AI - Client-Side Search Index Compiler
Compiles an ultra-compact JSON index of all 1,960 blueprints and legacy articles.
Total uncompressed size: ~140KB (gzipped ~35KB over Cloudflare CDN).
Runs 100% in client-side browser with 0ms backend latency.
"""

import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "search-index.json")

# Category mapping
CATEGORY_MAP = {
    "code-engineering": {
        "name": "Coding & Architecture",
        "keywords": ["code", "engineer", "architect", "system", "developer", "python", "devops", "api", "sql", "test", "docker", "k8s", "debug", "refactor", "ast", "frontend", "backend", "fullstack", "rust", "typescript", "golang"]
    },
    "autonomous-agents": {
        "name": "Autonomous Agents",
        "keywords": ["agent", "assistant", "workflow", "orchestrator", "tool", "bot", "task", "react", "function", "autonomous", "dispatcher", "loop"]
    },
    "data-analytics": {
        "name": "Data Analytics",
        "keywords": ["data", "analysis", "analyst", "extraction", "json", "schema", "metrics", "dashboard", "bi", "report", "stats", "database", "parser", "excel", "scraper"]
    },
    "seo-content-strategy": {
        "name": "Programmatic SEO",
        "keywords": ["seo", "content", "writing", "article", "guide", "story", "copywriting", "blog", "cluster", "keyword", "silo", "eeat", "author", "editor"]
    },
    "growth-marketing": {
        "name": "Growth & Copywriting",
        "keywords": ["marketing", "growth", "copy", "sales", "funnel", "landing", "email", "ad", "conversion", "hook", "social", "campaign", "lead", "outreach", "b2b"]
    },
    "customer-support": {
        "name": "Customer Support",
        "keywords": ["support", "customer", "ticket", "triage", "faq", "service", "client", "dispute", "refund", "resolution", "escalation"]
    }
}

def clean_slug_to_title(slug):
    words = slug.split("-")
    capitalized = []
    for w in words:
        if not w:
            continue
        if w.lower() in ["ai", "api", "seo", "json", "b2b", "saas", "ui", "ux", "sql", "html", "css", "js", "dpo", "llm"]:
            capitalized.append(w.upper())
        elif w.lower() in ["and", "or", "the", "for", "with", "in", "on", "of", "to"]:
            capitalized.append(w.lower())
        else:
            capitalized.append(w.capitalize())
    if capitalized and capitalized[0].islower():
        capitalized[0] = capitalized[0].capitalize()
    return " ".join(capitalized)

def determine_category(slug):
    slug_lower = slug.lower()
    for cat_slug, cat_data in CATEGORY_MAP.items():
        for kw in cat_data["keywords"]:
            if kw in slug_lower:
                return cat_slug, cat_data["name"]
    return "code-engineering", "Coding & Architecture"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    index_items = []

    # 1. Flagship Blueprints
    blueprints_file = os.path.join(DATA_DIR, "blueprints.json")
    if os.path.exists(blueprints_file):
        with open(blueprints_file, "r", encoding="utf-8") as f:
            blueprints = json.load(f)
        for b in blueprints:
            index_items.append({
                "t": b.get("title", ""),
                "u": f"/blueprints/{b.get('slug')}.html",
                "c": b.get("category_name", "Flagship Blueprint"),
                "cat_id": b.get("category", "code-engineering"),
                "f": 1  # Flagship priority
            })

    # 2. Legacy Blogger Posts (1,954 articles)
    blogger_file = os.path.join(DATA_DIR, "extracted_blogger_posts.json")
    if os.path.exists(blogger_file):
        with open(blogger_file, "r", encoding="utf-8") as f:
            posts = json.load(f)
        for p in posts:
            slug = p.get("slug", "")
            year = p.get("year", "2026")
            month = p.get("month", "09")
            title = clean_slug_to_title(slug)
            cat_slug, cat_name = determine_category(slug)
            index_items.append({
                "t": title,
                "u": f"/{year}/{month}/{slug}.html",
                "c": cat_name,
                "cat_id": cat_slug,
                "f": 0
            })

    print(f"[*] Compiled {len(index_items)} searchable blueprints into search index.")
    
    # Save compact JSON (no extra whitespace to minimize file size)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(index_items, f, separators=(',', ':'), ensure_ascii=False)

    size_kb = os.path.getsize(OUTPUT_FILE) / 1024.0
    print(f"[+] Output: {OUTPUT_FILE} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    main()
