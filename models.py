## TODO: define the convolutional neural network architecture

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I


class Net(nn.Module):

    def __init__(self, num_classes=136):
        super(Net, self).__init__()

        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs

        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, 3),
            nn.ReLU(True),
            nn.MaxPool2d(2, 2),
            nn.Dropout2d(0.1),

            nn.Conv2d(32, 64, 2),
            # nn.BatchNorm2d(64),
            nn.ReLU(True),
            nn.MaxPool2d(2, 2),
            nn.Dropout2d(0.2),

            nn.Conv2d(64, 128, 2),
            # nn.BatchNorm2d(128),
            nn.ReLU(True),
            nn.MaxPool2d(2, 2),
            nn.Dropout2d(0.3)

            # nn.Conv2d(128, 256, 3, padding=1),
            # nn.BatchNorm2d(256),
            # nn.ReLU(True),
            # nn.MaxPool2d(2, 2)
        )

        self.n_features = 128 * 11 * 11

        self.classifier = nn.Sequential(
            # nn.Dropout(),
            nn.Linear(self.n_features, 2048),
            nn.ReLU(True),
            nn.Dropout(),

            nn.Linear(2048, 2048),
            nn.ReLU(True),

            nn.Linear(2048, num_classes),
        )

        for m in self.modules():
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight.data)
                m.bias.data.fill_(0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)


        ## Note that among the layers to add, consider including:
        # maxpooling layers, multiple conv layers, fully-connected layers, and other layers (such as dropout or batch normalization) to avoid overfitting

    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:
        ## x = self.pool(F.relu(self.conv1(x)))
        x = self.features(x)
        x = x.view(x.size(0), self.n_features)
        x = self.classifier(x)

        # a modified x, having gone through all the layers of your model, should be returned
        return x
