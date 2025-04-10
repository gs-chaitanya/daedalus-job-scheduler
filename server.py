from flask import Flask, request, jsonify
from uuid import uuid4
from models import CassandraConnection, create_table
from datetime import datetime

app = Flask(__name__)

# Cassandra setup
cassandra = CassandraConnection('job_keyspace')
session = cassandra.get_session()
create_table(session)

@app.route("/")
def hello_world():
    return "<p>Nutanix Paglus</p>"

@app.route('/jobs', methods=['POST'])
def create_job():
    data = request.json
    # Generate a unique job id
    job_id = uuid4()
    
    # Required fields:
    start_time = datetime.fromisoformat(data['start_time'])
    payload = data.get('payload', '')
    status = data['status']
    
    # Optional fields with default values:
    periodic_flag = data.get('periodic_flag', False)
    period_time = data.get('period_time', 0)
    retry_count = data.get('retry_count', 0)
    retry_delay = data.get('retry_delay', 0)
    error_message = data.get('error_message', '')
    
    session.execute("""
        INSERT INTO JobExecutionHistory 
        (job_id, start_time, payload, status, periodic_flag, period_time, retry_count, retry_delay, error_message)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (job_id, start_time, payload, status, periodic_flag, period_time, retry_count, retry_delay, error_message))
    
    return jsonify({'message': 'Job created successfully', 'job_id': str(job_id)}), 201

@app.route('/jobs/<uuid:job_id>', methods=['GET'])
def get_job_history(job_id):
    # Retrieve the job record using the unique job_id
    row = session.execute("""
        SELECT * FROM JobExecutionHistory WHERE job_id = %s
    """, (job_id,)).one()
    
    if row:
        result = {
            'job_id': str(row.job_id),
            'start_time': row.start_time.isoformat() if row.start_time else None,
            'payload': row.payload,
            'status': row.status,
            'periodic_flag': row.periodic_flag,
            'period_time': row.period_time,
            'retry_count': row.retry_count,
            'retry_delay': row.retry_delay,
            'error_message': row.error_message
        }
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Job not found'}), 404

@app.route('/jobs/<uuid:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.json
    fields = []
    values = []

    # Update any of the allowed fields if provided.
    for field in ['start_time', 'payload', 'status', 'periodic_flag', 'period_time', 'retry_count', 'retry_delay', 'error_message']:
        if field in data:
            fields.append(f"{field} = %s")
            # Convert start_time to datetime if needed.
            value = datetime.fromisoformat(data[field]) if field == 'start_time' else data[field]
            values.append(value)

    if not fields:
        return jsonify({'message': 'No fields to update'}), 400

    values.append(job_id)
    query = f"UPDATE JobExecutionHistory SET {', '.join(fields)} WHERE job_id = %s"
    session.execute(query, values)
    
    return jsonify({'message': 'Job updated successfully'}), 200

@app.route('/jobs/<uuid:job_id>', methods=['DELETE'])
def delete_job(job_id):
    session.execute("""
        DELETE FROM JobExecutionHistory WHERE job_id = %s
    """, (job_id,))
    return jsonify({'message': 'Job deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
