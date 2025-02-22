#!/usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import
__author__ = 'Tony Beltramelli - www.tonybeltramelli.com'
#modified pix2code to pix2code2

import sys
from PIL import Image
from os.path import basename
from classes.Sampler import *
from classes.model.pix2code2 import *

argv = sys.argv[1:]

if len(argv) < 4:
    print("Error: not enough argument supplied:")
    print("sample.py <trained weights path> <trained model name> <input image> <output path> <search method (default: greedy)>")
    exit(0)
else:
    trained_weights_path = argv[0]
    trained_model_name = argv[1]
    input_path = argv[2]
    output_path = argv[3]
    search_method = "greedy" if len(argv) < 5 else argv[4]

meta_dataset = np.load("{}/meta_dataset.npy".format(trained_weights_path))
input_shape = meta_dataset[0]
output_size = meta_dataset[1]

#changed the pix2code model to pix2code2
model = pix2code2(input_shape, output_size, trained_weights_path)
model.load(trained_model_name)
print("loaded")

sampler = Sampler(trained_weights_path, input_shape, output_size, CONTEXT_LENGTH)

file_name = basename(input_path)[:basename(input_path).find(".")]
print(input_path)



def get_preprocessed_img(img_path, image_size):
    img = Image.open(img_path).convert("RGB")
    img = img.resize((image_size, image_size))
    img = np.array(img, dtype='float32')
    img /= 255.0
    return img

evaluation_img = get_preprocessed_img(input_path, IMAGE_SIZE)


if search_method == "greedy":
    result, _ = sampler.predict_greedy(model, np.array([evaluation_img]))
    print("Result greedy: {}".format(result))
else:
    beam_width = int(search_method)
    print("Search with beam width: {}".format(beam_width))
    result, _ = sampler.predict_beam_search(model, np.array([evaluation_img]), beam_width=beam_width)
    print("Result beam: {}".format(result))


with open("{}/{}.gui".format(output_path, file_name), 'w') as out_f:
    out_f.write(result.replace(START_TOKEN, "").replace(END_TOKEN, ""))
