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

def check_extension(image_url, image_response, i, path):
    extension = image_url.split('.')[-1]
    valid_extensions = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp', 'ico', 'tiff']
    if extension in valid_extensions:
        image_response.raise_for_status()
        with open(f'{path}image_{i+1}.{extension}', 'wb') as out_file:
            shutil.copyfileobj(image_response.raw, out_file)
    else:
        print(f"Extension non supportée: {extension}")

def download_images(url, recursive, level, path):
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
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erreur lors de la requête. {response} -> {url}")
        exit()

    soup = BeautifulSoup(response.content, 'html.parser')
    extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    attributes = ['src', 'data-src', 'content', 'href']

    image_urls = []
    already_downloaded = []

    base_url = get_base_url(url)
    print(f"Base URL: {base_url}")
    
    tags = soup.find_all(['img', 'link', 'meta', 'a'])
    for tag in tags:
        for attr in attributes:
            if attr in tag.attrs and any(tag[attr].endswith(ext) for ext in extensions):
                image_urls.append(tag[attr])
                break    
    for i, image_url in enumerate(image_urls):
        if recursive and i == level:
            break
        print(f"before - > {image_url}")
        
        if not image_url.startswith(('http://', 'https://')):
            image_url = urljoin(base_url, image_url)
        
        print(f"after - > {image_url}")
        image_response = requests.get(image_url, headers=headers, stream=True)

        if image_url in already_downloaded:
            print(f"Image {i+1} déjà téléchargée.")
            continue
        else:
            try:
                check_extension(image_url, image_response, i, path)
                already_downloaded.append(image_url)
            except Exception as e:
                print(f"{Back.RED} Erreur lors du téléchargement de l'image {i+1}. {e}, try with other method {Back.RESET}\n")
                try:
                    if not save_url.startswith(('http://', 'https://')):
                        save_url = urljoin("https:", image_url)
                    print(f"after second method- > {save_url}")
                    image_response = requests.get(save_url, headers=headers, stream=True)
                    check_extension(save_url, image_response, i, path)
                    already_downloaded.append(save_url)
                    continue
                except Exception as e:
                    print(f"{Back.RED} Erreur lors du téléchargement de l'image {i+1} avec https. {e}, try with http {Back.RESET}\n")
                    try:
                        if not save_url.startswith(('http://', 'https://')):
                            save_url = urljoin("http:", image_url)
                        print(f"after third method- > {save_url}")
                        image_response = requests.get(save_url, headers=headers, stream=True)
                        check_extension(save_url, image_response, i, path)
                        already_downloaded.append(save_url)
                        continue
                    except Exception as e:
                        print(f"{Back.RED} Erreur lors du téléchargement de l'image {i+1} avec http. {e} {Back.RESET}\n")
                        continue
        print(f"Image {i+1} téléchargée avec succès.\n\n")

def get_base_url(url):
    segments = url.split('/')
    if len(segments) > 3:
        return '/'.join(segments[:3]) + '/'
    return url

def main():
    parser = argparse.ArgumentParser(description='Spider script for downloading images.')

    parser.add_argument('-r', action='store_true', help='Recursively download images')
    parser.add_argument('-l', type=int, default=5, help='Maximum depth level for recursive download')
    parser.add_argument('-p', type=str, default='./data/', help='Path where downloaded files will be saved')
    parser.add_argument('url', type=str, help='The URL to download images from')

    args = parser.parse_args()

    if not args.url.startswith(('http://', 'https://')):
        print("Bad URL format. Please provide a valid URL.")
        exit()
    if not os.path.exists(args.p):
        os.makedirs(args.p)
        
    download_images(args.url, args.r, args.l, args.p)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Back.RED}An error occurred: {e}, traceback below:")
        print(f"{Fore.RED}\t" + traceback.format_exc().replace("\n", f"\n\t{Fore.RED}"))