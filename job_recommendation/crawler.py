import random

from playwright.sync_api import sync_playwright


def crawl_jobs() -> list:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.amazon.jobs/en/search?base_query=&loc_query=", wait_until="load")
        job_list = []
        page_no = 0
        while True:
            # Wait for job tiles to be rendered
            page.wait_for_selector(".job-tile")

            jobs = page.query_selector_all(".job-tile")
            for job in jobs:
                loc_and_job_id = job.query_selector(".list-unstyled").inner_text()
                location_and_job_id_list = loc_and_job_id.split('|')
                job_list.append({
                    "title": job.query_selector(".job-title").inner_text(),
                    "location": location_and_job_id_list[0].strip(),
                    "job_id": location_and_job_id_list[1].strip(),
                    "posted_at": job.query_selector(".posting-date").inner_text(),
                    "description": job.query_selector(".qualifications-preview").inner_text()
                })
            page_no += 1
            # try clicking 'Next' button for pagination
            next_button = page.query_selector(".btn.circle.right")
            if next_button and next_button.is_enabled():
                next_button.click()
                delay = random.uniform(4000, 7000)
                page.wait_for_timeout(delay)
            else:
                break

            if page_no > 3:
                break

        browser.close()
        return job_list
