import json
from colour import Color


def list_colors():
    rules_path = 'conf/flag-rules.json'
    rules = json.load(open(rules_path))

    css_begin = '* {'
    css_end = '\n}'

    light_colors = '\n\n\t/* Light colors */'
    other_colors = '\n\n\t/* Mid-colors */'
    dark_colors = '\n\n\t/* Dark colors */'

    color_dict = {"particular_colors": {}}

    color_groups = rules['colors']
    for cg in color_groups:
        for v in cg['variations']:

            color = Color(v['value'])
            luminance = color.get_luminance()
            lum = "{:.2f}".format(luminance)
            css_color = f"\n\tcolor: {v['value']};  /* {v['name']}, {lum} */"

            if luminance < 0.4:
                dark_colors += css_color
                color_dict['particular_colors'][v['name']] = -1
            elif luminance > 0.5:
                light_colors += css_color
                color_dict['particular_colors'][v['name']] = 1
            else:
                other_colors += css_color



    css = css_begin + light_colors + other_colors + dark_colors + css_end
    with open('static/css/colors_list.css', 'w') as f:
        f.write(css)

    with open('media/tmp/colors_list.json', 'w') as f:
        json.dump(color_dict, f)


if __name__ == '__main__':
    list_colors()