# PySpark JSON Loader

## Overview

`pyspark-json-loader` is a Python package designed to facilitate loading and preprocessing JSON data using PySpark. It provides functions to start a Spark session, connect to a PostgreSQL database, preprocess data, and convert Spark DataFrames to Pandas DataFrames.

## Installation

To install the package, run:

```bash
pip install pyspark-json-loader
```

## Usage

Here is a detailed guide on how to use the functions provided by the `pyspark-json-loader` package.

### Importing the Module

To use the functions in this package, you need to import them as follows:

```bash
from pyspark_json_loader import (
    load_json_file,
    start_spark_session,
    connect_to_db,
    preprocess_dataframe,
    convert_to_pandas,
    split_and_convert,
    add_lists,
    increment_index,
    index,
    multiply_lists,
    multiplyP_lists,
    sum_list,
    list_to_colon_separated_string
)
```

### Functions

#### 1. `load_json_file(file_name)`

Description: This function loads a JSON file and returns its contents as a Python dictionary.

Parameters:
- file_name (str): The path to the JSON file.

Returns:
- dict: The contents of the JSON file.

Example:

```bash
json_data = load_json_file('data.json')
print(json_data)
```

Output:
```bash
{
    "column1": "value1",
    "column2": "value2"
}
```

#### 2. `start_spark_session()`

Description: This function starts a Spark session with the specified JAR file.

Returns:
- SparkSession: The Spark session object.

Example:
```bash
spark = start_spark_session()
print(spark)
```
Output:
```bash
<pyspark.sql.session.SparkSession object at 0x...>
```

#### 3. `connect_to_db(spark, host_name, port_number, db_name, user, password, query, null_value=0)`

Description: This function connects to a PostgreSQL database using the provided connection details and query.

Parameters:
- spark (SparkSession): The Spark session object.
- host_name (str): The hostname of the PostgreSQL server.
- port_number (int): The port number of the PostgreSQL server.
- db_name (str): The name of the database.
- user (str): The username for the database.
- password (str): The password for the database.
- query (str): The SQL query to execute.
- null_value (int, optional): The value to use for null values. Default is 0.

Returns:
- DataFrame: The resulting DataFrame from the query.

Example:
```bash
df = connect_to_db(spark, 'localhost', 5432, 'mydatabase', 'user', 'password', 'SELECT * FROM mytable')
df.show()
```

Output:
```bash
| id | name |
|----|------|
| 1  | John |
| 2  | Jane |
```

#### 4. `preprocess_dataframe(df, json_data)`

Description: This function preprocesses a DataFrame by filling null values based on the provided JSON data.

Parameters:
- df (DataFrame): The Spark DataFrame to preprocess.
- json_data (dict): The JSON data to use for preprocessing.

Returns:
- DataFrame: The preprocessed DataFrame.

Example:
```bash
preprocessed_df = preprocess_dataframe(df, json_data)
preprocessed_df.show()
```

Output:
```bash
+---+------+
| id|  name|
+---+------+
|  1|  John|
|  2|  Jane|
+---+------+
```

#### 5. `convert_to_pandas(grouped_metrics_df)`

Description: This function converts a Spark DataFrame to a Pandas DataFrame and adds a UUID column.

Parameters:
- grouped_metrics_df (DataFrame): The Spark DataFrame to convert.

Returns:
- DataFrame: The resulting Pandas DataFrame.

Example:
```bash
pandas_df = convert_to_pandas(preprocessed_df)
print(pandas_df)
```

Output:
```bash
   id   name                               Id
0   1   John  0a539f3c... (UUID)
1   2   Jane  1d2e4f5a... (UUID)
```

#### 6. `split_and_convert(vector_string)`

Description: This function splits a colon-separated string and converts each part to an integer, handling edge cases.

Parameters:
- vector_string (str): The colon-separated string to split and convert.

Returns:
- list: The list of integers.

Example:
```bash
result = split_and_convert("1:2:3")
print(result)
```

Output:
```bash
[1, 2, 3]
```

#### 7. `add_lists(row)`

Description: This function adds corresponding elements of lists contained in a row, handling different lengths.

Parameters:
- row (list of lists): The lists to add.

Returns:
- list: The resulting list after addition.

Example:
```bash
result = add_lists([[1, 2, 3], [4, 5, 6]])
print(result)
```

Output:
```bash
[5, 7, 9]
```

#### 8. `increment_index(row)`

Description: This function creates a list of incremental integers starting from 1, with the same length as the input list.

Parameters:
- row (list): The input list.

Returns:
- list: The list of incremental integers.

Example:
```bash
result = increment_index([10, 20, 30])
print(result)
```

Output:
```bash
[1, 2, 3]
```

#### 9. `index(row)`

Description: This function creates a list of incremental integers starting from 0, with the same length as the input list.

Parameters:
- row (list): The input list.

Returns:
- list: The list of incremental integers.

Example:
```bash
result = index([10, 20, 30])
print(result)
```

Output:
```bash
[0, 1, 2]
```

#### 10. `multiply_lists(row1, row2)`

Description: This function multiplies corresponding elements of two lists and doubles the result.

Parameters:
- row1 (list): The first list of numbers. 
- row2 (list): The second list of numbers.

Returns:
- list: The list of multiplied and doubled results.

Example:
```bash
result = multiply_lists([1, 2, 3], [4, 5, 6])
print(result)
```

Output:
```bash
[8, 20, 36]
```

#### 11. `multiplyP_lists(row1, row2)`

Description: This function multiplies corresponding elements of two lists.

Parameters:
- row1 (list): The first list of numbers.
- row2 (list): The second list of numbers.

Returns:
- list: The list of multiplied results.

Example:
```bash
result = multiplyP_lists([1, 2, 3], [4, 5, 6])
print(result)
```

Output:
```bash
[4, 10, 18]
```

#### 12. `sum_list(row)`

Description: This function calculates the sum of elements in a list.

Parameters:
- row (list): The input list.

Returns:
- int: The sum of the list elements.

Example:
```bash
result = sum_list([1, 2, 3])
print(result)
```

Output:
```bash
6
```

#### 13. `list_to_colon_separated_string(lst)`

Description: This function converts a list of numbers to a colon-separated string.

Parameters:
- lst (list): The list of numbers.

Returns:
- str: The colon-separated string.

Example:
```bash
result = list_to_colon_separated_string([1, 2, 3])
print(result)
```

Output:
```bash
"1:2:3"
```