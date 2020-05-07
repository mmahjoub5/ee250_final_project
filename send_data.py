#this program will read in data from the accelrometer 
#and send it to the influxdb server which is running on the 
#aws EC2 instance using influxdb API



from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "Abj-wu1yWUh_ikwiQMDBA8Z0X_-wJfHeuk3LxS9Tgl70hJzPMfeSSjVJYDTcN1HK9wH3EMgXMumMRjNvDgw6Ew=="
org = "7256ca2ad5deacce"
bucket = "Abj-wu1yWUh_ikwiQMDBA8Z0X_-wJfHeuk3LxS9Tgl70hJzPMfeSSjVJYDTcN1HK9wH3EMgXMumMRjNvDgw6Ew=="

client = InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

data = "mem,host=host1 used_percent=23.43234543"
write_api.write(bucket, org, data)

query = f'from(bucket: \"{bucket}\") |> range(start: -1h)'
tables = client.query_api().query(query, org=org)