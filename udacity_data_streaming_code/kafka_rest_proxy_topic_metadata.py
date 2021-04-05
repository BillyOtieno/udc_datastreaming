import json
import requests

REST_PROXY_URL="http://localhost:8082"

# kafka-topics 
def get_topics():
    """ Gets topics from REST Proxy"""
    resp = requests.get(f"{REST_PROXY_URL}/topics")
    try:
        resp.raise_for_status()
    except:
        print("failed to list topics")
        return []

    print("topic details")
    return resp.json()


def get_topic(topic_name):
    """ Gets a specific topic specified by the {topic_name}"""
    resp = requests.get(f"{REST_PROXY_URL}/topics/{topic_name}")
    try:
        resp.raise_for_status()
    except:
        print(f"failed to fetch details of {topic_name}")
        exit(1)

    print("topic details")
    print(json.dumps(resp.json(), indent=2))


def get_brokers():
    """ Gets broker information"""
    resp = requests.get(f"{REST_PROXY_URL}/brokers")
    try:
        resp.raise_for_status()
    except:
        print(f"failed to fetch the list of brokers")
        exit(1)

    print("List of Brokers")
    print(json.dumps(resp.json(), indent=2))


def get_partitions(topic_name):
    resp = requests.get(f"{REST_PROXY_URL}/topics/{topic_name}/partitions")
    try:
        resp.raise_for_status()
    except:
        print(f"failed to fetch the list of partitions")
        exit(1)

    print("List of Partitions")
    print(json.dumps(resp.json(),indent=2))


if __name__ == '__main__':
    topics = get_topics()
    get_topic(topics[0])
    get_brokers()
    get_partitions(topics[-1])