#!/usr/bin/env python

import sys, os 
import json 
import logging 
import platform 
import subprocess
from resource_management import * 
from resource_management.core.logger import Logger

class FlinkMaster(Script):
  def install(self, env):
    import params
    env.set_params(params)

    if not os.path.exists(params.start_shell) :
      install_cmd = format("cp {flink_file_path} {install_path};cd {install_path};tar -xvf {flink_file_name};rm -f {flink_file_name}")
      Logger.info(install_cmd)
      os.system(install_cmd)

    self.configure(env)

  def status(self, env):
    import params
    env.set_params(params)

    pidfilePath = format("/tmp/flink-{flink_user}-standalonesession.pid")
    Logger.info("Check "+pidfilePath)

    check_process_status(pidfilePath)

  def configure(self, env):
    Logger.info("Cofigure flink master ...")
    import params
    env.set_params(params)
    
    open(params.flink_masters_f_path,'w').write(params.flink_masters)
    open(params.flink_slaves_f_path,'w').write(params.flink_slaves)
    open(params.flink_config_f_path,'w').write(params.flink_config)
    open(params.flink_sql_client_f_path,'w').write(params.sql_client_defaults_config)
    open(params.flink_zoo_f_path,'w').write(params.zoo_config)

  def start(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    cmd = format("export USER={flink_user};export PDSH_RCMD_TYPE=ssh;{start_shell}")
    Logger.info(cmd)
    os.system(cmd)

  def stop(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    cmd = format("export USER={flink_user};export PDSH_RCMD_TYPE=ssh;{stop_shell}")
    Logger.info(cmd)
    os.system(cmd)
 
if __name__ == "__main__":
  FlinkMaster().execute()