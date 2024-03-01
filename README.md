<!-- STEP CRAWL DATA FROM  https://www.coupang.com/-->

STEP 1: Add keywords in file: /keywords/keyword.txt
STEP 2: Install package:
pip install -r requirements.txt
STEP 3: Crawl data export to csv file: /data/crawl.csv
py crawl.py
STEP 4: From file csv download image save in folder:
py download_image.py
