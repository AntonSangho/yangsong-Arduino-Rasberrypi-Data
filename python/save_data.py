import serial
from datetime import datetime

# Adjust the serial port and baud rate accordingly
ser = serial.Serial('/dev/ttyUSB0', 9600)

file_path = 'sensor_data.csv'

# Open the file in append mode
with open(file_path, 'a') as file:
    try:
        while True:
            # Get the current date and time with seconds
            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Read data from the serial port
            data = ser.readline().decode('utf-8').strip()

            # Print data to console
            print(current_datetime, data)

            # Write date, time, seconds, data, and separator to the file
            file.write(current_datetime + ',' + data + '\n')

    except KeyboardInterrupt:
        print("Keyboard interrupt. Closing file and exiting.")
        file.close()
        ser.close()

