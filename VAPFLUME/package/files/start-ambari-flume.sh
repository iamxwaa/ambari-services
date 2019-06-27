#!/bin/bash
#---------------------启动参数配置-----------------------
#是否监听配置文件并重启
auto_restart=false
#文件扫描间隔时间(秒)
flume_file_scan=10
#是否在ambari中集成
is_ambari=false
#flume配置文件目录
flume_config_home=$flume_ui_home/flume/conf
#是否开启认证
flume_ui_auth=false
#认证地址
flume_ui_auth_url="http://localhost:8080/token/confirmation"
#rmi服务端口
flume_ui_rmi=17261
#是否后台启动
daemon=true
#-------------------启动参数配置结束-----------------------

java_home=""
app_jar=vap-flume-ui.jar
pid_file=$flume_ui_home/flume-ui.pid

f_status() {
  if [ -f "$pid_file" ];then
    pid=`cat $pid_file`
    ck=`ps -p $pid | wc -l`
    if [[ "1" == "$ck" ]];then
      echo "$pid_file exist,but process not running."
      return 1
    else
      echo $pid
      return 1
    fi
  fi
  return 0
}

f_check() {
  appath=$flume_ui_home/$app_jar
  if [ -f "$appath" ] ;then
    if [ -r "$appath" -a -w "$appath" -a -x "$appath" ] ;then
      echo "check $appath        ------------------OK"
	else
	  chmod 755 "$appath"
	  echo "fix $appath        ------------------OK"
	fi
  else
  	echo "check $appath        ------------------FAIL"
  	return 0
  fi
  appath2=$flume_ui_home/flume/bin/flume-ng
  if [ -f "$appath2" ] ;then
    if [ -r "$appath2" -a -w "$appath2" -a -x "$appath2" ] ;then
      echo "check $appath2        ------------------OK"
	else
	  chmod 755 "$appath2"
	  echo "fix $appath2        ------------------OK"
	fi
  else
  	echo "check $appath2        ------------------FAIL"
  	return 0
  fi
  return 1
}

f_start() {
  f_status
  stat=$?
  if [[ 0 == $stat ]];then
    f_check
    check=$?
    if [[ 1 == $check ]];then
      echo "start flume ui, port: $flume_ui_port."
      java_run="java"
      if [[ "" != "$java_home" ]];then
        java_run=$java_home/bin/java
      fi
      args="$java_opt"
      args="$args -DFLUME_UI_PORT=$flume_ui_port"
      args="$args -DFLUME_UI_HOME=$flume_ui_home"
      args="$args -DMAX_ALLOW_MEM=$max_allow_mem"
      args="$args -DAUTO_RESTART=$auto_restart"
      args="$args -DFLUME_FILE_SCAN=$flume_file_scan"
      args="$args -DIS_AMBARI=$is_ambari"
      args="$args -DFLUME_CONFIG_HOME=$flume_config_home"
      args="$args -DFLUME_UI_AUTH=$flume_ui_auth"
      args="$args -DFLUME_UI_AUTH_URL=$flume_ui_auth_url"
      args="$args -DFLUME_UI_RMI=$flume_ui_rmi"
      if [[ "" != "$java_home" ]];then
        args="$args -DUSER_JAVA_HOME=$java_home"
      fi
      cmd="$java_run $args -jar $flume_ui_home/$app_jar"
      if [[ "true" == "$daemon" ]];then
        nohup $cmd > /dev/null 2>&1 & echo $! > $pid_file
        cat $pid_file
      else
        $cmd
      fi
    else
      echo "start fail !!!"
    fi
  fi
}

f_stop() {
  echo "stop flume ui ..."
  pid=`cat $pid_file`
  kill -9 $pid
  rm -f $pid_file
}

case "$1" in
  start)
    f_start
  ;;
  stop)
    f_stop
  ;;
  status)
    f_status
  ;;
esac