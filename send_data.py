#this program will read in data from the accelrometer 
#and send it to the influxdb server which is running on the 
#aws EC2 instance using influxdb API


from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time
import board
import digitalio
import busio
import adafruit_lis3dh
import logging 
import numpy as np 
import datetime as dt
import RPi.GPIO as GPIO

import socket 




TCP_IP = '54.85.182.93' #LOCAL IP of EC2 Instance
TCP_PORT =  5015
buffer_size= 1024
LED =16
x_array = []
y_array = []
z_array = []

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED,GPIO.OUT)


#this function reads data from the sensor and appends the values to an numpy array so they can be avergaged 
# also it returns each  individual  value of x y and z
def read_data():
    # Hardware I2C setup. Use the CircuitPlayground built-in accelerometer if available;
    # otherwise check I2C pins.
    if hasattr(board, "ACCELEROMETER_SCL"):
        i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
        int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
        lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19, int1=int1)
    else:
        i2c = busio.I2C(board.SCL, board.SDA)
        int1 = digitalio.DigitalInOut(board.D6)  # Set to correct pin for interrupt!
        lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)


    # Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
    lis3dh.range = adafruit_lis3dh.RANGE_2_G


    
    # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
    # z axis values.  
    x, y, z = [
         value  for value in lis3dh.acceleration
    ]

    
    x_array.append(x)
    y_array.append(y)
    z_array.append(z)
    


    return x,y,z



#this function uses the python inflixdb-client api library to send the sensorr  values to the  influxdb cloud to be 
#analyzed and visualized 
def send_data_api(x,y,z):
    # You can generate a Token from the "Tokens Tab" in the UI
    token = "Abj-wu1yWUh_ikwiQMDBA8Z0X_-wJfHeuk3LxS9Tgl70hJzPMfeSSjVJYDTcN1HK9wH3EMgXMumMRjNvDgw6Ew=="
    org = "7256ca2ad5deacce"
    bucket = "mahjoub's Bucket"

    client = InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=token)

    write_api = client.write_api(write_options=SYNCHRONOUS)

    data_x = "mem,host=host1 x_value="+str(x)
    data_y = "mem,host=host1 y_value="+str(y)

    write_api.write(bucket, org, data_x)
    write_api.write(bucket, org, data_y)
    


    query = f'from(bucket: \"{bucket}\") |> range(start: -1h)'
    tables = client.query_api().query(query, org=org)


#this function sends the median and mean values of x,y,z to an AWS EC2 I set up and  once the data is received and 
# we recieve a message back from the instance it will turn on an LED on the bread board 
def send_data_tcp(mean,median):
    index = 1 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    

    message = str(median[index])
    message1 = str(median[index])
    s.send(message.encode())

    #s.send(message1.encode())


    data_recieved  = s.recv(buffer_size)

    if (data_recieved is not None):
        
        GPIO.output(LED,GPIO.HIGH)
    else:
        GPIO.output(LED,GPIO.LOW)
        
    print(data_recieved.decode())
    s.close()
    
    index = index +1 
    if (index == 3):
        index = 1
    
#this function takes in the x,y,z numpy arrays and finds the median and mean values 
def data_processing(x_array,y_array ,z_array):
    median= ([np.median(x_array),np.median(y_array),np.median(z_array)])
    mean = ([np.mean(x_array),np.mean(y_array),np.mean(z_array)])
    
    return median,mean


def main():
    while (True):
        #read in data from sensors
        x,y,z = read_data()

        #send the data to influxdb 
        #send_data_api(x,y,z)

        #process the data 
        median , mean = data_processing(x_array,y_array ,z_array)

        #send data to EC2 instance
        send_data_tcp(mean,median)



  

    


if __name__ == '__main__':
    main()

