from utils import format_image_name
import argparse

def main():
    parser = argparse.ArgumentParser(description='Rename or crawl files in a folder.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing files')
    parser.add_argument('--rename', action='store_true', help='Rename files')
    parser.add_argument('--crawl', action='store_true', help='Crawl files')
    args = parser.parse_args()
    if args.rename:
        format_image_name(args.folder_path)
    else:
        print("Please specify either --rename")

if __name__ == '__main__':
    main()