import os
import glob
import re

GTAG_SNIPPET = """  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-RCSR08B48N"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-RCSR08B48N');
  </script>
"""

ROOT_DIR = r"c:\Users\er\Desktop\prompthookai.com"

# 1. Update templates
templates_dir = os.path.join(ROOT_DIR, "scripts", "templates")
for t_file in glob.glob(os.path.join(templates_dir, "*.html")):
    with open(t_file, "r", encoding="utf-8") as f:
        content = f.read()
    if "G-RCSR08B48N" not in content:
        if "<head>" in content:
            new_content = content.replace("<head>", f"<head>\n{GTAG_SNIPPET}", 1)
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
            if "G-RCSR08B48N" in html_content:
                skipped_count += 1
                continue
            if "<head>" in html_content:
                new_html = html_content.replace("<head>", f"<head>\n{GTAG_SNIPPET}", 1)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_html)
                updated_count += 1
            else:
                print(f"Warning: No <head> tag found in {file_path}")

print(f"Total HTML files updated with GA4: {updated_count}")
print(f"Already had snippet: {skipped_count}")
