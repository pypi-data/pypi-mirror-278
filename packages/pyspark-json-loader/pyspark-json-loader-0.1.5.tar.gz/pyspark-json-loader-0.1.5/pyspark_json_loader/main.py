import json
import uuid

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when


def start_spark_session():
    spark = SparkSession.builder.appName("PostgreSQL Connection with PySpark").config("spark.jars",
                                                                                      "postgresql-42.7.2.jar").getOrCreate()
    return spark


def connect_to_db(spark, host_name, port_number, db_name, user, password, query, null_value=0):
    df = spark.read.format("jdbc") \
        .option("url", f"jdbc:postgresql://{host_name}:{port_number}/{db_name}") \
        .option("user", user) \
        .option("password", password) \
        .option("driver", "org.postgresql.Driver") \
        .option("query", query) \
        .option("nullValue", null_value) \
        .load()
    return df


def load_json_file(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data


def preprocess_dataframe(df, json_data):
    for column in df.columns:
        if column in json_data:
            df = df.withColumn(column, when(col(column).isNull(), 0).otherwise(col(column)))
    df = df.na.fill(0)
    return df


def convert_to_pandas(grouped_metrics_df):
    pf = grouped_metrics_df.toPandas()
    pf = pf.fillna(0)
    pf["DateTime"] = pf["DateTime"].astype(str)
    pf['Id'] = [uuid.uuid4().hex for _ in range(len(pf.index))]
    return pf

