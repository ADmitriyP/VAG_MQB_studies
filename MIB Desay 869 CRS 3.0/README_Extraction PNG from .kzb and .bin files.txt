This script is written in Python. With it, you can extract and view the contents of .kzb or .bin files for the presence of graphic files with the .png extension.
To do this, you need to unpack any firmware image for FAW-VW CRS 3.0 Desay 869-A. This image is a .tar archive with a .bin extension. After unpacking, find the share/ui directory, copy this script to any of the contents of the directories and run it.
The files will be recursively crawled to find files with the extension .kzb or .bin, followed by extraction and saving the found .png files to the IMAGES directory.
The number and information about the found files will be written to a text document and displayed in the console.
