#!/usr/bin/env python3
"""
PromptHook AI - Programmatic Static Site Generator & SEO Architect
Generates production-grade HTML pages from JSON datasets.
Produces:
  - blueprints/*.html (1,200 - 1,800+ words, Dual JSON-LD, Live Parameter Sandbox)
  - categories/*.html (Topic Silo Hubs)
  - models/*.html (Model Calibration Hubs)
  - sitemap.xml & robots.txt
"""

import json
import os
import html
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMPLATES_DIR = os.path.join(BASE_DIR, "scripts", "templates")
BLUEPRINTS_DIR = os.path.join(BASE_DIR, "blueprints")
CATEGORIES_DIR = os.path.join(BASE_DIR, "categories")
MODELS_DIR = os.path.join(BASE_DIR, "models")
DOMAIN = "https://www.prompthookai.com"

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_template(filename):
    with open(os.path.join(TEMPLATES_DIR, filename), "r", encoding="utf-8") as f:
        return f.read()

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def render_blueprint_card(b):
    category_slug = b.get("category", "")
    category_name = b.get("category_name", category_slug)
    version = b.get("version", "1.0.0")
    title = b.get("title", "")
    slug = b.get("slug", "")
    summary = b.get("summary", "")
    input_base = b.get("token_metrics", {}).get("input_base", 600)
    diff = b.get("difficulty", "Advanced")
    tags_str = " ".join(b.get("tags", []))

    models_html = ""
    for m in b.get("target_models", [])[:3]:
        models_html += f'<span class="model-tag">{html.escape(m.get("model_name", m.get("model_id")))}</span>'

    return f"""
    <article class="blueprint-card" data-category="{html.escape(category_slug)}" data-tags="{html.escape(tags_str)}">
      <div>
        <div class="card-header-top">
          <span class="card-category-badge">{html.escape(category_name)}</span>
          <span class="card-version-tag">v{html.escape(version)}</span>
        </div>
        <h3 class="card-title">
          <a href="/blueprints/{html.escape(slug)}.html">{html.escape(title)}</a>
        </h3>
        <p class="card-description">{html.escape(summary)}</p>
      </div>
      <div>
        <div class="card-meta-list">
          <div class="card-meta-item">Input: <span class="val">~{input_base} tkn</span></div>
          <div class="card-meta-item">Level: <span class="val">{html.escape(diff)}</span></div>
        </div>
        <div class="card-footer">
          <div class="models-support">{models_html}</div>
          <a href="/blueprints/{html.escape(slug)}.html" class="btn-open-blueprint">
            <span>Sandbox</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </a>
        </div>
      </div>
    </article>
    """

def generate_blueprints(blueprints, categories, models):
    template = load_template("blueprint_template.html")
    ensure_dir(BLUEPRINTS_DIR)
    generated_urls = []

    for b in blueprints:
        slug = b["slug"]
        print(f"[*] Compiling Blueprint: {b['title']} -> blueprints/{slug}.html")

        # Prepare reasoning steps
        reasoning_steps = b.get("architecture_deep_dive", {}).get("reasoning_steps", [])
        reasoning_steps_html = "".join([f"<li>{html.escape(step)}</li>" for step in reasoning_steps])

        # Anti-hallucination guardrails
        safeguards = b.get("architecture_deep_dive", {}).get("anti_hallucination_protocols", [])
        safeguards_html = "".join([f"<li><strong>Rule:</strong> {html.escape(s)}</li>" for s in safeguards])

        # Hyperparameters Table
        hyperparameters = b.get("hyperparameter_guide", [])
        hyper_rows = ""
        for hp in hyperparameters:
            hyper_rows += f"""
            <tr>
              <td><code>{html.escape(hp.get('parameter', ''))}</code></td>
              <td style="font-weight: 600; color: var(--brand-cyan);">{html.escape(hp.get('value', ''))}</td>
              <td>{html.escape(hp.get('explanation', ''))}</td>
            </tr>
            """

        # Model compatibility rows
        model_compat_rows = ""
        for m in b.get("target_models", []):
            model_compat_rows += f"""
            <tr>
              <td><strong>{html.escape(m.get('model_name', m.get('model_id')))}</strong></td>
              <td style="color: var(--brand-emerald); font-weight: 700;">{m.get('compatibility', 95)}%</td>
              <td><code>{m.get('recommended_temp', 0.2)}</code></td>
              <td><code>{m.get('top_p', 0.9)}</code></td>
            </tr>
            """

        # FAQs & FAQ JSON Schema
        faqs = b.get("faqs", [])
        faqs_html = ""
        faq_json_items = []
        for i, faq in enumerate(faqs):
            q = faq.get("question", "")
            a = faq.get("answer", "")
            faqs_html += f"""
            <div class="faq-item{' active' if i == 0 else ''}">
              <button type="button" class="faq-question" aria-expanded="{'true' if i == 0 else 'false'}">
                <span>{html.escape(q)}</span>
                <svg class="faq-icon-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"></polyline></svg>
              </button>
              <div class="faq-answer"><p>{html.escape(a)}</p></div>
            </div>
            """
            faq_json_items.append(f"""
            {{
              "@type": "Question",
              "name": {json.dumps(q)},
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": {json.dumps(a)}
              }}
            }}
            """)

        faq_json_str = ",".join(faq_json_items)

        # Parameter Inputs for Interactive Sandbox
        param_inputs_html = ""
        for p in b.get("parameters", []):
            p_key = p.get("key", "")
            p_label = p.get("label", p_key)
            p_type = p.get("type", "text")
            p_default = p.get("default", "")
            p_desc = p.get("description", "")
            p_placeholder = p.get("placeholder", "")

            if p_type == "select":
                opts_html = "".join([f'<option value="{html.escape(opt)}"{(" selected" if opt == p_default else "")}>{html.escape(opt)}</option>' for opt in p.get("options", [])])
                input_field = f'<select class="param-select" data-param-key="{html.escape(p_key)}" data-default="{html.escape(p_default)}">{opts_html}</select>'
            else:
                input_field = f'<input type="text" class="param-input" data-param-key="{html.escape(p_key)}" value="{html.escape(p_default)}" data-default="{html.escape(p_default)}" placeholder="{html.escape(p_placeholder)}">'

            param_inputs_html += f"""
            <div class="param-group">
              <div class="param-label-row">
                <label class="param-label">{html.escape(p_label)}</label>
                <span class="param-key-tag">{{{{{html.escape(p_key)}}}}}</span>
              </div>
              {input_field}
              <span class="param-hint">{html.escape(p_desc)}</span>
            </div>
            """

        # Related Blueprints (cards from other blueprints)
        related_cards = [render_blueprint_card(other) for other in blueprints if other["id"] != b["id"]][:3]
        related_cards_html = "".join(related_cards)

        target_models_summary = ", ".join([m.get("model_name", m.get("model_id")) for m in b.get("target_models", [])[:2]])

        # Compile replacements
        page_html = template
        replacements = {
            "{{META_TITLE}}": html.escape(b.get("meta_title", b.get("title"))),
            "{{META_DESCRIPTION}}": html.escape(b.get("meta_description", b.get("summary"))),
            "{{SLUG}}": slug,
            "{{TITLE}}": html.escape(b.get("title", "")),
            "{{SUMMARY}}": html.escape(b.get("summary", "")),
            "{{CATEGORY_SLUG}}": b.get("category", ""),
            "{{CATEGORY_NAME}}": html.escape(b.get("category_name", "")),
            "{{DIFFICULTY}}": html.escape(b.get("difficulty", "Production Architect")),
            "{{VERSION}}": html.escape(b.get("version", "1.0.0")),
            "{{UPDATED_AT}}": b.get("updated_at", "2026-09-24"),
            "{{INPUT_BASE}}": str(b.get("token_metrics", {}).get("input_base", 600)),
            "{{OUTPUT_AVG}}": str(b.get("token_metrics", {}).get("output_avg", 1800)),
            "{{EFFICIENCY_RATING}}": b.get("token_metrics", {}).get("efficiency_rating", "99.0%"),
            "{{TARGET_MODELS_SUMMARY}}": html.escape(target_models_summary),
            "{{TAGS_COMMA}}": html.escape(", ".join(b.get("tags", []))),
            "{{FAQ_JSON_ITEMS}}": faq_json_str,
            "{{SYSTEM_INSTRUCTIONS}}": html.escape(b.get("system_instructions", "")),
            "{{ARCH_RATIONALE}}": html.escape(b.get("architecture_deep_dive", {}).get("rationale", "")),
            "{{REASONING_STEPS_HTML}}": reasoning_steps_html,
            "{{ANTI_HALLUCINATION_HTML}}": safeguards_html,
            "{{EDGE_CASES_SECTION}}": f"""
        <h2>4. Production Edge Cases & Failure Mode Mitigations</h2>
        <p>When deploying this blueprint within high-throughput automation pipelines, systems encounter non-trivial edge vectors. The architecture enforces the following mitigations:</p>
        <ul>
          <li><strong>Memory Leak & Context Saturation:</strong> Hierarchical token eviction protocols safeguard against memory overflow during prolonged generation loops.</li>
          <li><strong>Malformed Payload Ingestion:</strong> Enforces schema validation failure traps before state mutations or database writes occur.</li>
          <li><strong>Stochastic Persona Drift:</strong> Low nucleus sampling boundaries guarantee output fidelity across concurrent worker nodes.</li>
        </ul>
            """,
            "{{HYPERPARAMETER_ROWS_HTML}}": hyper_rows,
            "{{MODEL_COMPAT_ROWS_HTML}}": model_compat_rows,
            "{{CASE_STUDY_SCENARIO}}": html.escape(b.get("real_world_case_study", {}).get("enterprise_scenario", "")),
            "{{CASE_STUDY_OUTCOME}}": html.escape(b.get("real_world_case_study", {}).get("outcome", "")),
            "{{FAQS_HTML}}": faqs_html,
            "{{PARAMETER_INPUTS_HTML}}": param_inputs_html,
            "{{RAW_PROMPT_TEMPLATE}}": html.escape(b.get("raw_prompt_template", "")),
            "{{RELATED_CARDS_HTML}}": related_cards_html
        }

        for k, v in replacements.items():
            page_html = page_html.replace(k, v)

        out_path = os.path.join(BLUEPRINTS_DIR, f"{slug}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)

        generated_urls.append(f"/blueprints/{slug}.html")

    return generated_urls

def generate_categories(categories, blueprints):
    template = load_template("category_template.html")
    ensure_dir(CATEGORIES_DIR)
    generated_urls = []

    for cat in categories:
        slug = cat["slug"]
        print(f"[*] Compiling Topic Silo Hub: {cat['name']} -> categories/{slug}.html")

        # Blueprints belonging to this category
        cat_blueprints = [b for b in blueprints if b.get("category") == slug]
        blueprints_grid_html = "".join([render_blueprint_card(b) for b in cat_blueprints])

        # Other silos
        other_silos = [c for c in categories if c["slug"] != slug]
        other_silos_html = ""
        for other in other_silos:
            other_silos_html += f"""
            <div class="hub-card">
              <h3 class="hub-card-title">{html.escape(other['name'])}</h3>
              <p class="hub-card-desc">{html.escape(other.get('tagline', other.get('description', '')))}</p>
              <a href="/categories/{html.escape(other['slug'])}.html" class="hub-card-link">View Silo &rarr;</a>
            </div>
            """

        page_html = template
        replacements = {
            "{{META_TITLE}}": html.escape(cat.get("meta_title", cat.get("name"))),
            "{{META_DESCRIPTION}}": html.escape(cat.get("meta_description", cat.get("description"))),
            "{{SLUG}}": slug,
            "{{NAME}}": html.escape(cat.get("name")),
            "{{STATS}}": html.escape(cat.get("stats", "Curated")),
            "{{DESCRIPTION}}": html.escape(cat.get("description", "")),
            "{{BLUEPRINTS_GRID_HTML}}": blueprints_grid_html,
            "{{OTHER_SILOS_HTML}}": other_silos_html
        }

        for k, v in replacements.items():
            page_html = page_html.replace(k, v)

        out_path = os.path.join(CATEGORIES_DIR, f"{slug}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)

        generated_urls.append(f"/categories/{slug}.html")

    return generated_urls

def generate_models(models, blueprints):
    template = load_template("model_template.html")
    ensure_dir(MODELS_DIR)
    generated_urls = []

    for m in models:
        slug = m["slug"]
        print(f"[*] Compiling Model Hub: {m['name']} -> models/{slug}.html")

        # Find blueprints that support this model
        supported_blueprints = []
        for b in blueprints:
            for tm in b.get("target_models", []):
                if tm.get("model_id") == slug:
                    supported_blueprints.append(b)
                    break
        
        # If none specifically, display top 3 blueprints as general support
        if not supported_blueprints:
            supported_blueprints = blueprints[:3]

        blueprints_grid_html = "".join([render_blueprint_card(b) for b in supported_blueprints])

        # Other models
        other_models = [om for om in models if om["slug"] != slug]
        other_models_html = ""
        for om in other_models:
            other_models_html += f"""
            <div class="hub-card">
              <h3 class="hub-card-title">{html.escape(om['name'])}</h3>
              <p class="hub-card-desc">{html.escape(om.get('tagline', om.get('strengths', '')))}</p>
              <a href="/models/{html.escape(om['slug'])}.html" class="hub-card-link">View Calibration &rarr;</a>
            </div>
            """

        page_html = template
        replacements = {
            "{{META_TITLE}}": html.escape(m.get("meta_title", m.get("name"))),
            "{{META_DESCRIPTION}}": html.escape(m.get("meta_description", m.get("strengths"))),
            "{{SLUG}}": slug,
            "{{NAME}}": html.escape(m.get("name")),
            "{{DEVELOPER}}": html.escape(m.get("developer", "AI Lab")),
            "{{TAGLINE}}": html.escape(m.get("tagline", "")),
            "{{CONTEXT_WINDOW}}": html.escape(m.get("context_window", "128k")),
            "{{IDEAL_TEMP_RANGE}}": html.escape(m.get("ideal_temperature_range", "0.2 - 0.7")),
            "{{STRENGTHS}}": html.escape(m.get("strengths", "")),
            "{{BLUEPRINTS_GRID_HTML}}": blueprints_grid_html,
            "{{OTHER_MODELS_HTML}}": other_models_html
        }

        for k, v in replacements.items():
            page_html = page_html.replace(k, v)

        out_path = os.path.join(MODELS_DIR, f"{slug}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)

        generated_urls.append(f"/models/{slug}.html")

    return generated_urls

def generate_sitemap_and_robots(all_urls):
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[*] Generating dynamic sitemap.xml with {len(all_urls)} URLs...")

    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    # Priority mapping
    for url in all_urls:
        if url == "/":
            priority = "1.0"
            changefreq = "daily"
        elif url.startswith("/categories/") or url.startswith("/models/"):
            priority = "0.9"
            changefreq = "weekly"
        elif url.startswith("/blueprints/"):
            priority = "0.8"
            changefreq = "weekly"
        else: # legal / static
            priority = "0.5"
            changefreq = "monthly"

        sitemap_lines.append("  <url>")
        sitemap_lines.append(f"    <loc>{DOMAIN}{url}</loc>")
        sitemap_lines.append(f"    <lastmod>{today}</lastmod>")
        sitemap_lines.append(f"    <changefreq>{changefreq}</changefreq>")
        sitemap_lines.append(f"    <priority>{priority}</priority>")
        sitemap_lines.append("  </url>")

    sitemap_lines.append("</urlset>")

    with open(os.path.join(BASE_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_lines) + "\n")

    # Generate robots.txt
    print("[*] Generating robots.txt with absolute sitemap reference...")
    robots_content = f"""# PromptHook AI - Advanced Crawler Directives
User-agent: *
Allow: /

# Googlebot specific
User-agent: Googlebot
Allow: /

# AdSense Crawler
User-agent: Mediapartners-Google
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""
    with open(os.path.join(BASE_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

def main():
    print("=============================================================")
    print("  PromptHook AI &mdash; Programmatic SEO Generator Engine")
    print("=============================================================")
    
    blueprints = load_json(os.path.join(DATA_DIR, "blueprints.json"))
    categories = load_json(os.path.join(DATA_DIR, "categories.json"))
    models = load_json(os.path.join(DATA_DIR, "models.json"))

    core_static_urls = ["/", "/about.html", "/contact.html", "/privacy.html", "/terms.html"]
    
    bp_urls = generate_blueprints(blueprints, categories, models)
    cat_urls = generate_categories(categories, blueprints)
    mod_urls = generate_models(models, blueprints)

    all_urls = core_static_urls + cat_urls + mod_urls + bp_urls
    generate_sitemap_and_robots(all_urls)

    print("\n[+] SUCCESS! Build summary:")
    print(f"    - Blueprints Generated:  {len(bp_urls)}")
    print(f"    - Topic Silos Generated: {len(cat_urls)}")
    print(f"    - Model Hubs Generated:  {len(mod_urls)}")
    print(f"    - Total Indexed URLs:    {len(all_urls)}")
    print("=============================================================\n")

if __name__ == "__main__":
    main()
