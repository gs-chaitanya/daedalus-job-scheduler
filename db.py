from cassandra.cluster import Cluster

def save_report(report):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('job_keyspace')
    session.execute(
        f"UPDATE jobexecutionhistory SET status='{report['status']}', error_message='{report['result']}' WHERE job_id={report['job_id']}"
    )
    # print('executed=------------------------')
    cluster.shutdown()
