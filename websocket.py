import asyncio
from fastapi import FastAPI, WebSocket
import json
from pathlib import Path

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

            # Identify new jobs by comparing with stored_jobs
            new_jobs = current_jobs[len(stored_jobs):]

            for job in new_jobs:
                await websocket.send_json(job)

            # Update stored_jobs with current snapshot
            stored_jobs = current_jobs
            if len(stored_jobs) > 5:
                stored_jobs = []
                clear_jobs_file()
                print("Job list exceeded 5 entries. Cleared jobs file.")
            await asyncio.sleep(2)  # Check every 2 seconds
    except Exception as e:
        print(f"WebSocket connection error: {e}")
        await websocket.close()
