#!/usr/bin/env python3
"""
PromptHook AI - Independent Background Hit Counter Integration Script
Injects a lightweight background beacon into all HTML files across the repository.
Allows real-time verification via direct browser URL.
"""

import os
import glob

BEACON_SNIPPET = """  <!-- Independent Background Hit Counter -->
  <img src="https://api.visitorbadge.io/api/combined?path=prompthookai.com" alt="PromptHook AI Traffic Monitor" style="position:absolute;width:1px;height:1px;opacity:0.01;pointer-events:none;" loading="eager" />
"""

ROOT_DIR = r"c:\Users\er\Desktop\prompthookai.com"

# 1. Update templates
templates_dir = os.path.join(ROOT_DIR, "scripts", "templates")
if os.path.exists(templates_dir):
    for t_file in glob.glob(os.path.join(templates_dir, "*.html")):
        with open(t_file, "r", encoding="utf-8") as f:
            content = f.read()
        if "api.visitorbadge.io" not in content:
            if "</body>" in content:
                new_content = content.replace("</body>", f"{BEACON_SNIPPET}</body>", 1)
                with open(t_file, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated template: {t_file}")

# 2. Update all HTML files in repository
updated_count = 0
skipped_count = 0

for root, dirs, files in os.walk(ROOT_DIR):
    if ".git" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            if "api.visitorbadge.io" in html_content:
                skipped_count += 1
                continue
            if "</body>" in html_content:
                new_html = html_content.replace("</body>", f"{BEACON_SNIPPET}</body>", 1)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_html)
                updated_count += 1
            else:
                print(f"Warning: No </body> tag found in {file_path}")

print(f"Total HTML files updated with Background Counter: {updated_count}")
print(f"Already had Counter: {skipped_count}")
