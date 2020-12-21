# kmux

A tmux launcher for Kubernetes that creates one pane per pod, sets the env
variables `POD`, `KUBE_CONTEXT`, and `KUBE_NAMESPACE` and runs the commands in
the given input file in every pane.

## Dependencies

 - Python 3.8+
 - [smux](https://github.com/hq6/smux/blob/master/setup.py)
 - tmux (any version)

## Installation

Manual Method:

    git clone https://github.com/hq6/kmux.git
    # Add the directory to your PATH

Automatic Method:

    pip3 install kmux.py

## Usage

   0. Create a new file, either from scratch or by copying Sample.kmux.
   1. Type in the commands that you want to run, likely dependent on the
      selected POD.
         ```
         ---------
         command1
         command2
         command3
         ```

      Note that a pane does not necessary need to run any commands.

   3. Run `kmux.py <input_file_name>`. By default, this will run the commands
      in the input file against all pods in the current Kubernetes [context](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)
      You may also specify a target context with the command line option
      `--kube_context`. It will exhibit undefined behavior if there is no
      current context and no context has been specified.

## Sample kmux inputs:
 * TODO(hq6): Add some sample inputs.
