import requests
from bs4 import BeautifulSoup


# search for remote jobs from stack overflow

# step 1 get the page
def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
  last_pages = pages[-2].get_text(strip=True)

  return int(last_pages)

# step 3 extract job
def extract_job(result):
  title = result.find("h2").find("a")["title"]
  company, location = result.find("h3").find_all("span", recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True).strip("-").strip(" \r ").strip("\n")
  job_id = result['data-jobid']
  return {
    "title":title,
    'company': company,
    'location': location,
    "apply_link": f"https://stackoverflow.com/jobs/{job_id}"
  }

# step 2 make request
def get_extracts(url, last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping So: page : {page+1}")
    result = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "-job"})

    # step 3 extract job
    for result in results:
      job = extract_job(result)
      jobs.append(job)

  return jobs
      
    
  



def get_jobs(word):
  url = f"https://stackoverflow.com/jobs?r=true&q={word}"
  # step 1 get the page
  last_page = get_last_page(url)
  # step 2 make request
  jobs = get_extracts(url, last_page)
  
  return jobs