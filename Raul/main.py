# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, make_response
import flask
from flask_restful import Api, Resource, reqparse, abort
import json
import requests
import urllib.parse
import sys
import codecs
from deep_translator import GoogleTranslator


app = Flask(__name__)
api = Api(app)

drugs = {"타이레놀": {"side_effects": "쇽 증상(호흡곤란, 온몸이 붉어짐, 혈관부기, 두드러기 등), 천식발작, 혈소판감소, 과립구감소, 용혈성빈혈, 메트헤모글로빈혈증, 혈소판기능 저하(출혈시간 연장), 청색증, 구역, 구토, 식욕부진, 위장출혈, 소화성궤양, 천공(뚫림) 과민증상(얼굴부기, 땀이 남, 저혈압), 발진, 피부점막안증후군(스티븐스-존슨증후군), 독성표피괴사용해(리엘증후군), AST 상승, ALT 상승, 고정발진 등이 나타나는 경우 즉각 복용을 중지하고 의사 또는 약사와 상의하십시오."}}

usersdb = {1: { 
                "name": "Raul",
                 "sex": "male", 
                 "age":25, 
                 "phone_number":"01057397622",
                 "setting": {
                     "language": "eng"
                 },
                 "prescriptions": {
                    1: [        
                                {
                                "drug_id": 1,
                                "drug_name": "타이레놀",
                                "dosage": "1 pill",
                                "frequency_per_day": "2 times per day",
                                "treatment_period": "4 days"},
                                
                                {
                                "drug_id": 2,
                                "drug_name": "Omeprazole",
                                "dosage": "1 pill",
                                "frequency_per_day": "1 time per day",
                                "treatment_period": "3 days"}]
                                }
                }
            }
#with open('usersdb.json', 'w',encoding="utf-8") as outfile:
   # json.dump(usersdb, outfile, ensure_ascii=False)

#Parser
DrugDetail_put_args = reqparse.RequestParser()
DrugDetail_put_args.add_argument("drug_id", type=int, help="Drug Name", required=True)
DrugDetail_put_args.add_argument("drug_name", type=str, help="Drug Name", required=True)
DrugDetail_put_args.add_argument("dosage", type=str, help="How many pills should you take", required=True)
DrugDetail_put_args.add_argument("frequency_per_day", type=str, help="How many times a day should you take the medicine", required=True)
DrugDetail_put_args.add_argument("treatment_period", type=str, help="How many days does this medication should be taken", required=True)

#Local DB
class PrescriptionInfo(Resource):
    #Access Prescription Info
    def get(self, user_id, prescription_id):

        drug_key = 1
        messages = {}
        for dict in usersdb[user_id]["prescriptions"][prescription_id]:
            name = dict["drug_name"]
            dosage = dict["dosage"]
            frequency = dict["frequency_per_day"]
            period = dict["treatment_period"]
            messages[drug_key] = "You should take {} of {}, {} for a period of {}".format(dosage, name, frequency, period)
            drug_key += 1
        return messages
class AddPrescription(Resource):
    def put(self, user_id, prescription_id):
        args = DrugDetail_put_args.parse_args()
        # How many drugs items are there in the database
        drug_id = len(usersdb[user_id]["prescriptions"][prescription_id]) + 1

        # Create new Drug ID item into Prescription List
        usersdb[1]["prescriptions"][1].append({"drug_id": drug_id})

        # Remove nested dict.
        usersdb[user_id]["prescriptions"][prescription_id][2].update({"drug_id": drug_id})

        # Adding args into DB.

        usersdb[user_id]["prescriptions"][prescription_id][2].update(args)
        return usersdb[user_id]["prescriptions"][prescription_id]
"""
class AddDrugToPrescription(Resource):
    
    def put(self, user_id, prescription_id):
        args = DrugDetail_put_args.parse_args()
        #How many drugs items are there in the database
        drug_id = len(usersdb[user_id]["prescriptions"][prescription_id]) + 1

        #Create new Drug ID item into Prescription List
        usersdb[1]["prescriptions"][1].append({"drug_id": drug_id})

        #Remove nested dict.
        usersdb[user_id]["prescriptions"][prescription_id][2].update({"drug_id":drug_id})
        
        #Adding args into DB.
        usersdb[user_id]["prescriptions"][prescription_id][2].update(args)
        print()
        return usersdb[user_id]["prescriptions"][prescription_id]
"""     

#OpenAPI  
class AddDrugToPrescription(Resource):
    
    def put(self, user_id, prescription_id):
        args = DrugDetail_put_args.parse_args()
        #How many drugs items are there in the database
        drug_id = len(usersdb[user_id]["prescriptions"][prescription_id]) + 1

        #Create new Drug ID item into Prescription List
        usersdb[1]["prescriptions"][1].append({"drug_id": drug_id})

        #Remove nested dict.
        usersdb[user_id]["prescriptions"][prescription_id][2].update({"drug_id":drug_id})
        
        #Adding args into DB.
        usersdb[user_id]["prescriptions"][prescription_id][2].update(args)
        print()
        return usersdb[user_id]["prescriptions"][prescription_id]
    
class DrugSideEffects(Resource):
    def get(self, drug_name):
        url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
        service_key ="7xbDbSQ3I2s4q0KHPgv0QRpHHE0FzSK6bflU2VxDLO1R2dD%2B5uaYwPNm9EQKqnlySYgKcJ8aX6m4H0t2jMF1iA%3D%3D"
        num_of_rows = 3
        response = requests.get(url, 'serviceKey={}&pageNo={}&numOfRows={}&itemName={}&type=json'.format(service_key, 1,num_of_rows,drug_name))
        side_effects = response.content.decode("utf-8")
        side_effects = json.loads(side_effects)
        side_effects = str(side_effects['body']['items'][0]['seQesitm'])
        print(side_effects)
        return {str(drug_name): side_effects}

class DrugEffects(Resource):
    def get(self, drug_name):
        url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
        service_key ="7xbDbSQ3I2s4q0KHPgv0QRpHHE0FzSK6bflU2VxDLO1R2dD%2B5uaYwPNm9EQKqnlySYgKcJ8aX6m4H0t2jMF1iA%3D%3D"
        num_of_rows = 3
        response = requests.get(url, 'serviceKey={}&pageNo={}&numOfRows={}&itemName={}&type=json'.format(service_key, 1,num_of_rows,drug_name))
        side_effects = response.content.decode("utf-8")
        side_effects = json.loads(side_effects)
        side_effects = str(side_effects['body']['items'][0]['efcyQesitm'])
        print(side_effects)
        return {str(drug_name): side_effects}

class FoodInteraction(Resource):
    def get(self, drug_name):
        url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
        service_key ="7xbDbSQ3I2s4q0KHPgv0QRpHHE0FzSK6bflU2VxDLO1R2dD%2B5uaYwPNm9EQKqnlySYgKcJ8aX6m4H0t2jMF1iA%3D%3D"
        num_of_rows = 3
        response = requests.get(url, 'serviceKey={}&pageNo={}&numOfRows={}&itemName={}&type=json'.format(service_key, 1,num_of_rows,drug_name))
        side_effects = response.content.decode("utf-8")
        side_effects = json.loads(side_effects)
        side_effects = str(side_effects['body']['items'][0]['intrcQesitm'])
        print(side_effects)
        return {str(drug_name): side_effects}

class DrugPrecautions(Resource):
    def get(self, drug_name):
        url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
        service_key ="7xbDbSQ3I2s4q0KHPgv0QRpHHE0FzSK6bflU2VxDLO1R2dD%2B5uaYwPNm9EQKqnlySYgKcJ8aX6m4H0t2jMF1iA%3D%3D"
        num_of_rows = 3
        response = requests.get(url, 'serviceKey={}&pageNo={}&numOfRows={}&itemName={}&type=json'.format(service_key, 1,num_of_rows,drug_name))
        side_effects = response.content.decode("utf-8")
        side_effects = json.loads(side_effects)
        side_effects = str(side_effects['body']['items'][0]['atpnQesitm'])
        print(side_effects)
        return {str(drug_name): side_effects}

class DrugStorage(Resource):
    def get(self, drug_name):
        url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
        service_key ="7xbDbSQ3I2s4q0KHPgv0QRpHHE0FzSK6bflU2VxDLO1R2dD%2B5uaYwPNm9EQKqnlySYgKcJ8aX6m4H0t2jMF1iA%3D%3D"
        num_of_rows = 3
        response = requests.get(url, 'serviceKey={}&pageNo={}&numOfRows={}&itemName={}&type=json'.format(service_key, 1,num_of_rows,drug_name))
        side_effects = response.content.decode("utf-8")
        side_effects = json.loads(side_effects)
        side_effects = str(side_effects['body']['items'][0]['depositMethodQesitm'])
        print(side_effects)
        return {str(drug_name): side_effects}

def TranslateToEnlglish(input):
    translated = GoogleTranslator(source='auto', target='en').translate(input)
    return translated
    
#Questions OPEN API
api.add_resource(DrugSideEffects, "/drugSideEffects/<string:drug_name>")
api.add_resource(DrugEffects, "/drugEffects/<string:drug_name>")
api.add_resource(FoodInteraction, "/foodInteraction/<string:drug_name>")
api.add_resource(DrugPrecautions, "/drugPrecautions/<string:drug_name>")
api.add_resource(DrugStorage, "/drugStorage/<string:drug_name>")

#Local Database
api.add_resource(PrescriptionInfo, "/prescriptionInfo/<int:user_id>/<int:prescription_id>")
api.add_resource(AddPrescription, "/addPrescription/<int:user_id>/<int:prescription_id>/<int:drug_id>")


if __name__ == "__main__":
    app.run(debug=True)
