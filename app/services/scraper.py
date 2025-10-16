import re
from datetime import datetime
from playwright.sync_api import sync_playwright



def scrape_remoteok(limit: int = 30):
    """
    Scrape detailed job listings from RemoteOK.
    Returns a list of job dictionaries ready for database insertion.
    """
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the site fully (JS included)
        page.goto("https://remoteok.com/", wait_until="networkidle")

        # Select all job rows
        rows = page.locator("tr.job")

        for row in rows.all()[:limit]:
            try:
                # Core job fields
                title = row.locator("td.position h2").inner_text().strip()
                company = row.locator("td.company h3").inner_text().strip()
                tags_list = row.locator("td.tags span").all_inner_texts()
                tags = ", ".join(tags_list)

                # Extract posting date (if present)
                try:
                    date_attr = row.locator("td.time time").get_attribute("datetime")
                    date_posted = (
                        datetime.fromisoformat(date_attr)
                        if date_attr
                        else datetime.now()
                    )
                except Exception:
                    date_posted = datetime.now()

                # Job URL (the main listing link)
                job_anchor = row.locator("td.position a.preventLink").first
                href = job_anchor.get_attribute("href") if job_anchor else None
                job_url = f"https://remoteok.com{href}" if href else None

                # Apply button link (direct apply)
                apply_anchor = row.locator("a[rel='noindex nofollow']").first
                apply_url = (
                    f"https://remoteok.com{apply_anchor.get_attribute('href')}"
                    if apply_anchor
                    else None
                )

                # Company logo (if available)
                logo = row.locator("td.has-logo img").first.get_attribute("data-src") if row.locator("td.has-logo img").count() > 0 else None


                # Guess job type (Full-time, Part-time, Contract)
                job_type = next(
                    (
                        tag
                        for tag in tags_list
                        if any(x in tag.lower() for x in ["full", "part", "contract"])
                    ),
                    "N/A",
                )

                # 🔥 Extract salary if listed in tags
                salary = None
                for tag in tags_list:
                    match = re.search(
                        r"\$?\d{2,3}k(?:\s*[-–]\s*\$?\d{2,3}k)?", tag.lower()
                    )
                    if match:
                        salary = match.group(0)
                        break

                jobs.append(
                    {
                        "title": title,
                        "company": company,
                        "location": "Remote",
                        "salary": salary,
                        "tech_stack": tags,
                        "job_type": job_type,
                        "logo": logo,
                        "source": "RemoteOK",
                        "external_id": job_url,
                        "apply_url": apply_url,
                        "date_posted": date_posted,
                    }
                )

            except Exception as e:
                print("Error parsing a job:", e)
                continue

        browser.close()

    return jobs
