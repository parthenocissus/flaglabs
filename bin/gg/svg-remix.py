"""
Napraviti Python funkciju koja učita 2 SVG fajla, zastavu i grb,
promeni boje grba, stavi grb preko zastave,
i novu grafiku sačuva kao novi SVG fajl. Precizno:

___
1. Učitati fajlove:

media/tmp/flag.svg (zastava dimenzija 150x100)
media/tmp/symbol.svg (grb dimenzija 100x100)

2. Uzeti kompletan sadržaj SVG taga iz fajla symbol.svg.
U trenutnom primeru to je jedan path koji opisuje oblik
ljiljana (fleur-de-lis), koji se koristi na raznim grbovima i zastavama
(ima ga i na srpskom grbu, ispod orlova, kao i na grbu Kvebeka, itd.)

3. Promeniti boju grba.

4. Otvoriti fajl flag.svg i grb staviti preko zastave.

5. Omogućiti pozicioniranje, skaliranje i dupliranje grba.
Tako da recimo smanjen grb bude u gornjem levom uglu,
ili da preko zastave idu 3 ista grba u redu.

6. Sačuvati novu grafiku kao SVG fajl.

___
SVG format u osnovi je XML format, tako da se mogu koristiti i generičke
Python biblioteke za XML, samo ne znam da li je to optimalno rešenje.
Python Biblioteke koje sam dosad koristio su:

svgwrite
svgutils
svgpathtools
drawSvg
xml.etree.ElementTree

"""

def svg_remix():

    flag_path = "media/tmp/flag.svg"  # zastava dimenzija 150x100
    symbol_path = "media/tmp/symbol.svg"  # grb dimenzija 100x100
    output_path = "media/tmp/final.svg"

    # ...
    pass