# Data Warehouse

This is the solution to the project **Data Warehouse** of Udacity's [Data Engineering Nanodegree](https://www.udacity.com/course/data-engineer-nanodegree--nd027).

## Introduction

The purpose of this project is to build an ETL pipeline to extract data from an S3 bucket, stage them in Redshift and transform the data into a set of dimensional tables in order to provide fast queries to analyze song play data from the startup Sparkify.

## Resources

* `create_cluster.py` is a script to create a Redshift cluster (and all everything else necessary) using the provided credentials in the `dwh.cfg` file.
* `delete_cluster.py` is a script to delete the Redshift cluster and remove the role created to access S3 buckets.
* `create_table.py` is a script to (re)create the staging tables and the fact and dimension tables for the star schema in Redshift.
* `etl.py` loads data from S3 into the staging tables on Redshift and then processes that data into the analytics tables.
* `sql_queries.py` is used to define the SQL statements which will be imported into the two other files above.
* `benchmark.py` is a script to run a few queries and analyze their performance.
* The `dwh.cfg` file should have the following structure and its values must be filled in.

```ini
[AWS]
KEY=
SECRET=

[CLUSTER] 
CLUSTER_TYPE=multi-node
NUM_NODES=4
NODE_TYPE=dc2.large

IAM_ROLE_NAME=
CLUSTER_IDENTIFIER=
HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=

[IAM_ROLE]
ARN=

[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'
```

## Executing ETL process

The first step is to either lauch a Redshift cluster and create a IAM role via the console or use the provided `create_cluster.py` script. When the cluster is ready, grab the cluster endpoint and IAM Role ARN and edit the `dwh.cfg` so that the future scripts can connect to the database.

The second step is to run `create_table.py`, which will delete the sparkify-related tables and recreate them.

The third step is to run `etl.py` to import data from the S3 bucket provided in the `dwh.cfg` file (log and song data) into two staging tables (`stg_events` and `stg_songs`), which have the same schemas of the .json files in the bucket. Then, after both staging tables are filled, they can be used to insert data into the analytical tables (`songplays`, `users`, `songs`, `artists` and `time`). These tables form a star schema and their `primary key`s are also `sortkey`s. There is a `distkey` in the column `songplay_id` to distribute the data into partitions and enhance the performance of future queries.

After all those steps, the database will be ready to be queried. An optional final step is to delete the cluster and remove the IAM role created using the `delete_cluster.py` script.

## Benchmark

The script `benchmark.py` can be used to connect to the Redshift cluster and execute a few queries in order to measure performance. The queries listed are the following:

### Most popular weekday on Sparkify

```sql
-- top_weekday_query
select count(sp.songplay_id) as song_count, t.weekday
from songplays sp
join time t on sp.start_time = t.start_time
group by t.weekday
order by 1 desc
```

### Evolution of the app usage during the day

```sql
-- app_usage_query
select count(sp.songplay_id) as song_count, t.hour
from songplays sp
join time t on sp.start_time = t.start_time
group by t.hour
order by t.hour
```

### Top listened songs all time

```sql
-- top_songs_query
select count(*) song_count, s.title, a."name"
from songplays sp
join songs s on sp.song_id = s.song_id
join artists a on sp.artist_id = a.artist_id
group by s.title, a."name"
order by 1 desc
```

### Locations the app is most used on

```sql
-- top_locations_query
select count(*), "location"
from songplays sp
group by "location"
order by 1 desc
```

Running the script with a cluster of 4 nodes of dc2.large machines resulted in the following results:

* `top_weekday_query`: 0.655 seconds
* `app_usage_query`: 4.928 seconds
* `top_songs_query`: 10.884 seconds
* `top_locations_query`: 4.202 seconds