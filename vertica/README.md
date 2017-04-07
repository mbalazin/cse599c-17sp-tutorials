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
To demonstrate the `TIMESLICE` facility of Vertica, we will use a dataset of GPS locations of Mallard ducks over a several month period in the UK. 

To download, change into your preferred directory and run: 
```
curl -O https://s3-us-west-2.amazonaws.com/cse599c-sp17/mallard.csv
```
You can also download the data directly by pasting the above S3 link into your browser. 

<small>Data from Kleyheeg E, van Dijk JGB, Tsopoglou-Gkina D, Woud TY, Boonstra DK, Nolet BA, Soons MB (2017) Movement patterns of a keystone waterbird species are highly predictable from landscape configuration. Movement Ecology 5(2). doi:10.1186/s40462-016-0092-7 </small>

# Running a query
- add sample queries
