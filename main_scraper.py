from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint
from datetime import date
import pandas as pd
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
#from webdriver_manager.chrome import ChromeDriverManager

website = """
Written By @agawand2 29/4/2023 12.40.31
#########################################
#           WEBSITE: naukri.com          #
######################################### 
"""
print(website)
start_time = datetime.now()
print('Crawl starting time : {}' .format(start_time.time()))
print()

df = pd.DataFrame(columns=['Title','Company','Ratings','Expirience','Location','Minimum Requirements','Tech Stack'])

def generate_url(index):
    if index == 1:
        return "https://www.naukri.com/java-developer-jobs-in-india"
    else:
        return format("https://www.naukri.com/java-developer-jobs-in-india-{}".format(index))
    return url

def extract_rating(rating_a):
    if rating_a is None or rating_a.find('span', class_="main-2") is None:
        return "None"
    else:
        return rating_a.find('span', class_="main-2").text

  
def parse_job_data_from_soup(page_jobs):
    df = pd.DataFrame(columns=['Title','Company','Ratings','Expirience','Location','Minimum Requirements','Tech Stack'])
    print("********PAGE_JOBS***********")
    for job in page_jobs:
        job = BeautifulSoup(str(job), 'html.parser')
        row1 = job.find('div', class_="row1")
        row2 = job.find('div', class_="row2")
        row3 = job.find('div', class_="row3")
        row4 = job.find('div', class_="row4")
        row5 = job.find('div', class_="row5")
        row6 = job.find('div', class_="row6")
        print("*************START***************")
        job_title = row1.a.text
        # print(row2.prettify())
        company_name = row2.span.a.text
        rating_a = row2.span
        rating = extract_rating(rating_a)
        
        job_details = row3.find('div', class_="job-details")
        ex_wrap = job_details.find('span', class_="exp-wrap").span.span.text
        location = job_details.find('span', class_="loc-wrap ver-line").span.span.text

        min_requirements = row4.span.text

        all_tech_stack = []
        for tech_stack in row5.ul.find_all('li', class_="dot-gt tag-li "):
            tech_stack = tech_stack.text
            all_tech_stack.append(tech_stack)
        """"
        #This part is to print results on terminal
        print("Job Title : {}" .format(job_title))
        print("Company Name : {}" .format(company_name))
        print("Rating : {}" .format(rating))
        print("Experience : {}" .format(ex_wrap))
        print("Location : {}" .format(location))
        print("Minimum Requirements : {}" .format(min_requirements))
        print("All Tech Stack : {}" .format(all_tech_stack))
        """
        temp_df={'Title':job_title,'Company':company_name,'Ratings':rating,'Expirience':ex_wrap,'Location':location,'Minimum Requirements':min_requirements,'Tech Stack':all_tech_stack}
        df=df._append(temp_df,ignore_index=True)
    print(df)
    today=date.today()
    df.to_csv('dataset{}.csv'.format(today))
    


options = webdriver.ChromeOptions() 
options.headless = True 
driver=webdriver.Chrome(options=options)

start_page = 1
# edit the page_end here
page_end = 2
for i in range(start_page, page_end):
    print(i)
    url = generate_url(i)
    driver.get(url)
    # sleep for 5-10 seconds randomly just to let it load
    sleep(randint(5, 10))
    get_url = driver.current_url
    if get_url == url:
        page_source = driver.page_source

    # Generate the soup
    soup = BeautifulSoup(page_source, 'html.parser')
    page_soup = soup.find_all("div", class_="srp-jobtuple-wrapper")
    parse_job_data_from_soup(page_soup)


