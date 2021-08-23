import json
import svgwrite
import time
import math
import random
from random import choices, random, randint, uniform, randrange
from colour import Color


# _________________________
# Flag Generating Engine
class GenFlag:

    # Constructor
    def __init__(self, width=150, height=100, rules_path='conf/flag-rules.json'):
        # Set the output directory
        out_dir = 'media/svgwrite-output/'
        time_stamp = time.strftime("%Y%m%d-%H%M%S") + "-" + str(time.time() * 1000)
        time_stamp = time_stamp + '-' + str(randint(100, 1000))
        file_name = out_dir + time_stamp + '.svg'

        # Set dimensions
        self.size = (width, height)
        self.w = width
        self.h = height

        # Set the empty SVG canvas
        flag_canvas = svgwrite.Drawing(file_name, size=(f'{self.w}px', f'{self.h}px'))
        rules = json.load(open(rules_path))

        # Create the actual flag using the Flag class
        self.flag = Flag(origin=self, flag_canvas=flag_canvas, rules=rules, width=self.w, height=self.h)
        self.flag.draw()

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
    def __init__(self, origin, flag_canvas, rules, width, height, recursive=False):

        self.genflag_origin = origin
        self.fc = flag_canvas
        self.rules = rules
        self.w = width
        self.h = height
        self.recursive = recursive
        self.alternating = False
        self.used_colors = []
        self.symbol_chance = 0.5
        self.symbol = None

        # Start generating flag elements.
        self.layout = self.select('layout')  # select basic layout
        if "rules" in self.layout:
            self.set_additional_layout_rules(self.layout)

        # Set second layout layer (eg. chevron over the tricolor)
        self.layer2 = self.set_layer2()
        if "rules" in self.layout:
            self.set_additional_layout_rules(self.layout)

        # Set symbol (eg. coat of arms, a circle, a star, etc)
        if random() > self.symbol_chance:
            self.symbol = self.choose_symbol()
        # Select colors and primary color groups
        self.primary_groups, self.colors = self.get_colors()

        # Alternating color picker or just a regular one?
        self.choose_different_color = self.choose_different_color_default
        if random() < self.alternating_colors_chance():
            self.choose_different_color = self.choose_different_color_alt

    # Getting the name of the function
    # from a distribution of possible functions
    # from a ruleset in JSON file
    def select(self, item):
        distribution = [d['weight'] for d in self.rules[item]]
        return choices(self.rules[item], distribution)[0]

    # Draw layout
    def draw(self):
        getattr(self, self.layout['fn'])()
        getattr(self, self.layer2['fn'])()

    # Choose a symbol (eg. coat of arms, a circle, a star, etc)
    def choose_symbol(self):
        distribution = [d['weight'] for d in self.rules['symbols']]
        symbol = choices(self.rules['symbols'], distribution)
        if 'file_name' in symbol:
            # symbol['svg'] =
            pass
        else:
            symbol['svg'] = getattr(self, symbol['name'])()
        return symbol

    # Choose a possible second layer (eg. chevron over the basic layout)
    def set_layer2(self):
        if "layer2" in self.layout:
            possible_layers2 = []
            dist_counter = 0
            for item in self.rules['layout']:
                if item['fn'] in self.layout['layer2']:
                    possible_layers2.append(item)
                else:
                    dist_counter += item['weight']
            possible_layers2.append({'weight': dist_counter, 'fn': 'none'})
            distribution = [item['weight'] for item in possible_layers2]
            return choices(possible_layers2, distribution)[0]
        else:
            return {'fn': 'none'}

    # Set additional layout rules (eg. alternating colors for many-stripes flag)
    def set_additional_layout_rules(self, layout):
        for layout_rule in layout['rules']:
            for base_rule in self.rules['special_rules']:
                # Enforce and empower layout-related rules
                if layout_rule == base_rule['name']:
                    base_rule['weight'] *= 10

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

    # _________________________
    # FLAG LAYOUTS

    # Unicolor
    def unicolor(self):
        c = self.choose_different_color()
        self.fc.add(self.fc.rect((0, 0), (self.w, self.h), stroke='none', fill=c))

    # Horizontal bicolor
    def bicolor_horizontal(self):
        for i in range(2):
            c = self.choose_different_color()
            self.fc.add(self.fc.rect((0, i * self.h / 2), (self.w, self.h / 2), stroke='none', fill=c))

    # Vertical bicolor
    def bicolor_vertical(self):
        for i in range(2):
            c = self.choose_different_color()
            self.fc.add(self.fc.rect((i * self.w / 2, 2), (self.w / 2, self.h), stroke='none', fill=c))

    # Diagonal (left)
    def bicolor_diagonal_left(self):
        d1 = f"M0,{self.h} L{self.w},0 L{self.w},{self.h} z"
        d2 = f"M0,{self.h} L{self.w},0 L0,0 z"
        c1 = self.choose_different_color()
        c2 = self.choose_different_color()
        self.fc.add(self.fc.path(d=d1, stroke='none', fill=c1))
        self.fc.add(self.fc.path(d=d2, stroke='none', fill=c2))

    # Diagonal (left)
    def bicolor_diagonal_right(self):
        d1 = f"M0,0 L{self.w},{self.h} L{self.w},0 z"
        d2 = f"M0,0 L{self.w},{self.h} L0,{self.h} z"
        c1 = self.choose_different_color()
        c2 = self.choose_different_color()
        self.fc.add(self.fc.path(d=d1, stroke='none', fill=c1))
        self.fc.add(self.fc.path(d=d2, stroke='none', fill=c2))

    # Bend (left)
    def bend_left(self):
        if random() > 0.5:
            self.bicolor_diagonal_left()
        else:
            self.unicolor()
        c = self.choose_different_color()
        str_w = uniform(self.h / 10, self.h / 3)
        if random() > 0.2:
            c2 = self.choose_different_color()
            str_w2 = uniform(str_w + self.h / 20, str_w + self.h / 3)
            self.fc.add(self.fc.line((0, self.h), (self.w, 0), stroke=c2, fill='none', stroke_width=str_w2))
        self.fc.add(self.fc.line((0, self.h), (self.w, 0), stroke=c, fill='none', stroke_width=str_w))

    # Bend (right)
    def bend_right(self):
        if random() > 0.5:
            self.bicolor_diagonal_right()
        else:
            self.unicolor()
        c = self.choose_different_color()
        str_w = uniform(self.h / 10, self.h / 3)
        if random() > 0.2:
            c2 = self.choose_different_color()
            str_w2 = uniform(str_w + self.h / 20, str_w + self.h / 3)
            self.fc.add(self.fc.line((0, 0), (self.w, self.h), stroke=c2, fill='none', stroke_width=str_w2))
        self.fc.add(self.fc.line((0, 0), (self.w, self.h), stroke=c, fill='none', stroke_width=str_w))

    # Horizontal tricolor
    def tricolor_horizontal(self):
        for i in range(3):
            c = self.choose_different_color()
            self.fc.add(self.fc.rect((0, i * self.h / 3), (self.w, self.h / 3), stroke='none', fill=c))

    # Vertical tricolor
    def tricolor_vertical(self):
        for i in range(3):
            c = self.choose_different_color()
            self.fc.add(self.fc.rect((i * self.w / 3, 0), (self.w / 3, self.h), stroke='none', fill=c))

    # Horizontal stripes
    def stripes_horizontal(self):
        n_stripes = randint(4, 14)
        for i in range(n_stripes):
            c = self.choose_different_color()
            self.fc.add(self.fc.rect((0, i * self.h / n_stripes), (self.w, self.h / n_stripes),
                                     stroke='none', fill=c))

    # Vertical stripes
    def stripes_vertical(self):
        n_stripes = randint(4, 8)
        for i in range(n_stripes):
            c = self.choose_different_color()
            self.fc.add(self.fc.rect((i * self.w / n_stripes, 0), (self.w / n_stripes, self.h),
                                     stroke='none', fill=c))

    # Checkered
    def checkered(self):
        n_hor = randint(4, 14)
        n_ver = randrange(3, 10, 2)
        for i in range(n_hor):
            for j in range(n_ver):
                c = self.choose_different_color()
                self.fc.add(self.fc.rect((i * self.w / n_hor, j * self.h / n_ver),
                                         (self.w / n_hor, self.h / n_ver),
                                         stroke='none', fill=c))

    # Lozenges
    def lozenges(self):
        n_hor = randint(4, 14)
        n_ver = randrange(3, 10, 2)
        skew_x, skew_y = uniform(10, 30), uniform(10, 30)
        dim_x, dim_y = self.w, self.h
        for i in range(5 * n_hor):
            for j in range(5 * n_ver):
                c = self.choose_different_color()
                x1, x2 = i * dim_x / n_hor, j * dim_y / n_ver
                r_w, r_h = dim_x / n_hor, dim_y / n_ver
                t = f"translate({-2*self.w} {-2*self.h}) skewX({skew_x}) skewY({skew_y})"
                self.fc.add(self.fc.rect((x1, x2), (r_w, r_h), stroke='none', fill=c, transform=t))

    # Sunburst (eg. Macedonian flag)
    def sunburst(self):
        n = randrange(6, 20, 2)
        theta = (2 * math.pi) / n
        offset = 0 if random() < 0.75 else uniform(0, theta)
        r = math.sqrt(self.w*self.w + self.h*self.h)
        r = self.w
        x1, y1 = r * math.sin(offset), r * math.cos(offset)
        for i in range(1, n+1):
            c = self.choose_different_color()
            x2, y2 = r * math.sin(i * theta + offset), r * math.cos(i * theta + offset)
            d = f"M0,0 L{x1},{y1} L{x2},{y2} z"
            t = f"translate({self.w/2}, {self.h/2})"
            self.fc.add(self.fc.path(d=d, stroke='none', fill=c, transform=t))
            x1, y1 = x2, y2

    # Diamond (eg. Brazilian flag)
    def diamond(self):
        self.unicolor()
        c = self.choose_different_color()
        q_y = 5 if self.layer2['fn'] is 'none' else 3
        q_x = 4 if self.layer2['fn'] is 'none' else 2.5
        margin_y = uniform(0, self.h / q_y)
        margin_x = uniform(0, self.h / q_x)
        x1, y1 = self.w / 2, margin_y
        x2, y2 = self.w - margin_x, self.h / 2
        x3, y3 = self.w / 2, self.h - margin_y
        x4, y4 = margin_x, self.h / 2
        d = f"M{x1},{y1} L{x2},{y2} L{x3},{y3} L{x4},{y4} z"
        self.fc.add(self.fc.path(d=d, stroke='none', fill=c))

    # Pale (eg. Canadian flag)
    def pale(self):
        self.unicolor()
        c = self.choose_different_color()
        qoef = uniform(2, 3)
        d = f"M{self.h / qoef},0 L{self.w - self.h / qoef},0 " \
            f"L{self.w - self.h / qoef},{self.h} L{self.h / qoef},{self.h} z"
        self.fc.add(self.fc.path(d=d, stroke='none', fill=c))

    # Chevron (left triangle), also chevronel (hollow chevron with stroke only)
    def chevron(self):
        if self.layer2['fn'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        chevron_w = self.h * math.sqrt(3) / 2
        d = f"M0,0 L{chevron_w},{self.h / 2} L0,{self.h} z"
        stroke = 'none'
        fill = c
        if random() > 0.7:
            d2 = f"M0,0 L{chevron_w},{self.h / 2} L0,{self.h}"
            c2 = self.choose_different_color()
            sw = self.h / uniform(6, 12)
            self.fc.add(self.fc.path(d=d2, stroke=c2, fill='none', stroke_width=sw))
            fill = 'none' if random() > 0.5 else c
        self.fc.add(self.fc.path(d=d, stroke=stroke, fill=fill))

    # Hoist Stripe
    def hoist_stripe(self):
        if self.layer2['fn'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        wid = self.h / uniform(2, 3)
        self.fc.add(self.fc.rect((0, 0), (wid, self.h), stroke='none', fill=c))

    # Fly Stripe
    def fly_stripe(self):
        if self.layer2['fn'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        wid = self.w - (self.h / uniform(2, 3))
        self.fc.add(self.fc.rect((wid, 0), (self.w, self.h), stroke='none', fill=c))

    # Bottom Stripe
    def bottom_stripe(self):
        if self.layer2['fn'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        margin = self.h - (self.h / uniform(2.5, 4))
        self.fc.add(self.fc.rect((0, margin), (self.w, self.h), stroke='none', fill=c))

    # Top Stripe
    def top_stripe(self):
        if self.layer2['fn'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        margin = self.h / uniform(2.5, 4)
        self.fc.add(self.fc.rect((0, 0), (self.w, margin), stroke='none', fill=c))

    # Offset stripes, vertical
    def offset_stripes_vertical(self):
        if self.layer2['fn'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        margin = self.h / uniform(5, 10)
        str_w = self.h / uniform(7, 16)
        self.fc.add(self.fc.line((margin, 0), (margin, self.h), stroke=c, fill='none', stroke_width=str_w))
        self.fc.add(
            self.fc.line((self.w - margin, 0), (self.w - margin, self.h),
                         stroke=c, fill='none', stroke_width=str_w))

    # Offset stripes, horizontal
    def offset_stripes_horizontal(self):
        if self.layer2['fn'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        margin = self.h / uniform(5, 10)
        str_w = self.h / uniform(7, 16)
        self.fc.add(self.fc.line((0, margin), (self.w, margin), stroke=c, fill='none', stroke_width=str_w))
        self.fc.add(self.fc.line((0, self.h - margin), (self.w, self.h - margin),
                                 stroke=c, fill='none', stroke_width=str_w))

    # Canton (upper left recursive flag)
    def canton(self):
        if self.layer2['fn'] is 'none':
            self.unicolor()
        # c = self.choose_different_color()

        # Recursively create another flag for canton (upper left rectangle):
        if self.h > self.genflag_origin.h * 0.25:
            recursive_flag = Flag(self.genflag_origin, self.fc, self.rules,
                                  self.w / 2, self.h / 2, recursive=True)
            if self.alternating and random() > 0.3:
                recursive_flag.set_used_colors(self.used_colors)
                recursive_flag.choose_different_color = recursive_flag.choose_different_color_alt
            recursive_flag.draw()

    # Border (also double border and border without the left hoist side)
    def border(self):
        if self.layer2['fn'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        wid = uniform(self.h / 16, self.h / 6)
        m = wid / 2
        fly = True if random() > 0.8 else False
        left = m if not fly else -m
        right = self.w - 2 * m if not fly else self.w
        if random() > 0.2:
            c2 = self.choose_different_color()
            wid2 = uniform(wid * 2, wid * 2.2)
            m2 = wid2 / 2
            left2 = m2 if not fly else -m2
            right2 = self.w - 2 * m2 if not fly else self.w
            self.fc.add(
                self.fc.rect((left2, m2), (right2, self.h - 2 * m2),
                             stroke=c2, fill='none', stroke_width=wid2))
        self.fc.add(self.fc.rect((left, m), (right, self.h - 2 * m),
                                 stroke=c, fill='none', stroke_width=wid))

    # Cross
    def cross(self):
        self.unicolor()
        c = self.choose_different_color()
        wid = self.h * uniform(0.1, 0.25)
        if random() > 0.75:
            wid2 = uniform(wid * 1.3, wid * 2)
            c2 = self.choose_different_color()
            self.fc.add(self.fc.line((self.w / 2, 0), (self.w / 2, self.h),
                                     stroke=c2, fill='none', stroke_width=wid2))
            self.fc.add(self.fc.line((0, self.h / 2), (self.w, self.h / 2),
                                     stroke=c2, fill='none', stroke_width=wid2))
        self.fc.add(self.fc.line((self.w / 2, 0), (self.w / 2, self.h),
                                 stroke=c, fill='none', stroke_width=wid))
        self.fc.add(self.fc.line((0, self.h / 2), (self.w, self.h / 2),
                                 stroke=c, fill='none', stroke_width=wid))

    # Nordic Cross
    def nordic_cross(self):
        self.unicolor()
        c = self.choose_different_color()
        wid = self.h * uniform(0.1, 0.25)
        if random() > 0.75:
            wid2 = uniform(wid * 1.3, wid * 2)
            c2 = self.choose_different_color()
            self.fc.add(self.fc.line((self.h / 2, 0), (self.h / 2, self.h),
                                     stroke=c2, fill='none', stroke_width=wid2))
            self.fc.add(self.fc.line((0, self.h / 2), (self.w, self.h / 2),
                                     stroke=c2, fill='none', stroke_width=wid2))
        self.fc.add(self.fc.line((self.h / 2, 0), (self.h / 2, self.h),
                                 stroke=c, fill='none', stroke_width=wid))
        self.fc.add(self.fc.line((0, self.h / 2), (self.w, self.h / 2),
                                 stroke=c, fill='none', stroke_width=wid))

    # Canton Cross
    def canton_cross(self):
        self.unicolor()
        c = self.choose_different_color()
        wid = self.h * uniform(0.08, 0.2)
        if random() > 0.75:
            wid2 = uniform(wid * 1.3, wid * 2)
            c2 = self.choose_different_color()
            self.fc.add(self.fc.line((self.h / 3, 0), (self.h / 3, self.h),
                                     stroke=c2, fill='none', stroke_width=wid2))
            self.fc.add(self.fc.line((0, self.h / 3), (self.w, self.h / 3),
                                     stroke=c2, fill='none', stroke_width=wid2))
        self.fc.add(self.fc.line((self.h / 3, 0), (self.h / 3, self.h),
                                 stroke=c, fill='none', stroke_width=wid))
        self.fc.add(self.fc.line((0, self.h / 3), (self.w, self.h / 3),
                                 stroke=c, fill='none', stroke_width=wid))

    # Saltire (X-cross)
    def saltire(self):
        self.unicolor()
        c = self.choose_different_color()
        wid = self.h * uniform(0.1, 0.25)
        if random() > 0.75:
            wid2 = uniform(wid * 1.3, wid * 2)
            c2 = self.choose_different_color()
            self.fc.add(self.fc.line((0, 0), (self.w, self.h),
                                     stroke=c2, fill='none', stroke_width=wid2))
            self.fc.add(self.fc.line((0, self.h), (self.w, 0),
                                     stroke=c2, fill='none', stroke_width=wid2))
        self.fc.add(self.fc.line((0, 0), (self.w, self.h),
                                 stroke=c, fill='none', stroke_width=wid))
        self.fc.add(self.fc.line((0, self.h), (self.w, 0),
                                 stroke=c, fill='none', stroke_width=wid))

    # Cross and saltire (eg. British flag)
    def cross_saltire(self):
        self.unicolor()
        c = self.choose_different_color()  # fill color
        c2 = self.choose_different_color()  # border color (if border)

        border = True if random() > 0.75 else False
        wid_cross = self.h * uniform(0.05, 0.18)
        wid_saltire = wid_cross * uniform(0.6, 0.9)
        wid_cross2 = wid_cross * uniform(1.8, 2.1)
        wid_saltire2 = wid_saltire * uniform(1.8, 2.1)

        # Saltire
        if border:
            self.fc.add(self.fc.line((0, 0), (self.w, self.h),
                                     stroke=c2, fill='none', stroke_width=wid_saltire2))
            self.fc.add(self.fc.line((0, self.h), (self.w, 0),
                                     stroke=c2, fill='none', stroke_width=wid_saltire2))
        self.fc.add(self.fc.line((0, 0), (self.w, self.h),
                                 stroke=c, fill='none', stroke_width=wid_saltire))
        self.fc.add(self.fc.line((0, self.h), (self.w, 0),
                                 stroke=c, fill='none', stroke_width=wid_saltire))
        # Cross
        if border:
            self.fc.add(self.fc.line((self.w / 2, 0), (self.w / 2, self.h),
                                     stroke=c2, fill='none', stroke_width=wid_cross2))
            self.fc.add(self.fc.line((0, self.h / 2), (self.w, self.h / 2),
                                     stroke=c2, fill='none', stroke_width=wid_cross2))
        self.fc.add(self.fc.line((self.w / 2, 0), (self.w / 2, self.h),
                                 stroke=c, fill='none', stroke_width=wid_cross))
        self.fc.add(self.fc.line((0, self.h / 2), (self.w, self.h / 2),
                                 stroke=c, fill='none', stroke_width=wid_cross))

    # Pall (Y-shape flags, eg. South African flag)
    def pall(self):
        if self.layer2['fn'] is 'none':
            if random() > 0.5:
                self.unicolor()
            else:
                c1 = self.choose_different_color()
                c2 = self.choose_different_color()
                c3 = self.choose_different_color()
                self.fc.add(self.fc.rect((0, 0), (self.w, self.h / 2), stroke='none', fill=c1))
                self.fc.add(self.fc.rect((0, self.h / 2), (self.w, self.h), stroke='none', fill=c2))
                d = f"M0,0 L{self.h * math.sqrt(3) / 2},{self.h / 2} L0,{self.h} z"
                self.fc.add(self.fc.path(d=d, stroke='none', fill=c3))
        c = self.choose_different_color()
        c_border = self.choose_different_color()
        wid = self.h * uniform(0.1, 0.25)
        wid_border = wid * uniform(1.8, 2.1)
        chevron_w = self.h * math.sqrt(3) / 2
        d_line = f"M0,0 L{chevron_w},{self.h / 2} L0,{self.h} " \
                 f"L{chevron_w},{self.h / 2} L{self.w},{self.h / 2}"
        if random() > 0.7:
            self.fc.add(self.fc.path(d=d_line, stroke_width=wid_border, stroke=c_border, fill='none'))
            if random() > 0.5:
                c_border2 = self.choose_different_color()
                diff = wid_border - wid
                d_line2 = f"M{-diff},0 L{chevron_w - diff},{self.h / 2} L{-diff},{self.h}"
                self.fc.add(self.fc.path(d=d_line2, stroke_width=diff, stroke=c_border2, fill='none'))
        self.fc.add(self.fc.path(d=d_line, stroke_width=wid, stroke=c, fill='none'))

    # Neutral action
    def none(self):
        pass


if __name__ == '__main__':
    for i in range(40):
        gf = GenFlag()
        gf.save()
