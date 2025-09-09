# Read SatNOGS client output from stdin and publish to NATS
import sys, asyncio, json, nats

async def main():
    nc = await nats.connect("nats://127.0.0.1:4222")
    for line in sys.stdin:
        msg = {"type":"sat_data","payload":{"raw":line.strip()}}
        await nc.publish("scar.sky.uplink", json.dumps(msg).encode())
    await nc.flush()
    await nc.close()

if __name__ == "__main__":
    asyncio.run(main())
