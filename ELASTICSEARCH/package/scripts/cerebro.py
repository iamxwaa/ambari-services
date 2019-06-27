#!/usr/bin/env python

import sys, os 
import json 
import logging 
import platform 
from resource_management import * 
from resource_management.core.logger import Logger

class Cerebro(Script):
  def install(self, env):
    import params
    env.set_params(params)

    self.install_packages(env)
    install_cmd = format("cp {cerebro_zip} {es_home};cd {es_home};unzip {cerebro_file};chmod 755 {cerebro_dir}/bin/cerebro")
    Execute(install_cmd)
    mk_cmd = format('mkdir {cerebro_pid_path};chmod 777 {cerebro_pid_path}')
    Execute(mk_cmd)

    self.configure(env)


  def status(self, env):
    import params
    env.set_params(params)

    pidfile = format("{cerebro_pid_file}")
    Logger.info("Check "+pidfile)
    check_process_status(pidfile)

  def configure(self, env):
    Logger.info("Cofigure cerebro ...")
    import params
    env.set_params(params)
    
    open(params.config_f_cerebro,'w').write(params.cerebro_config)

  def start(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    if not os.path.exists(params.cerebro_pid_path) :
      Execute("mkdir "+params.cerebro_pid_path)  
    
    start_cmd = format('export JAVA_HOME={java_home};nohup {es_home}/{cerebro_dir}/bin/cerebro -Dhttp.port={cerebro_http_port} > /dev/null 2>&1 & echo $! > {cerebro_pid_file}')
    Execute(start_cmd)

  def stop(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    pid_file = format("{cerebro_pid_file}")
    pid = format('`cat {pid_file}` > /dev/null 2>&1')
    Execute(format('kill {pid}'), ignore_failures=True)
    File(pid_file, action = 'delete')
 
if __name__ == "__main__":
  Cerebro().execute()