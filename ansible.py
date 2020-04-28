#!/usr/bin/env pythons

import re
import json
import shutil
from collections import namedtuple
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C


func_ret = ''

class ResultCallback(CallbackBase):

    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        global func_ret

        # ansible-playbook Result Save
        host = result._host
        func_ret = func_ret+ json.dumps({host.name : result._result}, indent = 4)



# since API is constructed for CLI it expects certain options to always be set, named tuple 'fakes' the args parsing options object
Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
options = Options(connection='local', module_path=['/to/mymodules'], forks=10, become=None, become_method=None, become_user=None, check=False, diff=False)

# initialize needed objects
loader = DataLoader() # Takes care of finding and reading yaml, json and ini files
passwords = dict(vault_pass='secret')

# Instantiate our ResultCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
results_callback = ResultCallback()

################
#:global func_ret
ip = '172.27.0.188'
pw = 'DgmOTd7xnTPV'
func_src = '/root/ansible-useradd/pytest.py'
func_dest = '/root/pytest1515.py'
script_src = '/root/ansible-useradd/phoronix.sh'
script_dest = '/root/phoronix.sh'
################

# create inventory, use path to host config file as source or hosts in a comma separated string
inventory = InventoryManager(loader=loader, sources='localhost,')

# variable manager takes care of merging all the different sources to give you a unifed view of variables available in each context
variable_manager = VariableManager(loader=loader, inventory=inventory)

# create datastructure that represents our play, including tasks, this is basically what our YAML loader does internally.
# add_host function of playbook
play_source_host =  dict(
        name = "add hosts with arg",
        hosts = 'localhost',
        gather_facts = 'no',
        tasks = [
            dict(action=dict(module='add_host', hostname=ip
                , group='tmp', ansible_connection='ssh', ansible_ssh_user='root', ansible_ssh_pass=pw)),
         ]
)

# act fucntion of playbook
play_source_run =  dict(
        name = "run script in hosts",
        hosts = 'tmp',
        tasks = [
            dict(action=dict(module="ping")),
            dict(action=dict(module='copy', src=func_src, dest=func_dest)),
            dict(action=dict(module='copy', src=script_src, dest=script_dest)),
            dict(action=dict(module='debug', var=func_ret)),
            dict(action=dict(module='command', args='chmod 777 ' + script_dest)),
            dict(action=dict(module='command', args='sh ' + script_dest), register='run_ret'),
            dict(action=dict(module='debug', msg='{{run_ret.stdout_lines}}')),
            #dict(action=dict(module='command', args='python ' + func_dest), register='run_ret'),
            dict(action=dict(module='set_fact', func_ret=func_ret+'{{item}}'), with_items='{{run_ret.stdout_lines}}'),
        ]

    )


# Create play object, playbook objects use .load instead of init or new methods,
# this will also automatically create the task objects from the info provided in play_source
play_host = Play().load(play_source_host, variable_manager=variable_manager, loader=loader)
play_run = Play().load(play_source_run, variable_manager=variable_manager, loader=loader)


# Run it - instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks

tqm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords=passwords,
              stdout_callback=results_callback,
        )
    result = tqm.run(play_host) #ansible playbook run
    result = tqm.run(play_run) #ansible playbook run

    # Print to std <value func_ret = result of each host>
    print "#################################"
    print func_ret
    print "#################################"

finally:
    # we always need to cleanup child procs and the structres we use to communicate with them
    if tqm is not None:
        tqm.cleanup()

    # Remove ansible tmpdir
    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)


