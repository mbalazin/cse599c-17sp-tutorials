# Installation intructions

We recommend installing Vertica via a pre-compiled Docker image.

### 1. Install Docker
*If you already have Docker installed, you can skip to Step 2.*

Docker is available for most major platforms, including Windows, Mac and Linux.
Installation instructions can be found [here](https://docs.docker.com/engine/getstarted/step_one/).
For those interested in learing more, the [Docker Docs](https://docs.docker.com) are a good
resource, especially this [Overview](https://docs.docker.com/engine/understanding-docker/).
This is also a nice [command line reference](https://docs.docker.com/engine/reference/commandline/docker/).

### 2. Install the Vertica docker container
Vertica is available on [Docker Hub](https://hub.docker.com/), which is a public
registry of Docker repositories. There are several Vertica repositories available,
but we will be using [this one](https://hub.docker.com/r/sumitchawla/vertica/).
The full installation instructions can be found by following the link, but the following
steps should suffice.

#### Retrieve the image:
`docker pull sumitchawla/vertica`

#### Run the container:
`docker run -p 5433:5433 sumitchawla/vertica`

### 3. Install the clients
There are several different clients available to comminucate with a Vertica database
that should now be running on your computer on port 5433.

#### Interactive shell: `vsql`
The vsql client is almost identical to the psql client for Postgres. [Go here](https://my.vertica.com/download/vertica/client-drivers/) to download the vsql client appropriate to your system. On OSX the download package will contain a binary `vsql` --- copy it into your working directory (preferably this one) and try to run it with `./vsql`. 

To connect to a running Vertica database (like the one you've installed above), be sure that the database is running and connect with 
```
./vsql -d docker dbadmin
```
#### Python library
The Python client library, `python-vertica`, is available on [Github](https://github.com/uber/vertica-python) and can be installed through a simple `pip` installation:
```
pip install vertica-python
```
Note that some functionality of the client depends on the Python PostgrSQL library, 
`psycopg2`, which you may need to install as well.
```
pip install psycopg2
```

#### Installation using a virtual environment
For those that would rather use a [virtual environment](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/), we provide a setup script to set that up and install the
dependencies for the Python clients. Simply run (from this directory):
```
./setup.sh
```
To activate the virtual environment:
```
source .env/bin/activate
```

Basic usage of the Python client is demonstrated in `sample.py`.

TODO: replace details in this script with actual small data

### 4. Connect to your Vertica database

Connection parameters:
Default DB Name - docker
Default User - dbadmin
Default Password (NO PASSWORD) -

### 5. Ingest data
- hava a sql file with create table statements
- commit a small example data file to repository
- put larger csv file on s3 

### 6. Download Timeseries data
To demonstrate the `TIMESLICE` facility of Vertica, we will use a dataset of GPS locations of Mallard ducks over a several month period in the UK. 

To download, change into your preferred directory and run: 
```
curl -O https://s3-us-west-2.amazonaws.com/cse599c-sp17/mallard.csv
```
You can also download the data directly by pasting the above S3 link into your browser. 

<small>Data from Kleyheeg E, van Dijk JGB, Tsopoglou-Gkina D, Woud TY, Boonstra DK, Nolet BA, Soons MB (2017) Movement patterns of a keystone waterbird species are highly predictable from landscape configuration. Movement Ecology 5(2). doi:10.1186/s40462-016-0092-7 </small>

### Generating data
- for more advanced users



# Running a query
- add sample queries
