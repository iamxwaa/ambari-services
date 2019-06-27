#!/usr/bin/env python

import sys, os 
import json 
import logging 
import platform 
from resource_management import * 
from resource_management.core.logger import Logger

class VapFlumeServer(Script):
  def install(self, env):
    import params
    env.set_params(params)

    if not os.path.exists(params.app_shell) :
      install_cmd = format("mkdir {install_dir_path};cp {file_path} {install_dir_path};cd {install_dir_path};unzip {file_name};rm -f {file_name}")
      Logger.info(install_cmd)
      os.system(install_cmd)

    self.configure(env)

  def status(self, env):
    import params
    env.set_params(params)

    pidfile = format("{install_dir_path}/flume-ui.pid")
    Logger.info("Check "+pidfile)

    check_process_status(pidfile)

  def configure(self, env):
    Logger.info("Cofigure Vap Flume ...")
    import params
    env.set_params(params)

  def start(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    if not os.path.exists(params.app_shell) :
      cp_cmd = format("cp {app_shell_origin} {install_dir_path};chmod 755 {app_shell}")
      Execute(cp_cmd)
      
    self.stop(env)

    start_cmd = format("export java_opt='-Xms{ui_memory}m -Xmx{ui_memory}m';export flume_ui_port={port};export flume_ui_home={install_dir_path};export max_allow_mem={collector_memory};{app_run} start")
    Logger.info(start_cmd)
    os.system(start_cmd)

  def stop(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    stop_cmd = format("export export flume_ui_home={install_dir_path};{app_run} stop")
    Logger.info(stop_cmd)
    os.system(stop_cmd)
 
if __name__ == "__main__":
  VapFlumeServer().execute()