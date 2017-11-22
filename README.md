# Navigation-System

## Commands to get gpsd started and pointed to UART
```python
# disable gpsd systemd service
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket

# kill all gpsd jobs
sudo killall gpsd

# enable uart
sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock


```
