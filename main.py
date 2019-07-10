# External imports
import slack
import spacy
import requests

# Builtin imports
import os
import json
import random
import sys

print("Loading spacy...")
nlp = spacy.load('en_core_web_lg')
print("Spacy loaded...")

TERM_UPDATE_URL = "https://willbeddow.com/app/hoc-slackbot"

CONF_FILE_NAME = "conf.json"

if not os.path.isfile(CONF_FILE_NAME):
    print("Configuration file not found, please run setup.sh")
    sys.exit()

CONF_DATA = json.load(open(CONF_FILE_NAME, encoding="utf-8"))

slack_token = CONF_DATA["slack_token"]


@slack.RTMClient.run_on(event='message')
def reject_hopes(**payload):
    data = payload['data']
    web_client = payload['web_client']
    student_message = data["text"]
    parsed_message = nlp(student_message)
    print(parsed_message)
    entity_choices = []
    sub_choices = []
    excluded_tokens = ["cultural", "allowance", "activity", "activities"]
    for token in parsed_message:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
             token.shape_, token.is_alpha, token.is_stop)
        if token.text.lower() not in excluded_tokens:
            if token.dep_ == "dobj":
                if token.text not in entity_choices:
                    entity_choices.append(token.text)
            if token.pos_ == "NOUN":
                if token.text not in sub_choices:
                    sub_choices.append(token.text)
    if entity_choices:
        if len(entity_choices) == 1 :
            buy_choice = entity_choices[0]
        else:
            buy_choice = f'one of {",".join(entity_choices)}'
    else:
        if sub_choices:
            buy_choice = sub_choices[0]
        else:
            buy_choice = None
    if buy_choice:
        text = f"I think you want to buy {buy_choice}"
    else:
        text = "I'm not sure what you want to buy"
    for ent in parsed_message.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
    if any([c in data["text"].lower() for c in ["cultural activities", "cultural allowance", "cultural activity"]]):
        channel_id = data['channel']
        responses = requests.get(TERM_UPDATE_URL).json()["updates"]["terms"]
        web_client.chat_postMessage(
            channel=channel_id,
            text=text
        )

print("Connecting...")
rtm_client = slack.RTMClient(token=slack_token)
print("Instantiated client")
rtm_client.start()
print("Connected.")