import sys
import os
from PIL import Image
import exifread
import traceback
from colorama import Fore, Back, Style, init

def display_metadata(file_path):
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
        
        print(f"{Fore.GREEN}File: {file_path}")
        print(f"{Fore.GREEN}Size: {os.path.getsize(file_path)} bytes")
        
        for tag in tags.keys():
            print(f"{Fore.YELLOW}{tag}: {tags[tag]}")
    except Exception as e:
        print(f"{Back.RED}Error processing {file_path}: {e}")

def main():
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Usage: python scorpion.py image1 image2 ...")
        exit()

    for image_path in sys.argv[1:]:
        if (sys.argv[1] != image_path):
            print(f"{Fore.BLUE}--------------------------")
        display_metadata(image_path)

if __name__ == "__main__":
    init(autoreset=True)
    try:
        main()
    except Exception as e:
        print(f"{Back.RED}An error occurred: {e}, traceback below:")
        print(f"{Fore.RED}\t" + traceback.format_exc().replace("\n", f"\n\t{Fore.RED}"))