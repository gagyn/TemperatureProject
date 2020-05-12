from typing import List
import serial
import datetime

def readFewLines() -> List[str]:
    lines = []
    for i in range(5):
        ser_bytes = ser.readline()
        try:
                decoded_bytes = ser_bytes[:-2].decode("utf-8")
                dt = datetime.datetime.now()
                time = dt.strftime('%Y-%m-%d %H:%M:%S')
                tempWithTime = time + ': ' + decoded_bytes 
                lines.append(tempWithTime)
                print(tempWithTime)
        except:
            continue
    return lines

def writeToFile(lines):
    with open('temperatures.txt', 'a') as file:
        for l in lines:
            file.write(l + '\n')

if __name__ == '__main__':
    arduinoPort = ''
    with open('config.txt') as configFile:
        arduinoPort = configFile.readline()

    ser = serial.Serial(port=arduinoPort, baudrate=19200)

    while True:
        lines = readFewLines() # read few lines and save to file once in a while
        writeToFile(lines)