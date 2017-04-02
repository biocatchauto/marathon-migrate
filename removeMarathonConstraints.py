import requests
import json
import argparse
import sys


def parse_args():
    """ Parses command line arguments. """
    parser = argparse.ArgumentParser(description='Marathon Remove Constraints Script')
    parser.add_argument('--url', dest='url', type=str, help='Marathon URL (http://marathon.example.com)')
    parser.add_argument('--hosts', dest='hosts', type=str, help='Hosts going to go for maintenance')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    maintenance_hosts = args.hosts.split(',')
    marathon_endpoint = args.url
    apps_endpoint = "/v2/apps"
    apps_url = marathon_endpoint +apps_endpoint
    headers = {'contentType': 'application/json'}
    apps = requests.get(url=apps_url)
    data = apps.json()

    for app in data['apps']:
        new_constraints = []
        del app['uris']
        del app['version']
        app_url = apps_url + app['id'] + "?force=true"
        constraints = app['constraints']
        print app['id']
        if constraints:
                print constraints
                for constraint in constraints:
                    exists = False
                    if constraint[1] == "UNLIKE":
                        for host in maintenance_hosts:
                            if constraint[2] == host:
                                exists = True
                    if not exists:
                        new_constraints.append(constraint)
                app['constraints'] = new_constraints
                try:
                    response = requests.put(url=app_url, data=json.dumps(app), headers=headers)
                    print(response.json())
                    if response.status_code == 200:
                        print ("constraints removed from: " + app['id'])
                except requests.exceptions.RequestException as e:
                    print(e)
                    sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())