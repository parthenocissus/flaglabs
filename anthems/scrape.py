# IMPORTS
# -------

import requests
from bs4 import BeautifulSoup
import os
import re #needed for figuring out filename from Links
from tqdm import tqdm #for progress bars
import time #for Pause functionality
import urllib3 #needed to disable warnings if the site being scraped has an SSL certificate error
import string #for function to fix filenames with illegal characters
import random #needed to randomize our User Header

# Defining Constants, Arrays, etc.
# --------------------------------

# Create List to store all URLs for downloadable files
scraped_links = []
# Keep track of the number of URL links for downloadable files you have interacted with
processed_links = 0
# Suppress warnings if the site being scraped has an SSL certificate error
urllib3.disable_warnings()
# Name of Subdirectory where scraped files will be placed
subdir = "downloads"
# Get current directory
here = os.path.dirname(os.path.realpath(__file__))
# Define User Agent -- This will allow our request to seem like it is coming from a "legitimate" source, rather than from a web scraper. Doing this will lower the probablity that we will get our IP address banned while scraping.
user_agents = [
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
	'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
	'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
]
user_agent = random.choice(user_agents)
headers = {'User-Agent': user_agent}

# Defining Functions
# ------------------

# Function to Clear the Screen
def clear():

    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

# Function to write all scraped URLs to a file
def writefile():
    file=open('scraped-links.txt','w')
    for items in tqdm(scraped_links):
        file.writelines(items+'\n')
    file.close()

# Function to get filename from Link
def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    r = requests.get(cd, allow_redirects=True,verify=False)
    cd = r.headers.get('content-disposition')
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

# Function to fix filenames with illegal characters
def makeSafeFilename(inputFilename):
    # Define valid characters
    invalid = '<>:"/\|?* '

    for char in invalid:
        inputFilename = inputFilename.replace(char, '')

    return inputFilename

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

# Main Script
# -----------
# Usual clean-up -- making a little space at runtime so things are easier to read
clear()
print("FILE AND LINK SCRAPING UTILITY: ")
print("      by Jacques Laroche")
print("-------------------------------")
print("")
time.sleep(2)

# For Header Testing Purposes
print("User Agent Header we will divulge while scraping:")
response = requests.get('https://httpbin.org/headers', headers=headers)
print(response.json()['headers']['User-Agent'])
input("\nPress [Enter] to continue... \n")

# Code to iterate through all pages
# ---------------------------------

for i in range(5): # number of pages we want to scrape
    url = "https://www.midiworld.com/search/" + str(i+1) + "/?q=national%20anthems"
    r = requests.get(url,verify=False)
    soup = BeautifulSoup(r.content, "html.parser")

    # Code for each individual page below
    # -----------------------------------

    # Find all hyperlinks present on page
    #links = soup.find_all('a', href=True)
    links = soup.find_all("a", string="download") # on this site all links we are interested in have the word "download" in the <a> tag

    # From all links check for MIDI file link and if present download file
    print("Saving URLs from " + url + " to List: ")
    for link in tqdm(links):
        scraped_links.append(link['href'])
        processed_links += 1

    print("Retrieved all Download file Links from: [Page " + str(i+1) + "]\n")
    time.sleep(3) # wait for a moment so it is easier to see what is happening in the script

# -----------------------------------------------
# Now we can do things with all the URLs gathered
# -----------------------------------------------
#print(scraped_links) # for debugging

# Feedback about number of items scraped
print("Total Number of Scraped Links: " + str(processed_links) + "\n")
input("Press [Enter] to continue... \n")
clear()

# Write List to File
print("Writing URLs to file: scraped-links.txt")
print("---------------------------------------")
print("NOTE: If the file exists it will be overwritten! \n")
writefile()
input("\nPress [Enter] to continue... \n")
clear()

# Downloading Files
print("Downloading all files: \n")
for items in tqdm(scraped_links):
    try:
        file_url = items
        file_stream = requests.get(file_url, stream=True, verify=False)
        rawFilename = getFilename_fromCd(items)
        fixedFilename = makeSafeFilename(rawFilename)
        path_with_filename = os.path.join(str(here), str(subdir), str(fixedFilename))

        with open(path_with_filename, 'wb') as local_file: # NOTE: writing in binary mode
            for data in file_stream:
                try:
                    local_file.write(data)
                except Exception as e:
                    logf = open("error.log", "a")
                    logf.write("Failed to download {0}: {1}\n".format(str(data), str(e)))
                    logf.close()
                finally:
                    # optional clean up code
                    pass

    except Exception as e:
        logf = open("error.log", "a")
        logf.write("Failed to download {0}: {1}\n".format(str(data), str(e)))
        logf.close()
    finally:
        # optional clean up code
        pass

print("[DOWNLOADING COMPLETE!]")
