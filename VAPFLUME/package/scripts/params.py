#!/usr/bin/env python

import sys, os 
from resource_management.libraries.script.script import Script

config = Script.get_config()

port = config['configurations']['vap-flume-site']['vap.flume.port']
ui_memory = config['configurations']['vap-flume-site']['vap.flume.ui.memory']
collector_memory = config['configurations']['vap-flume-site']['vap.flume.collector.memory']

file_name = "vap-flume.zip"
file_path = sys.path[0] + "/../files/" + file_name
install_dir_path = "/var/lib/vap-flume"

app_shell_origin = sys.path[0]+"/../files/start-ambari-flume.sh"
app_shell = install_dir_path + "/start-ambari-flume.sh"
app_run = app_shell