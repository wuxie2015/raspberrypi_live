#! /bin/sh
BASE_DIR="/usr/local/project/raspberrypi_video/raspberrypi/python_rtmp/"
CAPTURE_VIDEO="/usr/local/project/raspberrypi_video/raspberrypi/python_rtmp/capture_video.py"

start() {
    cd $BASE_DIR
    [ -f $CAPTURE_VIDEO ] || exit 5
    nohup python $CAPTURE_VIDEO > /dev/null 2>&1 &
    retval=$?
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
