from cassandra.cluster import Cluster
import json
from pathlib import Path

JOBS_FILE = Path("jobs.jsonl")

async def save_report(report):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('job_keyspace')

    session.execute(
        f"""
        UPDATE jobexecutionhistory
        SET status='{report['status']}',
            error_message='{report['result']}'
        WHERE job_id={report['job_id']}
        """
    )
    cluster.shutdown()
    
    # Append report to the JSONL file
    with JOBS_FILE.open("a") as f:
        f.write(json.dumps(report) + "\n")
