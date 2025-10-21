# src/fetch_news.py
from GoogleNews import GoogleNews
import requests
from bs4 import BeautifulSoup

def fetch_google_news(query: str, pages: int = 3):
    """Fetch news from GoogleNews library"""
    googlenews = GoogleNews(lang='en', region='IN')
    googlenews.search(f"{query} stock")
    
    all_articles = []
    for page in range(1, pages+1):
        googlenews.getpage(page)
        results = googlenews.result()
        for r in results:
            all_articles.append({
                "title": r.get("title"),
                "url": r.get("link"),
                "source": "GoogleNews"
            })
    return all_articles

def fetch_yahoo_finance_news(ticker: str):
    """Fetch stock news from Yahoo Finance"""
    url = f"https://finance.yahoo.com/quote/{ticker}/news?p={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    
    articles = []
    for item in soup.find_all('li', {'class': 'js-stream-content'}):
        a_tag = item.find('a')
        if a_tag and a_tag.get('href'):
            link = a_tag['href']
            if link.startswith('/'):
                link = 'https://finance.yahoo.com' + link
            title = a_tag.text.strip()
            articles.append({"title": title, "url": link, "source": "YahooFinance"})
    return articles

def fetch_newsdataio_news(query: str, api_key: str):
    """Fetch news from NewsData.io API (optional, free tier 200 requests/day)"""
    url = f"https://newsdata.io/api/1/news?q={query}&category=business&language=en&apikey={api_key}"
    res = requests.get(url).json()
    articles = []
    for a in res.get("results", []):
        articles.append({"title": a["title"], "url": a["link"], "source": "NewsData.io"})
    return articles

def deduplicate_articles(articles: list):
    """Deduplicate articles by URL or title"""
    seen_urls = set()
    deduped = []
    for a in articles:
        if a['url'] not in seen_urls:
            deduped.append(a)
            seen_urls.add(a['url'])
    return deduped

def get_stock_news(query: str, ticker: str = None, api_key: str = None, pages: int = 3):
    """Fetch combined stock news from multiple sources"""
    articles = []
    
    # Google News
    articles.extend(fetch_google_news(query, pages))
    
    # Yahoo Finance
    if ticker:
        articles.extend(fetch_yahoo_finance_news(ticker))
    
    # NewsData.io (optional)
    if api_key:
        articles.extend(fetch_newsdataio_news(query, api_key))
    
    # Deduplicate
    articles = deduplicate_articles(articles)
    
    return articles

# --------------------------
# Example usage
if __name__ == "__main__":
    news = get_stock_news("Reliance Industries", ticker="RELIANCE")
    for n in news:
        print(f"- {n['title']}\n  {n['url']}\n  Source: {n['source']}\n")
