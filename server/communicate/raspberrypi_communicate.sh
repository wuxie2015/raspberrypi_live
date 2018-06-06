#! /bin/sh

BASE_DIR="/usr/local/project/raspberrypi_light/server/communicate"
SOCKET_SERVER=$BASE_DIR"/tri_body_red_shore.py"
ETO=$BASE_DIR"/tri_body_eto.py"

start() {
    [ -f $SOCKET_SERVER ] || exit 5
    nohup python3 $SOCKET_SERVER > /dev/null 2>&1 &
    retval1=$?
    [ -f $ETO ] || exit 5
    nohup python3 $ETO > /dev/null 2>&1 &
    retval2=$?
    retval=`expr $retval1 + $retval2`
    return $retval
}
start_socket_server() {
    [ -f $SOCKET_SERVER ] || exit 5
    nohup python3 $SOCKET_SERVER > /dev/null 2>&1 &
    retval=$?
    return $retval
}
start_eto() {
    [ -f $ETO ] || exit 5
    nohup python3 $ETO > /dev/null 2>&1 &
    retval=$?
    return $retval
}

stop() {
    PID1=$(ps -aux|grep tri_body_red_shore.py|grep -v grep|awk 'NR==1 {printf $2}')
    kill -9 ${PID1}
    if [ $? -eq 0 ];then
        echo "kill tri_body_red_shore.py success"
    else
        echo "kill tri_body_red_shore.py fail"
    fi
    PID2=$(ps -aux|grep tri_body_eto.py|grep -v grep|awk 'NR==1 {printf $2}')
    kill -9 ${PID2}
    if [ $? -eq 0 ];then
    echo "kill tri_body_eto.py success"
    else
        echo "kill tri_body_eto.py fail"
    fi
}
restart() {
    stop
    sleep 1
    start
}
watch_dog() {
    p_count_red_shore_cmd=$(ps -aux|grep tri_body_red_shore.py|grep -v grep|wc -l)
    p_count_red_shore=${p_count_red_shore_cmd}
    if [[ $p_count_red_shore -eq 0 ]];then
        start_socket_server
    fi
    p_count_eto_cmd=$(ps -aux|grep tri_body_eto.py|grep -v grep|wc -l)
    p_count_eto=${p_count_eto_cmd}
    if [[ $p_count_eto -eq 0 ]];then
        start_eto
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
