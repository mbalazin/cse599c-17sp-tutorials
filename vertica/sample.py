import vertica_python as vp

args = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    # 10 minutes timeout on queries
    'read_timeout': 600,
    # default throw error on invalid UTF-8 results
    'unicode_error': 'strict',
    # SSL is disabled by default
    'ssl': False,
    # connection timeout is not enabled by default
    'connection_timeout': 5
}
# TODO: replace these placeholders with sample data
table_cmd = """
CREATE TABLE placeholder_table
(
    column1 INTEGER NOT NULL,
    column2 INTEGER NOT NULL,
    column3 INTEGER NOT NULL,
    column4 INTEGER NOT NULL,
    column5 VARCHAR(15) NOT NULL,
);
"""
ingest_cmd = "COPY placeholder_table from stdin DELIMITER ','"
ingest_path = "placeholder.csv"

with vp.connect(**args) as conn:
    cur = conn.cursor()
    # Create the table
    cur.execute(table_cmd)
    # Ingest the data
    with open(ingest_path) as f:
        cur.copy(ingest_cmd, f)
    # Execute some query
    cur.execute("select count(*) from paceholder_table")
    # Print the results
    print cur.fetchall()
    cur.close()

