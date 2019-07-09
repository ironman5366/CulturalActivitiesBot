# External imports
import slack

# Builtin imports
import os
import json

CONF_FILE_NAME = "conf.json"

assert os.path.isfile(CONF_FILE_NAME)

CONF_DATA = json.load(open(CONF_FILE_NAME, encoding="utf-8"))

OAUTH_CONF = CONF_DATA["oauth"]

