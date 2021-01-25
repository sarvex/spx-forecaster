#from IPython.core.display import clear_output
from datetime import timedelta
from bs4 import BeautifulSoup
from pytz import timezone

import pandas as pd
import datetime
import requests
import re

TIME_UNIT_LOOKUP = {
    "mins" : "minutes", 
    "hrs" : "hours"
    }

# for DailyFX
def get_dailyfx(page):
    url = dfx + str(page)
    print(url)
    response = requests.get(url, headers=headers)
    collection = []

    if(response.ok):
        data = response.text
        soup = BeautifulSoup(data, "html.parser")
        articles = soup.select("body > div.dfx-slidableContent > div > div.container > div > div.col-xl-8.dfx-border--r-xl-1 > div.dfx-articleList.jsdfx-articleList")

        for article in articles:  
            headlines = article.select("span.align-middle")
            span = article.select("span.text-nowrap")
            
        for i in range(0, len(headlines)):
            headline = str(headlines[i]).split('>')[1].split('<')[0]
            date = span[i]['data-time'].split('+')[0]
            dt = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S') + timedelta(hours=-5) # adjusting for EST
            dt_ = dt.strftime("%Y-%m-%d %H:%M:%S-05:00)

            nres = {
                "headline" : headline,
                "date" : dt_
            }
            collection.append(nres)
            #sleep(2)

        #print(collection)

    else:
        print(f"No response on page {page}")

    return collection

# for FXEmpire
def get_fxempire(page):
    url = fxe + str(page)
    print(url)
    response = requests.get(url, headers=headers)
    collection = []

    if(response.ok):
        data = response.text
        soup = BeautifulSoup(data, "html.parser")
        articles = soup.select("div.Article-sc-178sudu-0")
        
        for article in articles:
            text = article.get_text()
            text_ = text.split('\n')
            i = 1

            for title in article.select("a.Link-y81klt-0"):
                preproc = title.get_text()
                preproc_ = preproc.split('\n')[0]
                i +=1

                if i==2:
                    #headline.append(preproc_)
                    hd = preproc_

            for time in article.select("time"):
                dt = time["datetime"]
                dt = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S') + timedelta(hours=-5) # adjusting for EST
                dt_ = dt.strftime("%Y-%m-%d %H:%M:%S-05:00")           

            nres = {
                "headline" : hd,
                "date" : dt_
            }
            collection.append(nres)
            #sleep(2)

        #print(collection)

    else:
        print(f"No response on page {page}")
    
    return collection

# for CNBC
def get_cnbc(page):
    url = cnbc + str(page)
    print(url)
    response = requests.get(url, headers=headers)
    collection = []

    if(response.ok):
        data = response.text
        soup = BeautifulSoup(data, "html.parser")
        articles = soup.select("#pipeline_assetlist_0")

        for article in articles:
            headlines = article.select("div.headline > a")
            timedata = article.select("time")
        
        for i in range(0,len(headlines)):
            headline = str(headlines[i]).split('>')[1].split('<')[0].strip()
            date = str(timedata[i]).split('>')[1].split('<')[0].strip()
                    
            if "Ago" in date:
                parsed_s = [date.split()[:2]]
                parsed_s[0][1] = parsed_s[0][1].lower()
                if "s" not in parsed_s[0][1]:
                    parsed_s[0][1] += "s"
                time_dict = dict((TIME_UNIT_LOOKUP.get(fmt,fmt),float(amount)) for amount,fmt in parsed_s)
                dt = datetime.timedelta(**time_dict)
                past_time = datetime.datetime.now(est) - dt
                dt_ = past_time.strftime("%Y-%m-%d %H:%M:%S-05:00")

                nres = {
                    "headline" : headline,
                    "date" : dt_
                }
                collection.append(nres)

            elif ":" in date:
                hours = date[:2].replace(':', '')
                day = date.split(' ')[-3]

                if int(hours) < 10:
                    date = "0" + date                    

                if 'Sept' or 'July' or 'June' or 'March' or 'April' in date: # March, April, June, July, and Sept do not come in three-letter abbreviated format
                    date = date.replace('Sept', 'Sep').replace('July', 'Jul').replace('June', 'Jun').replace('April', 'Apr').replace('March', 'Mar')
                dt = datetime.datetime.strptime(date, '%H:%M  %p ET %a,  %d %b %Y')
                dt_ = dt.strftime("%Y-%m-%d %H:%M:%S-05:00")
                nres = {
                    "headline" : headline,
                    "date" : dt_
                }
                collection.append(nres)
                #sleep(2)

    else:
        print(f"No response on page {page}")
    
    return collection

# for Investing.com
def get_investing(page):
    url = inv + str(page)
    print(url)
    response = requests.get(url, headers=headers)
    collection = []

    if(response.ok):
        data = response.text
        soup = BeautifulSoup(data, "html.parser")
        articles = soup.select("div.mediumTitle1 > article.articleItem")

        for article in articles:
            text = article.get_text()
            text_ = text.strip().split('\n')
            
            to_filter = text_

            while("" in to_filter) : 
                to_filter.remove("")             
            
            if (len(to_filter) > 1):
                headline = to_filter[0].strip()
                date = to_filter[1].strip()
                date_ = re.findall("\w\d\sminute\sago|\w\d\sminutes\sago|\d\shour\sago|\w\d\shours\sago|\d\shours\sago|Jan\s+\d{1,2},\s+\d{4}|Feb\s+\d{1,2},\s+\d{4}|Mar\s+\d{1,2},\s+\d{4}|Apr\s+\d{1,2},\s+\d{4}|May\s+\d{1,2},\s+\d{4}|Jun\s+\d{1,2},\s+\d{4}|Jul\s+\d{1,2},\s+\d{4}|Aug\s+\d{1,2},\s+\d{4}|Sep\s+\d{1,2},\s+\d{4}|Oct\s+\d{1,2},\s+\d{4}|Nov\s+\d{1,2},\s+\d{4}|Dec\s+\d{1,2},\s+\d{4}", date)
                first_char = date_[0][0] # this is important for backtracking a.k.a. knowing the approximate time stamp for the articles <1 day old

                if(first_char.isdigit()):
                    parsed_s = [date_[0].split()[:2]]
                    if parsed_s[0][1] in ["hour", "minute"]:
                        parsed_s[0][1] += "s" # rare case but the new articles can be a minute or an hour old
                    time_dict = dict((fmt,float(amount)) for amount,fmt in parsed_s)
                    dt = datetime.timedelta(**time_dict)
                    past_time = datetime.datetime.now(est) - dt
                    dt_ = past_time.strftime("%Y-%m-%d %H:%M:%S-05:00")

                    nres = {
                        "headline" : headline,
                        "date" : dt_
                    }
                    collection.append(nres)
                
                else:
                    dt = datetime.datetime.strptime(date_[0], '%b %d, %Y')
                    dt_ = dt.strftime("%Y-%m-%d %H:%M:%S-05:00")
                    nres = {
                        "headline" : headline,
                        "date" : dt_
                    }
                    collection.append(nres)
                    #sleep(2)

        #print(collection)
        return collection
    
    else:
        print(f"No response on page {page}")
        return collection

# MAIN
dfx = "https://www.dailyfx.com/market-news/articles/"
fxe = "https://www.fxempire.com/indices/spx500-usd/news?page="
cnbc = "https://www.cnbc.com/sp-500/?page="
inv = "https://www.investing.com/indices/us-spx-500-news/"

fieldnames = ['headline', 'date']
srcs = [dfx, fxe, cnbc, inv]
headers = { # bypass anti-scrapers, but I probably have to start using proxies
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }
est = timezone('EST') # all news are tagged for EST
collection = [] # all news are to be put here
start_p = 1
end_p = 2


for p in range(start_p, end_p+1):
    collection.extend(get_dailyfx(p))
    collection.extend(get_fxempire(p))
    collection.extend(get_cnbc(p))
    collection.extend(get_investing(p))

timenow = datetime.datetime.now().strftime("%Y-%m-%d_%H%MH -0800")

pd.DataFrame(collection).to_csv(
    f'/opt/scr/data/news_{str(start_p)}-{str(end_p)}_{timenow}.zip', 
    index=False, 
    columns=['headline', 'date'], 
    compression='zip'
    )