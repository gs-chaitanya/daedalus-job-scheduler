from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from uuid import UUID, uuid4
from models import CassandraConnection, create_table
from datetime import datetime
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from cassandra.query import dict_factory

app = FastAPI(title="Nutanix API")

# 👇 Add this before your routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Cassandra setup
cassandra = CassandraConnection('job_keyspace')
session = cassandra.get_session()
create_table(session)

# --- Request Models ---
class JobCreate(BaseModel):
    start_time: str
    user_id: str
    payload: Optional[str] = ''
    status: str
    periodic_flag: Optional[bool] = False
    period_time: Optional[int] = 0
    retry_count: Optional[int] = 0
    retry_delay: Optional[int] = 0
    error_message: Optional[str] = ''

class JobUpdate(BaseModel):
    start_time: Optional[str] = None
    user_id: Optional[str] = None
    payload: Optional[str] = None
    status: Optional[str] = None
    periodic_flag: Optional[bool] = None
    period_time: Optional[int] = None
    retry_count: Optional[int] = None
    retry_delay: Optional[int] = None
    error_message: Optional[str] = None

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
def home():
    return "<p>Nutanix</p>"

@app.post("/jobs")
def create_job(job: JobCreate):
    job_id = uuid4()
    start_time = datetime.fromisoformat(job.start_time)
    session.execute("""
        INSERT INTO JobExecutionHistory 
        (job_id, start_time, user_id, payload, status, periodic_flag, period_time, retry_count, retry_delay, error_message)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (job_id, start_time, job.user_id, job.payload, job.status, job.periodic_flag,
          job.period_time, job.retry_count, job.retry_delay, job.error_message))
    return {"message": "Job created successfully", "job_id": str(job_id)}


@app.get("/jobs/{user_id}")
def get_jobs_by_user(user_id: str):
    session.row_factory = dict_factory
    
    
    rows = session.execute(
        "SELECT * FROM JobExecutionHistory WHERE user_id = %s ALLOW FILTERING", 
        (user_id,)
    )
    
    jobs = []
    for row in rows:
        jobs.append({
            "job_id": str(row["job_id"]),
            "start_time": row["start_time"].isoformat() if row["start_time"] else None,
            "user_id": row["user_id"],
            "payload": row["payload"],
            "status": row["status"],
            "periodic_flag": row["periodic_flag"],
            "period_time": row["period_time"],
            "retry_count": row["retry_count"],
            "retry_delay": row["retry_delay"],
            "error_message": row["error_message"]
        })

    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found for this user")
    
    return {"jobs": jobs}

@app.put("/jobs/{job_id}")
def update_job(job_id: UUID, update: JobUpdate):
    fields = []
    values = []

    for field_name, value in update.dict(exclude_unset=True).items():
        if value is not None:
            fields.append(f"{field_name} = %s")
            converted_value = datetime.fromisoformat(value) if field_name == 'start_time' else value
            values.append(converted_value)

    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    values.append(job_id)
    query = f"UPDATE JobExecutionHistory SET {', '.join(fields)} WHERE job_id = %s"
    session.execute(query, values)

    return {"message": "Job updated successfully"}

@app.delete("/jobs/{job_id}")
def delete_job(job_id: UUID):
    session.execute("DELETE FROM JobExecutionHistory WHERE job_id = %s", (job_id,))
    return {"message": "Job deleted successfully"}
