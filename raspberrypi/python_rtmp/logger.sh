#! /bin/sh
TCPDUMP_CMD="tcpdump -v -i wlan0 host 118.126.65.199"

generate_log(){
	log_name=/tmp/tcpdump_rtmp.log
    	nohup $TCPDUMP_CMD > $log_name 2>&1 &
}
stop(){
	PID=$(ps -aux|grep tcpdump |grep -v grep|awk 'NR==1 {printf $2}')
	kill -9 ${PID}
	if [ $? -eq 0 ];then
	        echo "kill tcpdump success"
	else
		echo "kill tcpdump fail"
	fi
}
move(){
	#yesterday=`date -d last-day +%Y%m%d%H%M%S`
	#log_name='/tmp/delete/tcpdump_rtmp.baklog$yesterday'
	#today_logname='/tmp/tcpdump_rtmp.log'
	#mv $today_logname $log_name
        rm -rf /tmp/tcpdump_rtmp.log
        touch /tmp/tcpdump_rtmp.log
}

start(){
	generate_log
}

restart(){
	stop
	move
	generate_log
}

case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
	restart)
		restart || exit 0
		;;
	*)
		echo $"Usage: $0 {start|stop|restart}"
		exit 2
esac
