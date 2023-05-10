import './App.css';
import {BlueBikeGetTwoStationStatus, BlueBikeGetStations} from './api-call';
import {useEffect,useState} from 'react'


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          Station Status:
          <BlueBikeStationStatus />
        </p>
        
      </header>
    </div>
  );
}

function BlueBikeStationStatus() {
  //create a box that allows a user to pick a start and end station, and displays the number of bikes available at the start station and the number of docks available at the end station.
  //The start and end stations are picked using a dropdown, and the names and ids are retrieved from the BlueBikeGetStations function. The ids are passed to the BlueBikeGetTwoStationsStatus function, which then displays the number of bikes and docks available.
  const [available_bikes, setAvailableBikes] = useState([-1,-1]);
  const [loading, setLoading] = useState(true);
  const [start_station, setStartStation] = useState(342);
  const [end_station, setEndStation] = useState(12);
  const [stations, setStations] = useState([{name:'Fenway', id:342}, {name:'Ruggles', id:12}]);

  useEffect(() => {
    BlueBikeGetTwoStationStatus(start_station, end_station).then(function(v) {
      setAvailableBikes(v);
      setLoading(false);
    }).catch(console.error);
    BlueBikeGetStations().then(function(v) {
      setStations(v);
      setLoading(false);
    }).catch(console.error);

    const interval = setInterval(() => {
      BlueBikeGetTwoStationStatus(start_station, end_station).then(function(v) {
        setAvailableBikes(v);
        setLoading(false);
      }).catch(console.error);
    }, 5000);
    return () => clearInterval(interval);
  }
  ,[start_station, end_station]);
  
  if(loading) {
    return (
      <p> Loading... </p>
    );
  }
  else {    
    return (
      <div>
        <select value={start_station} onChange={e => setStartStation(+e.target.value)}>
          {stations.map((station: any) => (
            <option value={station.id}>{station.id}</option>
          ))}
        </select>
        <select value={end_station} onChange={e => setEndStation(+e.target.value)}>
          {stations.map((station: any) => (
            <option value={station.id}>{station.id}</option>
          ))}
        </select>
        <div> </div>
        <p> {available_bikes[0]} bikes available at {stations.find(x => x.id === start_station)?.name} </p>
        <p> {available_bikes[1]} docks available at {stations.find(x => x.id === end_station)?.name} </p>
      </div>
    );
  }


}





export default App;
