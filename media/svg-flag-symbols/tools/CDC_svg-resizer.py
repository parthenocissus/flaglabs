# IMPORTS
# -------
#for xml parsing
from xml.dom import minidom
#for executing commands in OS (Linux)
import os
#for getting a list of files
import glob
#for detecting Python version
import sys
# ----> NOTE: All of these imports are from the standard library


# Main Function
# -------------
def main():
    
    # Definition of variables:
    # ------------------------
    dimensions = []
    list_of_files = []
    path = os.getcwd()
    resize_folder = "resize" # name of directory where resized SVG files will be saved
    
    # Populate List with all SVG filenames
    list_of_files = glob.glob("*.svg")
    #print(list_of_files) # for debugging
    
    # Create Directory where resized SVGs will go (if the directory doesn't already exist)
    if not os.path.exists(resize_folder):
        os.makedirs(resize_folder)
        
    # Information for user feedback
    print("\nPreparing to process SVGs: [" + str(len(list_of_files)) + " files]")
    if sys.version_info[0] == 2:
        raw_input("Press [Enter] to continue...\n")
    elif sys.version_info[0] == 3:
        input("Press [Enter] to continue...\n")
        
    
    # Main loop of script:
    # --------------------
    for file in list_of_files:
        
        # Create Variables for running the rsvg-convert command
        cmd1 = "rsvg-convert --width=100 --format svg --keep-aspect-ratio " + file + " > " + resize_folder + "/100px_" + file
        cmd2 = "rsvg-convert --height=100 --format svg --keep-aspect-ratio " + file + " > " + resize_folder + "/100px_" + file
        
        # use the parse() function to load and parse an XML file
        svg_file = minidom.parse(file)
        svgtag_elements = svg_file.getElementsByTagName('svg')
        dimensions = svgtag_elements[0].attributes['viewBox'].value
        dimensions = dimensions.split()
        width = float(dimensions[2])
        height = float(dimensions[3])
        
        print("Processing: " + str(file))
        print("Width: " + str(dimensions[2]))
        print("Height: " + str(dimensions[3]))
        print("")
        
        if width == height:
            #run this command--> rsvg-convert --width=100 --format svg --keep-aspect-ratio inputfilename.svg > outputfilename.svg
            #print("Width and Height are Equal")
            os.system(cmd1)
        elif width > height:
            #run this command--> rsvg-convert --width=100 --format svg --keep-aspect-ratio inputfilename.svg > outputfilename.svg
            #print("Width is greater than Height")
            os.system(cmd1)
        elif width < height:
            #run this command--> rsvg-convert --height=100 --format svg --keep-aspect-ratio inputfilename.svg > outputfilename.svg
            #print("Height is greater than Width")
            os.system(cmd2)
            
    print("")
    print("------------------------------------------")
    print("SVG file processing and resizing complete!")
    print("Resized files can be found in the following subdirectory: /" + str(resize_folder))
    

# Main Code:
# ----------
if __name__ == "__main__":
    main()