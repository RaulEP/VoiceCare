# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, make_response
import flask
from flask_restful import Api, Resource, reqparse, abort
import json

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
                                "frequency_per_day": "5 Days",
                                "treatment period": "4 days"},
                                
                                {
                                "drug_id": 2,
                                "drug_name": "Omeprazole",
                                "dosage": "1 pill",
                                "frequency_per_day": "1 time a day",
                                "treatment_period": "3 days"}]
                                }
                }
            }


#Parser
DrugDetail_put_args = reqparse.RequestParser()
DrugDetail_put_args.add_argument("drug_name", type=str, help="Drug Name", required=True)
DrugDetail_put_args.add_argument("dosage", type=str, help="How many pills should you take", required=True)
DrugDetail_put_args.add_argument("frequency_per_day", type=str, help="How many times a day should you take the medicine", required=True)
DrugDetail_put_args.add_argument("treatment_period", type=str, help="How many days does this medication should be taken", required=True)



class PrescriptionInfo(Resource):

    #Access Prescription Info
    def get(self, user_id, prescription_id, drug_id=0):
        if user_id in usersdb.keys():
            if drug_id != 0:
                return usersdb[user_id]["prescriptions"][prescription_id]
            else:
                return usersdb[user_id]["prescriptions"][prescription_id]
    
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
        return usersdb[user_id]["prescriptions"][prescription_id]

api.add_resource(PrescriptionInfo, "/prescriptionInfo/<int:user_id>/<int:prescription_id>")

class Drugs(Resource):  

    def get(self, name, side_effects):
        if side_effects == 1:
            return make_response(flask.json.dumps(drugs[name]["side_effects"], ensure_ascii=False))

api.add_resource(Drugs, "/drugs/<string:name>/<int:side_effects>")

if __name__ == "__main__":
    app.run(debug=True)
