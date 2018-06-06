#! /bin/sh

### BEGIN INIT INFO
# Provides:        ntp
# Required-Start:  $local_fs $network $named $remote_fs $time $syslog
# Required-Stop:   $local_fs $network $named $remote_fs $time $syslog
# Default-Start:   2 3 4 5
# Default-Stop:
# Short-Description: Start communicating daemon
### END INIT INFO

BASE_DIR="/usr/local/project/raspberry_light/raspberrypi/communicate/"
SCRIPT_NAME="tri_body_eto.py"
SCRIPT_PATH=$BASE_DIR$SCRIPT_NAME

start() {
    cd $BASE_DIR
    [ -f $SCRIPT_PATH ] || exit 5
	pids=`ps -aux|grep $SCRIPT_NAME|grep -v grep|awk '{print $2}'`
    if [ ! ${pids} ];then
		nohup python $SCRIPT_PATH > /dev/null 2>&1 &
		retval=$?
		echo start $SCRIPT_NAME success
	else
	    echo $SCRIPT_NAME is running
	    retval=0
	fi
	return $retval
}
stop() {
    PID=$(ps -aux|grep $SCRIPT_NAME|grep -v grep|awk 'NR==1 {printf $2}')
    kill -9 ${PID}
    if [ $? -eq 0 ];then
        echo kill $SCRIPT_NAME success
    else
        echo kill $SCRIPT_NAME fail
    fi
}
restart() {
    stop
    sleep 1
    start
}
watch_dog(){
    pids=`ps -aux|grep $SCRIPT_NAME|grep -v grep|awk '{print $2}'`
    if [ ${pids} ];then
        echo $SCRIPT_NAME is running
    else
        start
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    watchdog)
        watch_dog || exit 0
        ;;
    *)
        echo $"Usage: $0 {start|stop|watchdog}"
        exit 2
esac
