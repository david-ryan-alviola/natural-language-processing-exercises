import env
import pandas as pd
import requests as req
import bs4

_headers = {'User-Agent' :\
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
_blog_pages = ["https://codeup.com/codeups-data-science-career-accelerator-is-here/", "https://codeup.com/data-science-myths/", "https://codeup.com/data-science-vs-data-analytics-whats-the-difference/", "https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/", "https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/"]

def extract_page_information(soup):
    title = soup.select(".jupiterx-post-title")[0]
    content = soup.select(".jupiterx-post-content")[0]
    
    return {'title' : title.text, 'content' : content.text}

def scrape_webpage(url):
    response = req.get(url, headers=_headers)
    html = response.text

    soup = bs4.BeautifulSoup(html)
    
    return extract_page_information(soup)

def acquire_codeup_blog_data():
    return pd.DataFrame([scrape_webpage(page) for page in _blog_pages])

def extract_article_info(card):
    title = card.find("span", attrs={'itemprop' : "headline"})
    content = card.find("div", attrs={'itemprop' : "articleBody"})
    author = card.select(".author")[0]
    time = card.select(".time")[0]
    
    return {'title' : title.text, 'content' : content.text, 'author' : author.text, 'timestamp' : time['content']}

def acquire_inshort_data():
    response = req.get("https://inshorts.com/en/read")
    html = response.text

    news_soup = bs4.BeautifulSoup(html)
    
    card_stack = news_soup.select(".card-stack")[0]
    cards = card_stack.select(".news-card")
    
    return pd.DataFrame([extract_article_info(card) for card in cards])