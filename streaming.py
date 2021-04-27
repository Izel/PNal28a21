import requests
import os
import json
import configparser

PROPERTIES_PATH = "config.properties"

#
# Specify the real values in config.properties file
#
API_consumer_key = "THE CONSUMER KEY"
API_consumer_secret = "THE CONSUMER SECRET"
access_token_key = "THE ACCESS TOKEN KEY"
access_token_secret = "THE ACCESS TOKEN SECRET"
bearer_token = "THE BEARER TOKEN"

#
# Initial configuration to obtain the tweets stream access. Get the real values
# from config.properties file.
#
def config_app():
    config = configparser.RawConfigParser()
    config.read(PROPERTIES_PATH)
    config_dict = dict(config.items("TWITER_APP"))

    print(config_dict)
    API_consumer_key = config_dict["api_consumer_key"]
    API_consumer_secret = config_dict["api_consumer_secret"]
    access_token_key = config_dict["access_token_key"]
    access_token_secret = config_dict["access_token_secret"]
    bearer_token = config_dict["bearer_token"]


def get_header():
    header = {"Authorization": "Bearer {}".format(bearer_token)}
    return header


#
# Rules to filter the tweets to stream
#
def set_rules():
    header = get_header()
    rules = [
        {"value": "#ParoNacional #28Abril", "tag": "Paro Nal 28 Abril"},
        {"value": "#ParoNacional28A #28Abril", "tag": "Paro Nal 28 Abril"},
        {
            "value": "#ParoNacional 28 abril (vandalos OR vandalismo)",
            "tag": "Paro Nal 21 Abril vandalismo",
        },
        {"value": "#ParoNacional 28 abril", "tag": "Paro Nal 28 Abril"},
        {
            "value": "#ParoNacional reforma tributaria",
            "tag": "Paro Nal reforma tributaria",
        },
        {
            "value": "#ParoNacional (Carrasquilla OR Duque)",
            "tag": "Paro Nal Carrasquilla Duque",
        },
        {"value": "#ParoNacional #AbusoPolicial", "tag": "Paro Nal Abuso Policial"},
        {"value": "#ParoNacional Colombia", "tag": "Paro Nal Colombia"},
    ]
    payload = {"add": rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=header,
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


#
# Obtain all the current rules and delete them.
#
def delete_rules():
    header = get_header()
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=header
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    rules = response.json()

    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=header,
        json=payload,
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


#
# Tweets sreamming
#
def get_tweets(set):
    header = get_header()
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream",
        headers=header,
        stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    config_app()
    delete_rules()
    set_rules = set_rules()
    get_tweets(set_rules)
