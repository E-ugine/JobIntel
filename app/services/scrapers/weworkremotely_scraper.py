import re
from datetime import datetime
from playwright.sync_api import sync_playwright

def scrape_weworkremotely(limit: int = 30):
    """
    Resilient WeWorkRemotely scraper using multiple selector fallbacks and richer extraction.
    """
    jobs = []
    base_url = "https://weworkremotely.com"
    url = f"{base_url}/remote-jobs"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=40000)

        print(f"Visiting {url} ...")

        job_data = page.evaluate(
            """() => {
                const results = [];
                const rows = document.querySelectorAll('li.feature a[href^="/remote-jobs/"]');
                for (const link of rows) {
                    const li = link.closest('li.feature');
                    if (!li) continue;

                    const title = (
                        li.querySelector('span.title, h2, h3, a')?.innerText.trim() ||
                        li.querySelector('span')?.innerText.trim() ||
                        'Unknown Title'
                    );

                    const company = (
                        li.querySelector('span.company, .company, h4, strong')?.innerText.trim() ||
                        li.querySelector('div.company')?.innerText.trim() ||
                        'Unknown Company'
                    );

                    const tags = Array.from(
                        li.querySelectorAll('span.region, span.tag, .tooltip, .feature-tag')
                    )
                    .map(el => el.innerText.trim())
                    .filter(Boolean);

                    const logo = li.querySelector('div.logo img')?.src || null;
                    const job_url = link.href;

                    results.push({ title, company, tags, logo, job_url });
                }
                return results;
            }"""
        )

        browser.close()

    for j in job_data[:limit]:
        tech_stack = ", ".join(j["tags"]) if j["tags"] else None
        salary = None
        try:
            match = re.search(
                r"\$?\d{2,3}\s?[kK](?:\s*[-–]\s*\$?\d{2,3}\s?[kK])?",
                " ".join(j["tags"]) + " " + j["title"]
            )
            if match:
                salary = match.group(0)
        except Exception:
            pass

        jobs.append(
            {
                "title": j["title"].title(),
                "company": j["company"].title(),
                "location": "Remote",
                "salary": salary,
                "tech_stack": tech_stack,
                "job_type": "Remote",
                "logo": j["logo"],
                "source": "WeWorkRemotely",
                "external_id": j["job_url"],
                "apply_url": j["job_url"],
                "date_posted": datetime.now(),
            }
        )

    print(f"Scraped {len(jobs)} job listings successfully from WeWorkRemotely.")
    return jobs
