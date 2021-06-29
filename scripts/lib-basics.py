#!/usr/bin/env python

# references:
#  https://github.com/kubernetes-client/python
#  https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md
import yaml
from pprint import pprint
from kubernetes import client, config


config.load_kube_config()
v1 = client.CoreV1Api()
v1_beta = client.ExtensionsV1beta1Api()

# Pods
print("*PODS*")
print('')
pods = v1.list_pod_for_all_namespaces(watch=False).to_dict()
print(f"{len(pods['items'])} pods found across all namespaces")
for pod in pods['items']:
    print(f"  {pod['metadata']['namespace']}: {pod['metadata']['name']}")
print('')

# Nodes
print('*NODES*')
nodes = v1.list_node()
for node in nodes.items:
    print(node.metadata.name)
    print(f"  pod cidr: {node.spec.pod_cidr}")
    internal_ip = [e.address for e in node.status.addresses if e.type == 'InternalIP'][0]
    print(f"  internal IP: {internal_ip}")
    external_ip = [e.address for e in node.status.addresses if e.type == 'ExternalIP']
    if external_ip:
        print(f"  external IP: {external_ip[0]}")
    else:
        print(f"  external IP: NONE")
    print(f"  capacity: {node.status.capacity}")
    print(f"  allocatable: {node.status.allocatable}")
    print(f"  volumes attached: {node.status.volumes_attached}")
    print(f"  volumes in use: {node.status.volumes_in_use}")
    print(f"  unschedulable: {node.spec.unschedulable}")
    if node.spec.taints:
        print(f"  taints:")
        for taint in node.spec.taints:
            print(f"    {taint.key} = {taint.value} - {taint.effect}")

# Yaml Files
print ("*YAML FILE*")
path = "./test-pod.yaml"
with open(path) as fil:
    manifest = yaml.safe_load(fil)
print("Yeah ok this is silly.")
# This has an example https://github.com/kubernetes-client/python/blob/master/kubernetes/utils/create_from_yaml.py#L68
# it's not what I was hoping for. I'd wanted something far more flexible. Back to the API!
