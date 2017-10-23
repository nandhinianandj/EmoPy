import matplotlib.pyplot as plt

from skimage.feature import hog
from skimage import data, color, exposure, io

from sknn.mlp import Regressor, Convolution, Layer

import numpy as np



def extractFeatureVector(imageFile, verbose=False):
    image = io.imread(imageFile)
    image = color.rgb2gray(image)
    featureVector, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualise=True) #, transform_sqrt=True, feature_vector=False)

    if (verbose):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

        ax1.axis('off')
        ax1.imshow(image, cmap=plt.cm.gray)
        ax1.set_title('Input image')
        ax1.set_adjustable('box-forced')

        # Rescale histogram for better display
        hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))

        ax2.axis('off')
        ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
        ax2.set_title('Histogram of Oriented Gradients')
        ax1.set_adjustable('box-forced')
        plt.show()

    return featureVector


def getNeuralNet():
    hiddenLayer = Layer('Sigmoid', units=10) # channels=10, kernel_shape=(1,10800), kernel_stride=(1,10800))
    outputLayer = Layer('Linear')
    #outputLayer = Convolution('Sigmoid', channels=1, kernel_shape=(1,10800), kernel_stride=(1,10800))
    net = Regressor(layers=[hiddenLayer, outputLayer], learning_rate=0.01, n_iter=20)
    return net


def train(net, x_train=None, y_train=None):
    x_train = np.array([extractFeatureVector('/Users/aperez/Documents/TW/RIOT/Riot_python/images/S502_001_00000001.png')])
    y_train = np.ndarray([1])
    net.fit(x_train, y_train)

def main():
    imageFile = '/Users/aperez/Documents/TW/RIOT/Riot_python/images/S502_001_00000010.png'
    featureVector = np.array([extractFeatureVector(imageFile, verbose=False)])
    net = getNeuralNet()
    train(net)
    print "Prediction: " + str(net.predict(featureVector))



main()