import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import f1_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import joblib

class BikeCountPredictor:
    def __init__(self, dataFilename=r"C:\Users\leshe\Documents\GitHub\NER\bluebike-ai\src\data\2022-2023-dock-data-updated-fo-real.csv"):
        
        #initialization functions
        self.stationData = self.loadDataByStation(dataFilename)
        self.stationModels = {} # self.stationModels[stationId: int][desired_model: str] = model
        
    def loadDataByStation(self, allStationDataFilename: str) -> pd.DataFrame:
        dfAllStations = pd.read_csv(allStationDataFilename)
        dfAllStations = dfAllStations.dropna()
        return dfAllStations
    
    def existsStationData(self) -> None:
        if not self.stationData:
            raise Exception("There is no station data loaded.")
        
    def createModel(self, desired_model: str, verbose: bool = True):
        xCols = ["stationid","minutes", "average_temp","day","month","day_of_week"]
        dfX = self.stationData[xCols]
        dfY = self.stationData[["num_bikes"]]
        X_train, X_test, y_train, y_test = train_test_split(dfX.to_numpy(), dfY.to_numpy(), test_size=0.20, random_state=123)
        if (verbose): print(f"\nResults for {desired_model} model on station:")
        if desired_model == "linear":
            params = {}
            model = GridSearchCV(LinearRegression() , param_grid=params, scoring='neg_mean_squared_error',cv=5)
            model.fit(X_train, y_train)
            joblib.dump(model, './linear_model.pkl')
        elif desired_model == "knn":
            params = [{'n_neighbors': [3, 5, 7, 9],
                       'weights': ['uniform', 'distance']}]
            model = GridSearchCV(KNeighborsRegressor() , param_grid=params,scoring='neg_mean_squared_error',cv=5)
            model.fit(X_train, y_train)
            joblib.dump(model, './knn_model.pkl')
        elif desired_model == "decision tree":
            params = {'max_depth': range(1,10,2), 
                          "min_samples_split": range(2,10,2), 
                          "min_samples_leaf": range(1,10,2)}
            model = GridSearchCV(DecisionTreeRegressor() , param_grid=params,scoring='neg_mean_squared_error',cv=5)
            model.fit(X_train, y_train)
            joblib.dump(model, './decision_tree_model.pkl')
        else:
            raise Exception(f"Desired model type {desired_model} does not exist")
        
        y_pred = model.predict(X_test)
        if (verbose):
            print(f"The best parameters for {desired_model} model from gridsearch are {model.best_params_}")
            print(f"The test MSE for {desired_model} model is: ", mean_squared_error(y_test,y_pred))
            print(f"The R2 score {desired_model} model is: ", r2_score(y_test,y_pred))
        self.stationModels[desired_model] = model
        
        return model
        

    def existsStationModel(self, desired_model: str):
        return desired_model in self.stationModels
    
    def predictBikeCount(self, stationId: int, minutes: float, temp: float, day: int, month: int, day_of_week: int, desired_model: str, verbose:bool = True) -> int:
        if not self.existsStationModel(desired_model):
            model =  self.createModel(desired_model, verbose)
        if desired_model == "linear":
            model = joblib.load("linear_model.pkl")
        elif desired_model == "knn":
            model = joblib.load("knn_model.pkl")
        elif desired_model == "decision tree":
            model = joblib.load("decision_tree_model.pkl")
        else:
            raise Exception(f"Desired model type {desired_model} does not exist")

        y_pred = model.predict([[stationId, minutes, temp, day, month, day_of_week]])
        if (verbose):
            print(f"\nThe {desired_model} model predicts that station {stationId} at minutes {minutes} and temp {temp} will have {y_pred[0]} bikes")
        return y_pred[0]
            
        
    
    
def main():
    BCP = BikeCountPredictor()
    stationId = 81
    minutes = 852 #15:50
    temp = 83
    day = 12
    month = 5
    day_of_week = 4
    desired_model = 'linear'
    BCP.predictBikeCount(stationId, minutes, temp, day, month, day_of_week, desired_model)
    
    stationId = 81
    minutes = 852 #15:50
    temp = 83
    day = 12
    month = 5
    day_of_week = 4
    desired_model = 'decision tree'
    BCP.predictBikeCount(stationId, minutes, temp, day, month, day_of_week, desired_model)
    
    stationId = 81
    minutes = 852 #15:50
    temp = 83
    day = 12
    month = 5
    day_of_week = 4
    desired_model = 'knn'
    BCP.predictBikeCount(stationId, minutes, temp, day, month, day_of_week, desired_model)

    
    