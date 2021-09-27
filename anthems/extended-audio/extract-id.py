# IMPORTS
# -------
from tqdm import tqdm #for progress bars

# Definition of variables:
# ------------------------

# Create List to store contents of file with scraped links
file_contents = []
# Create List to store extracted IDs from the scraped links
id_list = []
# This is the place where the URLs will be split in order to extract the IDs
split_mark = "/scores/"
# Initializing the variable that will keep track of all extracted IDs
processed_IDs = 0

# Cleanup
# -------
print()


# Open the Scraped Link
with open('scraped-links.txt') as f:
    # Read file
    raw_contents = f.read()
    
    # Turn the contents of the file into a list
    file_contents = list(raw_contents.split("\n")) 
    
    # Print the contents of the List created from the file
    #print("Contents of the scraped-links txt file converted into a List:")
    #print("-------------------------------------------------------------")
    #print(file_contents)
    #print()
    #print("Length of List: " + str(len(file_contents)))
    #print()
    #input("\nPress [Enter] to continue... \n")
    
    #print(type(file_contents)) # for debugging purposes
    
    # Iterate over the list
    print("Processing all items and extracting IDs...\n")
    for items in tqdm(file_contents):
        #print(items) # for testing
        id_list.append(items.partition(split_mark)[2])
        #print(items.partition(split_mark)[2]) # for testing
      
#print(id_list) # for testing


# Writing all IDs to file
print()
print("Writing all extracted IDs to file...")
file=open('extracted-ids.txt','w', encoding="utf-8")
for items in id_list:
    file.write(str(items))
    file.write('\n')
    processed_IDs += 1
file.close()
print("--DONE--\n")

# Post-task Informaion:
print("[ " + str(processed_IDs) + " IDs saved to: extracted-ids.txt ]")

