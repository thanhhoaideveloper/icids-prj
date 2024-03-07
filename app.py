from utils import format_image_name, get_links, init_header_request
import argparse
from crawl import crawl_tool
from download_image import download_image

def main():
    parser = argparse.ArgumentParser(description='Rename or crawl files in a folder.')
    parser.add_argument('--folder_path', type=str, help='Path to the folder containing files')
    parser.add_argument('--rename', action='store_true', help='Rename files')
    parser.add_argument('--crawl', action='store_true', help='Crawl files')
    parser.add_argument('--link_detail_download', action='store_true', help='Crawl files links detalt')
    args = parser.parse_args()


    if args.rename:
        format_image_name(args.folder_path)
    elif args.crawl:
        crawl_tool()
    elif args.link_detail_download:
        crawl_tool("link_detail")
    else:
        print("Please specify either --rename")

if __name__ == '__main__':
    main()