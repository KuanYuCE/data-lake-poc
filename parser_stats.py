# get time cost
#  trino --output-format CSV_UNQUOTED  --execute "select query_id , started, \"end\" from system.runtime.queries where state!='RUNNING'" > test
from datetime import datetime

ts_diff=[]
query_cost = {}

with open('test', 'r') as f:
    for i in f.readlines():
        data = i.strip().split(",")
        q_id = data[0]
        start = data[1]
        end = data[2]
        query_cost[q_id] = [
                datetime.strptime(start.split("UTC")[0].strip(), '%Y-%m-%d %H:%M:%S.%f'),
                datetime.strptime(end.split("UTC")[0].strip(), '%Y-%m-%d %H:%M:%S.%f')
            ]


for k, v in query_cost.items():
    query_cost[k] = (v[1]-v[0]).total_seconds()

# print(query_cost)




# query map
# trino --output-format csv_header  --execute "select query_id , query from system.runtime.queries where state='RUNNING'" > test
import pandas as pd
df = pd.read_csv("test2")
map_list = df.to_dict(orient='records')
query_map = {}
for i in map_list:
    query_map[i['query_id']] = i['query']
# print(query_map)


# print(query_cost)

new_query = {}
for k, v in query_cost.items():
    try:
        new_query[query_map[k]] = v
    except Exception:
        pass


print(new_query)
