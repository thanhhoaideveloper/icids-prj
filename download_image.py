import os
import pandas as pd
import requests
import ast

def download_image(url, folder_path, headers):
    filename = os.path.join(folder_path, url.split('/')[-1])
    response = requests.get(url, headers)
    with open(filename, 'wb') as f:
        f.write(response.content)

def main():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    # Read the CSV file
    df = pd.read_csv('data/craw.csv')

    # Iterate over each row
    for index, row in df.iterrows():
        images = ast.literal_eval(row['image_url'])
        product_name = row['product_name']

        # Create directory if not exists
        folder_path = os.path.join('data/datasets', product_name)
        os.makedirs(folder_path, exist_ok=True)
        for image in images:
            if(image is not None):
                print(f"Download {image}...")
                # Download the image
                download_image(image, folder_path, headers)
            

if __name__ == "__main__":
    main()