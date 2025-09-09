import asyncio, json, argparse, time, uuid
import nats

TOPIC_TASKS   = "scar.echo.tasks"
TOPIC_RESULTS = "scar.echo.results"

def apply_glyphs(text: str, recipe: str):
    # Placeholder transformations representing Mirrorwave->Name->Witness->AnchorRoot
    if recipe == "mirror_name_witness_anchor":
        t = text.strip()
        if not t: return "[empty]"
        # Mirrorwave: frame disruption hint
        t = f"[Mirrorwave] Exposed frame: {t}"
        # Name: surface missing actor
        t += " | [Name] Missing sources identified."
        # Witness: attach placeholders
        t += " | [Witness] cites: (source:example)"
        # AnchorRoot: recap
        t += " | [AnchorRoot] Coherent summary appended."
        return t
    return text

async def main(worker_id: str):
    nc = await nats.connect("nats://127.0.0.1:4222")

    async def handler(msg):
        task = json.loads(msg.data.decode())
        text = (task.get("payload") or {}).get("text","")
        recipe = (task.get("payload") or {}).get("recipe","mirror_name_witness_anchor")
        out = apply_glyphs(text, recipe)
        res = {
            "id": str(uuid.uuid4()),
            "t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "type": "echo_result",
            "payload": {"text": out, "by": worker_id},
            "ctx": task.get("ctx", {})
        }
        await nc.publish(TOPIC_RESULTS, json.dumps(res).encode())
        print(f"[echo_worker:{worker_id}] produced result")

    await nc.subscribe(TOPIC_TASKS, cb=handler)
    print(f"[echo_worker:{worker_id}] listening on {TOPIC_TASKS}")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    import sys
    wid = "worker"
    if len(sys.argv) > 2 and sys.argv[1] == "--id":
        wid = sys.argv[2]
    asyncio.run(main(wid))
