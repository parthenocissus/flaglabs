import math
from random import choices, random, randint, uniform, randrange
from svgpathtools import svg2paths, svg2paths2, wsvg
from xml.etree import ElementTree as ET


class FlagSymbol:

    def __init__(self, origin, flag):
        self.genflag_origin = origin
        self.flag = flag
        self.fc = flag.fc
        self.w = flag.w
        self.h = flag.h

        self.rules = flag.rules
        self.used_colors = flag.used_colors

        self.symbols = self.rules['symbols']
        self.symbol_chance = 0.25
        self.symbol = None
        self.build_symbol = None

        # Set symbol (eg. coat of arms, a circle, a star, etc)
        if random() < self.symbol_chance:
            self.symbol = self.choose_symbol()
            # Alternating color fix
            if flag.alternating:
                self.flag.choose_different_color = self.flag.choose_different_color_default
                self.flag.alternating = False
        else:
            self.build_symbol = self.empty_symbol
            # self.symbol = self.empty_symbol()

    # Draw symbol
    def draw(self):
        symbol = self.build_symbol()
        self.fc.add(symbol)

    # Choose a color
    def choose_different_color(self):
        return self.flag.choose_different_color()

    # Build symbol from paths taken from a SVG file
    def build_symbol_from_paths(self):
        d = FlagSymbol.center_symbol(self.flag.symbol_data)
        return self.paths2symbol(d['pos'], d['scale'], d['rotate'], d['anchor_position'])

    # Recenter the symbol
    @staticmethod
    def center_symbol(symbol_data):
        x, y = symbol_data['pos']
        symbol_data['pos'] = (x - symbol_data['size'] / 2, y - symbol_data['size'] / 2)
        return symbol_data

    # Create a single symbol from paths and put it in a group (<g> element)
    def paths2symbol(self, position=(0, 0), scale=1,
                     rotation_angle=0, anchor_position=(50, 50)):
        x, y = position
        anchor_x, anchor_y = anchor_position
        t = f"translate({x}, {y}) scale({scale}) rotate({rotation_angle}, {anchor_x}, {anchor_y})"
        c = self.choose_different_color()
        group = self.fc.g(transform=t)
        for path in self.symbol['paths']:
            svg_path = self.fc.path(d=path['d'], fill=c, stroke='none')
            group.add(svg_path)
        return group

    # Choose a symbol (eg. coat of arms, a circle, a star, etc)
    def choose_symbol(self):
        distribution = [d['weight'] for d in self.rules['symbols']]
        symbol = choices(self.rules['symbols'], distribution)[0]
        if 'file_name' in symbol:
            try:
                symbol['paths'] = self.get_svg_paths(symbol['file_name'])
                self.build_symbol = self.build_symbol_from_paths
            except:
                print(symbol['file_name'])
        else:
            self.build_symbol = getattr(self, symbol['name'])
        return symbol

    # Empty symbol
    def empty_symbol(self):
        return self.fc.circle(center=(-1, -1), r=0, fill='none', stroke='none')

    # Open a SVG file and get all path-related data
    def get_svg_paths(self, file_name):

        path = f"{self.genflag_origin.symbols_typical_dir}{file_name}.svg"
        path_data = []

        # tree = ET.parse(path)
        # root = tree.getroot()
        # path_data = []
        # for item in root:
        #     if 'd' in item.attrib:
        #         path_object = {'d': item.attrib['d']}
        #         if 'fill' in item.attrib:
        #             path_object['fill'] = item.attrib['fill']
        #         if 'stroke' in item.attrib:
        #             path_object['stroke'] = item.attrib['stroke']
        #         path_data.append(path_object)

        paths, attrs, svg_attrs = svg2paths2(path)
        for p, a in zip(paths, attrs):
            path_object = {'d': p.d()}
            if 'fill' in a:
                path_object['fill'] = a['fill']
            if 'stroke' in a:
                path_object['stroke'] = a['stroke']
            path_data.append(path_object)
        return path_data

    # _________________________
    # SYMBOL DRAWING METHODS

    # Circle
    def circle(self):
        d = self.flag.symbol_data
        c = self.choose_different_color()
        return self.fc.circle(center=d['pos'], r=d['size'] * 0.4, fill=c, stroke='none')

    # Random Star
    def random_star(self):
        d = self.flag.symbol_data
        c = self.choose_different_color()
        n = randint(5, 10)
        x, y = d['pos']
        rad1 = d['size'] / 2
        rad2 = rad1 * uniform(0.3, 0.9)
        angle = 2 * math.pi / n
        half_angle = angle / 2
        path_d = ""
        letter = "M"
        for i in range(n):
            a1 = angle * i
            a2 = a1 + half_angle
            x1, y1 = x + math.cos(a1) * rad1, y + math.sin(a1) * rad1
            x2, y2 = x + math.cos(a2) * rad2, y + math.sin(a2) * rad2
            path_d += f"{letter} {x1} {y1} L {x2} {y2} "
            letter = "L"
        path_d += "z"
        path = self.fc.path(d=path_d, fill=c, stroke='none')
        return path
