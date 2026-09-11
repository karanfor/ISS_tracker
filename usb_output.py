# device has COM3 and COM4 ports
import serial
import time
import pandas as pd

currentTime = time.time()
minDifference = currentTime
closestTime = 0
# csv format will have column headers for ease of access which will be "timestamp", "pan", "tilt"
df = pd.read_csv("servo_angles.csv") #df stands for dataframe
timestamps = df["timestamp"]
for timestamp in timestamps: #this for loop searches for the closest timestamp in the CSV file to the current time
    timeDifference = timestamp - currentTime
    timeDifference = abs(timeDifference)
    if timeDifference < minDifference
        minDifference = timeDifference
        closestTime = timestamp
firstPosition = df[df["timestamp"] == closestTime] # help why is there a df inside a df what the
    



#usb = serial.Serial('COM3', 9600)
#usb.write("pan", "tilt")

