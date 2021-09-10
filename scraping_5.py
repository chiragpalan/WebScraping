# scraping for jos on one page posted few days ago
# Adding some more functionality in scraping_4.py

from bs4 import BeautifulSoup
import requests
import time

print('Put some unfamiliar skills')
Unfamiliar_skill = input('>')
print(f'filtering out {Unfamiliar_skill}')

def job_search():

    url = '''https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation='''
    html_text = requests.get(url).text
    #print(html_text)
    soup = BeautifulSoup(html_text,'lxml')
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
    
    # looking for each job in jobs
    no_of_jobs = 0
    for index, job in enumerate(jobs):
        posted_on = job.find('span', class_ = 'sim-posted').text
        
        if 'few' in posted_on:
            no_of_jobs += 1
            company_name = job.find('h3', class_ = 'joblist-comp-name').text.rstrip().lstrip()
            #print(company_name)
            key_skills = [i for i in job.find('span', class_ = 'srp-skills').text.split() if len(i)>1]
            more_info = job.header.h2.a['href']
            
            if Unfamiliar_skill not in key_skills:
                with open(f'C://Users//chigs//snipit//JobsPosts//{index}.txt','w' ) as f:                   
                    
                    f.write(f'''Company Name: {company_name}, \nRequired_skills: {key_skills}\n''')
                    f.write(f'''For More info check --> {more_info} \n''')
                    #f.write('*' * 20)
                    #f.write(f'for more info check --> {more_info}/n')
                
                print(f'file saved: {index}')
        
    #print(no_of_jobs)

if __name__ == '__main__':
    while True:
        job_search()
        wait_time = 10
        print(f'Waiting {wait_time} seconds...')
        time.sleep(wait_time) # 600 sec of wait time between each run