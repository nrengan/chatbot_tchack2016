#
# Copyright 2014 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
## -*- coding: utf-8 -*-

import os
import requests
import json

def getProfile(text):
    """Returns the profile by doing a POST to /v2/profile with text"""        
    url = "https://gateway.watsonplatform.net/personality-insights/api"
    username = "aa8cd577-e982-4c1a-94fb-b7a83714a95b"
    password = "24GfATDypTuV"

    if url is None:
        raise Exception("No Personality Insights service is bound to this app")
    response = requests.post(url + "/v2/profile",
                      auth=(username, password),
                      headers = {"content-type": "text/plain"},
                      data=text
                      )
    try:
    	return json.loads(response.text)
    except:
        raise Exception("Error processing the request, HTTP: %d" % response.status_code)

