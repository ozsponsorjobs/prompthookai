#!/usr/bin/env python3
"""
Propagate SEO & Technical Fixes Across All HTML Files:
1. Fix empty alt="" on visitor badge -> alt="PromptHook AI Traffic Monitor"
2. Inject favicon links into <head> of all HTML files if missing
3. Inject og:image & twitter:image into all HTML files if missing
"""

import os

ROOT_DIR = r"c:\Users\er\Desktop\prompthookai.com"

FAVICON_SNIPPET = """  <link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/icons/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">
  <link rel="shortcut icon" href="/favicon.ico">"""

OG_IMAGE_SNIPPET = """  <meta property="og:image" content="https://www.prompthookai.com/assets/images/og-image.png">
  <meta name="twitter:image" content="https://www.prompthookai.com/assets/images/og-image.png">"""

alt_updated = 0
favicon_updated = 0
og_updated = 0

for root, dirs, files in os.walk(ROOT_DIR):
    if ".git" in root or "admin-hub.html" in files:
        continue
    for file in files:
        if file.endswith(".html") and file != "admin-hub.html":
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            modified = False

            # 1. Fix visitor badge alt attribute
            if 'api.visitorbadge.io' in content and 'alt=""' in content:
                content = content.replace('alt="" style="position:absolute;width:1px;height:1px;opacity:0.01;pointer-events:none;"',
                                          'alt="PromptHook AI Traffic Monitor" style="position:absolute;width:1px;height:1px;opacity:0.01;pointer-events:none;"')
                alt_updated += 1
                modified = True

            # 2. Add favicon tags if missing
            if 'favicon.svg' not in content and '</head>' in content:
                # Insert before </head> or after canonical
                if '<link rel="canonical"' in content:
                    target_str = content[content.find('<link rel="canonical"'):]
                    canonical_line = target_str[:target_str.find('>') + 1]
                    content = content.replace(canonical_line, f"{canonical_line}\n{FAVICON_SNIPPET}", 1)
                else:
                    content = content.replace('</head>', f"{FAVICON_SNIPPET}\n</head>", 1)
                favicon_updated += 1
                modified = True

            # 3. Add og:image if missing
            if 'og:image' not in content and '</head>' in content:
                content = content.replace('</head>', f"{OG_IMAGE_SNIPPET}\n</head>", 1)
                og_updated += 1
                modified = True

            if modified:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

print(f"Total files updated with ALT text: {alt_updated}")
print(f"Total files updated with Favicon: {favicon_updated}")
print(f"Total files updated with OG Image: {og_updated}")
