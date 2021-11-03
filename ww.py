import requests
from bs4 import BeautifulSoup

# search for remote jobs from weworkremotely.com


def extract_job(result):
    link = result.find("a", recursive=False)["href"]
    company = result.find("span", {"class": "company"}).get_text()
    title = result.find("span", {"class": "title"}).get_text()
    region = result.find("span", {"class": "region company"})

    if link:
        link = f"https://weworkremotely.com{link}"
    if region:
        region = region.get_text()

    return {
        "title": title,
        'company': company,
        'region': region,
        "apply_link": link
    }


def get_extracts(url):
    jobs = []

    print(f"Scrapping ww")
    result = requests.get(f"{url}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find("div", {
        "class": "jobs-container"
    }).find_all("li", {"class": "feature"})

    for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={word}"
    jobs = get_extracts(url)

    return jobs
