## How to generate data and ingest data into your vertica database

### Generating database schema
Once your Vertica database is up and running, execute the following queries to generate the tables required to load our dataset.

`CREATE SCHEMA lobsters;`

`CREATE TABLE lobsters.tags ( id integer NOT NULL, tag varchar(64));`

`CREATE TABLE lobsters.taggings (id integer NOT NULL, story_id integer NOT NULL, tag_id integer NOT NULL);`

`CREATE TABLE lobsters.hiddens (id integer NOT NULL, user_id integer NOT NULL, story_id integer NOT NULL);`

`CREATE TABLE lobsters.stories (id integer NOT NULL, created_at TIMESTAMP, description varchar(4095), hotness float, markeddown_description varchar(4095), short_id varchar(255), title varchar(1023), upvotes integer, downvotes integer, url varchar(255), user_id integer);`

### Generating data
Once the schema is ready. Generate the sample data using the following command:

`First run ./dbgen.sh`

Edit the variables in the script to control the amount of data generated.

### Ingesting data into the database

Type the following commands on a vertical terminal, replacing the file path with the correct path to your generated data files. You can use the provided python script to load data into the database.

`COPY lobsters.tags FROM '/home/dbuser/cse599c-17sp-tutorials/vertica/dbgen_script/tags.csv' PARSER fcsvparser();`

`COPY lobsters.taggings FROM '/home/dbuser/cse599c-17sp-tutorials/vertica/dbgen_script/taggings.csv' PARSER fcsvparser();`

`COPY lobsters.hiddens FROM '/home/dbuser/cse599c-17sp-tutorials/vertica/dbgen_script/hidden.csv' PARSER fcsvparser();`

`COPY lobsters.stories FROM '/home/dbuser/cse599c-17sp-tutorials/vertica/dbgen_script/stories.csv' PARSER fcsvparser();`


The data is kind of a fake dataset for website http://lobste.rs
