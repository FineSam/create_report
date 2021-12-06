from prometheus_pandas import query
from matplotlib import pyplot as plt
import re
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import pymsteams

p = query.Prometheus('http://<prometheus>:9090')

def rename_column(column_name):
    match = re.search(r'instance="(.*?)"', column_name)
    return match.group(1)

last_day_of_last_month = datetime.today().replace(day=1) - relativedelta(days=1)
last_month = datetime.today() - relativedelta(months=1)
beginning_of_last_month = datetime(last_month.year,last_month.month,1,0,0)
end_of_last_month = datetime(last_month.year,last_month.month,last_day_of_last_month.day,23,59,59)

#start_time = beginning_of_last_month.strftime('%Y-%m-%dT%H:%M:%SZ')
#end_time = end_of_last_month.strftime('%Y-%m-%dT%H:%M:%SZ')

end_time = datetime.now()
start_time = end_time - relativedelta(hours=1)

step_time = '5m'
queries = ['memory_usage_percent','cpu_usage_percent','dns_query_count']

for query in queries:
    df = p.query_range(query,start_time, end_time, step_time)
    df.columns = df.columns.to_series().apply(rename_column)
    df['average'] = df.mean(axis=1)
    plt.style.use('dark_background')
    plot = df.plot(title=query, alpha=0.3)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.9), ncol=3)
    plot.get_figure().savefig(query+".png",bbox_inches='tight')
    plot.lines[-1].set_alpha(1)

myTeamsMessage = pymsteams.connectorcard("<Microsoft Webhook URL>")
myTeamsMessage.text("this is my text")
myTeamsMessage.color("blue")
myTeamsMessage.printme()
