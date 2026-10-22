#!/usr/bin/env python3
"""
PromptHook AI - Microsoft Clarity Integration Script
Injects Microsoft Clarity tracking snippet into all HTML files across the repository.
Project ID: z1p8ed86x9
"""

import os
import glob

CLARITY_SNIPPET = """  <!-- Microsoft Clarity -->
  <script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "z1p8ed86x9");
  </script>
"""

ROOT_DIR = r"c:\Users\er\Desktop\prompthookai.com"

# 1. Update templates
templates_dir = os.path.join(ROOT_DIR, "scripts", "templates")
if os.path.exists(templates_dir):
    for t_file in glob.glob(os.path.join(templates_dir, "*.html")):
        with open(t_file, "r", encoding="utf-8") as f:
            content = f.read()
        if "z1p8ed86x9" not in content:
            if "</head>" in content:
                new_content = content.replace("</head>", f"{CLARITY_SNIPPET}</head>", 1)
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
            if "z1p8ed86x9" in html_content:
                skipped_count += 1
                continue
            if "</head>" in html_content:
                new_html = html_content.replace("</head>", f"{CLARITY_SNIPPET}</head>", 1)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_html)
                updated_count += 1
            else:
                print(f"Warning: No </head> tag found in {file_path}")

print(f"Total HTML files updated with Clarity: {updated_count}")
print(f"Already had Clarity: {skipped_count}")
