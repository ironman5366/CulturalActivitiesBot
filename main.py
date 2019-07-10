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
    if any([c in data["text"].lower() for c in ["cultural activities", "cultural allowance", "cultural activity"]]):
        channel_id = data['channel']
        responses = requests.get(TERM_UPDATE_URL).json()["updates"]["terms"]
        web_client.chat_postMessage(
            channel=channel_id,
            text=random.choice(responses)
        )

print("Connecting...")
rtm_client = slack.RTMClient(token=slack_token)
print("Instantiated client")
rtm_client.start()
print("Connected.")