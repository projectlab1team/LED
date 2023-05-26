
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.clenup()

GPIO_LED_R=18
GPIO_LED_B=19
GPIO_LED_W=20

GPIO.setup(GPIO_LED_R,GPIO.OUT)
GPIO.setup(GPIO_LED_B,GPIO.OUT)
GPIO.setup(GPIO_LED_W,GPIO.OUT)

save1=0
save2=0

def main():
    while True:
        if save1<25:
            if(save2 > 30):
               GPIO.output(GPIO_LED_R,GPIO.HIGH)
               GPIO.output(GPIO_LED_B,GPIO.LOW)
               GPIO.output(GPIO_LED_W,GPIO.LOW)
            else :
               GPIO.output(GPIO_LED_B,GPIO.HIGH)
               GPIO.output(GPIO_LED_R,GPIO.LOW)
               GPIO.output(GPIO_LED_W,GPIO.LOW)
        elif save1>=25:
            GPIO.output(GPIO_LED_B,GPIO.LOW)
            GPIO.output(GPIO_LED_R,GPIO.LOW)
            GPIO.output(GPIO_LED_W,GPIO.HIGH)
        time.sleep(1)


def on_connect(client, userdata, rc):
    client.subscribe("environment/temperature")
    client.subscribe("environment/ultrasonic")

def on_message(client,userdata,msg):
    global save1
    global save2

    if(msg.topic == "evnrionment/temperature"):
        save1=int(msg.payload)
    if(msg.topic == "evnrionment/ultrasonic"):
        save2=float(msg.payload)


save3=threading.Thread(target=main)
client=mqtt.Client("pub client")
client=mqtt.Client("pub2 client")
client.on_connect=on_connect
client.on_message = on_message
clinet.connect("127.0.0.0",1883,30)

save3.start()
client.loop_forever()