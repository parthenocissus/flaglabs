# Uros Krcadinac 2021
# Flag Generating App

import json
import glob
from flask import Flask, render_template, request
from bin.gg.flag_generator import GenFlag

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
flag_set = []
n_flags = 36  # 1


@app.route("/")
def home():
    return render_template('flaglabs_home.html', params=[])


@app.route("/fractals")
def fractals():
    return render_template('fractals.html', params=[])


@app.route("/selected")
def selected():
    return render_template('flags_selected.html', params=[])


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


@app.route('/_get_selected')
def get_selected():
    request.args.get('vector')
    svg_data = []
    for file_name in glob.iglob("media/selected_flags/*"):
        file = open(file_name, "r")
        svg = file.read()
        svg_data.append(svg)
    return json.dumps(svg_data)


@app.route('/_get_random_selected')
def get_random_selected():
    request.args.get('vector')
    svg_data = []

    files = [
        "media/selected_flags/001.svg",
        "media/selected_flags/002.svg",
        "media/selected_flags/003.svg",
        "media/selected_flags/004.svg"
    ]
    for f in files:
        # file = open(f, "r")
        svg_data.append(open(f, "r").read())
    return json.dumps(svg_data)


@app.route('/_get_random')
def get_random():
    data_txt = request.args.get('vector')
    n = int(json.loads(data_txt))
    svg_data = []
    for i in range(n):
        gf = GenFlag()
        svg = gf.svg_string()
        # svg = f'{svg[:4]} id="flag{i}" {svg[5:]}'
        svg_data.append(svg)
    return json.dumps(svg_data)


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(host='127.0.0.1', debug=True)
