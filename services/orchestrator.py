import asyncio, json, os, uuid, time
import argparse
from typing import Dict, Any
import nats

TOPIC_EVENTS = "scar.drift.events"
TOPIC_TASKS  = "scar.echo.tasks"

def make_task(evt: Dict[str, Any]) -> Dict[str, Any]:
    payload = evt.get("payload", {})
    ctx = evt.get("ctx", {})
    recipe = ctx.get("recipe", "mirror_name_witness_anchor")
    return {
        "id": str(uuid.uuid4()),
        "t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "type": "echo_task",
        "payload": {"text": payload.get("text",""), "recipe": recipe},
        "ctx": {"priority": ctx.get("priority","normal"), "glyphs": ctx.get("glyphs", [])}
    }

async def main():
    nc = await nats.connect(servers=["nats://127.0.0.1:4222"])
    async def handler(msg):
        try:
            evt = json.loads(msg.data.decode())
            task = make_task(evt)
            await nc.publish(TOPIC_TASKS, json.dumps(task).encode())
            print("[orchestrator] created task", task["id"])
        except Exception as e:
            print("[orchestrator] error:", e)

    await nc.subscribe(TOPIC_EVENTS, cb=handler)
    print("[orchestrator] listening on", TOPIC_EVENTS)
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
