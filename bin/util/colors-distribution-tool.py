import math
import json
import os
from colour import Color
from PIL import Image
from matplotlib import pyplot as plt

##################################################################
class PrimaryColor:
    def __init__(self, name):
        self.name = name
        self.variations = []

##################################################################
class ColorVariation:
    def __init__(self, color, primary, name, hex_value):
        self.color = color
        self.primary = primary
        self.name = name
        self.hex_value = hex_value

        self.R = color.red * 255.0
        self.G = color.green * 255.0
        self.B = color.blue * 255.0

    def calculate_eucledian_distance(self, color_to_compare_to):
        #     ________________________________________
        #    / 
        #   V  (R1 - R2)^2 + (G1 - G2)^2 + (B1 - B2)^2
        #
        sum_squared = \
            (self.R - color_to_compare_to.R) ** 2 + \
            (self.G - color_to_compare_to.G) ** 2 + \
            (self.B - color_to_compare_to.B) ** 2

        return math.sqrt(sum_squared)

##################################################################
class ColorsCash:
    def __init__(self):
        # cash is represented as a simple dictionary
        # where keys are color hex values and values
        # are color hex values of the nearest color 
        # from our vocabulary
        self.cash = {}
    
    def add(self, current_color_hex, nearest_color_hex):
        if current_color_hex not in self.cash:
            self.cash[current_color_hex] = nearest_color_hex

    def get(self, current_color_hex):
        if current_color_hex in self.cash:
            return self.cash[current_color_hex]
        else:
            return None

##################################################################
class ColorDistributionsProcessor:
    def __init__(self, rules_path="conf\\flag-rules.json", flags_dir="media\\raster100px"):
        # load rules and build color vocabulary
        all_rules = json.load(open(rules_path))
        color_definitions = all_rules["colors"]
        self.color_vocabulary = self.build_color_vocabulary(color_definitions)

        # create colors cash
        # - this will be used to use already calculated nearest colors,
        #   instead of calculating each time
        self.colors_cash = ColorsCash()

        self.flags_dir = flags_dir

    def build_color_vocabulary(self, color_definitions):
        # this dictionary data structure consists of key-value pairs
        # where keys are color names and the values are objects
        # of type FlaglabsColor
        colors_vocab = {}
        for color_info in color_definitions:
            primary_name = color_info["name"]
            primary_color = PrimaryColor(primary_name)

            variations = color_info["variations"]
            for variation in variations:
                hex_value = variation["value"]
                name = variation["name"]
                color = Color(hex_value)
                flaglabs_color = ColorVariation(color, primary_color, name, hex_value)
                primary_color.variations.append(flaglabs_color)
                colors_vocab[name] = flaglabs_color
        return colors_vocab

    def get_most_similar_color(self, color):
        nearest_color = None
        nearest_distance = float("inf")
        for _, vocab_color in self.color_vocabulary.items():

            distance = vocab_color.calculate_eucledian_distance(color)
            
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_color = vocab_color

        return nearest_color

    def add_to_total_histogram(self, hist_total, hist_per_flag):
        # for each color and its number of occurances in histogram of colors
        # check if it exists in total histogram and update the value there.
        # if it does not exist, set it to the initial value
        for color_name, num_of_occurances in hist_per_flag.items():
            if color_name in hist_total:
                hist_total[color_name] += num_of_occurances
            else:
                hist_total[color_name] = num_of_occurances
        return hist_total

    def dump_histograms_to_files(self, list_of_histograms, total_histogram):
        print("Exporting list of histograms per flag...")
        with open("conf/color-distributions-per-flag-NEW.json", "w") as f_per_flag:
            json.dump(list_of_histograms, f_per_flag, indent=4)

        print("Exporting the histogram for the whole dataset...")
        with open("conf/color-distributions-total-NEW.json", "w") as f_total:
            json.dump(total_histogram, f_total, indent=4)

    def plot_histogram(self, histogram):
        ax = plt.axes()
        ax.set_facecolor("#e0e0e0")
        idx = 0
        for color_name, color_count in histogram.items():
            color_hex = self.color_vocabulary[color_name].hex_value
            plt.bar(color_name, color_count, color=color_hex)
            idx += 1
        
        plt.xticks(rotation=90)
        plt.tight_layout()

        plt.show()

    def group_by_primary_color(self, histogram_of_percentages):
        hist_grouped = {}
        for key, value in histogram_of_percentages.items():
            color = self.color_vocabulary[key]
            primary_color_name = color.primary.name
            
            hist_of_primary = {}
            if primary_color_name in hist_grouped:
                hist_of_primary = hist_grouped[primary_color_name]
            else:
                hist_grouped[primary_color_name] = hist_of_primary

            hist_of_primary[key] = value

        return hist_grouped

    # main method
    def get_histograms(self):
        list_of_histograms = []
        total_histogram = {}

        # iterate through all the files in the dataset
        for subdir, _, files in os.walk(self.flags_dir):
            # skip the root directory itself
            if (subdir == self.flags_dir):
                continue

            print("Processing: " + subdir)
            for file in files:

                flag_full_path = os.path.join(subdir, file)
                hist_per_flag, number_of_pixels = self.process_flag(flag_full_path)
                total_histogram = self.add_to_total_histogram(total_histogram, hist_per_flag)
                hist_per_flag, hist_percentages = self.get_histogram_of_percentages(hist_per_flag, number_of_pixels)
                hist_percentages = self.group_by_primary_color(hist_percentages)

                list_of_histograms.append({ 
                    'path': flag_full_path, 
                    'colors_percentages' : hist_percentages
                })

        self.plot_histogram(total_histogram)

        print("Calculating the color percentages...")
        total_num_of_pixels_in_dataset = sum(total_histogram.values())
        total_histogram, total_histogram_percentages = self.get_histogram_of_percentages(total_histogram, total_num_of_pixels_in_dataset)
        print(total_histogram)
        total_histogram_percentages = self.group_by_primary_color(total_histogram_percentages)
        total_hist_for_json = { 'histogram_percentages' : total_histogram_percentages }

        return list_of_histograms, total_hist_for_json

    def get_histogram_of_percentages(self, histogram_of_colors, pixels_total_count):
        # this histogram dictionary contains the percentage that
        # each color from the flag occupies
        # 
        # Note: colors occuring in less than 1% of pixels will be discarded
        keys_to_remove = []

        histogram_of_percentages = {}
        for key, value in histogram_of_colors.items():
            percentage = value / pixels_total_count
            if percentage < 0.01:
                # remove this color from histogram_of_colors
                # and do not add it to histogram_percentages
                keys_to_remove.append(key)
                continue

            histogram_of_percentages[key] = percentage

        for key in keys_to_remove:
            histogram_of_colors.pop(key)

        return histogram_of_colors, histogram_of_percentages

    def process_flag(self, path):
        # color distributions
        histogram_of_colors = {}

        # load the image
        img = Image.open(path)
        img.load()

        width = img.width
        height = img.height

        # total number of pixels
        total_count = width * height

        colors_hist = img.getcolors(total_count)

        for color_with_count in colors_hist:
            color_count = color_with_count[0]
            rgb = (color_with_count[1][0] / 255.0, 
                   color_with_count[1][1] / 255.0, 
                   color_with_count[1][2] / 255.0, )
            color = Color(rgb=rgb)
            flaglabs_color = ColorVariation(color, "", "", color.hex_l)

            # try to find the most similar color in cash
            nearest_color = self.colors_cash.get(flaglabs_color.hex_value)
            if nearest_color is None:
                # we didn't come across this particular color until now, 
                # so we calculate the most similar color and save it to
                # the cash for future use.
                vocab_color = self.get_most_similar_color(flaglabs_color)
                self.colors_cash.add(flaglabs_color.hex_value, vocab_color)
                nearest_color = vocab_color

            # update the count for this color if it exists in the histogram.
            # else, add it to the histogram, and set its count to the initial color count.
            if nearest_color.name in histogram_of_colors:
                histogram_of_colors[nearest_color.name] += color_count
            else:
                histogram_of_colors[nearest_color.name] = color_count

        return histogram_of_colors, total_count

if __name__ == '__main__':
    processor = ColorDistributionsProcessor()
    list_of_histograms, total_histogram = processor.get_histograms()
    processor.dump_histograms_to_files(list_of_histograms, total_histogram)
