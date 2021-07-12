"""
Colab with GPU:
https://colab.research.google.com/drive/1F9JiSKNhISC2u4psqLCdxYOEmxSrA2vd?usp=sharing
"""

import tensorflow as tf
from tensorflow.keras.layers import Input, Reshape, Dropout, Dense
from tensorflow.keras.layers import Flatten, BatchNormalization
from tensorflow.keras.layers import Activation, ZeroPadding2D
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import UpSampling2D, Conv2D
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.optimizers import Adam
import numpy as np
from tqdm import tqdm
import os
import time
import matplotlib.pyplot as plt
import random
import glob
from PIL import Image, ImageFile
import requests
from io import BytesIO
from IPython.display import display, HTML

GENERATE_RES = 3  # Generation resolution factor
# (1=32, 2=64, 3=96, 4=128, etc.)
GENERATE_SQUARE = 32 * GENERATE_RES  # rows/cols (should be square)
IMAGE_CHANNELS = 4

images = []
training_data = []


def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return f"{h}:{m:>02}:{s:>05.2f}"


def fill_image(img, limit=200):
    w, h = img.size
    if w < limit:
        new_background = (255, 255, 255)
        tmp = Image.new(img.mode, (limit, h), new_background)
        tmp.paste(img, (0, 0, w, h))
        img = tmp
    elif w > limit:
        img = img.crop((0, 0, limit, h))
    return img


def fill_image_alpha(img, limit=200):
    w, h = img.size
    img.putalpha(255)
    if w < limit:
        new_background = (255, 255, 255, 0)
        tmp = Image.new(img.mode, (limit, h), new_background)
        tmp.paste(img, (0, 0, w, h))
        img = tmp
    elif w > limit:
        img = img.crop((0, 0, limit, h))
    return img


# for f in glob.iglob("/content/img/*"):
for f in glob.iglob("/media/flagtest/*"):
    img = Image.open(f)
    img.load()

    # img = fill_image(img)
    img = fill_image_alpha(img)

    img = img.resize((GENERATE_SQUARE, GENERATE_SQUARE), Image.ANTIALIAS)

    img_vect = np.asarray(img)
    print(img_vect.shape)
    plt.figure()
    plt.imshow(img_vect)

    training_data.append(img_vect)

# Preview image
PREVIEW_ROWS = 4
PREVIEW_COLS = 7
PREVIEW_MARGIN = 16

# Size vector to generate images from
SEED_SIZE = 100

# Configuration
EPOCHS = 5
BATCH_SIZE = 32
BUFFER_SIZE = 60000

training_data = np.reshape(training_data, (-1, GENERATE_SQUARE, GENERATE_SQUARE, IMAGE_CHANNELS))
training_data = training_data.astype(np.float32)
training_data = training_data / 127.5 - 1.

# print(training_data.shape)

# Batch and shuffle the data
train_dataset = tf.data.Dataset.from_tensor_slices(training_data) \
    .shuffle(BUFFER_SIZE).batch(BATCH_SIZE)


def build_generator(seed_size, channels):
    model = Sequential()

    model.add(Dense(4 * 4 * 256, activation="relu", input_dim=seed_size))
    model.add(Reshape((4, 4, 256)))

    model.add(UpSampling2D())
    model.add(Conv2D(256, kernel_size=3, padding="same"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Activation("relu"))

    model.add(UpSampling2D())
    model.add(Conv2D(256, kernel_size=3, padding="same"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Activation("relu"))

    # Output resolution, additional upsampling
    model.add(UpSampling2D())
    model.add(Conv2D(128, kernel_size=3, padding="same"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Activation("relu"))

    if GENERATE_RES > 1:
        model.add(UpSampling2D(size=(GENERATE_RES, GENERATE_RES)))
        model.add(Conv2D(128, kernel_size=3, padding="same"))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Activation("relu"))

    # Final CNN layer
    model.add(Conv2D(channels, kernel_size=3, padding="same"))
    model.add(Activation("tanh"))

    return model


def build_discriminator(image_shape):
    model = Sequential()

    model.add(Conv2D(32, kernel_size=3, strides=2, input_shape=image_shape,
                     padding="same"))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Dropout(0.25))
    model.add(Conv2D(64, kernel_size=3, strides=2, padding="same"))
    model.add(ZeroPadding2D(padding=((0, 1), (0, 1))))
    model.add(BatchNormalization(momentum=0.8))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Dropout(0.25))
    model.add(Conv2D(128, kernel_size=3, strides=2, padding="same"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Dropout(0.25))
    model.add(Conv2D(256, kernel_size=3, strides=1, padding="same"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Dropout(0.25))
    model.add(Conv2D(512, kernel_size=3, strides=1, padding="same"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))

    return model


def save_images(cnt, noise):
    image_array = np.full((
        PREVIEW_MARGIN + (PREVIEW_ROWS * (GENERATE_SQUARE + PREVIEW_MARGIN)),
        PREVIEW_MARGIN + (PREVIEW_COLS * (GENERATE_SQUARE + PREVIEW_MARGIN)), IMAGE_CHANNELS),
        255, dtype=np.uint8)

    generated_images = generator.predict(noise)

    generated_images = 0.5 * generated_images + 0.5

    image_count = 0
    for row in range(PREVIEW_ROWS):
        for col in range(PREVIEW_COLS):
            r = row * (GENERATE_SQUARE + 16) + PREVIEW_MARGIN
            c = col * (GENERATE_SQUARE + 16) + PREVIEW_MARGIN
            image_array[r:r + GENERATE_SQUARE, c:c + GENERATE_SQUARE] \
                = generated_images[image_count] * 255
            image_count += 1

    output_path = os.path.join(DATA_PATH, 'output')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    filename = os.path.join(output_path, f"train-{cnt}.png")
    im = Image.fromarray(image_array)
    im.save(filename)


generator = build_generator(SEED_SIZE, IMAGE_CHANNELS)

noise = tf.random.normal([1, SEED_SIZE])
generated_image = generator(noise, training=False)

plt.imshow(generated_image[0, :, :, 0])

image_shape = (GENERATE_SQUARE, GENERATE_SQUARE, IMAGE_CHANNELS)

discriminator = build_discriminator(image_shape)
decision = discriminator(generated_image)
print(decision)

# This method returns a helper function to compute cross entropy loss
cross_entropy = tf.keras.losses.BinaryCrossentropy()


def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss


def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output), fake_output)


generator_optimizer = tf.keras.optimizers.Adam(1.5e-4, 0.5)
discriminator_optimizer = tf.keras.optimizers.Adam(1.5e-4, 0.5)


# Notice the use of `tf.function`
# This annotation causes the function to be "compiled".
@tf.function
def train_step(images):
    seed = tf.random.normal([BATCH_SIZE, SEED_SIZE])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_images = generator(seed, training=True)

        real_output = discriminator(images, training=True)
        fake_output = discriminator(generated_images, training=True)

        gen_loss = generator_loss(fake_output)
        disc_loss = discriminator_loss(real_output, fake_output)

        gradients_of_generator = gen_tape.gradient( \
            gen_loss, generator.trainable_variables)
        gradients_of_discriminator = disc_tape.gradient( \
            disc_loss, discriminator.trainable_variables)

        generator_optimizer.apply_gradients(zip(
            gradients_of_generator, generator.trainable_variables))
        discriminator_optimizer.apply_gradients(zip(
            gradients_of_discriminator,
            discriminator.trainable_variables))
    return gen_loss, disc_loss


def train(dataset, epochs):
    fixed_seed = np.random.normal(0, 1, (PREVIEW_ROWS * PREVIEW_COLS,
                                         SEED_SIZE))
    start = time.time()

    for epoch in range(epochs):
        epoch_start = time.time()

        gen_loss_list = []
        disc_loss_list = []

        for image_batch in dataset:
            t = train_step(image_batch)
            gen_loss_list.append(t[0])
            disc_loss_list.append(t[1])

        g_loss = 0
        d_loss = 0

        if len(gen_loss_list) != 0:
            g_loss = sum(gen_loss_list) / len(gen_loss_list)

        if len(disc_loss_list) != 0:
            d_loss = sum(disc_loss_list) / len(disc_loss_list)


        epoch_elapsed = time.time() - epoch_start
        print(f'Epoch {epoch + 1}, gen loss={g_loss},disc loss={d_loss},' \
              ' {hms_string(epoch_elapsed)}')
        save_images(epoch, fixed_seed)

    elapsed = time.time() - start
    print(f'Training time: {hms_string(elapsed)}')


DATA_PATH = '/content/results'

# EPOCHS = 1000
train(train_dataset, EPOCHS)

# generator.save(os.path.join(DATA_PATH, "flag_generator.h5"))


def generate_random():
    fixed_seed = np.random.normal(0, 1, (PREVIEW_ROWS * PREVIEW_COLS, SEED_SIZE))
    image_array = np.full((GENERATE_SQUARE, GENERATE_SQUARE, IMAGE_CHANNELS), 255, dtype=np.uint8)

    generated_images = generator.predict(fixed_seed)
    generated_images = 0.5 * generated_images + 0.5
    gen_img = generated_images[0] * 255
    gen_img = gen_img.astype(np.uint8)

    output_path = os.path.join(DATA_PATH, 'output')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    rnd = random.randrange(1, 1000)
    filename = os.path.join(output_path, f"gen-{rnd}.png")
    im = Image.fromarray(gen_img)
    im = im.resize((GENERATE_SQUARE * 2, GENERATE_SQUARE), Image.ANTIALIAS)
    im.save(filename)

generate_random()