#! /bin/sh
SOCKET_SERVER_LOG="/usr/local/project/raspberrypi_video/server/socket_server.log"
SCAN_FILE_LOG="/usr/local/project/raspberrypi_video/server/socket_server.log"
SOCKET_SERVER="/usr/local/project/raspberrypi_video/server/socket_server.py"
SCAN_FILE="/usr/local/project/raspberrypi_video/server/scan_file.py"

start() {
    [ -x $SOCKET_SERVER ] || exit 5
    nohup python $SOCKET_SERVER > $SOCKET_SERVER_LOG 2>&1 &
    retval1=$?
    [ -x $SCAN_FILE ] || exit 5
    nohup python $SCAN_FILE > $SCAN_FILE_LOG 2>&1 &
    retval2=$?
    retval=`expr $retval1 + $retval2`
    return $retval
}
start_socket_server() {
    [ -x $SOCKET_SERVER ] || exit 5
    nohup python $SOCKET_SERVER > $SOCKET_SERVER_LOG 2>&1 &
    retval=$?
    return $retval
}
start_scan_file() {
    [ -x $SCAN_FILE ] || exit 5
    nohup python $SCAN_FILE > $SCAN_FILE_LOG 2>&1 &
    retval=$?
    return $retval
}

stop() {
    PID1=$(ps -aux|grep socket_server.py|grep ^[^grep]|awk 'NR==1 {printf $2}')
    kill -9 ${PID1}
    if [ $? -eq 0 ];then
        echo "kill $input1 success"
    else
        echo "kill $input1 fail"
    fi
    PID2=$(ps -aux|grep scan_file.py|grep ^[^grep]|awk 'NR==1 {printf $2}')
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
watch_dog() {
    p_count_capture_video_cmd=$(ps -aux|grep socket_server.py|grep ^[^grep]|wc -l)
    p_count_capture_video=${p_count_capture_video_cmd}
    if [[ $p_count_capture_video -eq 0 ]];then
        start_socket_server
    fi
    p_count_scan_file_cmd=$(ps -aux|grep scan_file.py|grep ^[^grep]|wc -l)
    p_count_scan_file=${p_count_scan_file_cmd}
    if [[ $p_count_scan_file -eq 0 ]];then
        start_scan_file
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
