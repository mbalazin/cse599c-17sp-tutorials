# Databricks notebook source
# MAGIC %md # RDDs, Dataframes, and Datasets
# MAGIC 
# MAGIC ## RDDs
# MAGIC 
# MAGIC Resilient Distributed Datasets (We talked about these!). A new range of API's has been introduced to let people take advantage of Spark's parallel execution framework and fault tolerance without making the same set of mistakes.
# MAGIC 
# MAGIC ## Dataframes
# MAGIC 
# MAGIC - RDD's with named columns.
# MAGIC - Columnar storage
# MAGIC   - Similar optimizations for OLAP queries as vertica
# MAGIC - Memory Management (Tungsten)
# MAGIC   - direct control of data storage in memory
# MAGIC     - cpu cache, and read ahead
# MAGIC   - largest source of performance increase
# MAGIC - avoids java serialization (or other not as slow but still slow serialization)
# MAGIC   - Kryo serialization
# MAGIC   - compression
# MAGIC - no garbage collection overhead
# MAGIC - Execution plans (Catalyst Optimizer)
# MAGIC   - rule based instead of cost-based optimizer
# MAGIC 
# MAGIC ## Datasets
# MAGIC 
# MAGIC adds to Dataframes
# MAGIC - compile time safety
# MAGIC - API only available through the scala (python has no type safety)
# MAGIC 
# MAGIC Encoders act as liason between JVM object and off-heap memory (the new formats introduced with Tungsten)

# COMMAND ----------

# MAGIC %md ## Let's load a file
# MAGIC 
# MAGIC 1. select 'Tables'
# MAGIC 2. in new tab, select 'Create Table'
# MAGIC 3. we could really select anything (from file upload, s3, DBFS, or JDBC) here but for now we will upload the 'mallard.csv' from the vertica demo
# MAGIC   (https://s3-us-west-2.amazonaws.com/cse599c-sp17/mallard.csv)
# MAGIC 4. select preview table
# MAGIC 5. we can name the table, select our file delimiter, etc.
# MAGIC 6. retrieve the DBFS path befor
# MAGIC 7. select 'create table'

# COMMAND ----------

# MAGIC %md # RDD's and an Introduction to the DataFram API
# MAGIC In this next section we will look at importing data from a csv file into an RDD and how to do basic queries with RDDs.
# MAGIC We will then look at how to convert an RDD into a Dataframe and repeate the same query with the Datafame API.

# COMMAND ----------

# set file path for mallard.csv import
#mallardFilePath = '/FileStore/tables/<uuid>/mallard.csv'
#mallardFilePath = ''

# structure of mallard.csv
# event-id,timestamp,location-long,location-lat

# COMMAND ----------

# Import raw rdd convert to dataframe
from pyspark.sql import types

# Create RDD from csv file
# pysqark RDD documentation: http://spark.apache.org/docs/2.1.0/api/python/pyspark.html#pyspark.RDD
mallard_rdd = sc.textFile(mallardFilePath)

# .take(n) is the standard method to return the first n elements of the RDD
mallard_rdd.take(10)

# COMMAND ----------

# display(rdd) does not work so we will make this small helper function to display an rdd
def rdd_head(rdd,n=3):
  displayHTML("Count: {} <br> {}".format(rdd.count(), "<br>".join(str(row) for row in rdd.take(n))) )

# We notice two things: 1) the header row is still included and 2) each row is a string not split into columns.
# sc.textFile simply makes a new row for each new line of the file and does not know it is a CSV.
rdd_head(mallard_rdd)

# COMMAND ----------

# We want to skip the first row using filter()

# Save header row for later 
header_row = mallard_rdd.first()

# Use a lambda function to create a new rdd without the header row.
mallard_rdd = mallard_rdd.filter(lambda row : not row.startswith('event-id'))

# The header row is now gone
rdd_head(mallard_rdd)


# COMMAND ----------

#Split rows and convert
from datetime import datetime


def make_row(row):
  """
  Convert a csv row from mallard into a tuple data type
  Input: row<str>
  Output: tuple<int,datetime,float,float>
  """
  row = row.split(',')
  return ( int(row[0]), datetime.strptime(row[1],'%Y-%m-%d %H:%M:%S.000') , float(row[2]) , float(row[3]) )

mallard_rdd = mallard_rdd.map(make_row)

# Each row of mallard_rdd is now a tuple with the data split
rdd_head(mallard_rdd)

# COMMAND ----------

# MAGIC %md #Question: What day had the most sightings?

# COMMAND ----------

# Group the data by the date
mallard_rdd_days = mallard_rdd.groupBy( 
  lambda row: str(row[1].date()) # return the date_str as the group by key
) \ #RDD with tuple rows (date_str, list of tuples from that date)
.map(
  lambda row: (row[0],len(row[1])) # tuple (date_str, len(sightings for that day) ) 
) 

rdd_head(mallard_rdd_days)

# COMMAND ----------

# Get the max dumper of sightings
mallard_rdd_days.max( lambda row: row[1] )

# COMMAND ----------

# pyspark Dataframe documentation: http://spark.apache.org/docs/2.1.0/api/python/pyspark.sql.html#pyspark.sql.DataFrame
# For structured data the DataFrame API is much more powerful than the RDD API
mallard_dataframe = mallard_rdd.toDF()
mallard_dataframe.printSchema()  # Schema does't have column names (we'll fix this)
mallard_dataframe.count()

# COMMAND ----------

# Add column names to schema using header_row from above 
header_row = header_row.split(',')
def row_func(row):
  return { header : obj for header , obj in zip(header_row,row) }

mallard_dataframe = mallard_rdd.map(row_func).toDF()
mallard_dataframe.printSchema()
mallard_dataframe.head(10)

# COMMAND ----------

# If the data is structured there is no need to go through an RDD first.  Spark now has a direct to DataFrame function.
mallard = sqlContext.read.format("com.databricks.spark.csv").options(header='true', inferschema='true', delimiter=',').load(mallardFilePath)
mallard.printSchema()
display(mallard)

# COMMAND ----------

# MAGIC %md #Question: What day had the most sightings?

# COMMAND ----------

#pyspark sql functions: http://spark.apache.org/docs/2.1.0/api/python/pyspark.sql.html#module-pyspark.sql.functions
# offers programatic SQL type commands
import pyspark.sql.functions as sf

# Answer the same question from above using the DataFrame
mallard_days = mallard \
  .select(sf.col('timestamp').cast('date').alias('date')) \
  .groupBy('date') \
  .agg(sf.count("date").alias("count")) \
  .sort(sf.col("count").desc())

display(mallard_days)

# COMMAND ----------

# A more complicated example to show the expressiveness of pysqark 
# Calculate number of sightings in 1.1km squares (~= 1 decimal places of latitude and longitude )

countOneKM = mallard.withColumn("round-long",sf.round("location-long",1)) \
  .withColumn("round-lat",sf.round("location-lat",1))\
  .select("round-long","round-lat") \
  .groupBy("round-long", "round-lat") \
  .agg(sf.count("round-long").alias('location-bin')) \
  .sort(sf.col("location-bin").desc())
display(countOneKM)

# COMMAND ----------

# MAGIC %md # Use Case: On-Time Flight Performance
# MAGIC 
# MAGIC This notebook provides an analysis of On-Time Flight Performance and Departure Delays
# MAGIC 
# MAGIC Source Data: 
# MAGIC * [OpenFlights: Airport, airline and route data](http://openflights.org/data.html)
# MAGIC * [United States Department of Transportation: Bureau of Transportation Statistics (TranStats)](http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time)
# MAGIC  * Note, the data used here was extracted from the US DOT:BTS between 1/1/2014 and 3/31/2014*
# MAGIC 
# MAGIC References:
# MAGIC * [GraphFrames User Guide](http://graphframes.github.io/user-guide.html)
# MAGIC * [GraphFrames: DataFrame-based Graphs (GitHub)](https://github.com/graphframes/graphframes)
# MAGIC * [D3 Airports Example](http://mbostock.github.io/d3/talk/20111116/airports.html)

# COMMAND ----------

# MAGIC %md ### Preparation
# MAGIC Extract the Airports and Departure Delays information from S3 / DBFS

# COMMAND ----------

# We may start by getting the DBFS paths. These are essentially just HDFS specifically for databricks
tripdelaysFilePath = "/databricks-datasets/flights/departuredelays.csv"
airportsnaFilePath = "/databricks-datasets/flights/airport-codes-na.txt"

# COMMAND ----------

# Obtain airports data. The 'sqlContext.read.format' call is the standard method for structured data ingestion (in this case for a DataFrame)
airportsna = sqlContext.read.format("com.databricks.spark.csv").options(header='true', inferschema='true', delimiter='\t').load(airportsnaFilePath)
airportsna.registerTempTable("airports_na")

# COMMAND ----------

# Obtain departure Delays data and also cache the results (materialize the 'intermediate' result in memory)
departureDelays = sqlContext.read.format("com.databricks.spark.csv").options(header='true').load(tripdelaysFilePath)
departureDelays.registerTempTable("departureDelays")
departureDelays.cache()

# COMMAND ----------

# we can not print the schema for either DF
airportsna.printSchema()

# COMMAND ----------

departureDelays.printSchema()

# COMMAND ----------

# MAGIC %md ### We can query our DF with both a programatic and SQL interface (via the registered table)
# MAGIC 
# MAGIC it depends on which is more practical

# COMMAND ----------

# try and sort departueDelays on the delay column and preview the first 3 and save it as a new table sortDelays
sortDelays = departureDelays.sort("delay")
sortDelays.head(3)

# COMMAND ----------

# We have already registered departure delays and we may write an equivalent query in SQL
# use pysqark.sql.functions which is already imported as sf
departureDelays.registerTempTable("depature_delays")
sortDelays_sql = sqlContext.sql("SELECT * FROM depature_delays ORDER BY delay")
sortDelays_sql.head(3)

# COMMAND ----------

# We might want to use group bys and aggregates. This is doable through the .agg and SQL function ('sf' from earlier)
# find all desitinations whose average distance is greater than 1000
# (note that queries for learning purposes need not make sense)
longAvgDistByDest = departureDelays.groupBy("destination")\
  .agg(sf.avg("distance").alias("avg_dist"))\
  .where("avg_dist > 1000")
longAvgDistByDest.head(3)

# COMMAND ----------

# That wasn't too tedious but it might be easier just to write it as a SQL command:
longAvgDistByDest_sql = sqlContext.sql("SELECT destination, avg(distance) AS avg_dist FROM depature_delays GROUP BY destination HAVING avg_dist > 1000")
longAvgDistByDest_sql.head(3)

# COMMAND ----------

# we can also use the python fluent API to execute joins
# lets get the average flight delay to every city from seattle
# but we want the actual city name and not just the airport code
from pyspark.sql.functions import col
delayedSeaDest = departureDelays.join(airportsna, departureDelays["destination"] == airportsna["IATA"], 'inner')\
  .filter(col("origin") == 'SEA')\
  .groupBy("City")\
  .agg(sf.avg("delay").alias("avg_delay"))\
  .orderBy(sf.col("avg_delay").desc())
delayedSeaDest.head(3)

# COMMAND ----------

# this would likley be easier using the declarative API.
airportsna.registerTempTable("airports")
delayedSeaDest_sql = sqlContext.sql("SELECT destination, avg(delay) AS avg_delay FROM depature_delays, airports WHERE origin = 'SEA' AND destination = IATA GROUP BY destination ORDER BY -avg_delay")
delayedSeaDest_sql.head(3)

# COMMAND ----------

# spark also allows you to look up the query plan.
# We should observe that the plans look the same for both the SQL and programatic approaches 
delayedSeaDest.explain()

# COMMAND ----------

delayedSeaDest_sql.explain()

# COMMAND ----------


