#! /bin/sh
SRS_DIR="/usr/local/srs"
SRS_LOG="/usr/local/srs/srs.log"
SRS="/usr/local/srs/objs/srs"
SRS_CONF="/usr/local/srs/conf/rtmp.conf"

start() {
    cd $SRS_DIR
    [ -x $SRS ] || exit 5
    nohup $SRS -c $SRS_CONF > $SRS_LOG 2>&1 &
    retval1=$?
    nohup rabbitmq-server --detached > /dev/null 2>&1 &
    retval2=$?
    retval=`expr $retval1 + $retval2`
    return $retval
}
start_srs() {
    cd $SRS_DIR
    [ -x $SRS ] || exit 5
    nohup $SRS -c $SRS_CONF > $SRS_LOG 2>&1 &
    retval=$?
    return $retval
}
start_rabbitmq() {
    nohup rabbitmq-server --detached > /dev/null 2>&1 &
    retval=$?
    return $retval
}

stop() {
    PID1=$(ps -aux|grep srs|grep -v grep|awk 'NR==1 {printf $2}')
    kill -9 ${PID1}
    if [ $? -eq 0 ];then
        echo "kill srs success"
    else
        echo "kill srs fail"
    fi
    PID2=$(ps -aux|grep rabbitmq|grep -v grep|awk 'NR==1 {printf $2}')
    PID3=$(ps -aux|grep rabbitmq|grep -v grep|awk 'NR==2 {printf $2}')
    kill -9 ${PID2} ${PID3}
    if [ $? -eq 0 ];then
    echo "kill rabbitmq success"
    else
        echo "kill rabbitmq fail"
    fi
}
restart() {
    stop
    sleep 1
    start
}
watch_dog() {
    p_count_srs_cmd=$(ps -aux|grep srs|grep -v grep|wc -l)
    p_count_srs=${p_count_srs_cmd}
    if [[ $p_count_srs -eq 0 ]];then
        start_srs
    fi
    p_count_rabbitmq_cmd=$(ps -aux|grep rabbitmq|grep -v grep|wc -l)
    p_count_rabbitmq=${p_count_rabbitmq_cmd}
    if [[ $p_count_rabbitmq -eq 0 ]];then
        start_rabbitmq
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
