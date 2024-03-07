import os
import pandas as pd
import requests
import ast
from utils import init_header_request

def download_image(url, folder_path, headers):
    filename = os.path.join(folder_path, url.split('/')[-1])
    response = requests.get(url, headers)
    with open(filename, 'wb') as f:
        f.write(response.content)

def main():
    headers = init_header_request()
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