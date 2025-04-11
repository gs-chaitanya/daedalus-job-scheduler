# app/push_job.py

import json
from pathlib import Path
from datetime import datetime

JOBS_FILE = Path("./jobs.jsonl")

def push_job():
    job_update = {
        "type": "job_update",
        "job": {
        "job_id": "5e9ba2b1-3700-4156-8b8c-f719295cdacb",
        "start_time": "2025-04-10T23:38:00",
        "user_id": "10",
        "payload": " ",
        "status": "done",
        "periodic_flag": False,
        "period_time": 1,
        "retry_count": 0,
        "retry_delay": 0,
        "error_message": ""
    }
    }

    # Append the job to the file
    with JOBS_FILE.open("a") as f:
        f.write(json.dumps(job_update) + "\n")

    print("Job pushed to file!")

if __name__ == "__main__":
    push_job()
