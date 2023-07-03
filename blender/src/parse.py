import csv
from pyquaternion import Quaternion
from astropy.time import Time
from datetime import datetime

def csvread(filename, remove_header=True):
    # Open the CSV file and read all rows
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        if remove_header:
            rows.pop(0)
    return rows


def parse_data():
    rows = csvread('quaternions.csv')
    # Construct the times (as Julian dates) and quaternions tuples, ignoring incomplete or empty rows
    times = tuple((Time(datetime.strptime(row[0], '%d %b %Y %H:%M:%S.%f'), scale='utc').jd) for row in rows)
    quaternions = tuple(Quaternion(float(row[4]), float(row[2]), float(row[3]), float(row[1])) for row in rows)

    rows = csvread('area.csv')
    areas = tuple(float(row[1]) for row in rows)

    # rows = csvread('power.csv')
    # powers = tuple(float(row[1]) for row in rows)
    powers = tuple()

    rows = csvread('position-velocity.csv')
    positions = tuple((float(row[1]), float(row[2]), float(row[3])) for row in rows)
    velocities = tuple((float(row[4]), float(row[5]), float(row[6])) for row in rows)

    return times, quaternions, areas, powers, positions, velocities