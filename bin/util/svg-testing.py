# Converting SVG paths into numpy arrays

from svgpathtools import svg2paths, svg2paths2, wsvg
import numpy as np
import glob

svg_ext = '.svg'
media_path = 'media/svg-pictograms/'

# paths, attributes = svg2paths(file_name)

svg_data = []

# Going trough all SVG files in the "media/svg-pictograms" directory
for f in glob.iglob(media_path + "/*"):
    print(f"\n_______\n{f}")
    paths, attributes, svg_attributes = svg2paths2(f)
    single_file_svg_data = []

    # Now going through all path within a single file
    for i, p in enumerate(paths):
        print(f"\npath{i}")
        print(p)
        path_segments = []

        # Now through all path segmets, that is all cubic bezier objects
        for item in p:
            # print(item)
            points = []

            # Now through all points (x, y) in a within a signle cubic bezier path segment,
            # points that consist of a real part and an imaginary part,
            # since they are defined as complex numbers with 2 pars
            for part in item:
                points.append(part.real)
                points.append(part.imag)
                # print(f"[{part.real}, {part.imag}]")

            # Appending all arrays in a nested fashion
            path_segments.append(points)
        single_file_svg_data.append(path_segments)
    svg_data.append(single_file_svg_data)

# Printing number data, as a basic Python nested array
print("\n\nraw svg data:")
print(svg_data)

# Now to covert it into a numpy array
# (This np array will need to be reshaped!)
print("\n\nsvg data as a basic numpy array:")
data = np.array(svg_data, dtype=object)
print(data)

# Saving to a new file...
# wsvg(paths, attributes=attributes, svg_attributes=svg_attributes, filename=output_file)