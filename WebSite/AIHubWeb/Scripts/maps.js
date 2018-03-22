

function initialize(weatherList) {
    var mapOptions;
    var currentStation;

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

    InitializeDatePicker();
   
    for (var i = 0; i < weatherList.length; i++) {
        var currStation = weatherList[i];
        AddPinForStation(currStation);
        //Reset the station before adding all them back
        document.getElementById("station_list").innerHTML = "";
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
        GetConfigSetDisplayDialog(weatherStation.StationName);
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
    content = "<div><table id=\"currentTable\" class=\"table table-condensed table-striped table-bordered table-hover\">";
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
    content += "<button type=\"button\" id=\"dialogButton\" class=\"btn btn-secondary btn-lg btn-block\" data-toggle=\"modal\" data-target=\"#modalConfigSettings\">Configure Station</button></div>";
    
    return content;
}

function GetWeatherSetsForTable(stationName) {
    currentStation = stationName;
    var serviceURL = '/Home/GetWeatherSetsForNameAndRange';
    var drp = $('#resultrange').data('daterangepicker');
    var start = drp.startDate.format('YYYY-MM-DD');
    var end = drp.endDate.format('YYYY-MM-DD');

    //Get all the info for that table
    $.ajax({
        type: "Get",
        url: serviceURL,
        data: {statName: stationName, startDate: start, endDate: end},
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: DisplayWeatherSetsForTable,
        error: errorFunc
    });
}

function GetWeatherSetsForNewRange() {
    var serviceURL = '/Home/GetWeatherSetsForNameAndRange';
    var drp = $('#resultrange').data('daterangepicker');
    var start = drp.startDate.format('YYYY-MM-DD');
    var end = drp.endDate.format('YYYY-MM-DD');

    //Get all the info for that table
    $.ajax({
        type: "Get",
        url: serviceURL,
        data: { statName: currentStation, startDate: start, endDate: end },
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: DisplayWeatherSetsForTable,
        error: errorFunc
    });
}

function GetConfigSetDisplayDialog(stationName) {
    var serviceURL = '/Home/GetConfigSetForStation';

    //Get all the info for that table
    $.ajax({
        type: "Get",
        url: serviceURL,
        data: {statName: stationName},
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: SetConfigModalInformation,
        error: errorFunc
    });
}


function DisplayWeatherSetsForTable(data, status) {

    if (data == null) {
        alert("No data available for this station");
    }

    //Our chosen date format
    var options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };


    var content = "";
    if (data.length == 0) {
        content = "<div style=\"margin-top:200px;margin-bottom:200px;\"><h2>No Content For Selected Date Range and Station: " + currentStation + "</h2></div>";
    }
    else {
        //Table will be built in parts so that we can keep the table building complety dynamic
        var tableHeaderContent = "";
        var tableDetailContent = "";
        content += "<h2>" + currentStation +  "</h2><div><table class=\"table table-striped table-bordered table-hover\">";
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
                else {
                    tableDetailContent += "<td>" + set[propName] + "</td>";
                }

            }
            tableDetailContent += "</tr>";
        }

        tableHeaderContent += "</tr></thead>";
        content += tableHeaderContent + tableDetailContent + "</table></div>";
    }

    document.getElementById("map_list").innerHTML = content;

    //Scroll to the newly made table
    $('html, body').animate({
        'scrollTop': $("#map_list").position().top
    });

    //Display the tab for viewing different data sets
    document.getElementById("TableSwitching").style.display = "block";
}

function errorFunc(err) {
    alert("Error Getting data for stations - Error Code: " + err.status.toString());
}

//Given a clicked on weather station, center the map there
function CenterMapOnStation(lat,lng) {

    var stationLatLng = new google.maps.LatLng(lat, lng);

    map.panTo(stationLatLng);

}
//Populate the list of stations next to the map
function CreateStationList(lat, lng, stationName) {
    var content = "";

    //Grabs only the lat, lng, and station name to create new button
    content += "<a href=\"#\" style=\"margin:5px;\" class=\"list-group-item list-group-item-action flex-column align-items-start\" onclick=\"CenterMapOnStation('" + lat + "','" + lng + "')\"><h5>" + stationName + "</h5></a > ";

    // Generate the html content
    document.getElementById("station_list").innerHTML += content;
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
    };
    
    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    };

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
}

function SetConfigModalInformation(data, status)
{
    var content = "<form>";
    var contentBool = "";

    if (data == null) {
        alert("No data available for this station");
    }

    //Set the title of the dialog
    document.getElementById('modalConfigSettingsTitle').innerHTML = data.RowKey + " - Configuration Settings";

    for (var name in data) {
        if (name == 'PartitionKey' || name == 'RowKey' || name == "ETag") {
            continue;
        }

        var value = data[name];

        //Since we use camel case put spaces between the capital then capitalize first letter
        var propNameDisplay = "";
        if (name == "Use3G") {
            propNameDisplay = "Use 3G";
        }
        else {
            propNameDisplay = name.replace(/([A-Z])/g, ' $1').trim();
            propNameDisplay = propNameDisplay.charAt(0).toUpperCase() + propNameDisplay.slice(1);
        }
 
        if (typeof value === 'boolean') {
            contentBool += "<div class=\"form-check\">";
            contentBool += "<input type=\"checkbox\" checked=\""+ value + "\" class=\"form-check-input\" id=\"" + name + "\">";
            contentBool += "<label style=\"margin-left:5px;\"class=\"form-check-label\" for=\"" + name + "\">     " + propNameDisplay + "</label>";
            contentBool += "</div>";
        }
        else if (typeof value === 'number') {
            content += "<div class=\"form-group\">";
            content += "<label for=\"" + name + "\">" + propNameDisplay + "</label>";
            content += "<input type=\"number\" class=\"form-control\" id=\"" + name + "\" value=\"" + value + "\">";
            content += "</div>";
        }
        //This checks if it is a time
        else if ((new Date(parseInt(value.substr(6)))).getTime() > 0) {

            var options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
            var date = new Date(parseInt(value.substr(6)));
            var dateString = date.toLocaleString("en-US", options);

            content += "<div class=\"form-group\">";
            content += "<label for=\"" + name + "\">" + propNameDisplay + "</label>";
            content += "<input type=\"text\" readonly class=\"form-control\" id=\"" + name + "\" value=\"" + dateString + "\">";
            content += "</div>";
        }

        else {
            content += "<div class=\"form-group\">";
            content += "<label for=\"" + name + "\">" + propNameDisplay + "</label>";
            content += "<input type=\"number\" class=\"form-control\" id=\"" + name + "\" value=\"" + value + "\">";
            content += "</div>";
        }
    }

    //Boolean often are at the bottom of forms
    content += contentBool + "<div class=\"modal-footer\"> <button type=\"submit\" class=\"btn btn-primary\">Update Config</button></div></form>";
    document.getElementById("modalConfigSettingsBody").innerHTML = content;   
}

function InitializeDatePicker() {

    document.getElementById("resultrange").style.display = "block";

    $('#resultrange').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
            'Today': [moment(), moment()],
            'Last 3 Days': [moment().subtract(3, 'days'), moment()],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'This Year': [moment().startOf('year'), moment().endOf('year')],
            'All Time': [moment(new Date(1995, 1, 4)), moment()]
        }
    }, DateRangeChange);


    var start = moment().subtract(6, 'days');
    var end = moment();
    DateRangeChange(start, end, true);
}

function DateRangeChange(start, end, init) {
    //Change the range on the display
    $('#resultrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));

    var drp = $('#resultrange').data('daterangepicker');
    drp.setStartDate(start);
    drp.setEndDate(end);

    if (init != true) {
        GetWeatherSetsForNewRange();
    }
}

function DisplayWeatherContent() {

    //Set the right tab to show
    document.getElementById("ai_info_list").style.display = "none";
    document.getElementById("map_list").style.display = "block";

    //Update the active tabs
    document.getElementById("WeatherResultsTab").className = "active";
    document.getElementById("AIResultsTab").className = "";
}

function DisplayAITable() {
    //Set the right tab to show
    document.getElementById("ai_info_list").style.display = "block";
    document.getElementById("map_list").style.display = "none";

    //Update the active tabs
    document.getElementById("WeatherResultsTab").className = "";
    document.getElementById("AIResultsTab").className = "active";
}




