# IMPORTS
# -------
import csv #for working with csv files
from tqdm import tqdm #for progress bars

# Definition of variables:
# ------------------------
filename = "mscz-files.csv" # Name of the file we will be opening
filename2 = "ipfs-links.txt" # Name of the ilfe we will save all matched IPFS links to

# Create List to store contents of TXT file
txtfile_contents = []
# Create List to store all IDs from the TXT file
ids = []
# Create List to store all rows in the CSV file
rows = []
# Create Lists to store all matched IPFS hashes within the "mscz-files.csv" file to the ID numbers from the "extracted-ids.txt" file
correlation_list = []
#deduped_correlation_list = [] # This is for the deduplication of this list

# Initializing the variable that will keep track of ...
processed_ipfs = 0

# Cleanup
# -------
print()


# Open the TXT file with all extracted IDs --NOTE: entries are separated by "/n" 
txtfile=open('extracted-ids.txt')

# Read file
raw_contents = txtfile.read()
    
# Turn the contents of the file into a list
txtfile_contents = list(raw_contents.split("\n")) 

# Iterate over the list
print("Processing all IDs from the [extracted-ids.txt] file...")
print("-------------------------------------------------------")
for items in tqdm(txtfile_contents):
    ids.append(items)
        
# Close the file
txtfile.close()

# For testing purposes
#print("\nContents of ids List:")
#print("---------------------")
#input("\nPress [Enter] to continue... \n")
#print(ids)
#input("\nPress [Enter] to continue... \n")

#------------------------------------------------------------

# Open the large CSV with the IPFS hashes for MSCZ files
with open(filename, 'r') as csvfile:
    # Read file
    csv_contents = csv.reader(csvfile)
    
    # extracting field names through first row
    fields = next(csv_contents)
    
    # extracting each data row one by one
    print("\nExtracting data from: " + filename)
    
    for row in tqdm(csv_contents):
        rows.append(row)   
    print()
    
    
    #print("\nTotal number of rows: %d" %(csv_contents.line_num))
    #print("----------------------" + len(str(abs(csv_contents.line_num)))*"-")
    
    #input("\nPress [Enter] to continue... \n")
    
#  printing first 5 rows
#print('\nFirst 5 rows:')
#print("-------------\n")
#for row in rows[:5]:
    # parsing each column of a row
    #for col in row:
    #    print("%10s"%col)
        
# NOTE: To download the IPFS files you must use this format ---
# https://ipfs.io/ipfs/QmXoj9hcQKPaP8zjfJADsvPfccM6duMVT6eNXPjhcTqjQ3
# (after the "https://ipfs.io.ipfs/" goes the hash to the IPFS file resource

# NOTE: Below methodology is very slow and dumb...
# ------------------------------------------------
# Iterate over the "ids" List, look for a matching ID in the "rows" List and place the 2nd column associated with that matched ID's row into the "correlation_list" List
#for id in ids:
#    for row in rows:
#        if id == row[0]:
#            print(id + " and " + row + " are the same.")


# Create a Set with all the IDs, then check if the ID in the CSV data is within the ID Set then append the corresponding IPFS link into the "correlation_list" List
    print("Matching IDs with IPFS link:")
    print("----------------------------")
    ids = set(ids)
    for row in tqdm(rows):
        if row[0] in ids:
            #print("ID: " + str(row[0] + " IPFS: " + str(row[1])))
            #correlation_list.append(str(row[1]))
            correlation_list.append("https://ipfs.io" + str(row[1]))
            #correlation_list.append(str(row[0] + " " + str(row[1])))
    print()
    input("\nPress [Enter] to continue... \n")


# Removing duplicate items from 'correlation_list'
#[deduped_correlation_list.append(x) for x in correlation_list if x not in deduped_correlation_list]
deduped_correlation_list = list(set(correlation_list))

print()
print("Number of matches found: [" + str(len(deduped_correlation_list)) + "]\n")

# Writing all IDs to file
print("Saving List of matched IPFS links to file: [" +str(filename2) +"] ...")
print("-------------------------------------------------" + "-"*(len(str(filename2))))
file=open(filename2,'w', encoding="utf-8")
for items in tqdm(deduped_correlation_list):
    file.write(str(items))
    file.write('\n')
    processed_ipfs += 1
file.close()

print("-- Saved [" + str(processed_ipfs) + "] IPFS links --")
print("-- DONE! --\n")