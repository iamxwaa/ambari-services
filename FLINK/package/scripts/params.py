#!/usr/bin/env python

import sys, os 
from resource_management.libraries.script.script import Script

config = Script.get_config()

flink_user = config['configurations']['flink-site']['user']

flink_file_name = "flink-1.6.4-bin-scala_2.11.tgz"
flink_file_path = sys.path[0]+"/../files/" + flink_file_name
flink_dir_name = "/flink-1.6.4"
install_path = "/var/lib"
install_dir_path = install_path + flink_dir_name

start_shell = install_dir_path + "/bin/start-cluster.sh"
stop_shell = install_dir_path + "/bin/stop-cluster.sh"

pid_file_name = "flink-root-standalonesession.pid"
pid_path = "/tmp/" + pid_file_name

flink_config_dir_path = install_dir_path + "/conf"

#configuration
flink_masters_f_path = flink_config_dir_path + "/masters"
flink_slaves_f_path = flink_config_dir_path + "/slaves"
flink_config_f_path = flink_config_dir_path + "/flink-conf.yaml"
flink_sql_client_f_path = flink_config_dir_path + "/sql-client-defaults.yaml"
flink_zoo_f_path = flink_config_dir_path + "/zoo.cfg"

flink_masters = config['configurations']['flink-site']['masters']
flink_slaves = config['configurations']['flink-site']['slaves']

flink_config = config['configurations']['flink-conf']['content']
sql_client_defaults_config = config['configurations']['sql-client-defaults']['content']
zoo_config = config['configurations']['zoo']['content']