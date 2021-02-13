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

    def validateColor(self, color):
        if color > 255:
            return 255
        elif color < 0:
            return 0
        else:
            return color

    def setBrightness(self, brightness):
        self.brightness = brightness

    def setRed(self, red):
        self.R = self.validateColor(red)

    def setGreen(self, green):
        self.G = self.validateColor(green)

    def setBlue(self, blue):
        self.B = self.validateColor(blue)

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

    def getRGB(self, colorToDecode):
        if colorToDecode[0] == '#':
            return ImageColor.getrgb(colorToDecode)
        else:
            return list(map(int, colorToDecode.split(",")))

    def inputMode(self):
        print("Enter hex color or RGB values (separated by commas and no brackets):")
        while True:
            userInput = input()

            if userInput == 'c':
                return

            rgbValues = self.getRGB(userInput)
            self.setAllColors(rgbValues[0], rgbValues[1], rgbValues[2])

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

            time.sleep(0.01)
            self.updateColorsForAllChannels()

    def fade(self, firstColor, secondColor):
        oldRed = firstColor[0]
        oldGreen = firstColor[1]
        oldBlue = firstColor[2]
        differenceR = firstColor[0] - secondColor[0]
        differenceG = firstColor[1] - secondColor[1]
        differenceB = firstColor[2] - secondColor[2]
        # print(differenceR)
        # print(differenceG)
        # print(differenceB)
        # print(max([abs(differenceB), abs(differenceG), abs(differenceR)]))
        maxDifference = max([abs(differenceB), abs(differenceG), abs(differenceR)])
        stepsRed = abs(maxDifference/differenceR)
        stepsGreen = abs(maxDifference/differenceG)
        stepsBlue = abs(maxDifference/differenceB)

        for i in range(maxDifference):
            newRed = oldRed + round(differenceR / stepsRed)
            newGreen = oldGreen + round(differenceG / stepsGreen)
            newBlue = oldBlue + round(differenceB / stepsBlue)

            oldRed = newRed
            oldGreen = newGreen
            oldBlue = newBlue
            print(newRed, end=", ")
            print(newGreen, end=", ")
            print(newBlue)
            self.setAllColors(newRed, newGreen, newBlue)
            time.sleep(0.1)

    def fadeMode(self):
        # firstColor = self.getRGB(input("input fist color (hex or rgb separated by commas)"))
        # secondColor = self.getRGB(input("input fist color (hex or rgb separated by commas)"))
        firstColor = self.getRGB('#1ED760')
        secondColor = self.getRGB('#FCF84A')
        self.fade(firstColor, secondColor)

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
                self.fadeMode()
                printInstructions = True

            elif mode == 'c' and not self.abort:
                self.stop()

            time.sleep(0.01)

    def run(self):
        while not self.abort:
            self.updateColorsForAllChannels()
            time.sleep(0.01)
        self.pi.stop()


    def stop(self):
        print("aboring...")
        self.setAllColors(0, 0, 0)
        time.sleep(0.2)
        self.abort = True

    def setPWMForChannel(self, channel, channelBrightness):
        realBrightness = int(int(self.brightness) * (float(channelBrightness) / 255.0))
        self.pi.set_PWM_dutycycle(channel, realBrightness)

    def updateColorsForAllChannels(self):
        try:
            self.setPWMForChannel(self.RED_PIN, self.R)
            self.setPWMForChannel(self.GREEN_PIN, self.G)
            self.setPWMForChannel(self.BLUE_PIN, self.B)
        except TypeError:
            print(self.R)
            print(self.G)
            print(self.B)


rgb = RGBController(13, 26, 19)
try:
    # uncomment this if you wish to test whether the pins are set correctly
    # rgb.testAllChannels()
    _thread.start_new_thread(rgb.listen, ())
    rgb.run()

except KeyboardInterrupt:
    rgb.stop()