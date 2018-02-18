# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from wavToTextHoundify import getTextFromWav
import json
import get_numeric
import time
import os

def index(request):
        return render(request, "home.html")

def about(request):
        return render(request, "about.html")

def doc(request):
        return render(request, "documentation.html")

def upload(request):
        #get post data 

        if request.method == 'POST':
                if 'file_upload_temp' in request.FILES:
                        file_upload = request.FILES['file_upload_temp']

                        # os.system("ffmpeg -i audio.wav -ac 1 mono.wav")

                        with open("temp" + ".wav", "w") as local_file: #audio_file_name.rpartition("/")[2]
                                local_file.write(file_upload.read())
                        result = getTextFromWav("temp.wav", 8, False)
                        with open("./highlightsml/one_time_example.json", "w") as jsonFile:
                                json.dump(get_numeric.get_from_data(result), jsonFile)
                        os.system("python ./highlightsml/ML_Model2.py")
                        with open("./highlightsml/one_time_example.json", "r") as jsonFile:
                                result_highlights = json.load(jsonFile)
                        return HttpResponse(json.dumps(result_highlights))
                else:
                        return HttpResponse(json.dumps(request.FILES))
        else:
                return HttpResponse("Error: No POST Request")

def train(request, positive):
    #get post data
    return render(request, "home.html")
