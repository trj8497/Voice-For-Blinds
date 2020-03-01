from playsound import playsound
from datetime import datetime
from os import path as p
import time as t
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Vision Project-9d1350f85714.json"

from google.cloud import texttospeech
from google.cloud import vision

client = vision.ImageAnnotatorClient()
counter = 0

def text_to_speech(text):
    global counter
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.types.SynthesisInput(text=text)

    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Standard-C',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = client.synthesize_speech(input_text, voice, audio_config)  # The response's audio_content is binary.

    with open('audio/output'+str(counter)+'.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

def detect_img(path):
    global counter
    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))

    finalstr = ''
    for object_ in objects:
        print('\n{}'.format(object_.name))
        finalstr = finalstr + ' {}'.format(object_.name)
        finalstr = finalstr + '    '

    text_to_speech(finalstr)
    playsound('audio/output'+str(counter)+'.mp3')
    os.unlink('audio/output'+str(counter)+'.mp3')
    counter += 1
    # os.remove('output.mp3')
# img = cv2.VideoCapture(0)

while(True):

    now = datetime.now()
    time = ""
    hour = str(now.strftime("%H"))
    minute = str(now.strftime("%M"))
    second = str(now.strftime("%S"))
    time = time + (hour + "-" + minute + "-" + second)

    path = 'Capture/{}.jpg'.format(time)
    if p.exists(path):
        detect_img(path)
        os.unlink(path)

    t.sleep(1)
    # ret, frame = img.read()
    # path = 'Capture/live.png'
    # cv2.imwrite(path, frame)

    # cv2.imshow('frame', frame)

    # key = cv2.waitKey(1)
    # if key == ord('c'):
    # detect_img(path)
        # break

# img.release()
# cv2.destroyAllWindows()
