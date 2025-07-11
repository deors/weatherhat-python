current_date=`date +%s`
log_timestamp=`stat -c "%Y" /home/pi/weatherhat.log`
pid=`pgrep -f weatherhat-adafruit.py | pgrep python`

if [ $(($current_date-$log_timestamp)) -gt 300 ]; then
    echo "process is not responding - killing pid $pid";
    kill -9 $pid;
    echo "process $pid killed at $current_date" >> /home/pi/weatherhat-monitor.log;
fi
