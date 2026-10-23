#!/usr/bin/env python3
"""
PromptHook AI - Asset Generator for SEO & Social Media
Generates:
1. favicon.svg (Modern vector SVG favicon)
2. favicon.ico (Multi-resolution Windows/Browser icon: 16, 32, 48)
3. favicon-16x16.png & favicon-32x32.png
4. apple-touch-icon.png (180x180)
5. logo.png (512x512 high-res organization logo)
6. og-image.png (1200x630 Open Graph & Twitter Social Card)
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = r"c:\Users\er\Desktop\prompthookai.com"
ICONS_DIR = os.path.join(ROOT_DIR, "assets", "icons")
IMAGES_DIR = os.path.join(ROOT_DIR, "assets", "images")

os.makedirs(ICONS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. Create favicon.svg
# -------------------------------------------------------------
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#0284c7"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#818cf8"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#38bdf8" flood-opacity="0.5"/>
    </filter>
  </defs>
  
  <!-- Outer Rounded Container -->
  <rect x="2" y="2" width="60" height="60" rx="14" fill="#090d16" stroke="rgba(56, 189, 248, 0.4)" stroke-width="2"/>
  <rect x="6" y="6" width="52" height="52" rx="10" fill="url(#bgGrad)" opacity="0.35"/>
  
  <!-- Prompt Symbol >_ and Hook Accent -->
  <g filter="url(#glow)">
    <!-- Terminal Prompt Chevron > -->
    <path d="M 18 20 L 30 32 L 18 44" fill="none" stroke="#f8fafc" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
    
    <!-- Hook / Node Accent -->
    <path d="M 33 44 L 46 44 C 47.5 44 48.5 43 48.5 41.5 L 48.5 28 C 48.5 23 44.5 19 39.5 19 C 34.5 19 30.5 23 30.5 28" 
          fill="none" stroke="url(#accentGrad)" stroke-width="4.5" stroke-linecap="round"/>
    <circle cx="30.5" cy="28" r="3" fill="#38bdf8"/>
  </g>
</svg>
'''

with open(os.path.join(ICONS_DIR, "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(svg_content)
print("Generated assets/icons/favicon.svg")


# -------------------------------------------------------------
# 2. Render High-Res Base Icon using PIL (512x512)
# -------------------------------------------------------------
def create_base_icon(size=512):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Rounded dark slate background
    margin = int(size * 0.04)
    radius = int(size * 0.22)
    bg_color = (9, 13, 22, 255)
    border_color = (56, 189, 248, 120)
    
    draw.rounded_rectangle([margin, margin, size - margin, size - margin], radius=radius, fill=bg_color, outline=border_color, width=max(2, int(size * 0.02)))
    
    # Inner subtle glow
    inner_m = int(size * 0.08)
    inner_r = int(size * 0.18)
    draw.rounded_rectangle([inner_m, inner_m, size - inner_m, size - inner_m], radius=inner_r, fill=(15, 23, 42, 180), outline=(2, 132, 199, 80), width=max(1, int(size * 0.01)))
    
    # Draw Prompt Chevron ( > )
    # Points
    p1 = (int(size * 0.28), int(size * 0.32))
    p2 = (int(size * 0.46), int(size * 0.50))
    p3 = (int(size * 0.28), int(size * 0.68))
    line_w = max(3, int(size * 0.07))
    
    draw.line([p1, p2, p3], fill=(248, 250, 252, 255), width=line_w, joint="round")
    
    # Draw Hook & Spark Node
    h_start = (int(size * 0.52), int(size * 0.68))
    h_corner = (int(size * 0.72), int(size * 0.68))
    h_up = (int(size * 0.72), int(size * 0.44))
    draw.line([h_start, h_corner, h_up], fill=(56, 189, 248, 255), width=line_w, joint="round")
    
    # Top arc curve of hook
    # Arc bounding box:
    arc_box = [int(size * 0.48), int(size * 0.28), int(size * 0.72), int(size * 0.52)]
    draw.arc(arc_box, start=180, end=360, fill=(56, 189, 248, 255), width=line_w)
    
    # Terminal spark circle
    spark_center = (int(size * 0.48), int(size * 0.40))
    s_r = int(size * 0.045)
    draw.ellipse([spark_center[0] - s_r, spark_center[1] - s_r, spark_center[0] + s_r, spark_center[1] + s_r], fill=(129, 140, 248, 255))
    
    return img

base_icon_512 = create_base_icon(512)

# Save logo.png (512x512)
logo_path = os.path.join(ICONS_DIR, "logo.png")
base_icon_512.save(logo_path, format="PNG")
print(f"Generated {logo_path}")

# Save apple-touch-icon.png (180x180)
apple_icon = base_icon_512.resize((180, 180), Image.Resampling.LANCZOS)
apple_icon_path = os.path.join(ICONS_DIR, "apple-touch-icon.png")
apple_icon.save(apple_icon_path, format="PNG")
print(f"Generated {apple_icon_path}")

# Save favicon-32x32.png
icon_32 = base_icon_512.resize((32, 32), Image.Resampling.LANCZOS)
icon_32_path = os.path.join(ICONS_DIR, "favicon-32x32.png")
icon_32.save(icon_32_path, format="PNG")
print(f"Generated {icon_32_path}")

# Save favicon-16x16.png
icon_16 = base_icon_512.resize((16, 16), Image.Resampling.LANCZOS)
icon_16_path = os.path.join(ICONS_DIR, "favicon-16x16.png")
icon_16.save(icon_16_path, format="PNG")
print(f"Generated {icon_16_path}")

# Save root favicon.ico (multi-size: 16, 32, 48)
icon_48 = base_icon_512.resize((48, 48), Image.Resampling.LANCZOS)
root_favicon_path = os.path.join(ROOT_DIR, "favicon.ico")
icon_48.save(root_favicon_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
print(f"Generated {root_favicon_path}")


# -------------------------------------------------------------
# 3. Render High-Impact Open Graph Banner (og-image.png 1200x630)
# -------------------------------------------------------------
def create_og_image():
    w, h = 1200, 630
    img = Image.new("RGBA", (w, h), (9, 13, 22, 255))
    draw = ImageDraw.Draw(img)
    
    # Background subtle gradient simulation
    for y in range(h):
        ratio = y / h
        r = int(9 + ratio * 8)
        g = int(13 + ratio * 15)
        b = int(22 + ratio * 32)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
    # Decorative ambient glow circles
    glow1 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow1)
    glow_draw.ellipse([800, -100, 1300, 400], fill=(2, 132, 199, 45))
    glow_draw.ellipse([-100, 300, 400, 800], fill=(99, 102, 241, 35))
    img = Image.alpha_composite(img, glow1)
    draw = ImageDraw.Draw(img)
    
    # Outer modern border
    draw.rounded_rectangle([20, 20, w - 20, h - 20], radius=24, outline=(56, 189, 248, 60), width=2)
    
    # Add prompt icon on top left
    icon_sub = base_icon_512.resize((96, 96), Image.Resampling.LANCZOS)
    img.paste(icon_sub, (70, 65), icon_sub)
    
    # Text fonts
    try:
        font_brand = ImageFont.truetype("arialbd.ttf", 36)
        font_badge = ImageFont.truetype("arialbd.ttf", 18)
        font_h1 = ImageFont.truetype("arialbd.ttf", 52)
        font_sub = ImageFont.truetype("arial.ttf", 26)
        font_tag = ImageFont.truetype("arialbd.ttf", 20)
    except:
        font_brand = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_h1 = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        
    # Brand Name next to icon
    draw.text((185, 75), "PromptHook", fill=(248, 250, 252), font=font_brand)
    draw.text((395, 75), "AI", fill=(56, 189, 248), font=font_brand)
    
    # Pill Badge (TOP RIGHT)
    badge_text = "PRODUCTION PROMPT DIRECTIVES"
    draw.rounded_rectangle([w - 430, 75, w - 70, 115], radius=20, fill=(15, 23, 42, 220), outline=(56, 189, 248, 120), width=1)
    draw.text((w - 410, 85), badge_text, fill=(56, 189, 248), font=font_badge)
    
    # Main Headline
    draw.text((70, 205), "Prompt Engineering as", fill=(248, 250, 252), font=font_h1)
    draw.text((70, 270), "Executable Code & Injection", fill=(56, 189, 248), font=font_h1)
    
    # Subheadline
    sub_line1 = "Hyper-optimized prompt blueprints with zero-hallucination protocols."
    sub_line2 = "Instant parameters calibration for autonomous agent architectures."
    draw.text((70, 360), sub_line1, fill=(203, 213, 225), font=font_sub)
    draw.text((70, 400), sub_line2, fill=(148, 163, 184), font=font_sub)
    
    # Model Badges along bottom
    models = ["Claude 3.7", "GPT-4o", "DeepSeek R1", "xAI Grok 3", "Gemini 2.0"]
    cur_x = 70
    y_pos = 485
    for m in models:
        pill_w = len(m) * 14 + 36
        draw.rounded_rectangle([cur_x, y_pos, cur_x + pill_w, y_pos + 46], radius=12, fill=(15, 23, 42, 240), outline=(56, 189, 248, 90), width=1)
        draw.text((cur_x + 18, y_pos + 12), m, fill=(224, 242, 254), font=font_tag)
        cur_x += pill_w + 16
        
    # Domain Tag bottom right
    draw.text((w - 320, 500), "https://prompthookai.com", fill=(56, 189, 248), font=font_sub)
    
    og_path = os.path.join(IMAGES_DIR, "og-image.png")
    img.save(og_path, format="PNG")
    print(f"Generated {og_path}")

create_og_image()
print("All asset generations finished successfully.")
