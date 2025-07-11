current_date=`date +%s`
log_timestamp=`stat -c "%Y" /home/pi/weatherhat.log`
pid=`pgrep -f weatherhat-adafruit.py | pgrep python`

#echo process id $pid
#echo $(($current_date-$log_timestamp))

if [ $(($current_date-$log_timestamp)) -gt 300 ]; then
     echo "process is not responding - maybe you should kill pid $pid";
fi
