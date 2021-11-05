'''
INFO:
-----
This Script opens up the mottos_full_dataset.txt file and places its contents into a Python List.
That list then has all it's contents converted to lowercase and then deduplicated (by converting the list to a Dictionary and then creating a new List from that Dictionary).
The number of entries in the original List and the new deduplicated List are then displayed so we know if there are duplicates.

Suggestions for further modifications of this cript:
----------------------------------------------------
1. Make it more Pythonic and adhering to standard Python Coding Practices (i.e. using "if __name__ == __main__", creating functions, etc.)
2. I went through and just manually removed the duplicates after running this code, but the new deduplicated List could easily be written to file so that this would be automated.
3. Creating a "requirements.txt" file for the imports.

-Jacques Laroche
11/5/2021
'''

# IMPORTS
# -------
from tqdm import tqdm #for progress bars
import os #for screen clearing function

# Defining Constants, Arrays, etc.
# --------------------------------

# Create List to store contents of opened file
file_contents = []


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


# MAIN CODE
# ---------

clear()
print("")

# Open the files with our Mottos
with open('mottos_full_dataset.txt') as f:
    # Read file
    raw_contents = f.read()

    # Turn the contents of the file into a list
    file_contents = list(raw_contents.split("\n"))

    # Iterate over the list
    print("Processing List: Converting each item to Lowercase...\n")
    for items in tqdm(range(len(file_contents))):
        #print(items) # for testing
        file_contents[items] = file_contents[items].lower()
    print()
    input("\nPress [Enter] to continue... \n")
    clear()

#print("Printing All List Items:")
#print("------------------------")
#input("\nPress [Enter] to continue... \n")
#print(file_contents)


# Remove Duplicates from file_contents list (by using a dictionary)
dictionary = dict.fromkeys(file_contents)
deduplicated_list = list(dictionary)

print("Printing Deduplicated List of Items:")
print("------------------------")
input("\nPress [Enter] to continue... \n")
print(deduplicated_list)
print()
input("\nPress [Enter] to continue... \n")
clear()


print("Were there duplicates?")
print("----------------------\n")
print("Original File Contents | Number of items: " + str(len(file_contents)))
print("Deduplicated File Contents | Number of items: " + str(len(deduplicated_list)))
