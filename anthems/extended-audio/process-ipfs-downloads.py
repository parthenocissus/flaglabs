# IMPORTS
# -------
from tqdm import tqdm #for progress bars
import os #library for interacting with the underlying operating system
import zipfile #for unzipping files


# Definition of variables:
# ------------------------

# Get current directory
here = os.path.dirname(os.path.realpath(__file__))
# Name of Subdirectory where downloaded files will be placed
download_subdir = "soundtracks"
download_path = here + "\\" + download_subdir
# Name of Subdirectory where the downloaded files will be unzipped
unzip_subdir = "unzip"
unzip_path = download_path + "\\" + unzip_subdir


# Defining Functions
# ------------------

# Function to create directories
def create_folder(path):
        try:
            if os.path.isdir(path):
                #print("Error: The directory you're attempting to create already exists") # or just pass
                pass
            else:
                os.makedirs(path)
        except IOError as exception:
            raise IOError('%s: %s' % (path, exception.strerror))
        return None
        
# Function to Clear the Screen
def clear():

    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')
        
# Function to change names for all files in download directory (.\soundtracks)
def filename_change():
    print("\nRenaming all files in the soundtracks directory...")
    print("--------------------------------------------------") 
    for file in tqdm(os.listdir(download_path)):
        f_ext = ".zip"
        new_name = f'{file}{f_ext}'
        if file != unzip_subdir:
            os.rename(download_path+"\\"+file, download_path+"\\"+new_name)

# Function to unzip all downloaded files and place the contents in the unzip directory (.\soundtracks\unzip)
def unzip_all():
    print("\nUnpacking all files and placing them in .\\soundtracks\\unzip...")
    print("--------------------------------------------------------------") 
    
    # Variable for counting how many files were unzipped
    file_count = 0
    
    for file in tqdm(os.listdir(download_path)):   # get the list of files -- display with progress bar
        #print("File found in " + str(download_path) + " --> " + str(file))
        if zipfile.is_zipfile(download_path + "\\" + file): # if it is a zipfile, extract it
            with zipfile.ZipFile(download_path + "\\" + file) as item: # treat the file as a zip
                item.extractall(unzip_path)  # extract it in the working directory
                file_count += 1
                
    print()
    print("Path where files have been unzipped: " + str(unzip_path))
    print("Number of files unzipped: " + str(file_count))
 
# Main Code:
# ----------

# "Cleanup"
clear()
print()

# Creating Subdirectory where downloaded files will go
print("Creating subdirectory: .\\" + str(download_subdir))
create_folder(download_subdir)
print("[DONE]\n")
# Creating Subdirectory where the unzipped files will be placed
print("Creating subdirectory: .\\" + str(download_subdir) + "\\" + str(unzip_subdir))
create_folder(download_subdir + "\\" + unzip_subdir)
print("[DONE]\n")

# Break point
input("\nPress [Enter] to continue... \n")
clear()
print()

# --------------------------->

changename = input("Would you like to add the .zip extension to all filenames in the download directory? (y/yes or n/no): ").lower()
if changename == "yes" or changename == "y":
	filename_change()
elif changename == "no" or changename == "n":
	pass

print()

unpack = input("Would you like to unzip all files in the download directory? (y/yes or n/no): ").lower()
if unpack == "yes" or unpack == "y":
	unzip_all()
elif unpack == "no" or unpack == "n":
	pass
