import cv2
import numpy as np
from pybrain.supervised import BackpropTrainer
from pybrain import TanhLayer, SoftmaxLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork

import NNTrainData
import NNTestData

class NeuralNework:
    def __init__(self):
        self.encodingDict = {
            "can": [1, 0, 0],
            "stain": [0, 1, 0],
            "dirt": [0, 0, 1]
        }
        self.trainData = []

    def initializeNetwork(self):
        can1 = NNTrainData.NNTrainData(cv2.imread('NNTrain/can1.png'), self.encodingDict["can"])
        can2 = NNTrainData.NNTrainData(cv2.imread('NNTrain/can2.png'), self.encodingDict["can"])
        can3 = NNTrainData.NNTrainData(cv2.imread('NNTrain/can3.png'), self.encodingDict["can"])
        stain1 = NNTrainData.NNTrainData(cv2.imread('NNTrain/stain1.png'), self.encodingDict["stain"])
        stain2 = NNTrainData.NNTrainData(cv2.imread('NNTrain/stain2.png'), self.encodingDict["stain"])
        stain3 = NNTrainData.NNTrainData(cv2.imread('NNTrain/stain3.png'), self.encodingDict["stain"])
        dirt1 = NNTrainData.NNTrainData(cv2.imread('NNTrain/dirt1.png'), self.encodingDict["dirt"])
        dirt2 = NNTrainData.NNTrainData(cv2.imread('NNTrain/dirt2.png'), self.encodingDict["dirt"])
        dirt3 = NNTrainData.NNTrainData(cv2.imread('NNTrain/dirt3.png'), self.encodingDict["dirt"])

        self.trainData.append(can1)
        self.trainData.append(can2)
        self.trainData.append(can3)
        self.trainData.append(stain1)
        self.trainData.append(stain2)
        self.trainData.append(stain3)
        self.trainData.append(dirt1)
        self.trainData.append(dirt2)
        self.trainData.append(dirt3)

        for x in self.trainData:
            x.prepareTrainData()

        self.net = buildNetwork(4, 3, 3, hiddenclass=TanhLayer, outclass=SoftmaxLayer)
        ds = SupervisedDataSet(4, 3)

        for x in self.trainData:
            ds.addSample((x.contours/100.0, x.color[0]/1000.0, x.color[1]/1000.0, x.color[2]/1000.0), x.output)

        trainer = BackpropTrainer(self.net, momentum=0.1, verbose=True, weightdecay=0.01)
        trainer.trainOnDataset(ds, 1000)
        trainer.testOnData(verbose=True)
        print "\nSiec nauczona\n"

    def testNetwork(self, test):
        output = np.around(self.net.activate([test.contours/100.0, test.color[0]/1000.0, test.color[1]/1000.0, test.color[2]/1000.0]))
        for key, value in self.encodingDict.items():
            if (value == output).all():
                return key
