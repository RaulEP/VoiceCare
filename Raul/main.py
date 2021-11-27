# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, make_response
import flask
from flask_restful import Api, Resource
import json

app = Flask(__name__)
api = Api(app)

drugs = {"타이레놀": {"side_effects": "쇽 증상(호흡곤란, 온몸이 붉어짐, 혈관부기, 두드러기 등), 천식발작, 혈소판감소, 과립구감소, 용혈성빈혈, 메트헤모글로빈혈증, 혈소판기능 저하(출혈시간 연장), 청색증, 구역, 구토, 식욕부진, 위장출혈, 소화성궤양, 천공(뚫림) 과민증상(얼굴부기, 땀이 남, 저혈압), 발진, 피부점막안증후군(스티븐스-존슨증후군), 독성표피괴사용해(리엘증후군), AST 상승, ALT 상승, 고정발진 등이 나타나는 경우 즉각 복용을 중지하고 의사 또는 약사와 상의하십시오."}}

class Drugs(Resource):

    def get(self, name, side_effects):
        if side_effects == 1:
            return make_response(flask.json.dumps(drugs[name]["side_effects"], ensure_ascii=False))

api.add_resource(Drugs, "/drugs/<string:name>/<int:side_effects>")

if __name__ == "__main__":
    app.run(debug=True)
