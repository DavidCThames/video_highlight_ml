import sys
from google.cloud import language
import json
import time as timer

client = language.LanguageServiceClient()

x = []
y = []
t = []

def run_game(data, quality):
    global x
    global y
    global t
    i = 0
    for timecode, sentance in data.items():
        t.append(timecode)
        if(sentance == ""):
            x.append([0, 0, 0])
            y.append(0)
        else:
            document = language.types.Document(
                content= sentance,
                language='en',
                type='PLAIN_TEXT',
            )

            response = client.analyze_sentiment(
                document=document,
                encoding_type='UTF32',
            )

            sentiment = response.document_sentiment

            sentance_length = len(sentance.rsplit(" "))

            x.append([sentiment.score, sentiment.magnitude, sentance_length])
            y.append(quality)
            # print json.dumps([sentiment.score, sentiment.magnitude])
            timer.sleep(0.11)
        # if i % (len(data) / 10) == 0:
            # print "-", 
        i = i + 1
    

def get_from_database():
    data = json.load(open("../data/dataBase.json", "r")); #'{"Game1": {"0": "this is a test", "8": "this is a better test", "12": "this is the best test"}, "Game2": {}}')

    # NOTE: Need to be global
    global x
    global y

    x = []
    y = []

    for game in ["Game1_Full.wav", "Game2_Full.wav"]: 
        run_game(data[game], 0)
    for game in ["Game1_Highlights.wav", "Game2_Highlights.wav"]: 
        run_game(data[game], 1)

    with open("dataBase_results_x.json", "w") as jsonFile:
        json.dump(x, jsonFile)
    with open("dataBase_results_y.json", "w") as jsonFile:
        json.dump(y, jsonFile)

def get_from_data(data):
    global x
    run_game(data, 0)
    return [x, t]