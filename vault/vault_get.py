import sys
import json
import requests
import os
import yaml

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-v', '--vault-yaml',
                    help='vault yaml file')
parser.add_argument('-k', '--key-json-list',
                    help='json list of keys to read')


args = parser.parse_args()


def request_secret(vault_yaml, key):
    url = os.path.join(vault_yaml['host'], 'v1/secret', key)
    req_headers = {
        "X-Vault-Token": vault_yaml['token']
    }
    response = requests.get(url, headers=req_headers)
    if response.status_code == 200:
        response_json = json.loads(response.content.decode())
        return response_json['data']['value']
    else:
        raise RuntimeError(f'bad response code {response.status_code} for GET, {url}')


with open(args.key_json_list, 'r') as f:
    key_json_array = json.load(f)
    #print(key_json_array)

with open(args.vault_yaml, 'r') as f:
    vault_yaml = yaml.load(f, Loader=yaml.FullLoader)
    #print(vault_yaml)

output = {}
for key in key_json_array:
    output[key] = request_secret(vault_yaml, key)

print(json.dumps(output, indent=True))
