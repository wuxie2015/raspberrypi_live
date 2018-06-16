#!/bin/bash


function status {
  ps xf |grep "supervisord -c supervisord.conf" |grep -v grep
  ps xf |grep "python" |grep "manage.py" |grep -v grep
  supervisorctl status
}


function start {
  supervisord -c supervisord.conf
}


function stop {
  supervisorctl stop all
  ps axu |grep "python" |grep "manage.py" |grep -v grep |awk '{print $2}' |xargs kill -9 >/dev/null 2>&1
}


case $1 in
  status)
    status
    ;;
  start)
    start
    status
    ;;
  stop)
    stop
    status
    ;;
  restart)
    stop
    start
    status
    ;;
  *)
    echo "Usage: $0 {status|start|stop|restart}"
    ;;
esac