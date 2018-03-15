
function initialize(weatherList) {
    var mapOptions;

    //Default location is edmonton otherwise center it on the 1st object in the list
    if (weatherList.length > 0) {
        var latlng = weatherList[0].latlng;
        mapOptions = {
            center: new google.maps.LatLng(latlng.Lat, latlng.Lng),
            zoom: 10,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
    }
    else {
        mapOptions = {
            center: new google.maps.LatLng(53.544, -113.0909),
            zoom: 10,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
    }

    map = new google.maps.Map(document.getElementById("map_canvas"),
        mapOptions);

    for (var i = 0; i < weatherList.length; i++) {
        var currStation = weatherList[i];
        AddPinForStation(currStation);
    }
}

function AddPinForStation(weatherStation) {
    var latlng = weatherStation.latlng;
    var googLatLng = new google.maps.LatLng(latlng.Lat, latlng.Lng);
    var marker = new google.maps.Marker({
        position: googLatLng,
        map: map,
        title: weatherStation.StationName
    });

    var infoWindowString = GenerateInfoString(weatherStation.StationName, weatherStation.latestTime, weatherStation.rgWeatherSets);
    var infowindow = new google.maps.InfoWindow({
        content: infoWindowString
    });

    marker.addListener('click', function () {
        infowindow.open(map, marker);
    });

    marker.setMap(window.map);
}

function GenerateInfoString(name, latestRecordedTime, weatherSets) {



    //JSON dates are a bit strange this is the reccomended way to parse them
    var date = new Date(parseInt(latestRecordedTime.substr(6)));
    //Its in UTC so use local
    var dateString = date.toString();

    //Json.Encode(
    var content;
    content += "<div><table class=\"table table-condensed table-striped table-bordered table-hover\" \"\">>";
    content += "<content><h2>" + name + "</h2>";
    content += "<span style=\"margin:5px\">" + dateString + "</span></content>";
    content +="<thead><tr><th>Attribute</th><th>Reading</th></tr></thead>";
    for (var i = 0; i < weatherSets.length; i++) {
        var set = weatherSets[i];
        for (var propName in set) {

            if (propName == "RecordedTime") {
                continue;
            }

            content += "<tr><td>" + propName + "</td><td>" + set[propName] + "</td></tr>";
        }

        //For now just show the first one
        break;
    }
    content += "</table></div>";
    content += "<p><button type=\"button\" class=\"bbtn btn-primary btn-lg btn-block\">View Details</button></p>";

    return content;
}