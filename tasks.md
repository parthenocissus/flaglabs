# Current To Do List


**Jacques Laroche**:

- [x] Create "National Mottos" dataset<br/> 
	**NOTE:** create set from various web sources and specify those sources

- [x] Add Real Mottos to "National Mottos" dataset<br/>
	**NOTE:** Didn't need to run Antonije's scraper because he already ran it and placed the data in a JSON file. That file needed to be cleaned up, so I did the necessary cleaning manually and with a Python script I wrote.
	
- [x] Study NLP and work on an implementation approach for the National Mottos Generator<br/> 
	**NOTE:** the preliminary work on this has been done, but without direct assistance from someone with intimate NLP knowledge this is going to be an ongoing task for probably another two weekly cycles

- [ ] Push current code for growing the Anthems audio dataset to our GitHub repo

- [ ] Resize SVG symbols that were previously generated. Size needs to be 100x100 pixels. NOTE: For images that are not square reduce the larger side to 100px. 

**Uroš Krčadinac**:

- [ ] add item(s)

**Dušan Pavlović**:

- [ ] Investigate structure of MIDI files
- [ ] Write the script for conversion of midi files to numpy array structure.


___


# Previous tasks (for Archive purposes)

## September 18th - September 24th

**Jacques Laroche**:

 - [x] Finish Growing the Anthems Audio Dataset <br>
	Here is what needs to be done to complete the pipeline:
	- [x] 1) Scrape the following pages:
	https://musescore.com/sheetmusic/soundtrack?page=1 thru /soundtrack?page=100
	- [x] 2) From the Pages in Step 1 save all URLs with the following construction:
	https://musescore.com/user/XXXXXX
	Example: https://musescore.com/user/16006641/scores/4197961
	**NOTE:** Save all these URLs in a TXT or CSV file
	- [x] 3) Write a Python script to go through the file created in Step 2 and extract all the ID numbers (which are the last set of numbers in each URL). Save all these ID numbers to a TXT or CSV file.
	- [x] 4) Write a Python script to correlate ID numbers from the file created in Step 3 to the IPFS hash info within the mscz-files.csv spreadsheet (available at https://musescore-dataset.xmader.com/mscz-files.csv). After finding the IPFS hash for the ID number the script should download the corresponding MSCZ file within a subdirectory named "Soundtrack".
	- [x] 5) Convert all MSCZ files from the "Soundtrack" directory created in Step 5 into MIDI files. **NOTE:
	** Please see https://musescore.org/en/project/batch-convert for details


- [ ] Assist with "National Mottos" dataset task 
	NOTE: https://en.wikipedia.org/wiki/List_of_national_mottos

- [ ] Connect Lab with Igor Popvić (who has an ML research company in Japan)

- [ ] Push current code for growing the Anthems audio dataset to our Github repo

**Miloš Rančić**:

- [ ] Resize all SVGs provided by Jacques to 100x100 pixels. For images that are not square reduce the larger side to 100px. NOTE: Images with instructions will be sent by Jacques via email

**Antonije Petrović**:

- [ ] add item(s)

**Uroš Krčadinac**:

- [ ] add item(s)

**Dušan Pavlović**:

- [ ] Look into the midi file structure.
- [ ] Write the script for conversion of midi files to numpy array structure.
___

## September 11th - September 17th

**Jacques Laroche**:

 - [ ] Finish Growing the Anthems Dataset <br>
	Here is what needs to be done to complete the pipeline:
	- [x] 1) Scrape the following pages:
	https://musescore.com/sheetmusic/soundtrack?page=1 thru /soundtrack?page=100
	- [x] 2) From the Pages in Step 1 save all URLs with the following construction:
	https://musescore.com/user/XXXXXX
	Example: https://musescore.com/user/16006641/scores/4197961
	**NOTE:** Save all these URLs in a TXT or CSV file
	- [x] 3) Write a Python script to go through the file created in Step 2 and extract all the ID numbers (which are the last set of numbers in each URL). Save all these ID numbers to a TXT or CSV file.
	- [ ] 4) Write a Python script to correlate ID numbers from the file created in Step 3 to the IPFS hash info within the mscz-files.csv spreadsheet (available at https://musescore-dataset.xmader.com/mscz-files.csv). After finding the IPFS hash for the ID number the script should download the corresponding MSCZ file within a subdirectory named "Soundtrack".
	- [ ] 5) Convert all MSCZ files from the "Soundtrack" directory created in Step 5 into MIDI files. **NOTE:
	** Please see https://musescore.org/en/project/batch-convert for details



 - [ ] Build / Find a dataset of pictograms / icons

- [ ] Assist with "National Mottos" dataset task 
	NOTE: https://en.wikipedia.org/wiki/List_of_national_mottos


- [x] Add more SVG Symbols that can be used for Flags

___

## August 28th - September 3rd

**Miloš Rančić**:

- [ ] Color semantics
- [ ] Find a way to map the text from the Design section of a flag-related Wiki page onto a particular flag variant layout that we can use for generating (https://www.reddit.com/r/vexillology/comments/agbwrb/flag_variants/)
- [ ] Create Coat of Arms dataset
- [ ] Assist team with text generation of "National Mottos"

**Antonije Petrović**:

- [x] Clean the flags dataset 
- [x] Find out distributions of colors in the flags dataset. Also, find a way to map colors to the most similar color from our color vocabulary. Depends on: color vocabulary for flags by Uroš. 
- [ ] Start working on text generation of mottos (and national anthem lyrics at some point): Find out if is it possible to use existing models, and then "finetune" them for this dataset. Depends on: national mottos dataset
- [ ] Continue learning about RNNs in general

**Uroš Krčadinac**:

- [x] Continue working on a Web app.
- [ ] Create more SVG vector stick-figure pictograms.
- [ ] Be involved with text generation of mottos

**Jacques Laroche**:

- [ ] Finish Growing the Anthems Dataset <br><br>
A way forward has been determined for this task. Below is an outline of the pipeline:
	1. Scrape the following pages:
https://musescore.com/sheetmusic/soundtrack?page=1 thru /soundtrack?page=100

	1. From the Pages in Step 1 save all URLs with the following construction:
https://musescore.com/user/XXXXXX
Example: https://musescore.com/user/16006641/scores/4197961
NOTE: Save all these URLs in a TXT or CSV file

	1. Write a Python script to go through the file created in Step 2 and extract all the ID numbers (which are the last set of numbers in each URL). Save all these ID numbers to a TXT or CSV file.

	1. Write a Python script to go through the file created in Step 3. The script should iterate through each ID number, find the corresponding MSCZ file within the subdirectories of the Bulk MSCZ download, and finally, copy each of these found files placing them in one spot -- preferably a Directory called "Soundtrack".

	1. Convert all MSCZ files from the "Soundtrack" directory created in Step 5 into MIDI files. NOTE: Please see https://musescore.org/en/project/batch-convert for details

- [ ] Continue looking up other ML projects related to the Anthems project and take note of their approach   

- [x] Change our meetings to use Zoom instead of Google Meet
	Status: Completed. The Zoom link is https://us02web.zoom.us/j/85446992747 and I added it to the calendar invitation.

- [ ] Build / Find a dataset of pictograms / icons

- [ ] Assist team with "National Mottos" task (growing dataset, etc.) 	
	NOTE: https://en.wikipedia.org/wiki/List_of_national_mottos

___

## August 14th - August 27th

**Jacques Laroche**:

- [ ] Finish Growing the Anthems Dataset <br><br>
A way forward has been determined for this task. Below is an outline of the pipeline:
	1. Scrape the following pages:
https://musescore.com/sheetmusic/soundtrack?page=1 thru /soundtrack?page=100

	1. From the Pages in Step 1 save all URLs with the following construction:
https://musescore.com/user/XXXXXX
Example: https://musescore.com/user/16006641/scores/4197961
NOTE: Save all these URLs in a TXT or CSV file

	1. Write a Python script to go through the file created in Step 3 and extract all the ID numbers (which are the last set of numbers in each URL). Save all these ID numbers to a TXT or CSV file.

	1. Write a Python script to go through the file created in Step 4. The script should iterate through each ID number, find the corresponding MSCZ file within the subdirectories of the Bulk MSCZ download, and finally, copy each of these found files placing them in one spot -- preferably a Directory called "Soundtrack".

	1. Convert all MSCZ files from the "Soundtrack" directory created in Step 5 into MIDI files. NOTE: Please see https://musescore.org/en/project/batch-convert for details

- [ ] Continue looking up other ML projects related to the Anthems project and take note of their approach   

- [ ] Go through code and add comments

- [x] Add an "Open Questions" Markdown document to our Github repo and inform the team

- [x] Lookup how to use Adobe Illustrator programatically / via command line

    *NOTE*: Illustrator has no CLI interface, but it does accept scripts! I found a script that can batch-convert any file readable by Adobe Illustrator to an SVG. I'm imagining we could batch-convert files from SVG to Raster (either jpg or png) then convert all these Raster files back to SVG with the Adobe Illustrator script mentioned above. The link to the conversion script: https://gist.github.com/seltzered/4405256#file-illustratorsaveassvgs-jsx

- [ ] Build / Find a dataset of pictograms / icons

- [ ] Start thinking about creating a dataset of "National Mottos" for the Flaglabs project. A National Motto is "used to describe the intent or motivation of the state in a short phrase." 	
	NOTE: Great place to start - https://en.wikipedia.org/wiki/List_of_national_mottos
- [ ] (*LOW PRIORITY*) Look up how to train Keras networks on arrays of different sizes

**Antonije Petrovic**:

- [ ] Research about LSTM Autoencoders.
- [ ] Research about RNNs.
- [ ] Consider more ways of SVG feature representation.

**Uroš Krčadinac**:

- [ ] Create more SVG vector stick-figure pictograms.
- [x] Research: generative grammars, expert systems, rule-based systems, procedural generation, etc.

___

## August 6th - August 13th

**Jacques Laroche**:

- [ ] Look up how to train Keras networks on arrays of different sizes

- [ ] [WORKED ON] Grow the Anthems Dataset
   Look up getting Midi files from MuseScore (reference: https://www.tech-gate.org/usa/2021/07/21/audacitys-new-owner-is-in-another-fight-with-the-open-source-community/)
   Status:
    I've identified what Genre and files we could use for training. I then tried to use the Github tools to bulk download Midi files from the MuseScore site that we could use for training. Unfortunately, the tools seem to be a bit lacking and I'm talking to the developer (Xmader) on the project's Discord schannel to see what possible ways forward there are for us.

- [ ] [WORKED ON] Look up other ML projects related to the Anthems project and take note of their approach
   Status:
    Found an article about using audio instead of images as the dataset for a GAN. Link to the piece is below.
    https://towardsdatascience.com/synthesizing-audio-with-generative-adversarial-networks-8e0308184edd
	NOTE: This article got me thinking that maybe we are thinking about things wrong when it comes to using SVGs instead of raster images. SPecifically, perhaps we should be analyzing the SVGs with an NLP algorithm since we are actually dealing with text rather than an image (in the traditional sense).

- [ ] Go through code and add comments

- [x] Add a weekly tasks document and add to Github --> inform team

**Antonije Petrovic**:

- [ ] [WORKED ON] Research about LSTM Autoencoders.
    Status: Tried different basic examples, but nothing too interesting for now.
- [ ] Research about RNNs.
- [ ] [WORKED ON] Consider more ways of SVG feature representation.
    Status: Found yet another way for svg2vector representation. Added a link to the article to our Google Doc. Will research more about this. Maybe we will end up trying out different approaches and in the end we'll see what works best.
    Uroš's comment: Stroke-3 and Stroke-5 models work fine, at least so far. What we actually need is to find what is the right amount of points density.
