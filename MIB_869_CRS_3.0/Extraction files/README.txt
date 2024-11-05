This script is written in Python.It allows you to extract and view the contents of .kzb or .bin files to check for graphic files with the .png extension.

To use it, start by unpacking a firmware image for the FAW-VW MIB 869 CRS 3.0 system. This image is a .tar archive with a .bin extension. After unpacking, locate the share/ui directory, copy this script into any subdirectory, and run it.

The script will recursively scan all files to locate those with .kzb or .bin extensions, extract their contents, and save any found .png files in the IMAGES directory.

A log of the number and details of the discovered files will be saved to a text document and displayed in the console.