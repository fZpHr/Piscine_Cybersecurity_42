import requests
from bs4 import BeautifulSoup
import shutil
import os
import sys
import argparse
import traceback
from colorama import init, Fore, Back, Style 

init(autoreset=True)

def download_images(url, recursive, level, path):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur lors de la requête. {response} -> {url}")
        exit()

    soup = BeautifulSoup(response.content, 'html.parser')
    extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    attributes = ['src', 'data-src', 'content', 'href']

    image_urls = []
    already_downloaded = []

    url = url.split('/')
    if len(url) > 3:
        url = '/'.join(url[:3])
    tags = soup.find_all(['img', 'link', 'meta', 'a'])
    for tag in tags:
        for attr in attributes:
            if attr in tag.attrs and any(tag[attr].endswith(ext) for ext in extensions):
                image_urls.append(tag[attr])
                break    
    for i, image_url in enumerate(image_urls):
        print(f"before - > {image_url}")
        if not image_url.startswith(('http://', 'https://')):
            image_url = url + image_url

        print(f"after - > {image_url} \n\n")
        image_response = requests.get(image_url, stream=True)

        if image_url in already_downloaded:
            print(f"Image {i+1} déjà téléchargée.")
            continue
        else:
            if image_url.endswith('.png'):
                with open(f'image_{i+1}.png', 'wb') as out_file:
                    shutil.copyfileobj(image_response.raw, out_file)
            elif image_url.endswith('.jpg'):
                with open(f'image_{i+1}.jpg', 'wb') as out_file:
                    shutil.copyfileobj(image_response.raw, out_file)
            elif image_url.endswith('.jpeg'):
                with open(f'image_{i+1}.jpeg', 'wb') as out_file:
                    shutil.copyfileobj(image_response.raw, out_file)
            elif image_url.endswith('.gif'):
                with open(f'image_{i+1}.gif', 'wb') as out_file:
                    shutil.copyfileobj(image_response.raw, out_file)
            elif image_url.endswith('.bmp'):
                with open(f'image_{i+1}.bmp', 'wb') as out_file:
                    shutil.copyfileobj(image_response.raw, out_file)
        already_downloaded.append(image_url)

        print(f"Image {i} téléchargée avec succès. ")

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
    
    download_images(args.url, args.r, args.l, args.p)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Back.RED}An error occurred: {e}, traceback below:")
        print(f"{Fore.RED}\t" + traceback.format_exc().replace("\n", f"\n\t{Fore.RED}"))
        sys.exit(1)