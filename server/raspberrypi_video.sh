#! /bin/sh
SOCKET_SERVER = "/usr/local/project/raspberrypi_video/server/socket_server.py"
SCAN_FILE = "/usr/local/project/raspberrypi_video/server/scan_file.py"

start() {
    [ -x $SOCKET_SERVER ] || exit 5
    daemon $SOCKET_SERVER
    retval1=$?
    [ -x $SCAN_FILE ] || exit 5
    daemon $SCAN_FILE
    retval2=$?
    $retval = `expr $retval1 + $retval2`
    return $retval
}
start_socket_server() {
    [ -x $SOCKET_SERVER ] || exit 5
    daemon $SOCKET_SERVER
    retval=$?
    return $retval
}
start_scan_file() {
    [ -x $SCAN_FILE ] || exit 5
    daemon $SCAN_FILE
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
    p_count_capture_video=$(ps -e|grep socket_server.py|wc -l)
    if [$p_count_capture_video -eq 0];then
        start_socket_server
    fi
    p_count_scan_file=$(ps -e|grep scan_file.py|wc -l)
    if [$p_count_scan_file -eq 0];then
        start_scan_file
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