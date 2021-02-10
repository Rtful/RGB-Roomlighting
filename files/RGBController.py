# import os
# import sys
# import termios
# import tty
import pigpio
import time
import _thread
from PIL import ImageColor

class RGBController:

    abort = False
    pause = False
    R = 0
    G = 0
    B = 0

    def __init__(self, redPin = 17, greenPin = 22, bluePin = 24, brightness = 255):
        self.RED_PIN = redPin
        self.GREEN_PIN = greenPin
        self.BLUE_PIN = bluePin
        self.brightness = brightness
        self.pi = pigpio.pi()

    def setBrightness(self, brightness):
        self.brightness = brightness

    def setRed(self, red):
        self.R = red

    def setGreen(self, green):
        self.G = green

    def setBlue(self, blue):
        self.B = blue

    def setAllColors(self, R, G, B):
        self.setRed(R)
        self.setGreen(G)
        self.setBlue(B)

    def setHex(self, hex):
        rgbValues = ImageColor.getrgb(hex)
        self.setAllColors(rgbValues[0], rgbValues[1], rgbValues[2])

    def testAllChannels(self):
        print("Testing all Channels")
        self.setAllColors(255, 0, 0)
        self.updateColorsForAllChannels()
        print("RED")
        time.sleep(0.5)
        self.setAllColors(0, 255, 0)
        self.updateColorsForAllChannels()
        print("GREEN")
        time.sleep(0.5)
        self.setAllColors(0, 0, 255)
        self.updateColorsForAllChannels()
        print("BLUE")
        time.sleep(0.5)
        self.setAllColors(255, 255, 255)
        self.updateColorsForAllChannels()
        print("WHITE")

    def inputMode(self):
        print("Enter hex color or RGB values (separated with a space and no brackets):")
        while True:
            userInput = input()

            if userInput[0] == '#':
                self.setHex(userInput)

            # Commeted out bc not very functional here but might use in a fade
            # elif userInput == 'p' and not self.pause:
            #     self.pause = True
            #     print("Pausing...")
            #     self.setAllColors(0, 0, 0)
            #     time.sleep(0.1)
            #
            # elif userInput == 'r' and self.pause:
            #     self.pause = False
            #     print("Resuming...")

            elif userInput == 'c':
                return

            else:
                self.R, self.G, self.B = map(int, userInput.split())

            time.sleep(0.01)
            self.updateColorsForAllChannels()

    def listen(self):
        printInstructions = True
        while True:
            if printInstructions:
                print("Select Mode:[1] Input [2] Fade")
                printInstructions = False

            mode = input()
            if mode == '1':
                self.inputMode()
                printInstructions = True

            elif mode == '2':
                print("mode 2 was chosen")
                printInstructions = True

            elif mode == 'c' and not self.abort:
                print("aboring...")
                self.setAllColors(0, 0, 0)
                time.sleep(0.2)
                self.abort = True

            time.sleep(0.01)

    def run(self):
        while not self.abort:
            self.updateColorsForAllChannels()
            time.sleep(0.01)
        self.pi.stop()

    def setPWMForChannel(self, channel, channelBrightness):
        realBrightness = int(int(self.brightness) * (float(channelBrightness) / 255.0))
        self.pi.set_PWM_dutycycle(channel, realBrightness)

    def updateColorsForAllChannels(self):
        self.setPWMForChannel(self.RED_PIN, self.R)
        self.setPWMForChannel(self.GREEN_PIN, self.G)
        self.setPWMForChannel(self.BLUE_PIN, self.B)


rgb = RGBController(13, 26, 19)
try:
    # rgb.testAllChannels()
    _thread.start_new_thread(rgb.listen, ())
    rgb.run()

except KeyboardInterrupt:
    rgb.pi.stop()