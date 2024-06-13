# Installation:
## Without any dependencies:
```commandline
pip install fosforio
```
## With all dependencies:
```commandline
pip install fosforio[all]
```
## With snowflake:
```commandline
pip install fosforio[snowflake]
```
## With s3:
```commandline
pip install fosforio[s3]
```
## With azureblob:
```commandline
pip install fosforio[azureblob]
```
## With local:
```commandline
pip install fosforio[local]
```
## With sftp:
```commandline
pip install fosforio[sftp]
```
## With mysql:
```commandline
pip install fosforio[mysql]
```
## With hive:
```commandline
pip install fosforio[hive]
```
## With sqlserver:
```commandline
pip install fosforio[sqlserver]
```
## With postgres:
```commandline
pip install fosforio[postgres]
```

#### Source code is available at: https://gitlab.fosfor.com/fosfor-decision-cloud/intelligence/refract-sdk 

# Usage:
## To read dataframe with dataset name only -
```python
from fosforio import get_dataframe
get_dataframe("dataset_name")

# To read top 3 records from dataframe with filter condition of col1=value1 and col2>value2 and sort by col1.
get_dataframe("dataset_name", row_count=3, filter_condition="where col1='value1' and col2>value2 order by col1")

# For reading data from any other connections not listed here, please pip install mosaic-connector-python package.
```
## To read dataframe with filename from local storage -
```python
from refracio import get_local_dataframe
get_local_dataframe("local_file_name_with_absolute_path", row_count=3)
```
## To use snowflake related operations -
```python
from fosforio import snowflake

# To get snowflake connection object with a default snowflake connection created by the user, if available.
snowflake.get_connection()

# To get snowflake connection object with a specific connection name
snowflake.get_connection(connection_name="snowflake_con_name")

# To read a specific dataset published from a snowflake connection
snowflake.get_dataframe("dataset_name")

# To read a specific dataset published from a snowflake connection with only top few records.
snowflake.get_dataframe("dataset_name", row_count=3)

# To read a specific dataset published from a snowflake connection with only top few records and filter conditions.
snowflake.get_dataframe("dataset_name", row_count=3, filter_condition="where col1='value1' and col2>value2 order by col1")

# To execute a user specific query in snowflake, with the specified connection name.
snowflake.execute_query(query="user_query", database="db_name", schema="schema", connection_name="connection_name")

# To execute a user specific query in snowflake, with the current connection object or with the default connection for the user.
snowflake.execute_query(query="user_query", database="db_name", schema="schema")

# To close snowflake connection, please do close the connection after use!
snowflake.close_connection()
```

## To use mysql related operations -
```python
from fosforio import mysql

# To get mysql connection object with a default mysql connection created by the user, if available.
mysql.get_connection()

# To get mysql connection object with a specific connection name
mysql.get_connection(connection_name="mysql_con_name")

# To read a specific dataset published from a mysql connection
mysql.get_dataframe("dataset_name")

# To read a specific dataset published from a mysql connection with only top few records.
mysql.get_dataframe("dataset_name", row_count=3)

# To read a specific dataset published from a mysql connection with only top few records and filter conditions.
mysql.get_dataframe("dataset_name", row_count=3, filter_condition="where col1='value1' and col2>value2 order by col1")

# To execute a user specific query in mysql, with the specified connection name.
mysql.execute_query(query="user_query", connection_name="connection_name")

# To execute a user specific query in mysql, with the current connection object or with the default connection for the user.
mysql.execute_query(query="user_query")

# To close mysql connection, please do close the connection after use!
mysql.close_connection()
```

## To use sqlserver related operations -
### Requires sqlserver driver library
```python
# Create a custom template with the following commands added in "Pre Init Script" section,
# sudo curl -o /etc/yum.repos.d/mssql-release.repo https://packages.microsoft.com/config/rhel/9.0/prod.repo
# sudo ACCEPT_EULA=Y yum install -y msodbcsql18
from fosforio import sqlserver

# To get sqlserver connection object with a default sqlserver connection created by the user, if available.
sqlserver.get_connection()

# To get sqlserver connection object with a specific connection name
sqlserver.get_connection(connection_name="sqlserver_con_name")

# To read a specific dataset published from a sqlserver connection
sqlserver.get_dataframe("dataset_name")

# To read a specific dataset published from a sqlserver connection with only top few records.
sqlserver.get_dataframe("dataset_name", row_count=3)

# To read a specific dataset published from a sqlserver connection with only top few records and filter conditions.
sqlserver.get_dataframe("dataset_name", row_count=3, filter_condition="where col1='value1' and col2>value2 order by col1")

# To execute a user specific query in sqlserver, with the specified connection name.
sqlserver.execute_query(query="user_query", database="db_name", connection_name="connection_name")

# To execute a user specific query in sqlserver, with the current connection object or with the default connection for the user.
sqlserver.execute_query(query="user_query", database="db_name")

# To close sqlserver connection, please do close the connection after use!
sqlserver.close_connection()
```

## To use hive related operations -
```python
from fosforio import hive

# To get hive connection object with a default hive connection created by the user, if available. User id is required (1001 is default user_id used).
hive.get_connection(user_id=1001)

# To get hive connection object with a specific connection name, User id is required (1001 is default user_id used).
hive.get_connection(connection_name="hive_con_name", user_id=1001)

# To read a specific dataset published from a hive connection. User id is required (1001 is default user_id used).
hive.get_dataframe("dataset_name", user_id="1001")

# To read a specific dataset published from a hive connection with only top few records. User id is required (1001 is default user_id used)
hive.get_dataframe("dataset_name", user_id="1001", row_count=3)

# To read a specific dataset published from a hive connection with only top few records and filter conditions. User id is required (1001 is default user_id used)
hive.get_dataframe("dataset_name", user_id="1001", row_count=3, filter_condition="where col1='value1' and col2>value2 order by col1")

# To execute a user specific query in hive, with the specified connection name. User id is required (1001 is default user_id used).
hive.execute_query(query="user_query", connection_name="connection_name", user_id="1001")

# To execute a user specific query in hive, with the current connection object or with the default connection for the user. User id is required (1001 is default user_id used).
hive.execute_query(query="user_query", user_id="1001")

# To close hive connection, please do close the connection after use!
hive.close_connection()
```

## To use postgres related operations -
```python
from fosforio import postgres

# To get postgres connection object with a default postgres connection created by the user, if available.
postgres.get_connection()

# To get postgres connection object with a specific connection name
postgres.get_connection(connection_name="mysql_con_name")

# To read a specific dataset published from a postgres connection
postgres.get_dataframe("dataset_name")

# To read a specific dataset published from a postgres connection with only top few records.
postgres.get_dataframe("dataset_name", row_count=3)

# To read a specific dataset published from a postgres connection with only top few records and filter conditions.
postgres.get_dataframe("dataset_name", row_count=3, filter_condition="where col1='value1' and col2>value2 order by col1")

# To execute a user specific query in postgres, with the specified connection name.
postgres.execute_query(query="user_query", connection_name="connection_name")

# To execute a user specific query in postgres, with the current connection object or with the default connection for the user.
postgres.execute_query(query="user_query")

# To close postgres connection, please do close the connection after use!
postgres.close_connection()
```

## To use sftp related operations -
```python
from fosforio import sftp

# To get sftp connection object with a default sftp connection created by the user, if available.
sftp.get_connection()

# To get sftp connection object with a specific connection name
sftp.get_connection(connection_name="sftp_con_name")

# To read a specific dataset published from a sftp connection
sftp.get_dataframe("dataset_name")

# To read a specific dataset published from a sftp connection with only top few records.
sftp.get_dataframe("dataset_name", row_count=3)

# Use sftp connection object c to do any operation related to sftp like (get, put, listdir etc)
c = sftp.get_connection()

# To close sftp connection, please do close the connection after use!
sftp.close_connection()
```

## To use amazon S3 related operations -
```python
from fosforio import s3

# To get s3 connection object with a default s3 connection created by the user, if available.
s3.get_connection()

# To get s3 connection object with a specific connection name
s3.get_connection(connection_name="s3_con_name")

# To read a specific dataset published from a s3 connection
s3.get_dataframe("dataset_name")

# To read a specific dataset published from a s3 connection with only top few records.
s3.get_dataframe("dataset_name", row_count=3)

# Use s3 connection object c to do any operation related to s3.
c = s3.get_connection()
```

## To use azure blob related operations -
```python
from fosforio import azure

# To get azure blob connection object with a default azure connection created by the user, if available.
azure.get_connection()

# To get azure blob connection object with a specific connection name
azure.get_connection(connection_name="azureblob_con_name")

# To read a specific dataset published from a azureblob connection
azure.get_dataframe("dataset_name")

# To read a specific dataset published from a azure connection with only top few records.
azure.get_dataframe("dataset_name", row_count=3)

# Use azure connection object c to do any operation related to azure.
c = azure.get_connection()
```

*Note: Currently supported native connectors - snowflake, mysql, hive, sqlserver, postgres, sftp, s3, azureblob, local(NAS)*
