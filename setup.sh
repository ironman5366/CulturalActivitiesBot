#!/usr/bin/env bash
echo "Installing dependencies..."
pip3 install -r requirements.txt;
echo "Downloading language model..";
python3 -m spacy download en_core_web_lg;
echo "Please enter your slack token>";
read token;
echo "{\"slack_token\": \"$token\"}" > "conf.json";
echo "Finished";