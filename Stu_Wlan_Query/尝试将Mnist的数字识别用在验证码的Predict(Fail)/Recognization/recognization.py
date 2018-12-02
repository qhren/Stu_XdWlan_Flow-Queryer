import numpy as np
import json
import cv2
import settings
from Recognization.sigmoid import sigmoid
from Recognization.Soft_Max import soft_max


class FigureRecognization(object):
    '''
    :input a 784*1 vector
    :return a figure represents the picture
    '''
    def __init__(self, x):
        self.sizes, self.weights, self.biases = FigureRecognization.load_data()
        self.result = self.feed_forward(x)

    @staticmethod
    def load_data():
        with open("%sMnist_Data" % settings.Recognization_Data_Path, 'r') as fp:
            dict_data = json.load(fp)
        sizes = dict_data["sizes"]
        weights = [np.array(dict_data["weights"][page]) for page in range(len(dict_data["weights"]))]
        biases = [np.array(dict_data["biases"][page]) for page in range(len(dict_data["biases"]))]
        return sizes, weights, biases

    def feed_forward(self, x):
        a = x
        for w, b in zip(self.weights[:-1], self.biases[:-1]):
            a = sigmoid(np.dot(w, a) + b)
        a = soft_max(np.dot(self.weights[-1], a) + self.biases[-1])
        return a.argmax()


if __name__ == "__main__":
    temp_image = cv2.imread("%schar%d.png" % (settings.Project_Path + settings.Cutout_Path, 0), 0)
    Input = np.reshape(temp_image, (784, 1)) / 255
    Object = FigureRecognization(Input)
    results = Object.result
