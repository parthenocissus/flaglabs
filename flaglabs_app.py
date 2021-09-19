# Uros Krcadinac 2021
# Flag Generating App

import json
import glob
import time
import random
from os import listdir
from os.path import isfile, join
from flask import Flask, render_template, request
from bin.gg.flag_generator import GenFlag

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
flag_set = []
n_flags = 30  # 1


def flag_mappings():
    input_ponders_path = 'conf/input-ponders.json'
    input_ponders = json.load(open(input_ponders_path))
    mappings = {}

    def data_for_type(t):
        if t == "unipolar":
            return {"min": 0, "max": 1, "step": 0.1, "value": 0}
        else:
            return {"min": -1, "max": 1, "step": 0.2, "value": 0}

    for p in input_ponders:
        md = input_ponders[p]['meta_data']
        mappings[p] = {
            "label": md['label'],
            "type": md['type'],
            "data": data_for_type(md['type'])
        }
    return json.dumps(mappings)


# URL Routes and Pages

@app.route("/")
def home():
    return render_template('flaglabs_home.html', params=flag_mappings())


@app.route("/fractals")
def fractals():
    return render_template('fractals.html', params=flag_mappings())


@app.route("/selected")
def selected():
    svg_data = []
    for file_name in glob.iglob("media/selected_flags/single/*"):
        svg = open(file_name, "r").read()
        svg_data.append(svg)
    return render_template('flags_selected.html', params=json.dumps(svg_data))


# API Services

@app.route('/_generate')
def generate():
    flag_set.clear()
    data_txt = request.args.get('vector')
    data = json.loads(data_txt)
    svg_data = []
    for i in range(n_flags):
        gf = GenFlag(raw_input=data, raw=True)
        flag_set.append(gf)
        svg = gf.svg_string()
        svg = f'{svg[:4]} id="flag{i}" {svg[5:]}'
        svg_data.append(svg)
    return json.dumps(svg_data)


@app.route('/_save')
def save():
    data_txt = request.args.get('vector')
    index = int(json.loads(data_txt))
    flag_set[index].save()
    # flag_set[index].save_svg_and_png()
    return json.dumps({"info": "success"})


@app.route('/_save_svg_string')
def save_svg_string():
    svg_text = json.loads(request.args.get('svg'))
    path = "media/selected_flags/fractal_composite"
    time_stamp = time.strftime("%Y%m%d-%H%M%S") + "-" + str(time.time() * 1000)
    file_name = f"{path}/{time_stamp}.svg"
    with open(file_name, 'w') as f:
        f.write(svg_text)
    return json.dumps({"info": "success"})


@app.route('/_get_from_database')
def get_from_database():
    n = int(json.loads(request.args.get('n')))
    svg_data = []
    path = "media/selected_flags/single"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for _ in range(n):
        file_name = random.choice(files)
        full_name = f"{path}/{file_name}"
        svg = open(full_name, "r").read()
        svg_data.append(svg)
    return json.dumps(svg_data)


@app.route('/_get_random')
def get_random():
    raw_input = json.loads(request.args.get('raw'))
    n = int(json.loads(request.args.get('n')))
    svg_data = []
    for _ in range(n):
        gf = GenFlag(raw_input=raw_input, raw=True)
        svg = gf.svg_string()
        # svg = f'{svg[:4]} id="flag{i}" {svg[5:]}'
        svg_data.append(svg)
    return json.dumps(svg_data)


# @app.route('/_get_mappings')
# def get_mappings():
#     data_txt = request.args.get('vector')
#     input_ponders_path = 'conf/input-ponders.json'
#     input_ponders = json.load(open(input_ponders_path))
#     mappings = {}
#
#     def data_for_type(t):
#         if t == "unipolar":
#             return {"min": 0, "max": 1, "step": 0.1, "value": 0}
#         else:
#             return {"min": -1, "max": 1, "step": 0.2, "value": 0}
#     for p in input_ponders:
#         md = input_ponders[p]['meta_data']
#         mappings[p] = {
#             "label": md['label'],
#             "type": md['type'],
#             "data": data_for_type(md['type'])
#         }
#     return json.dumps(mappings)


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
