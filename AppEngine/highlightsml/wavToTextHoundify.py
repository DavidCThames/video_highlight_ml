from pydub import AudioSegment
from pydub.utils import make_chunks
import os, glob
import json
import urllib2
from multiprocessing.dummy import Pool as ThreadPool


class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):  
        result = urllib2.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)              
        result.status = code
        return result                                       

    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)              
        result.status = code                                
        return result                                       


# takes the video file name which should be in the same file as this program
# takes the segment size in seconds
# returns a dictionary of numbers to strings
# also adds this dictionary to the list of ones in the database
# keys of the dictionary will start at 0 and should increment by
def getTextFromWav(audio_file_name, split_size, shouldAddToDB):
    
    # opener = urllib2.build_opener(SmartRedirectHandler()) 
    # file_temp = opener.open(audio_file_name)

    # response = urllib2.urlopen(audio_file_name)
    # audio_file_name = response.geturl() # 'http://stackoverflow.com/'
    

    # testfile = urllib2.URLopener()
    # testfile.retrieve(audio_file_name, audio_file_name.rpartition("/")[2])
    # print audio_file_name.rpartition("/")[2]

    myaudio = AudioSegment.from_file("temp" + ".wav", "wav")
    chunk_length_ms = 1000*split_size     # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms)  # Make chunks of one sec

    transcript = ""

    for i, chunk in enumerate(chunks):
        chunk_name = "temp_wave_file" + str(i) + ".wav"
        chunk.export(chunk_name, format="wav")


    my_array = []
    for i, chunk in enumerate(chunks):
        chunk_name = "temp_wave_file" + str(i) + ".wav"
        my_array.append("python highlightsml/File_Wave_Sample.py " + chunk_name + " > tempTextOutput" + str(i) + ".txt")

    pool = ThreadPool(20)
    pool.map(os.system, my_array)

    result = {}
    for i, chunk in enumerate(chunks):
        result[i*split_size] = open('tempTextOutput' + str(i) + '.txt', 'r').read()

    for filename in glob.glob("./temp*"):
        os.remove(filename)

    if shouldAddToDB:
        my_dict = {}
        try:
            with open('dataBase.json') as inFile:
                try:
                    my_dict = json.load(inFile)
                except ValueError:
                    my_dict = {}
        except IOError:
            my_dict = {}

        my_dict[audio_file_name] = result

        with open("dataBase.json", "w") as jsonFile:
            json.dump(my_dict, jsonFile)


    return result
