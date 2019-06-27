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

    self.configure(env)
    self.install_packages(env)

  def status(self, env):
    pidfile = "/var/run/vap-flume/vap-flume.pid"
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

    print params.app_shell_origin
    if not os.path.exists(params.app_shell) :
      cp_cmd = format("cp {app_shell_origin} {home};chmod 755 {app_shell}")
      Execute(cp_cmd)
      
    start_cmd = format("{app_run} start -p {port} -h {home} -jm {ui_memory} -mam {collector_memory} -ar {auto_restart}")
    Execute(start_cmd)

  def stop(self, env):
    import params
    env.set_params(params)

    self.configure(env)

    stop_cmd = format("{app_run} stop")
    Execute(stop_cmd)
 
if __name__ == "__main__":
  VapFlumeServer().execute()