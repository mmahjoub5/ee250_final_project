import time
import board
import digitalio
import busio
import adafruit_lis3dh
import logging 
import numpy as np 
#import matplotlib as plt 


from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient 

select = 0
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
         value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration
    ]
    
    x_array.append(x)
    y_array.append(y)
    z_array.append(z)
    print(x_array)
    print(y_array)
    print(z_array)




    #print("x = %0.3f G, y = %0.3f G, z = %0.3f G" % (x, y, z))
    # Sall delay to keep things responsive but give time for interrupt processing.
    if lis3dh.shake(shake_threshold=15):
        print("Shaken!")
        new = 1
        select.update(new)
        time.sleep(0.1)

        return 'shaken'


    return x,y,z

def payload_report(self, params, packet):
    print("----- New Payload -----")
    print("Topic: ", packet.topic)
    print("Message: ", packet.payload)
    print("-----------------------")
    
def data_processing(x_array,y_array ,z_array):
    median= ([np.median(x_array),np.median(y_array),np.median(z_array)])
    mean = ([np.mean(x_array),np.mean(y_array),np.mean(z_array)])
    print(mean)
    print(median)

    return median,mean
    
if __name__ == '__main__':
    '''
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
    myMQTTClient.subscribe("home/acc_value", 1, payload_report)
    '''
    
    time.sleep(1)
    while (True):

        x, y, z = read_data()
        print(data_processing(x_array,y_array ,z_array))
        #publish a float
        #myMQTTClient.publish("rpi-mahjoub/acc", str(x,y,z),0)
        #myMQTTClient.publish("rpi-mahjoub/acc", str(y) , 0)
        #myMQTTClient.publish("rpi-mahjoub/acc", str(z), 0)

        time.sleep(1)




