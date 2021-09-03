# Uros Krcadinac 2021
# Flag Generating App

import json
from flask import Flask, render_template, send_file, redirect, request
from bin.gg.flag_generator import GenFlag

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
n_flags = 30  # 1

@app.route("/")
def home():
    return render_template('flaglabs_home.html', params=[])


@app.route('/_generate')
def generate():
    data_txt = request.args.get('vector')
    data = json.loads(data_txt)
    svg_data = []
    for _ in range(n_flags):
        svg_data.append(GenFlag(raw_input=data, raw=True).svg_string())
        # svg_data.append(GenFlag().svg_string())
    svg_data_txt = json.dumps(svg_data)
    return svg_data_txt


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(host='127.0.0.1', debug=True)
