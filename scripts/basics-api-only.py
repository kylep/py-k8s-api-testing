#!/usr/bin/env python
import requests
import urllib3
import os
import yaml
from pprint import pprint

# disable tls warnings
urllib3.disable_warnings()

# load the kubeconfig
kubeconf_path = os.environ["PY_KUBECONFIG"]
cluster_name = os.environ["PY_KUBECLUSTER"]
print(f"Load kubeconfig file {kubeconf_path}")
with open(kubeconf_path, "r") as kubeconf_file:
    kubeconf = yaml.load(kubeconf_file, Loader=yaml.FullLoader)
cluster = next(c for c in kubeconf['clusters'] if c['name'] == cluster_name)
print("")

# Try a GET to the API server: 403 access denied
url = cluster['cluster']['server']
resp = requests.get(url, verify=False)
print(f"GET {url}")
pprint(resp.json())
print("")

# Try the /api/ resource, also 403 access denied
api_url = f"{url}/api/"
resp = requests.get(api_url, verify=False)
print(f"GET {api_url}")
pprint(resp.json())
print("")

# Authenticate
print("So, there are like *no* examples of a TokenRequest with just the API's. Pivoting to lib.")
