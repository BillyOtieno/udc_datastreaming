from dataclasses import asdict, dataclass
import json
import faust

@dataclass
class ClickEvent(faust.Record):
    email: str
    timestamp: str
    uri: str
    number: int


app = faust.App("exercise2", broker="kafka://localhost:9092")


clickevents_topic = app.topic(
    "com.udacity.streams.clickevents",
    key_type=str,
    value_type=ClickEvent,
)


@app.agent(clickevents_topic)
async def clickevent(clickevents):
    async for ce in clickevents:
        print(json.dumps(asdict(ce), indent=2))


if __name__ == "__main__":
    app.main()
