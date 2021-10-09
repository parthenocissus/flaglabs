from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import json
import pycountry

class Motto:
    def __init__(self, name, entity_type, motto):
        self.entity_name = name
        self.entity_type = entity_type
        self.motto = motto

# Get names of languages from pycountry
languages = [x.name for x in pycountry.languages]

# Date of access: 01.09.2021
url = 'https://en.wikipedia.org/wiki/List_of_national_mottos'
filepath = 'media/mottos/List_of_national_mottos_Wikipedia.html'

def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
    exit()

# Detect language from the text using Google Cloud Translate API.
# Setting up ENV variable is needed in order to use this library.
# Docs: https://cloud.google.com/translate/docs/basic/detecting-language
def detect_language(text):
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    result = translate_client.detect_language(text)
    return result["confidence"], result["language"]


def beautiful_soup_with_existing_page():
    print("Processing offline Wikipedia page")
    with open(filepath, 'rb') as f:
        return BeautifulSoup(f.read(), 'html.parser')

def beautiful_soup_from_url():
    print("Processing the Wikipedia page from URL: " + url)
    html = urlopen(url)
    return BeautifulSoup(html, 'html.parser')

def process_wiki_page(soup):
    mottos_list = []

    # Get the main div class where all the <h2> elements are stored
    main_div = soup.find_all('div', class_="mw-parser-output")[0]
    h2_list = main_div.find_all('h2', recursive=False)

    for h2 in h2_list:
        h2_text = h2.find_next('span').text
        if h2_text == "Notes":
            break

        entity_type = h2_text
        print("####### " + entity_type + " #######")

        # All the <h2> elements and <ul> elements are in the same depth level.
        # Therefore, <ul> elements are siblings of <h2> elements (but so are other <h2> too).
        #
        # We want to iterate over all <ul> between two <h2> elements.
        el_list = h2.next_siblings
        for el in el_list:
            # Break if next <h2> element is found
            if el.name == "h2":
                break
            # Ignore all non <ul> elements
            if el.name != "ul":
                continue

            # We take the <ul> element and extract all <li> elements from it
            li_list = el.find_all('li')
            for li in li_list:
                # Extracting country name before the semicolon
                semicolon_idx = li.text.find(':')
                country = li.text[:semicolon_idx].strip()

                print(country)

                motto = None
                # Extracting the motto
                i_el_list = li.find_all('i', recursive=False)
                if len(i_el_list) == 0 or i_el_list[-1].span == None:
                    motto = li.text[semicolon_idx + 1:].strip()
                else:
                    spans = i_el_list[-1].find_all('span')
                    motto = spans[-1].text.strip()

                # Removing Wikipedia reference numbers i.e. [167]
                motto = re.sub(r'\[(\d|\d\d|\d\d\d)\]', '', motto)

                # Usually motto consists of several parts. 
                # Wikipedia states the motto in several languages, sometimes
                # with information regarding years when it was used, etc.
                motto_left_part = ""
                motto_right_part = ""
                if "(" in motto and ")" in motto:
                    motto_left_part = motto[:motto.index("(")]
                    for lang in languages:
                        if lang + ":" in motto:
                            motto_right_part = motto
                            lang_pos = motto_right_part.index(lang)
                            motto_right_part = motto_right_part[lang_pos + len(lang) + 1:]
                            right_par = motto_right_part.index(")")
                            motto_right_part = motto_right_part[:right_par].strip()
                            break
                else:
                    motto_right_part = motto

                # Removing bunch of different useless characters
                motto_left_part = motto_left_part.strip().strip(".").strip("'").strip("\"")
                motto_right_part = motto_right_part.strip().strip("'").strip("\"")
                
                # Sometimes a country does not have an official motto.
                if "no official motto" in motto_right_part.lower():
                    new_motto = Motto(country, entity_type, motto_right_part)
                    mottos_list.append(new_motto)
                    continue

                # If left part is empty, then motto will be right part.
                # If right part is empty, then motto will be left part.
                # Else, we have to figure out which of the parts is in English
                # and we use that one as a motto.
                new_motto = None
                if motto_left_part == "":
                    new_motto = Motto(country, entity_type, motto_right_part)
                elif motto_right_part == "":
                    new_motto = Motto(country, entity_type, motto_left_part)
                else:
                    left_lang_confidence, left_lang = detect_language(motto_left_part)
                    right_lang_confidence, right_lang = detect_language(motto_right_part)
                    if left_lang == 'en':
                        new_motto = Motto(country, entity_type, motto_left_part)
                    elif right_lang == 'en':
                        new_motto = Motto(country, entity_type, motto_right_part)
                    else:
                        print("-------------------------")
                        print("Left: {}, Right: {}".format(left_lang, right_lang))
                        print(country + " #### Unknown language")
                        print("\t\t" + motto_left_part)
                        print("\t\t" + motto_right_part)
                        new_motto = Motto(country, entity_type, motto_right_part)
                
                mottos_list.append(new_motto)

    return mottos_list


if __name__ == '__main__':
    soup = beautiful_soup_from_url()

    mottos_list = process_wiki_page(soup)

    with open("media/mottos/national-mottos.json", "w", encoding="utf-8") as f_out:
        json.dump(mottos_list, f_out, default=lambda x: x.__dict__, indent=4)