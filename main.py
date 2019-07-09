# External imports
import slack

# Builtin imports
import os
import json
import random

CONF_FILE_NAME = "conf.json"

assert os.path.isfile(CONF_FILE_NAME)

CONF_DATA = json.load(open(CONF_FILE_NAME, encoding="utf-8"))

slack_token = CONF_DATA["slack_token"]


@slack.RTMClient.run_on(event='message')
def reject_hopes(**payload):
    data = payload['data']
    web_client = payload['web_client']
    if any([c in data["text"].lower() for c in ["cultural activities", "cultural allowance", "cultural activity"]]):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']
        responses = ["Nope!", "The answer is a definitive no!", "In your dreams", "hahahahahahahah no.", "Really?",
                     "No.", "Thanks for reaching out! Not a chance!",
                     "How could you even *think* about bothering me about this? I'm unfathomably busy"]
        web_client.chat_postMessage(
            channel=channel_id,
            text=random.choice(responses)
        )

print("Connecting...")
rtm_client = slack.RTMClient(token=slack_token)
print("Instantiated client")
rtm_client.start()
print("Connected.")