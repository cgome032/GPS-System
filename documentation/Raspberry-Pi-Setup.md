# GPS-System

## Commands to get gpsd started and pointed to UART

```bash
# disable gpsd systemd service
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket

# kill all gpsd jobs
sudo killall gpsd

# enable uart
sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock


```

## Citations
[gpsd code used from MartijnBraam](https://github.com/MartijnBraam/gpsd-py3.git "gpsd repository")
