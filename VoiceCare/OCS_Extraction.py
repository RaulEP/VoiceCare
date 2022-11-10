#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import uuid
import time
import re
import json

api_url = 'https://e5ccf0131d8f485da4ca458c61b66e38.apigw.ntruss.com/custom/v1/12711/2c50ba4817e810ce4fe4ac713d843b6c87e262ceeb057a523f8e528e0845f9e9/infer'
secret_key = 'RGlLUkN1RHlFT1lpRGtXcXRtaFZhckVxdGpKaUpHc0I='

from tkinter import filedialog as fd
image_file = fd.askopenfilename()

#image_file = 'sample.jpg'

regex_01 = re.compile("[1-9](정|캡슐)씩[1-9]회[1-9]일")
regex_02 = re.compile("[1-9]")


def get_pills_regex(pills):

    results = regex_01.search(pills).group(0)
    nums = regex_02.finditer(results)
    nums = [x.group() for x in nums]
    return nums[0],nums[1],nums[2]

request_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo'
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = {'message': json.dumps(request_json).encode('UTF-8')}
files = [
  ('file', open(image_file,'rb'))
]
headers = {
  'X-OCR-SECRET': secret_key
}

response = requests.request("POST", api_url, headers=headers, data = payload, files = files)
extracted_text = response.content.decode('utf8')
parsed_text = json.loads(extracted_text)

fields = parsed_text['images'][0]["fields"]
med1 = fields[0]['inferText'].split("\n")[0]
med2 = fields[1]['inferText'].split("\n")[0]
med1_det = fields[2]['inferText'].split("\n")[0]
med3 = fields[3]['inferText'].split("\n")[0]
med2_det = fields[4]['inferText'].split("\n")[0]
med3_det = fields[5]['inferText'].split("\n")[0]
med4 = fields[6]['inferText'].split("\n")[0]
med4_det = fields[7]['inferText'].split("\n")[0]
med5 = fields[8]['inferText'].split("\n")[0]
med5_det = fields[9]['inferText'].split("\n")[0]

list_med = [med1, med2, med3, med4, med5]
list_med_det = [med1_det, med2_det, med3_det, med4_det, med5_det]

userID = 0

medic_dict = {
    "drug_name": "",  # medicine name
    "dosage": "",  # how many pills do you take each time
    "frequency_per_day": "",  # how many times per day
    "treatment_period": ""  # for how many days to you take the medicine
}

pres_dict = {

    "UserID": userID,  # user ID
    "prescriptions": []  # The list of medicine (list of dictionaries of type medic_dict)

}
drug_id = 1
for x in range(len(list_med_det)):
    medic_dict["drug_id"] = drug_id
    medic_dict["drug_name"] = list_med[x]
    a, b, c = get_pills_regex(list_med_det[x])
    medic_dict["dosage"] = a
    medic_dict["frequency_per_day"] = b
    medic_dict["treatment_period"] = c
    
    #print("llegue aqui")
    response = requests.put("http://127.0.0.1:5000/addPrescription/1/5/{}".format(drug_id), medic_dict)
    print(response.json())
    drug_id += 1
    #pres_dict["prescriptions"].append(medic_dict)

print("Request answer: ")
