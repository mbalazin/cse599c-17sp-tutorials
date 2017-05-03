## 1. Ingesting data
Myria can read and store a CSV file from S3 via the `load` command:

### 1.1. Loading and storing "TwitterK" dataset

```sql
    T = load("s3://uwdb/sampleData/TwitterK.csv", csv(schema(src:int, dst:int), skip=0));
    store(T, TwitterK, [src, dst]);
```

The `skip` option takes the number of lines at the beginning of the CSV file to skip over (such as column headers).
Here, Myria will create a relation `T1` with the contents of `TwitterK.csv` and store it in a table called `TwitterK`. The third argument, `[src, dst]`, is a list of attributes to partition the rows by.

Note that the `load` command can also handle TSV data:

```sql
    T = load("path/to/your/file.tsv", csv(schema(src:int, dst:int), skip=0, delimiter="\t"));
    store(T, TwitterK, [src, dst]);
```

### 1.2. Loading and storing "Points" dataset

```sql
    T = load("s3://uwdb/sampleData/sampleCrossmatch/points.txt",
              csv(schema(id:int,
                         x:float,
                         y:float,
                         z:float), skip=0));
        store(T, points, [x,y,z]);
```

### 1.3. Loading data from other sources (optional)
You can also load data from other sources including your own local file system. To ingest from a local file source, you must deploy a local instance of Myria. Below is an example of loading a smallTable from a local file.

```sql
    T = load("file:///path/to/smallTable/file",
              csv(schema(x:float,
                         y:float), skip=0));
    store(T, points, [x,y]);
```

If your table is in HDFS, you can also run something like the following:

```sql
    T = load("hdfs://server:port/path/to/file",
              csv(schema(x:float,
                         y:float), skip=0));
    store(T, points, [x,y]);
```

### 1.4. Reading existing relations

Once a relation is stored, Myria can access use it in later queries with `scan`. This example simply repartitions the `TwitterK` relation by just attribute `src`.

```sql
    T = scan(TwitterK);
    store(T, TwitterK_Src, [src]);
```

### 1.5. Create an empty relation

```sql
--Create an empty relation with a particular schema
r = empty(x:int, y:float, z:string);
store(r, myrelation);
```

### 1.6. Compute the result without storing it

MyriaL has fairly aggressive *deadcode elimination*. That means if you do not store a relation, Myria may not bother computing anything.

This program, for example,

```sql
T = scan(TwitterK);
```

results in the following error message:

`MyrialCompileException: Optimized program is empty`


MyriaL provides the `sink` command to get around this. We often find `sink` useful when benchmarking Myria's performance. The following program scans `TwitterK` from disk into memory and then throws the relation away.

```sql
T = scan(TwitterK);
sink(T);
```

## 2. Transforming Data

Now for some real queries! MyriaL has two styles of syntax: **SQL** and **comprehensions**. If you've used [list comprehensions in python](https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions) then MyriaL's comprehensions will look familiar. Use the style you prefer or mix and match.

You can try all the examples in this section yourself by copy/pasting them into your allotted demo cluster. 


### 2.1. select, from, where

Let's find the twitter relationships where the follower and followee are the same user.

```sql
T = scan(TwitterK);
-- SQL style syntax
s = select * from T where src = dst;
store(s, selfloops);
```

```sql
T = scan(TwitterK);
-- comprehension syntax
s = [from T where src = dst emit *];
store(s, selfloops);
```

`from T` means read tuples from relation T. `where src = dst` means only keep tuples where the value of `src` is equal to the value of `dst`. The `*` in `emit *` means the resulting relation should contain *all* the attributes from the relations in the `from` clause (in this case, the attributes of `T`: `src` and `dst`).

### 2.2. join

Joins let us match two relations on 1 or more attributes. This query finds all the friend-of-friend relationships in TwitterK.

```sql
T1 = scan(TwitterK);
T2 = scan(TwitterK);
joined = select T1.src as src, T1.dst as link, T2.dst as dst
         from T1, T2
         where T1.dst = T2.src;
store(joined, TwoHopsInTwitter);
```

```sql
T1 = scan(TwitterK);
T2 = scan(TwitterK);
joined = [from T1, T2
          where T1.dst = T2.src
          emit T1.src AS src, T1.dst AS link, T2.dst AS dst];     
store(joined, TwoHopsInTwitter);
```

### 2.3. aggregation

Aggregation lets us combine results from multiple tuples. This query counts the number of friends for user 821.

```sql
T = scan(TwitterK);
cnt = select count(*) from T where src=821;
store(cnt, user821);
```

```sql
T1 = scan(TwitterK);
cnt = [from T1 where src=821 emit count(*) as x];
store(cnt, user821);
```

### 2.4. group-by aggregates
We can also group the aggregation by attributes. This query counts the number of friends for *each* user.

```sql
T = scan(TwitterK);
T1 = select src as user, count(*) as degree from T;
store(T1, user_degrees);
```

```sql
T = scan(TwitterK);
T1 = [from T emit src as user, count(*) as degree];
store(T1, user_degrees);
```

Notice that MyriaL's syntax differs from SQL for group by. MyriaL groups by all attributes in the select clause without using a group by clause. For clarity, the equivalent SQL query is:

```sql
select src as user, count(*) as degree from T group by src;
```


### 2.4. unionall
`+` or `unionall` concatenates two relations in MyriaL using the bag semantics.

```sql
T1 = scan(TwitterK);
result = T1+T1;
result = unionall(result, T1);
store(result, threeTimes);
```

## 3. Set operations

Most operations in MyriaL treat the relation [like a bag rather than a set](https://courses.cs.washington.edu/courses/cse444/10sp/lectures/lecture16.pdf), like SQL. However, MyriaL also has set operators: `diff`, and `distinct`. `intersect` and `union` are not implemented yet. 

### 3.1. List all unique users

```sql
edges = scan(TwitterK);
left = select src as vertex from edges;
right = select dst as vertex from edges;
dups = left + right; 
vertices = select distinct vertex from dups;
store(vertices, users);
```
Note the query plan created by MyriaX for the above query! It computes `left` and `right` in parallel.

### 3.2. Find the users that only appear as the source of an edge
```sql
edges = scan(TwitterK);
left = select src as vertex from edges;
right = select dst as vertex from edges;
onlyleft = diff(left, right);
store(onlyleft, onlyAsSource);
```
Also, notice how the query plans for the union, distinct operation is different from that of just diff!


## 4. User-defined functions

MyriaL allows users to define two kinds of functions: UDF and UDA. A *user-defined function (UDF)* takes one or more parameters to produce an output. The function `foo` below is a UDF and it can be directly invoked in any of the expressions.

```sql
def foo(a, b): a - int(a/(b+1))*b;
T1 = [from scan(TwitterK) as t emit foo(src, dst)];
store(T1, udf_result);
```
A *user-defined aggregate function*, which is sometimes called an UDAF or UDA takes in a series of inputs and produces a single output for the series. The syntax for defining a UDA is as follows:
```
uda func-name(args) {
 initialization-expr(s);
 update-expr(s);
 result-expr(s);
};
```
User-defined aggregate function to calculate an arg max. We'll use it to find the vertex with the largest degree.

```sql
-- break ties by picking the first value
def pickBasedOnValue(value1, arg1, value2, arg2):
    case
    	when value1 >= value2
    	then arg1
    	else arg2
    end;

-- User defined aggregate that finds the argmax and max
uda argMaxAndMax(arg, val) {
   -- init
   [-1 as _arg, -1 as _val];

   -- update
   [pickBasedOnValue(val, arg, _val, _arg),
    pickBasedOnValue(val, val, _val, _val)];

   -- output
   [_arg, _val];
};

T = scan(TwitterK);
degrees = select dst as vertex, count(*) as followers
		  from T;
most_followed_follower = select T.dst, argMaxAndMax(D.followers, D.vertex)
						 from T, degrees as D
                         where T.src = D.vertex;
store(most_followed_follower, MostFollowedFollower);
```

### 5. Stateful Apply

General SQL syntax only allows pure functions in expression. Even UDFs described above does not allow you to do more complicated map functions such as those that require an internal state. 

A very good example is to assign session ids to clickstreams based on the interval between two clicks. You need to record the last time a click was received in order to decide whether to assign the next session id or the same session id to a clickstream. 

The following program assigns a sequential id to each tuple. **Important**: stateful apply is partition-local. That means every partition keeps its own state. The following program produces 0,1,2... for the tuples on every partition.

```sql
apply counter() {
  [0 AS c];
  [c + 1];
  c;
};
T1 = scan(TwitterK);
T2 = [from T1 emit a, counter()];
store(T2, identified);
```

To do a distributed counter, Myria has coordination operators like broadcast and collect, but these are not currently exposed in MyriaL.

## 6. Synchronous iterations

MyriaL supports `do...while` loops. The loop condition must be an expression that evaluates to a singleton relation with one boolean attribute ie. either `[true]` or `[false]`. Here are a few examples:

### 6.1. Reachability test
In this example, we will find the set of nodes that are reachable from a given node in the Twitter dataset. Note that there is a special syntax for a scalar constant in MyriaL. 

```sql
edges = scan(TwitterK);
-- special syntax for scalar constants
source = [2 AS addr];
reachable = source;
do
    before_size = select count(*) as B
                  from reachable;
    new_reachable = select edges.dst as addr
    			from reachable, edges
             	where reachable.addr = edges.src;
    reachable = new_reachable + reachable;
    reachable = select distinct addr
    			from reachable;
    after_size = select count(*) as A
    		 from reachable;
while [from before_size, after_size emit A - B > 0];
store(reachable, Reachable);
```

### 6.2. Connected components
Here is another example of a `do...while` loop used to find the connected components in the Twitter dataset.

```sql
edges = scan(TwitterK);
con_comp = select src as nid, src as cid
	   from edges;
do
  before_size = select count(*) as B
  		from con_comp;
  new_con_comp = select edges.dst as nid, con_comp.cid as cid
		 from edges, con_comp
                 where edges.src = con_comp.nid;
  new_con_comp = new_con_comp + con_comp;
  new_con_comp = select nid, min(cid) as cid
  		 from new_con_comp;
  con_comp = new_con_comp;
  after_size = select count(*) as A
	       from con_comp;
while [from before_size, after_size emit A - B > 0];
comp_count = [from con_comp emit cid as id, count(*) as cnt];
store(comp_count, TwitterCC);
```

## 7. Asynchronous iterations

The following code computes the connected components in the twitter dataset using asynchronous mode of computation. The algorithm runs until convergence. 

```sql
E = load("s3://uwdb/sampleData/TwitterK.csv", csv(schema(src:int, dst:int)));
V = [from E emit src as x] + [from E emit dst as x];
V = select distinct x from V;
do
  CC = [nid, MIN(cid) as cid] <-
    [from V emit V.x as nid, V.x as cid] +
    [from E, CC where E.src = CC.nid emit E.dst as nid, CC.cid];
until convergence async pull_idb;
store(CC, CC_output);
```

## 8. Advanced Examples

* [PageRank in MyriaL](https://github.com/uwescience/raco/blob/master/examples/pagerank.myl)
* [K-Means in MyriaL](https://github.com/uwescience/raco/blob/master/examples/kmeans.myl)
* [Sigma Clipping in MyriaL](https://github.com/uwescience/raco/blob/master/examples/sigma-clipping.myl)
* [Connected Components in MyriaL](https://github.com/uwescience/raco/blob/master/examples/connected_components.myl)
* [Coordinate Matching in MyriaL](https://github.com/uwescience/raco/blob/master/examples/crossmatch_2d.myl)
* [Pairwise Distance Computation](https://github.com/uwescience/raco/blob/master/examples/pairwise_distances.myl)
* [TPC-H in MyriaL](https://github.com/uwescience/tpch-radish)
