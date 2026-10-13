import os
import glob

ADSENSE_SCRIPT = """  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4863275050514892" crossorigin="anonymous"></script>
"""

ADS_TXT_CONTENT = "google.com, pub-4863275050514892, DIRECT, f08c47fec0942fa0\n"

ROOT_DIR = r"c:\Users\er\Desktop\prompthookai.com"

# 1. Create/Update ads.txt
ads_txt_path = os.path.join(ROOT_DIR, "ads.txt")
with open(ads_txt_path, "w", encoding="utf-8") as f:
    f.write(ADS_TXT_CONTENT)
print(f"Created/Updated {ads_txt_path}")

# 2. Update templates
templates_dir = os.path.join(ROOT_DIR, "scripts", "templates")
for t_file in glob.glob(os.path.join(templates_dir, "*.html")):
    with open(t_file, "r", encoding="utf-8") as f:
        content = f.read()
    if "ca-pub-4863275050514892" not in content:
        if "</head>" in content:
            new_content = content.replace("</head>", f"{ADSENSE_SCRIPT}</head>", 1)
            with open(t_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated template: {t_file}")

# 3. Update all HTML files in repository
updated_count = 0
skipped_count = 0

for root, dirs, files in os.walk(ROOT_DIR):
    # Skip .git directory
    if ".git" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            if "ca-pub-4863275050514892" in html_content:
                skipped_count += 1
                continue
            if "</head>" in html_content:
                new_html = html_content.replace("</head>", f"{ADSENSE_SCRIPT}</head>", 1)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_html)
                updated_count += 1
            else:
                print(f"Warning: No </head> tag found in {file_path}")

print(f"Total HTML files updated: {updated_count}")
print(f"Already had snippet: {skipped_count}")
