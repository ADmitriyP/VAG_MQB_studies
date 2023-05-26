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
    
def write_image_meta_information(meta_info):
    with open("IMAGES/extracted_meta_info_of_images.txt", "a+") as image_info:
        print(meta_info, file=image_info)
        
def write_list_image_names(found_filenames, filename):
    if not os.path.isdir("IMAGES"):
        os.makedirs("IMAGES")
    with open("IMAGES/extracted_list_of_images.txt", "a+") as image_names:
        image_names.write(f"\nFile found {filename:*^50}\n\nFound filenames with .png extension:\n\n")
        for number, line in enumerate(found_filenames, 1):
            print(f"{number}) {line}", file=image_names)

def extract_and_write_images(filename):
    try:
        result_search_images = list(zip(*search_images(filename)))
        creation_directory_extract(filename)
        pbar = tqdm(result_search_images, bar_format="{l_bar}{bar}")
        number_image = 0
        with open("IMAGES/extracted_meta_info_of_images.txt", "a+") as image_info:
            image_info.write(f"\nFile found {filename:*^50}\n\n")
        for png, name in pbar:
            #pbar.set_description(f'\nExtraction process {count_image + 1}')
            output_file_name = f"IMAGES/{filename.split('.')[0]}_Extract/{name}"
            with open(output_file_name, 'wb') as out_file:
                out_file.write(png)
            with Image.open(output_file_name) as im:
                number_image += 1
                meta_info = f"{number_image}) {output_file_name} - size:{im.size} / {im.mode} / {sys.getsizeof(png)} byte"
                write_image_meta_information(meta_info)
    except Exception as e:
        sys.exit(f"\nError parsing files. {e}")
    else:
        print("Finished writing output files.")
        print(f"Total PNG images found: {number_image}.")

        
def find_filenames(bin_data, found_filenames):
    pattern = r"([A-Z]?[a-zA-Z0-9\s_\.\-]+\.(?:png|PNG))+\s?"
    text = bin_data.decode("ANSI")
    list_names_png = re.findall(pattern, text)
    for name in list_names_png:
        found_filenames.add(name)
       
def search_work_files(directory, flag=False):
    #Search files in current directory
    for current_dir, dirs, files in os.walk(directory): 
        for filename in files:
            if filename[-4:] == ".kzb" or filename[-4:] == ".bin":
                print(f"\nFile found {filename:*^50}")
                flag = True
                extract_and_write_images(filename)
    if not flag:
        print("Files with extension .KZB or .BIN not found.\n")
        input("Press Enter to exit...")
        sys.exit(0)
        
def search_images(filename):
    with open(f"{filename}", "rb") as binary_file:
        bin_data = binary_file.read()
    png_data, found_index_png, found_filenames, start_index = [], [], set(), 0
    find_filenames(bin_data, found_filenames)
    write_list_image_names(found_filenames, filename)
    #print(*found_filenames, sep='\n')
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
    #Current working directory
    directory = os.getcwd()
    meta_image_file = "IMAGES/extracted_meta_info_of_images.txt"
    name_image_file = "IMAGES/extracted_list_of_images.txt"
    if os.path.isfile(meta_image_file) and os.path.isfile(name_image_file):
        os.remove(meta_image_file)
        os.remove(name_image_file)
    print(f"Search in current category: {directory}\n")
    time.sleep(1)
    parsing_kzb_bin_files(directory)