#! /bin/bash
BASE_DIR="/usr/local/project/raspberrypi_video/raspberrypi/python_rtmp/"
SCRIPT_NAME="capture_video.py"
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
    time=`sed -n "1p" watchdog_record.txt`
    timeStamp=`date -d "$time" +%s`
    current=`date "+%Y-%m-%d %H:%M:%S"`
    currentTimeStamp=`date -d "$current" +%s`
    timeDelta=$[$currentTimeStamp-$timeStamp]
    if [ $timeDelta -lt 50000 ];then
        echo $SCRIPT_NAME is running
    else
        restart
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
