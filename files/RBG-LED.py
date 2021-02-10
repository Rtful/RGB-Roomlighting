#!/usr/bin/python3
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

# GPIO-Pins mit entsprechender Led-Farbe
rot = 33
gruen = 37
blau = 35
GPIO.setup(rot, GPIO.OUT)
GPIO.setup(gruen, GPIO.OUT)
GPIO.setup(blau, GPIO.OUT)

# Funktion, um alle genutzten Pins auf Low zu schalten
def all_off():
    GPIO.output(rot, False)
    GPIO.output(gruen, False)
    GPIO.output(blau, False)
    return

# Modusauswahl
auswahl = eval(input ("[1] Mischen      [2] Auto \n"))

# PWM festlegen mit Frequenz 255hz
pwm_r=GPIO.PWM(rot,255)
pwm_g=GPIO.PWM(gruen,255)
pwm_b=GPIO.PWM(blau,255)

# PWM starten mit Frequenz 0 % Duty Cycle
pwm_r.start(0)
pwm_g.start(0)
pwm_b.start(0)

try:
    if auswahl == 1:
       while True:
           # Werte von 0- 100 zulässig
           dcr= eval(input("Rotanteil [0-100]: \n" ))
           dcb= eval(input("Blauanteil [0-100]: \n" ))
           dcg= eval(input("Gruenanteil [0-100]: \n" ))

           # Duty Cycle entsprechend Eingabe ändern
           pwm_g.ChangeDutyCycle(dcg)
           pwm_b.ChangeDutyCycle(dcb)
           pwm_r.ChangeDutyCycle(dcr)
 
    # Farbwechsel bei Modus "Auto"
    if auswahl == 2:
        pwm_g.ChangeDutyCycle(100)
        pwm_b.ChangeDutyCycle(100)
        pwm_r.ChangeDutyCycle(100)
        sleep(0.5)
        pwm_g.ChangeDutyCycle(0)
        pwm_b.ChangeDutyCycle(0)
        pwm_r.ChangeDutyCycle(0)
        sleep(0.5)
        pwm_g.ChangeDutyCycle(100)
        pwm_b.ChangeDutyCycle(100)
        pwm_r.ChangeDutyCycle(100)
        sleep(0.5)
        pwm_g.ChangeDutyCycle(0)
        pwm_b.ChangeDutyCycle(0)
        pwm_r.ChangeDutyCycle(0)
        sleep(0.5)
        pwm_g.ChangeDutyCycle(100)
        pwm_b.ChangeDutyCycle(0)
        pwm_r.ChangeDutyCycle(0)
        sleep(1)
        pwm_g.ChangeDutyCycle(0)
        pwm_b.ChangeDutyCycle(100)
        pwm_r.ChangeDutyCycle(0)
        sleep(1)
        pwm_g.ChangeDutyCycle(0)
        pwm_b.ChangeDutyCycle(0)
        pwm_r.ChangeDutyCycle(100)
        sleep(1)
        for a in range(100):
            pwm_g.ChangeDutyCycle(a)
            pwm_b.ChangeDutyCycle(0)
            pwm_r.ChangeDutyCycle(0)
            sleep (0.05)
            if a == 99:
                while True:                                    
                    pwm_g.ChangeDutyCycle(99)
                    pwm_r.ChangeDutyCycle(0)   
                    for i in range(100):
                        pwm_b.ChangeDutyCycle(i)
                        sleep (0.05)

                    pwm_b.ChangeDutyCycle(99)
                    pwm_r.ChangeDutyCycle(0)                    
                    for i in range(99, 0, -1):
                        pwm_g.ChangeDutyCycle(i)
                        sleep(0.05)

                    pwm_g.ChangeDutyCycle(0)
                    pwm_b.ChangeDutyCycle(99)
                    for i in range(100):
                        pwm_r.ChangeDutyCycle(i) 
                        sleep(0.05)

                    pwm_r.ChangeDutyCycle(99)
                    pwm_g.ChangeDutyCycle(0)                      
                    for i in range(99, 0, -1):
                        pwm_b.ChangeDutyCycle(i)
                        sleep(0.05)

                    pwm_r.ChangeDutyCycle(99) 
                    pwm_b.ChangeDutyCycle(0)
                    for i in range(100):
                        pwm_g.ChangeDutyCycle(i)
                        sleep(0.05)

                    pwm_g.ChangeDutyCycle(99)
                    pwm_b.ChangeDutyCycle(0)
                    for i in range(99, 0, -1):
                        pwm_r.ChangeDutyCycle(i) 
                        sleep(0.05)
                        
                                                                                                                  
                                  
except KeyboardInterrupt:
    all_off()
