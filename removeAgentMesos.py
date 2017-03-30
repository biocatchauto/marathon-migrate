import requests
import json
import argparse
import time
import sys

maintenance_endpoint = "/maintenance/schedule"
machine_endpoint = "/machine/"


def parse_args():
    """ Parses command line arguments. """
    parser = argparse.ArgumentParser(description='Mesos Maintenance Script')
    parser.add_argument('--url', dest='url', type=str, help='Marathon URL (http://marathon.example.com)')
    parser.add_argument('--hosts', dest='hosts', type=str, help='Hosts going to go for maintenance')
    parser.add_argument('--json', dest='json', type=str, help='json path')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    maintenance_hosts = args.hosts.split(',')
    cluster_endpoint = args.url
    json_path = args.json
    # marathonUrl = "https://dcos-cus-prod.customers.biocatch.com/mesos"

    with open(json_path) as data_file:
        data = json.load(data_file)

    windows = data['windows']
    hosts = windows[0]['machine_ids']

    for ip in maintenance_hosts:
        hosts_dict = {"hostname": ip, "ip": ip}
        hosts.append(hosts_dict)

    windows[0]['machine_ids'] = hosts
    data['windows'] = windows

    maintenance_url = cluster_endpoint + maintenance_endpoint
    try:
        response = requests.post(url=maintenance_url, data=json.dumps(data))
        if response.status_code == 200:
            print("maintenance window set for hosts")
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    print response.status_code

    time.sleep(3)

    machine_down_url = cluster_endpoint + machine_endpoint + "down"
    try:
        response = requests.post(url=machine_down_url, data=json.dumps(hosts))
        if response.status_code == 200:
            print("Removed hosts from mesos")
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    time.sleep(2)
    machine_up_url = cluster_endpoint + machine_endpoint + "up"
    try:
        response = requests.post(url=machine_up_url, data=json.dumps(hosts))
        if response.status_code == 200:
            print("maintenance window cleared")
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
