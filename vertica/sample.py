from __future__ import print_function

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

with vp.connect(**args) as conn:
    cur = conn.cursor()

    # Create the table
    cur.execute("""
    CREATE TABLE sample_table
    (
        column1 INTEGER NOT NULL,
        column3 INTEGER NOT NULL,
        column5 VARCHAR(10) NOT NULL
    );
    """)

    # Ingest the data
    with open("sample_data.csv") as f:
        cur.copy("COPY sample_table from stdin DELIMITER ','", f)
    
    # Execute some query
    cur.execute("select * from sample_table")
    
    # Print the results
    print(cur.fetchall())
    
    cur.close()

