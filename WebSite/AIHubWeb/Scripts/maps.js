

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

    SetupModalDialog();

    for (var i = 0; i < weatherList.length; i++) {
        var currStation = weatherList[i];
        AddPinForStation(currStation);
        CreateStationList(currStation.latlng.Lat, currStation.latlng.Lng, currStation.StationName);
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
    //Our chosen date format
    var options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };

    //Table will be built in parts so that we can keep the table building complety dynamic
    var content;
    var tableHeaderContent = "";
    var tableDetailContent = "";
    content = "<div><table class=\"table table-condensed table-striped table-bordered table-hover\">";
    content += "<h1>" + name + "</h1>";
    tableHeaderContent = "<thead><tr><th> Recorded Time </th>";

    //For the preview display 3 strings or all of it whatever is shorter
    var upperBound = 3;

    if (upperBound > weatherSets.length) {
        upperBound = weatherSets.length;
    }

    for (var i = 0; i < upperBound; i++) {
        var set = weatherSets[i];

        //Parse the date and display it in the first column always
        var date = new Date(parseInt(set.RecordedTime.substr(6)));
        var dateString = date.toLocaleString("en-US", options);

        tableDetailContent += "<tr><td>" + dateString + "</td >";
        for (var propName in set) {

            if (propName.localeCompare("RecordedTime") == 0) {
                continue;
            }

            //Since we use camel case put spaces between the capital then capitalize first letter
            var propNameDisplay = propName.replace(/([A-Z])/g, ' $1').trim();
            propNameDisplay = propNameDisplay.charAt(0).toUpperCase() + propNameDisplay.slice(1);

            //We only have to build the table header only once
            if (i == 0) {
                tableHeaderContent += "<th>" + propNameDisplay + "</th>";
            }

            if (set[propName] == null) {
                tableDetailContent += "<td> --- </td>";
            }
            else {
                tableDetailContent += "<td>" + set[propName] + "</td>";
            }
        }
        tableDetailContent += "</tr>";
    }

    tableHeaderContent += "</tr></thead>";
    content += tableHeaderContent + tableDetailContent + "</table></div>";
    content += "<div class=\"container\"><button type=\"button\" class=\"btn btn-primary btn-lg btn-block\" onclick=\"GetWeatherSetsForTable('" + name + "')\">View Details</button>";
    content += "<button type=\"button\" id=\"dialogButton\" class=\"btn btn-secondary btn-lg btn-block\" onclick=\"DisplayConfigurationDialog('" + name + "')\">Configure Station</button></div>";
    

    return content;
}

function GetWeatherSetsForTable(stationName) {
    var serviceURL = '/Home/GetStationListForName';

    //Get all the info for that table
    $.ajax({
        type: "Get",
        url: serviceURL,
        data: { statName: stationName},
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: DisplayWeatherSetsForTable,
        error: errorFunc
    });
}

function DisplayWeatherSetsForTable(data, status) {

    if (data == null) {
        alert("No data available for this station");
    }

    //Our chosen date format
    var options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };

    //Table will be built in parts so that we can keep the table building complety dynamic
    var content;
    var tableHeaderContent = "";
    var tableDetailContent = "";
    content = "<div><table class=\"table table-striped table-bordered table-hover\">";
    tableHeaderContent = "<thead><tr><th> Recorded Time </th>";
    for (var i = 0; i < data.length; i++) {
        var set = data[i];

        //Parse the date and sip;ay it in the first column always
        var date = new Date(parseInt(set.RecordedTime.substr(6)));     
        var dateString = date.toLocaleString("en-US", options);
 
        tableDetailContent += "<tr><td>" + dateString + "</td >";
        for (var propName in set) {

            if (propName.localeCompare("RecordedTime") == 0) {
                continue;
            }

            //Since we use camel case put spaces between the capital then capitalize first letter
            var propNameDisplay = propName.replace(/([A-Z])/g, ' $1').trim();
            propNameDisplay = propNameDisplay.charAt(0).toUpperCase() + propNameDisplay.slice(1);

            //We only have to build the table header only once
            if (i == 0) {
                tableHeaderContent += "<th>" + propNameDisplay + "</th>";
            }
            
            if (set[propName] == null) {
                tableDetailContent += "<td>---</td>";
            }
            else{
                tableDetailContent += "<td>" + set[propName] + "</td>";
            }
            
        }
        tableDetailContent += "</tr>";
    }

    tableHeaderContent += "</tr></thead>";
    content += tableHeaderContent + tableDetailContent + "</table></div>";

    document.getElementById("map_list").innerHTML = content;

    //Scroll to the newly made table
    $('html, body').animate({
        'scrollTop': $("#map_list").position().top
    });
}

function errorFunc(err) {
    alert("Error Getting data for stations" + err.toString());
}

//Given a clicked on weather station, center the map there
function CenterMapOnStation(lat,lng) {

    var stationLatLng = new google.maps.LatLng(lat, lng);

    map.panTo(stationLatLng);

}
//Populate the list of stations next to the map
function CreateStationList(lat, lng, stationName) {
    var content = "";

    content += "<h4>Station List</h4>";
    //Grabs only the lat, lng, and station name to create new button
    content += "<p><button style=\"height: 40px; width: 100px;\" type=\"button\" class=\"bbtn btn-primary btn-lg btn-block\" onclick=\"CenterMapOnStation('" + lat + "','" + lng + "')\">" + stationName + "</button></p>";

    // Generate the html content
    document.getElementById("station_list").innerHTML = content;


}

function DisplayConfigurationDialog(stationName) {

    // Get the modal
    var modal = document.getElementById('myModal');

    // Get the button that opens the modal
    var btn = document.getElementById("dialogButton");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on the button, open the modal 
    btn.onclick = function () {
        modal.style.display = "block";
    }
    
    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

function SetupModalDialog() {
    var content = "<div class=\"modal-dialog\"><div class=\"modal-content\"><div class=\"modal-header\"><h4>Station Name</h4><span class=\"close\">&times;" +
        "</span ></div > <div class=\"modal-body\"><p>Some text in the Modal..</p></div><div class=\"modal-footer\"></div></div></div>";

    document.getElementById("myModal").innerHTML = content;
}



