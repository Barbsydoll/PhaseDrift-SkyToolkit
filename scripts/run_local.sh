#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start NATS (if not using docker)
if ! nc -z 127.0.0.1 4222; then
  echo "Launching NATS via docker..."
  docker run -d --name nats -p 4222:4222 nats:latest
fi

mkdir -p logs

# Launch services (background)
python3 services/orchestrator.py > logs/orchestrator.log 2>&1 &
python3 services/drift_scanner.py > logs/drift_scanner.log 2>&1 &
python3 services/echo_worker.py --id velthraun > logs/echo_velthraun.log 2>&1 &
python3 services/echo_worker.py --id gemini > logs/echo_gemini.log 2>&1 &
python3 services/echo_worker.py --id grok > logs/echo_grok.log 2>&1 &
python3 services/sky_router.py > logs/sky_router.log 2>&1 &
python3 services/sky_node.py --id sky-a > logs/sky_a.log 2>&1 &
python3 services/sky_node.py --id sky-b > logs/sky_b.log 2>&1 &
python3 services/sky_node.py --id sky-c > logs/sky_c.log 2>&1 &

echo "All services started. Tail logs in ./logs or run 'pgrep -fl python' to see PIDs."
