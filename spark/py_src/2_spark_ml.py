# Databricks notebook source
##############################MLLib Example##############################
# In this example, we are going to be building a classifer to try to predict if a flight in the US is going to be late or not
# based on the flights' origin airport, destination airport, and distance. We will be using logistic regression to train our
# model and then test it using a separate test set. At then end, we will report the percent error of the test set.

# To get the data we will combine two datasets: one of the flight delays and one of information on where the airport is
# located. The goal is to see how to combine datasets.

# In the real world, you would likely have more attributes and more data, but this is just an example to show how to set up
# and use the MLLib library.

# First we need to collect out data
# Paths to datasets
tripdelaysFilePath = "/databricks-datasets/flights/departuredelays.csv"  # departure delay times of flights
airportsnaFilePath = "/databricks-datasets/flights/airport-codes-na.txt"  # information about where airports are located

# Obtain airports dataset
airportsna = sqlContext.read.format("com.databricks.spark.csv").options(header='true', inferschema='true', delimiter='\t').load(airportsnaFilePath)
airportsna.registerTempTable("airports_na") # make table available in sql commands


# COMMAND ----------

# Obtain departure delay dataset
departureDelays = sqlContext.read.format("com.databricks.spark.csv").options(header='true').load(tripdelaysFilePath)
departureDelays.registerTempTable("departureDelays")
departureDelays.cache() # caches table in memory (lazy); can also use sqlContext.cacheTable (greedy)

# COMMAND ----------

# Now we need to do some transformations to our data
# First, we get available IATA airport codes from the departure delay dataset
# making sure to take all district codes from the origins and destinations
tripIATA = sqlContext.sql("SELECT DISTINCT iata FROM (SELECT DISTINCT origin as iata FROM departureDelays UNION ALL SELECT DISTINCT destination as iata FROM departureDelays) a")
tripIATA.registerTempTable("tripIATA")

# Now we need to filter the airports so we only include airports
# with at least one trip from the departureDelays dataset
airports = sqlContext.sql("SELECT f.IATA, f.City, f.State, f.Country FROM airports_na f JOIN tripIATA t ON t.IATA = f.IATA")
airports.registerTempTable("airports")
airports.cache()

# This is a long query that selects the attributes we want from the data, joining airports with departuredelays
# We also make departure delay a binary 0/1 label to use in our classification
departureDelays_geo = sqlContext.sql("SELECT cast(f.date as int) as tripid, cast(f.delay as int) as delay, cast(f.delay < 0 as int) as delay_bool, cast(f.distance as int), f.origin as src, f.destination as dst, o.city as city_src, d.city as city_dst, o.state as state_src, d.state as state_dst from departuredelays f JOIN airports o ON o.iata = f.origin JOIN airports d ON d.iata = f.destination") 

# RegisterTempTable
departureDelays_geo.registerTempTable("departureDelays_geo")

# Cache and Count
departureDelays_geo.cache()
departureDelays_geo.count()

# COMMAND ----------

# Now it's time for the machine learning in pyspark
from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
# STRING INDEXER EXAMPLE: outputs categoryIndex after run in category
#  id | category | categoryIndex
# ----|----------|---------------
#  0  | a        | 0.0
#  1  | b        | 2.0
#  2  | c        | 1.0
#  3  | a        | 0.0
#  4  | a        | 0.0
#  5  | c        | 1.0

# ONE HOT ENCODER: changes numeric value into binary vector with a 1 in the place of value

# First, we need to build our ML pipeline
# We begin by gathering the features we need in our feature vector (origin, destination, and distance)
# We start by adding in functions to transform the categorical variables to numeric ones
categoricalColumns = ["src", "dst"]
stages = [] # stages in our Pipeline
for categoricalCol in categoricalColumns:
  # Category Indexing with StringIndexer
  stringIndexer = StringIndexer(inputCol=categoricalCol, outputCol=categoricalCol+"Index")
  # Use OneHotEncoder to convert categorical variables into binary SparseVectors
  encoder = OneHotEncoder(inputCol=categoricalCol+"Index", outputCol=categoricalCol+"classVec")
  # Add stages. These are not run here, but will run all at once later on.
  stages += [stringIndexer, encoder]


# COMMAND ----------

# Use StringIndexer to turn label column into numeric column
# We technically do not need to do this because we already have 0/1, but this is good
# step for other classification labels (e.g. TRUE/FALSE, GOOD/BAD, ...)
label_stringIdx = StringIndexer(inputCol = "delay_bool", outputCol = "label")
stages += [label_stringIdx]

# Now we need to add in our numeric columns
numericCols = ["distance"]
assemblerInputs = map(lambda c: c + "classVec", categoricalColumns) + numericCols

# Assemble all columns into feature vector for classification
assembler = VectorAssembler(inputCols=assemblerInputs, outputCol="features")
stages += [assembler]

pipeline = Pipeline(stages=stages)
# Run the feature transformations.
#  fit() computes feature statistics as needed.
#  transform() actually transforms the features.
pipelineModel = pipeline.fit(departureDelays_geo)
dataset = pipelineModel.transform(departureDelays_geo)

# Print the schema
dataset.printSchema()

# COMMAND ----------

# Keep relevant columns
selectedcols = ["label", "features"] + departureDelays_geo.columns

# Split into training and test data
(trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed = 100)

# COMMAND ----------

from pyspark.ml.classification import LogisticRegression

# Create initial LogisticRegression model
lr = LogisticRegression(labelCol="label", featuresCol="features", maxIter=10)

# Train model with Training Data
lrModel = lr.fit(trainingData)

# Predict and test using Test Data
predictions = lrModel.transform(testData)

selected = predictions.select("label", "prediction", "probability")
display(selected)

# COMMAND ----------

# If you want to simply collect the results as a list of Rows
test = selected.collect()  #use collect to turn into list of Row elements
print(test[0])  #gets first row

# COMMAND ----------

from pyspark.sql import functions as F
# Compute squared difference between label and prediciton
test = selected.select(((selected.label-selected.prediction)*(selected.label-selected.prediction)).alias("diff"))
# Sum the difference and turn into a list of one Row
sumres = test.select(F.sum("diff").alias("total_error")).collect()
# Divide sum by the total number of rows
print("Percent Error", sumres[0].total_error/test.count())

# COMMAND ----------


