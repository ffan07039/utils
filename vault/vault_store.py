import sys
import json
import requests
import os
import yaml

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-v', '--vault-yaml',
                    help='vault yaml file', default='vault.yml')
parser.add_argument('-s', '--secrets-json',
                    help='json k-v pair of secrets', default='secrets.json')

args = parser.parse_args()


def store_secret(vault_yaml, key, value):
    url = os.path.join(vault_yaml['server_url'], 'v1/secret', vault_yaml['root_path'], key)
    req_headers = {
        "X-Vault-Token": vault_yaml['token'],
        "Content-Type": "application/json",
    }
    json_payload ={'value': value}
    response = requests.post(url, headers=req_headers, json=json_payload)
    if response.status_code == 200 or response.status_code == 204:
        return
    else:
        raise RuntimeError(f'bad response code {response.status_code} for POST, {url}')


with open(args.secrets_json, 'r') as f:
    secrets_json = json.load(f)
    #print(secrets_json)

with open(args.vault_yaml, 'r') as f:
    vault_yaml = yaml.load(f, Loader=yaml.FullLoader)
    #print(vault_yaml)

for k, v in secrets_json.items():
    store_secret(vault_yaml, k, v)
