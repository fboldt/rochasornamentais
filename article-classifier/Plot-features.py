from core.Classifier import Classifier
from core.Util import *
from core.Model import Model
import xlrd
import scipy
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.model_selection import StratifiedKFold
from tqdm import tqdm
import random
import csv
import sys
import os
from joblib import Parallel, delayed
import argparse
import datetime




importances = bModel.classifier.algorithm.feature_importances_
std = np.std([tree.feature_importances_ for tree in bModel.classifier.algorithm.estimators_],
     axis=0)
indices = np.argsort(importances)[::-1]
aux  = []
for i in indices[:50]:
    for word in bModel.dictionary:
        if bModel.dictionary[word]['id'] == i:
            aux.append(word)
            continue
plt.figure()
plt.title("Model:{} - Acc:{:.4}".format(bModel.classifier.name,bModel.acc))
plt.bar(range(50), importances[indices[:50]],
       color="g",  align="center")
plt.xticks(range(50), aux,rotation=90)
plt.xlim([-1, 50])
plt.show()

