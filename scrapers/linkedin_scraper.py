# scrapers/linkedin_scraper.py

from playwright.sync_api import sync_playwright
import time

def scrape_linkedin_jobs(query: str, location: str = "Remote", posted_filter: str = "past_24_hours", max_jobs: int = 10):
    print(f"🔍 Searching LinkedIn for: '{query}' in '{location}' with filter '{posted_filter}'")

    # Map filters to LinkedIn URL params
    date_filter_map = {
        "any": "",
        "past_24_hours": "f_TPR=r86400",  # posted in last 24 hours
        "past_week": "f_TPR=r604800"
    }

    query_formatted = query.replace(" ", "%20")
    location_formatted = location.replace(" ", "%20")
    date_param = date_filter_map.get(posted_filter, "")

    search_url = f"https://www.linkedin.com/jobs/search/?keywords={query_formatted}&location={location_formatted}&{date_param}"

    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # browser = p.chromium.launch(headless=False, slow_mo=500)  # 500 ms delay between actions

        page = browser.new_page()

        print(f"🌐 Visiting: {search_url}")
        page.goto(search_url)

        # page.pause()

        # Wait for page to load and try to close popup
        try:
            page.wait_for_selector("button[aria-label='Dismiss']", timeout=5000)
            page.click("button[aria-label='Dismiss']")
            print("❎ Closed popup successfully.")
        except TimeoutError:
            print("⚠️ No popup found, continuing...")

        page.wait_for_timeout(5000)  # wait 5 seconds for job cards to load
        # page.pause()

        # job_cards = page.query_selector_all(".jobs-search__results-list-item")
        job_cards = page.query_selector_all("ul.jobs-search__results-list > li")
        print(f"Found {len(job_cards)} job cards")

        for card in job_cards[:max_jobs]:
            try:
                title = card.query_selector("h3").inner_text()
                company = card.query_selector("h4").inner_text()
                link = card.query_selector("a").get_attribute("href")

                jobs.append({
                    "title": title,
                    "company": company,
                    "link":  link
                })
            except Exception as e:
                print(f"⚠️ Error parsing job card: {e}")
                continue

        browser.close()

    print(f"✅ Scraped {len(jobs)} jobs.")
    return jobs
