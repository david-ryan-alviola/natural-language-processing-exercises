import env
import pandas as pd
import requests as req
import bs4

_headers = {'User-Agent' :\
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

_blog_pages = ["https://codeup.com/codeups-data-science-career-accelerator-is-here/", "https://codeup.com/data-science-myths/", "https://codeup.com/data-science-vs-data-analytics-whats-the-difference/", "https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/", "https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/"]

_categories = ["national", "business", "sports", "world", "politics", "technology", "startup", "entertainment", "miscellaneous", \
             "hatke", "science", "automobile"]

def extract_page_information(soup):
    """
    Extracts the title and content from the soup object generated from the Codeup blog page.\
    Returns a dictionary with the title and page content.
    """
    title = soup.select(".jupiterx-post-title")[0]
    content = soup.select(".jupiterx-post-content")[0]
    
    return {'title' : title.text, 'content' : content.text}

def scrape_webpage(url):
    """
    Scrapes the given webpage for information. Returns a dictionary with the title and page content.
    """
    response = req.get(url, headers=_headers)
    html = response.text

    soup = bs4.BeautifulSoup(html)
    
    return extract_page_information(soup)

def acquire_codeup_blog_data():
    """
    Loops through the Codeup blog pages and generates a dataframe with each page's title and content.
    """
    return pd.DataFrame([scrape_webpage(page) for page in _blog_pages])

def extract_article_info(card, category):
    """
    Extracts the title, content, author, and timestamp for the card. Returns a dictionary containing the extracted information.
    """
    title = card.find("span", attrs={'itemprop' : "headline"})
    content = card.find("div", attrs={'itemprop' : "articleBody"})
    author = card.select(".author")[0]
    time = card.select(".time")[0]
    
    return {'title' : title.text, 'category' : category, 'content' : content.text, 'author' : author.text, 'timestamp' : time['content']}

def acquire_inshort_data():
    """
    Generates a dataframe containing the title, content, author, and timestamp\
    from each article featured on the All News section of inshorts.com.
    """
    news_df = pd.DataFrame()
    base_url = "https://inshorts.com/en/read/"

    for category in _categories:
        response = req.get(base_url + category)

        html = response.text
        news_soup = bs4.BeautifulSoup(html)

        card_stack = news_soup.select(".card-stack")[0]
        cards = card_stack.select(".news-card")

        page_df = pd.DataFrame([extract_article_info(card, category) for card in cards])
        news_df = pd.concat([news_df, page_df], axis=0)
    
    return news_df