import asyncio, json, time, uuid, argparse, random
from croniter import croniter
import nats
from datetime import datetime

TOPIC_DOWNLINK = "scar.sky.downlink"
TOPIC_UPLINK   = "scar.sky.uplink"

def visible_now(expr: str, now=None) -> bool:
    now = now or datetime.utcnow()
    # Visible if we're within first 20s of a cron tick
    base = croniter(expr, now).get_prev(datetime)
    return (now - base).total_seconds() <= 20

async def main(node_id: str, cron_expr: str):
    nc = await nats.connect("nats://127.0.0.1:4222")

    async def handler(msg):
        pkt = json.loads(msg.data.decode())
        if not visible_now(cron_expr):
            # no pass right now; drop
            return
        if random.random() < 0.2:
            # simulate dropout
            return
        uplink = {
            "id": str(uuid.uuid4()),
            "t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "type": "sky_receipt",
            "payload": {"ok": True, "node": node_id, "echo": pkt.get("payload",{})},
            "ctx": {"route":"uplink"}
        }
        await nc.publish(TOPIC_UPLINK, json.dumps(uplink).encode())
        print(f"[sky_node:{node_id}] acked one packet")

    await nc.subscribe(TOPIC_DOWNLINK, cb=handler)
    print(f"[sky_node:{node_id}] online; pass window:", cron_expr)
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    import sys
    node_id = "sky-a"
    cron_expr = "*/7 * * * *"
    # crude arg parse
    if "--id" in sys.argv:
        node_id = sys.argv[sys.argv.index("--id")+1]
    if "--cron" in sys.argv:
        cron_expr = sys.argv[sys.argv.index("--cron")+1]
    asyncio.run(main(node_id, cron_expr))
