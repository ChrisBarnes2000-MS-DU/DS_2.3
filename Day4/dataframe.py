import sqlite3 as lite
import sqlite3
import pandas as pd
import boto3

bucket = "makeschool-data"
file_name = "data/Churn_Modelling.csv"

s3 = boto3.client('s3')
# 's3' is a key word. create connection to S3 using default config and all buckets within S3

obj = s3.get_object(Bucket=bucket, Key=file_name)
# get object and file (key) from bucket

df = pd.read_csv(obj['Body'])  # 'Body' is a key word
print(df.head())


# Write a SQL syntax in Python that return all records where population field is greater or equal than 50Mfrom Population table in population database
# A great resource to self-earn SQL: https://www.w3schools.com/sql/default.asp

con = lite.connect('population-2.db')

with con:
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE Population(id INTEGER PRIMARY KEY, country TEXT, population INT)")
    cur.execute("INSERT INTO Population VALUES(NULL,'Germany',81197537)")
    cur.execute("INSERT INTO Population VALUES(NULL,'France', 66415161)")
    cur.execute("INSERT INTO Population VALUES(NULL,'Spain', 46439864)")
    cur.execute("INSERT INTO Population VALUES(NULL,'Italy', 60795612)")
    cur.execute("INSERT INTO Population VALUES(NULL,'Spain', 46439864)")

conn = sqlite3.connect('population.db')
# query = "SELECT country FROM Population WHERE population > 50000000;"
query = "SELECT country FROM Population WHERE country LIKE 's%';"

df = pd.read_sql_query(query, conn)

for country in df['country']:
    print(country)



# Q1) what is the name of table in NoSQL domain?
# Collection

# Q2) what is the name of record in NoSQL domain?
# Document

# Q3) what is the data type structure for a document in NoSQL?
# Record


# https://www.kidscodecs.com/database-design/
