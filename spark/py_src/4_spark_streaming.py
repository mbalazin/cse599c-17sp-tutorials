# Databricks notebook source
# MAGIC %md # Structured Streaming using Python DataFrames API
# MAGIC 
# MAGIC Apache Spark 2.0 adds the first version of a new higher-level stream processing API, Structured Streaming. In this notebook we are going to take a quick look at how to use DataFrame API to build Structured Streaming applications. We want to compute real-time metrics like running counts and windowed counts on a stream of timestamped actions.
# MAGIC 
# MAGIC To run this notebook, import it to Databricks Community Edition and attach it to a **Spark 2.1 (Scala 2.10)** cluster.

# COMMAND ----------

# MAGIC %md ## Data
# MAGIC We will be using the same flights datasets as the previous sections.
# MAGIC The first few cells are simply the same data loading and cleaning you have already seen.

# COMMAND ----------

# To make sure that this notebook is being run on a Spark 2.0 cluster, let's see if we can access the SparkSession - the new entry point of Apache Spark 2.0.
# If this fails, then you are not connected to a Spark 2.0 cluster. Please recreate your cluster and select the version to be "Spark 2.0 (Scala 2.10)".
spark

# COMMAND ----------

# Set File Paths
tripdelaysFilePath = "/databricks-datasets/flights/departuredelays.csv"
airportsnaFilePath = "/databricks-datasets/flights/airport-codes-na.txt"

# Obtain airports dataset
airportsna = sqlContext.read.format("com.databricks.spark.csv").options(header='true', inferschema='true', delimiter='\t').load(airportsnaFilePath)
airportsna.registerTempTable("airports_na")

# Obtain departure Delays data
departureDelay = sqlContext.read.format("com.databricks.spark.csv").options(header='true').load(tripdelaysFilePath)

departureDelays = sqlContext.read.format("com.databricks.spark.csv").schema(departureDelay.schema).options(header='true').load(tripdelaysFilePath)

departureDelays.registerTempTable("departureDelays")
departureDelays.cache()

# Available IATA codes from the departuredelays sample dataset
tripIATA = sqlContext.sql("select distinct iata from (select distinct origin as iata from departureDelays union all select distinct destination as iata from departureDelays) a")
tripIATA.registerTempTable("tripIATA")

# Only include airports with atleast one trip from the departureDelays dataset
airports = sqlContext.sql("select f.IATA, f.City, f.State, f.Country from airports_na f join tripIATA t on t.IATA = f.IATA")
airports.registerTempTable("airports")
airports.cache()

# COMMAND ----------

# Build `departureDelays_geo` DataFrame
#  Obtain key attributes such as Date of flight, delays, distance, and airport information (Origin, Destination)  
departureDelays_geo = sqlContext.sql("select cast(f.date as int) as tripid, cast(concat(concat(concat(concat(concat(concat('2014-', concat(concat(substr(cast(f.date as string), 1, 2), '-')), substr(cast(f.date as string), 3, 2)), ' '), substr(cast(f.date as string), 5, 2)), ':'), substr(cast(f.date as string), 7, 2)), ':00') as timestamp) as `localdate`, cast(f.delay as int), cast(f.distance as int), f.origin as src, f.destination as dst, o.city as city_src, d.city as city_dst, o.state as state_src, d.state as state_dst from departuredelays f join airports o on o.iata = f.origin join airports d on d.iata = f.destination") 

# RegisterTempTable
#departureDelays_geo.repartition(50).write.json("departureDelays_json")

# Cache and Count
departureDelays_geo.cache()
departureDelays_geo.count()


# COMMAND ----------

# MAGIC %md ##Databricks Slides about Structured Streaming
# MAGIC ![Image of Slide 1](https://raw.githubusercontent.com/mbalazin/cse599c-17sp-tutorials/spark/spark/streaming_slides/1.png)
# MAGIC 
# MAGIC ![Image of Slide 2](https://raw.githubusercontent.com/mbalazin/cse599c-17sp-tutorials/spark/spark/streaming_slides/2.png)
# MAGIC 
# MAGIC ![Image of Slide 3](https://raw.githubusercontent.com/mbalazin/cse599c-17sp-tutorials/spark/spark/streaming_slides/3.png)
# MAGIC 
# MAGIC ![Image of Slide 4](https://raw.githubusercontent.com/mbalazin/cse599c-17sp-tutorials/spark/spark/streaming_slides/4.png)
# MAGIC 
# MAGIC ![Image of Slide 5](https://raw.githubusercontent.com/mbalazin/cse599c-17sp-tutorials/spark/spark/streaming_slides/5.png)
# MAGIC 
# MAGIC ![Image of Slide 6](https://raw.githubusercontent.com/mbalazin/cse599c-17sp-tutorials/spark/spark/streaming_slides/6.png)

# COMMAND ----------

# MAGIC %md ## Sample Data
# MAGIC We are now going to save the contents of the departureDelays_geo dataframe to JSON files, and use it to simulate streaming data.

# COMMAND ----------

spark.conf.set("spark.sql.shuffle.partitions", "200")  # Use 200 partitions for shuffling
departureDelays_geo.orderBy("localdate").write.json("departureDelays_json")
departureDelays_geo_schema = departureDelays_geo.schema
departureDelays_geo_schema

# COMMAND ----------

# MAGIC %fs ls departureDelays_json

# COMMAND ----------

# MAGIC %md There are 200 JSON files in the directory. Let's see what each JSON file contains.

# COMMAND ----------

# Uncomment the following line, and replace the referred filename with the desired file.
#%fs head departureDelays_json/part-00000-520fd872-efec-45c5-b5fd-1529c9be9f58-c000.json

# COMMAND ----------

# MAGIC %md ## Batch/Interactive Processing
# MAGIC The usual first step in attempting to process the data is to interactively query the data. Let's define a static DataFrame on the files, and give it a table name.

# COMMAND ----------

from pyspark.sql.types import *

inputPath = "/departureDelays_json"

# Static DataFrame representing data in the JSON files
staticInputDF = (
  spark
    .read
    .schema(departureDelays_geo_schema)
    .json(inputPath)
)

display(staticInputDF)

# COMMAND ----------

# MAGIC %md Now we can compute the number of flights leaving from each state, with 5 hour time windows. To do this, we will group by the `state_src` column and 5 hour windows over the `localdate` column.

# COMMAND ----------

from pyspark.sql.functions import *      # for window() function

staticCountsDF = (
  staticInputDF
    .groupBy(
      staticInputDF.state_src, 
      window(staticInputDF.localdate, "5 hours"))    
    .count()

)
staticCountsDF.cache()

# Register the DataFrame as table 'static_counts'
staticCountsDF.createOrReplaceTempView("static_counts")

# COMMAND ----------

# MAGIC %md Now we can directly use SQL to query the table. For example, here is a timeline of the windowed counts of flights leaving from each state.

# COMMAND ----------

# MAGIC %sql select state_src, date_format(window.end, "MMM-dd HH:mm") as time, count from static_counts order by time, state_src

# COMMAND ----------

# MAGIC %md ## Stream Processing 
# MAGIC Now that we have analyzed the data interactively, let's convert this to a streaming query that continuously updates as data comes. Since we just have a static set of files, we are going to emulate a stream from them by reading one file at a time, in the chronological order they were created. The query we have to write is pretty much the same as the interactive query above.

# COMMAND ----------

from pyspark.sql.functions import *

inputPath = "/departureDelays_json"

# Similar to definition of staticInputDF above, just using `readStream` instead of `read`
streamingInputDF = (
  spark
    .readStream                       
    .schema(departureDelays_geo_schema) # Set the schema of the JSON data
    .option("maxFilesPerTrigger", 1)  # Treat a sequence of files as a stream by picking one file at a time
    .json(inputPath)
)

# Same query as staticInputDF
streamingCountsDF = (                 
  streamingInputDF
    .groupBy(
      streamingInputDF.state_src, 
      window(streamingInputDF.localdate, "5 hours"))    
    .count()
)

# Is this DF actually a streaming DF?
streamingCountsDF.isStreaming

# COMMAND ----------

# MAGIC %md As you can see, `streamingCountsDF` is a streaming Dataframe (`streamingCountsDF.isStreaming` was `true`). You can start streaming computation, by defining the sink and starting it. 
# MAGIC In our case, we want to interactively query the counts (same queries as above), so we will set the complete set of 1 hour counts to be in a in-memory table (note that this for testing purpose only in Spark 2.0).

# COMMAND ----------

spark.conf.set("spark.sql.shuffle.partitions", "1")  # keep the size of shuffles small

query = (
  streamingCountsDF
    .writeStream
    .format("memory")        # memory = store in-memory table (for testing only in Spark 2.0)
    .queryName("counts")     # counts = name of the in-memory table
    .outputMode("complete")  # complete = all the counts should be in the table
    .start()
)

# COMMAND ----------

# MAGIC %md `query` is a handle to the streaming query that is running in the background. This query is continuously picking up files and updating the windowed counts. 
# MAGIC 
# MAGIC Note the status of query in the above cell. Both the `Status: ACTIVE` and the progress bar shows that the query is active. 
# MAGIC Furthermore, if you expand the `>Details` above, you will find the number of files they have already processed. 
# MAGIC 
# MAGIC Let's wait a bit for a few files to be processed and then interactively query the in-memory `counts` table.

# COMMAND ----------

from time import sleep
sleep(5)  # wait a bit for computation to start

# COMMAND ----------

# MAGIC %sql select state_src, date_format(window.end, "MMM-dd HH:mm") as time, count from counts order by time, state_src

# COMMAND ----------

# MAGIC %md We see the timeline of windowed counts (similar to the static one ealrier) building up. If we keep running this interactive query repeatedly, we will see the latest updated counts which the streaming query is updating in the background.

# COMMAND ----------

sleep(5)  # wait a bit more for more data to be computed

# COMMAND ----------

# MAGIC %sql select state_src, date_format(window.end, "MMM-dd HH:mm") as time, count from counts order by time, state_src

# COMMAND ----------

# MAGIC %md If you keep running the above query repeatedly, you will observe that earlier dates don't appear after later dates have been observed, as expected in a data stream where data appears in time-sorted order. This shows that Structured Streaming ensures **prefix integrity**. Structured streaming also has settings to control how out-of-order data is handled. Read the blog posts linked below if you want to know more.
# MAGIC 
# MAGIC Note that there are only a few files, so after consuming all of them there will be no updates to the counts. Rerun the query if you want to interact with the streaming query again.
# MAGIC 
# MAGIC Finally, you can stop the query running in the background, either by clicking on the 'Cancel' link in the cell of the query, or by executing `query.stop()`. Either way, when the query is stopped, the status of the corresponding cell above will automatically update to `TERMINATED`.

# COMMAND ----------

# MAGIC %md ##What's next?
# MAGIC If you want to learn more about Structured Streaming, here are a few pointers.
# MAGIC 
# MAGIC - Databricks blog posts on Structured Streaming and Continuous Applications
# MAGIC   - Blog post 1: [Continuous Applications: Evolving Streaming in Apache Spark 2.0](https://databricks.com/blog/2016/07/28/continuous-applications-evolving-streaming-in-apache-spark-2-0.html)
# MAGIC   - Blog post 2: [Structured Streaming in Apache Spark]( https://databricks.com/blog/2016/07/28/structured-streaming-in-apache-spark.html)
# MAGIC 
# MAGIC - [Structured Streaming Programming Guide](http://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
# MAGIC 
# MAGIC - Spark Summit 2016 Talks
# MAGIC   - [Structuring Spark: Dataframes, Datasets And Streaming](https://spark-summit.org/2016/events/structuring-spark-dataframes-datasets-and-streaming/)
# MAGIC   - [A Deep Dive Into Structured Streaming](https://spark-summit.org/2016/events/a-deep-dive-into-structured-streaming/)

# COMMAND ----------

# MAGIC %md ##Launching Spark not on Databricks
# MAGIC Databricks cloud is the easiest way to get Spark clusters up and running.
# MAGIC But, without paying Databricks you are limited to 1 CPU!
# MAGIC 
# MAGIC Want to run Spark locally? Download a [pre-built Spark release](http://spark.apache.org/downloads.html).
# MAGIC These come with interactive shells in python and Scala, and a dedicated Spark SQL shell.
# MAGIC You can also submit python scripts & the main classes in scala/java jars. 
# MAGIC You can configure the number of cores & amount of heap space.
# MAGIC 
# MAGIC Want a cluster on AWS? [Flintrock](https://github.com/nchammas/flintrock) by Nicholas Chammas.
# MAGIC "If you want to play around with Spark, develop a prototype application, run a one-off job, or otherwise just experiment, Flintrock is the fastest way to get you a working Spark cluster."
# MAGIC 
# MAGIC Feel free to reach out to me (Tomer) on slack if you are running into issues getting Spark up and running.
# MAGIC 
# MAGIC Getting a python notebook environment is a lot trickier. [Apache Toree](https://toree.apache.org) is attempting to solve it, but it's under incubation & proceed at your own risk!

# COMMAND ----------


