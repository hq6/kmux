#!/usr/bin/env python3

from kubernetes import client, config

config.load_kube_config()
current_namespace = config.list_kube_config_contexts()[1]['context']['namespace']
print(current_namespace)

v1 = client.CoreV1Api()
print("Listing pods with their IPs:")
ret = v1.list_namespaced_pod(current_namespace)
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
