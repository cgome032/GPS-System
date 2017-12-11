import time

from gps3 import gps3

gpsd_socket = gps3.GPSDSocket()
gpsd_socket.connect()
gpsd_socket.watch()
data_stream = gps3.DataStream()

try:
    for new_data in gpsd_socket:
        if new_data:
            data_stream.unpack(new_data)
        if data_stream.TPV['lat'] != 'n/a':
            speed = data_stream.TPV['speed']
            latitude = data_stream.TPV['lat']
            longitude = data_stream.TPV['lon']
            altitude = data_stream.TPV['alt']
            print(speed, latitude, longitude, altitude)

        else:
            print('Nothin in gps')
            time.sleep(.1)
        time.sleep(.8)

except KeyboardInterrupt:
    gpsd_socket.close()
    print('\nTerminated by user\nGood Bye.\n')

