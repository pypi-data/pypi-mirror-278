import json
import uuid

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit


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


def split_and_convert(vector_string):
    if vector_string is None:
        return []  # Return an empty list if vector_string is None
    if vector_string == "0":
        return [0]
    else:
        result = []
        for x in vector_string.split(":"):
            if x.strip():  # Skip empty strings
                try:
                    result.append(int(x))
                except ValueError:
                    # Handle non-integer values gracefully
                    print(f"Warning: Non-integer value '{x}' encountered, skipping conversion.")
            else:
                result.append(0)  # Assign zero to x when encountering an empty string
        return result


def add_lists(row):
    max_len = max(len(sublist) for sublist in row)
    result = []
    for i in range(max_len):
        sum_at_index = sum(sublist[i] if i < len(sublist) else 0 for sublist in row)
        result.append(sum_at_index)
    return result


def increment_index(row):
    return list(range(1, len(row) + 1))


def index(row):
    return list(range(0, len(row)))


def multiply_lists(row1, row2):
    return [x * y * 2 for x, y in zip(row1, row2)]


def multiplyP_lists(row1, row2):
    return [x * y for x, y in zip(row1, row2)]


def sum_list(row):
    return sum(row)


def list_to_colon_separated_string(lst):
    return ":".join(str(x) for x in lst)


def calculate_availability(df, file_count_col, downtime_col, period_hours, total_periods, comments_threshold):
    # Calculate availability
    df = df.withColumn(
        "Availability",
        lit(100) * (lit(15) * lit(60) * col(file_count_col) - col(downtime_col)) / (
                    lit(3600) * lit(period_hours) * lit(total_periods))
    )

    # Add availability comments
    df = df.withColumn(
        "Availability_Comments",
        when(col(file_count_col) < comments_threshold, "Suspected Down Site").otherwise("")
    )

    return df
