# IMPORTS
# -------
import wget # for downloading files
from tqdm import tqdm #for progress bars
import os #library for interacting with the underlying operating system


# Definition of variables:
# ------------------------
download_links = [] # this is where all download links from the ipfs-links.txt file will be stored for download procedure
# Name of Subdirectory where data and scraped files will be placed
subdir = "soundtracks"


# Defining Functions
# ------------------

# Function to create directory where scraped files will be saved
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

create_folder(subdir)


# Cleanup:
# --------
print()


# Open the TXT file with all extracted IPFS download links --NOTE: entries are separated by "/n" 
txtfile=open('ipfs-links.txt')
# Read file
raw_contents = txtfile.read()
# Turn the contents of the file into a list
txtfile_contents = list(raw_contents.split("\n")) 

# Iterate over the list
print("Processing all URLs from the [ipfs-links.txt] file...")
print("----------------------------------------------------")
for items in tqdm(txtfile_contents):
    download_links.append(items)
        
# Close the file
txtfile.close()
print()

#print(download_links) # for testing

# Download all the files
print("Downloading all files from the [ipfs-links.txt] file...")
print("-------------------------------------------------------")
for item in tqdm(download_links):
    try:
        wget.download(item, out=subdir)
    except Exception as e:
        logf = open("error.log", "a")
        logf.write("Failed to download {0}: {1}\n".format(str(item), str(e)))
        logf.close()
    finally:
        # optional clean up code
        pass