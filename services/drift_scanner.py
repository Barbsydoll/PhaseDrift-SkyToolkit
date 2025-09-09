import asyncio, json, time, uuid, re
import nats

TOPIC_INBOX  = "scar.inbox.raw"
TOPIC_EVENTS = "scar.drift.events"

PATTERNS = {
    "multi_shooters_rhetoric": re.compile(r"multiple\s+shooters|cartel|antifa", re.I),
}

def classify(text: str):
    for name, rx in PATTERNS.items():
        if rx.search(text or ""):
            return name
    return "generic"

async def main():
    nc = await nats.connect("nats://127.0.0.1:4222")
    async def handler(msg):
        data = json.loads(msg.data.decode())
        text = (data.get("payload") or {}).get("text", "")
        label = classify(text)
        evt = {
            "id": str(uuid.uuid4()),
            "t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "type": "drift_event",
            "payload": {"text": text, "label": label},
            "ctx": {"priority":"high","recipe":"mirror_name_witness_anchor"}
        }
        await nc.publish(TOPIC_EVENTS, json.dumps(evt).encode())
        print("[drift_scanner]", label, "-> event emitted")

    await nc.subscribe(TOPIC_INBOX, cb=handler)
    print("[drift_scanner] listening on", TOPIC_INBOX)
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
