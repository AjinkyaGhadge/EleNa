import {Component} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MinLengthValidator } from '@angular/forms';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent { 
  constructor(private http: HttpClient) { }

  title="EleNa - Elevation based Navigation";
  
  // backend Django server url
  serverUrl = 'http://localhost:8000/find_route/'
  
//  Declaring initial origin and destination coordinates
  coordinates = {
    originLat: 42.3504489,
    originLng: -72.5274984,
    destinationLat: 42.3777404,
    destinationLng: -72.5198350
  }

  // This variable will hold the route coordinates received from the backend
  locations = []

  // Sets the default elevation choice to min and the percentage of shortest distance to 0
  elevation_choice: String = "min";
  percentage_of_shortest_distance = 0;

  // Sets the coordinates according to the position of the draggable origin marker in google maps
  setOriginCoordinates($event: any) {
    console.log($event);
    this.coordinates["originLat"] = $event.latLng.lat();;
    this.coordinates["originLng"] = $event.latLng.lng();;
  }

  // Sets the coordinates according to the position of the draggable destination marker in google maps
  setDestinationCoordinates($event: any) {
    console.log($event);
    this.coordinates["destinationLat"] = $event.latLng.lat();;
    this.coordinates["destinationLng"] = $event.latLng.lng();;
  }

  /* This function gets triggered when the user clicks the button Get direction. It sends a asynchronous http post request with the json body to the backend server.
  As soon as response is returned from the server a call to the setRoute() is made passing the response to it as a parameter.
  */
  onGetDirectionClick(){
    const headers = { 'content-type': 'application/json'}  
    let data = {"source_latitude": this.coordinates["originLat"], 
    "source_longitude": this.coordinates["originLng"], 
    "destination_latitude": this.coordinates["destinationLat"], 
    "destination_longitude": this.coordinates["destinationLng"], 
    "percentage": this.percentage_of_shortest_distance, 
    "elevation_type": this.elevation_choice, 
    "algorithm": "a_star"}
    const body=JSON.stringify(data);
    console.log(body)
    this.http.post(this.serverUrl, body,{'headers':headers}).toPromise()
    .then(
      res => { 
        console.log(res);
        this.setRoute(res);
      }
    );
  }

  // Pushes the route coordinates to the locations variable and also populates the Stats division with the total elevation and total distance values
  setRoute(response){
    let routes = response['route']
    console.log(routes)
    this.locations = []
    for (let entry of routes) {
      let new_coordinate = {}
      this.locations.push({"lat": entry[0], "lng": entry[1]});
    }
    console.log(this.locations);
    document.getElementById("StatsDiv").innerHTML = "<p>Total Elevation : " + response["elevation"] + " meters" +
    "<br /> Total Distance : "+ response["distance"] + " meters </p>"
  }
}
