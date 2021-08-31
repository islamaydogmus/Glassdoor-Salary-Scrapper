from os import curdir
from bs4 import BeautifulSoup as soup
import requests
import re
import pandas as pd
from requests.api import head

def search_salary(job_title,location):
    """
    Fuction that searches for top 15 most recorded salaries for given job in given area and returns what he can find.
    Location can only be Turkey, Germany and United States at the time being since I don't fully grasped how glassdoor uses his url methods
    """

    # Requesting URL
    search_name = job_title.strip().lower().replace(" ","-")
    search_location = location.strip().lower()
    headers = {"user-agent":"Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18"}
    if location.lower() == "turkey":
        url = "https://www.glassdoor.com/Salaries/turkey-"+ search_name + "-salary-SRCH_IL.0,6_IN238_KO7,24.htm?clickSource=searchBtn"
    elif location.lower() == "germany":
        url = "https://www.glassdoor.com/Salaries/germany-"+ search_name + "-salary-SRCH_IL.0,7_IN96_KO8,25.htm?clickSource=searchBtn"
    elif location.lower() == "united states":
        url = "https://www.glassdoor.com/Salaries/"+ search_name + "-salary-SRCH_KO0,17.htm"
    req = requests.get(url,headers=headers)

    # Scraping the names
    bsobj = soup(req.content,'lxml')
    jobs = bsobj.find_all('div',{'class':'css-1oz9wk4 e1j46pbu0'})
    if len(jobs) == 0:
        return None
    
    try:
        companies = jobs[0].find_all("tbody")
        titles = companies[0].find_all("a")
        prices = companies[0].find_all("span")

        titles = [re.findall("(.*) salaries -.*",title.string)[0] for title in titles] # [title.string for title in titles] 
        prices = [re.findall("<.*>(.*)<.*>",str(price).replace("<!-- -->","").replace("\xa0"," "))[0] for price in prices]
        
        
        salary = [int(re.findall("[€$TRY]*(\d*,\d*)\/[\w]*",str(price))[0].replace(",","")) for price in prices]
        currency = [re.findall("([€$TRYs]*).*",str(price))[0] for price in prices]
        payment_interval = [re.findall(".*\/([\w]*)",str(price))[0] for price in prices]
    except IndexError:
        return None

    return pd.DataFrame(list(zip(titles,salary,currency,payment_interval)),columns=["Title","Salary","Currency","Payment Interval"])
