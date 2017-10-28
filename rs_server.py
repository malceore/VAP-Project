import pyaudio,os
import speech_recognition as sr
from Levenshtein import distance

def lights():
        os.system("curl 192.168.0.101:8080:/index.html?param=light1toggle")
        os.system("curl 192.168.0.101:8080:/index.html?param=light2toggle")
        os.system("curl 192.168.0.101:8080:/index.html?param=light3toggle")
        os.system("curl 192.168.0.101:8080:/index.html?param=light4toggle")

def internet():
        os.system("firefox &")

def media():
        os.system("vlc &")

def mainfunction(source):
#print distance("ah", "aho")
    audio = r.listen(source)
    input = r.recognize_sphinx(audio)
    print(">>> Word heard:" + input)
    if distance(input, "lights") < 5:
        lights()
    elif distance(input, "internet") < 7:
        internet()
    elif distance(input, "media") < 5:
        media()

if __name__ == "__main__":
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        #while 1:
        mainfunction(source)
