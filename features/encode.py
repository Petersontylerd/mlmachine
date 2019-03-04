
import sklearn.base as base
import sklearn.preprocessing as preprocessing

import numpy as np
import pandas as pd

# from mlmachine import Machine

from collections import defaultdict

def cleanLabel(self, reverse = False):
    """

    """
    if self.targetType == 'continuous':
        self.y_ = self.y_.values.reshape(-1)
    elif self.targetType == 'categorical':
        self.le_ = prepocessing.LabelEncoder()

        self.y_ = self.le_.fit_transform(self.y_.values.reshape(-1))
        
        print('******************\nCategorical label encoding\n')
        for origLbl, encLbl in zip(np.sort(self.le_.classes_), np.sort(np.unique(self.y_))):
            print('{} --> {}'.format(origLbl, encLbl))

    if reverse:
        self.y_ = self.le_.inverse_transform(self.y_)

class NomCatFeatureDummies(base.TransformerMixin, base.BaseEstimator):
    """

    """
    def __init__(self, nomCatCols, dropFirst = True):
        self.nomCatCols = nomCatCols
        self.dropFirst = dropFirst
    
    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        X = pd.get_dummies(data = X, columns = self.nomCatCols, drop_first = self.dropFirst)
        return X

class OrdCatFeatureEncoder(base.TransformerMixin, base.BaseEstimator):
    """
    
    """
    def __init__(self, ordCatCols, train = True, classDict = None):
        """
        Info:
            Description:
                Encode ordinal categorical columns. Capable of fit_transforming
                new data, as well as transforming validation data with the same
                encodings.
            Parameters:
                ordCatCols : list
                    List of features to be encoded
                train : boolean, default = True
                    Controls whether to fit_transform training data or
                    transform validation data using encoder fit on 
                    training data
                classDict : dict, default = None
                    Dictionary containing feature : LabelEncoder() pairs to be used
                    to transform validation data. Only used when train = False.
        """        
        self.ordCatCols = ordCatCols
        self.train = train
        self.classDict = classDict

        self.d_ = defaultdict(preprocessing.LabelEncoder)
    
    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        # Encode training data
        if self.train:
            X[self.ordCatCols] = X[self.ordCatCols].apply(lambda x: self.d_[x.name].fit_transform(x))
        # Encode validation data with training data encodings.
        else:
            X[self.ordCatCols] = X[self.ordCatCols].apply(lambda x: self.classDict[x.name].transform(x))
        return X

class testSetMissingLevel(base.TransformerMixin, base.BaseEstimator):
    """

    """
    def __init__(self, trainCols):
        self.trainCols = trainCols
        
    def fit(self, X, y = None):
        return self
    
    def transform(self, X):
        missingLevels = set(self.trainCols) - set(X.columns)
        for c in missingLevels:
            X[c] = 0
        X = X[self.trainCols]
        return X
