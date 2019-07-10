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
    rtm_client_local = payload['rtm_client']
    if "text" not in data.keys():
        print(data)
    student_message = data["text"]
    ts = data["ts"]
    if any([c in data["text"].lower() for c in ["cultural activities", "cultural allowance", "cultural activity"]]):
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
                        token_lefts = list(token.lefts)
                        if token_lefts:
                            entity_choices.append(" ".join([l.text for l in token_lefts] + [token.text]))
                        else:
                            entity_choices.append(token.text)
                if token.pos_ == "NOUN":
                    if token.text not in sub_choices:
                        sub_choices.append(token.text)
        if entity_choices:
            if len(entity_choices) == 1:
                buy_choice = entity_choices[0]
            else:
                buy_choice = f'one of {",".join(entity_choices)}'
        else:
            if sub_choices:
                buy_choice = sub_choices[0]
            else:
                buy_choice = None
        channel_id = data['channel']
        if buy_choice:
            button_block = {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"It looks like you want to buy `{buy_choice}` with your cultural allowance"
                        f", is that correct?"
                    },
                    "accessory": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select an item",
                            "emoji": True
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Yes",
                                    "emoji": True
                                },
                                "value": "yes"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "No",
                                    "emoji": True
                                },
                                "value": "no"
                            },
                        ]
                    }
                }
            web_client.chat_postMessage(
                channel=channel_id,
                thread_ts=ts,
                blocks=json.dumps([button_block])
            )
        else:
            text = "What do you want to buy with your cultural allowance?"
            web_client.chat_postMessage(
                channel=channel_id,
                thread_ts=ts,
                text=text
            )


        responses = requests.get(TERM_UPDATE_URL).json()["updates"]["terms"]


print("Connecting...")
rtm_client = slack.RTMClient(token=slack_token)
print("Instantiated client")
rtm_client.start()
print("Connected.")