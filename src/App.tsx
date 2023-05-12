import './App.css';
import React from 'react'
import {BlueBikeGetTwoStationStatus, BlueBikeGetStations} from './api-call';
import {useEffect,useState} from 'react'


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          BlueBike Station Status:
          <BlueBikeStationStatus />
        </p>
        
      </header>
    </div>
  );
}

//create a box that allows a user to pick a start and end station, and displays the number of bikes available at the start station and the number of docks available at the end station.
//The start and end stations are picked using a dropdown, and the names and ids are retrieved from the BlueBikeGetStations function. The ids are passed to the BlueBikeGetTwoStationsStatus 
//function, which then displays the number of bikes and docks available.
function BlueBikeStationStatus() {
  const [available_bikes, setAvailableBikes] = useState([-1,-1]);
  const [loading, setLoading] = useState(true);
  const [start_station, setStartStation] = useState(() => {
    const saved = localStorage.getItem('start_station');
    const initialValue = JSON.parse(saved!);
    return initialValue || 342;
  });

  const [end_station, setEndStation] = useState(() => {
    const saved = localStorage.getItem('end_station');
    const initialValue = JSON.parse(saved!);
    return initialValue || 12;
  });

  const [stations, setStations] = useState([{name:'Fenway', id:342}, {name:'Ruggles', id:12}]);

  useEffect(() => {
    BlueBikeGetStations().then(function(v) {
      setStations(v);
      setLoading(false);
    }).catch(console.error);
    //adds the stations to the the local storage to keep if user refreshes the page
    localStorage.setItem('start_station', JSON.stringify(start_station));
    localStorage.setItem('end_station', JSON.stringify(end_station));
    BlueBikeGetTwoStationStatus(start_station, end_station).then(function(v) {
      setAvailableBikes(v);
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
        <small>Start Station: </small>
        <br></br>
        <small><select value={start_station} onChange={e => setStartStation(+e.target.value)}>
          {stations.map((station: any) => (
            <option value={station.id}>{station.name}</option>
          ))}
        </select>: {available_bikes[0]} bike(s) available. </small>
        <br></br>
        <small>End Station: </small>
        <br></br>
        <small><select value={end_station} onChange={e => setEndStation(+e.target.value)}>
          {stations.map((station: any) => (
            <option value={station.id}>{station.name}</option>
          ))}
        </select>: {available_bikes[1]} dock(s) available. </small>
      </div>
    );
  }
}


export default App;
