sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sudo killall gpsd
sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock
cgps -s
