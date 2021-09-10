# scraping for jos on one page posted few days ago
from bs4 import BeautifulSoup
import requests
url = '''https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation='''
html_text = requests.get(url).text
#print(html_text)
soup = BeautifulSoup(html_text,'lxml')
jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

# looking for each job in jobs
no_of_jobs = 0
for job in jobs:
    posted_on = job.find('span', class_ = 'sim-posted').text
    
    if 'few' in posted_on:
        no_of_jobs += 1
        company_name = job.find('h3', class_ = 'joblist-comp-name').text.rstrip().lstrip()
        print(company_name)
        key_skills = [i for i in job.find('span', class_ = 'srp-skills').text.split() if len(i)>1]
        more_info = job.header.h2.a['href']
        print(more_info)
        print(f'''Company Name: {company_name}, \nRequired_skills: {key_skills}
              ''')
        print('*' * 20)
    
#print(no_of_jobs)
