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
        func_ret = func_ret+ json.dumps({host.name : result._result['stdout_lines']}, indent = 4)


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
cache_src = '/root/ansible-useradd/cachebench.sh'
cache_dest = '/root/cachebench.sh'
cache_txt = '/root/cachebench.txt'
crafty_src = '/root/ansible-useradd/crafty.sh'
crafty_dest = '/root/crafty.sh'
crafty_txt = '/root/crafty.txt'
himeno_src = '/root/ansible-useradd/himeno.sh'
himeno_dest = '/root/himeno.sh'
himeno_txt = '/root/himeno.txt'
apache_src = '/root/ansible-useradd/apache.sh'
apache_dest = '/root/apache.sh'
apache_txt = '/root/apache.txt'
openssl_src = '/root/ansible-useradd/openssl.sh'
openssl_dest = '/root/openssl.sh'
openssl_txt = '/root/openssl.txt'
zip7_src = '/root/ansible-useradd/7zip.sh'
zip7_dest = '/root/7zip.sh'
zip7_txt = '/root/compress-7zip.txt'
gzip_src = '/root/ansible-useradd/gzip.sh'
gzip_dest = '/root/gzip.sh'
gzip_txt = '/root/compress-gzip.txt'
lzma_src = '/root/ansible-useradd/lzma.sh'
lzma_dest = '/root/lzma.sh'
lzma_txt = '/root/compress-lzma.txt'
pbzip2_src = '/root/ansible-useradd/pbzip2.sh'
pbzip2_dest = '/root/pbzip2.sh'
pbzip2_txt = '/root/compress-pbzip2.txt'
cray_src = '/root/ansible-useradd/cray.sh'
cray_dest = '/root/cray.sh'
cray_txt = '/root/c-ray.txt'
gnu_src = '/root/ansible-useradd/gnu.sh'
gnu_dest = '/root/gnu.sh'
gnu_txt = '/root/gnupg.txt'
sample_src = '/root/ansible-useradd/sample.sh'
sample_dest = '/root/sample.sh'
sample_txt = '/root/sample-program.txt'
################

# create inventory, use path to host config file as source or hosts in a comma separated string
inventory = InventoryManager(loader=loader, sources='localhost,')

# variable manager takes care of merging all the different sources to give you a unifed view of variables available in each context
variable_manager = VariableManager(loader=loader, inventory=inventory)

# create datastructure that represents our play, including tasks, this is basically what our YAML loader does internally.
# add_host function of playbook
play_source_host = dict(
    name="add hosts with arg",
    hosts='localhost',
    gather_facts='no',
    tasks=[
        dict(action=dict(module='add_host', hostname=ip
                         , group='tmp', ansible_connection='ssh', ansible_ssh_user='root', ansible_ssh_pass=pw)),
    ]
)

# act cpu check of playbook
play_source_crafty =  dict(
        name = "run script in hosts",
        hosts = 'tmp',
        tasks = [
            dict(action=dict(module="ping")),
            dict(action=dict(module='copy', src=crafty_src, dest=crafty_dest, mode='a+x')),
            dict(action=dict(module='command', args='sh ' + crafty_dest)),
            dict(action=dict(module='command', args='cat ' + crafty_txt), register='crafty_ret'),
            dict(action=dict(module='debug', msg='{{crafty_ret.stdout_lines}}')),
        ]

    )


# act cpu check of playbook
play_source_himeno =  dict(
        name = "run script in hosts",
        hosts = 'tmp',
        tasks = [
            dict(action=dict(module="ping")),
            dict(action=dict(module='copy', src=himeno_src, dest=himeno_dest, mode='a+x')),
            dict(action=dict(module='command', args='sh ' + himeno_dest)),
            dict(action=dict(module='command', args='cat ' + himeno_txt), register='himeno_ret'),
            dict(action=dict(module='debug', msg='{{himeno_ret.stdout_lines}}')),
        ]

    )


# act cpu check of playbook
play_source_openssl =  dict(
        name = "run script in hosts",
        hosts = 'tmp',
        tasks = [
            dict(action=dict(module="ping")),
            dict(action=dict(module='copy', src=openssl_src, dest=openssl_dest, mode='a+x')),
            dict(action=dict(module='command', args='sh ' + openssl_dest)),
            dict(action=dict(module='command', args='cat ' + openssl_txt), register='openssl_ret'),
            dict(action=dict(module='debug', msg='{{openssl_ret.stdout_lines}}')),
        ]

    )


# act cpu check of playbook
play_source_apache =  dict(
        name = "run script in hosts",
        hosts = 'tmp',
        tasks = [
            dict(action=dict(module="ping")),
            dict(action=dict(module='copy', src=apache_src, dest=apache_dest, mode='a+x')),
            dict(action=dict(module='command', args='sh ' + apache_dest)),
            dict(action=dict(module='command', args='cat ' + apache_txt), register='apache_ret'),
            dict(action=dict(module='debug', msg='{{apache_ret.stdout_lines}}')),
        ]

    )

# act memory check of playbook
play_source_cache = dict(
        name = "run script in hosts",
        hosts = 'tmp',
        tasks = [
            dict(action=dict(module='copy', src=cache_src, dest=cache_dest, mode='a+x')),
            dict(action=dict(module='command', args='sh ' + cache_dest)),
            dict(action=dict(module='command', args='cat ' + cache_txt), register='cache_ret'),
            dict(action=dict(module='debug', msg='{{cache_ret.stdout_lines}}')),
            ]
            )


# act memory check of playbook
play_source_7zip = dict(
        name = "run script in hosts",
        hosts = 'tmp',
        tasks = [
            dict(action=dict(module='copy', src=zip7_src, dest=zip7_dest, mode='a+x')),
            dict(action=dict(module='command', args='sh ' + zip7_dest)),
            dict(action=dict(module='command', args='cat ' + zip7_txt), register='7zip_ret'),
            dict(action=dict(module='debug', msg='{{7zip_ret.stdout_lines}}')),
            ]
            )


# act memory check of playbook
play_source_gzip = dict(
        name = "run script in hosts",
        hosts = 'tmp',
        tasks = [
            dict(action=dict(module='copy', src=gzip_src, dest=gzip_dest, mode='a+x')),
            dict(action=dict(module='command', args='sh ' + gzip_dest)),
            dict(action=dict(module='command', args='cat ' + gzip_txt), register='gzip_ret'),
            dict(action=dict(module='debug', msg='{{gzip_ret.stdout_lines}}')),
            ]
            )



# act memory check of playbook
play_source_lzma = dict(
        name = "run script in hosts",
        hosts = 'tmp',
        tasks = [
            dict(action=dict(module='copy', src=lzma_src, dest=lzma_dest, mode='a+x')),
            dict(action=dict(module='command', args='sh ' + lzma_dest)),
            dict(action=dict(module='command', args='cat ' + lzma_txt), register='lzma_ret'),
            dict(action=dict(module='debug', msg='{{lzma_ret.stdout_lines}}')),
            ]
            )
# act memory check of playbook
play_source_pbzip2 = dict(
    name="run script in hosts",
    hosts='tmp',
    tasks=[
        dict(action=dict(module='copy', src=pbzip2_src, dest=pbzip2_dest, mode='a+x')),
        dict(action=dict(module='command', args='sh ' + pbzip2_dest)),
        dict(action=dict(module='command', args='cat ' + pbzip2_txt), register='pbzip2_ret'),
        dict(action=dict(module='debug', msg='{{pbzip2_ret.stdout_lines}}')),
    ]
)

# act memory check of playbook
play_source_cray = dict(
    name="run script in hosts",
    hosts='tmp',
    tasks=[
        dict(action=dict(module='copy', src=cray_src, dest=cray_dest, mode='a+x')),
        dict(action=dict(module='command', args='sh ' + cray_dest)),
        dict(action=dict(module='command', args='cat ' + cray_txt), register='cray_ret'),
        dict(action=dict(module='debug', msg='{{cray_ret.stdout_lines}}')),
    ]
)

# act memory check of playbook
play_source_gnu = dict(
    name="run script in hosts",
    hosts='tmp',
    tasks=[
        dict(action=dict(module='copy', src=gnu_src, dest=gnu_dest, mode='a+x')),
        dict(action=dict(module='command', args='sh ' + gnu_dest)),
        dict(action=dict(module='command', args='cat ' + gnu_txt), register='gnu_ret'),
        dict(action=dict(module='debug', msg='{{gnu_ret.stdout_lines}}')),
    ]
)

# act memory check of playbook
play_source_sample = dict(
    name="run script in hosts",
    hosts='tmp',
    tasks=[
        dict(action=dict(module='copy', src=cray_src, dest=sample_dest, mode='a+x')),
        dict(action=dict(module='command', args='sh ' + sample_dest)),
        dict(action=dict(module='command', args='cat ' + sample_txt), register='sample_ret'),
        dict(action=dict(module='debug', msg='{{sample_ret.stdout_lines}}')),
    ]
)

# FIO
play_source_fio = dict(
    name="run FIO",
    hosts='tmp',
    tasks=[
        dict(action=dict(module='command',
                         args='fio --directory=/root/fio --name fio_test_file --direct=1 --rw=randread --bs=4K --size=1G --numjobs=5 --time_based --runtime=180 --group_reporting --norandommap > /root/fio.txt')),
        dict(action=dict(module='command', args='rm -r /root/fio')),
    ]
)

# Create play object, playbook objects use .load instead of init or new methods,
# this will also automatically create the task objects from the info provided in play_source
play_host = Play().load(play_source_host, variable_manager=variable_manager, loader=loader)
play_crafty = Play().load(play_source_crafty, variable_manager=variable_manager, loader=loader)
play_cache = Play().load(play_source_cache, variable_manager=variable_manager, loader=loader)
play_himeno = Play().load(play_source_himeno, variable_manager=variable_manager, loader=loader)
play_openssl = Play().load(play_source_openssl, variable_manager=variable_manager, loader=loader)
play_apache = Play().load(play_source_apache, variable_manager=variable_manager, loader=loader)
play_7zip = Play().load(play_source_7zip, variable_manager=variable_manager, loader=loader)
play_gzip = Play().load(play_source_gzip, variable_manager=variable_manager, loader=loader)
play_lzma = Play().load(play_source_lzma, variable_manager=variable_manager, loader=loader)
play_pbzip2 = Play().load(play_source_pbzip2, variable_manager=variable_manager, loader=loader)
play_cray = Play().load(play_source_cray, variable_manager=variable_manager, loader=loader)
play_gnu = Play().load(play_source_gnu, variable_manager=variable_manager, loader=loader)
play_sample = Play().load(play_source_sample, variable_manager=variable_manager, loader=loader)
play_fio = Play().load(play_source_fio, variable_manager=variable_manager, loader=loader)
# Run it - instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks

tqm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords=passwords,
              #stdout_callback=results_callback,
        )
    result = tqm.run(play_host) #ansible playbook run


    '''
    p = find final result in all result of crafty result
    func_ret = temp value of result
    crafty = final result of CPU check (using crafty module)
    '''

    p = re.compile('Average: [0-9]+')

    result = tqm.run(play_crafty)
    func_ret = p.findall(func_ret)
    crafty = ''
    if len(func_ret) >= 1 :
        crafty = func_ret[0]
    else :
        crafty = 'Error'
    func_ret = ''


    result = tqm.run(play_cache)
    func_ret = p.findall(func_ret)
    cache = ''
    if len(func_ret) >= 1 :
        cache = func_ret[0]
    else :
        cache = 'Error'
    func_ret = ''

    result = tqm.run(play_himeno)
    func_ret = p.findall(func_ret)
    himeno = ''
    if len(func_ret) >= 1:
        himeno = func_ret[0]
    else:
        himeno = 'Error'
    func_ret = ''

    result = tqm.run(play_openssl)
    func_ret = p.findall(func_ret)
    openssl = ''
    if len(func_ret) >= 1:
        openssl = func_ret[0]
    else:
        openssl = 'Error'
    func_ret = ''

    result = tqm.run(play_apache)
    func_ret = p.findall(func_ret)
    apache = ''
    if len(func_ret) >= 1:
        apache = func_ret[0]
    else:
        apache = 'Error'
    func_ret = ''

    result = tqm.run(play_7zip)
    func_ret = p.findall(func_ret)
    zip7 = ''
    if len(func_ret) >= 1:
        zip7 = func_ret[0]
    else:
        zip7 = 'Error'
    func_ret = ''

    '''
    result = tqm.run(play_gzip)
    func_ret = p.findall(func_ret)
    gzip = ''
    if len(func_ret) >= 1 :
        gzip = func_ret[0]
    else :
        gzip = 'Error'
    func_ret = ''
    '''

    result = tqm.run(play_lzma)
    func_ret = p.findall(func_ret)
    lzma = ''
    if len(func_ret) >= 1:
        lzma = func_ret[0]
    else:
        lzma = 'Error'
    func_ret = ''

    result = tqm.run(play_pbzip2)
    func_ret = p.findall(func_ret)
    pbzip2 = ''
    if len(func_ret) >= 1:
        pbzip2 = func_ret[0]
    else :
        pbzip2 = 'Error'
    func_ret = ''

    result = tqm.run(play_cray)
    func_ret = p.findall(func_ret)
    cray = ''
    if len(func_ret) >= 1 :
        cray = func_ret[0]
    else :
        cray = 'Error'
    func_ret = ''

    result = tqm.run(play_gnu)
    func_ret = p.findall(func_ret)
    gnu = ''
    if len(func_ret) >= 1 :
        gnu = func_ret[0]
    else :
        gnu = 'Error'
    func_ret = ''

    result = tqm.run(play_sample)
    func_ret = p.findall(func_ret)
    sample = ''
    if len(func_ret) >= 1 :
        sample = func_ret[0]
    else :
        sample = 'Error'
    func_ret = ''

    result = tqm.run(play_fio)

    # Print to std <value func_ret = result of each host>
    print "#################################"
    print "Crafty Result // " + crafty
    print "CacheBench Result // " + cache
    print "Himeno Result // " + himeno
    print "Openssl Result // " + openssl
    print "Apache Result // " + apache
    print "Compress-7zip Result // " + zip7
    #print "Compress-gzip Result // " + gzip
    print "Compress-lzma Result // " + lzma
    print "Compress-pbzip2 Result // " + pbzip2
    print "C-ray Result // " + cray
    print "Gnupg Result // " + gnu
    print "Sample-Program Result // " + sample
    print "#################################"

finally:
    # we always need to cleanup child procs and the structres we use to communicate with them
    if tqm is not None:
        tqm.cleanup()

    # Remove ansible tmpdir
    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)




