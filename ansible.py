#!/usr/bin/env pythons

import re
import json
import shutil
import time
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
        func_ret = func_ret+ json.dumps({host.name : result._result["stdout_lines"]}, indent = 4)



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
phoronix_ret = '/root/phoronix.txt'
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

# act cpu check of playbook
play_source_cpu =  dict(
        name = "run script in hosts",
        hosts = 'tmp',
        tasks = [
            dict(action=dict(module="ping")),
            dict(action=dict(module='copy', src=script_src, dest=script_dest, mode='a+x')),
            dict(action=dict(module='command', args='sh ' + script_dest)),
            dict(action=dict(module='command', args='cat ' + phoronix_ret), register='run_ret'),
            dict(action=dict(module='debug', msg='{{run_ret.stdout_lines}}')),
        ]

    )
# act memory check of playbook
play_source_mem = dict(
        name = "run script in hosts",
        hosts = 'tmp',
        tasks = [
            dict(action=dict(module='copy', src=script_src, dest=script_dest, mode='a+x')),
            dict(action=dict(module='command', args='sh ' + script_dest)),
            dict(action=dict(module='command', args='cat ' + phoronix_ret), register='run_ret'),
            dict(action=dict(module='debug', msg='{{run_ret.stdout_lines}}')),
            ]
            )

#add_host init
play_source_host_ini = dict(
        name = "host ini",
        hosts = 'localhost',
        gather_facts = 'no',
        tasks = [
            dict(action=dict(module='add_host', hostname=ip
                   , group='ini', ansible_connection='ssh',ansible_ssh_user='root', ansible_ssh_pass=pw)),
        ]

)

# read to result
play_source_ret = dict (
        name = "Save result to python value",
        hosts = 'tmp',
        tasks = [
            dict(action=dict(module="ping")),
            dict(action=dict(module='command', args='cat ' + phoronix_ret), register='run_ret'),
            dict(action=dict(module='debug',msg='{{run_ret.stdout_lines}}')),
        ]

    )

# Create play object, playbook objects use .load instead of init or new methods,
# this will also automatically create the task objects from the info provided in play_source
play_host = Play().load(play_source_host, variable_manager=variable_manager, loader=loader)
play_cpu = Play().load(play_source_cpu, variable_manager=variable_manager, loader=loader)


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
    result = tqm.run(play_cpu) #ansible playbook run

    '''
    p = find final result in all result of crafty result
    func_ret = temp value of result
    crafty = final result of CPU check (using crafty module)
    '''
    p = re.compile('Average: [0-9]+')
    func_ret = p.findall(func_ret)
    func_ret = func_ret[0]
    crafty = func_ret
    func_ret = ''

    # Print to std <value func_ret = result of each host>
    print "#################################"
    print "CPU Check (With crafty) Result : " + crafty
    print "#################################"

finally:
    # we always need to cleanup child procs and the structres we use to communicate with them
    if tqm is not None:
        tqm.cleanup()

    # Remove ansible tmpdir
    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)



