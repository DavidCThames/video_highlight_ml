from pydub import AudioSegment
from pydub.utils import make_chunks
import os, glob
import json

from multiprocessing.dummy import Pool as ThreadPool





# takes the video file name which should be in the same file as this program
# takes the segment size in seconds
# returns a dictionary of numbers to strings
# also adds this dictionary to the list of ones in the database
# keys of the dictionary will start at 0 and should increment by
def getTextFromWav(audio_file_name, split_size, shouldAddToDB):
    myaudio = AudioSegment.from_file(audio_file_name, "wav")
    chunk_length_ms = 1000*split_size  # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms)  # Make chunks of one sec

    transcript = ""

    for i, chunk in enumerate(chunks):
        chunk_name = "temp_wave_file" + str(i) + ".wav"
        chunk.export(chunk_name, format="wav")


    my_array = []
    for i, chunk in enumerate(chunks):
        chunk_name = "temp_wave_file" + str(i) + ".wav"
        my_array.append("python File_Wave_Sample.py " + chunk_name + " > tempTextOutput" + str(i) + ".txt")

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
