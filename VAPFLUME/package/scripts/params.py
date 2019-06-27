#!/usr/bin/env python

import sys, os 
from resource_management.libraries.script.script import Script

config = Script.get_config()

port = config['configurations']['vap-flume-site']['vap.flume.port']
home = config['configurations']['vap-flume-site']['vap.flume.home']
ui_memory = config['configurations']['vap-flume-site']['vap.flume.ui.memory']
collector_memory = config['configurations']['vap-flume-site']['vap.flume.collector.memory']
auto_restart = config['configurations']['vap-flume-site']['vap.flume.auto.restart']

app_shell_origin = sys.path[0]+"/../files/start-ambari-flume.sh"
app_shell = home + "/start-ambari-flume.sh"
app_run = app_shell