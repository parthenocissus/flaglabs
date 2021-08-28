import json
import svgwrite
import time
from random import choices, random, randint, uniform, randrange
from colour import Color

from bin.gg.flag_layout import FlagLayout
from bin.gg.flag_symbol import FlagSymbol


# _________________________
# Flag Generating Engine
class GenFlag:

    # Constructor
    def __init__(self, width=150, height=100, input_params=None,
                 rules_path='conf/flag-rules.json',
                 symbols_path='conf/flag-symbols.json'):

        # Set the output directory
        out_dir = 'media/svgwrite-output/'
        time_stamp = time.strftime("%Y%m%d-%H%M%S") + "-" + str(time.time() * 1000)
        time_stamp = time_stamp + '-' + str(randint(100, 1000))
        file_name = out_dir + time_stamp + '.svg'

        self.symbols_typical_dir = 'media/svg-flag-symbols/typical/'
        self.symbols_other_dir = 'media/svg-flag-symbols/other/'

        # Set dimensions
        self.size = (width, height)
        self.w = width
        self.h = height

        # Set the empty SVG canvas
        flag_canvas = svgwrite.Drawing(file_name, size=(f'{self.w}px', f'{self.h}px'))

        # Load rules, layouts, colors, and symbols
        self.rules = json.load(open(rules_path))
        symbols = json.load(open(symbols_path))
        self.rules['symbols'] = symbols['symbols']

        # Adjust rules based on input parameters
        if input_params:
            self.apply_input_params(input_params)

        # Create the actual flag using the Flag class
        self.flag = Flag(origin=self, flag_canvas=flag_canvas, rules=self.rules, width=self.w, height=self.h)
        self.flag.draw()

    # Recursively create a flag within a flag (eg. canton flags, such as an Australian flag)
    def create_new_flag(self, origin, canvas, rules, w, h, recursive=True, recursive_level=0):
        return Flag(origin, canvas, rules, w, h, recursive, recursive_level)

    # Get SVG code as string
    def svg_string(self):
        return self.flag.svg_string()

    # Saving the flag into a SVG file
    def save(self):
        self.flag.save()

    # Adjusting rules based on input parameters from the user,
    # parameters that the user set in frontend
    def apply_input_params(self, input_params):
        ruleset = [
            {"key": "layout", "name": "fn"},
            {"key": "special_rules", "name": "name"},
            {"key": "colors", "name": "primary"},
            {"key": "symbols", "name": "name"}
        ]
        for r in ruleset:
            if r['key'] in input_params:
                self.update_weights(input_params, r['key'], r['name'])

    # Updating weights for input parameters
    def update_weights(self, input_params, key, name='name'):
        input_set = input_params[key]
        default = self.rules[key]
        for input_item in input_set:
            for d_item in default:
                if input_item[name] == d_item[name]:
                    d_item['weight'] *= input_item['factor']


# _________________________
# Single Flag
class Flag:

    # Constructor
    def __init__(self, origin, flag_canvas, rules, width, height,
                 recursive=False, recursive_level=0):

        self.genflag_origin = origin
        self.origin_h = origin.h
        self.fc = flag_canvas
        self.rules = rules
        self.w = width
        self.h = height
        self.recursive = recursive
        self.recursive_level = recursive_level
        self.alternating = False
        self.used_colors = []

        scale_baseline = 1 / (2**recursive_level)
        scale_factor = 0.5 * scale_baseline
        self.symbol_data = {
            "pos": (self.w/2, self.h/2),
            "scale": scale_factor,
            "size": self.origin_h * scale_factor,
            "rotate": 0,
            "anchor_position": (self.h/2, self.h/2),
            "scale_baseline": scale_baseline
        }

        # Set layouts and symbols
        self.flag_layout = FlagLayout(self.genflag_origin, self)
        self.flag_symbol = FlagSymbol(self.genflag_origin, self)

        # Select colors and primary color groups
        self.primary_groups, self.colors = self.get_colors()

        # Alternating color picker or just a regular one?
        self.choose_different_color = self.choose_different_color_default
        if random() < self.alternating_colors_chance():
            self.alternating = True
            self.choose_different_color = self.choose_different_color_alt

    # Draw layout
    def draw(self):
        self.flag_layout.draw()
        self.flag_symbol.draw()

    # Get possible colors
    def get_colors(self):
        groups = []
        colors = []
        for primary_group in self.rules['colors']:
            groups.append(primary_group)
            for c in primary_group['variations']:
                colors.append(c)
        return groups, colors

    # Explicitly set a list of used colors
    def set_used_colors(self, colors):
        self.used_colors = colors

    # Calculating chance for alternating color scheme (eg. Greek flag)
    def alternating_colors_chance(self):
        weights_total = 0
        alternating_colors_weight = 0
        for rule in self.rules['special_rules']:
            if rule['name'] == 'alternating_colors':
                alternating_colors_weight = rule['weight']
            weights_total += rule['weight']
        return alternating_colors_weight / weights_total

    # Choose different color every time
    def choose_different_color_default(self):
        if random() > 0.9:
            color = Color(rgb=(random(), random(), random()))
            color_object = {"name": "random", "value": color.get_web()}
            self.used_colors.append(color_object)
            return color_object['value']
        if not self.primary_groups:
            self.primary_groups, self.colors = self.get_colors()
        primary_distribution = [d['weight'] for d in self.primary_groups]
        primary = choices(self.primary_groups, primary_distribution)[0]
        color_distribution = [d['weight'] for d in primary['variations']]
        color = choices(primary['variations'], color_distribution)[0]
        self.primary_groups.remove(primary)
        self.used_colors.append(color)
        return color["value"]

    # Alternating between colors
    def choose_different_color_alt(self):
        self.alternating = True
        if len(self.used_colors) < 2:
            return self.choose_different_color_default()
        else:
            colors_len = len(self.used_colors)
            color = self.used_colors[colors_len - 2]
            self.used_colors.append(color)
            return color["value"]

    # Get SVG code as string
    def svg_string(self):
        return self.fc.tostring()

    # Save flag drawing as SVG
    def save(self):
        self.fc.save()


if __name__ == '__main__':
    for i in range(10):
        input_data = {
            "layout": [
                {"fn": "unicolor", "factor": 100}
            ],
            "colors": [
                {"primary": "red", "factor": 100}
            ],
            "symbols": [
                {"name": "anarchism", "factor": 100}
            ]
        }
        # gf = GenFlag(input_params=input_data)
        gf = GenFlag()
        gf.save()
