import './App.css';
import {BlueBikeAPICall} from './api-call';
import {useEffect,useState} from 'react'


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          Station Status:
        </p>
        <BlueBikeButton />
      </header>
    </div>
  );
}

function BlueBikeButton() {
  //create a box that displays the number of bikes available at the default station and the number of docks available at the end station,
  // using the BlueBikeAPICall function, and update the box every 5 seconds, and display the name of the start and end stations, and have a nice layout.
  const [available_bikes, setAvailableBikes] = useState([-1,-1]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    BlueBikeAPICall().then(function(v) {
      setAvailableBikes(v);
      setLoading(false);
    }).catch(console.error);
  }
  ,[]);
  if(loading) {
    return (
      <p> Loading... </p>
    );
  }
  else {
    return (
      <ul>
        <li> Bikes Available at Fenway Station:{available_bikes[0]} </li>
        <li> Docks Available at Ruggles Station:{available_bikes[1]} </li>
      </ul>
      
      
    );
  }
}



export default App;








  // // const [available_bikes, setAvailableBikes] = useState([-1,-1]);
  // const [available_bikes, setAvailableBikes] = useState([-1,-1]);
  // const [loading, setLoading] = useState(true);
  
  // useEffect(() => {
  //   BlueBikeAPICall().then(function(v) {
  //     setAvailableBikes(v);
  //     setLoading(false);
  //   }).catch(console.error);
  // }
  // ,[]);

  // if(loading) {
  //   return (
  //     <button> Loading... </button>
  //   );
  // }
  // else {
  //   return (
  //     <p> Bikes Available at Fenway Station:{available_bikes[0]} {'\n'}
  //     Docks Available at Ruggles Station:{available_bikes[1]}
  //     </p>
      
      
  //   );
  // }