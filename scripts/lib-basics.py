#!/usr/bin/env python
from pprint import pprint
from kubernetes import client, config


config.load_kube_config()
v1 = client.CoreV1Api()

print("Information about pods")
print('')
pods = v1.list_pod_for_all_namespaces(watch=False).to_dict()
print(f"{len(pods['items'])} pods found across all namespaces")
for pod in pods['items']:
    print(f"  {pod['metadata']['namespace']}: {pod['metadata']['name']}")
print('')
