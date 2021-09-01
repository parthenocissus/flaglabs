import math
import copy
from random import choices, random, randint, uniform, randrange

from bin.gg.flag_symbol_config import FlagSymbolConfig


class FlagLayout:

    def __init__(self, origin, flag):
        self.genflag_origin = origin
        self.flag = flag

        self.mask_name = f"mask{flag.recursive_level}"
        self.fc = flag.fc
        self.g = flag.fc.g(clip_path=f"url(#{self.mask_name})")

        self.w = flag.w
        self.h = flag.h
        self.symbol_chance = flag.symbol_chance
        self.original_symbol_chance = copy.copy(flag.symbol_chance)
        self.alternating = flag.alternating
        self.recursive_level = flag.recursive_level
        self.rules = flag.rules
        self.used_colors = flag.used_colors
        self.sd = flag.symbol_data
        self.fsc = FlagSymbolConfig(flag.genflag_origin, flag.symbol_data, self.w, flag.h)

        # Start generating flag elements with the first layer of the layout
        self.layout = self.select('layout')
        # Set second layout layer (eg. chevron over the tricolor)
        self.layer2 = self.set_layer2()

    # Draw layout
    def draw(self):
        clip_path = self.fc.defs.add(self.fc.clipPath(id=self.mask_name))
        clip_path.add(self.fc.rect((0, 0), (self.w, self.h)))
        self.fc.add(self.g)
        getattr(self, self.layout['name'])()
        self.symbol_chance = self.original_symbol_chance
        getattr(self, self.layer2['name'])()

    # Getting the name of the function
    # from a distribution of possible functions
    # from a ruleset in JSON file
    def select(self, item):
        distribution = [d['weight'] for d in self.rules[item]]
        return choices(self.rules[item], distribution)[0]

    # Choose a color
    def choose_different_color(self):
        return self.flag.choose_different_color()

    # Choose a possible second layer (eg. chevron over the basic layout)
    def set_layer2(self):
        if "layer2" in self.layout:
            possible_layers2 = []
            dist_counter = 0
            for item in self.rules['layout']:
                if item['name'] in self.layout['layer2']:
                    possible_layers2.append(item)
                else:
                    dist_counter += item['weight']
            possible_layers2.append({'weight': dist_counter, 'name': 'none'})
            distribution = [item['weight'] for item in possible_layers2]
            return choices(possible_layers2, distribution)[0]
        else:
            return {'name': 'none'}


    # _________________________
    # FLAG LAYOUTS

    # Unicolor
    def unicolor(self):
        c = self.choose_different_color()
        self.g.add(self.fc.rect((0, 0), (self.w, self.h), stroke='none', fill=c))
        self.fsc.default_center_center_left()
        self.symbol_chance *= 1.95

    # Horizontal bicolor
    def bicolor_horizontal(self):
        for i in range(2):
            c = self.choose_different_color()
            self.g.add(self.fc.rect((0, i * self.h / 2), (self.w, self.h / 2), stroke='none', fill=c))
        self.fsc.default_center_center_left()
        self.symbol_chance *= 1.4

    # Vertical bicolor
    def bicolor_vertical(self):
        for i in range(2):
            c = self.choose_different_color()
            self.g.add(self.fc.rect((i * self.w / 2, 2), (self.w / 2, self.h), stroke='none', fill=c))
        self.fsc.center(scale_factor=uniform(0.4, 0.7))
        self.symbol_chance *= 1.4

    # Diagonal (left)
    def bicolor_diagonal_left(self):
        d1 = f"M0,{self.h} L{self.w},0 L{self.w},{self.h} z"
        d2 = f"M0,{self.h} L{self.w},0 L0,0 z"
        c1 = self.choose_different_color()
        c2 = self.choose_different_color()
        self.g.add(self.fc.path(d=d1, stroke='none', fill=c1))
        self.g.add(self.fc.path(d=d2, stroke='none', fill=c2))
        self.fsc.default_center_canton_small()

    # Diagonal (right)
    def bicolor_diagonal_right(self):
        d1 = f"M0,0 L{self.w},{self.h} L{self.w},0 z"
        d2 = f"M0,0 L{self.w},{self.h} L0,{self.h} z"
        c1 = self.choose_different_color()
        c2 = self.choose_different_color()
        self.g.add(self.fc.path(d=d1, stroke='none', fill=c2))
        self.g.add(self.fc.path(d=d2, stroke='none', fill=c1))
        self.fsc.center(scale_factor=uniform(0.4, 0.7))

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
            self.g.add(self.fc.line((0, self.h), (self.w, 0), stroke=c2, fill='none', stroke_width=str_w2))
        self.g.add(self.fc.line((0, self.h), (self.w, 0), stroke=c, fill='none', stroke_width=str_w))
        self.fsc.default_center_canton_small()

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
            self.g.add(self.fc.line((0, 0), (self.w, self.h), stroke=c2, fill='none', stroke_width=str_w2))
        self.g.add(self.fc.line((0, 0), (self.w, self.h), stroke=c, fill='none', stroke_width=str_w))
        size_ratio = str_w / self.h
        self.fsc.center(scale_factor=uniform(0.4, 0.7))

    # Horizontal tricolor
    def tricolor_horizontal(self):
        for i in range(3):
            c = self.choose_different_color()
            self.g.add(self.fc.rect((0, i * self.h / 3), (self.w, self.h / 3), stroke='none', fill=c))
        self.fsc.default_center_center_left()
        self.symbol_chance *= 1.4

    # Vertical tricolor
    def tricolor_vertical(self):
        for i in range(3):
            c = self.choose_different_color()
            self.g.add(self.fc.rect((i * self.w / 3, 0), (self.w / 3, self.h), stroke='none', fill=c))
        self.fsc.center(scale_factor=uniform(0.4, 0.7))
        self.symbol_chance *= 1.4

    # Horizontal stripes
    def stripes_horizontal(self):
        self.flag.set_alternating_colors_chance(factor=4.5)
        n_stripes = randint(4, 14)
        for i in range(n_stripes):
            c = self.choose_different_color()
            self.g.add(self.fc.rect((0, i * self.h / n_stripes), (self.w, self.h / n_stripes),
                                     stroke='none', fill=c))
        self.fsc.default_center_center_left()
        self.symbol_chance *= 1.2

    # Vertical stripes
    def stripes_vertical(self):
        self.flag.set_alternating_colors_chance(factor=4.5)
        n_stripes = randint(4, 8)
        for i in range(n_stripes):
            c = self.choose_different_color()
            self.g.add(self.fc.rect((i * self.w / n_stripes, 0), (self.w / n_stripes, self.h),
                                     stroke='none', fill=c))
        self.fsc.center(scale_factor=uniform(0.4, 0.7))
        self.symbol_chance *= 1.2

    # Checkered
    def checkered(self):
        self.flag.set_alternating_colors_chance(factor=4.5)
        n_hor = randint(4, 14)
        n_ver = randrange(3, 10, 2)
        for i in range(n_hor):
            for j in range(n_ver):
                c = self.choose_different_color()
                self.g.add(self.fc.rect((i * self.w / n_hor, j * self.h / n_ver),
                                         (self.w / n_hor, self.h / n_ver),
                                         stroke='none', fill=c))
        self.fsc.center(scale_factor=uniform(0.4, 0.7))
        self.symbol_chance *= 1.2

    # Lozenges
    def lozenges(self):
        self.flag.set_alternating_colors_chance(factor=4.5)
        n_hor = randint(4, 10)
        n_ver = randrange(3, 8, 2)
        skew_x, skew_y = uniform(10, 30), uniform(10, 30)
        dim_x, dim_y = self.w, self.h
        for i in range(5 * n_hor):
            for j in range(5 * n_ver):
                c = self.choose_different_color()
                x1, x2 = i * dim_x / n_hor, j * dim_y / n_ver
                r_w, r_h = dim_x / n_hor, dim_y / n_ver
                t = f"translate({-4 * self.w} {-4 * self.h}) skewX({skew_x}) skewY({skew_y})"
                self.g.add(self.fc.rect((x1, x2), (r_w, r_h), stroke='none', fill=c, transform=t))
        self.fsc.center(scale_factor=uniform(0.4, 0.7))
        self.symbol_chance *= 1.2

    # Sunburst (eg. Macedonian flag)
    def sunburst(self):
        self.flag.set_alternating_colors_chance(factor=4.5)
        n = randrange(6, 20, 2)
        theta = (2 * math.pi) / n
        offset = 0 if random() < 0.75 else uniform(0, theta)
        r = self.w
        x1, y1 = r * math.sin(offset), r * math.cos(offset)
        for i in range(1, n + 1):
            c = self.choose_different_color()
            x2, y2 = r * math.sin(i * theta + offset), r * math.cos(i * theta + offset)
            d = f"M0,0 L{x1},{y1} L{x2},{y2} z"
            t = f"translate({self.w / 2}, {self.h / 2})"
            self.g.add(self.fc.path(d=d, stroke='none', fill=c, transform=t))
            x1, y1 = x2, y2
        self.fsc.center(scale_factor=uniform(0.4, 0.7))
        self.symbol_chance *= 1.4

    # Diamond (eg. Brazilian flag)
    def diamond(self):
        self.unicolor()
        c = self.choose_different_color()
        q_y = 5 if self.layer2['name'] is 'none' else 3
        q_x = 4 if self.layer2['name'] is 'none' else 2.5
        margin_y = uniform(0, self.h / q_y)
        margin_x = uniform(0, self.h / q_x)
        x1, y1 = self.w / 2, margin_y
        x2, y2 = self.w - margin_x, self.h / 2
        x3, y3 = self.w / 2, self.h - margin_y
        x4, y4 = margin_x, self.h / 2
        d = f"M{x1},{y1} L{x2},{y2} L{x3},{y3} L{x4},{y4} z"
        self.g.add(self.fc.path(d=d, stroke='none', fill=c))
        self.fsc.center(scale_factor=uniform(0.2, 0.4))
        self.symbol_chance *= 1.6

    # Pale (eg. Canadian flag)
    def pale(self):
        self.unicolor()
        c = self.choose_different_color()
        qoef = uniform(2, 3)
        d = f"M{self.h / qoef},0 L{self.w - self.h / qoef},0 " \
            f"L{self.w - self.h / qoef},{self.h} L{self.h / qoef},{self.h} z"
        self.g.add(self.fc.path(d=d, stroke='none', fill=c))
        self.fsc.center(scale_factor=uniform(0.4, 0.7))
        self.symbol_chance *= 1.6

    # Chevron (left triangle), also chevronel (hollow chevron with stroke only)
    def chevron(self):
        if self.layer2['name'] is 'none':
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
            self.g.add(self.fc.path(d=d2, stroke=c2, fill='none', stroke_width=sw))
            fill = 'none' if random() > 0.5 else c
        self.g.add(self.fc.path(d=d, stroke=stroke, fill=fill))
        self.fsc.default_left_or_right()
        self.symbol_chance *= 1.4

    # Hoist Stripe
    def hoist_stripe(self):
        if self.layer2['name'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        wid = self.h / uniform(2, 3)
        self.g.add(self.fc.rect((0, 0), (wid, self.h), stroke='none', fill=c))
        wf = (wid + (self.w - wid)/2) / self.w
        self.fsc.center_right(scale_factor=uniform(0.4, 0.7), width_fraction=wf)
        self.symbol_chance *= 1.6

    # Fly Stripe
    def fly_stripe(self):
        if self.layer2['name'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        wid = self.w - (self.h / uniform(2, 3))
        self.g.add(self.fc.rect((wid, 0), (self.w, self.h), stroke='none', fill=c))
        wf = wid / self.w / 2
        self.fsc.center_right(scale_factor=uniform(0.4, 0.7), width_fraction=wf)
        self.symbol_chance *= 1.7

    # Bottom Stripe
    def bottom_stripe(self):
        if self.layer2['name'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        margin = self.h - (self.h / uniform(2.5, 4))
        self.g.add(self.fc.rect((0, margin), (self.w, self.h), stroke='none', fill=c))
        hf = (margin / self.h) / 2
        sf = 2 * hf * uniform(0.4, 0.6)
        self.fsc.center_down(scale_factor=sf, height_fraction=hf)
        self.symbol_chance *= 1.7

    # Top Stripe
    def top_stripe(self):
        if self.layer2['name'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        margin = self.h / uniform(2.5, 4)
        self.g.add(self.fc.rect((0, 0), (self.w, margin), stroke='none', fill=c))
        hf = (margin + (self.h - margin) / 2) / self.h
        sf = uniform(0.3, 0.6)
        cd = (margin / self.h) / 2
        self.fsc.default_canton_center_down(scale_factor=sf, height_fraction=hf,
                                                      canton_dim=cd)
        self.symbol_chance *= 1.7

    # Offset stripes, vertical
    def offset_stripes_vertical(self):
        if self.layer2['name'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        margin = self.h / uniform(5, 10)
        str_w = self.h / uniform(7, 16)
        self.g.add(self.fc.line((margin, 0), (margin, self.h), stroke=c, fill='none', stroke_width=str_w))
        self.g.add(
            self.fc.line((self.w - margin, 0), (self.w - margin, self.h),
                         stroke=c, fill='none', stroke_width=str_w))
        self.fsc.center(scale_factor=uniform(0.3, 0.6))
        self.symbol_chance *= 1.6

    # Offset stripes, horizontal
    def offset_stripes_horizontal(self):
        if self.layer2['name'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        margin = self.h / uniform(5, 10)
        str_w = self.h / uniform(7, 16)
        self.g.add(self.fc.line((0, margin), (self.w, margin), stroke=c, fill='none', stroke_width=str_w))
        self.g.add(self.fc.line((0, self.h - margin), (self.w, self.h - margin),
                                 stroke=c, fill='none', stroke_width=str_w))
        self.fsc.default_center_center_left()
        self.symbol_chance *= 1.6

    # Canton (upper left recursive flag)
    def canton(self):
        if self.layer2['name'] is 'none':
            self.unicolor()
        self.fsc.center_right(scale_factor=uniform(0.4, 0.55), width_fraction=0.75)
        self.symbol_chance *= 1.2
        # Recursively create another flag for canton (upper left rectangle):
        if self.h > self.genflag_origin.h * 0.25:
            meta_lvl = self.recursive_level + 1
            recursive_flag = self.genflag_origin.create_new_flag(self.genflag_origin,
                                                                 self.fc, self.rules,
                                                                 self.w / 2, self.h / 2,
                                                                 recursive=True,
                                                                 recursive_level=meta_lvl)
            if self.alternating and random() > 0.3:
                recursive_flag.set_used_colors(self.used_colors)
                recursive_flag.choose_different_color = recursive_flag.choose_different_color_alt
            recursive_flag.draw()

    # Border (also double border and border without the left hoist side)
    def border(self):
        if self.layer2['name'] is 'none':
            self.unicolor()
        c = self.choose_different_color()
        wid = uniform(self.h / 16, self.h / 6)
        space = wid*2
        m = wid / 2
        fly = True if random() > 0.1 else False
        left = m if not fly else -m
        right = self.w - 2 * m if not fly else self.w
        if random() > 0.2:
            c2 = self.choose_different_color()
            wid2 = uniform(wid * 2, wid * 2.2)
            space = wid2 * 2
            m2 = wid2 / 2
            left2 = m2 if not fly else -m2
            right2 = self.w - 2 * m2 if not fly else self.w
            self.g.add(
                self.fc.rect((left2, m2), (right2, self.h - 2 * m2),
                             stroke=c2, fill='none', stroke_width=wid2))
        self.g.add(self.fc.rect((left, m), (right, self.h - 2 * m),
                                 stroke=c, fill='none', stroke_width=wid))
        # scale_factor = uniform(0.7, 1) * (space / self.h)
        if fly:
            self.fsc.default_center_center_left(scale_factor=uniform(0.3, 0.6))
        else:
            self.fsc.center(scale_factor=uniform(0.3, 0.6))
        self.symbol_chance *= 1.5

    # Cross
    def cross(self):
        self.unicolor()
        c = self.choose_different_color()
        wid = self.h * uniform(0.1, 0.25)
        if random() > 0.75:
            wid2 = uniform(wid * 1.3, wid * 2)
            c2 = self.choose_different_color()
            self.g.add(self.fc.line((self.w / 2, 0), (self.w / 2, self.h),
                                     stroke=c2, fill='none', stroke_width=wid2))
            self.g.add(self.fc.line((0, self.h / 2), (self.w, self.h / 2),
                                     stroke=c2, fill='none', stroke_width=wid2))
        self.g.add(self.fc.line((self.w / 2, 0), (self.w / 2, self.h),
                                 stroke=c, fill='none', stroke_width=wid))
        self.g.add(self.fc.line((0, self.h / 2), (self.w, self.h / 2),
                                 stroke=c, fill='none', stroke_width=wid))
        self.fsc.center(scale_factor=uniform(0.1, 0.7))
        self.symbol_chance *= 0.8

    # Nordic Cross
    def nordic_cross(self):
        self.unicolor()
        c = self.choose_different_color()
        wid = self.h * uniform(0.1, 0.25)
        if random() > 0.75:
            wid2 = uniform(wid * 1.3, wid * 2)
            c2 = self.choose_different_color()
            self.g.add(self.fc.line((self.h / 2, 0), (self.h / 2, self.h),
                                     stroke=c2, fill='none', stroke_width=wid2))
            self.g.add(self.fc.line((0, self.h / 2), (self.w, self.h / 2),
                                     stroke=c2, fill='none', stroke_width=wid2))
        self.g.add(self.fc.line((self.h / 2, 0), (self.h / 2, self.h),
                                 stroke=c, fill='none', stroke_width=wid))
        self.g.add(self.fc.line((0, self.h / 2), (self.w, self.h / 2),
                                 stroke=c, fill='none', stroke_width=wid))
        sf = uniform(0.1, 0.6)
        wf = (self.h/2) / self.w
        self.fsc.center_left(scale_factor=sf, width_fraction=wf)
        self.symbol_chance *= 0.6

    # Canton Cross
    def canton_cross(self):
        self.unicolor()
        c = self.choose_different_color()
        wid = self.h * uniform(0.08, 0.2)
        if random() > 0.75:
            wid2 = uniform(wid * 1.3, wid * 2)
            c2 = self.choose_different_color()
            self.g.add(self.fc.line((self.h / 3, 0), (self.h / 3, self.h),
                                     stroke=c2, fill='none', stroke_width=wid2))
            self.g.add(self.fc.line((0, self.h / 3), (self.w, self.h / 3),
                                     stroke=c2, fill='none', stroke_width=wid2))
        self.g.add(self.fc.line((self.h / 3, 0), (self.h / 3, self.h),
                                 stroke=c, fill='none', stroke_width=wid))
        self.g.add(self.fc.line((0, self.h / 3), (self.w, self.h / 3),
                                 stroke=c, fill='none', stroke_width=wid))
        self.fsc.canton_small(scale_factor=uniform(0.2, 0.33), dim=(1/3, 1/3))
        self.symbol_chance *= 0.6

    # Saltire (X-cross)
    def saltire(self):
        self.unicolor()
        c = self.choose_different_color()
        wid = self.h * uniform(0.1, 0.25)
        if random() > 0.75:
            wid2 = uniform(wid * 1.3, wid * 2)
            c2 = self.choose_different_color()
            self.g.add(self.fc.line((0, 0), (self.w, self.h),
                                     stroke=c2, fill='none', stroke_width=wid2))
            self.g.add(self.fc.line((0, self.h), (self.w, 0),
                                     stroke=c2, fill='none', stroke_width=wid2))
        self.g.add(self.fc.line((0, 0), (self.w, self.h),
                                 stroke=c, fill='none', stroke_width=wid))
        self.g.add(self.fc.line((0, self.h), (self.w, 0),
                                 stroke=c, fill='none', stroke_width=wid))
        self.fsc.center(scale_factor=uniform(0.1, 0.7))
        self.symbol_chance *= 0.6

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
            self.g.add(self.fc.line((0, 0), (self.w, self.h),
                                     stroke=c2, fill='none', stroke_width=wid_saltire2))
            self.g.add(self.fc.line((0, self.h), (self.w, 0),
                                     stroke=c2, fill='none', stroke_width=wid_saltire2))
        self.g.add(self.fc.line((0, 0), (self.w, self.h),
                                 stroke=c, fill='none', stroke_width=wid_saltire))
        self.g.add(self.fc.line((0, self.h), (self.w, 0),
                                 stroke=c, fill='none', stroke_width=wid_saltire))
        # Cross
        if border:
            self.g.add(self.fc.line((self.w / 2, 0), (self.w / 2, self.h),
                                     stroke=c2, fill='none', stroke_width=wid_cross2))
            self.g.add(self.fc.line((0, self.h / 2), (self.w, self.h / 2),
                                     stroke=c2, fill='none', stroke_width=wid_cross2))
        self.g.add(self.fc.line((self.w / 2, 0), (self.w / 2, self.h),
                                 stroke=c, fill='none', stroke_width=wid_cross))
        self.g.add(self.fc.line((0, self.h / 2), (self.w, self.h / 2),
                                 stroke=c, fill='none', stroke_width=wid_cross))
        self.fsc.center(scale_factor=uniform(0.1, 0.7))
        self.symbol_chance *= 0.6

    # Pall (Y-shape flags, eg. South African flag)
    def pall(self):
        if self.layer2['name'] is 'none':
            if random() > 0.5:
                self.unicolor()
            else:
                c1 = self.choose_different_color()
                c2 = self.choose_different_color()
                c3 = self.choose_different_color()
                self.g.add(self.fc.rect((0, 0), (self.w, self.h / 2), stroke='none', fill=c1))
                self.g.add(self.fc.rect((0, self.h / 2), (self.w, self.h), stroke='none', fill=c2))
                d = f"M0,0 L{self.h * math.sqrt(3) / 2},{self.h / 2} L0,{self.h} z"
                self.g.add(self.fc.path(d=d, stroke='none', fill=c3))
        c = self.choose_different_color()
        c_border = self.choose_different_color()
        wid = self.h * uniform(0.1, 0.25)
        wid_border = wid * uniform(1.8, 2.1)
        chevron_w = self.h * math.sqrt(3) / 2
        d_line = f"M0,0 L{chevron_w},{self.h / 2} L0,{self.h} " \
                 f"L{chevron_w},{self.h / 2} L{self.w},{self.h / 2}"
        if random() > 0.7:
            self.g.add(self.fc.path(d=d_line, stroke_width=wid_border, stroke=c_border, fill='none'))
            if random() > 0.5:
                c_border2 = self.choose_different_color()
                diff = wid_border - wid
                d_line2 = f"M{-diff},0 L{chevron_w - diff},{self.h / 2} L{-diff},{self.h}"
                self.g.add(self.fc.path(d=d_line2, stroke_width=diff, stroke=c_border2, fill='none'))
        self.g.add(self.fc.path(d=d_line, stroke_width=wid, stroke=c, fill='none'))
        scale_left = uniform(0.2, 0.3)
        self.fsc.center_left(scale_factor=scale_left, width_fraction=0.13)
        self.symbol_chance *= 0.8

    # Neutral action
    def none(self):
        pass
