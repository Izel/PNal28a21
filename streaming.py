import requests
import os
from time import gmtime, strftime
import json
import configparser

from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists, InvalidArgument


#
# Set the environment variable with your bearer_token
#
bearer_token = os.environ.get("BEARER_TOKEN")

#
# Setting up GCP Variables
#
project_id = "pnal28a21"
topic_id = "twitter28a"
topic_name = "projects/{project}/topics/{topic}".format(
    project=project_id,
    topic=topic_id,
)


def init_GCP():
    publisher_client = pubsub_v1.PublisherClient()
    # Check if the topic exists. If dont, the topic is created
    try:
        topic = publisher_client.create_topic(request={"name": topic_name})
    except AlreadyExists:
        return publisher_client
    except InvalidArgument:
        print(
            "Error: Please, check if the Project name '{project}' is correct and the topic name '{topic}' format is correct".format(
                project=project_id,
                topic=topic_id,
            )
        )
        return None


def get_header():
    header = {"Authorization": "Bearer {}".format(bearer_token)}
    return header


#
# Rules to filter the tweets to stream
#
def set_rules():
    header = get_header()
    with open("rules.json") as f:
        rules = json.load(f)
        payload = {"add": rules["rules"]}

        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers=header,
            json=payload,
        )

        if response.status_code != 201:
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )

        print("### Rules setting result")
        print(json.dumps(response.json()))
        print("###")
        return

    raise Exception("Not possible open fine rules.json")


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
    print("### Rules deletion result")
    print(json.dumps(response.json()))
    print("###")


#
# Tweets sreaming
#
def get_tweets(set, publisher_client):
    header = get_header()
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream",
        headers=header,
        stream=True,
    )

    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            json_response["data"]["datetime"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            data = json.dumps(json_response).encode("utf-8")
            future = publisher_client.publish(topic_name, data)


def main():
    publisher_client = init_GCP()
    delete_rules()
    rules = set_rules()
    get_tweets(rules, publisher_client)


if __name__ == "__main__":
    main()
