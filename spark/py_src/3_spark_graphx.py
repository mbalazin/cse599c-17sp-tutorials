# Databricks notebook source
##############################GraphFrames (GraphX) Example##############################
# This is an example of using GraphX library over airport and flights dataset. We will 
# build a graph where each airport is a vertex and the flights between airports are
# edges. Then we will query this graph to utilize the power of graph operations. One of
# the powerful built-in tool is getting page rank for each vertex.
########################################################################################


# Paths to datasets
tripdelaysFilePath = "/databricks-datasets/flights/departuredelays.csv"  # departure delay times of flights
airportsnaFilePath = "/databricks-datasets/flights/airport-codes-na.txt"  # information about where airports are located

# Obtain airports dataset
airportsna = sqlContext.read.format("com.databricks.spark.csv").options(header='true', inferschema='true', delimiter='\t').load(airportsnaFilePath)
airportsna.registerTempTable("airports_na") # make table available in sql commands

# Obtain departure delay dataset
departureDelays = sqlContext.read.format("com.databricks.spark.csv").options(header='true').load(tripdelaysFilePath)
departureDelays.registerTempTable("departureDelays")
departureDelays.cache() # caches table in memory (lazy); can also use sqlContext.cacheTable (greedy)

# Available IATA codes from the departure delay dataset
tripIATA = sqlContext.sql("SELECT DISTINCT iata FROM (SELECT DISTINCT origin as iata FROM departureDelays UNION ALL SELECT DISTINCT destination as iata FROM departureDelays) a")
tripIATA.registerTempTable("tripIATA")

# Only include airports with at least one trip from the departureDelays dataset
airports = sqlContext.sql("SELECT f.IATA, f.City, f.State, f.Country FROM airports_na f JOIN tripIATA t ON t.IATA = f.IATA")
airports.registerTempTable("airports")
airports.cache()

departureDelays_geo = sqlContext.sql("SELECT cast(f.date as int) as tripid, cast(f.delay as int) as delay, cast(f.delay < 0 as int) as delay_bool, cast(f.distance as int), f.origin as src, f.destination as dst, o.city as city_src, d.city as city_dst, o.state as state_src, d.state as state_dst from departuredelays f JOIN airports o ON o.iata = f.origin JOIN airports d ON d.iata = f.destination") 

# RegisterTempTable
departureDelays_geo.registerTempTable("departureDelays_geo")

# Cache and Count
departureDelays_geo.cache()
departureDelays_geo.count()


# COMMAND ----------

#List all airports
display(airports)

# COMMAND ----------

#List all flights
display(departureDelays_geo)

# COMMAND ----------

# Importing graph frames and building a graph from the data

from graphframes import *

#Vertex DataFrame: A vertex DataFrame should contain a special column named ?id? which specifies unique IDs for each vertex in the graph.
vertices = sqlContext.sql("SELECT iata as id, City FROM airports")

#Edge DataFrame: An edge DataFrame should contain two special columns: ?src? (source vertex ID of edge) and ?dst? (destination vertex ID of edge).
edges = sqlContext.sql("SELECT src, dst, delay FROM departureDelays_geo")

#Both DataFrames can have arbitrary other columns. Those columns can represent vertex and edge attributes.

#Vertices need a column named id that is unique
display(vertices)


# COMMAND ----------

#Edges need a src and dst column representing the source and destination of the edge
display(edges)

# COMMAND ----------

#Let's create a graph from these vertices and edges:
g = GraphFrame(vertices, edges)

# COMMAND ----------

#Basic graph and DataFrame queries

#List all the vertices in the graph
display(g.vertices)

# COMMAND ----------

#List all the edges in the graph
display(g.edges)

# COMMAND ----------

#List all the vertices with the number of edges pointing to it
display(g.inDegrees)

# COMMAND ----------

#List all the vertices with the number of edges originating from it 
display(g.outDegrees)

# COMMAND ----------

#List most busy airports based on number of flights landing
display(g.inDegrees.orderBy('inDegree', ascending=False).limit(5))

# COMMAND ----------

#List most busy airports based on number of flights taking off
display(g.outDegrees.orderBy('outDegree', ascending=False).limit(5))

# COMMAND ----------

#Set a check point directory to save data without linkage
sc.setCheckpointDir("/tmp/")

#Find connected airports
result_con = g.connectedComponents()
result_con.show()

# COMMAND ----------

#Count the number of airports in the first connected graph
result_con.where(result_con.component == 1).count()

# COMMAND ----------

#Count the number of airports in the graph
vertices.count()

# COMMAND ----------

#Compare the delays between two airports. Meaning search for pairs of vertices with edges in both directions between them.
motifs = g.find("(a)-[e1]->(b); (b)-[e2]->(a)")
display(motifs)

# COMMAND ----------

#See a shorter list
display(motifs.distinct())

# COMMAND ----------

#Shortest Path: Find the number of flights from each airport to listed airport(s)
results_path = g.shortestPaths(landmarks=["ATL", "GFK"])
display(results_path)

# COMMAND ----------

#Search for specific airport within the results
display(results_path.where(results_path.id == "ATL"))

# COMMAND ----------

#PageRank: Identify important airports in the graph based on connections.
results_rank = g.pageRank(maxIter=2, sourceId="ATL")
results_rank.show()

# COMMAND ----------

#Order the airports by page rank
display(results_rank.vertices.orderBy('pagerank', ascending=False))
