import time
import board
import digitalio
import busio
import adafruit_lis3dh
import logging 
import numpy as np 
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation


from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient 

select = 0
xs = []
x_array = []
y_array = []
z_array = []
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

    # Loop forever printing accelerometer values
    
    # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
    # z axis values.  Divide them by 9.806 to convert to Gs.
    x, y, z = [
         value  for value in lis3dh.acceleration
    ]

    
    x_array.append(x)
    y_array.append(y)
    z_array.append(z)
    

    return x,y,z

def payload_report(self, params, packet):
    print("----- New Payload -----")
    print("Topic: ", packet.topic)
    print("Message: ", packet.payload)
    print("-----------------------")
    
def data_processing(x_array,y_array ,z_array):
    median= ([np.median(x_array),np.median(y_array),np.median(z_array)])
    mean = ([np.mean(x_array),np.mean(y_array),np.mean(z_array)])
    
    

    return median,mean
    

def pub_sub(x_avg,y_avg,z_avg,x):
    
    #attach the on_connect() callback function defined above to the mqtt client
    #AWSIoTMQTTClient.on_connect = on_connect
    myMQTTClient = AWSIoTMQTTClient("raspberryPiHome")
    myMQTTClient.configureEndpoint("a2coyrat7ns928-ats.iot.us-west-2.amazonaws.com", 8883)
    path = '/home/pi/ee250_final_project/'
    myMQTTClient.configureCredentials("{}root-ca.pem".format(path), "{}cloud.pem.key".format(path), "{}cloud.pem.crt".format(path))


    myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec

    myMQTTClient.connect()
    myMQTTClient.subscribe("rpi-mahjoub/acc", 1, payload_report)

    #publish a float
    myMQTTClient.publish("rpi-mahjoub/acc", str(x),0)
    #myMQTTClient.publish("rpi-mahjoub/acc", str(y) , 0)
    #myMQTTClient.publish("rpi-mahjoub/acc", str(z), 0)

if __name__ == '__main__':
    
    time.sleep(1)
    while (True):

        x, y, z = read_data()
        '''
            #attach the on_connect() callback function defined above to the mqtt client
        #AWSIoTMQTTClient.on_connect = on_connect
        myMQTTClient = AWSIoTMQTTClient("raspberryPiHome")
        myMQTTClient.configureEndpoint("a2coyrat7ns928-ats.iot.us-east-1.amazonaws.com", 8883)
        path = '/home/pi/ee250_final_project/'
        myMQTTClient.configureCredentials("{}root-ca.pem".format(path), "{}cloud.pem.key".format(path), "{}cloud.pem.crt".format(path))


        myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
        myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
        myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
        myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec

        myMQTTClient.connect()
        myMQTTClient.subscribe("rpi-mahjoub/acc", 1, payload_report)

        #publish a float
        myMQTTClient.publish("rpi-mahjoub/acc", str(x),0)
        #myMQTTClient.publish("rpi-mahjoub/acc", str(y) , 0)
        #myMQTTClient.publish("rpi-mahjoub/acc", str(z), 0)
        
        
        '''
        x_avg = mean[0]
        y_avg  = mean[1]
        z_avg  = mean[2]
        '''
        #print (x_avg,y_avg,z_avg)

        
   
        #pub_sub(x_avg,y_avg,z_avg,5)
        time.sleep(0.25)




