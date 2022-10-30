from uptime_kuma_api import UptimeKumaApi, MonitorType
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def authenticate():
    global api
    api = UptimeKumaApi(os.getenv('UPTIME_KUMA_URL'))
    api.login(os.getenv('USERNAME'), os.getenv('PASSWORD'))


def _get_service_list():
    data = pd.read_csv("service_list.csv")
    return data


def _add_services_to_kuma(service_list):
    result = []
    global api
    for index, row in service_list.iterrows():
        result.append(api.add_monitor(type=row.monitor_type, name=row.name, url=row.url, interval=row.interval, retryInterval=row.retry_interval, maxretries=row.max_retries, ignoreTls=True))

    return result


def _disconnect():
    global api
    api.disconnect()


if __name__ == '__main__':
    authenticate()
    service_list = _get_service_list()
    result = _add_services_to_kuma(service_list)
    print(result)
    _disconnect()
