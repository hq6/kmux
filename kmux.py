#!/usr/bin/env python3

from kubernetes import client, config
import smux

config.load_kube_config()
current_namespace = config.list_kube_config_contexts()[1]['context']['namespace']
current_context = config.list_kube_config_contexts()[1]['name']

v1 = client.CoreV1Api()
pods = v1.list_namespaced_pod(current_namespace)
pod_names = [x.metadata.name for x in pods.items]

pod_commands = [[
    f'POD={pod_name}',
    f'KUBE_CONTEXT={current_context}',
    f'KUBE_NAMESPACE={current_namespace}',
    'echo $POD $KUBE_CONTEXT $KUBE_NAMESPACE'] for pod_name in pod_names]

smux.create(len(pod_commands), pod_commands, executeBeforeAttach=lambda : smux.tcmd("setw synchronize-panes on"))
