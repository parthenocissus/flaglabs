import os
import shutil
from PIL import Image, ImageChops
import numpy as np

class FlagsDatasetCleaner:
    def __init__(self, flags_dir="media/raster100px",
        cleaned_dir = "media/raster100px-cleaned",
        discarded_dir = "media/raster100px-discarded"):

        self.flags_dir = flags_dir
        self.cleaned_dir = cleaned_dir
        self.discarded_dir = discarded_dir

        self.count_cleaned = 0
        self.count_discarded = 0

        # Create root directories if they don't exist
        if not os.path.exists(self.cleaned_dir):
            os.mkdir(self.cleaned_dir)
        if not os.path.exists(self.discarded_dir):
            os.mkdir(self.discarded_dir)

    def clean(self):
        # Iterate over files in subfolders
        for subdir, _, files in os.walk(self.flags_dir):
            print("Processing subdir: " + subdir)
            for file in files:
                img_full_path = os.path.join(subdir, file)
                self.process_img(img_full_path)
        
        print("___________________________")
        print("Total count of discarded images: {}".format(self.count_discarded))
        print("Total count of cleaned images: {}".format(self.count_cleaned))
    
    def remove_transparency(self, img, bg_colour=(255, 255, 255)):
        # Explanation of PNG modes: https://pillow.readthedocs.io/en/stable/handbook/concepts.html 
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):

            # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
            alpha = img.convert('RGBA').split()[-1]

            # Create a new background image of our matt color.
            # Must be RGBA because paste requires both images have the same format
            # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
            bg = Image.new("RGBA", img.size, bg_colour + (255,))
            bg.paste(img, mask=alpha)
            return bg.convert('RGB')
        else:
            return img


    def is_BW_only(self, img):
        # Image.getbbox() returns the falsy None if there are no non-black pixels in the image
        if not img.getbbox():
            return True

        # Similarly, inverting the image and then running Image.getbbox()
        # returns the falsy None if there are no non-white pixels in the image
        if not ImageChops.invert(img).getbbox():
            return True

        # Else, the image is not all-white or all-black!
        return False

    def process_img(self, path):
        filename = os.path.basename(path)
        parent_folder = os.path.dirname(path)
        parent_folder = os.path.basename(parent_folder)
        
        # Load image
        img = Image.open(path)
        img.load()

        # Remove transparency
        img = self.remove_transparency(img)

        # Convert to RGB if the PNG format is either of the following:
        # - 1 (1-bit pixels, black and white, stored with one pixel per byte)
        # - L (8-bit pixels, black and white)
        # - P (8-bit pixels, mapped to any other mode using a color palette)
        # - I (32-bit signed integer pixels)
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Check if the image consists of only black or only white pixels
        if (self.is_BW_only(img)):
            # Create subfolder if it doesn't exist
            # i.e. media/raster100px-discarded/52 
            discarded_subdir = os.path.join(self.discarded_dir, parent_folder)
            if not os.path.exists(discarded_subdir):
                os.mkdir(discarded_subdir)

            # Copy the image from the original dataset
            discarded_img_path = os.path.join(discarded_subdir, filename)
            shutil.copyfile(path, discarded_img_path)
            self.count_discarded += 1
        else:
            # Create subfolder if it doesn't exist
            # i.e. media/raster100px-cleaned/135 
            cleaned_subdir = os.path.join(self.cleaned_dir, parent_folder)
            if not os.path.exists(cleaned_subdir):
                os.mkdir(cleaned_subdir)

            # Save new cleaned image
            cleaned_img_path = os.path.join(cleaned_subdir, filename)
            img.save(cleaned_img_path)

            self.count_cleaned += 1

if __name__ == '__main__':
    cleaner = FlagsDatasetCleaner()
    cleaner.clean()