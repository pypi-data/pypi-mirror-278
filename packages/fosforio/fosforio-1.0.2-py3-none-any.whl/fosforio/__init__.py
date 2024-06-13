import os

# initialising constants, initialing before other import statements to resolve circular import issue.
connection_manager = os.getenv("CONNECTION_MANAGER_BASE_URL", "http://fdc-project-manager:80/project-manager")
print(f"Connection manager service url initialised to {connection_manager}\n"
      f"If you need to update its value then update the variable CONNECTION_MANAGER_BASE_URL in os env.")

# importing class and methods
from .fosforio import get_dataframe, get_local_dataframe
from .snowflake import Snowflake
from .mysql import Mysql
from .hive import Hive
from .sftp import Sftp
from .amazons3 import AmazonS3
from .azure import Azure
from .sqlserver import Sqlserver
from .postgres import Postgres
from .feature_store import FeastFeatureStore

# initialising class objects
snowflake = Snowflake()
mysql = Mysql()
hive = Hive()
sftp = Sftp()
s3 = AmazonS3()
azure = Azure()
sqlserver = Sqlserver()
postgres = Postgres()

fs = FeastFeatureStore()
