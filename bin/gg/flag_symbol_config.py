import math
import copy
from random import choices, random, randint, uniform, randrange


# _____________________________________________________
# Class for defining the position of a symbol on a flag
# Mostly used by layout functions
class FlagSymbolConfig:

    def __init__(self, origin, engine, w, h):
        self.sd = engine.symbol_data
        self.origin_h = origin.h
        self.engine = engine
        self.scale_baseline = engine.symbol_data['scale_baseline']
        self.w, self.h = w, h

    # Symbol data deepcopy
    def symbol_data_copy(self):
        return copy.deepcopy(self.sd)

    # Scaling the symbol
    def scale(self, scale_factor=0.5):
        self.sd['scale'] = scale_factor * self.scale_baseline
        self.sd['size'] = self.sd['scale'] * self.origin_h

    # Scaling the symbol for multisymbol flags
    def scale_data(self, data, scale_factor=0.5):
        data['scale'] = scale_factor * self.scale_baseline
        data['size'] = data['scale'] * self.origin_h
        return data

    # _____________________
    # Basic transformations

    # Center (eg. Japanese flag)
    def center(self, scale_factor=uniform(0.4, 0.7)):
        self.sd['pos'] = (self.w / 2, self.h / 2)
        self.scale(scale_factor)
        return self.sd

    # Center left (eg. Serbian flag)
    def center_left(self, scale_factor=0.5, width_fraction=0.382):
        self.sd['pos'] = (self.w * width_fraction, self.h / 2)
        self.scale(scale_factor)
        return self.sd

    # Center right (eg. New Zealand flag)
    def center_right(self, scale_factor=0.5, width_fraction=0.618):
        self.sd['pos'] = (self.w * width_fraction, self.h / 2)
        self.scale(scale_factor)
        return self.sd

    # Center up
    def center_up(self, scale_factor=0.5, height_fraction=0.33):
        self.sd['pos'] = (self.w / 2, self.h * height_fraction)
        self.scale(scale_factor)
        return self.sd

    # Center down
    def center_down(self, scale_factor=0.5, height_fraction=0.67):
        self.sd['pos'] = (self.w / 2, self.h * height_fraction)
        self.scale(scale_factor)
        return self.sd

    # Canton, upper left corner
    def canton_small(self, scale_factor=0.2, dim=(0.2, 0.2)):
        self.sd['pos'] = (self.h * dim[0], self.h * dim[1])
        self.scale(scale_factor)
        return self.sd

    # Cantons in other directions:
    def canton_small_upper_right(self, scale_factor=0.2, dim=(0.2, 0.2)):
        self.sd['pos'] = (self.h * dim[0], self.h - self.h * dim[1])
        self.scale(scale_factor)
        return self.sd

    def canton_small_lower_right(self, scale_factor=0.2, dim=(0.2, 0.2)):
        self.sd['pos'] = (self.w - self.h * dim[0], self.h - self.h * dim[1])
        self.scale(scale_factor)
        return self.sd

    def canton_small_lower_left(self, scale_factor=0.2, dim=(0.2, 0.2)):
        self.sd['pos'] = (self.w - self.h * dim[0], self.h * dim[1])
        self.scale(scale_factor)
        return self.sd

    # __________________________
    # Shortcuts for layout types

    def default_center_canton_small(self, scale_factor=uniform(0.3, 0.8), center_chance=0.33):
        if random() <= center_chance:
            return self.center(scale_factor)
        else:
            return self.canton_small(scale_factor=uniform(0.2, 0.3))

    def default_center_center_left(self, scale_factor=uniform(0.3, 0.8)):
        if random() <= 0.8:  # 1:
            return self.center(scale_factor)
        elif 0.8 < random() <= 0.9:
            return self.center_left(scale_factor)
        else:
            return self.center_left(scale_factor, width_fraction=uniform(0.25, 0.45))

    def default_left_or_right(self, width_fraction_left=0.18, width_fraction_right=0.8):
        if random() <= 0.67:
            scale_left = uniform(0.26, 0.4)
            return self.center_left(scale_left, width_fraction=width_fraction_left)
        else:
            scale_right = uniform(0.3, 0.5)
            return self.center_left(scale_right, width_fraction=width_fraction_right)

    def default_canton_center_down(self, scale_factor, height_fraction, canton_dim):
        if random() < 0.3:
            dim = (canton_dim, canton_dim)
            return self.canton_small(dim=dim)
        else:
            return self.center_up(scale_factor=scale_factor, height_fraction=height_fraction)

    def default_canton_small_variations(self, scale=uniform(0.3, 0.4), canton_dim=0.3):
        dim = (canton_dim, canton_dim)
        toss = random()
        if toss < 0.25:
            return self.canton_small(scale_factor=scale, dim=dim)
        elif 0.25 <= toss < 0.5:
            return self.canton_small_lower_right(scale_factor=scale, dim=dim)
        elif 0.5 <= toss < 0.75:
            return self.canton_small_upper_right(scale_factor=scale, dim=dim)
        else:
            return self.canton_small_lower_left(scale_factor=scale, dim=dim)

    # ________________
    # Multiple Emblems

    def linear_multiemblem(self, scale_factor, positions):
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()
        for x in positions:
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, 0.5 * self.h)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)

    def linear_multiemblem_diag(self, scale_factor, positions):
        s = self.engine.create_main_symbol()
        s.define_colors()
        for pos in positions:
            x, y = pos
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, y * self.h)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)

    def linear_multiemblem_diff(self, scale_factor, positions):
        self.engine.multisymbol_vector()
        for x in positions:
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, 0.5 * self.h)
            self.engine.add_symbol(d)

    def linear_multiemblem_diff_diag(self, scale_factor, positions):
        self.engine.multisymbol_vector()
        for pos in positions:
            x, y = pos
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, y * self.h)
            self.engine.add_symbol(d)

    def quadriemblem(self, void=0.33, diag1=0.5, diag2=0.5):
        self.engine.multisymbol_vector()
        if random() <= void:
            return
        if random() > diag1:
            scale_factor = uniform(0.2, 0.3)
            positions = [(0.25, 0.25), (0.75, 0.75)]
            self.linear_multiemblem_diag(scale_factor=scale_factor, positions=positions)
        if random() > diag2:
            scale_factor = uniform(0.2, 0.3)
            positions = [(0.25, 0.75), (0.75, 0.25)]
            self.linear_multiemblem_diag(scale_factor=scale_factor, positions=positions)

    def void_multiemblem(self):
        self.engine.multisymbol_vector()

    def american_multiemblem(self):
        scale_factor = 0.1
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()
        nx, ny = randint(4, 6), randint(3, 4)
        inc_x, inc_y = (self.w / 2) / nx, (self.h / 2) / ny
        for i in range(1, nx):
            for j in range(1, ny):
                d = self.symbol_data_copy()
                d = self.scale_data(d, scale_factor)
                shift = 0 if j % 2 == 0 else inc_x / 2
                if shift != 0 and i == nx - 1:
                    pass
                else:
                    d['pos'] = ((i * inc_x) + shift, j * inc_y)
                    sym = s.copy(d)
                    self.engine.add_symbol_directly(sym)


    def circular_multiemblem(self):
        scale_factor = uniform(0.12, 0.2)
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()

        data = self.symbol_data_copy()
        n = randint(5, 12)
        angle = 2 * math.pi / n
        rad = data['size'] * uniform(0.5, 0.65)
        x, y = data['pos']

        for i in range(n):
            theta = (angle * i) - math.pi / 2
            x1, y1 = x + math.cos(theta) * rad, y + math.sin(theta) * rad
            d = self.scale_data(self.symbol_data_copy(), scale_factor)
            d['pos'] = (x1, y1)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)


    def diagonal_multiemblem(self, up_chance=0.5):
        scale_factor = uniform(0.12, 0.2)
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()

        n = randint(5, 10)
        inc_x, inc_y = self.w / n, self.h / n
        x1, y1 = 0, 0
        if random() > up_chance:
            y1 = self.h
            inc_y = -inc_y

        for i in range(0, n + 1):
            d = self.scale_data(self.symbol_data_copy(), scale_factor)
            d['pos'] = (x1, y1)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)
            x1 += inc_x
            y1 += inc_y


    def bosnian_diagonal(self):
        scale_factor = uniform(0.09, 0.13)
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()

        n = randint(7, 10)
        inc = self.h / n
        x1, y1 = self.w * 0.09, 0

        for i in range(0, n + 1):
            d = self.scale_data(self.symbol_data_copy(), scale_factor)
            d['pos'] = (x1, y1)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)
            x1 += inc
            y1 += inc


    # _______________________________________________
    # Shortcuts for layout types for multiple emblems

    def default_multiemblem(self):
        toss = random()
        if toss < 0.4:
            self.linear_multiemblem_diff(scale_factor=uniform(0.4, 0.5), positions=[0.3, 0.7])
        elif 0.4 <= toss < 0.6:
            self.linear_multiemblem_diff(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        elif 0.6 <= toss < 0.8:
            self.linear_multiemblem(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        else:
            self.linear_multiemblem(scale_factor=uniform(0.2, 0.2), positions=[0.2, 0.4, 0.6, 0.8])


    def variable_multiemblem(self):
        toss = random()
        if toss < 0.3:
            self.linear_multiemblem_diff(scale_factor=uniform(0.4, 0.5), positions=[0.3, 0.7])
        elif 0.3 <= toss < 0.4:
            self.linear_multiemblem_diff(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        elif 0.4 <= toss < 0.5:
            self.linear_multiemblem(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        elif 0.5 <= toss < 0.6:
            self.linear_multiemblem(scale_factor=uniform(0.2, 0.2), positions=[0.2, 0.4, 0.6, 0.8])
        elif 0.6 <= toss < 0.7:
            self.diagonal_multiemblem()
        elif 0.7 <= toss < 0.8:
            self.diagonal_multiemblem()
        else:
            self.circular_multiemblem()


    def vertical_multiemblem(self):
        toss = random()
        if toss < 0.5:
            self.linear_multiemblem_diff(scale_factor=uniform(0.4, 0.5), positions=[0.3, 0.7])
        else:
            self.circular_multiemblem()


    def default_diag_multiemblem(self, up_chance=0.5):
        toss = random()
        positions = [(0.25, 0.33), (0.75, 0.67)]
        if random() < up_chance:
            positions = [(0.25, 0.67), (0.75, 0.33)]
        if toss < 0.7:
            self.linear_multiemblem_diff_diag(scale_factor=uniform(0.25, 0.33), positions=positions)
        else:
            self.diagonal_multiemblem(up_chance=up_chance)

    # ________________
    # Multiple Emblems

    def linear_multiemblem(self, scale_factor, positions):
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()
        for x in positions:
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, 0.5 * self.h)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)

    def linear_multiemblem_diag(self, scale_factor, positions):
        s = self.engine.create_main_symbol()
        s.define_colors()
        for pos in positions:
            x, y = pos
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, y * self.h)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)

    def linear_multiemblem_diff(self, scale_factor, positions):
        self.engine.multisymbol_vector()
        for x in positions:
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, 0.5 * self.h)
            self.engine.add_symbol(d)

    def linear_multiemblem_diff_diag(self, scale_factor, positions):
        self.engine.multisymbol_vector()
        for pos in positions:
            x, y = pos
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, y * self.h)
            self.engine.add_symbol(d)

    def quadriemblem(self, void=0.33, diag1=0.5, diag2=0.5):
        self.engine.multisymbol_vector()
        if random() <= void:
            return
        if random() > diag1:
            scale_factor = uniform(0.2, 0.3)
            positions = [(0.25, 0.25), (0.75, 0.75)]
            self.linear_multiemblem_diag(scale_factor=scale_factor, positions=positions)
        if random() > diag2:
            scale_factor = uniform(0.2, 0.3)
            positions = [(0.25, 0.75), (0.75, 0.25)]
            self.linear_multiemblem_diag(scale_factor=scale_factor, positions=positions)

    def void_multiemblem(self):
        self.engine.multisymbol_vector()

    def american_multiemblem(self):
        scale_factor = 0.1
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()
        nx, ny = randint(4, 6), randint(3, 4)
        inc_x, inc_y = (self.w / 2) / nx, (self.h / 2) / ny
        for i in range(1, nx):
            for j in range(1, ny):
                d = self.symbol_data_copy()
                d = self.scale_data(d, scale_factor)
                shift = 0 if j % 2 == 0 else inc_x / 2
                if shift != 0 and i == nx - 1:
                    pass
                else:
                    d['pos'] = ((i * inc_x) + shift, j * inc_y)
                    sym = s.copy(d)
                    self.engine.add_symbol_directly(sym)


    def circular_multiemblem(self):
        scale_factor = uniform(0.12, 0.2)
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()

        data = self.symbol_data_copy()
        n = randint(5, 12)
        angle = 2 * math.pi / n
        rad = data['size'] * uniform(0.5, 0.65)
        x, y = data['pos']

        for i in range(n):
            theta = (angle * i) - math.pi / 2
            x1, y1 = x + math.cos(theta) * rad, y + math.sin(theta) * rad
            d = self.scale_data(self.symbol_data_copy(), scale_factor)
            d['pos'] = (x1, y1)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)


    def diagonal_multiemblem(self, up_chance=0.5):
        scale_factor = uniform(0.12, 0.2)
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()

        n = randint(5, 10)
        inc_x, inc_y = self.w / n, self.h / n
        x1, y1 = 0, 0
        if random() > up_chance:
            y1 = self.h
            inc_y = -inc_y

        for i in range(0, n + 1):
            d = self.scale_data(self.symbol_data_copy(), scale_factor)
            d['pos'] = (x1, y1)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)
            x1 += inc_x
            y1 += inc_y


    def bosnian_diagonal(self):
        scale_factor = uniform(0.09, 0.13)
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()

        n = randint(7, 10)
        inc = self.h / n
        x1, y1 = self.w * 0.09, 0

        for i in range(0, n + 1):
            d = self.scale_data(self.symbol_data_copy(), scale_factor)
            d['pos'] = (x1, y1)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)
            x1 += inc
            y1 += inc


    # _______________________________________________
    # Shortcuts for layout types for multiple emblems

    def default_multiemblem(self):
        toss = random()
        if toss < 0.4:
            self.linear_multiemblem_diff(scale_factor=uniform(0.4, 0.5), positions=[0.3, 0.7])
        elif 0.4 <= toss < 0.6:
            self.linear_multiemblem_diff(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        elif 0.6 <= toss < 0.8:
            self.linear_multiemblem(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        else:
            self.linear_multiemblem(scale_factor=uniform(0.2, 0.2), positions=[0.2, 0.4, 0.6, 0.8])


    def variable_multiemblem(self):
        toss = random()
        if toss < 0.3:
            self.linear_multiemblem_diff(scale_factor=uniform(0.4, 0.5), positions=[0.3, 0.7])
        elif 0.3 <= toss < 0.4:
            self.linear_multiemblem_diff(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        elif 0.4 <= toss < 0.5:
            self.linear_multiemblem(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        elif 0.5 <= toss < 0.6:
            self.linear_multiemblem(scale_factor=uniform(0.2, 0.2), positions=[0.2, 0.4, 0.6, 0.8])
        elif 0.6 <= toss < 0.7:
            self.diagonal_multiemblem()
        elif 0.7 <= toss < 0.8:
            self.diagonal_multiemblem()
        else:
            self.circular_multiemblem()


    def vertical_multiemblem(self):
        toss = random()
        if toss < 0.5:
            self.linear_multiemblem_diff(scale_factor=uniform(0.4, 0.5), positions=[0.3, 0.7])
        else:
            self.circular_multiemblem()


    def default_diag_multiemblem(self, up_chance=0.5):
        toss = random()
        positions = [(0.25, 0.33), (0.75, 0.67)]
        if random() < up_chance:
            positions = [(0.25, 0.67), (0.75, 0.33)]
        if toss < 0.7:
            self.linear_multiemblem_diff_diag(scale_factor=uniform(0.25, 0.33), positions=positions)
        else:
            self.diagonal_multiemblem(up_chance=up_chance)

    # ________________
    # Multiple Emblems

    def linear_multiemblem(self, scale_factor, positions):
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()
        for x in positions:
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, 0.5 * self.h)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)

    def linear_multiemblem_diag(self, scale_factor, positions):
        s = self.engine.create_main_symbol()
        s.define_colors()
        for pos in positions:
            x, y = pos
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, y * self.h)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)

    def linear_multiemblem_diff(self, scale_factor, positions):
        self.engine.multisymbol_vector()
        for x in positions:
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, 0.5 * self.h)
            self.engine.add_symbol(d)

    def linear_multiemblem_diff_diag(self, scale_factor, positions):
        self.engine.multisymbol_vector()
        for pos in positions:
            x, y = pos
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, y * self.h)
            self.engine.add_symbol(d)

    def quadriemblem(self, void=0.33, diag1=0.5, diag2=0.5):
        self.engine.multisymbol_vector()
        if random() <= void:
            return
        if random() > diag1:
            scale_factor = uniform(0.2, 0.3)
            positions = [(0.25, 0.25), (0.75, 0.75)]
            self.linear_multiemblem_diag(scale_factor=scale_factor, positions=positions)
        if random() > diag2:
            scale_factor = uniform(0.2, 0.3)
            positions = [(0.25, 0.75), (0.75, 0.25)]
            self.linear_multiemblem_diag(scale_factor=scale_factor, positions=positions)

    def void_multiemblem(self):
        self.engine.multisymbol_vector()

    def american_multiemblem(self):
        scale_factor = 0.1
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()
        nx, ny = randint(4, 6), randint(3, 4)
        inc_x, inc_y = (self.w / 2) / nx, (self.h / 2) / ny
        for i in range(1, nx):
            for j in range(1, ny):
                d = self.symbol_data_copy()
                d = self.scale_data(d, scale_factor)
                shift = 0 if j % 2 == 0 else inc_x / 2
                if shift != 0 and i == nx - 1:
                    pass
                else:
                    d['pos'] = ((i * inc_x) + shift, j * inc_y)
                    sym = s.copy(d)
                    self.engine.add_symbol_directly(sym)


    def circular_multiemblem(self):
        scale_factor = uniform(0.12, 0.2)
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()

        data = self.symbol_data_copy()
        n = randint(5, 12)
        angle = 2 * math.pi / n
        rad = data['size'] * uniform(0.5, 0.65)
        x, y = data['pos']

        for i in range(n):
            theta = (angle * i) - math.pi / 2
            x1, y1 = x + math.cos(theta) * rad, y + math.sin(theta) * rad
            d = self.scale_data(self.symbol_data_copy(), scale_factor)
            d['pos'] = (x1, y1)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)


    def diagonal_multiemblem(self, up_chance=0.5):
        scale_factor = uniform(0.12, 0.2)
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()

        n = randint(5, 10)
        inc_x, inc_y = self.w / n, self.h / n
        x1, y1 = 0, 0
        if random() > up_chance:
            y1 = self.h
            inc_y = -inc_y

        for i in range(0, n + 1):
            d = self.scale_data(self.symbol_data_copy(), scale_factor)
            d['pos'] = (x1, y1)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)
            x1 += inc_x
            y1 += inc_y


    def bosnian_diagonal(self):
        scale_factor = uniform(0.09, 0.13)
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()

        n = randint(7, 10)
        inc = self.h / n
        x1, y1 = self.w * 0.09, 0

        for i in range(0, n + 1):
            d = self.scale_data(self.symbol_data_copy(), scale_factor)
            d['pos'] = (x1, y1)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)
            x1 += inc
            y1 += inc


    # _______________________________________________
    # Shortcuts for layout types for multiple emblems

    def default_multiemblem(self):
        toss = random()
        if toss < 0.4:
            self.linear_multiemblem_diff(scale_factor=uniform(0.4, 0.5), positions=[0.3, 0.7])
        elif 0.4 <= toss < 0.6:
            self.linear_multiemblem_diff(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        elif 0.6 <= toss < 0.8:
            self.linear_multiemblem(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        else:
            self.linear_multiemblem(scale_factor=uniform(0.2, 0.2), positions=[0.2, 0.4, 0.6, 0.8])


    def variable_multiemblem(self):
        toss = random()
        if toss < 0.3:
            self.linear_multiemblem_diff(scale_factor=uniform(0.4, 0.5), positions=[0.3, 0.7])
        elif 0.3 <= toss < 0.4:
            self.linear_multiemblem_diff(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        elif 0.4 <= toss < 0.5:
            self.linear_multiemblem(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        elif 0.5 <= toss < 0.6:
            self.linear_multiemblem(scale_factor=uniform(0.2, 0.2), positions=[0.2, 0.4, 0.6, 0.8])
        elif 0.6 <= toss < 0.7:
            self.diagonal_multiemblem()
        elif 0.7 <= toss < 0.8:
            self.diagonal_multiemblem()
        else:
            self.circular_multiemblem()


    def vertical_multiemblem(self):
        toss = random()
        if toss < 0.5:
            self.linear_multiemblem_diff(scale_factor=uniform(0.4, 0.5), positions=[0.3, 0.7])
        else:
            self.circular_multiemblem()


    def default_diag_multiemblem(self, up_chance=0.5):
        toss = random()
        positions = [(0.25, 0.33), (0.75, 0.67)]
        if random() < up_chance:
            positions = [(0.25, 0.67), (0.75, 0.33)]
        if toss < 0.7:
            self.linear_multiemblem_diff_diag(scale_factor=uniform(0.25, 0.33), positions=positions)
        else:
            self.diagonal_multiemblem(up_chance=up_chance)

    # ________________
    # Multiple Emblems

    def linear_multiemblem(self, scale_factor, positions):
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()
        for x in positions:
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, 0.5 * self.h)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)

    def linear_multiemblem_diag(self, scale_factor, positions):
        s = self.engine.create_main_symbol()
        s.define_colors()
        for pos in positions:
            x, y = pos
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, y * self.h)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)

    def linear_multiemblem_diff(self, scale_factor, positions):
        self.engine.multisymbol_vector()
        for x in positions:
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, 0.5 * self.h)
            self.engine.add_symbol(d)

    def linear_multiemblem_diff_diag(self, scale_factor, positions):
        self.engine.multisymbol_vector()
        for pos in positions:
            x, y = pos
            d = self.symbol_data_copy()
            d = self.scale_data(d, scale_factor)
            d['pos'] = (x * self.w, y * self.h)
            self.engine.add_symbol(d)

    def quadriemblem(self, void=0.33, diag1=0.5, diag2=0.5):
        self.engine.multisymbol_vector()
        if random() <= void:
            return
        if random() > diag1:
            scale_factor = uniform(0.2, 0.3)
            positions = [(0.25, 0.25), (0.75, 0.75)]
            self.linear_multiemblem_diag(scale_factor=scale_factor, positions=positions)
        if random() > diag2:
            scale_factor = uniform(0.2, 0.3)
            positions = [(0.25, 0.75), (0.75, 0.25)]
            self.linear_multiemblem_diag(scale_factor=scale_factor, positions=positions)

    def void_multiemblem(self):
        self.engine.multisymbol_vector()

    def american_multiemblem(self):
        scale_factor = 0.1
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()
        nx, ny = randint(4, 6), randint(3, 4)
        inc_x, inc_y = (self.w / 2) / nx, (self.h / 2) / ny
        for i in range(1, nx):
            for j in range(1, ny):
                d = self.symbol_data_copy()
                d = self.scale_data(d, scale_factor)
                shift = 0 if j % 2 == 0 else inc_x / 2
                if shift != 0 and i == nx - 1:
                    pass
                else:
                    d['pos'] = ((i * inc_x) + shift, j * inc_y)
                    sym = s.copy(d)
                    self.engine.add_symbol_directly(sym)


    def circular_multiemblem(self):
        scale_factor = uniform(0.12, 0.2)
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()

        data = self.symbol_data_copy()
        n = randint(5, 12)
        angle = 2 * math.pi / n
        rad = data['size'] * uniform(0.5, 0.65)
        x, y = data['pos']

        for i in range(n):
            theta = (angle * i) - math.pi / 2
            x1, y1 = x + math.cos(theta) * rad, y + math.sin(theta) * rad
            d = self.scale_data(self.symbol_data_copy(), scale_factor)
            d['pos'] = (x1, y1)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)


    def diagonal_multiemblem(self, up_chance=0.5):
        scale_factor = uniform(0.12, 0.2)
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()

        n = randint(5, 10)
        inc_x, inc_y = self.w / n, self.h / n
        x1, y1 = 0, 0
        if random() > up_chance:
            y1 = self.h
            inc_y = -inc_y

        for i in range(0, n + 1):
            d = self.scale_data(self.symbol_data_copy(), scale_factor)
            d['pos'] = (x1, y1)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)
            x1 += inc_x
            y1 += inc_y


    def bosnian_diagonal(self):
        scale_factor = uniform(0.09, 0.13)
        self.engine.multisymbol_vector()
        s = self.engine.create_main_symbol()
        s.define_colors()

        n = randint(7, 10)
        inc = self.h / n
        x1, y1 = self.w * 0.09, 0

        for i in range(0, n + 1):
            d = self.scale_data(self.symbol_data_copy(), scale_factor)
            d['pos'] = (x1, y1)
            sym = s.copy(d)
            self.engine.add_symbol_directly(sym)
            x1 += inc
            y1 += inc


    # _______________________________________________
    # Shortcuts for layout types for multiple emblems

    def default_multiemblem(self):
        toss = random()
        if toss < 0.4:
            self.linear_multiemblem_diff(scale_factor=uniform(0.4, 0.5), positions=[0.3, 0.7])
        elif 0.4 <= toss < 0.6:
            self.linear_multiemblem_diff(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        elif 0.6 <= toss < 0.8:
            self.linear_multiemblem(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        else:
            self.linear_multiemblem(scale_factor=uniform(0.2, 0.2), positions=[0.2, 0.4, 0.6, 0.8])


    def variable_multiemblem(self):
        toss = random()
        if toss < 0.3:
            self.linear_multiemblem_diff(scale_factor=uniform(0.4, 0.5), positions=[0.3, 0.7])
        elif 0.3 <= toss < 0.4:
            self.linear_multiemblem_diff(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        elif 0.4 <= toss < 0.5:
            self.linear_multiemblem(scale_factor=uniform(0.25, 0.3), positions=[0.25, 0.5, 0.75])
        elif 0.5 <= toss < 0.6:
            self.linear_multiemblem(scale_factor=uniform(0.2, 0.2), positions=[0.2, 0.4, 0.6, 0.8])
        elif 0.6 <= toss < 0.7:
            self.diagonal_multiemblem()
        elif 0.7 <= toss < 0.8:
            self.diagonal_multiemblem()
        else:
            self.circular_multiemblem()


    def vertical_multiemblem(self):
        toss = random()
        if toss < 0.5:
            self.linear_multiemblem_diff(scale_factor=uniform(0.4, 0.5), positions=[0.3, 0.7])
        else:
            self.circular_multiemblem()


    def default_diag_multiemblem(self, up_chance=0.5):
        toss = random()
        positions = [(0.25, 0.33), (0.75, 0.67)]
        if random() < up_chance:
            positions = [(0.25, 0.67), (0.75, 0.33)]
        if toss < 0.7:
            self.linear_multiemblem_diff_diag(scale_factor=uniform(0.25, 0.33), positions=positions)
        else:
            self.diagonal_multiemblem(up_chance=up_chance)
