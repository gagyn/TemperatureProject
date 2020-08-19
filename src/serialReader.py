from typing import List
import serial
import datetime

def read_few_serial_lines() -> List[str]:
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


def write_to_file(lines):
    with open('temperatures.txt', 'a') as file:
        for l in lines:
            file.write(l + '\n')


if __name__ == '__main__':
    arduinoPort = get_arduino_port()
    ser = serial.Serial(port=arduinoPort, baudrate=19200)

    while True:
        lines = read_few_serial_lines()  # read few lines and save to file once in a while
        write_to_file(lines)
