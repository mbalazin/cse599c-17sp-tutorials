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
    T = load("s3://uwdb/sampleData/TwitterK.tsv", csv(schema(src:int, dst:int), skip=0, delimiter="\t"));
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


### select, from, where

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

### join

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
store(Joined, TwoHopsInTwitter);
```

### Aggregation

Aggregation lets us combine results from multiple tuples. This query counts the number of friends for user 821.

```sql
T = scan(TwitterK);
cnt = select COUNT(*) from T where a=821;
store(cnt, user821);
```

```sql
T1 = scan(TwitterK);
cnt = [from T1 where a=821 emit COUNT(*) as x];
store(cnt, user821);
```

We can also group the aggregation by attributes. This query counts the number of friends for *each* user.

```sql
T = scan(TwitterK);
cnt = select a, COUNT(*) from T;
store(cnt, degrees);
```

```sql
T1 = scan(TwitterK);
cnt = [from T1 emit a, COUNT(*) as x];
store(cnt, degrees);
```

Notice that MyriaL's syntax differs from SQL for group by. MyriaL groups by all attributes in the select clause without using a group by clause. For clarity, the equivalent SQL query is:

```sql
select a, COUNT(*) from T group by a;
```


### `unionall` (Concatentation)

`+` or `UNIONALL` concatenates to relations in MyriaL

```sql
T1 = SCAN(TwitterK);
result = T1+T1;
result = UNIONALL(result, T1);
STORE(result, threeTimes);
```

### Set operations

Most operations in MyriaL treat the relation [like a bag rather than a set](https://courses.cs.washington.edu/courses/cse444/10sp/lectures/lecture16.pdf), like SQL. However, MyriaL also has set operations like union, difference, and distinct.

List all unique users.

```sql
Edges = scan(TwitterK);
Left = select a as v from Edges;
Right = select b as v from Edges;
Dups = Left + Right;
Vertices = select distinct v from Dups;
store(Vertices, users);
```

Find the users that only appear as the source of an edge.
```sql
Edges = scan(TwitterK);
Left = select a as v from Edges;
Right = select b as v from Edges;
onlyleft = diff(Left, Right);
store(onlyleft, onlyleft);
```

## Loops

MyriaL supports Do-While loops. The loop can be terminated on a condition about the data, so you can write iterative programs.

Find the vertices reachable from user 821.

```sql
Edge = scan(TwitterK);
-- special syntax for a scalar constant in MyriaL.
Source = [821 AS addr];
Reachable = Source;
Delta = Source;

DO
    -- join to follow the horizon
    NewlyReachable = DISTINCT([FROM Delta, Edge
                              WHERE Delta.addr == Edge.src
                              EMIT Edge.dst AS addr]);
    -- which users are discovered for the first time?
    Delta = DIFF(NewlyReachable, Reachable);
    -- add them to our set of reachable users
    Reachable = UNIONALL(Delta, Reachable);
WHILE [FROM COUNTALL(Delta) AS size EMIT *size > 0];

STORE(Reachable, OUTPUT);
```

The condition should be a relation with one tuple with one boolean attribute.

## Expressions

Expressions are any code that evaluate to scalar values in MyriaL. They can appear in the EMIT (comprehesions) or SELECT (SQL) or WHERE clauses.

### Arithmetic
 MyriaL has a number of math functions.

```sql
    T3 = [FROM SCAN(TwitterK) as t EMIT sin(a)/4 + b AS x];
    STORE(T3, ArithmeticExample);

    --Unicode math operators ≤, ≥, ≠

    T4 = [FROM SCAN(TwitterK) as t WHERE a ≤ b and a ≠ b and b ≥ a EMIT *];
    STORE(T4,  ArithmeticExample2);
```

### Constants

A constant is a *singleton relation* (a relation with a single 1-attribute tuple). You can use the relation as a scalar in an expression by preceding the name with `*` (we saw this in the loop example above).

```sql
N = [12];
T = scan(TwitterK);
S = select a, b from T where a = *N;
store(S, filtered);
```

### User-defined functions

MyriaL supports writing User-defined Functions (UDFs) and User-defined Aggregates (UDAs) in the MyriaL syntax.
*Coming soon: Python UDFs!!*.

User-defined function to calculate modulo.

```sql
def mod(x, n): x - int(x/n)*n;
T1 = [from scan(TwitterK) as t emit mod(a, b)];
STORE(T1, udf_result);
```

User-defined aggregate function to calculate an arg max. We'll use it to find the vertex with the largest degree.

```sql
-- break ties by picking the first value
def pickval(value, arg, _value, _arg):
    case when value >= _value then arg
        else _arg end;

-- Every UDA has three statements: *init* to specify the state attributes and set initial values, *update* run for each tuple, and *output* to calculate the final result.

uda ArgMax(arg, val) {
   -- init
   [0 as _arg, 0 as _val];

   -- update
   [pickval(val, arg, _val, _arg),
    pickval(val, val, _val, _val)];

   -- output
   [_val, _arg];
};

cnt = [from scan(TwitterK) as t emit t.a as v, count(*) as degree];
T1 = [from cnt emit ArgMax(v, degree)];
STORE(T1, max_degree);
```

### Stateful Apply

Stateful apply provides a way to define functions that keep mutable state.

This program assigns a sequential id to each tuple. **Important**: stateful apply is partition-local. That means every partition keeps its own state. The following program produces 0,1,2... for the tuples on every partition.

```sql
APPLY counter() {
  [0 AS c];
  [c + 1];
  c;
};
T1 = SCAN(TwitterK);
T2 = [FROM T1 EMIT a, counter()];
STORE (T2, identified);
```

To do a distributed counter, Myria has coordination operators like broadcast and collect, but these are not currently exposed in MyriaL.

### Types

MyriaL supports a number of types for attributes (and expressions) and performs type checking.

- integer
- long
- float
- double
- string
- datetime
- *coming soon:* blob

## Gotchas

The Myria Catalog is case sensitive, so please make sure to Scan the correct relation name.

## Advanced Examples

* [PageRank in MyriaL](https://github.com/uwescience/raco/blob/master/examples/pagerank.myl)
* [K-Means in MyriaL](https://github.com/uwescience/raco/blob/master/examples/kmeans.myl)
* [Sigma Clipping in MyriaL](https://github.com/uwescience/raco/blob/master/examples/sigma-clipping.myl)
* [Connected Components in MyriaL](https://github.com/uwescience/raco/blob/master/examples/connected_components.myl)
* [Coordinate Matching in MyriaL](https://github.com/uwescience/raco/blob/master/examples/crossmatch_2d.myl)
* [Pairwise Distance Computation](https://github.com/uwescience/raco/blob/master/examples/pairwise_distances.myl)
* [TPC-H in MyriaL](https://github.com/uwescience/tpch-radish)
