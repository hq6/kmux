#!/usr/bin/env python3

from kubernetes import client, config
import smux
import argparse
from sys import argv
import sys, os
import re

def main():
  parser = argparse.ArgumentParser(description='Start tmux panes on K8 pods.')
  parser.add_argument('--pods', '-p', metavar='PODS', type=str,
                      help='Whitespace-separated list of pods. When given, -r is ignored.')
  parser.add_argument('--pod_name_regex', '-r',
                      metavar='POD_NAME_REGEX',
                      type=re.compile,
                      help='Regular expression matching a pod in the namespace.')
  parser.add_argument('--kube_context', '-k',
                      metavar='KUBE_CONTEXT',
                      type=str,
                      help='The Kubernetes context to pull pods from. Defaults to current context.')
  parser.add_argument('--no_create', '-n', action='store_true',
                      help='Do not crerate new tmux windows and panes. Run the ' +
                      'commands in only the first found pod in the current ' +
                      'window. One pane will be created if kmux is not started inside a tmux.')
  parser.add_argument('commands_file', nargs='?',
                      type=argparse.FileType('r'),
                      default=open(os.devnull, 'r'),
                      help="Commands to run against every pod. " +
                      "The env variables POD, KUBE_CONTEXT, and KUBE_NAMESPACE will be set before these commands are run." +
                      "If not given, will be read from stdin.")

  # Check for environmental variable with args, command line overrides
  args = argv[1:]
  if 'KMUX_ARGS' in os.environ:
    args = os.environ['KMUX_ARGS'].split() + args

  options = parser.parse_args(args)
  commands = options.commands_file.read().strip().split("\n")
  # Deal with Python split producing an extra empty string at the end when
  # input is one or zero lines by removing it.
  if commands[-1] == '':
    commands = commands[:-1]
  ################################################################################ 
  # Load K8 config and Initialize magic variables
  config.load_kube_config()
  contexts = config.list_kube_config_contexts()[0]
  current_context = config.list_kube_config_contexts()[1]['name']
  current_namespace = config.list_kube_config_contexts()[1]['context']['namespace']

  PODS = None
  KUBE_CONTEXT = None
  KUBE_NAMESPACE = None

  if options.kube_context:
    KUBE_CONTEXT = options.kube_context
    for context in contexts:
      if context['name'] == KUBE_CONTEXT:
        KUBE_NAMESPACE = context['context']['namespace']
        break
    if not KUBE_NAMESPACE:
      print(f"Invalid context {KUBE_CONTEXT} given")
      sys.exit(1)
  else:
    KUBE_CONTEXT = current_context
    KUBE_NAMESPACE = current_namespace

  if options.pods:
    PODS = options.pods.split()
  else:
    # Collect all the pods in the context.
    kubeClient = client.CoreV1Api(
        api_client=config.new_client_from_config(context=KUBE_CONTEXT))
    podObjects = kubeClient.list_namespaced_pod(current_namespace)
    PODS = [x.metadata.name for x in podObjects.items]

    # Filter by regex if given
    if options.pod_name_regex:
      PODS = [pod for pod in PODS if options.pod_name_regex.match(pod)]
  if not PODS:
    print("No pods selected.")
    return
  ################################################################################ 
  pod_commands = [[
      f'POD={POD}',
      f'KUBE_CONTEXT={KUBE_CONTEXT}',
      f'KUBE_NAMESPACE={KUBE_NAMESPACE}'] + (commands) for POD in PODS]

  smux.create(len(pod_commands), pod_commands[1:] if options.no_create else pod_commands,
      executeAfterCreate=lambda : smux.tcmd("setw synchronize-panes on"),
      noCreate=options.no_create)

if __name__ == "__main__":
    # execute only if run as a script
    main()
