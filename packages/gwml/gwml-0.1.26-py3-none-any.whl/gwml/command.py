import os
import sys
import json
import yaml
import requests
import getpass
from gwml.cmdLib.getHyperParam import extractHyperParamstoFile
from gwml.cmdLib.envCollector import generate_requirements
from gwml.cmdLib.organizeModel import ModelOrganizer


def yaml_to_json(yaml_file):
    with open(yaml_file, "r", encoding="utf-8") as yf:
        yaml_data = yaml.safe_load(yf)

    return yaml_data


def post_request(url, data, headers=None):
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def send_post_request(url, file_path, data, jwt_token):
    url += "/api/model"
    headers = {"Authorization": f"Bearer {jwt_token}"}

    files = {"file": open(file_path, "rb")}

    json_data = json.dumps(data)
    print(url)
    print(headers)
    print(data)

    response = requests.post(
        url, headers=headers, files=files, data={"json": json_data}
    )

    return response.json()


def handle_pull():
    print("Executing pull command...")


def save_json_to_file(json_data, file_path):
    with open(file_path, "w") as file:
        json.dump(json_data, file, indent=4)


def handle_push(string1, string2):

    # 필수 파일이 있는지 여부 검사
    if fileCheck()["code"] == 400:
        print(fileCheck()["msg"])
        sys.exit()

    # 설정 파일 불러오기
    opt = yaml_to_json("setting.yaml")

    # 설정에 호스트가 있느지, 없다면 사용자 입력 받기
    if "host" not in opt:
        q = input("Host information is missing. Please enter it: ").strip().lower()
        opt["host"] = q

    url = opt["host"] + "/api/user-auth/login"
    id = input("Please enter your Login ID: ").strip().lower()
    pwd = getpass.getpass("Please enter your Login Passowrd: ")
    data = {"userId": id, "password": pwd}
    headers = {"Content-Type": "application/json"}

    # 로그인
    response = post_request(url, data, headers)
    if "userInfo" not in response:
        print(response["message"])
        sys.exit()

    types = ["regression", "classification", "clustering", "timeseries"]

    if "modelName" not in opt:
        environment = (
            input("Please enter the name of your deployment model: ").strip().lower()
        )
        opt["environment"] = environment

    if "purposeType" not in opt:
        purposeType = (
            input(
                "The machine learning objective type has not been defined. Please input one of the following: \n(regression, Classification, clustering, timeseries) :"
            )
            .strip()
            .lower()
        )
        opt["purposeType"] = purposeType

    if opt["purposeType"] not in types:
        print("You did not enter the correct objective type.")
        sys.exit()

    # 설정을 테스트파일을 통해 자동 생성할지, 수동으로 진행할지 여부 설정
    if "hpoOpt" not in opt:
        manualOptQ = "n"
        if "manualOpt" not in opt or opt["manualOpt"] == False:
            manualOptQ = (
                input(
                    "Should we automatically configure the options through test.py? (y/n): "
                )
                .strip()
                .lower()
            )
        if manualOptQ == "y" or opt["manualOpt"]:
            filename = (
                input(
                    "What is the file name of the test code you wrote? For example ('test.py'): "
                )
                .strip()
                .lower()
            )
            hyperparm = ""
            try:
                hyperparm = extractHyperParamstoFile(filename)
                if len(hyperparm) == 0:
                    hyperparm = {}
                else:
                    hyperparm = hyperparm[0]
                opt["hpoOpt"] = hyperparm
            except:
                print("The {} file could not be found.".format(filename))
                sys.exit()

    # ENV 파일을 자동으로 설정할지 여부 검사
    requirementsAutoCollectQ = "n"
    if "requirementsAutoCollect" not in opt or opt["requirementsAutoCollect"] == False:
        requirementsAutoCollectQ = (
            input("Should we automatically collect the requirements.txt file? (y/n): ")
            .strip()
            .lower()
        )
    if requirementsAutoCollectQ == "y" or opt["requirementsAutoCollect"]:
        requirements = generate_requirements("model.py")
        requirements = generate_requirements("predict.py")

    modelInfo = {
        "environment": opt["environment"],
        "mlType": "tabular",
        "purposeType": opt["purposeType"],
        "customTF": True,
        "trainTf": False,
        "baseModelName": "XGBoost-Regression",
        "baseModelVersion": "latest",
    }

    # 모델 tar파일 만들기
    base_directory = "."  # 현재 디렉토리
    output_filename = "model.tar.gz"

    hyperParameter = {"hyperParameter": []}
    hyperscheme = opt["hpoOpt"]
    for key in hyperscheme:
        hyperParam = {}
        if hyperscheme[key]["type"] == "int":
            hyperParam["range"] = {
                "min": hyperscheme[key]["min"],
                "max": hyperscheme[key]["max"],
            }
        elif hyperscheme[key]["type"] == "float":
            hyperParam["range"] = {
                "min": hyperscheme[key]["min"],
                "max": hyperscheme[key]["max"],
            }

        elif hyperscheme[key]["type"] == "str":
            hyperParam["range"] = [
                {"label": str(v), "value": str(v)}
                for v in hyperscheme[key]["value"]
            ]
            
        hyperParam["parameterName"] = key
        hyperParam["defaultValue"] = hyperscheme[key]["defaultValue"]
        hyperParam["type"] = hyperscheme[key]["type"]
        hyperParameter["hyperParameter"].append(hyperParam)
            
    organizer = ModelOrganizer(base_directory)
    organizer.organize_and_compress(
        output_filename, opt["purposeType"] + ".py", modelInfo, hyperParameter # opt["hpoOpt"]
    )

    sendData = {"modelName": opt["environment"], "trainTf": False}
    mhResult = send_post_request(
        response["systemInfo"]["mhUrl"],
        os.path.join("./", output_filename),
        sendData,
        response["jwt"],
    )
    print(mhResult)
    print(
        "You have successfully registered {}/{}".format(
            response["systemInfo"]["mhUrl"], opt["environment"]
        )
    )


def fileCheck():
    # 현재 디렉토리 경로를 가져옵니다.
    current_directory = os.getcwd()

    # 현재 디렉토리 내부의 파일 및 디렉토리 리스트를 가져옵니다.
    files = os.listdir(current_directory)

    if "model.py" not in files:
        return {
            "code": 400,
            "msg": "'model.py' is not present in the current directory.",
        }
    elif "predict.py" not in files:
        return {
            "code": 400,
            "msg": "'predict.py' is not present in the current directory.",
        }
    elif "setting.yaml" not in files:
        return {
            "code": 400,
            "msg": "'setting.yaml' is not present in the current directory.",
        }
    else:
        return {"code": 200}
