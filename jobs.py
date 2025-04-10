import time
import random
from db import save_report

def execute_job(job_data):
    job_id = job_data["job_id"]
    payload = job_data["payload"]
    start_time = time.time()
    time.sleep(random.uniform(1, 2))  # simulate work

    if random.random() < 0.2:
        print("Simulated failure")

    duration = round(time.time() - start_time, 2)
    report = {
        "job_id": job_id,
        "status": 'done',
        "duration": duration,
        "result": f'Processed: {payload}'
    }
    save_report(report)
    return report
