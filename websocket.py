import asyncio
from fastapi import FastAPI, WebSocket
import json
from pathlib import Path
from starlette.websockets import WebSocketDisconnect

app = FastAPI()
JOBS_FILE = Path("jobs.jsonl")

# In-memory store of already seen jobs
stored_jobs = []

def load_jobs_from_file():
    jobs = []

    if JOBS_FILE.exists():
        with JOBS_FILE.open("r") as f:
            for line in f:
                try:
                    jobs.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
    return jobs

def clear_jobs_file():
    if JOBS_FILE.exists():
        JOBS_FILE.write_text("")

@app.on_event("startup")
async def startup_event():
    global stored_jobs
    stored_jobs = load_jobs_from_file()
    print("Jobs loaded at startup:")
    print(json.dumps(stored_jobs, indent=2))

@app.websocket("/ws/jobs")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global stored_jobs

    try:
        while True:
            current_jobs = load_jobs_from_file()
            new_jobs = current_jobs[len(stored_jobs):]

            for job in new_jobs:
                try:
                    await websocket.send_json(job)
                except RuntimeError:
                    print("Tried to send to a closed WebSocket.")
                    break

            stored_jobs = current_jobs
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        print("Client disconnected cleanly.")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        try:
            await websocket.close()
        except:
            pass
