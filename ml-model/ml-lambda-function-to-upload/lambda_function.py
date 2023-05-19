import json
from BikeCountController import BikeCountController

def lambda_handler(event, context):
    #pass in an event containing all the parameters for the ml stuff
    
    #call ml controller
    output = BikeCountController().initiateBikeQuery(event.get('startStation'), event.get('endStation'), event.get('lengthOfTrip'), event.get('temp'))
    
    #return response
    return {
        'statusCode': 200,
        'hour' : output['hour'],
        'minute' : output['minute']
    }


test = {
  "startStation": 12,
  "endStation": 324,
  "lengthOfTrip": 15,
  "temp": 82
}

lambda_handler(test, None)