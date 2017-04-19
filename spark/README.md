# Spark in the cloud (with Databricks)

## 1. Getting Started
For this tutorial, we are going to use Databricks - the commercialization of spark
as a cloud based service from some of the original designers. Using Databricks makes
setup very easy, and the free tier is enough to explore Spark functionality.

  1. **Before class** please create a [Databricks Community Edition](https://accounts.cloud.databricks.com/registration.html#signup/community) account.  [This](https://databricks.com/product/getting-started-guide) 3 min video provides a quick overview of Databricks and how to setup up a cluster and notebook.
  2. Databricks makes it easy to create a basic free cluster (6GB of RAM). On the left panel click the *Clusters* icon and then the *Create Cluster* button. Follow the prompts to create a cluster.  In free mode, clusters will become deactivate after 2h of inactivity.
  3. Import our *Spark Tutorial Notebook*.
      1. Open up [this](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/371142130727624/2056133347430741/653376218961520/latest.html) tutorial in a new tab.
      2. Import it into your own Databricks workspace.
  4. Your notebook should open up but is not attached to a cluster.  In the top left,
     where it says *Detached*, click on the menu dropdown and select the cluster
     you created earlier. (If no cluster is there, you can create one from the dropdown).

## 2. Spark and Databricks Tutorial

  We will now go through *spark_tutorial_inclass.ipynb*

  For this section of the tutorial, we will both upload our own csv file to Databricks as well as use common datesets provided by Databricks (a list of which can be [listed like this](https://docs.databricks.com/user-guide/faq/databricks-datasets.html).

  1. Upload mallard.csv dataset from previous tutorials.

      1. If you don't already have a local copy of mallard.csv download it with curl.

          ```
          curl -O https://s3-us-west-2.amazonaws.com/cse599c-sp17/mallard.csv
          ```

      2. On the left panel, click the *Tables* icon to open the Table Explorer.
      3. Click *Create Table*, and select *File* as the data source.
      4. Upload the *mallard.csv* file.
          1. **Important:** once the file is uploaded, a file path such as */FileStore/tables/s3siau3s1492133966611/mallard.csv* will appear under it. Copy this file path into the *mallardFilePath* variable in your notebook.

## 3. Spark ML Example

  The spark ML example will use two datasets already in the */databricks-datasets/* file system.

  To start the ML example, import the [Spark ML Notebook](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/371142130727624/2056133347430889/653376218961520/latest.html) into your Databricks instance.

## 4. Graph processing (GraphX).

  In the graph processing Spark tutorial, we will explore more builten features of Spark (as provided by Databricks). This section uses the same datasets from the ML example.

  To start the GraphX example, import the [Spark GraphX Notebook](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/371142130727624/2056133347430954/653376218961520/latest.html) into your Databricks instance. You can use [GraphFrames documentation](https://graphframes.github.io/api/python/graphframes.html#subpackages) for programming in python and expand this notebook. If you want to just use scala then use this [GraphX documentation](http://spark.apache.org/docs/latest/graphx-programming-guide.html).

## 5. Streaming

  To start the streaming example, import the [Spark Streaming Notebook](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/371142130727624/2056133347430856/653376218961520/latest.html) into your Databricks instance.
