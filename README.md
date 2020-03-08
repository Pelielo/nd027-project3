# Data Warehouse

This is the solution to the project **Data Warehouse** of Udacity's [Data Engineering Nanodegree](https://www.udacity.com/course/data-engineer-nanodegree--nd027).

## Introduction

The purpose of this project is to build an ETL pipeline to extract data from an S3 bucket, stage them in Redshift and transform the data into a set of dimensional tables in order to provide fast queries to analyze song play data from the startup Sparkify.

## Resources


* `create_table.py` is a script to create the fact and dimension tables for the star schema in Redshift.
* `etl.py` loads data from S3 into staging tables on Redshift and then processes that data into the analytics tables on Redshift.
* `sql_queries.py` is used to define the SQL statements which will be imported into the two other files above.


## Executing ETL process

