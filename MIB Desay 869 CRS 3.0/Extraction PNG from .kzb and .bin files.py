import sys
import os
import re
import time


if sys.version_info[0] < 3:
    print("Install Python 3 or newer!")
    sys.exit(1)
    
try:
    from tqdm import tqdm
    from PIL import Image
except ImportError:
    print("Check required modules\n: tqdm, PIL")
    input("\nPress Enter to exit...")
    sys.exit(1)

def creation_directory_extract(filename):
    path = f"IMAGES/{filename.split('.')[0]}_Extract"
    if not os.path.isdir(path):
        os.makedirs(path)
    print(f"\nCreated directory extract: {path}")

def extract_images(filename):
    try:
        result_search_images = list(zip(*search_images(filename)))
        creation_directory_extract(filename)
        pbar = tqdm(result_search_images, bar_format="{l_bar}{bar}")
        number_image = 0
        for png, name in pbar:
            #pbar.set_description(f'\nExtraction process {count_image + 1}')
            output_file_name = f"IMAGES/{filename.split('.')[0]}_Extract/{name}"
            with open(output_file_name, 'wb') as out_file:
                out_file.write(png)
                number_image += 1
            im = Image.open(output_file_name)
            meta_info = f"{number_image}) {output_file_name} - size:{im.size} {im.mode}"
            write_meta_info_image_file(meta_info)
        else:
            print("Finished writing output files.")
    except Exception:
        sys.exit("\nError parsing files.")
    else:
        print(f"Total PNG images found: {number_image}.")

def write_meta_info_image_file(meta_info):
    with open("IMAGES/meta_extract_images.txt", "a+") as image_info:
        print(meta_info, file=image_info)
        
def find_filenames(buffer, found_filenames):
    pattern = r"([A-Z]?[a-zA-Z0-9\s_\.\-]+\.(?:png|PNG))+\s?"
    text = buffer.decode("ANSI")
    list_names_png = re.findall(pattern, text)
    for name in list_names_png:
        found_filenames.add(name)
       
def search_work_files(directory, flag=False):
    # Search files in current directory
    for current_dir, dirs, files in os.walk(directory): 
        for filename in files:
            if filename[-4:] == ".kzb" or filename[-3:] == ".bin":
                print(f"\nFile found {filename:*^50}")
                extract_images(filename)
                flag = True
    if not flag:
        print("Files with extension .KZB or .BIN not found.\n")
        input("Press Enter to exit...")
        sys.exit(0)
        
def search_images(filename):
    with open(f"{filename}", "rb") as binary_file:
        bin_data = binary_file.read()
    png_data, found_index_png, found_filenames, start_index = [], [], set(), 0
    find_filenames(bin_data, found_filenames)

    print("\nFound filenames with .png extension:\n")
    print(*found_filenames, sep='\n')

    while True:
        start_index = bin_data.find(b"\x89\x50\x4e\x47", start_index)
        if start_index == -1:
            break
        end_index = bin_data.find(b"\x49\x45\x4e\x44\xae\x42\x60\x82", start_index + 8)
        if end_index == -1:
            break
        png_data.append(bin_data[start_index:end_index + 8])
        found_index_png.append(f"png_{start_index}_{end_index}.png")
        start_index = end_index + 8
    if png_data and found_index_png:
        return png_data, found_index_png
    else:
        print("Extract image files not found")
        input("Press Enter to exit...")
        sys.exit(0)
   
def parsing_kzb_bin_files(directory):
    search_work_files(directory)
    print("\nDone's.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    # Current working directory
    directory = os.getcwd()
    meta_file = "IMAGES/meta_extract_images.txt"
    if os.path.isfile(meta_file):
        os.remove(meta_file)
    print(f"Search in current category: {directory}\n")
    time.sleep(1)
    parsing_kzb_bin_files(directory)
