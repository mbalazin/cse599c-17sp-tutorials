## Installing Docker, Vertica, clients
*See README.md for detailed instructions*

### Docker Containers
```
docker run ubuntu /bin/echo "Hello World!"
docker run -ti ubuntu /bin/bash
```
From within the container try running `ps aux` and `ls /bin`.

- Docker containers run in their own isolated *namespace*.
- Resource allocation can be managed through *control groups*.
- Lightweight: Immutable base image and layered file system.

#### Creating Docker Images
The [Dockerfile](https://github.com/sumitchawla/docker-vertica) 
for the Vertica image we installed is a great example.

#### Useful commands
```
docker ps
docker ps -a
docker start
docker stop
docker cp
docker rm
```

## Vertica Tutorial

### 1. Connect to the container
```
docker exec -ti <CONTAINER ID> /bin/bash
```
Explore the environment. Look at `/home/dbadmin/docker`.
Connect to a Vertica interactive shell:
```
/opt/vertica/bin/vsql -d docker dbadmin
\h
\d
select * from sample_table;
```
You can also do this more directly through Docker:
```
docker exec -ti <CONTAINER ID> /opt/vertica/bin/vsql -d docker dbadmin
```

### 2. Generate data
```
./dbgen_script/dbgen.sh
```
You should see six new csv files in your directory: 
`comments.csv, hidden.csv, messages.csv, sample_data.csv, stories.csv, taggings.csv, 
tags.csv`.

### 3. Create the schema
Create the schema and tables by executing a sql file.
```
./opt/vertica/bin/vsql -f dbgen_script/create_tables.sql -d docker dbadmin
./opt/vertica/bin/vsql -d docker dbadmin
\d
\d lobsters.hidden
```
### 4. Ingesting the data through `vsql`
From `vsql` executing something like `COPY lobsters.tags FROM 'tags.csv';` will fail
because the container does not have access to your file system.
You can mount a volume to make it accessible to the container (`run -v` command).
A simple way to transfer a file over to Docker is to copy it.
```
docker cp tags.csv [CONTAINER ID]:/path
```
Now you can ingest the file through `vqsl`
```
COPY lobsters.tags FROM '/tmp/tags.csv' DELIMITER ',';
select * from lobsters.tags;
```

### 5. Ingesting the data through `python-vertica`
In a Python shell:
```
with open("args.json") as f:
    args = json.load(f)
conn = vp.connect(**args)
cur = conn.cursor()
cur.execute("select * from sample_table")
cur.fetchone()
cur.fetchall()

with open("taggings.csv", "rb") as f:
    cur.copy("COPY lobsters.taggings from stdin DELIMITER ','", f)
with open("hidden.csv", "rb") as f:
    cur.copy("COPY lobsters.hiddens from stdin DELIMITER ','", f)
with open("stories.csv", "rb") as f:
    cur.copy("COPY lobsters.stories from stdin DELIMITER ','", f)

```

