import RPi.GPIO as GPIO
import time

##HARDWARE
GPIO.setmode(GPIO.BOARD)

TRIG_PIN = 12
ECHO_PIN = 16
BUZZER_PIN = 18

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

buzzer = GPIO.PWM(BUZZER_PIN, 440)
buzzer.start(0)

##MAIN
try:
    while True:
        GPIO.output(TRIG_PIN, False)
        time.sleep(0.5)

        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)

        pulse_start = time.time()
        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()

        pulse_end = time.time()
        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print("Distance:", distance, "cm")

        if distance <= 50:
            volume = (50 - distance) / 50 * 100
            buzzer.ChangeDutyCycle(volume)
        else:
            buzzer.ChangeDutyCycle(0)

except KeyboardInterrupt:
    GPIO.cleanup()
    buzzer.stop()
