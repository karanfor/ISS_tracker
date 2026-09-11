import urllib.request
import json
import time
from datetime import datetime
import csv
import math
from math import cos, sin, radians 
import numpy as np

#   // 2: use formula to convert lat and long to x,y,z space :)
#   // 3: add altitude info to show exact ISS position :)
#   // 4: draw a vector from our point to ISS :)
#   // 5: create triangle using the vector, shadow of the vector on tangent plane to us on the sphere, and a normal to that plane which passes through the ISS
#   // 6: use trig to determine tilt angle
#   // 7: find angle between shadow of vector on tangent plane and a vector on the tangent plane pointing north
#   // 8: output as pan and tilt angle

#(-0.35799432,-0.56980847,0.73970155) is our point

def vector_length(vector):
    length = np.sqrt(np.sum(np.square(vector)))
    return length
def vector_angle(vector_a, vector_b):
    angle = math.acos(radians((np.sum(vector_a * vector_b))/(vector_length(vector_a) * vector_length(vector_b)))) #using the dot product equation to find angle
    return angle

def convert_lat_lon_to_servo_angles(lat: float, lon: float, alt: float) -> tuple[float, float]:
    vector_me = np.array([-0.35799432],[-0.56980847],[0.73970155])
    vector_U = np.array([(cos(radians(lat))) * cos(radians(lon))]  ,  [sin(radians(lon)) * cos(radians(lat))]  ,  [sin(radians(lat))]) #U is a vector from origin to the spot of earth underneath the ISS

    vector_U_length = np.sqrt(np.sum(np.square(vector_U))) #check with print if code throws error
    unit_vector_U = vector_U / vector_U_length #self explanatory I think

    earth_radius = 6,371 #an average (in kilometers)
    ISS_radius = (earth_radius + alt) / earth_radius #getting total length and scaling to my scale of 1 = earth_radius

    vector_ISS = unit_vector_U * ISS_radius #vector_ISS is a vector from the origin to the ISS, upgrading U from ground to exact position
    vector_C = vector_ISS - vector_me #vector_C points from our position to the ISS

    tilt_angle = (np.pi / 2) - vector_angle(vector_C, vector_me) #something to keep in mind, zero is horizontal and lower is negative degrees

    vector_L = list([0],[0],[1]) - vector_me #vector_L points from our position to the north pole
    vector_mynorth = np.cross(np.cross(vector_me, vector_L), vector_me) #mynorth is a vector tangent to the earth that 'points' north from our position
    vector_myISS = np.cross(np.cross(vector_me, vector_C), vector_me) #myISS is a vector tangent to the earth that 'points' towards the ISS from our position
    pan_angle = vector_angle(vector_mynorth, vector_myISS) #north is zero

    return pan_angle, tilt_angle

exit()

ang1, ang2 = convert_lat_lon_to_servo_angles(3.5, 4.5)
print(ang1, ang2)

ang1, ang2 = convert_lat_lon_to_servo_angles(3.5, 4.5)
print(ang1, ang2)

# get pass times with https://www.amsat.org/track/ and enter 47.705998 N, 122.139968 W and 16 meters for 60 acres location

print("input your start and end time in UTC when prompted")

start_time_input = input("start year/month/day hour:minute:second: ")
start_utc_time = datetime.strptime(start_time_input, "%Y/%m/%d %H:%M:%S")
time_start = int((start_utc_time - datetime(1970, 1, 1)).total_seconds())

end_time_input = input("end year/month/day hour:minute:second: ")
end_utc_time = datetime.strptime(end_time_input, "%Y/%m/%d %H:%M:%S")
time_end = int((end_utc_time - datetime(1970, 1, 1)).total_seconds())

# takes start and end times and converts to epoch

#print(time_start)
#print(time_end)

all_times = list(range(time_start, time_end, 2)) #range(start,stop,step)  change number if want to change frequency of data

# creates a list of times between the start and end times

length = len(all_times)
#print (length)

# sees how many entries in the list
print(all_times)

with open('ISS_position.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    header = ["timestamp","latitude","longitude","altitude"]
    writer.writerow(header)

    for t in all_times:
        print(t)
        with urllib.request.urlopen(f"https://api.wheretheiss.at/v1/satellites/25544/positions?timestamps={t}&units=kilometers") as url:
            data = json.load(url)
            data = data[0]
            csv_entry = [data["timestamp"],data["latitude"],data["longitude"],data["altitude"]]
            print(data["timestamp"],data["latitude"],data["longitude"],data["altitude"]) #just as test
        writer.writerow(csv_entry)
        time.sleep(0.01) #respecting request limit on wheretheissat with buffer :)

# requests data from each timestamp in list and puts into ISS_position.csv

# 2026/9/11 2:49:52
# 2026/9/11 2:59:52

# 2026/9/12 6:52:34
# 2026/9/12 7:3:23




