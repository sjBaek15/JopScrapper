import requests
from bs4 import BeautifulSoup

# search for remote jobs from weworkremotely.com


def extract_job(result):
  try:
    link = result.find("a", itemprop="url")['href']
    company = result.find("h3", itemprop="name").get_text()
    title = result.find("h2", itemprop="title").get_text()
    location = result.find("div", class_="location").get_text()

    return{
      'title': title,
      'company': company,
      'location': location,
      'link': f"https://remoteok.io{link}",
    }
    print(link, company, title, location)
  except:
    return None    


def get_extracts(url):
    jobs = []

    print(f"Scrapping ro")
    result = requests.get(f"{url}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find("table", {
        "id": "jobsboard"
    }).find_all("tr")
    
    for result in results:
        job = extract_job(result)
        if job != None:
          jobs.append(job)        
    return jobs


def get_jobs(word):
    url = f"https://remoteok.io/remote-dev+{word}-jobs"
    jobs = get_extracts(url)
    
    return jobs
