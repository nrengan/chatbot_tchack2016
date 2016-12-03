from tokenize import String
import json
import requests

search_url = "https://api.crystalknows.com/v1/people.json?search[first_name]={}&search[last_name]={}&search" \
             "[deep_search]=true&deep_search=true&form_submitted=false"
add_person_url = "https://api.crystalknows.com/v1/people/{}add_contact.json"

headers = {"Host": "api.crystalknows.com",
           "Connection": "keep-alive",
           "X-App-Version": "0.10.0",
           "X-SDK-Consumer": "crystal-chrome-extension",
           "X-User-Email": "leo.josts@gmail.com",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
           "X-SDK-Consumer-Version": "3.6.19",
           "Accept": "application/json, text/plain, */*",
           "X-User-Token": "arEqzrLTsXqTdGs7ecnM",
           "X-App-Client": "js_sdk",
           "DNT": "1",
           "Referer": "https://www.linkedin.com/",
           "Accept-Encoding": "gzip, deflate, sdch, br",
           "Accept-Language": "en-US,en;q=0.8",
           "Cookie": "__cfduid=dbf8aef498600e6de3f23a528357315801480789797; __insp_wid=1613728583; __insp_nv=true; __insp_targlpu=https%3A%2F%2Fwww.crystalknows.com%2F; __insp_targlpt=Crystal%20%7C%20The%20world's%20largest%20personality%20platform%20%7C%20Free%20personality%20test; __insp_sid=3455621838; __insp_uid=2725622806; __insp_slim=1480789970908"}


def get_person_data(firstname, secondname):
    r = requests.get(search_url.format(firstname, secondname), headers=headers, proxies={"http": "http://127.0.0.1:8888", "https":"http:127.0.0.1:8888"},verify=r"FiddlerRoot.crt")
    return r

def person_query(firstname, secondname):
    r = requests.get(search_url.format(firstname, secondname), headers=headers)
    return json.loads(r.content)


def person_details(basic_result, index):
    if len(basic_result["people"]) > index:
        personDataUri = basic_result["people"][index]["_links"]["self"]
        r = requests.get(personDataUri, headers=headers)
        return json.loads(r.content)
    return None


def personality_type(details):
    return details["person"]["personality"]["disc_type"]["disc"]


print personality_type(person_details(person_query("Joshua", "Richardson"), 0))
