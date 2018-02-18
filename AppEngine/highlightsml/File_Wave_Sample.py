#!/usr/bin/env python2.7
import houndify
import sys
import time
import wave

CLIENT_ID = "q5SIP4-ilmRoGACzE9p62A=="
CLIENT_KEY = "MrWWVDbwdQV_GR9lE46x4VZqCUWYX50vv1mmE2IaVlWuXqZCADx6WGJf-94s24NwAcAD8H63lD4qJyRn9D0m0Q=="
AUDIO_FILE = sys.argv[1]
BUFFER_SIZE = 512


#
# Simplest HoundListener; just print out what we receive.
# You can use these callbacks to interact with your UI.
#
class MyListener(houndify.HoundListener):
    def onPartialTranscript(self, transcript):
        #print "Partial transcript: " + transcript
        pass

    def onFinalResponse(self, response):
        print response["Disambiguation"]["ChoiceData"][0]["Transcription"]

    def onError(self, err):
        print "Error: " + str(err)


client = houndify.StreamingHoundClient(CLIENT_ID, CLIENT_KEY, "test_user")
client.setLocation(37.388309, -121.973968)


audio = wave.open(AUDIO_FILE)
if audio.getsampwidth() != 2:
    print "%s: wrong sample width (must be 16-bit)" % AUDIO_FILE
if audio.getframerate() != 8000 and audio.getframerate() != 16000:
    print audio.getframerate()
    print "%s: unsupported sampling frequency (must be either 8 or 16 khz)" % AUDIO_FILE
if audio.getnchannels() != 1:
    print "%s: must be single channel (mono)" % AUDIO_FILE

client.setSampleRate(audio.getframerate())
client.start(MyListener())

# samples = audio.readframes(BUFFER_SIZE)
while True:
    samples = audio.readframes(BUFFER_SIZE)
    if len(samples) == 0: break
    if client.fill(samples): break
    time.sleep(0.032)  # simulate real-time so we can see the partial transcripts

result = client.finish()  # returns either final response or error
