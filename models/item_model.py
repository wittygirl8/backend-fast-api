from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from openai import AzureOpenAI
import re
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




# OpenAI 
client = AzureOpenAI(
    azure_endpoint="https://swcdoai2x2aoa01.openai.azure.com/",
    api_key="cb4b1a0311454198ad4c9c42e9c4e5d7",
    api_version="2024-07-01-preview"
)

def remove_first_and_last_two_sentences(paragraph):
    print("sentences1_____")
    sentences = re.split(r'(?<=[.!?]) +', paragraph)
    print("sentences2_____")
    if len(sentences) <= 4:
        return ""
    print("sentences3_____")
    value = ' '.join(sentences[2:-2])
    print("value___________________", value)
    return value

async def summarize_text(text, person):
    summary = None
    message_text = [
        {"role": "system", "content": "You are an AI assistant that summarizes"},
        {"role": "user",
         "content": f"Summarize the text in english language within 30 words strictly (without deviation from topic) and highlight {person} contribution in it. Output should only the summary. The input text is {text}"}
    ]
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=message_text
        )
        summary = completion.choices[0].message.content.strip()
        return summary
    except Exception as e:
        if summary:
            reason = 'XYZ' + completion.choices[0].message.finish_reason
            print(reason)
        else:
            print(f"Error in summarizing text: {e}")
            reason = 'XYZ' + str(e)
        return reason


async def related_to_person(person, text):
    summary = None
    message_text = [
        {"role": "system", "content": "You are an AI assistant that identifies"},
        {"role": "user",
         "content": f"Do the following text has a mention of {person}?(ignore profession,designation and qualification like dr,m.d,prof,phd and such). If its true, output is: Y. If it is false, output is 'N'. No other output. The input text is {text}"}
    ]
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=message_text
        )
        summary = completion.choices[0].message.content.strip()
        return str(summary)
    except Exception as e:
        if summary:
            reason = 'XYZ' + completion.choices[0].message.finish_reason
            print(reason)
        else:
            print(f"Error in relating to hcp text: {e}")
            reason = 'XYZ' + str(e)
        return str(reason)


async def related_to_domain(domain, text):
    summary = None
    message_text = [
        {"role": "system", "content": "You are an AI assistant that identifies."},
        {"role": "user",
         "content": f"For the following text, verify weather it is related to {domain}. If its true, output is: Y. If it is false, output is 'N'. No other output. The input text is {text}"}
    ]
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=message_text
        )
        summary = completion.choices[0].message.content.strip()
        return summary
    except Exception as e:
        if summary:
            reason = 'XYZ' + completion.choices[0].message.finish_reason
            print(reason)
        else:
            print(f"Error in detecting healthcare related news text: {e}")
            reason = 'XYZ' + str(e)
        return str(reason)


async def sentiment(text):
    summary = None
    message_text = [
        {"role": "system", "content": "You are an AI assistant that categorizes."},
        {"role": "user",
         "content": f"For the provided text, categorize the sentiment as either 'positive' or 'negative'. If it doesn't fit into either of these, categorize it as 'neutral'. The output should be one of these three categories. The input text is {text}"}
    ]
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=message_text
        )
        summary = completion.choices[0].message.content.strip()
        return summary
    except Exception as e:
        if summary:
            reason = 'XYZ' + completion.choices[0].message.finish_reason
            print(reason)
        else:
            print(f"Error in emotion: {e}")
            reason = 'XYZ' + str(e)
        return reason

   
async def keyword(text):
    summary = None
    message_text = [
        {"role": "system", "content": "You are an AI assistant that identifies."},
        {"role": "user",
         "content": f"For the provided text of news, generate a list of relevant categorical keywords. The first value in the list should represent the major categorical keyword, followed by other relevant keywords. The input text is {text}"}
    ]
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=message_text
        )
        summary = completion.choices[0].message.content.strip()
        return summary
    except Exception as e:
        if summary:
            reason = 'XYZ' + completion.choices[0].message.finish_reason
            print(reason)
        else:
            print(f"Error in detecting healthcare related news text: {e}")
            reason = 'XYZ' + str(e)
        return reason


# async def news_link(name, start_year, end_year, domain, driver):
#     duration = list(range(start_year, end_year + 1))
#     duration = [str(num) for num in duration]
#     base_url = 'https://news.google.com/search?q='
#     news = []
#     for n in duration:
#         hco_url = base_url + urllib.parse.quote(name + '  info after:' + n + '-01-01 before:' + n + '-12-31')
#         driver.get(hco_url)
#         print(hco_url)
#         # Accept cookies if prompted
#         # try:
#         #     accept_cookies_button = driver.find_element(By.XPATH, "//button[contains(text(),'Accept')]")
#         #     if accept_cookies_button:
#         #         accept_cookies_button.click()
#         #         print("Accepted cookies.")
#         # except:
#         #     print("No cookies popup found.")

#         # await asyncio.sleep(random.uniform(2, 5))  # Random delay between 2-5 seconds
#         # Scroll the page to load more news articles
#         scroll_attempts = 3
#         while scroll_attempts:
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             await asyncio.sleep(random.uniform(1, 3))  # Random delay between scrolls
#             scroll_attempts -= 1

#         try:
#             # Wait for the articles section to load
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "D9SJMe"))
#             )
#         # try:
#         #     while i:
#         #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         #         time.sleep(1)
#         #         i = i - 1
#         # except:
#         #     i = 0
#         # try:
#             body = driver.find_element(By.CLASS_NAME, "D9SJMe")
#             articles = body.find_elements(By.CLASS_NAME, "IFHyqb.DeXSAc")
#             print(len(articles))
#             if len(articles) == 0:
#                 print('no news')
#                 continue
#             for article in articles:
#                 date_element = article.find_element(By.CLASS_NAME, 'hvbAAd')
#                 date = date_element.get_attribute('datetime')
#                 date = date[:10]
#                 # print(date)
#                 title_element = article.find_element(By.CLASS_NAME, 'JtKRv')
#                 title = title_element.text
#                 # anchor_tag = title_element.find_element(By.TAG_NAME,'a')
#                 link = title_element.get_attribute('href')
#                 # print(i)
#                 news.append({'title': title, 'date': date, 'link': link})
#                 # print(title, date)
#                 # print(link)
#             if len(articles) == 0:
#                 print('no news in the timeframe given')
#                 continue
#             else:
#                 print(len(news), 'found in year:', n)
#                 # with open(f'{name}.json', 'w') as file:
#                 #     json.dump(news, file, indent=2)
#                 print(f'news appeneded')
#         except Exception as e:
#             print(name, e)

#         # print("news__________", news)
#         return news

async def news_link(name, start_year, end_year, domain, driver):

    duration = list(range(start_year, end_year + 1))
    duration = [str(num) for num in duration]
    base_url = "https://news.google.com/search?q="
    news = []
    for n in duration:
        hco_url = base_url + urllib.parse.quote(
            name + " after:" + n + "-01-01 before:" + n + "-12-31"
        )
        driver.get(hco_url)
        print(hco_url)
        i = 3
        await asyncio.sleep(random.uniform(2, 5))  # Random delay between 2-5 seconds

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
                print("no news")
                continue
            i = 0
            for article in articles:
                date_element = article.find_element(By.CLASS_NAME, "hvbAAd")
                date = date_element.get_attribute("datetime")
                date = date[:10]
                # print(date)
                #if i < number_of_urls:
                # if 1:
                title_element = article.find_element(By.CLASS_NAME, "JtKRv")
                title = title_element.text
                # anchor_tag = title_element.find_element(By.TAG_NAME,'a')
                link = title_element.get_attribute("href")
                i = i + 1
                # print(i)
                news.append({"title": title, "date": date, "link": link})
                # print(title, date)
                # print(link)
            if i == 0:
                print("no news in the timeframe given")

                continue
            else:
                print(len(news), "found in year:", n)
                with open(f"{name}.json", "w") as file:
                    json.dump(news, file, indent=2)
                print(f"news appeneded")
        except Exception as e:
            print(name, e)
            return e

        return news

async def get_article_sentiments(news, name, domain, driver):
    final_news = []
    count = 0
    for n in range(0, len(news[:15])):
        driver.get(news[n]["link"])
        time.sleep(4)
        # Remove accept cookies
        try:
            accept_cookies_button = driver.find_element(By.XPATH, "//button[contains(text(),'Accept')]")
            if accept_cookies_button:
                accept_cookies_button.click()
        except:
            print("No cookies popup found.")

        await asyncio.sleep(random.uniform(2, 5))  # Random delay between requests
        # title = driver.title
        # print(f"Title: {title}")
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        text_content = " ".join(soup.stripped_strings)
        # print("text_content", text_content)
        news[n]["full_article"] = text_content
        article = remove_first_and_last_two_sentences(text_content)
        print("article", article)
        words = str(article).split()
        restricted_words = words[:100]
        article = ' '.join(restricted_words)
        # print(article)
        ans = await related_to_person(name, article)
        print("related_to_person____________", ans, n)
        if "Y" in ans:
            count += 1
            rtd = await related_to_domain(domain, article)
            print("related_to_domain____________", ans, n)
            print(ans, n)
            # if "Y" in ans:
            summary = await summarize_text(article, name)
            print(n, summary)
            senti = await sentiment(article)
            print("senti", senti)
            key = await keyword(article)
            print("keywords", keyword)
            final_news.append(
                    {
                        'title': news[n]['title'], 
                        'date': news[n]['date'], 
                        'link': news[n]['link'], 
                        'full_article': text_content,
                        'summary': summary,
                        'sentiment': senti,
                        'Keywords': key, 
                        'domain' : True if "Y" in rtd else False 
                    })
            # news[n]["summary"] = summary
            # news[n]["sentiment"] = senti
            # news[n]["Keyword"] = key
            # news[n]["domain"] = True if "Y" in rtd else False
        else:
            continue
        if count == 3:
            break
    return final_news 


async def link_extraction(name, start_year, end_year, domain):
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
    news = await news_link(name, start_year, end_year, domain, driver)
    # print("len(news)", news)
    count = 0
    count = 0
    while not news and count < 5:
        count += 1
        print(f"Retrying... attempt {count}")
        # time.sleep(2)  # Wait before retrying
        news = await news_link(name, start_year, end_year, domain, driver)

    if not news:
        return {"status": 404, "message": "No News Found"}

    # Process and analyze news articles if found
    news = await get_article_sentiments(news, name, domain, driver)
    
    driver.quit()  # Close the browser once done
    return return {"status": 200, "data": news}
