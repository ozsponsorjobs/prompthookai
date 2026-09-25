import urllib.request
import ssl
import subprocess

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Nameservers check
print("=== 1. CHECKING NAMESERVERS (NS) ===")
try:
    ns_out = subprocess.check_output("nslookup -type=NS prompthookai.com 8.8.8.8", shell=True).decode()
    for line in ns_out.splitlines():
        if "nameserver" in line.lower():
            print(" ", line.strip())
except Exception as e:
    print("  NS lookup error:", e)

# 2. HTTP check
print("\n=== 2. CHECKING HTTP LIVE RESPONSE ===")
urls_to_test = [
    "https://www.prompthookai.com/",
    "https://www.prompthookai.com/about.html",
    "https://www.prompthookai.com/2026/09/apple-store-aso-expert-guide.html"
]

for url in urls_to_test:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            title = "No Title"
            for line in content.splitlines():
                if "<title>" in line.lower():
                    title = line.strip()
                    break
            print(f"{url}:")
            print(f"  Status: {resp.status}")
            print(f"  Server: {resp.headers.get('Server')}")
            print(f"  CF-Ray: {resp.headers.get('CF-RAY')}")
            print(f"  Title:  {title}")
    except Exception as e:
        print(f"{url}: ERROR -> {e}")
