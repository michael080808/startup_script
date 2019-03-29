cd `dirname $0`
path=`pwd`
user=`whoami`
echo "*  *    * * *   $user $path/seu-wlan/seu-wlan.sh" | sudo tee -a /etc/crontab
echo "*  *    * * *   $user $path/ip-monitor/ip-monitor.sh" | sudo tee -a /etc/crontab
sudo service cron restart
