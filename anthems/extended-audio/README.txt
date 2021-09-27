Prepare your Python Environment:
--------------------------------
Simply load up the "requirements.txt" file in your preferred Python virtual environment so you have all the necessary Python Libraries installed to run this project.

	-- Loading Python Packages from a requirements file --
        ------------------------------------------------------
	> pip install -r requirements.txt

Instructions:
-------------

1) > First choose the type, or genre of files you want to retrieve from the MuseScore website (at https://musescore.com/)
   > Click on checkbox for the Genre(s)
   > Write down the URL and take note of how many hits & pages the search result returned. Note you can check how many pages by clicking on the "Last" button
 
2) scrape-musescore.py
   > This is the first script we will use. Open up the script and add the URL you wrote down from Step 1 to the "url" Variable. Then under the
   "Code to iterate through all pages" section change the For Loop to be one less than the number of pages you noted from the search results in Step 1.

   > Run the code to scrape all the links for the files you want. The list will be saved to a file named "scraped-links.txt" in the same directory.

3) extract-id.py
   > This is the second script we will use. Run the script in the same location the "scraped-links.txt" file was saved. It will extract all file IDs from the
   URLs in the "scraped-links.txt" file generated in Step 2. A file called "extracted-ids.txt" with all these extracted IDs will be saved in the same directory.

4) get-ipfs.py
   > This is the third script we will use. Please make sure to download mscz-files.csv from the musescore-dataset Github page (https://github.com/Xmader/musescore-dataset).
   The exact link to the CSV file is https://musescore-dataset.xmader.com/mscz-files.csv. Run the script in the same directory as the CSV file and the
   "extracted-ids.txt" file generated in Step 3. This script will modify the "ipfs-links.txt" file so that it has all the IPFS download links for the
   IDs we got earlier. This is done by matching the IDs from the extracted-ids.txt file from Step 3 to the links in the CSV file.

5) ipfs-downloader.py
   > This is the fourth script we will run. This script will download all the files from the updated "ipfs-links.txt" file and place them in a subdirectory called "soundtracks".

6) process-ipfs-downloads.py
   > This is the sixth and last script we will run. This script will go into the soundtracks folder and rename all the downloaded files so they have a .zip
   extension. It will then create another subdirectory called "unzip" underneath the "soundtracks" subdirectory (i.e. ./soundtracks/unzip). All the Zip files
   will be unzipped into this new directory.

7) > The last step in this pipeline is to convert all the mscx files to MIDI files. Go to https://musescore.org/en/download, then download and install the newest
   version for your OS. Then go to https://musescore.org/en/project/batch-convert to download the "Batch Convert" plugin for MuseScore. Assuming you installed
   MuseScore 3.x, unzip the plugin file and place the contents in your Plugin directory (according to the instructions here: https://musescore.org/en/handbook/3/plugins#installation).
   Open MuseScore and make sure to activate the plugin.

   > To use the converter choose the "Batch Convert" option under the "Plugins" menu within MuseScore. Specify the Input Format, Output Format(s), etc. and press the "OK"
   button. A dialog box will open asking you to choose the source folder. Choose where your .mscx files were unzipped to in Step 6. Then a new dialog box will open
   asking you where you would like to place the converted files (if you checked the "Different Export Path" option - which I recommend doing).

   NOTE: If the mscx file you are converting was originally created in an older version of MuseScore you will be prompted to save the file when the batch conversion process
         attempts to close it during the conversion operation. Unfortunately, this breaks the whole point of having an unattended batch process, but there doesn't seem to be
         a solution to this issue as this is happening due to functionality built-in to the MuseScore application. For now, we will have to make due with 6 out of 7 processes
         being truly and fully automated.