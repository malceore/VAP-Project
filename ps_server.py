#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from pocketsphinx.pocketsphinx import *
import pyaudio, os

CHUNK = 2048


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
    #audio = r.listen(source)
    #input = r.recognize_sphinx(audio)
    input=decode_sphinx
    print(">>> Word heard:" + input)
    if distance(input, "lights") < 1:
        lights()
    elif distance(input, "internet") < 2:
        internet()
    elif distance(input, "media") < 1:
        media()

def decode_sphinx():
    config = Decoder.default_config()
    #config.set_string('-kws', "commands.txt")
    #config.set_float('-kws_threshold', 1e-30)
    config.set_string('-hmm', 'pocketsphinx/model/en-us/en-us')
    config.set_string('-lm', 'pocketsphinx/model/en-us/en-us.lm.bin')
    config.set_string('-dict', 'pocketsphinx/model/en-us/cmudict-en-us.dict')
    config.set_string('-logfn', '/dev/null')
    decoder = Decoder(config)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, output=True, frames_per_buffer=1024)
    stream.start_stream()

    decoder.start_utt()
    print("Starting to listener..")

    while True:
        buf = stream.read(CHUNK, exception_on_overflow=False)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
        if decoder.hyp() is not None:
            for seg in decoder.seg():
                print("", seg.word, seg.prob, seg.start_frame, seg.end_frame)
                #return seg.word
            decoder.end_utt()
            decoder.start_utt()


test = decode_sphinx()
