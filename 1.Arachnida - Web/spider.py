import requests
from bs4 import BeautifulSoup
import shutil
import os
import sys
import argparse
import traceback
from urllib.parse import urljoin
from colorama import init, Fore, Back, Style

init(autoreset=True)

number_of_images = 0
already_downloaded = []
MAX_LEVEL = 15

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

def get_base_url(url):
    segments = url.split('/')
    if len(segments) > 3:
        return '/'.join(segments[:3]) + '/'
    return url

def check_extension(image_url, image_response, path):
    global number_of_images
    extension = image_url.split('.')[-1]
    valid_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp', 'ico', 'tiff']
    if extension in valid_extensions:
        image_response.raise_for_status()
        with open(f'{path}image_{number_of_images}.{extension}', 'wb') as out_file:
            shutil.copyfileobj(image_response.raw, out_file)
        number_of_images += 1
    else:
        print(f"{Back.RED}Extension non supportée: {extension}")

def handle_image_on_page(image_urls, base_url, path):
    global already_downloaded
    global number_of_images
    for i, image_url in enumerate(image_urls):
        
        if not image_url.startswith(('http://', 'https://')):
            image_url = urljoin(base_url, image_url)
        
        image_response = requests.get(image_url, headers=headers, stream=True)

        if image_url in already_downloaded:
            print(f"{Fore.RED} Image {number_of_images+1} déjà téléchargée.")
            continue
        else:
            try:
                check_extension(image_url, image_response, path)
                already_downloaded.append(image_url)
            except Exception as e:
                print(f"{Back.RED} Erreur lors du téléchargement de l'image {i+1}. {e}, try with other method {Back.RESET}\n")
                try:
                    if not image_url.startswith(('http://', 'https://')):
                        save_url = urljoin("https:", image_url)
                    image_response = requests.get(save_url, headers=headers, stream=True)
                    check_extension(save_url, image_response, path)
                    already_downloaded.append(save_url)
                    continue
                except Exception as e:
                    print(f"{Back.RED} Erreur lors du téléchargement de l'image {i+1} avec https. {e}, try with http {Back.RESET}\n")
                    try:
                        if not image_url.startswith(('http://', 'https://')):
                            save_url = urljoin("http:", image_url)
                        image_response = requests.get(save_url, headers=headers, stream=True)
                        check_extension(save_url, image_response, path)
                        already_downloaded.append(save_url)
                        continue
                    except Exception as e:
                        print(f"{Back.RED} Erreur lors du téléchargement de l'image {i+1} avec http. {e} {Back.RESET}\n")
                        continue
        print(f"{Fore.GREEN} Image {number_of_images+1} téléchargée avec succès.")

def download_images(url, r, level, path, visited_urls):
    if level is not None and level == 0 or url in visited_urls:
        return
    print(f"{Fore.YELLOW}\n\nSur le level: {level}")
    print(f"{Fore.BLUE}Url: {url}")
    visited_urls.add(url)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erreur lors de la requête. {response} -> {url}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    attributes = ['src', 'data-src', 'content', 'href']

    image_urls = []
    recursive_urls = []
    base_url = get_base_url(url)
    tags = soup.find_all(['img', 'link', 'meta', 'a'])
    for tag in tags:
        for attr in attributes:
            if attr in tag.attrs and any(tag[attr].endswith(ext) for ext in extensions):
                image_urls.append(tag[attr])
            elif attr in tag.attrs and tag.name == 'a':
                recursive_urls.append(urljoin(base_url, tag[attr]))

    handle_image_on_page(image_urls, base_url, path)
    if r:
        for recursive_url in recursive_urls:
            if recursive_url is url or not recursive_url.startswith(base_url):
                continue
            else:
                print(f"{Fore.YELLOW}   - Chemin : {recursive_url}......")
                download_images(recursive_url, r, None if level is None else level - 1, path, visited_urls)
    

def main():
    url = None
    for arg in sys.argv[1:]:
        if arg.startswith(('http://', 'https://')):
            url = arg
            break

    if url is None:
        print("URL is required. Please provide a valid URL , e.g. \"python spider.py https://example.com -h\" for help.")
        exit()

    args_without_url = [arg for arg in sys.argv[1:] if arg != url]

    parser = argparse.ArgumentParser(prog="Arachnida - Web Spider 🕷️",description="Web spider script for downloading images from websites 🌐",epilog="Developed by: https://github.com/fZpHr/ 👨‍💻")
    parser.add_argument("--recursive", "-r", action="store_true", help="Recursively download images 🔄")
    parser.add_argument("--level", "-l", nargs='?', const=5, type=int, help="Maximum depth level for recursive download (default: 5) 📏")
    parser.add_argument("--path", "-p", type=str, default='./data/', help="Path where downloaded files will be saved 🗂️")
    args = parser.parse_args(args_without_url)

    if (args.level is not None):
        if args.level > MAX_LEVEL or args.level <= 0:
            print(f"{Back.RED}Level must be between 1 and {MAX_LEVEL}.")
            exit()

    print(f"{Fore.YELLOW}Downloading images from {url}, level: {args.level if args.level is not None else '∞'}, recursive: {args.recursive}, path: {args.path}")
    if os.path.exists(args.path):
        if os.path.isfile(args.path):
            print(f"{Back.RED}A file with the same name as the desired directory already exists: {args.path}{Back.RESET}")
            exit()
        elif not os.access(args.path, os.W_OK):
            print(f"{Back.RED}No write access to the path: {args.path}{Back.RESET}")
            exit()
    else:
        try:
            os.makedirs(args.path)
        except Exception as e:
            print(f"{Back.RED}Unable to create directory {args.path}: {e}{Back.RESET}")
            exit()
    if not args.path.endswith("/"):
        args.path += "/"
    download_images(url, args.recursive, args.level, args.path, set())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Back.RED}An error occurred: {e}, traceback below:")
        print(f"{Fore.RED}\t" + traceback.format_exc().replace("\n", f"\n\t{Fore.RED}"))