function generateExplorerDestination(){
    // radius of the world in meters
    var r = 6367449;

    //pre-set the distance in meters
    var distance = 1000000;
    
    var angularDistance = distance/r;
    
    //Extract the home location coordinates
    var oldLat = homeLocation.lat() * Math.PI/100;
    var oldLng = homeLocation.lng() * Math.PI/100;

    //generate radom bearing
    var bearing = Math.random() * 2 * Math.PI;
    // var bearing = Math.random() * 360;

    //Calculate new location. There is definitely comething wrong with
    //the calculation here!
    var latShift = Math.asin(Math.sin(oldLat) * Math.cos(angularDistance) +
			     Math.cos(oldLat) * Math.sin(angularDistance) *
			     Math.cos(bearing));
    var newLat = (latShift)/Math.PI * 100;
    var lngShift = Math.atan2(Math.sin(bearing) * 
			      Math.sin(angularDistance) *
			      Math.cos(oldLat),
			      Math.cos(angularDistance) - 
			      Math.sin(oldLat) * 
			      Math.sin(newLat));
    var newLng = (oldLng + lngShift)/Math.PI * 100;
    console.log(latShift);
    console.log(lngShift);
    console.log(newLat);
    console.log(newLng);
    newDestination = new google.maps.LatLng(newLat, newLng);
    // window.alert(newDestination)
    return newDestination
};
