import axios from 'axios';

export async function BlueBikeGetTwoStationStatus(start_station_id:number = 342, end_station_id:number = 12) {
    
    const result = await axios.get('https://gbfs.bluebikes.com/gbfs/en/station_status.json');
    const stations = result.data.data.stations
    let start_station;
    let end_station;


    for (var station of stations) {

        if (station.station_id == start_station_id) {
            start_station = station
        }  
        if (station.station_id == end_station_id) {
            end_station = station
        }
            
    }
    
    const available:number[] = [start_station.num_bikes_available, end_station.num_docks_available]

    return available;
    
    
}

export async function BlueBikeGetStations() {
    
    const result = await axios.get('https://gbfs.bluebikes.com/gbfs/en/station_information.json');
    const stations = result.data.data.stations

    let station_names_and_ids: {name:string, id:number}[] = []
    for (var station of stations) {
        station_names_and_ids.push({name:station.name, id:station.station_id})
            
    }
    
    return station_names_and_ids;

    
}

