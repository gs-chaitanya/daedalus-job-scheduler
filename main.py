from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

from models import CassandraConnection, create_table

app = FastAPI(title="Job Space API")

# Cassandra setup
cassandra = CassandraConnection('job_space')
session = cassandra.get_session()
create_table(session)

# Pydantic Model for job creation/updation
class JobBase(BaseModel):
    start_time: datetime
    payload: Optional[str] = ''
    status: str
    periodic_flag: Optional[bool] = False
    period_time: Optional[int] = 0
    retry_count: Optional[int] = 0
    retry_delay: Optional[int] = 0
    error_message: Optional[str] = ''

class JobUpdate(BaseModel):
    start_time: Optional[datetime] = None
    payload: Optional[str] = None
    status: Optional[str] = None
    periodic_flag: Optional[bool] = None
    period_time: Optional[int] = None
    retry_count: Optional[int] = None
    retry_delay: Optional[int] = None
    error_message: Optional[str] = None

@app.get("/")
def hello_world():
    return {"message": "Nutanix Paglus"}

@app.post("/jobs")
def create_job(job: JobBase):
    job_id = uuid4()
    session.execute("""
        INSERT INTO JobExecutionHistory 
        (job_id, start_time, payload, status, periodic_flag, period_time, retry_count, retry_delay, error_message)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (job_id, job.start_time, job.payload, job.status, job.periodic_flag, job.period_time, job.retry_count, job.retry_delay, job.error_message))
    
    return {"message": "Job created successfully", "job_id": str(job_id)}

@app.get("/jobs/{job_id}")
def get_job_history(job_id: UUID):
    row = session.execute("""
        SELECT * FROM JobExecutionHistory WHERE job_id = %s
    """, (job_id,)).one()

    if row:
        return {
            "job_id": str(row.job_id),
            "start_time": row.start_time.isoformat() if row.start_time else None,
            "payload": row.payload,
            "status": row.status,
            "periodic_flag": row.periodic_flag,
            "period_time": row.period_time,
            "retry_count": row.retry_count,
            "retry_delay": row.retry_delay,
            "error_message": row.error_message
        }
    else:
        raise HTTPException(status_code=404, detail="Job not found")

@app.put("/jobs/{job_id}")
def update_job(job_id: UUID, job: JobUpdate):
    fields = []
    values = []

    for field_name, field_value in job.dict(exclude_unset=True).items():
        fields.append(f"{field_name} = %s")
        values.append(field_value)

    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    values.append(job_id)
    query = f"UPDATE JobExecutionHistory SET {', '.join(fields)} WHERE job_id = %s"
    session.execute(query, values)
    
    return {"message": "Job updated successfully"}

@app.delete("/jobs/{job_id}")
def delete_job(job_id: UUID):
    session.execute("""
        DELETE FROM JobExecutionHistory WHERE job_id = %s
    """, (job_id,))
    return {"message": "Job deleted successfully"}
