import RPi.GPIO as GPIO
import time
import os

# GPIO 핀 번호 설정
LED_PIN = 16
BUTTON_PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

def shutdown(channel):
    print("버튼이 눌렸습니다. 라즈베리 파이를 종료합니다.")
    GPIO.cleanup()
    os.system("sudo shutdown -h now")

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=shutdown, bouncetime=200)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
