from dataclasses import asdict, dataclass
import json
import faust


@dataclass
class ClickEvent(faust.Record):
    email: str
    timestamp: str
    uri: str
    number: int


@dataclass
class ClickEventSanitized(faust.Record):
    timestamp: str
    uri: str
    number: int


app = faust.App("exercise3", broker="kafka://localhost:9092")
clickevents_topic = app.topic("com.udacity.streams.clickevents", value_type=ClickEvent)


sanitized_topic = app.topic('com.udacity.streams.clickevents.noemail')

@app.agent(clickevents_topic)
async def clickevent(clickevents):
    async for clickevent in clickevents:
        #
        # TODO: Modify the incoming click event to remove the user email.
        #       Create and send a ClickEventSanitized object.
        #
        clickeventsanitized = ClickEventSanitized(
            timestamp= clickevent.timestamp,
            uri= clickevent.uri,
            number= clickevent.number
        )

        #
        # TODO: Send the data to the topic you created above.
        #       Make sure to set a key and value
        #
        await sanitized_topic.send(key=clickevent.email, value=clickeventsanitized)

if __name__ == "__main__":
    app.main()
