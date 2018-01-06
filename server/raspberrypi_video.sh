SOCKET_SERVER = "/usr/local/project/raspberrypi_video/server/capture_video_alone.py"
SCAN_FILE = "/usr/local/project/raspberrypi_video/server/scan_file.py"

start() {
    [ -x $nginx ] || exit 5
    daemon $nginx -c SOCKET_SERVER
    retval1=$?
    daemon $nginx -c SCAN_FILE
    retval2=$?
    $retval = `expr $retval1 + $retval2`
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
    configtest || return $?
    stop
    sleep 1
    start
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
    *)
        echo $"Usage: $0 {start|stop}"
        exit 2
esac