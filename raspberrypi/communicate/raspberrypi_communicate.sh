#! /bin/sh

### BEGIN INIT INFO
# Provides:        ntp
# Required-Start:  $local_fs $network $named $remote_fs $time $syslog
# Required-Stop:   $local_fs $network $named $remote_fs $time $syslog
# Default-Start:   2 3 4 5
# Default-Stop:
# Short-Description: Start communicating daemon
### END INIT INFO

BASE_DIR="/usr/local/project/raspberry_light/raspberrypi/communicate"
ETO=$BASE_DIR"/tri_body_eto.py"

start() {
    cd $BASE_DIR
    [ -f $ETO ] || exit 5
    nohup python $ETO > /dev/null 2>&1 &
    retval=$?
    return $retval
}
stop() {
    PID=$(ps -aux|grep tri_body_eto.py|grep -v grep|awk 'NR==1 {printf $2}')
    kill -9 ${PID}
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
watch_dog(){
    p_count_eto_cmd=$(ps -aux|grep tri_body_eto.py|grep -v grep|wc -l)
    p_count_eto=${p_count_eto_cmd}
    if [ $p_count_eto -eq 0 ];then
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
    restart)
        restart
        ;;
    watchdog)
        watch_dog || exit 0
        ;;
    *)
        echo $"Usage: $0 {start|stop|watchdog}"
        exit 2
esac
