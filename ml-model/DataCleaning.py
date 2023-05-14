import pandas as pd
from pandas import to_datetime
import seaborn as sns
import matplotlib.pyplot as plti
import requests

#"C:\Users\leshe\Documents\GitHub\BlueBike-AI-Copy"
#balancing first
def rebalance(year_month):
    df = pd.read_csv(r"C:\Users\leshe\Documents\GitHub\BlueBike-AI-Copy\src\data\%s-bluebikes-tripdata.csv" % year_month,
            usecols=['starttime','start station id',
                    'stoptime','end station id', 'bikeid'],
            parse_dates=['starttime','stoptime'])

    dfbike=df.sort_values(by=['bikeid','starttime'])
    dfbike.head(10)

    offset = pd.DataFrame({'starttime': pd.to_datetime('2010-09-01'),
    'start station id':0,'stoptime': pd.to_datetime('2010-09-01'),
    'end station id':0,'bikeid':0},index=[0])

    dfbike1 = pd.concat([offset,dfbike]).reset_index(drop=True)
    dfbike2 = pd.concat([dfbike,offset]).reset_index(drop=True)

    dfbike=pd.concat ([dfbike1[['bikeid','stoptime','end station id']]\
                ,dfbike2[['bikeid','starttime','start station id']] ],\
                axis=1 )
    dfbike.head()

    dfbike.columns=['bikeid1','starttime','start station id',\
                    'bikeid2','stoptime','end station id']
    dfrebal = dfbike[['starttime','start station id',\
                    'stoptime','end station id']].\
            loc[(dfbike.bikeid1==dfbike.bikeid2) & \
            (dfbike['start station id'] != dfbike['end station id']) ]
    dfrebal.reset_index(drop=True, inplace=True)
    dfrebal
    dfrebal.to_parquet(r"C:\Users\leshe\Documents\GitHub\BlueBike-AI-Copy\src\data\%s-bluebike-reblance.parquet" % year_month)
    print("Rebalancing done for %s!" % year_month)

#create csv for number of bikes at particular station, using the rebalanced parquet file
def bikeAvail(year_month):
    
    df = pd.read_csv(r"C:\Users\leshe\Documents\GitHub\BlueBike-AI-Copy\src\data\%s-bluebikes-tripdata.csv" % year_month,
            usecols=['starttime','start station id',
                    'stoptime','end station id'],
            parse_dates=['starttime','stoptime'])
    dfrebal = pd.read_parquet (r"C:\Users\leshe\Documents\GitHub\BlueBike-AI-Copy\src\data\%s-bluebike-reblance.parquet" % year_month)
    df = pd.concat([df,dfrebal])
    df.reset_index(drop=True, inplace=True)

    dfs=df[['starttime','start station id']].assign(act=-1)
    dfe=df[['stoptime','end station id']].assign(act=1)
    dfs.columns=['docktime','stationid','act']
    dfe.columns=['docktime','stationid','act']
    dfse=pd.concat([dfs,dfe])


    dfse.sort_values(by=['docktime'], inplace=True) 
    dfse.reset_index(drop=True, inplace=True) 
    dfOut = pd.DataFrame()

    unique_station_id = dfse.stationid.unique()
    for station_id in unique_station_id:
        dfStation = dfse.loc[(dfse.stationid==station_id) ]
        dfStation.reset_index(drop=True, inplace=True)


        dfStation = dfStation.assign(num_bikes = dfStation.act.cumsum())
        dfStation.at[0, 'act'] += abs(dfStation.act.cumsum().min())
        dfStation = dfStation.assign(num_bikes = dfStation.act.cumsum())
        dfStation['minutes'] = 0
        dfStation = dfStation.assign(minutes =  dfStation['docktime'].dt.hour * 60 + dfStation['docktime'].dt.minute + round(dfStation['docktime'].dt.second / 60, 3))
        dfStation = dfStation.drop('act', axis = 1)
        dfOut = pd.concat([dfOut, dfStation], ignore_index=True)
        
    
    print("Dock data generated for %s" % year_month)
    attachClimateData(dfOut)


#clean climate data csv to include only daily average temp in boston over the year we're looking at. Only needs to be run once.
def cleanClimateData():
        dfClimate = pd.read_csv(r"C:\Users\leshe\Documents\GitHub\BlueBike-AI-Copy\src\data\2022-2023-climate-data.csv",
                usecols=['DATE','DailyAverageDryBulbTemperature'],
                parse_dates=['DATE'])
        dfClimate = dfClimate.dropna()
        dfClimate.reset_index(inplace=True)
        dfClimate.to_csv('./data/2022-2023-climate-data-processed.csv')
        print(dfClimate.head(10))
        print(dfClimate.index)

#merge the climate data and the dock data so that every day has an average temperature.
def attachClimateData(df2):
        df1 = pd.read_csv(r"C:\Users\leshe\Documents\GitHub\BlueBike-AI-Copy\src\data\2022-2023-climate-data-processed.csv",
                usecols=['DATE','DailyAverageDryBulbTemperature'],
                parse_dates=['DATE'])
        df1.rename(columns = {'DATE': 'docktime'}, inplace = True)
        df1.docktime = df1.docktime.apply(lambda x: x.date())
        df2.docktime = df2.docktime.apply(lambda x: x.date())

        merged_df = pd.merge(df2, df1, how='left', on= 'docktime')
        merged_df.rename(columns = {'docktime': 'day'}, inplace = True)
        merged_df.rename(columns = {'DailyAverageDryBulbTemperature': 'average_temp'}, inplace = True)
        merged_df.to_csv('./data/2022-2023-dock-data-updated.csv', mode='a', header=False)
        print("Average temp attached to dock data!")

def addMoreParams():
       dfA = pd.read_csv(r"C:\Users\leshe\Documents\GitHub\BlueBike-AI-Copy\src\data\2022-2023-dock-data-updated.csv",
                         usecols=['day', 'stationid', 'num_bikes', 'minutes', 'average_temp'],
                        parse_dates=['day'])
       #rename day column to date
       dfA.rename(columns = {'day': 'date'}, inplace = True)
#        #add day of week
       dfA['day'] = dfA.date.apply(lambda x: x.date().day)
       dfA['month'] = dfA.date.apply(lambda x: x.date().month)


       #add weekday (as in Monday, Tuesday, etc.)
       dfA['day_of_week'] = dfA.date.apply(lambda x: x.weekday())
       dfA = dfA.sort_values(by=['stationid', 'date'])

       dfA.to_csv('./data/2022-2023-dock-data-updated-fo-real.csv', index=False)

def doTheThing():
        array_of_year_months = ["202302", "202301", "202212", "202211", "202210", "202209", "202208", "202207", "202206", "202205", "202204"]
        start_station = "Boylston St at Jersey St"
        end_station = "Ruggles T Stop - Columbus Ave at Melnea Cass Blvd"
        for year_month in array_of_year_months:
                rebalance(year_month)
                bikeAvail(year_month)




def getStationCapacity():
      response = requests.get("https://gbfs.bluebikes.com/gbfs/en/station_information.json")
      response = response.json()
      out = {}
      for station in response['data']['stations']:
           out[station['station_id']] = station['capacity'] 
      return out

getStationCapacity()