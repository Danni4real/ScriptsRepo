
nohup $(while [ 1 == 1 ]; do week=`date | awk '{print $1}'`;day=`date | awk '{print $2 $3}'`;hour=`date | awk '{print $4}' | awk -F ':' '{print $1}'`;minute=`date | awk '{print $4}' | awk -F ':' '{print $2}'`; if { [ $day == "Oct8" -o $day == "Oct9" ] || [ $week != "Sat" -a $week != "Sun" -a $day != "Jun3" -a $day != "Sep12" -a $day != "Oct3" -a $day != "Oct4" -a $day != "Oct5" -a $day != "Oct6" -a $day != "Oct7" ]; }&&[ $hour == "08" -o $hour == "20" ]; then input tap 700 450;sleep 10;input tap 550 1500;sleep 10;input tap 30 100;sleep 1860; fi; sleep 1740;done)&


