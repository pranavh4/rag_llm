from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_articles(search_term: str) -> list[str]:
    html: str = requests.get("https://www.ft.com/search", params={"q": search_term}).text
    articles: list[str] = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')

    with webdriver.Chrome(options=chrome_options) as driver:
        wait = WebDriverWait(driver, 3)

        for img_container in BeautifulSoup(html, "html.parser").find_all("div", "o-teaser__image-container")[:5]:
            try:
                driver.get(f"https://archive.is/https://www.ft.com{img_container.a['href']}")
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "head")))
                elem = ((driver.find_element(By.CLASS_NAME, "THUMBS-BLOCK")
                         .find_element(By.TAG_NAME, "div"))
                        .find_element(By.TAG_NAME, "a"))
                elem.click()
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "head")))
                article_text = driver.find_element(By.ID, "article-body").text
                articles.append(article_text)
            except (KeyError, NoSuchElementException):
                pass

    return articles
