# Converting SVG paths into numpy arrays

from svgpathtools import svg2paths, svg2paths2, wsvg
import numpy as np
import glob

# media_path = 'media/svg-pictograms-stroke3-tst/'
media_path = 'media/svg-pictograms-stroke3/'

# Compute the size of all points within all paths within a single SVG file
# So it can be used for defining the shape of an empty numpy array
def get_shape_size(ps):
    size = 0
    for path in ps:
        size += len(path) + 1
    return size


# Parsing SVGs into a numpy array for training
def parse_svg_pictograms(media_path=media_path):

    svg_data = []

    float_formatter = "{:.2f}".format
    np.set_printoptions(formatter={'float_kind': float_formatter})

    # Going trough all SVG files in the media_path directory
    for f in glob.iglob(media_path + "/*"):
        print(f"\n_______\n{f}")
        paths, attributes, svg_attributes = svg2paths2(f)
        shape_size = get_shape_size(paths)
        points = np.zeros(shape=(shape_size, 3), dtype=float)

        itr = 0
        current = {"x": 0, "y": 0}

        # Now going through all path within a single file
        for i1, p in enumerate(paths):

            # Now through all path segmets, that is all cubic bezier objects
            for i2, item in enumerate(p):
                x = item.start.real
                y = item.start.imag
                dx = x - current["x"]
                dy = y - current["y"]
                pen_state = 0.0
                points[itr] = [dx, dy, pen_state]
                itr += 1
                current = {"x": x, "y": y}

                if i2 == len(p) - 1:
                    x = item.end.real
                    y = item.end.imag
                    dx = x - current["x"]
                    dy = y - current["y"]
                    pen_state = 2.0 if i1 == len(paths) - 1 else 1.0
                    points[itr] = [dx, dy, pen_state]
                    itr += 1
                    current = {"x": x, "y": y}

        svg_data.append(points)

    return np.array(svg_data, dtype=object)


data = parse_svg_pictograms()
print(data)
