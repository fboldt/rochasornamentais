from core.Classifier import Classifier
import joblib
import datetime
import os



class Model:
    def __init__(self,_classifier=None,_dictionary=None,_features=None,_labels=None,_seed=None,_acc=None,_label_map=None):
        self.classifier = _classifier
        self.dictionary = _dictionary
        self.features = _features
        self.labels = _labels
        self.seed = _seed
        self.acc = _acc
        self.label_map = _label_map

    def saveModel(self,_output=None,_path=None):
        if not _path:
            _path = ''
        else:
            if not os.path.exists(_path):
                raise Exception('Path not exists!:',_path)    
            else:
                if _path[-1] != '/':
                    _path += '/'
        if not _output:
            #VERSÂO FINAL DO NOME DOS MODELOS
            # now = datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
            now = datetime.datetime.now().strftime('%d-%m-%Y')
            _output = '{}model-{}-{:.5f}.joblib'.format(_path,now,self.acc)
        joblib.dump(self,_output)
        print('Model:',_output)
        
        
    def loadModel(self,_file):
        if os.path.exists(_file):            
            aux = joblib.load(_file)
            self.classifier = aux.classifier
            self.acc = aux.acc
            self.dictionary = aux.dictionary
            self.features = aux.features
            self.labels = aux.labels
            self.seed = aux.seed
            try:
                self.label_map = aux.label_map
            except AttributeError:
                pass

        else:
            raise Exception('Model file not exists!')