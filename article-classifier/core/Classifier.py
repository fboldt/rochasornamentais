import sklearn
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import NearestNeighbors,KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import precision_score,f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
import random
import spacy
import pickle
import datetime
from scipy import io, sparse
import joblib
import json


class Classifier:    
    def __init__(self):
        self.algorithm = None
        
    def trainModel(self,_data,_labels):
        self.algorithm.fit(_data,_labels)

    def setAlgorithm(self, _algorithm):
        if _algorithm == 'randomForest':
            self.name = 'randomForest'
            self.algorithm = RandomForestClassifier()
        elif _algorithm == 'knn':
            self.name = 'knn'
            self.algorithm = KNeighborsClassifier()
        elif not _algorithm:
            raise Exception('Error: Algorithm not set!')
    
