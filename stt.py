import pyaudio
import wave
from os import environ, path
import sys
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
from flask import Flask
#import flask
from flask import request,Request
#import time

#from werkzeug.utils import secure_filename
#import os,io

app = Flask(__name__)


def VoiceRecorder():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    #RECORD_SECONDS = 5

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)    
    buf = stream.read(1024)
    return buf

def StreamParser(ByteArray):
    MODELDIR = "/home/jjadhad/sphinx_examples/ac_mo"
    #DATADIR = "/usr/share/pocketsphinx/test/data"

    # Create a decoder with certain model
    config = Decoder.default_config()
    config.set_string('-hmm', path.join(MODELDIR, 'en-us'))
    config.set_string('-lm', path.join(MODELDIR, 'en-us.lm'))
    config.set_string('-dict', path.join(MODELDIR, 'cmudict-en-us.dict'))
    decoder = Decoder(config)

    decoder.start_utt()
    in_speech_bf = True
    a=20
    while True:
        #buf = stream.read(1024)
        if ByteArray:
            decoder.process_raw(ByteArray, False, False)
            try:
                if decoder.hyp().hypstr != '':
		    print "********** Partial Result ***********"
                    print('Partial decoding result:', decoder.hyp().hypstr)
                    #return decoder.hyp().hypstr
            except AttributeError:
                pass
            #decoder.hyp().hypstr = ''
            '''
            if decoder.get_in_speech():
                sys.stdout.write('.')
                sys.stdout.flush()
            '''    
            if decoder.get_in_speech() != in_speech_bf:
                in_speech_bf = decoder.get_in_speech()
                if not in_speech_bf:
                    decoder.end_utt()
                    try:
                        if decoder.hyp().hypstr != '':
                            print "         ____________ Final Result ___________"
                            print('Stream decoding result:', decoder.hyp().hypstr)
                            #return decoder.hyp().hypstr
                    except AttributeError:
                        pass
                    decoder.start_utt()
        else:
            break
    decoder.end_utt()
    print('An Error occured:', decoder.hyp().hypstr)

#func()
#UPLOAD_FOLDER = '/home/jjadhad/'
#ALLOWED_EXTENSIONS = set(['txt', 'wav'])
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#request.environ['CONTENT_TYPE'] = 'audio/wav'



@app.route("/stream/<int:flag>",methods=['POST'])
def stream_read_handler(flag):
    #print "****************************************************************************************************************"	
    print  "Flag: ", flag
    print "flag type:", type(flag) 
    #print "data:",request.get_data()	
    #print "data: " , request.args.get('myfile')
    #print "data:",request.body['data']
    #print "data:",request.form['data']
    #print "data:",request.args['data']
    #print "data:",request.stream.read()
    temp_data_2 = request.stream.read()
    print "type of bytearray: ", type(temp_data_2)
    print "temp_data_2 len", len(temp_data_2)
    fd = wave.open("sample_3.wav","w")
    fd.setparams((1, 2, 16000, 70997, 'NONE', 'not compressed'))
    fd.writeframesraw(temp_data_2)
    #fd.close()
    fd.close()
     
    command = 0	
    if (flag == 0):
	print "----------------------------------------  byte array recved  ---------------------------------------------------"
        return "show me the energy consumption"	 
    else:
	print "******************************************* mic enabled  *******************************************************"
	command = StreamParser(temp_data_2[44:])
    if command == 0:
	return 0	
    return command		    	
		  
    #cmd = process_raw_handler()

#@app.route("/process_raw")
def process_raw_handler():
    return "processed raw buf output is here"


if __name__ == "__main__":
        #app.debug = True
        app.run()
        #app.run(debug = True)
