#!/bin/bash
export FLUME_UI_HOME=/usr/hdp/current/vap-flume
export FLUME_UI_APP=vap-flume-ui.jar
export IS_AMBARI=true
export FLUME_CONFIG_HOME=/etc/vap-flume
FLUME_PID_PATH=/var/run/vap-flume
FLUME_PID_FILE=vap-flume.pid

f_pid() {
  if [ ! -d "$FLUME_PID_PATH" ];then
    mkdir -p $FLUME_PID_PATH
    echo 0
  fi
  pidfile=`ls $FLUME_PID_PATH`
  if [[ "" != "$pidfile" ]] ;then
    fpid=`cat $FLUME_PID_PATH/$FLUME_PID_FILE`
    echo $fpid
  else
    echo 0
  fi
}

f_fix() {
  val_input=$1
  val_default=$2
  if [ -z "$val_input" ] ;then
    echo $val_default
  else
    echo $val_input
  fi
}

f_help() {
  cat <<EOF
示例: $0 <命令> [可选参数]...

命令:
  help                      show this help
  start                     start flume ui
  stop                      stop flume ui
  status                    show status
  
start 参数:
  --port,-p                 flume ui port,default 28080
  --max-allow-memory,-mam   default 61440MB
  --jvm-memory,-jm          jvm memory,default 1024mb
  --auto-restart,-ar        watch config file and auto reload
  
stop 参数:
  --force                   kill -9 pid
  
EOF
}

f_check() {
  appath=$FLUME_UI_HOME/$FLUME_UI_APP
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
  appath2=$FLUME_UI_HOME/flume/bin/flume-ng
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
  pid=`f_pid`
  if [[ 0 = "$pid" ]] || [[ "-1" = "$pid" ]];then
    f_check
    stat=$?
    if [[ 1 = "$stat" ]] ;then
      if [ ! -d "$FLUME_UI_HOME/logs" ];then
        mkdir -p $FLUME_UI_HOME/logs
      fi
      args="-Xms$1m -Xmx$1m -DFLUME_UI_HOME=$FLUME_UI_HOME -DFLUME_UI_PORT=$2 -DMAX_ALLOW_MEM=$3 -DAUTO_RESTART=$4 -DIS_AMBARI=true -DFLUME_CONFIG_HOME=/etc/vap-flume"
	    java $args -jar $FLUME_UI_HOME/$FLUME_UI_APP > /dev/null &
      fpid=$!
      if [ ! -d "$FLUME_PID_PATH" ];then
        mkdir -p $FLUME_PID_PATH
      fi
      echo $fpid > $FLUME_PID_PATH/$FLUME_PID_FILE
      sleep 2
      echo $fpid 
    fi
  else
    echo "$pid"
  fi
}

f_stop() {
  pid=`f_pid`
  if [[ 0 = "$pid" ]] || [[ "-1" = "$pid" ]];then
    echo "not running"
  else
    kill -$1 $pid
    rm -f $FLUME_PID_PATH/$FLUME_PID_FILE
  fi
}

f_status() {
  pid=`f_pid`
  if [ 0 = "$pid" ] ;then 
    echo "not running" 
  else 
    echo $pid
  fi
}

cmd=$1

case "$cmd" in
  start)
    while [ -n "$*" ] ;do
    arg=$1
    shift
      case $arg in
        --port|-p)
          ui_port=$1
          shift
        ;;
        --max-allow-memory|-mam)
          mam=$1
          shift
        ;;
        --jvm-memory,-jm)
          jvmm=$1
          shift
        ;;
        --auto-restart,-ar)
          auto=$1
          shift
        ;;
      esac
    done
    export FLUME_UI_AUTH=false
    export FLUME_UI_AUTH_URL="http://localhost:8080/token/confirmation"
    FLUME_JVM=`f_fix $jvmm 1024`
    FLUME_UI_PORT=`f_fix $ui_port 28080`
    MAX_ALLOW_MEM=`f_fix $mam 61400`
    AUTO_RESTART=`f_fix $auto false`
    f_start $FLUME_JVM $FLUME_UI_PORT $MAX_ALLOW_MEM $AUTO_RESTART
  ;;
  stop)
    if [ "$2" = "--force" ] ;then
	    sign=9
    else
      sign=15
    fi
    f_stop $sign
  ;;
  status)
    f_status
  ;;
  *)
    f_help
  ;;
esac