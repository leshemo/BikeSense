import json
from BikeCountLambda import BikeCountLambda
import datetime


#generate 
def lambda_handler(event, context):
    output = BikeCountLambda().initiateBikeQuery(event.get('startStation'), event.get('endStation'), event.get('lengthOfTrip'), event.get('temp'))
    
    #return response
    return {
        'statusCode': 200,
        'hour' : output['hour'],
        'minute' : output['minute']
    }


lambda_handler({'startStation': 342, 'endStation': 12, 'lengthOfTrip': 10, 'temp': 50}, None)  # 1: 1, 2, 10, 50