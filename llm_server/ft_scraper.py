from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import load_config_file

config = load_config_file()


def get_articles(search_term: str) -> list[str]:
    """
    Search for articles on ft.com given the search_term and
    scrape the content of the returned articles using archive.is
    """

    html: str = requests.get("https://www.ft.com/search", params={"q": search_term}).text
    articles: list[str] = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("user-agent=Chrome/37.0.2049.0")

    with webdriver.Chrome(options=chrome_options) as driver:
        wait = WebDriverWait(driver, 3)
        num_articles = int(config['scraper']['num_articles'])

        for img_container in BeautifulSoup(html, "html.parser").find_all("div", "o-teaser__image-container")[:num_articles]:
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
