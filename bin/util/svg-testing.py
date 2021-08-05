from svgpathtools import svg2paths, svg2paths2, wsvg
import numpy as np
import glob

svg_ext = '.svg'
media_path = 'media/svg-pictograms/'

# paths, attributes = svg2paths(file_name)

svg_data = []

for f in glob.iglob(media_path + "/*"):
    print(f"\n_______\n{f}")
    paths, attributes, svg_attributes = svg2paths2(f)
    single_file_svg_data = []
    for i, p in enumerate(paths):
        print(f"\npath{i}")
        print(p)
        path_segments = []
        for item in p:
            # print(item)
            points = []
            for part in item:
                points.append(part.real)
                points.append(part.imag)
                # print(f"[{part.real}, {part.imag}]")
            path_segments.append(points)
        single_file_svg_data.append(path_segments)
    svg_data.append(single_file_svg_data)

print("\n\nraw svg data:")
print(svg_data)

print("\n\nsvg data as a basic numpy array:")
data = np.array(svg_data, dtype=object)
print(data)

# saving to a new file...
# wsvg(paths, attributes=attributes, svg_attributes=svg_attributes, filename=output_file)