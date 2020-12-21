#!/usr/bin/env python3

from kubernetes import client, config
import smux
import argparse
from sys import argv
import sys

# config.load_kube_config()
# current_namespace = config.list_kube_config_contexts()[1]['context']['namespace']
# current_context = config.list_kube_config_contexts()[1]['name']
# 
# v1 = client.CoreV1Api()
# pods = v1.list_namespaced_pod(current_namespace)
# pod_names = [x.metadata.name for x in pods.items]
# 
# pod_commands = [[
#     f'POD={pod_name}',
#     f'KUBE_CONTEXT={current_context}',
#     f'KUBE_NAMESPACE={current_namespace}',
#     'echo $POD $KUBE_CONTEXT $KUBE_NAMESPACE'] for pod_name in pod_names]
# 
# smux.create(len(pod_commands), pod_commands, executeBeforeAttach=lambda : smux.tcmd("setw synchronize-panes on"))

def main():
  parser = argparse.ArgumentParser(description='Start tmux panes on K8 pods.')
  parser.add_argument('--pods', '-p', metavar='PODS', type=str,
                      help='Whitespace-separated list of pods. When given, -r is ignored.')
  parser.add_argument('--pod_name_regex', '-r',
                      metavar='POD_NAME_REGEX',
                      type=str,
                      help='Regular expression matching a pod in the namespace.')
  parser.add_argument('--kube_context', '-k',
                      metavar='KUBERNETES_CONTEXT',
                      type=str,
                      help='The Kubernetes context to pull pods from. Defaults to current context.')
  parser.add_argument('commands_file', nargs='?',
                      type=argparse.FileType('r'),
                      default=sys.stdin,
                      help="Commands to run against every pod. " +
                      "The env variables POD, KUBE_CONTEXT, and KUBE_NAMESPACE will be set before these commands are run." +
                      "If not given, will be read from stdin.")

  options = parser.parse_args(argv[1:])
  commands = options.commands_file.read().split("\n")


if __name__ == "__main__":
    # execute only if run as a script
    main()
