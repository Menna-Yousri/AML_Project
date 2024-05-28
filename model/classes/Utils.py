__author__ = 'Tony Beltramelli - www.tonybeltramelli.com'

import numpy as np
from PIL import Image

class Utils:
    @staticmethod
    def sparsify(label_vector, output_size):
        sparse_vector = []

        for label in label_vector:
            sparse_label = np.zeros(output_size)
            sparse_label[label] = 1

            sparse_vector.append(sparse_label)

        return np.array(sparse_vector)

    @staticmethod
    def get_preprocessed_img(img_path , image_size):
        img = Image.open(img_path).convert("RGB")
        img = img.resize((image_size , image_size))
        img = np.array(img , dtype='float32')
        img /= 255.0
        return img

    @staticmethod
    def show(image):
        import cv2
        cv2.namedWindow("view", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("view", image)
        cv2.waitKey(0)
        cv2.destroyWindow("view")
