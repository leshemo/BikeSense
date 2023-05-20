import sys
from BikeCountPredictor import BikeCountPredictor
from datetime import time as t
from datetime import datetime
import math
from DataCleaning import getStationCapacity


class BikeCountController:
    def __init__(self):
        self.oracle = BikeCountPredictor()
        self.capacities = getStationCapacity()


    def heuristic(self, startStationId, endStationId, minutes, time, temp,day, month, day_of_week, model = 'linear'):
        bikes = self.oracle.predictBikeCount(startStationId, minutes, temp, day, month, day_of_week, model, False)
        stationCapacity = self.capacities[str(endStationId)]
        spaces = stationCapacity - self.oracle.predictBikeCount(endStationId, (minutes + time), temp, day, month, day_of_week, model, False)
        if bikes == 0 or spaces == 0:
            return -sys.maxsize
        else:
            return self.curve(spaces) + self.curve(bikes)

    def curve(self, num):
        return 10 * math.log(num**3 + 1)


    def initiateBikeQuery(self, startStation: int, endStation: int, lengthOfTrip: int, temp: int):
        # startStation = int(input("Please enter the start station: "))
        # endStation = int(input("Please enter the end station: "))
        # time = int(input("Please enter the length of time for the trip in minutes: "))
        # temp = int(input("What is the temperature at the moment in fahrenheit? "))
        now = datetime.now()
        minutes = (60 * now.hour) + now.minute
        day = now.day
        month = now.month
        day_of_week = now.weekday()
        leave = (0, minutes)

        for i in range(30):     # Evaluate the next 30 minutes
            heur = self.heuristic(startStation, endStation, minutes, lengthOfTrip, temp, day, month, day_of_week)
            if (heur > leave[0]):
                leave = (heur, minutes)
            minutes = minutes + 1
        minute = minutes % 60
        hour = int((minutes - minute) / 60)
        if hour >= 24:
            hour = hour - 24
        print("\nThe best moment to leave would be at", t(hour, minute, 0).strftime("%H:%M"))
        return {'hour': hour, 'minute': minute}
        
def main():
    # Prompts for the query
    BCC = BikeCountController()
    BCC.initiateBikeQuery()



# if __name__ == "__main__":
#     main()

BikeCountController().initiateBikeQuery(417,12,20,50)
