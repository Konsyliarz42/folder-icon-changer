import json


LANG = "EN"

with open("language.json", "r") as jsonfile:
    languages: dict = json.loads(jsonfile.read())

text = lambda txt: languages[LANG].get(txt.upper(), languages["EN"][txt.upper()])
