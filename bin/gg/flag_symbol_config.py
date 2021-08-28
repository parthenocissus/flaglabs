import math
from random import choices, random, randint, uniform, randrange


# _____________________________________________________
# Class for defining the position of a symbol on a flag
# Mostly used by layout functions
class FlagSymbolConfig:

    def __init__(self, origin, symbol_data, w, h):
        self.sd = symbol_data
        self.origin_h = origin.h
        self.scale_baseline = symbol_data['scale_baseline']
        self.w, self.h = w, h

    # Scaling the symbol
    def scale(self, scale_factor=0.5):
        self.sd['scale'] = scale_factor * self.scale_baseline
        # self.sd['size'] = self.sd['scale'] * self.h
        self.sd['size'] = self.sd['scale'] * self.origin_h

    # _____________________
    # Basic transformations

    # Center (eg. Japanese flag)
    def center(self, scale_factor=0.5):
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

    # __________________________
    # Shortcuts for layout types

    def default_center_canton_small(self, scale_factor=uniform(0.3, 0.8)):
        if random() <= 0.33:
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