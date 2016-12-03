# CTEC 121 Intro to Programming and Problem Solving
# Bruce Elgort / Clark College
# Using IBM Watson's Tone Analyzer to detect and interpret emotional, social, and writing cues found in text.
# February 26, 2016
# Version 1.0
 
import requests
import json
from watson_developer_cloud import ToneAnalyzerV3


 
def analyze_tone(text):

    tone_analyzer = ToneAnalyzerV3(
        username='fb3a4eef-3535-4ea1-9920-5f944f536501',
        password='C4lmPJgiupQB',
        version='2016-05-19 ')
    try:
        return json.dumps(tone_analyzer.tone(text='A word is dead when it is said, some say. Emily Dickinson'), indent=2)
    except:
        return False
