# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 08:37:58 2017

@author: jjadhad
"""

import pyaudio
#import wave
from os import environ, path
import sys
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
from flask import Flask
#import flask
#from flask import request,Request
#---------------------------------------------------------------------------------#

app = Flask(__name__)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
#RECORD_SECONDS = 5

  

#MODELDIR = "/home/jjadhad/workspace/speech_to_text/cmusphinx-en-in-5.2"
MODELDIR = "/home/jjadhad/workspace/speech_to_text/ac_mo"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us'))
config.set_string('-lm', path.join(MODELDIR, '3456.lm'))
config.set_string('-dict', path.join(MODELDIR, '3456.dic'))
#config.set_string('-logfn', '/dev/null')
decoder = Decoder(config)



p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)  


decoder.start_utt()
in_speech_bf = True

while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        try:
            if decoder.hyp().hypstr != '':
                print('Partial decoding result:', decoder.hyp().hypstr)
        except AttributeError:
            pass
        if decoder.get_in_speech():
            sys.stdout.write('.')
            sys.stdout.flush()
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                try:
                    if decoder.hyp().hypstr != '':
                        print('Stream decoding result:', decoder.hyp().hypstr)
                except AttributeError:
                    pass
                decoder.start_utt()
    else:
        break
decoder.end_utt()
print('An Error occured:', decoder.hyp().hypstr)
