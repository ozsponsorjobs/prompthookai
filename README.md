# PromptHook AI &mdash; Hyper-Optimized Prompt Blueprints

> **Tagline:** Hyper-optimized prompt blueprints. Inject parameters, stream instant configurations.  
> **Canonical Domain:** [https://www.prompthookai.com/](https://www.prompthookai.com/)  
> **Tech Stack:** Pure Static HTML5 + Modern Vanilla CSS3 + Vanilla JavaScript (Zero bloated frameworks, 100% Google PageSpeed score).

---

## ⚡ Architectural Overview

PromptHook AI is an enterprise-grade programmatic SEO platform engineered for AI developers, prompt architects, and engineering leaders. Every blueprint is treated as an executable software specification rather than conversational prose.

### 🌟 Core Capabilities
1. **Interactive Client-Side Parameter Injector:**
   - Real-time variable substitution directly in the browser runtime (Zero server transmission &rarr; 100% private).
   - Live token footprint counter (`~tokens`).
   - 1-click clipboard copy with visual feedback.
2. **Programmatic Silo & Topic Clusters (E-E-A-T Ready):**
   - 6 Core Topic Silos (`categories/*.html`).
   - 4 Model Architecture Hubs (`models/*.html`).
   - 1,200 to 1,500+ words per generated blueprint page, featuring AST breakdowns, negative guardrails, hyperparameter tuning matrices, and FAQ schema to guarantee zero "thin content" penalties.
3. **Advanced Technical SEO & Dual Schemas:**
   - Multi-graph JSON-LD: `BreadcrumbList` + `TechArticle` / `SoftwareApplication` + `FAQPage` + `WebSite`.
   - Open Graph & Twitter Cards.
   - Dynamic `sitemap.xml` with priority and change frequencies.
   - Advanced `robots.txt` with specific crawler allowances for Googlebot and Google AdSense Mediapartners.
4. **Google AdSense & Privacy Compliance:**
   - Compliant `privacy.html` (Google AdSense, DoubleClick DART, GDPR, CCPA).
   - `terms.html`, `about.html` (E-E-A-T methodology), and `contact.html` (with real-time vanilla JS validation).
   - Lightweight Cookie Consent banner saving state to `localStorage`.
   - Dedicated high-CTR responsive ad zones (`.ad-zone-container`).
5. **Instant Indexing Automation:**
   - `scripts/indexing_api.py` for automated batch notifications to Google Indexing API and Google Search Console.

---

## 📁 Directory Structure

```text
prompthookai.com/
├── index.html                       # Flagship homepage with instant search and live category filter
├── about.html                       # Authoritative E-E-A-T methodology and testing rubric
├── contact.html                     # Contact portal with vanilla JS form validation
├── privacy.html                     # Privacy policy (GDPR, CCPA, AdSense & DART cookies)
├── terms.html                       # Terms of service and commercial open license
├── sitemap.xml                      # Generated XML sitemap (21 URLs indexed)
├── robots.txt                       # Search crawler directives
│
├── categories/                      # Topic Silo Hubs
│   ├── code-engineering.html
│   ├── autonomous-agents.html
│   ├── data-analytics.html
│   ├── seo-content-strategy.html
│   ├── growth-marketing.html
│   └── customer-support.html
│
├── models/                          # Model Calibration Hubs
│   ├── gpt-4o.html
│   ├── claude-sonnet-3-7.html
│   ├── deepseek-r1.html
│   └── gemini-2-flash.html
│
├── blueprints/                      # 1,200+ word programmatic blueprint pages
│   ├── enterprise-codebase-refactor-security-auditor.html
│   ├── autonomous-react-agent-tool-orchestrator.html
│   ├── zero-hallucination-json-extractor.html
│   ├── programmatic-seo-silo-content-architect.html
│   ├── b2b-saas-cold-outreach-sequence-engine.html
│   └── multiturn-customer-support-triage-arbiter.html
│
├── assets/
│   ├── css/
│   │   ├── main.css                 # Dark modern developer stylesheet (Zero dependencies)
│   │   └── blueprint.css            # Interactive sandbox, code blocks, tables, and FAQ styles
│   └── js/
│       ├── app.js                   # Homepage instant search & filtering
│       ├── blueprint-runtime.js     # Live parameter injector & copy engine
│       └── cookie-consent.js        # GDPR / AdSense cookie consent banner
│
├── data/
│   ├── blueprints.json              # Master blueprints dataset
│   ├── categories.json              # Category taxonomy & metadata
│   └── models.json                  # Model hyperparameter guidelines
│
└── scripts/
    ├── generator.py                 # Programmatic site generator
    ├── indexing_api.py              # Google Indexing API automation tool
    └── templates/                   # Clean HTML templates for compilation
```

---

## 🚀 How to Run & Generate Locally

### 1. Rebuild All Programmatic Pages & Sitemap
Whenever you add or edit records in `data/blueprints.json`, `data/categories.json`, or `data/models.json`:
```bash
python scripts/generator.py
```
This automatically updates:
- All `blueprints/*.html`
- All `categories/*.html`
- All `models/*.html`
- `sitemap.xml`
- `robots.txt`

### 2. Preview the Site Locally
You can run any local static web server:
```bash
python -m http.server 8000
```
Open your browser at `http://localhost:8000`.

---

## 🔍 Google Indexing API Setup

To send batch indexing requests to Google:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable both the **Webmaster Tools API (Search Console)** and the **Indexing API**.
3. Create a **Service Account** and generate a **JSON key file**.
4. Save the key file to:
   ```text
   scripts/service_account.json
   ```
5. In **Google Search Console**, add your Service Account email (e.g. `your-service@project.iam.gserviceaccount.com`) as an **Owner** under *Settings &rarr; Users and permissions*.
6. Run the indexing script:
   ```bash
   # Dry-Run Simulation (Tests all URLs without consuming quota):
   python scripts/indexing_api.py

   # Live Batch Dispatch to Google:
   python scripts/indexing_api.py --live
   ```

---

## 🌐 Deployment to GitHub Pages or Cloudflare Pages

### Option A: GitHub Pages
1. Initialize git and commit:
   ```bash
   git init
   git add .
   git commit -m "feat: initial PromptHook AI release"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/prompthookai.git
   git push -u origin main
   ```
2. In your GitHub repository, navigate to **Settings &rarr; Pages**.
3. Under **Branch**, select `main` and root directory `/`. Click **Save**.
4. Set your custom domain `www.prompthookai.com`.

### Option B: Cloudflare Pages
1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/) &rarr; **Workers & Pages**.
2. Click **Create Application &rarr; Pages &rarr; Connect to Git**.
3. Select your repository.
4. Set build settings:
   - Framework preset: `None`
   - Build output directory: `.` (root)
5. Deploy. Cloudflare will serve all static assets across their ultra-fast global edge network with instant HTTP/3 and 100% PageSpeed.

---

## 💰 Google AdSense Approval Checklist

- [x] **Zero Thin Content:** Every blueprint page exceeds 1,200 to 1,500 words of technical guidance.
- [x] **AdSense-Compliant Privacy Policy:** Explicitly includes DART cookie disclosures, Google AdSense third-party vendor clause, GDPR rights, and CCPA terms in `privacy.html`.
- [x] **E-E-A-T Demonstration:** Dedicated `about.html` explaining prompt benchmarking criteria and the 4-stage testing rubric.
- [x] **Contact Portal:** `contact.html` with working input validation, SLA, and email contact info.
- [x] **Cookie Consent:** Banner implemented via `assets/js/cookie-consent.js` storing consent in `localStorage`.
- [x] **Ad Zones:** Non-intrusive container placeholders (`.ad-zone-container`) ready for your `adsbygoogle` snippet.

---

&copy; 2026 PromptHook AI. Engineered for zero-defect LLM prompt execution.
