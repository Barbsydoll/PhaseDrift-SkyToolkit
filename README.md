# Phase Drift / Sky Toolkit

This repository contains working notes and a runnable **MVP pipeline** that mirrors MAVLink swarm concepts into a
**Civic AI Mesh + Sovereign Sky** toolkit. It includes:
- A **pub/sub bus** (NATS)
- A simple **drift scanner** → **orchestrator** → **echo workers** → **sky router** → **sky nodes**
- A **SatNOGS bridge** to ingest real satellite downlink data later
- The companion **PDF guide**

> Status: Prototype. Use for simulation and integration tests. RF transmission to satellites requires proper licensing.
> Start with receive-only (SatNOGS) and HAM Technician privileges where applicable.
