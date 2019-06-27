#!/usr/bin/env python

import sys, os 
import json 
import logging 
import platform 
from resource_management import * 
from resource_management.core.logger import Logger

class Elasticsearch(Script):
  def install(self, env):
    import params
    env.set_params(params)

    self.install_packages(env)
    
    Execute(format("usermod -G root {es_user}"))
    Execute(format("usermod -G hadoop {es_user}"))
    Execute(format("mkdir {es_data_path};chmod 777 {es_data_path}"))
    
    self.configure(env)


  def status(self, env):
    import params
    env.set_params(params)

    pidfile = format("{es_pid_path}")
    Logger.info("Check "+pidfile)
    check_process_status(pidfile)

  def configure(self, env):
    Logger.info("Cofigure elasticsearch ...")
    import params
    env.set_params(params)
    
    open(params.config_f_es,'w').write(params.elasticsearch_config)
    open(params.config_f_jvm,'w').write(params.jvm_config)
    open(params.config_f_log,'w').write(params.log4j2_config)

  def start(self, env):
    import params
    env.set_params(params)

    self.configure(env)
      
    start_cmd = 'su -s /bin/bash {es_user} -c "export JAVA_HOME={java_home};{es_home}/bin/elasticsearch -p {es_pid_path} --quiet -Edefault.path.logs={es_log_path} -Edefault.path.conf={es_config_path} -Edefault.path.data={es_data_path}"'
    Execute(format(start_cmd), wait_for_finish=False)

  def stop(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    pid_file = format("{es_pid_path}")
    pid = format('`cat {pid_file}` > /dev/null 2>&1')
    Execute(format('kill {pid}'), ignore_failures=True)
    File(pid_file, action = 'delete')
 
if __name__ == "__main__":
  Elasticsearch().execute()