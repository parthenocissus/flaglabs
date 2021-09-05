import json
import svgwrite
import time
from random import choices, random, randint, uniform, randrange
from colour import Color

from bin.gg.flag_layout import FlagLayout
from bin.gg.flag_symbol import FlagSymbol
from bin.gg.input_data_utils import InputDataUtil as IDU


# _________________________
# Flag Generating Engine
class GenFlag:

    # Constructor
    def __init__(self, width=150, height=100, input_params=None,
                 raw_input=None, raw=False,
                 rules_path='conf/flag-rules.json',
                 symbols_path='conf/flag-symbols.json'):

        # Set the output directory
        out_dir = 'media/svgwrite-output/'
        time_stamp = time.strftime("%Y%m%d-%H%M%S") + "-" + str(time.time() * 1000)
        time_stamp = time_stamp + '-' + str(randint(100, 1000))
        file_name = out_dir + time_stamp + '.svg'
        self.symbols_typical_dir = 'media/svg-flag-symbols/typical/'
        self.symbols_other_dir = 'media/svg-flag-symbols/other/'
        ponders_path = 'conf/input-ponders.json'

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
        if raw_input and raw:
            ponders = json.load(open(ponders_path))
            iu = IDU(default_rules=self.rules, input_ponders=ponders, raw_input=raw_input)
            self.rules = iu.update_rules()

        # Compute flag complexity
        self.complexity = self.rules['direct_rules']['complexity']

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
        self.choose_different_color = self.choose_different_color_default

        self.symbol_chance = rules['direct_rules']['symbol_chance']
        self.alternating_chance = rules['direct_rules']['alternating_colors_chance']

        # Set rules if rainbow palette
        self.ordered_palette = []
        self.ordered_palette_index = 0
        self.pick_primary_color = self.pick_primary_color_default
        self.rainbow_palette = random() < rules['direct_rules']['rainbow_palette'] * 0.7
        if self.rainbow_palette:
            self.pick_primary_color = self.pick_primary_color_rainbow
            self.ordered_palette = ["red", "orange", "yellow", "green", "blue", "purple", "brown"]
            self.ordered_palette_index = randrange(len(self.ordered_palette))

        # Set symbol data, such as position and scale
        scale_baseline = 1 / (2 ** recursive_level)
        scale_factor = 0.5 * scale_baseline
        self.symbol_data = {
            "pos": (self.w / 2, self.h / 2),
            "scale": scale_factor,
            "size": self.origin_h * scale_factor,
            "rotate": 0,
            "anchor_position": (self.h / 2, self.h / 2),
            "scale_baseline": scale_baseline
        }

        # Set layouts and symbols
        self.flag_layout = FlagLayout(self.genflag_origin, self)
        self.flag_symbol = FlagSymbol(self.genflag_origin, self)

        # Select colors and primary color groups
        self.primary_groups, self.colors = self.get_colors()

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

    # Set a chance for colors to alternate (eg. Greek flag)
    def set_alternating_colors_chance(self, factor=1):
        self.alternating_chance *= factor
        if random() < self.alternating_chance:
            self.alternating = True
            self.choose_different_color = self.choose_different_color_alt

    def pick_primary_color_default(self):
        primary_distribution = [d['weight'] for d in self.primary_groups]
        return choices(self.primary_groups, primary_distribution)[0]

    def pick_primary_color_rainbow(self):
        i = self.ordered_palette_index
        primary_name = self.ordered_palette[i]
        self.ordered_palette_index = 0 if i == len(self.ordered_palette) - 1 else i + 1
        result = [c for c in self.primary_groups if c['name'] == primary_name]
        if len(result) == 0:
            self.primary_groups, self.colors = self.get_colors()
            result = [c for c in self.primary_groups if c['name'] == primary_name]
        return result[0]

    # Choose different color every time
    def choose_different_color_default(self):
        if random() > 0.9 and not self.rainbow_palette:
            color = Color(rgb=(random(), random(), random()))
            color_object = {"name": "random", "value": color.get_web()}
            self.used_colors.append(color_object)
            return color_object['value']
        if not self.primary_groups:
            self.primary_groups, self.colors = self.get_colors()
        primary = self.pick_primary_color()
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
    GenFlag.process_raw_input()
    # for i in range(10):
    #     gf = GenFlag()
    #     gf.save()
