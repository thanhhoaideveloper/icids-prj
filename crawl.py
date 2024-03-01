from utils import get_keywords, fetch_url_content, save_csv, process_coupang_images, convert_keyword_to_querystring, init_browser
import requests
from bs4 import BeautifulSoup
import time

keywords = get_keywords()
headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

try:
    data = []
    print("Starting...")
    driver = init_browser()
    for keyword in keywords:
        query_keyword = convert_keyword_to_querystring(keyword)
        url = f"https://www.coupang.com/np/search?component=&q={query_keyword}&channel=user&listSize=72"
        soup = fetch_url_content(url, headers)
        # Tìm tất cả các thẻ <a> có class là "search-product-link"
        search_product_links = soup.find_all("a", class_="search-product-link")
        # Lấy 5 href từ các thẻ <a> đã tìm được
        for i, link in enumerate(search_product_links[:20], 1):
            href = "https://www.coupang.com" + link.get("href")
            image_url = process_coupang_images(href, headers, driver)
            data.append({
                "link": href,
                "product_name": keyword,
                "image_url": image_url
            })
            
    save_csv(data)

except Exception as e:
    print(str(e))
finally:
    print("Finally!")



