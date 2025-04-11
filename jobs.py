import time
import random
from db import save_report

async def execute_job(job_data):
    print(job_data)
    job_id = job_data["job_id"]
    # user_id = job_data["user_id"]
    payload = job_data["payload"]
    start_time = time.time()
    time.sleep(random.uniform(1, 2))  

    duration = round(time.time() - start_time, 2)
    status = 'failed' if random.random() < 0.2 else 'done'

    report = {
        "job_id": job_id,
        "status": status,
        "duration": duration,
        "result": f'Processed: {payload}',
        "payload" : payload,
        # "user_id" : user_id
    }

    await save_report(report)
    return report
