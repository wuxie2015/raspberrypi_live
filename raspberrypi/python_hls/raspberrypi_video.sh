#! /bin/sh
BASE_DIR="/usr/local/project/raspberrypi_video/raspberrypi/python_hls/"
CAPTURE_VIDEO="/usr/local/project/raspberrypi_video/raspberrypi/python_hls/capture_video.py"
SOCKET_CLIENT="/usr/local/project/raspberrypi_video/raspberrypi/python_hls/socket_client.py"

start() {
    cd $BASE_DIR
    [ -f $SOCKET_CLIENT ] || exit 5
    nohup python $SOCKET_CLIENT > /dev/null 2>&1 &
    retval1=$?
    [ -f $CAPTURE_VIDEO ] || exit 5
    nohup python $CAPTURE_VIDEO > /dev/null 2>&1 &
    retval2=$?
    retval=`expr $retval1 + $retval2`
    return $retval
}
start_socket_client() {
    cd $BASE_DIR
    [ -f $SOCKET_CLIENT ] || exit 5
    nohup python $SOCKET_CLIENT > /dev/null 2>&1 &
    retval=$?
    return $retval
}
start_capture_video() {
    cd $BASE_DIR
    [ -f $CAPTURE_VIDEO ] || exit 5
    nohup python $CAPTURE_VIDEO > /dev/null 2>&1 &
    retval=$?
    return $retval
}
stop() {
    PID1=$(ps -aux|grep capture_video_alone.py|grep -v grep|awk 'NR==1 {printf $2}')
    kill -9 ${PID1}
    if [ $? -eq 0 ];then
    echo "kill capture_video_alone.py success"
    else
        echo "kill capture_video_alone.py fail"
    fi
    PID2=$(ps -aux|grep socket_client_alone.py|grep -v grep|awk 'NR==1 {printf $2}')
    kill -9 ${PID2}
    if [ $? -eq 0 ];then
    echo "kill socket_client_alone.py success"
    else
        echo "kill socket_client_alone.py fail"
    fi
}
restart() {
    stop
    sleep 1
    start
}
watch_dog(){
    p_count_socket_client_cmd=$(ps -aux|grep socket_client_alone.py|grep -v grep|wc -l)
    p_count_socket_client=${p_count_socket_client_cmd}
    if [ $p_count_socket_client -eq 0 ];then
        start_socket_client
    fi
    p_count_capture_video_cmd=$(ps -aux|grep capture_video_alone.py|grep -v grep|wc -l)
    p_count_capture_video=${p_count_capture_video_cmd}
    if [ $p_count_capture_video -eq 0 ];then
        start_capture_video
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
