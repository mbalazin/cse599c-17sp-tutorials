## How to generate data


1. Schema of the database is defined in schema.txt

2. Some sample queries are listed in queries.txt. Some query parameters needs to be changed, for instance, the created\_at

3. To generate data, run:
```
./dbgen.sh
```
parameters defining how large the data set is listed in dbgen.sh. All generated data files are in csv format.

4. The data is kind of a fake dataset for website http://lobste.rs
