import sys
from datetime import time as t
from datetime import datetime
import math
import joblib
import requests



class BikeCountLambda:
    def __init__(self):
        self.capacities = self.getStationCapacity()

    def predictBikeCount(self, stationId: int, minutes: float, temp: float, day: int, month: int, day_of_week: int, model, verbose:bool = False) -> int:
        y_pred = model.predict([[stationId, minutes, temp, day, month, day_of_week]])
        if (verbose):
            print(f"\nThe {desired_model} model predicts that station {stationId} at minutes {minutes} and temp {temp} will have {y_pred[0]} bikes")
        return y_pred[0]

    def getStationCapacity(self):
      response = requests.get("https://gbfs.bluebikes.com/gbfs/en/station_information.json")
      response = response.json()
      out = {}
      for station in response['data']['stations']:
           out[station['station_id']] = station['capacity'] 
      return out


    def heuristic(self, startStationId, endStationId, minutes, time, temp,day, month, day_of_week, model):
        bikes = self.predictBikeCount(startStationId, minutes, temp, day, month, day_of_week, model, False)
        try:
            stationCapacity = self.capacities[str(endStationId)]
        except:
            err = Exception("Station Id incorrect. Please try again.")
            raise SystemExit(err)
            
        spaces = stationCapacity - self.predictBikeCount(endStationId, (minutes + time), temp, day, month, day_of_week, model, False)
        if bikes == 0 or spaces == 0:
            return -sys.maxsize
        else:
            return self.curve(spaces) + self.curve(bikes)

    def curve(self, num):
        return 10 * math.log(num**3 + 1)


    def initiateBikeQuery(self, startStation: int, endStation: int, lengthOfTrip: int, temp: int):
        now = datetime.now()
        minutes = (60 * now.hour) + now.minute
        day = now.day
        month = now.month
        day_of_week = now.weekday()
        leave = (0, minutes)
        model = joblib.load("knn_model.pkl")

        for i in range(30):     # Evaluate the next 30 minutes
            heur = self.heuristic(startStation, endStation, minutes, lengthOfTrip, temp, day, month, day_of_week, model)
            if (heur > leave[0]):
                leave = (heur, minutes)
            minutes = minutes + 1
        
        minute = leave[1] % 60
        hour = int((leave[1] - minute) / 60)
        if hour >= 24:
            hour = hour - 24
        print("\nThe best moment to leave would be at", t(hour, minute, 0).strftime("%H:%M"))
        return {'hour': hour, 'minute': minute}