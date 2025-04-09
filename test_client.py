import requests
import uuid
from datetime import datetime
import json


BASE_URL = "http://localhost:5000"

def test_create_job():
    print("\n=== Testing Job Creation ===")
    job_data = {
        "start_time": datetime.now().isoformat(),
        "payload": "Fuck ankita",
        "status": "pending",
        "periodic_flag": True,
        "period_time": 3600,
        "retry_count": 3
    }
    
    response = requests.post(f"{BASE_URL}/jobs", json=job_data)
    print(f"Status Code: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2))
    
    if response.status_code == 201:
        return response.json()['job_id']
    return None

def test_get_job(job_id):
    print("\n=== Testing Job Retrieval ===")
    response = requests.get(f"{BASE_URL}/jobs/{job_id}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("Job Details:")
        print(json.dumps(response.json(), indent=2))
    else:
        print("Error:", response.json())

def test_update_job(job_id):
    print("\n=== Testing Job Update ===")
    update_data = {
        "status": "processing",
        "error_message": "Initializing resources",
        "retry_count": 2
    }
    
    response = requests.put(f"{BASE_URL}/jobs/{job_id}", json=update_data)
    print(f"Status Code: {response.status_code}")
    print("Update Response:", json.dumps(response.json(), indent=2))
    
    # Verify changes
    if response.status_code == 200:
        verify_response = requests.get(f"{BASE_URL}/jobs/{job_id}")
        print("\nUpdated Job Details:")
        print(json.dumps(verify_response.json(), indent=2))

def test_delete_job(job_id):
    print("\n=== Testing Job Deletion ===")
    response = requests.delete(f"{BASE_URL}/jobs/{job_id}")
    print(f"Status Code: {response.status_code}")
    print("Delete Response:", json.dumps(response.json(), indent=2))
    
    # Verify deletion
    verify_response = requests.get(f"{BASE_URL}/jobs/{job_id}")
    print("\nPost-Deletion Verification:")
    print(f"Status Code: {verify_response.status_code}")
    print("Response:", verify_response.json())

def main():
    # Test full CRUD lifecycle
    job_id = test_create_job()
    
    # if job_id:
    #     # test_get_job(job_id)
    #     # test_update_job(job_id)
    #     # test_delete_job(job_id)
    # else:
    #     print("Initial creation failed, skipping other tests")

if __name__ == "__main__":
    main()
