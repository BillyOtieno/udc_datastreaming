import asyncio
from dataclasses import dataclass, field
import json as json
import random


from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic
from faker import Faker


faker = Faker()

BROKER_URL = "PLAINTEXT://localhost:9092"

async def produce(topic_name):
    """ Produces data into the Kafka Topic"""
    p = Producer({"bootstrap.servers":BROKER_URL})
    while True:
        p.produce(topic_name, ClickEvent().serialize())
        await asyncio.sleep(1.0)


async def consumer(topic_name):
    """ Consumes data from a Kafka Topic """
    c = Consumer({'bootstrap.servers':BROKER_URL, 'group.id':"0"})
    c.subscribe([topic_name])

    while True:
        if message is None:
            print("No message received by Consumer")
        elif message.error() is not None:
            print(f"error from consumer {message.error()}")
        else:
            try:
                print(message.key(), message.value())
            except KeyError as e:
                print(f"Failed to unpack message {e}")
        await asyncio.sleep(1.0)

def main():
    """ Checks from topic and creates topic if it doesn't exist"""
    client = AdminClient({"bootstrap.servers":BROKER_URL})

    try:
        asyncio.run(produce_consumer("com.udacity.lesson3.exercise1.clicks"))
    except KeyboardInterrupt as e:
        print("Shutting down")

async def produce_consumer(topic_name):
    """ Runs the Producer and Consumer Tasks"""
    t1 = asyncio.create_task(produce(topic_name))
    t2 = asyncio.create_task(consumer(topic_name))
    await t1
    await t2

@dataclass
class ClickEvent:
    email: str = field(default_factory=faker.email)
    timestamp: str = field(default_factory=faker.iso8601)
    uri: str = field(default_factory=faker.uri)

    num_calls = 0

    def serialize(self):
        email_key = "email" if ClickEvent.num_calls < 10 else "user_email"
        ClickEvent.num_calls += 1
        return json.dumps({
            "uri": self.uri,
            # "timestamp":self.timestamp,
            random.choice(["timestamp","time"]): self.timestamp,
            email_key:self.email
        })


if __name__=="__main__":
    main()
