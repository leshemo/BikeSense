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
