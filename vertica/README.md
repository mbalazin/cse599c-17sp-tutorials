# Installation intructions

We recommend installing Vertica via a pre-compiled Docker image.

### Installing Docker
Docker is available for most major platforms, including Windows, Mac and Linux.
Installation instructions can be found [here](https://docs.docker.com/engine/getstarted/step_one/).
For those interested in learing more, the [Docker Docs](https://docs.docker.com) are a good
resource, especially this [Overview](https://docs.docker.com/engine/understanding-docker/).
This is also a nice [command line reference](https://docs.docker.com/engine/reference/commandline/docker/).

### Installing the Vertica docker container
Vertica is available on [Docker Hub](https://hub.docker.com/), which is a public
registry of Docker repositories. There are several Vertica repositories available,
but we will be using [this one](https://hub.docker.com/r/sumitchawla/vertica/).
The full installation instructions can be found by following the link, but the following
steps should suffice.

#### Retrieve the image:
`docker pull sumitchawla/vertica`

#### Run the container:
`docker run -p 5433:5433 sumitchawla/vertica`

## Installing the clients
Different clients:
- vsql 
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


# Running a query
- add sample queries
