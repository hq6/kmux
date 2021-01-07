from setuptools import setup

long_description=\
"""
kmux
====================

A tmux launcher for Kubernetes that creates one pane per pod, sets the env
variables ``POD``, ``KUBE_CONTEXT``, and ``KUBE_NAMESPACE`` and runs the commands in
the given input file in every pane.

Dependencies
========================================

* Python3.8+
* smux
* tmux (any version)

Installation
========================================

Run the following command::

    pip3 install kmux.py

Usage
========================================

0. Create a new file, either from scratch or by copying Sample.kmux.
1. Type in the commands that you want to run, likely dependent on the
   selected POD.::

     ---------
     command1
     command2
     command3

  Note that a pane does not necessary need to run any commands.

3. Run ``kmux.py <input_file_name>``. By default, this will run the commands
   in the input file against all pods in the current Kubernetes context.
   You may also specify a target context with the command line option
   ``--kube_context``. It will exhibit undefined behavior if there is no
   current context and no context has been specified.

"""

setup(
  name="kmux.py",
  version='0.1.9',
  author="Henry Qin",
  author_email="root@hq6.me",
  description="Tmux launcher for kubernetes",
  long_description=long_description,
  long_description_content_type="text/x-rst",
  platforms=["All platforms that tmux runs on."],
  license="MIT",
  url="https://github.com/hq6/kmux",
  scripts=['kmux.py'],
  python_requires='>=3.8',
  install_requires = ['smux.py>=0.1.19', 'kubernetes']
)
