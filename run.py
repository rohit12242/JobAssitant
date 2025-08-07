# run.py

from scrapers.linkedin_scraper import scrape_linkedin_jobs

def main():
    query = "Python Developer"
    location = "Remote"
    jobs = scrape_linkedin_jobs(query, location, posted_filter="past_24_hours")

    for idx, job in enumerate(jobs, start=1):
        print(f"{idx}. {job['title']} at {job['company']}")
        print(f"   🔗 {job['link']}\n")

if __name__ == "__main__":
    main()
