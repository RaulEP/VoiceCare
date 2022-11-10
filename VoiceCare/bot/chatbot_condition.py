



user_input = "hi"  # INPUT FROM THE USER

# call chat() and use the returns

### ---------------- TTS CODE
#sound = "test.mp3"

#from gtts import gTTS
#from playsound import playsound
#import os

#tts = gTTS(text=response, lang='en')
#tts.save(sound)
#playsound(sound)

#os.remove(sound)

### ----------------------------------------------


if response_tag == "greeting":
    print(response)

elif response_tag == "goodbye" or user_input == "quit":
    print(response)
    ## TODO STOP and leave the chatbot !!!

elif response_tag == "thanks":
    print(response)

elif response_tag == "medicine_take":
    ## call back-end to receive medicine taken and dosage etc..
    pass

elif response_tag == "medicine_effect":
    ## call backend to receive medicine side effects
    pass

elif response_tag == "prescription":
    ## call backend to receive prescription
    pass

elif response_tag == "pharmacy":
    print(response)

elif response_tag == "nounderstand":
    print(response)

else:
    print("Error !! Unrecognized tag returned")