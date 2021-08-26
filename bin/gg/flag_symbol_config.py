import math
from random import choices, random, randint, uniform, randrange


# _____________________________________________________
# Class for defining the position of a symbol on a flag
# Mostly used by layout functions
class FlagSymbolConfig:

    def __init__(self, symbol_data, w, h):
        self.sd = symbol_data
        self.w, self.h = w, h

    # Scaling the symbol
    def scale(self, scale_factor=0.5):
        self.sd['size'] = scale_factor * self.h
        self.sd['scale'] = scale_factor

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

    def default_center_center_left(self):
        scale = uniform(0.3, 0.8)
        if random() <= 0.8:
            return self.center(scale)
        elif 0.8 < random() <= 0.9:
            return self.center_left(scale)
        else:
            return self.center_left(scale, width_fraction=uniform(0.25, 0.45))