<<<<<<< HEAD
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
=======
#! /bin/bash

BASE_DIR="/usr/local/project/raspberrypi_light/server/communicate/"
SOCKET_SERVER_NAME="tri_body_red_shore.py"
ETO_NAME="tri_body_eto.py"
SOCKET_SERVER=$BASE_DIR$SOCKET_SERVER_NAME
ETO=$BASE_DIR$ETO_NAME

start() {
    [ -f $SOCKET_SERVER ] || exit 5
    pids1=`ps -aux|grep $SOCKET_SERVER_NAME|grep -v grep|awk '{print $2}'`
    if [ ! ${pids1} ];then
        nohup python3 $SOCKET_SERVER > /dev/null 2>&1 &
        retval1=$?
        echo start $SOCKET_SERVER_NAME success
    else
	    echo $SOCKET_SERVER_NAME is running
	    retval1=0
	fi
    [ -f $ETO ] || exit 5
    pids2=`ps -aux|grep $ETO_NAME|grep -v grep|awk '{print $2}'`
    if [ ! ${pids2} ];then
        nohup python3 $ETO > /dev/null 2>&1 &
        retval2=$?
        echo start $ETO_NAME success
    else
	    echo $ETO_NAME is running
	    retval2=0
>>>>>>> bc2ebfe5aed7998f7b62599c1143004cc214b7e5
    retval=`expr $retval1 + $retval2`
    return $retval
}
start_socket_server() {
    [ -f $SOCKET_SERVER ] || exit 5
<<<<<<< HEAD
    nohup python3 $SOCKET_SERVER > /dev/null 2>&1 &
    retval=$?
=======
    pids=`ps -aux|grep $SOCKET_SERVER_NAME|grep -v grep|awk '{print $2}'`
    if [ ! ${pids} ];then
        nohup python3 $SOCKET_SERVER > /dev/null 2>&1 &
        retval=$?
        echo start $SOCKET_SERVER_NAME success
    else
	    echo $SOCKET_SERVER_NAME is running
	    retval=0
	fi
>>>>>>> bc2ebfe5aed7998f7b62599c1143004cc214b7e5
    return $retval
}
start_eto() {
    [ -f $ETO ] || exit 5
<<<<<<< HEAD
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
=======
    pids=`ps -aux|grep $ETO_NAME|grep -v grep|awk '{print $2}'`
    if [ ! ${pids} ];then
        nohup python3 $ETO > /dev/null 2>&1 &
        retval=$?
        echo start $ETO_NAME success
    else
	    echo $ETO_NAME is running
	    retval=0
	fi
	return $retval
}

stop() {
    PID1=$(ps -aux|grep $SOCKET_SERVER_NAME|grep -v grep|awk 'NR==1 {printf $2}')
    kill -9 ${PID1}
    if [ $? -eq 0 ];then
        echo kill $SOCKET_SERVER_NAME success
    else
        echo kill $SOCKET_SERVER_NAME fail
    fi
    PID2=$(ps -aux|grep $ETO_NAME|grep -v grep|awk 'NR==1 {printf $2}')
    kill -9 ${PID2}
    if [ $? -eq 0 ];then
        echo kill $ETO_NAME success
    else
        echo kill $ETO_NAME fail
>>>>>>> bc2ebfe5aed7998f7b62599c1143004cc214b7e5
    fi
}
restart() {
    stop
    sleep 1
    start
}
watch_dog() {
<<<<<<< HEAD
    p_count_red_shore_cmd=$(ps -aux|grep tri_body_red_shore.py|grep -v grep|wc -l)
    p_count_red_shore=${p_count_red_shore_cmd}
    if [[ $p_count_red_shore -eq 0 ]];then
        start_socket_server
    fi
    p_count_eto_cmd=$(ps -aux|grep tri_body_eto.py|grep -v grep|wc -l)
    p_count_eto=${p_count_eto_cmd}
    if [[ $p_count_eto -eq 0 ]];then
=======
    pids_red_shore=`ps -aux|grep $SOCKET_SERVER_NAME|grep -v grep|awk '{print $2}'`
    if [ ${pids_red_shore} ];then
        echo $SOCKET_SERVER_NAME is running
    else
        start_socket_server
    fi
    pids_eto=`ps -aux|grep $ETO_NAME|grep -v grep|awk '{print $2}'`
    if [ ${pids_eto} ];then
        echo $ETO_NAME is running
    else
>>>>>>> bc2ebfe5aed7998f7b62599c1143004cc214b7e5
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
