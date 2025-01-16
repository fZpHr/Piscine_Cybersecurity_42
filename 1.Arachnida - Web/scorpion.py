import sys
import os
from colorama import Fore, Back, Style, init
import traceback
import exiftool

def display_metadata(file_path):
    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(file_path)
        for d in metadata:
            for key, value in d.items():
                print(f"{key}: {value}")

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