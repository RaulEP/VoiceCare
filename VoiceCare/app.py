import speech_recognition as sr
import wikipedia
from flask import Flask, render_template, request
import requests
from requests.models import Response

try:
    from bot.chatbot import *
except ImportError as error:
    print(error)

app = Flask(__name__)
app.secret_key = "hello_world2021"

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/chat", methods=["GET","POST"])
def get_response():
    text = request.args.get('msg')
    tag, response = chat(text)
    response = conditions(tag, response)
    return str(response)

@app.route("/voice", methods=["GET","POST"])
def get_voice():
    response = "There is no recording"
    if request.method == "POST":
        if "file" not in request.files:
            print("No file")
        stream = request.files['file']
        if stream:
            input = take_command(stream)
            print(input)
            tag, response = chat(input)
            response = conditions(tag, response)
            print(response)
    return render_template('chat.html', response = response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True, threaded=True)

def take_command(file):
    recognizer = sr.Recognizer()
    audioFile = sr.AudioFile(file)
    with audioFile as source:
        sound = recognizer.record(source)
        try:
            text = recognizer.recognize_google(sound, language="en-US") 
        except:
            text = "We couldn't get the transcript"
    return text

def conditions(response_tag, response):

    if response_tag == "medicine_take":
        ## call back-end to receive medicine taken and dosage etc..
        pass

    elif response_tag == "medicine_effect":
        ## call backend to receive medicine side effects
        data = requests.get("http://127.0.0.1:5000/drugSideEffects/타이레놀")
        response = data.json()

    elif response_tag == "prescription":
        data = requests.get("http://127.0.0.1:5000" + "/prescriptionInfo/1/1")
        response = data.json()['1']
    return response
