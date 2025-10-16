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

        page.set_default_timeout(10000)
        page.goto("https://remoteok.com/", wait_until="networkidle")

        rows = page.locator("tr.job")

        for row in rows.all()[:limit]:
            try:
                # --- BASIC DETAILS ---
                title = row.locator("td.position h2").inner_text().strip()
                company = row.locator("td.company h3").inner_text().strip()

                # --- TAGS / TECH STACK ---
                tags_list = []
                try:
                    tag_elements = row.locator("td.tags a, td.tags span, div.tags a")
                    tags_list = [
                        t.inner_text().strip()
                        for t in tag_elements.all()
                        if t.inner_text().strip()
                    ]
                except Exception:
                    tags_list = []
                tech_stack = ", ".join(tags_list) if tags_list else None

                # --- DATE POSTED ---
                try:
                    date_attr = row.locator("td.time time").get_attribute("datetime")
                    date_posted = (
                        datetime.fromisoformat(date_attr)
                        if date_attr
                        else datetime.now()
                    )
                except Exception:
                    date_posted = datetime.now()

                # --- LINKS ---
                job_anchor = row.locator("td.position a.preventLink").first
                href = job_anchor.get_attribute("href") if job_anchor else None
                job_url = f"https://remoteok.com{href}" if href else None

                apply_anchor = row.locator("a[rel='noindex nofollow']").first
                apply_url = (
                    f"https://remoteok.com{apply_anchor.get_attribute('href')}"
                    if apply_anchor
                    else None
                )

                # --- LOGO ---
                logo = None
                try:
                    if row.locator("td.has-logo img").count() > 0:
                        logo = (
                            row.locator("td.has-logo img")
                            .first.get_attribute("data-src", timeout=2000)
                        )
                except Exception:
                    logo = None

                # --- JOB TYPE ---
                job_type = next(
                    (
                        tag
                        for tag in tags_list
                        if any(x in tag.lower() for x in ["full", "part", "contract"])
                    ),
                    "N/A",
                )

                # --- SALARY EXTRACTION (Fixed) ---
                                # --- SALARY EXTRACTION (Improved Universal Catch) ---
                salary = None
                try:
                    # 1️⃣ Look for a dedicated salary cell
                    salary_cell = row.locator("td.salary, td.tags span, td.tags a")
                    if salary_cell.count() > 0:
                        for element in salary_cell.all():
                            text = element.inner_text().strip()
                            tooltip = element.get_attribute("data-tooltip") or ""
                            combined_text = f"{text} {tooltip}"
                            match = re.search(
                                r"\$?\d{2,3}\s?[kK](?:\s*[-–]\s*\$?\d{2,3}\s?[kK])?",
                                combined_text
                            )
                            if match:
                                salary = match.group(0)
                                break

                    # 2️⃣ Fallback: search full row HTML for salary patterns
                    if not salary:
                        html = row.inner_html()
                        match = re.search(
                            r"\$?\d{2,3}\s?[kK](?:\s*[-–]\s*\$?\d{2,3}\s?[kK])?",
                            html
                        )
                        if match:
                            salary = match.group(0)
                except Exception as e:
                    print(f"⚠️ Salary extraction failed for {title}: {e}")


                # --- FINAL STRUCTURED JOB RECORD ---
                jobs.append(
                    {
                        "title": title,
                        "company": company,
                        "location": "Remote",
                        "salary": salary,
                        "tech_stack": tech_stack,
                        "job_type": job_type,
                        "logo": logo,
                        "source": "RemoteOK",
                        "external_id": job_url,
                        "apply_url": apply_url,
                        "date_posted": date_posted,
                    }
                )

            except Exception as e:
                print("⚠️ Error parsing a job row:", e)
                continue

        browser.close()

    print(f"✅ Scraped {len(jobs)} job listings successfully.")
    return jobs
