'''
<다른 부분>
1. xai
2. graph
3. model output?
4. hpo convert 
5. model : hpo setting

<동일한 부분>
runTrain
runHpo
getTrainResult(안에서 fit, graph, xai 실행함)

<분류>
purposeType: reg, clf, clu, time 별로 그래프, xai fit 결과 다름
각 purposeType 안에서도 모델 별로 graph, xai, hpo다름
'''

import os
import sys
import time
import json
import numpy as np
import datetime
import pathlib
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import shap
import joblib


basePath = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), os.path.pardir)))
modelPath = os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), os.path.pardir), os.path.pardir), "modeldata/WEDA-Custom")) # modeldata 위치

sys.path.append(os.path.join(modelPath, "model"))
sys.path.append(os.path.join(modelPath, "bin"))
sys.path.append(os.path.join(basePath, "datalib"))
sys.path.append(os.path.join(basePath, "utils"))
sys.path.append(os.path.join(basePath, "decorator"))

from model import learningModel
from train import modelGraph, convertParam

from dataLib import dataLib
from utils import utils
from sender import sendMsg
from logger.Logger import Logger

from error.WedaErrorDecorator import WedaErrorDecorator
from logger.WedaLogDecorator import WedaLogDecorator
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials, STATUS_FAIL



class trainer():
  # @WedaLogDecorator(text="Train Start...", logLevel="info")
  def __init__(self, param, xTrain, xTest, yTrain, yTest, xHoldout, yHoldout, log, lm=None):
    self.model = None
    self.startTime = time.time()
    self.param = param
    self.dataInfo = param["dataInfo"] if "dataInfo" in param else None
    self.serverParam = param["serverParam"] if "serverParam" in param else None
    self.selectedHyperParam = utils.getHyperParam(param["selectedHyperParam"], modelPath) if param["selectedHyperParam"] else param["selectedHyperParam"]

    # self.modelInfo = param["dataInfo"]
    self.timeColumn = self.dataInfo.get("timeColumn", "")
    self.purposeType = self.dataInfo["purposeType"]
    self.labelColumnNm = self.dataInfo["targetColumn"]
    self.labelColumnNms = [ i["className"] for i in param["dataInfo"].get("classInfo", []) ]
    self.encodeData = self.dataInfo["encodeData"]
    self.columnNms = self.dataInfo["columnNameList"]

    self.originColumnNms = self.dataInfo["originColumnNameList"]
    if self.labelColumnNm in  self.originColumnNms:
      self.originColumnNms.remove(self.labelColumnNm)

    self.columnTypeDict = self.param.get("columnTypeDict", {})
    if not self.columnTypeDict:
      for i in self.dataInfo["columnList"]:
        self.columnTypeDict[i["columnName"]] = i["columnType"]
    self.param["columnTypeDict"] = self.columnTypeDict

    # 애매한 변수들
    self.customLM = lm
    
    # 데이터셋
    self.xTrain = xTrain
    self.xTest = xTest
    self.yTrain = yTrain
    self.yTest = yTest
    self.xHoldout = xHoldout
    self.yHoldout = yHoldout
    
    self.tryCount = 0
    self.orgLogPath = pathlib.Path(param["pathInfo"]["logPath"])
    self.log = log
    
    # 모델 저장
    self.weightPath = self.param["pathInfo"]["weightPath"]
    self.saveMdlPath = os.path.join(self.weightPath, "weight.pkl")
    

  def hyperParamTuning(self, space):
    output = {
      "status": 200,
      "message": "",
      "extTime": None,
      "result": None,
    }

    st = time.time()
    startTime = datetime.datetime.now()

    try:
      model = learningModel(
        param_grid=space,
        param=self.param,
        log=self.log,
        startTime=startTime
      )
      model.setSpaceType()
      self.model = model.new_fit(X=self.xTrain, y=self.yTrain, log=log, saveYn=False)
      output, yPred, score = model.validation(xTrain=self.xTrain, xTest=self.xTest, yTrain=self.yTrain, yTest=self.yTest, model=self.model, log=log)
      print(score)
      return {"loss": 1 - score, "status": STATUS_OK, "model": model}
    except:
      return {"status": STATUS_FAIL}

  @WedaLogDecorator(text="Running Trainer...", logLevel="info")
  def getTrainResult(self, sendResultUrl, startTime, log):
    output = {
        "status": 200,
        "message": "",
        "extTime": None,
        "result": None,
    }

    param_grid = self.selectedHyperParam
    
    # learningModel 정의
    model = learningModel(
        param_grid=param_grid,
        param=self.param,
        log=self.log,
        startTime=startTime
    )

    self.model = model.fit(X=self.xTrain, y=self.yTrain)
    pickle.dump(self.model, open(self.saveMdlPath, 'wb')) 

    if self.purposeType=="timeSeries":
      output = model.validation(xTest=self.xHoldout, yTest=self.yHoldout, model=self.model, log=log)
    else:
      output = model.validation(xTest=self.xTest, yTest=self.yTest, model=self.model, log=log)

    output["yPred"] = output["yPred"]
    output["score"] = output["score"]
    
    _ = sendMsg(sendResultUrl, output, "TRAIN", log)
    return output
      
      
  def getGraphResult(self, result, sendResultUrl, log):
      output = {
          "status": 200,
          "message": "",
          "extTime": None,
          "result": None,
      }
      score = result["score"]
      yPred = result["yPred"]
      
      yPred = list(map(lambda x: round(x, 4), yPred))
      print(score)
      
      mG = modelGraph(self.param, self.xTrain, self.xTest, self.yTrain, self.yTest, self.xHoldout, self.yHoldout, self.model, log)

      graphResult = mG.getGraphData(yPred=yPred, score=score, model=self.model, log=log)

      output["result"] = graphResult["result"]
      output["selectedHyperParam"] = self.selectedHyperParam

      _ = sendMsg(sendResultUrl, output, "GRAPH", log)

      partialDict, columnFlag = mG.makeFeatureEffect(log=log)
      xaiResult = mG.getXAIData(yPred=yPred, partialDict=partialDict, columnFlag=columnFlag, log=log)

      output["result"] = xaiResult["result"]
      output["extTime"] = time.time() - self.startTime
      _ = sendMsg(sendResultUrl, output, "XAI", log)
      
      return output


# opr에서 모델 입출력 스키마 정의
def setModelInfo(scheme):
    subList = []
    for i in scheme["dataInfo"]["columnList"]:
      subList.append({
        "type": "string" if i["columnType"] == "string" else "number",
        "name": i["columnName"]
      })

    inputScheme = [
      {
        "type": "object",
        "name": "opData",
        "subObject": [
          {
            "type": "array",
            "name": "header",
            "subList": subList
          },
          {
            "type": "array",
            "name": "xTest"
          }
        ]
      }
    ]
    
    # output 타입, 분류 등 다른 모델에서 OPR에서 다르게 나올 경우 수정 필요
    subList.append({
          "type": "string",
          "name": "errMessage"
        })
    subList.append({        
          "type": "number",
          "name": "label"
        })
    subList.append(                   
        {
          "type": "number",
          "name": "accuracy"
        })
    
    outputScheme = [
    {
      "type": "array",
      "name": "opResult",
      "subList": subList
    },
    {
      "type": "string",
      "name": "modelId"
    }
  ]
    with open(os.path.join(modelPath, "modelInfo.json"), "r+") as jsonFile:
      file_data = json.load(jsonFile)
      file_data["ioScheme"] = {}
      file_data["ioScheme"]["inputScheme"] = inputScheme
      file_data["ioScheme"]["outputScheme"] = outputScheme
      jsonFile.seek(0)
      json.dump(file_data, jsonFile, indent = 4)
      

def runCustomTrain(params, df, startTime, sendResultUrl, lm, log):
  
  dl = dataLib(params, log)
  data = dl.getData(log=log, dataFrame=df)
  
  xTrain = data["result"]["xTrain"]
  xTest = data["result"]["xTest"]
  yTrain = data["result"]["yTrain"]
  yTest = data["result"]["yTest"]
  
  t = trainer(param=params, xTrain=xTrain, xTest=xTest, yTrain=yTrain, yTest=yTest, lm=lm, startTime=startTime)
  output = t.getTrainResult(startTime=startTime, hpoTf=False, sendResultUrl=sendResultUrl, log=log)
  
  with open(os.path.join(basePath, "param.json"), "w") as jsonFile:
    json.dump(t.param, jsonFile, ensure_ascii=False)
    
  return output


def train(
            df=pd.DataFrame(),
            lm=None,
            target:str="",
            graph:bool=False,
            xai:bool=False,
            splitInfo:int=70,
            hyperParams:dict={},
            savePath:str="./",
            graphList:list = [], 
            hyperParamSheme: dict = {},
            *args,
            **kwargs
          ):
  '''
    df : 학습할 dataframe
    lm : 사용자가 정의한 lm 클래스
    target : 학습 타겟
    graph : 그래프 계산 유무
    xai : xai 계산 유무
    splitInfo : 학습, 테스트 비율
    hyperParams : 모델의 하이퍼 파라미터
    graphList: grapTf가 True일 떄 그릴 그래프 종류 (reg: regPlot, distribution Plot, Feature Importance)
    savePath: 모델, 그래프 등등 저장할 경로
  '''

  
  startTime = datetime.datetime.now()
  if target == "":
    target = df.columns[-1]
    
  dataInfo = {}
  dataInfo["targetColumn"] = target
  dataInfo["purposeType"] = "regression"
  dataInfo["sourceType"] = "dataframe"
  dataInfo["columnList"] = [{"columnName": col, "columnType": str(df[col].dtype)} for col in df.columns]
  dataInfo["splitInfo"] = splitInfo
  dataInfo["hyperParam"] = hyperParams
  dataInfo["savePath"] = savePath
  dataInfo["graphList"] = graphList
  data = {
            "runType": "custom",
            "dataInfo": dataInfo,
            "splitInfo": splitInfo,
            "selectedHyperParam" : hyperParams,
            "pathInfo": {},
            "selectedHyperParam" : {},
            "graphTf" :  graph,
            "xaiTf" :  xai,
          }
  
  
  data = json.dumps(data)
  runType, params, sendResultUrl = utils.initData(data)
  
  log = Logger("log.log", "info")
  output = runCustomTrain(params=params, df=df, startTime=startTime, sendResultUrl=sendResultUrl, lm=lm, log=log)
  return output


def hpo(df, lm, hyperParamSheme={}, splitInfo=0.7, target="", graph=False, xai=False, trialCount=10, savePath="./") :
  '''
    df : 학습할 dataframe
    lm : 사용자가 정의한 lm 클래스
    target : 학습 타겟
    graph : 그래프 계산 유무
    xai : xai 계산 유무
    splitInfo : 학습, 테스트 비율
    trialCount : 파라미터를 찾는 trial 횟수
    hyperParamSheme : 모델의 하이퍼 정보({"파라미터명": {"min": 0, "max": 100, "type":"float", "q":0.05, "defaultValue": 1.3},})
    graphList: grapTf가 True일 떄 그릴 그래프 종류 (reg: regPlot, distribution Plot, Feature Importance)
    savePath: 모델, 그래프 등등 저장할 경로
  '''
  
  hpoOption = {
        "graphTf": graph,
        "xaiTf": xai,
        "splitInfo" : splitInfo,
        "hyperParamSheme": hyperParamSheme,
        "savePath": savePath
      }
  
  startTime = datetime.datetime.now()
  
  dataInfo = {}
  
  if target == "":
    target = df.columns[-1]
    
  dataInfo["targetColumn"] = target
  dataInfo["purposeType"] = "regression"
  dataInfo["sourceType"] = "dataframe"
  dataInfo["columnList"] = [{"columnName": col, "columnType": str(df[col].dtype)} for col in df.columns]
  data = {
          "runType": "custom",
          "dataInfo": dataInfo,
          "splitInfo": hpoOption["splitInfo"],
          "trialCount": trialCount,
          "hyperParamSheme": hyperParamSheme,
          "selectedHyperParam" : {},
          "pathInfo": {},
          }
  
  data = json.dumps(data)
  
  runType, params, sendResultUrl = utils.initData(data)
  log = Logger("hpo.log", "info")
  
  output = runCustomHPO(params=params, df=df, startTime=startTime, hpoOption=hpoOption, sendResultUrl=sendResultUrl, lm=lm, log=log)
  return output
      
  