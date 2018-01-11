#! /bin/sh
BASE_DIR="/usr/local/project/raspberrypi_video/raspberrypi/python_rtmp"
CAPTURE_VIDEO=$BASE_DIR"/capture_video.py"
LOG_PATH="log_name/tmp/tcpdump_rtmp.log"
LOGGER_PATH=$BASE_DIR"/logger.sh"

start() {
    cd $BASE_DIR
    [ -f $CAPTURE_VIDEO ] || exit 5
    nohup python $CAPTURE_VIDEO > /dev/null 2>&1 &
    retval1=$?
    sh $LOGGER_PATH restart
    retval2=$?
    retval=`expr $retval1 + $retval2`
    return $retval
}
stop() {
    PID=$(ps -aux|grep capture_video.py|grep -v grep|awk 'NR==1 {printf $2}')
    kill -9 ${PID}
    if [ $? -eq 0 ];then
        echo "kill capture_video.py success"
    else
        echo "kill capture_video.py fail"
    fi
}
restart() {
    stop
    sleep 1
    start
}
watch_dog(){
    p_count_capture_video_cmd=$(ps -aux|grep capture_video.py|grep -v grep|wc -l)
    p_count_capture_video=${p_count_capture_video_cmd}
    if [ $p_count_capture_video -eq 0 ];then
        start
    fi
    if [ -f $LOG_PATH ]; then 
        file_modify_time=$(ls --full-time $LOG_PATH  | awk '{print $6 " " $7}')
        first_stamp=`date -d "${file_modify_time}" +%s`
        today_stamp=`date +%s`
        let second_stamp= $today_stamp - $first_stamp 
        if [ $second_stamp -gt 300];then
	        restart
        fi
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    watchdog)
        watch_dog || exit 0
        ;;
    *)
        echo $"Usage: $0 {start|stop|watchdog}"
        exit 2
esac
