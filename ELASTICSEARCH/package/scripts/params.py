#!/usr/bin/env python

import sys, os 
from resource_management.libraries.script.script import Script

config = Script.get_config()

java_home = config['configurations']['elasticsearch-site']['java.home']

es_user = config['configurations']['elasticsearch-site']['user']


es_home = config['configurations']['elasticsearch-site']['elasticsearch.home']
es_config_path = config['configurations']['elasticsearch-site']['elasticsearch.config.path']
es_log_path = config['configurations']['elasticsearch-site']['elasticsearch.log.path']
es_data_path = config['configurations']['elasticsearch-site']['elasticsearch.data.path']
es_pid_path = "/var/run/elasticsearch/elasticsearch.pid"


elasticsearch_config = config['configurations']['elasticsearch']['content']
jvm_config = config['configurations']['jvm']['content']
log4j2_config = config['configurations']['log4j2']['content']

config_f_es = es_config_path + "/elasticsearch.yml"
config_f_jvm = es_config_path + "/jvm.options"
config_f_log = es_config_path + "/log4j2.properties"

cerebro_dir = "cerebro-0.7.2"
cerebro_file = "cerebro-0.7.2.zip"
cerebro_zip = sys.path[0]+"/../files/" + cerebro_file
cerebro_pid_path = "/var/run/cerebro"
cerebro_pid_file = cerebro_pid_path + "/cerebro.pid"
cerebro_http_port = config['configurations']['cerebro-site']['cerebro.http.port']

cerebro_config = config['configurations']['cerebro-site']['content']
config_f_cerebro = es_home + "/" + cerebro_dir + "/conf/application.conf"

files_dir = sys.path[0]+"/../files/"
es_rpm_name = "elasticsearch-5.6.16.rpm"
