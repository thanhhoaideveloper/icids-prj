from utils import get_keywords,fetch_url_detail, save_csv, process_coupang_images, convert_keyword_to_querystring, init_header_request, get_links, download_image
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def crawl_tool(type="keyword"):
    try:
        data = []
        driver = webdriver.Chrome()
        headers = init_header_request()
        print("Starting...")
        if type == "keyword":
            keywords = get_keywords()
            for keyword in keywords:
                query_keyword = convert_keyword_to_querystring(keyword)
                url = f"https://www.coupang.com/np/search?component=&q={query_keyword}&channel=user&listSize=72"
                soup = fetch_url_detail(url, headers)
                # Tìm tất cả các thẻ <a> có class là "search-product-link"
                search_product_links = soup.find_all("a", class_="search-product-link")
                # Lấy 5 href từ các thẻ <a> đã tìm được
                for i, link in enumerate(search_product_links[:15], 1):
                    href = "https://www.coupang.com" + link.get("href")
                    image_url = process_coupang_images(href, headers, driver)
                    data.append({
                        "link": href,
                        "product_name": keyword,
                        "image_url": image_url
                    })
            save_csv(data)
        else:
            links = get_links()
            for link in links:
                image_url = process_coupang_images(href, headers, driver)
                time.sleep(10)
                print("Waiting for image...")
                download_image(source="link_detail", images_url=image_url)

        driver.quit()

    except Exception as e:
        print(str(e))
    finally:
        print("Crawl data successfully")

if __name__ == "__main__":
    crawl_tool()
else:
    crawl_tool(type)



