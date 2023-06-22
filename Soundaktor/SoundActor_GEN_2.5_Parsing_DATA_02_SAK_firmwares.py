import sys
import os
import re
import time


if sys.version_info[0] < 3:
    print("Install Python 3 or newer!")
    sys.exit(1)
    
def creation_directory_extract(filename):
    path = f"GEN_2.5_SAK_DATA_02"
    if not os.path.isdir(path):
        os.makedirs(path)
    print(f"Created directory extract: {path}")

def extract_data_02(filename, num_file):
    try:
        result_data_02 = search_data_02(filename)
        creation_directory_extract(filename)
        output_file_name = f"GEN_2.5_SAK_DATA_02/{'_'.join(filename.rsplit('.')[:-1])}_DATA_02.bin"
        with open(output_file_name, 'wb') as out_file:
            out_file.write(result_data_02)
            write_meta_info_data_02_file(f"{num_file}) {output_file_name}")
    except Exception as e:
        sys.exit(f"\nError parsing files.\n{e}")
    else:
        print("Finished writing output files.")

def write_meta_info_data_02_file(filename):
    with open("GEN_2.5_SAK_DATA_02/meta_extract_data_02_firmwares_SAK.txt", "a+") as firmware_names:
        print(filename, file=firmware_names)
        
def search_work_files(directory, num_file=1, flag=False):
    # Search files in current directory
    for current_dir, dirs, files in os.walk(directory): 
        for file in files:
            if file[-4:] == ".odx":
                print(f"\nFile found {file:*^50}")
                extract_data_02(file, num_file)
                flag = True
                num_file += 1
    if not flag:
        print("Files with extension .ODX not found.\n")
        input("Press Enter to exit...")
        sys.exit(0)
        
def search_data_02(file, data_02=None):
    with open(f'{file}', 'r', encoding='utf-8') as file:
        for line in file:
            response = re.findall(r'<DATA>([A-Za-z0-9]{196608})</DATA>', f'{line}')
            if response:
                data_02 = bytearray.fromhex(''.join(response))
                break
        if data_02:
            return data_02
        print("Extract DATA_02 not found.")
        input("Press Enter to exit...")
        sys.exit(0)
   
def parsing_odx_files(directory):
    search_work_files(directory)
    print("\nDone's.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    # Current working directory
    directory = os.getcwd()
    meta_file = "GEN_2.5_SAK_DATA_02/meta_extract_data_02_firmwares_SAK.txt"
    if os.path.isfile(meta_file):
        os.remove(meta_file)
    print(f"Search in current category: {directory}\n")
    time.sleep(1)
    parsing_odx_files(directory)


