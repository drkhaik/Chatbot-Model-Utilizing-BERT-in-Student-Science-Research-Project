# database.py
from neo4j import GraphDatabase


class Database:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    def execute_query(self, query, database_="neo4j"):
        with self.driver.session(database=database_) as session:
            result = session.run(query)
            records = result.data()
            summary = result.consume()
            return records, summary
