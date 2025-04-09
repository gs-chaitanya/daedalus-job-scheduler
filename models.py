from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class CassandraConnection:
    def __init__(self, keyspace):
        auth_provider = PlainTextAuthProvider('', '')
        self.cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
        self.session = self.cluster.connect()
        self.session.set_keyspace(keyspace)

    def get_session(self):
        return self.session

    def shutdown(self):
        self.cluster.shutdown()

def create_table(session):
    session.execute("""
        CREATE TABLE IF NOT EXISTS JobExecutionHistory (
            job_id UUID PRIMARY KEY,
            start_time timestamp,
            payload text,
            status text,
            periodic_flag boolean,
            period_time int,
            retry_count int,
            retry_delay int,
            error_message text
        );
    """)
