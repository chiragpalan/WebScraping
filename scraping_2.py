# scrapping job website
# scraping for single job
from bs4 import BeautifulSoup
import requests
url = '''https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation='''
html_text = requests.get(url).text
#print(html_text)
soup = BeautifulSoup(html_text,'lxml')
job = soup.find('li', class_ = 'clearfix job-bx wht-shd-bx')
company_name = job.find('h3', class_ = 'joblist-comp-name').text.rstrip().lstrip()
key_skills = [i for i in job.find('span', class_ = 'srp-skills').text.split() if len(i)>1]
#print(key_skills)
posted_on = job.find('span', class_ = 'sim-posted').text
print(posted_on)
