import serial
import datetime

def readFewLines():
    lines = []
    for i in range(5):
        ser_bytes = ser.readline()
        try:
                decoded_bytes = ser_bytes[:-2].decode("utf-8")
                lines.append(decoded_bytes)
        except:
            continue
    return lines

def writeToFile(lines):
    with open('temperatures.txt', 'a') as file:
        for l in lines:
            file.write(str(datetime.datetime.now()) + ' ' + l + '\n')

ser = serial.Serial(port='COM3', baudrate=19200)
#ser.flushInput()
while True:
    lines = readFewLines()
    writeToFile(lines)