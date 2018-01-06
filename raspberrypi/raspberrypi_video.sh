#! /bin/sh
CAPTURE_VIDEO = "/usr/local/project/raspberrypi_video/raspberrypi/alone/capture_video_alone.py"
SOCKET_CLIENT = "/usr/local/project/raspberrypi_video/raspberrypi/alone/socket_client_alone.py"

start() {
    [ -x $SOCKET_CLIENT ] || exit 5
    daemon $SOCKET_CLIENT
    retval1=$?
    [ -x $CAPTURE_VIDEO ] || exit 5
    daemon $CAPTURE_VIDEO
    retval2=$?
    $retval = `expr $retval1 + $retval2`
    return $retval
}
start_socket_client() {
    [ -x $SOCKET_CLIENT ] || exit 5
    daemon $SOCKET_CLIENT
    retval=$?
    return $retval
}
start_capture_video() {
    [ -x $CAPTURE_VIDEO ] || exit 5
    daemon $CAPTURE_VIDEO
    retval=$?
    return $retval
}
stop() {
    PID1=$(ps -e|grep capture_video_alone.py|awk '{printf $1}')
    kill -9 ${PID1}
    if [ $? -eq 0 ];then
    echo "kill $input1 success"
    else
        echo "kill $input1 fail"
    fi
    PID2=$(ps -e|grep socket_client_alone.py|awk '{printf $1}')
    kill -9 ${PID2}
    if [ $? -eq 0 ];then
    echo "kill $input1 success"
    else
        echo "kill $input1 fail"
    fi
}
restart() {
    stop
    sleep 1
    start
}
watch_dog(){
    p_count_capture_video_alone=$(ps -e|grep capture_video_alone.py|wc -l)
    if [$p_count_capture_video -eq 0];then
        start_socket_client
    fi
    p_count_socket_client_alone=$(ps -e|grep socket_client_alone.py|wc -l)
    if [$p_count_scan_file -eq 0];then
        start_capture_video
    fi
}

case "$1" in
    start)
        rh_status_q && exit 0
        $1
        ;;
    stop)
        rh_status_q || exit 0
        $1
        ;;
    watchdog)
        watch_dog || exit 0
        $1
        ;;
    *)
        echo $"Usage: $0 {start|stop|watchdog}"
        exit 2
esac