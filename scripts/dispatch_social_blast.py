import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

RECIPIENT = "qw9chheouhfhj8pyfnklv5wuvjn0wwtk@hook.eu2.make.com"
SENDER = "broadcast@prompthookai.com"
MX_HOST = "mailhook.eu2.make.com"

CAMPAIGNS = [
    {
        "site": "prompthookai.com",
        "title": "⚡ 30+ Battle-Tested .cursorrules & Self-Improving .mdc Generator",
        "url": "https://www.prompthookai.com/cursorrules.html",
        "excerpt": "Eliminate AI code hallucination and outdated API calls in Cursor & Claude Code. 1-click generator for Next.js 15, FastAPI, Flutter, Supabase, Go and Rust.",
        "bullets": [
            "Continuous Self-Improvement Protocol (.cursor/rules/self-improve.mdc)",
            "Meta-Standardizer rule for team-wide Cursor 2026 conventions",
            "1-click copy & instant file download with zero login or paywall"
        ],
        "tags": "#CursorAI #AIagents #Nextjs #PromptEngineering #WebDev #OpenSource"
    },
    {
        "site": "bestwatchdeals.com",
        "title": "⌚ Best Value Watch Deals & Buying Guide 2026: Automatic & Field Watches",
        "url": "https://www.bestwatchdeals.com",
        "excerpt": "Curated horology roundups and verified deals on sports watches, chronographs, and accessible luxury alternatives from Seiko, Tissot, Hamilton and more.",
        "bullets": [
            "Daily vetted discount tracker across authorized retailers",
            "In-depth mechanical movement reviews and durability tests",
            "Affiliate verified direct links with verified warranty protection"
        ],
        "tags": "#Watches #Horology #WatchDeals #Seiko #MensStyle #AffiliateDeals"
    },
    {
        "site": "ozsponsorjobs.site",
        "title": "🇦🇺 Australia Visa Sponsorship Jobs 2026: Subclass 482 & 186 Vacancies",
        "url": "https://www.ozsponsorjobs.site",
        "excerpt": "Verified employer-sponsored job listings for international professionals seeking relocation to Australia under TSS 482, ENS 186, and regional 494 schemes.",
        "bullets": [
            "Active vacancies in Healthcare, IT, Engineering & Skilled Trades",
            "Direct application routes with accredited Australian employers",
            "Updated eligibility criteria and minimum salary requirements"
        ],
        "tags": "#AustraliaJobs #VisaSponsorship #MigrateToAustralia #Subclass482 #JobSearch"
    }
]

def dispatch_campaign(campaign):
    title = campaign["title"]
    url = campaign["url"]
    excerpt = campaign["excerpt"]
    bullets = "\n".join([f"• {b}" for b in campaign["bullets"]])
    tags = campaign["tags"]
    site = campaign["site"]

    msg = MIMEMultipart('alternative')
    msg['From'] = SENDER
    msg['To'] = RECIPIENT
    msg['Subject'] = f"[{site}] {title}"

    body = f"""{title}

🔗 Direct Link: {url}

{excerpt}

✨ Highlights:
{bullets}

👉 Explore full details free:
{url}

Tags: {tags}
"""
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    print(f"Connecting to {MX_HOST}:25 to dispatch '{site}'...")
    try:
        with smtplib.SMTP(MX_HOST, 25, timeout=15) as server:
            server.ehlo("prompthookai.com")
            server.sendmail(SENDER, [RECIPIENT], msg.as_string())
            print(f"✓ Dispatched [{site}] successfully!")
            return True
    except Exception as e:
        print(f"✗ Failed to dispatch [{site}]: {e}")
        return False

def dispatch_all():
    print(f"Launching multi-campaign broadcast across {len(CAMPAIGNS)} sites...")
    success_count = 0
    for idx, c in enumerate(CAMPAIGNS, 1):
        print(f"\n[{idx}/{len(CAMPAIGNS)}] Broadcasting {c['site']}...")
        if dispatch_campaign(c):
            success_count += 1
        time.sleep(2)  # courteous delay between dispatches

    print(f"\n==========================================")
    print(f"Completed! {success_count}/{len(CAMPAIGNS)} campaigns dispatched to Make.com.")
    print(f"==========================================")

if __name__ == "__main__":
    dispatch_all()
