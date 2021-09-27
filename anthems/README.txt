Information about this program:
-------------------------------

I wrote this script to download all of the Nation Anthem MIDI files from the website www.midiworld.com.
I haven't really universalized this script, but there are lots of parts that can easily be reused in
other scraping projects.

Please use the requirements.txt file to load all Python Packages necessary to successfully run this script.

A few notes:
------------
> The www.midiworld.com website has a broken SSL certificate. I've coded the scraper to deal with that and ignore the errors.
> The files will download in the same directory you run the script in.
> I've attempted to write the script to be cross-platform, but have only tested it in a Windows environment. It may, or may not work in Linux/OSX.
> The last few National Anthem MIDI files on the www.midiworld.com site are not needed. These seem like extra uploads (page 5 of "National Anthems" on site)


HOW TO USE REQUIREMENTS.TXT:
----------------------------
1) Saving all packages in a requirements.txt file:
pip freeze > requirements.txt

2) Loading packages from a requirements.txt file:
pip install -r requirements.txt
