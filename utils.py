import csv
import requests
from bs4 import BeautifulSoup
import re
import os
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import requests
import ast


def get_keywords():
    file_path = "dataSource/keyword.txt"
    keywords = []
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file.readlines():
            keywords.append(line.strip())
            
    file.close()
    return keywords

def save_link_details(hrefs_by_keyword):
    save_path = "data/linkDetail"
    for keyword, hrefs in hrefs_by_keyword.items():
        with open(f"{save_path}/{keyword}.txt", "w") as file:
            file.write("\n".join(hrefs))


def save_csv(data):
    csv_file = "data/craw.csv"
    headers = ["link", "product_name", "image_url"]
    print("Writing File...")
    with open(csv_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    print("Writed CSV")

def fetch_url_detail(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Error:{str(e)}")

def fetch_img_content(url, headers, driver):
    print(f"Crawl url {url}")
    # Open the webpage
    driver.get(url)

    # Wait for the dynamic content to load or for interactions
    time.sleep(5)

    # Now you can access the page source
    html = driver.page_source

    # Close the browser
    time.sleep(5)
    return BeautifulSoup(html, 'html.parser')


def process_coupang_images(url, headers, driver):
    """
    Processes Coupang images from the given URL.
    Args:
        url (str): The URL of the Coupang page.
        headers (dict): Headers for the request.

    Returns:
        list: List of processed image URLs.
    """
    try:
        soup = fetch_img_content(url, headers, driver)
        image_urls = extract_coupang_image_urls(soup)
        return [convert_to_coupang_image_url(url) for url in image_urls]
    except Exception as e:
        return []
    

def extract_coupang_image_urls(soup):
    """
    Extracts image URLs from Coupang page's BeautifulSoup object.
    Args:
        soup (BeautifulSoup): Parsed HTML content of the Coupang page.

    Returns:
        list: List of extracted image URLs.
    """
    try:
        divs_primary = soup.find_all('div', class_='prod-image__item')
        divs_content = soup.find_all('div', class_='subType-IMAGE')
        image_urls = []
        #Get imaage primary
        image_urls += [img['data-src'] for div in divs_primary for img in div.find_all('img') if 'data-src' in img.attrs]
        #Get image content
        image_urls += [img['src'] for div in divs_content for img in div.find_all('img') if 'src' in img.attrs]
        return image_urls
    except Exception as e:
        print(str(e))

def convert_to_coupang_image_url(url):
    match = re.search(r'/(vendor_inventory|retail|rs_quotation_api)/(.+\.(jpg|png))', url)
    if match:
        return f"https://image10.coupangcdn.com/image/{match.group(1)}/{match.group(2)}"

def convert_keyword_to_querystring(keyword):
    if " " in keyword:
        return keyword.replace(" ", "+")
    return keyword

def get_image_content(soup):
    divs = soup.find_all("div", id="productDetail")
    for div in divs:
        # Find all img elements within the div
        imgs = div.find_all("img")
        # Iterate over each img element and get the src attribute
        for img in imgs:
            src = img.get("src")
            print(src)

def format_image_name(folder_path):
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print("Starting rename file...")
    for index, file_name in enumerate(image_files):
        # Get the file extension
        file_extension = os.path.splitext(file_name)[1]
        # Generate the new file name (e.g., 0.jpg, 1.jpg, 2.jpg, ...)
        new_file_name = f"{index}{file_extension}"
        # Get the full path of the input and output files
        input_file_path = os.path.join(folder_path, file_name)
        output_file_path = os.path.join(folder_path, new_file_name)
        # Rename the file
        os.rename(input_file_path, output_file_path)

    print("Rename successfully!")

def get_links():
    file_path = "dataSource/link_detail.txt"
    links = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            links.append(line.strip())
            
    file.close()
    return links

def init_header_request():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

def download_image(, images_url=[]):
    headers = init_header_request()
    if source == "csv":
        # Read the CSV file
        df = pd.read_csv('data/craw.csv')
        # Iterate over each row
        for index, row in df.iterrows():
            images = ast.literal_eval(row['image_url'])
            product_name = row['product_name']

            # Create directory if not exists
            folder_path = os.path.join('data/datasets', product_name)
            os.makedirs(folder_path, exist_ok=True)
            for url in images:
                if(url is not None):
                    download_image(url, folder_path, headers)
    else:
        # Create directory if not exists
        folder_path = os.path.join('data/datasets', 'image_from_link')
        os.makedirs(folder_path, exist_ok=True)
        for url in images_url:
            download_image(url, folder_path, headers)


def download_image_from_url(url, folder_path, headers):
    print(f"Download {url}...")
    # Download the image
    filename = os.path.join(folder_path, url.split('/')[-1])
    response = requests.get(url, headers)
    with open(filename, 'wb') as f:
        f.write(response.content)