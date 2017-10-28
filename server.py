#!/usr/bin/env python
from os import environ, path, system 
import serial
from Levenshtein import distance
import math
import wave
import pyaudio
import audioop
import time
from collections import deque
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

# Globals
MODELDIR = "pocketsphinx/model"
DATADIR = "pocketsphinx/test/data"
CHUNK = 1024  # CHUNKS of bytes to read each time from mic, changed from 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 3200  # The threshold intensity that defines silence
                  # and noise signal (an int. lower than THRESHOLD is silence).
SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                   # only silence is recorded. When this time passes the
                   # recording finishes and the file is delivered.
PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                  # is detected, how much of previously recorded audio is
                  # prepended. This helps to prevent chopping the beggining
                  # of the phrase.
# How long should transcribe for before acting on what was said, now set to one minute.
TIMEOUT = 5


def audio_int(num_samples=50):
    """ Gets average audio intensity of your mic sound. You can use it to get
        average intensities while you're talking and/or silent. The average
        is the avg of the 20% largest intensities recorded.
    """

    print "Getting intensity values from mic."
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4))) 
              for x in range(num_samples)] 
    values = sorted(values, reverse=True)
    r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
    print " Finished "
    print " Average audio intensity is ", r
    stream.close()
    p.terminate()
    if r < 3000:
        THRESHOLD = 3500
    else:
        THRESHOLD = r + 100
    #return r



print("***********************")
print("* Simple Voice Lights *")
print("*   Brandon T. Wood   *")
print("***********************")

# Configure audio first.
audio_int()
#print THRESHOLD

#Get serial lights for light based arduino.
#ser = serial.Serial('/dev/ttyACM0', 9600)
# Set lights to off by default.
#time.sleep(1)
LIGHTS_ON=False

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
config.set_string('-logfn', '/dev/null') # Hide noisey logs.
#config.set_string('-keyphrase', 'hello')
#config.set_float('-kws_threshold', 1e+20)
#config.set_string('-kws', 'commands.txt')
#config.set_string('-keyphrase', 'hello')
#config.set_float('-kws_threshold', 1e+20)
#decoder.set_kws('keyword', 'commands.list')
#decoder.set_lm_file('lm', 'query.lm')
#decoder.set_search('keyword')

# Decode streaming data.
decoder = Decoder(config)
decoder.set_kws('keyword', 'commands.txt')
#decoder.set_lm_file('lm', 'query.lm')
decoder.set_search('keyword')
decoder.start_utt()

# Start listening..
print "* Listening for sound.. "
audio2send = []
cur_data = ''  # current chunk  of audio data
rel = RATE/CHUNK
slid_win = deque(maxlen=SILENCE_LIMIT * rel)

# Prepend audio from 0.5 seconds before noise was detected
num_phrases=-1
prev_audio = deque(maxlen=PREV_AUDIO * rel) 
started = False
n = num_phrases
response = []

# Main loop
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=1024)
stream.start_stream() 
in_speech_bf = False
print (">>> Listening!")
while (num_phrases == -1 or n > 0):
    cur_data = stream.read(CHUNK)
    slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
    #print slid_win[-1]
    if(sum([x > THRESHOLD for x in slid_win]) > 0):
        if(not started):
            #Little bleep, requires bleep be installed.
            print ">>> Starting Transcription"
            system("beep -f 855 -l 110")
            system("beep -f 645 -l 110")
            time.sleep(0.5)
            started = True
            timeout = time.time() + TIMEOUT
            while True:
                buf=stream.read(CHUNK)
                decoder.process_raw(buf, False, False)
                if decoder.get_in_speech() != in_speech_bf:
                    in_speech_bf = decoder.get_in_speech()
                    if not in_speech_bf:
                        decoder.end_utt()
                        #print 'Result:', 
                        # Place holder light controls.
                        if LIGHTS_ON:
                            print "Lights off"
                            #ser.write("one:off")
                            #ser.write("two:off")
                            #ser.write("three:off")
                            #ser.write("four:off")
                            LIGHTS_OFF=False
                        else:
                            print "Lights on"
                            #ser.write("one:on")
                            #ser.write("two:on")
                            #ser.write("three:on")
                            #ser.write("four:on")
                            LIGHTS_ON=True

                        print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
                        result=decoder.hyp().hypstr
                        #dist=distance("hello",result)
                        print " >>> Result: ", result, " | Dist: ", dist                    
                        decoder.start_utt()
                if time.time() > timeout:
                    break
            system("beep -f 555 -l 110")
            system("beep -f 745 -l 110")
            #decoder.end_utt()
            time.sleep(5)

    elif (started is True):
        print ">>>Finished, reseting.."
        started = False
        slid_win = deque(maxlen=SILENCE_LIMIT * rel)
        prev_audio = deque(maxlen=0.5 * rel)
        n -= 1
        print ">>>Listening ..."

print "* Done recording"
#decoder.end_utt()
stream.close()
p.terminate()





