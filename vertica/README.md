# Installation intructions

TODO: make this more verbose

We recommend installing Vertica via a pre-compiled Docker images.

TODO:
- list of instructions for installing/configuring docker for mac/ubuntu?

To install Vertica, follow the instructions at:
https://hub.docker.com/r/sumitchawla/vertica/

## Installing the clients
Different clients:

### `vsql`
The vsql client is almost identical to the psql client for Postgres. [Go here](https://my.vertica.com/download/vertica/client-drivers/) to download the vsql client appropriate to your system. On OSX the download package will contain a binary `vsql` --- copy it into your working directory (preferably this one) and try to run it with `./vsql`. 

To connect to a running Vertica database (like the one you've installed above), be sure that the database is running and connect with 
```
./vsql -d docker dbadmin
```


- vertica-python (virtualenv scripts)

## Connecting to your Vertica database

Connection parameters:
Default DB Name - docker
Default User - dbadmin
Default Password (NO PASSWORD) -

# Ingesting data
- hava a sql file with create table statements
- commit a small example data file to repository
- put larger csv file on s3 

## Generating data
- for more advanced users

## Timeseries data
To download: 
```
curl -O https://s3-us-west-2.amazonaws.com/cse599c-sp17/mallard.csv
```

# Running a query
- add sample queries
