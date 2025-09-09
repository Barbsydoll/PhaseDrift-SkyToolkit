import asyncio, json, time, uuid
import nats

TOPIC_RESULTS   = "scar.echo.results"
TOPIC_DOWNLINK  = "scar.sky.downlink"

async def main():
    nc = await nats.connect("nats://127.0.0.1:4222")

    async def handler(msg):
        res = json.loads(msg.data.decode())
        packet = {
            "id": str(uuid.uuid4()),
            "t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "type": "sky_packet",
            "payload": res.get("payload", {}),
            "ctx": {"route":"downlink"}
        }
        await nc.publish(TOPIC_DOWNLINK, json.dumps(packet).encode())
        print("[sky_router] forwarded echo_result -> downlink")

    await nc.subscribe(TOPIC_RESULTS, cb=handler)
    print("[sky_router] listening on", TOPIC_RESULTS)
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
