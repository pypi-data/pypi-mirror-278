# 각 파라미터 별 타입 지정 필요

import os
import pickle
import joblib
import datetime
import numpy as np
import importlib

from sklearn.metrics import r2_score as r2
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae
from hyperopt import hp

basePath = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), os.path.pardir)))
commonPath = os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), os.path.pardir), os.path.pardir), os.path.pardir), "common"))

def rmse(y_test, y_pred):
    return np.sqrt(mse(y_test, y_pred))    
  
def fit(func):
    def wrapper(self, X, y, log=None, saveYn=False):

        # 함수 호출
        model = func(self, X, y)
        if saveYn:
            pickle.dump(model, open(self.saveMdlPath, 'wb'))

        return model
    return wrapper


def validation(func):
    def wrapper(self, xTest:list,  yTest=None, model=None, log=None):
        output =  {
            "status": 200,
            "massage": "",
            "result": {
                "r2": None,
                "mse": None,
                "mae": None,
                "rmse": None,
                "endTime": None,
                "dur": None
            },
            "score": None,
            "yPred": []
        }

            
        # 함수 호출
        yPred = func(self, xTest, yTest, model)
        if yTest is None:
            return yPred
        
        try:
          if np.array(yPred).ndim != 1:
            yPred = np.array(yPred).flatten().tolist()
            
          endTime = datetime.datetime.now()
          output["yPred"] = yPred
          output["result"]["r2"] = r2(yTest, yPred)
          output["result"]["mse"] = mse(yTest, yPred)
          output["result"]["mae"] = mae(yTest, yPred)
          output["result"]["rmse"] = rmse(yTest, yPred)
          output["result"]["endTime"] = endTime.astimezone().replace(microsecond=0).isoformat()
          output["result"]["startTime"] =  self.startTime.astimezone().replace(microsecond=0).isoformat()
          output["result"]["dur"] = float("{:.4f}".format(endTime.timestamp() - self.startTime.timestamp()))          
          
        except Exception as e:
          output["status"] = 400
          output["message"] = str(e)
          
        monitorName = str(self.scoreMethod)
        score = output["result"][monitorName.lower()]
        return output, yPred, score
    return wrapper


# ===========================데코레이터 활용===========================
# learningModel 정의
def wedaLearningModel(func):
    def init(self, startTime:datetime, param_grid:dict={}, param:dict={}, log=None):
        self.param = param
        self.param_grid = param_grid
        self.scoreMethod = param.get("scoreMethod", "r2")
        self.weightPath = self.param["pathInfo"].get("weightPath", "./")
        self.saveMdlPath = os.path.join(self.weightPath, "weight.pkl")
        
        self.log = log
        self.startTime = startTime
        self.params = {}

        os.makedirs(self.weightPath, exist_ok=True)
        
        if 'n_estimators' in self.param_grid.keys():
            self.epochs = self.param_grid["n_estimators"]
        elif 'max_iter' in self.param_grid.keys():
            self.epochs = self.param_grid["max_iter"]
        elif 'n_neighbors' in self.param_grid.keys():
            self.epochs = self.param_grid["n_neighbors"]
        elif 'iterations' in self.param_grid.keys():
            self.epochs = self.param_grid["iterations"]
        else:
            self.epochs = 0

        self.epochs = int(self.epochs)
        self.fstEpochStartTime = 0
        self.fstEpochEndTime = 0
        self.model = self.createModel()
        

    def getSpace(hyperParamScheme={}):
        space = {}

        # learningModel.getSpace() 대신
        for key, value in hyperParamScheme.items():
            if value.get("q", "") != "":
                if value["type"] == "int":
                    space[key] = hp.quniform(key, value["min"], value["max"], value["q"])
                elif value["type"] == "float":
                    space[key] = hp.quniform(key, value["min"], value["max"], value["q"])
            else:
                if value["type"] == "int":
                    space[key] = hp.uniform(key, value["min"], value["max"])

                elif value["type"] == "float":
                    space[key] = hp.uniform(key, value["min"], value["max"])

                elif value["type"] == "str":
                    space[key] = hp.choice(key, value["value"])
        return space
    
    setattr(func, '__init__', init)
    setattr(func, 'getSpace', getSpace)
    return func
        
  
def predictor(func):
    def init(self, param, log=None):
        self.saveMdlPath = os.path.join(param, "weight.pkl")
        self.model =  joblib.load(open(self.saveMdlPath, "rb"))

    setattr(func, '__init__', init)
    return func
        
def runPredict(func):
    def wrapper(self, model, xTest:list, yTest:list=None, log=None):

        output =  {
            "status": 200,
            "massage": "",
            "result": {},
        }

        # 함수 호출
        yPred = func(self, model, xTest)

        try:
            if np.array(yPred).ndim != 1:
                yPred = np.array(yPred).flatten().tolist()
            
            output["result"]["yPred"] = yPred
            output["result"]["score"] = None
        
        except Exception as e:
            output["status"] = 400
            output["message"] = str(e)
        finally:
            return output
    return wrapper