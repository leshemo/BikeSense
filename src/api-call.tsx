import axios from 'axios';

export async function BlueBikeAPICall(start_station_id:number = 342, end_station_id:number = 12) {
    
    const result = await axios.get('https://gbfs.bluebikes.com/gbfs/en/station_status.json');
    const stations = result.data.data.stations
    let start_station;
    let end_station;

    for (var station of stations) {
        if (station.station_id == start_station_id) {
            start_station = station
        } else if (station.station_id == end_station_id) {
            end_station = station
        }
            
    }
    const available:number[] = [start_station.num_bikes_available, end_station.num_docks_available]

    return available;
    
}

//create a new function that does what the below function does but avoid returning a promise
// export function BlueBikeAPICall(start_station_id:number = 342, end_station_id:number = 12) {
//     axios.get('https://gbfs.bluebikes.com/gbfs/en/station_status.json')
//     .then(function (response) {
//         const stations = response.data.data.stations
//         let start_station;
//         let end_station;

//         for (var station of stations) {
//             if (station.station_id == start_station_id) {
//                 start_station = station
//             } else if (station.station_id == end_station_id) {
//                 end_station = station
//             }

//         }
//         const available:number[] = [start_station.num_bikes_available, end_station.num_docks_available]

//         return available;

//     })
//     .catch(function (error) {
//         console.log(error);
//     })
//     .then(function () {
//         // always executed
//     });
// }