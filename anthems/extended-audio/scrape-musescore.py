# IMPORTS
# -------

import requests #give Python ability to make and process HTML requests
from bs4 import BeautifulSoup #library for parsing scraped HTML content
import os #library for interacting with the underlying operating system
import re #needed for figuring out filename from Links
from tqdm import tqdm #for progress bars
import time #for Pause functionality
import string #for function to fix filenames with illegal characters
import random #needed to randomize our User Header (see "user_agents" List, "user_agent" Variable, and "headers" Variable
import json #used to pase json files (which is how the data we need is encoded on the page)

# Defining Constants, Arrays, etc.
# --------------------------------

# This is the prefix of all URLs we are interested in collecting
prefix = "https://musescore.com/user/"
# Create List to store all URLs of interest
scraped_links = []
# Initializing the variable that will keep track of all pertinent URLs you've interacted with
processed_links = 0
# Name of Subdirectory where data and scraped files will be placed
subdir = "downloads"
# Get current directory
here = os.path.dirname(os.path.realpath(__file__))
# Define User Agent -- This will allow our request to seem like it is coming from a "legitimate" source rather than from a web scraper. Doing this will lower the probablity that we will get our IP address banned while scraping.
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

    # for Windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for Mac and Linux (here, os.name is 'posix')
    else:
        _ = os.system('clear')
        

# Function to write all scraped URLs to a file
def writefile():
    file=open('scraped-links.txt','w', encoding="utf-8") # include utf-8 encoding to avoid UnicodeEncodeError

    # PICK ONE OF THE OPTIONS BELOW
    # -----------------------------
    # 1 |
    #----
    # Iterating through entries in the "scraped_links" List and saving to file
    #for items in tqdm(scraped_links):
    #    file.writelines(str(items))
   
    # 2 |
    #----
    # Note that option #1 should write all contents of the List to file on separate lines, but for some reason it does not. On the other hand, this code definitely does.
    for items in tqdm(scraped_links):
        file.write(str(items))
        file.write('\n')
    file.close()

# -------------------------------------------------------------------------------------------------------------------------
# Main Script
# -----------
# Usual "clean-up" (i.e. making a little space at runtime so things are easier to read)
clear()
print("FILE AND LINK SCRAPING UTILITY:")
print("             by Jacques Laroche")
print("-------------------------------")
print("")
time.sleep(2)

# Choose User Header and print it on screen
print("User Agent Header we will report while scraping:")
response = requests.get('https://httpbin.org/headers', headers=headers)
print(response.json()['headers']['User-Agent'])
input("\nPress [Enter] to continue... \n")
clear()

# Code to iterate through all pages
# ---------------------------------

for i in range(99): # number of pages we want to scrape
#for i in range(2): # --> Scrape first 2 pages just to test code <--
    
    # Code for each individual page below
    # -----------------------------------
    
    random_number = random.randint(2,11)
    print("Waiting [" + str(random_number) + "] seconds before scraping next page...\n")
    time.sleep(random_number) # Wait for a random amount of time between each page before scraping. This should make you a bit less detectable.
    
    url = "https://musescore.com/sheetmusic/soundtrack?page=" + str(i+1)
    r = requests.get(url)
    #html_contents = r.text
    soup = BeautifulSoup(r.content, 'html.parser') # r.content would be preferred for "binary" filetypes, such as an image or PDF file
    #soup = BeautifulSoup(r.text, 'html.parser') # r.text would be preferred for textual responses, such as an HTML or XML document
    
    # Looking for the JSON content on the webpage and saving it to a List
    # NOTE: JSON content on the page is in the Class "js-store"
    content_we_want_raw = soup.find("div", attrs={"class": "js-store"})
    
    # Cleaning up the JSON content retrieved from the webpage (removing div tags from the front and the end, and changing encoding of quotes back into quotes), then saving to a new List
    content_we_want_cleaned = str(content_we_want_raw)
    content_we_want_cleaned = content_we_want_cleaned[36:]
    content_we_want_cleaned = content_we_want_cleaned[:-8]
    content_we_want_cleaned = content_we_want_cleaned.replace("&quot;", "\"")
        
    # Saving cleaned up JSON content to file for testing purposes
    #clear()
    #print("Cleaned the site_json string and saving to file...")
    #print("--------------------------------------------------")
    #print()
    #input("\nPress [Enter] to continue... \n") # test breakpoint
    #file=open('json-dump.txt','w', encoding="utf-8") # include utf-8 encoding to avoid UnicodeEncodeError
    #file.write(content_we_want_cleaned)
    #file.close()
    #print("file json-dump.txt saved")
    #input("\nPress [Enter] to continue... \n") # test breakpoint
    
    # Transforming the cleaned up JSON data into actual JSON content
    data_we_want_json = json.loads(content_we_want_cleaned)
       
    
    print("Saving URLs from: [" + url + "]")
    xnum = 0
    while xnum < len(data_we_want_json['store']['page']['data']['scores']):
        #print(data_we_want_json['store']['page']['data']['scores'][xnum]['share'].items())
        #print(data_we_want_json['store']['page']['data']['scores'][xnum]['share'].get('publicUrl'))
        scraped_links.append(data_we_want_json['store']['page']['data']['scores'][xnum]['share'].get('publicUrl'))
        xnum += 1
    print("--DONE--")
    #input("\nPress [Enter] to continue... \n") # testing breakpoint
    
    print("Retrieved all Download file Links from: [Page " + str(i+1) + "]\n")
    print("Number of processed links: [" + str(len(data_we_want_json['store']['page']['data']['scores'])) + "]") # for testing
    print("------------------------------------------------------------------------------------------\n")
    time.sleep(3) # wait for a moment so it is easier to see what is happening in the script


# -----------------------------------------------
# Now we can do things with all the URLs gathered
# -----------------------------------------------
#print(scraped_links) # for debugging

# Write List to File
print("Writing URLs to file: scraped-links.txt")
print("---------------------------------------")
print("NOTE: If the file exists it will be overwritten! \n")
writefile()
input("\nPress [Enter] to continue... \n")
clear()
