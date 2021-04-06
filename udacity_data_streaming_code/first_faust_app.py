import faust

app = faust.App("hello-world-faust", broker="localhost:9092")
topic = app.topic("com.udacity.streams.clickevents")

@app.agent(topic)
async def clickevent(clickevents):
    async for event in clickevents:
        print(event)

if __name__ == '__main__':
    app.main()