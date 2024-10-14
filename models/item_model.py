from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib.parse
import time
import json
import random
import asyncio


# A simple in-memory database replacement
class ItemModel:
    def __init__(self, id: int, name: str, description: Optional[str] = None):
        self.id = id
        self.name = name
        self.description = description


# Fake in-memory database, simulating persistence
items_db: List[ItemModel] = [
    ItemModel(id=1, name="Item One", description="This is the first item."),
    ItemModel(id=2, name="Item Two", description="This is the second item."),
    ItemModel(id=3, name="Item Three", description="This is the third item."),
]


def find_item_by_id(item_id: int) -> Optional[ItemModel]:
    for item in items_db:
        if item.id == item_id:
            return item
    return None

async def news_link(name, start_year, end_year, driver):
    duration = list(range(start_year, end_year + 1))
    duration = [str(num) for num in duration]
    base_url = 'https://news.google.com/search?q='
    news = []
    for n in duration:
        hco_url = base_url + urllib.parse.quote(name + ' after:' + n + '-01-01 before:' + n + '-12-31')
        driver.get(hco_url)
        print(hco_url)
        i = 3
        try:
            while i:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                i = i - 1
        except:
            i = 0
        try:
            body = driver.find_element(By.CLASS_NAME, "D9SJMe")
            articles = body.find_elements(By.CLASS_NAME, "IFHyqb.DeXSAc")
            print(len(articles))
            if len(articles) == 0:
                print('no news')
                continue
            for article in articles:
                date_element = article.find_element(By.CLASS_NAME, 'hvbAAd')
                date = date_element.get_attribute('datetime')
                date = date[:10]
                # print(date)
                title_element = article.find_element(By.CLASS_NAME, 'JtKRv')
                title = title_element.text
                # anchor_tag = title_element.find_element(By.TAG_NAME,'a')
                link = title_element.get_attribute('href')
                # print(i)
                news.append({'title': title, 'date': date, 'link': link})
                # print(title, date)
                # print(link)
            if len(articles) == 0:
                print('no news in the timeframe given')
                continue
            else:
                print(len(news), 'found in year:', n)
                # with open(f'{name}.json', 'w') as file:
                #     json.dump(news, file, indent=2)
                print(f'news appeneded')
        except Exception as e:
            print(name, e)

        print("news__________", news)
        return news

# async def news_links(name, start_year, end_year, number_of_urls, driver):

#     duration = list(range(start_year, end_year + 1))
#     duration = [str(num) for num in duration]
#     base_url = "https://news.google.com/search?q="
#     news = []
#     for n in duration:
#         hco_url = base_url + urllib.parse.quote(
#             name + " after:" + n + "-01-01 before:" + n + "-12-31"
#         )
#         driver.get(hco_url)
#         print(hco_url)
#         i = 3
#         await asyncio.sleep(random.uniform(2, 5))  # Random delay between 2-5 seconds

#         try:
#             while i:
#                 driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 time.sleep(1)
#                 i = i - 1
#         except:
#             i = 0
#         try:
#             body = driver.find_element(By.CLASS_NAME, "D9SJMe")
#             articles = body.find_elements(By.CLASS_NAME, "IFHyqb.DeXSAc")
#             print(len(articles))
#             if len(articles) == 0:
#                 print("no news")
#                 continue
#             i = 0
#             for article in articles:
#                 date_element = article.find_element(By.CLASS_NAME, "hvbAAd")
#                 date = date_element.get_attribute("datetime")
#                 date = date[:10]
#                 # print(date)
#                 if i < number_of_urls:
#                     # if 1:
#                     title_element = article.find_element(By.CLASS_NAME, "JtKRv")
#                     title = title_element.text
#                     # anchor_tag = title_element.find_element(By.TAG_NAME,'a')
#                     link = title_element.get_attribute("href")
#                     i = i + 1
#                     # print(i)
#                     news.append({"title": title, "date": date, "link": link})
#                     # print(title, date)
#                     # print(link)
#             if i == 0:
#                 print("no news in the timeframe given")

#                 continue
#             else:
#                 print(len(news), "found in year:", n)
#                 with open(f"{name}.json", "w") as file:
#                     json.dump(news, file, indent=2)
#                 print(f"news appeneded")
#         except Exception as e:
#             print(name, e)
#             return e

#         return news


async def link_extraction(name, start_year, end_year):
    print(
        "name, start_year, end_year",
        name,
        start_year,
        end_year    )
    options = Options()
    ua = UserAgent()
    options = Options()
    options.add_argument(f"user-agent={ua.random}")  # Rotate user agent
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    options.use_chromium = True  # Necessary for Edge Chromium
    # options.add_argument("--headless")  # Optional: Run in headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")

    ser_obj = Service(
        r"C:/Users/VC899BC/OneDrive - EY/Documents/EYProjects/Fastapi/driver/msedgedriver.exe"
    )
    driver = webdriver.Edge(service=ser_obj, options=options)
    news = await news_link(name, start_year, end_year, driver)
    print("len(news)", news)

    for n in range(0, len(news[:3])):
        driver.get(news[n]["link"])
        time.sleep(4)
        # title = driver.title
        # print(f"Title: {title}")
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        text_content = " ".join(soup.stripped_strings)
        print("text_content", text_content)
        news[n]["full_article"] = text_content
        # filename = f"Vladimir Putin{n}_Text.txt"
        # with open(f'articles/{filename}', 'w', encoding='utf-8') as f:
        #     f.write(text_content)
        #     print(f"Extracted text saved for URL: {n}")
    return news
