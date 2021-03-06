import svgutils.transform as sg
import sys
from svgpathtools import svg2paths, svg2paths2, wsvg
from xml.etree import ElementTree as ET
from lxml import etree

def xml_test_read_only():
    tree = ET.parse('media/tmp/symbol2.svg')
    root = tree.getroot()
    for item in root:
        if 'd' in item.attrib:
            print(f"\n{item.attrib['d']}")
            if 'fill' in item.attrib:
                print(item.attrib['fill'])
            if 'stroke' in item.attrib:
                print(item.attrib['stroke'])

def xml_test():

    flag_tree = ET.parse('media/tmp/flag.svg')
    flag_root = flag_tree.getroot()
    # for item in root_flag:
    #     print(item.attrib)

    symbol_tree = ET.parse('media/tmp/symbol.svg')
    symbol_root = symbol_tree.getroot()

    flag_svg = flag_root.find('svg')
    symbol_svg = symbol_root.find('svg')
    # added = ET.SubElement(fleur_svg)

    for element in symbol_tree.iter('svg'):
        print(element)
        print(element.attrib)
        flag_svg.append(element)

    # fleur_svg.insert(0, root_flag)

    flag_tree.write("media/tmp/final.svg")

def svgutils_test():

    #create a new SVG figure
    fig = sg.SVGFigure()
    fig.set_size(("150px", "100px"))

    # load figures
    flag = sg.fromfile('media/tmp/flag.svg')
    symbol = sg.fromfile('media/tmp/symbol.svg')

    # get the plot objects
    flag_root = flag.getroot()
    symbol_root = symbol.getroot()

    for item in symbol_root:
        print(item)

    # symbol_root.scale(0.5)
    # symbol_root.moveto(50, 25)
    # symbol.attrib['fill'] = 'blue'
    # print(symbol_root)

def svgpathtools_test():
    f1 = 'media/tmp/flag.svg'
    f2 = 'media/tmp/symbol.svg'
    f3 = 'media/tmp/final.svg'
    paths1, attributes1, svg_attributes1 = svg2paths2(f1)
    # wsvg(paths1, attributes=attributes1, svg_attributes=svg_attributes1, filename=f3)
    wsvg(paths1, attributes=attributes1, filename=f3)

def svgpathtools_test():
    f1 = 'media/tmp/flag.svg'
    f2 = 'media/tmp/symbol.svg'
    f3 = 'media/tmp/final.svg'
    paths1, attributes1, svg_attributes1 = svg2paths2(f2)
    # wsvg(paths1, attributes=attributes1, svg_attributes=svg_attributes1, filename=f3)
    for p in paths1:
        print(p.d())

svgpathtools_test()
# svgutils_test()
# xml_test()
# xml_test_read_only()