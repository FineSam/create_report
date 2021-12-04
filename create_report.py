from prometheus_pandas import query
from matplotlib import pyplot as plt
import sys
from varname import nameof
import re

p = query.Prometheus('http://<prometheus>:9090')

def rename_column(column_name):
    match = re.search(r'instance="(.*?)"', column_name)
    return match.group(1)

start_time = '2021-12-03T00:00:00Z'
end_time = '2021-12-04T16:10:00Z'
step_time = '5m'
queries = ['memory_usage_percent','cpu_usage_percent','dns_query_count']

for query in queries:
    df = p.query_range(query,start_time, end_time, step_time)
    df.columns = df.columns.to_series().apply(rename_column)
    plt.style.use('dark_background')
    plot = df.plot(title=query)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.9), ncol=3)
    plot.get_figure().savefig(query+".png",bbox_inches='tight')
