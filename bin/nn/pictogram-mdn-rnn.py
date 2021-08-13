# https://colab.research.google.com/drive/1wuGHcJC2PiMs0hJ1g2SdjOs1r9Y_3MbL?usp=sharing

import keras
# from context import * # imports the MDN layer
import mdn
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# %matplotlib inline

# Converting SVG paths into numpy arrays

from svgpathtools import svg2paths, svg2paths2, wsvg
import numpy as np
import glob

media_path = 'flaglabs/media/svg-pictograms-stroke3/'


# media_path = 'flaglabs/media/svg-pictograms/'

# Compute the size of all points within all paths within a single SVG file
# So it can be used for defining the shape of an empty numpy array
def get_shape_size(ps):
    size = 0
    for path in ps:
        size += len(path) + 1
    return size


# Parsing SVGs into a numpy array for training
# (Without flipping, the flipping version is bellow)
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


# Parsing SVGs into a numpy array for training
# with flipping, so we can have 4 versions of a vector image
# out of 1 SVG file with that image
def parse_svg_pictograms_x4(media_path=media_path):
    svg_data = []

    float_formatter = "{:.2f}".format
    np.set_printoptions(formatter={'float_kind': float_formatter})

    # Going trough all SVG files in the media_path directory
    for f in glob.iglob(media_path + "/*"):
        print(f"\n_______\n{f}")
        paths, attributes, svg_attributes = svg2paths2(f)
        shape_size = get_shape_size(paths)
        points = np.zeros(shape=(shape_size, 3), dtype=float)
        points_xflip = np.zeros(shape=(shape_size, 3), dtype=float)
        points_yflip = np.zeros(shape=(shape_size, 3), dtype=float)
        points_xyflip = np.zeros(shape=(shape_size, 3), dtype=float)

        itr = 0
        current = {"x": 0, "y": 0}
        current_flip = {"x": 0, "y": 0}

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
                current = {"x": x, "y": y}

                x_flip = 17 - x
                y_flip = 35 - y
                dx_flip = x_flip - current_flip["x"]
                dy_flip = y_flip - current_flip["y"]
                points_xflip[itr] = [dx_flip, dy, pen_state]
                points_yflip[itr] = [dx, dy_flip, pen_state]
                points_xyflip[itr] = [dx_flip, dy_flip, pen_state]
                current_flip = {"x": x_flip, "y": y_flip}

                itr += 1

                if i2 == len(p) - 1:
                    x = item.end.real
                    y = item.end.imag
                    dx = x - current["x"]
                    dy = y - current["y"]
                    pen_state = 2.0 if i1 == len(paths) - 1 else 1.0
                    points[itr] = [dx, dy, pen_state]

                    current = {"x": x, "y": y}

                    x_flip = 17 - x
                    y_flip = 35 - y
                    dx_flip = x_flip - current_flip["x"]
                    dy_flip = y_flip - current_flip["y"]
                    points_xflip[itr] = [dx_flip, dy, pen_state]
                    points_yflip[itr] = [dx, dy_flip, pen_state]
                    points_xyflip[itr] = [dx_flip, dy_flip, pen_state]
                    current_flip = {"x": x_flip, "y": y_flip}

                    itr += 1

        svg_data.append(points)
        svg_data.append(points_xflip)
        svg_data.append(points_yflip)
        svg_data.append(points_xyflip)

    return np.array(svg_data, dtype=object)


tdata = parse_svg_pictograms_x4()
print(tdata)
for i in range(15):
    print(tdata[i].shape)

train_set = tdata
valid_set = tdata
test_set = tdata

# Have a look at the data.
example = train_set[16]
print("Shape:", example.shape)
print(example[:5])

plt.plot(example.T[0].cumsum(), -1 * example.T[1].cumsum())
plt.title("Accumulated values for one training example")
plt.show()


#Setting up an MDN RNN to learn how to create similar drawings.
#One dimension for `pen-X`, one for `pen-Y`, and one for `pen-UpDown`

# Training Hyperparameters:
SEQ_LEN = 100  # 30
BATCH_SIZE = 64
HIDDEN_UNITS = 256
EPOCHS = 1000
SEED = 2345  # set random seed for reproducibility
random.seed(SEED)
np.random.seed(SEED)
OUTPUT_DIMENSION = 3
NUMBER_MIXTURES = 10

# Sequential model
model = keras.Sequential()

# Add two LSTM layers, make sure the input shape of the first one is (?, 30, 3)
model.add(keras.layers.LSTM(HIDDEN_UNITS, batch_input_shape=(None, SEQ_LEN, OUTPUT_DIMENSION), return_sequences=True))
model.add(keras.layers.LSTM(HIDDEN_UNITS))

# Here's the MDN layer, need to specify the output dimension (3) and number of mixtures (10)
model.add(mdn.MDN(OUTPUT_DIMENSION, NUMBER_MIXTURES))

# Now we compile the MDN RNN - need to use a special loss function with the right number of dimensions and mixtures.
model.compile(loss=mdn.get_mixture_loss_func(OUTPUT_DIMENSION, NUMBER_MIXTURES), optimizer=keras.optimizers.Adam())

# Let's see what we have:
model.summary()


# Functions for slicing up data
def slice_sequence_examples(sequence, num_steps):
    xs = []
    for i in range(len(sequence) - num_steps - 1):
        example = sequence[i: i + num_steps]
        xs.append(example)
    return xs


def seq_to_singleton_format(examples):
    xs = []
    ys = []
    for ex in examples:
        xs.append(ex[:-1])
        ys.append(ex[-1])
    return (xs, ys)


# Prepare training data as X and Y.
slices = []
for seq in train_set:
    slices += slice_sequence_examples(seq, SEQ_LEN + 1)
X, y = seq_to_singleton_format(slices)

X = np.array(X)
y = np.array(y)

print("Number of training examples:")
print("X:", X.shape)
print("y:", y.shape)

# Train!
EPOCHS = 700
history = model.fit(X, y, batch_size=BATCH_SIZE, epochs=EPOCHS, callbacks=[keras.callbacks.TerminateOnNaN()])

# Plot
plt.figure()
plt.plot(history.history['loss'])
plt.show()

# Decoding Model
# Same as training model except for dimension and mixtures.
decoder = keras.Sequential()
decoder.add(
    keras.layers.LSTM(HIDDEN_UNITS, batch_input_shape=(1, 1, OUTPUT_DIMENSION), return_sequences=True, stateful=True))
decoder.add(keras.layers.LSTM(HIDDEN_UNITS, stateful=True))
decoder.add(mdn.MDN(OUTPUT_DIMENSION, NUMBER_MIXTURES))
decoder.compile(loss=mdn.get_mixture_loss_func(OUTPUT_DIMENSION, NUMBER_MIXTURES), optimizer=keras.optimizers.Adam())
decoder.summary()

decoder.set_weights(model.get_weights())

# Commented out IPython magic to ensure Python compatibility.
# Generating new drawings...
import pandas as pd
import matplotlib.pyplot as plt

def zero_start_position():
    # A zeroed out start position with pen down
    out = np.zeros((1, 1, 3), dtype=np.float32)
    out[0, 0, 2] = 1  # set pen down.
    return out

def generate_sketch(model, start_pos, num_points=100):
    return None

def cutoff_stroke(x):
    return np.greater(x, 0.5) * 1.0


def plot_sketch(sketch_array):
    # Plot a sketch quickly to see what it looks like.
    sketch_df = pd.DataFrame({'x': sketch_array.T[0], 'y': sketch_array.T[1], 'z': sketch_array.T[2]})
    sketch_df.x = sketch_df.x.cumsum()
    sketch_df.y = -1 * sketch_df.y.cumsum()

    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111)

    ax1.plot(sketch_df.x, sketch_df.y, 'r-')
    plt.show()


# Generating SVGs
# Via Hardmaru's Drawing Functions from write-rnn-tensorflow
# https://github.com/hardmaru/write-rnn-tensorflow/blob/master/utils.py
import svgwrite
from IPython.display import SVG, display


def get_bounds(data, factor):
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    abs_x = 0
    abs_y = 0
    for i in range(len(data)):
        x = float(data[i, 0]) / factor
        y = float(data[i, 1]) / factor
        abs_x += x
        abs_y += y
        min_x = min(min_x, abs_x)
        min_y = min(min_y, abs_y)
        max_x = max(max_x, abs_x)
        max_y = max(max_y, abs_y)

    return (min_x, max_x, min_y, max_y)


def draw_strokes(data, factor=1, svg_filename='sample.svg'):
    min_x, max_x, min_y, max_y = get_bounds(data, factor)
    dims = (50 + max_x - min_x, 50 + max_y - min_y)

    dwg = svgwrite.Drawing(svg_filename, size=dims)
    dwg.add(dwg.rect(insert=(0, 0), size=dims, fill='white'))

    lift_pen = 1

    abs_x = 25 - min_x
    abs_y = 25 - min_y
    p = "M%s,%s " % (abs_x, abs_y)

    command = "m"

    for i in range(len(data)):
        if (lift_pen == 1):
            command = "m"
        elif (command != "l"):
            command = "l"
        else:
            command = ""
        x = float(data[i, 0]) / factor
        y = float(data[i, 1]) / factor
        lift_pen = data[i, 2]
        p += command + str(x) + "," + str(y) + " "

    the_color = "black"
    stroke_width = 1

    dwg.add(dwg.path(p).stroke(the_color, stroke_width).fill("none"))

    dwg.save()
    display(SVG(dwg.tostring()))


# Predict a pictogram and plot the result.
temperature = 0.01
sigma_temp = 1.5

p = zero_start_position()
sketch = [p.reshape(3, )]

for i in range(150):
    params = decoder.predict(p.reshape(1, 1, 3))
    p = mdn.sample_from_output(params[0], OUTPUT_DIMENSION, NUMBER_MIXTURES, temp=temperature, sigma_temp=sigma_temp)
    sketch.append(p.reshape((3,)))

sketch = np.array(sketch)
decoder.reset_states()

sketch.T[2] = cutoff_stroke(sketch.T[2])
draw_strokes(sketch, factor=0.5)
# plot_sketch(sketch)