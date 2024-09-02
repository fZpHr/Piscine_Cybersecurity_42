import requests
from bs4 import BeautifulSoup
import shutil
import os
import sys

url = sys.argv[1]

response = requests.get(url)
if response.status_code != 200:
    print("Erreur lors de la requête.")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')
img_tags = soup.find_all('img')
png_urls = [img['src'] for img in img_tags if 'src' in img.attrs and img['src'].endswith('.png')]
for i, image_url in enumerate(png_urls):

    if not image_url.startswith(('http://', 'https://')):
        image_url = os.path.join(url, image_url)

    image_response = requests.get(image_url, stream=True)

    with open(f'image_{i}.png', 'wb') as out_file:
        shutil.copyfileobj(image_response.raw, out_file)

    print(f"Image {i} téléchargée avec succès. ")
    