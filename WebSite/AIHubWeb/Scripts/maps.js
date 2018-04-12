var currentStation;
var currentConfigOptions; //We want to push this object back through a post so change field

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

    //Reset the station before adding all them back
    document.getElementById("station_list").innerHTML = "";
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
        icon: "Images/station.png",
        position: googLatLng,
        map: map,
        optimized: false,
        title: weatherStation.StationName
    });

    var infoWindowString = GenerateInfoString(weatherStation.StationName, weatherStation.latestTime, weatherStation.rgWeatherSets);
    var infowindow = new google.maps.InfoWindow({
        content: infoWindowString
    });

    marker.addListener('click', function () {
        GetConfigSetForStation(weatherStation.StationName);
        infowindow.open(map, marker);
    });

    marker.setMap(window.map);
}

function GenerateInfoString(name, latestRecordedTime, weatherSets) {
    //Our chosen date format
    var options = {year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };

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

            if (propName.localeCompare("RecordedTime") === 0) {
                continue;
            }

            //Since we use camel case put spaces between the capital then capitalize first letter
            var propNameDisplay = propName.replace(/([A-Z])/g, ' $1').trim();
            propNameDisplay = propNameDisplay.charAt(0).toUpperCase() + propNameDisplay.slice(1);

            //We only have to build the table header only once
            if (i === 0) {
                tableHeaderContent += "<th>" + propNameDisplay + "</th>";
            }

            if (set[propName] === null) {
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
    content += "<div class=\"container\"><button type=\"button\" class=\"btn btn-primary btn-lg btn-block\" onclick=\"DisplayStationDataTable('" + name + "')\">View Details</button>";
    content += "<button type=\"button\" id=\"dialogButton\" class=\"btn btn-secondary btn-lg btn-block\" onclick=\"SetConfigModalInformation()\" data-toggle=\"modal\" data-target=\"#modalConfigSettings\">Configure Station</button></div>";
    
    return content;
}

function DisplayWeatherSetsForTable(data, status) {

    if (data === null) {
        alert("No data available for this station");
    }

    InsertWeatherTableHtml(data);
    InsertAITableHtml(data);

    //Scroll to the newly made table weather table
    if (document.getElementById("map_list").style.display !== "none") {
        $('html, body').animate({
            'scrollTop': $("#map_list").position().top
            });
    }

    //Scroll to the newly made table ai table
    if (document.getElementById("ai_info_list").style.display !== "none") {
        $('html, body').animate({
            'scrollTop': $("#ai_info_list").position().top
        });
    }

    //Display the tab for viewing different data sets
    document.getElementById("TableSwitching").style.display = "block";
}

function DisplayWeatherSetsForTableOnRefresh(data, status) {

    if (data === null) {
        alert("No data available for this station");
    }

    InsertWeatherTableHtml(data);
    InsertAITableHtml(data);

    document.getElementById("refreshIcon").classList.remove("fa-spin");
}

function InsertWeatherTableHtml(data) {
    //Our chosen date format
    var options = {weekday:'short', year:'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };

    var content = "";
    if (data.length === 0) {
        content = "<div style=\"margin-top:200px;margin-bottom:200px;\"><h2>No Content For Selected Date Range and Station: " + currentStation + "</h2></div>";
    }
    else {
        //Table will be built in parts so that we can keep the table building complety dynamic
        var tableHeaderContent = "";
        var tableDetailContent = "";
        content += "<h2>" + currentStation + "</h2><div><table id=\"resultsTable\" class=\"table table-striped table-bordered table-hover\">";
        tableHeaderContent = "<thead><tr><th> Recorded Time </th>";
        for (var i = 0; i < data.length; i++) {
            var set = data[i];

            //Parse the date and sip;ay it in the first column always
            var date = new Date(parseInt(set.RecordedTime.substr(6)));
            var dateString = date.toLocaleString("en-US", options);

            tableDetailContent += "<tr><td>" + dateString + "</td >";
            for (var propName in set) {

                if (propName.localeCompare("RecordedTime") === 0 || propName.toLocaleLowerCase().startsWith("ai")) {
                    continue;
                }

                //Since we use camel case put spaces between the capital then capitalize first letter
                var propNameDisplay = propName.replace(/([A-Z])/g, ' $1').trim();
                propNameDisplay = propNameDisplay.charAt(0).toUpperCase() + propNameDisplay.slice(1);

                //We only have to build the table header only once
                if (i === 0) {
                    tableHeaderContent += "<th>" + propNameDisplay + "</th>";
                }

                if (set[propName] === null) {
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
}

function InsertAITableHtml(data) {
    //Our chosen date format
    var options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };

    var content = "";
    if (data.length === 0) {
        content = "<div style=\"margin-top:200px;margin-bottom:200px;\"><h2>No Content For Selected Date Range and Station: " + currentStation + "</h2></div>";
    }
    else {
        //Table will be built in parts so that we can keep the table building complety dynamic
        var tableHeaderContent = "";
        var tableDetailContent = "";
        content += "<h2>" + currentStation + "</h2><div><table id=\"resultsTable\" class=\"table table-condensed table-striped table-bordered table-hover\">";
        tableHeaderContent = "<thead><tr><th> Recorded Time </th>";
        for (var i = 0; i < data.length; i++) {
            var set = data[i];

            //Parse the date and sip;ay it in the first column always
            var date = new Date(parseInt(set.RecordedTime.substr(6)));
            var dateString = date.toLocaleString("en-US", options);

            tableDetailContent += "<tr><td>" + dateString + "</td >";
            for (var propName in set) {

                if (!propName.toLocaleLowerCase().startsWith("ai")) {
                    continue;
                }

                //Since we use camel case put spaces between the capital then capitalize first letter
                var propNameDisplay = propName.replace(/_/g, ' ');
                propNameDisplay = propNameDisplay.substring(2); // Trim AI in the name
                propNameDisplay = propNameDisplay.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase(); });

                //We only have to build the table header only once
                if (i === 0) {
                    tableHeaderContent += "<th>" + propNameDisplay + "</th>";
                }

                if (set[propName] === null) {
                    tableDetailContent += "<td>---</td>";
                }
                else {
                    var tempRound = parseFloat(set[propName]).toFixed(2);

                    tableDetailContent += "<td>" + tempRound + "</td>";
                }

            }
            tableDetailContent += "</tr>";
        }

        tableHeaderContent += "</tr></thead>";
        content += tableHeaderContent + tableDetailContent + "</table></div>";
    }

    document.getElementById("ai_info_list").innerHTML = content;
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
    content += "<a href=\"#map_canvas\" style=\"margin:5px;\" class=\"list-group-item list-group-item-action flex-column align-items-start\" onclick=\"CenterMapOnStation('" + lat + "','" + lng + "')\"><h5>" + stationName + "</h5></a > ";

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
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
}
function SetCurrentConfig(data, status) {

    if (status === 'success') {
        currentConfigOptions = data;
        currentConfigOptions["Timestamp"] = parseInt(currentConfigOptions["Timestamp"].substr(6));
    }       
}

function SetConfigModalInformation()
{
    var content = "<form id=\"configForm\" action=\"\" method=\"post\" onsubmit=\"UpdateConfigInformation()\">";
    var contentBool = "";

    if (currentConfigOptions === null) {
        alert("No data available for this station, try again shortly.");
        return;
    }

    //Set the title of the dialog
    document.getElementById('modalConfigSettingsTitle').innerHTML = currentConfigOptions.RowKey + " - Configuration Settings";

    for (var name in currentConfigOptions) {

        //These are the Meta-Data
        if (name === 'PartitionKey' || name === 'RowKey' || name === "ETag") {
            continue;
        }

        var value = currentConfigOptions[name];

        //Since we use camel case put spaces between the capital then capitalize first letter
        var propNameDisplay = "";
        //if (name === "use_3G") {
        //    propNameDisplay = "Use 3G";
        //}
        //else {
        propNameDisplay = name.replace(/_/g, ' ');
        propNameDisplay = propNameDisplay.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase(); });

        //boolean check for some reason does not evaluate strings as 'true' 'false' as boolean
        if (typeof value === 'boolean' || value === "true" || value === "false") {
            contentBool += "<div class=\"form-check\">";
            //contentBool += "<input type=\"checkbox\" checked=\""+ value  +"\" value=\"" + value + "\" class=\"form-check-input\" name=\"" + name + "\" id=\"" + name + "\">";
            contentBool += "<label for=\"" + name + "\">     " + propNameDisplay + "</label>";
            contentBool += "<select class=\"form-control\" id=\"" +name +"\" name=\"" + name + "\">";

            if (value === true || value === "true") {
                contentBool += "<option value=\"false\">No</option>";
                contentBool += "<option value=\"true\" selected>Yes</option></select></div>";
            }
            else {
                contentBool += "<option value=\"false\" selected>No</option>";
                contentBool += "<option value=\"true\">Yes</option></select></div>";
            }

        }
        else if (name.endsWith("ro")) {
            //Trim the ro
            propNameDisplay = propNameDisplay.slice(0, -2);
            content += "<div class=\"form-group\">";
            content += "<label for=\"" + name + "\">" + propNameDisplay + "</label>";
            content += "<input type=\"text\" readonly class=\"form-control\" name=\"" + name + "\" id=\"" + name + "\" value=\"" + value + "\">";
            content += "</div>";
        }
        //number
        else if (typeof value === 'number' && name !== "Timestamp") {
            content += "<div class=\"form-group\">";
            content += "<label for=\"" + name + "\">" + propNameDisplay + "</label>";
            content += "<input type=\"number\" class=\"form-control\" name=\"" + name + "\" id=\"" + name + "\" value=\"" + value + "\">";
            content += "</div>";
        }
        //timestamp is a special case.. display read only different title
        else if (name === "Timestamp") {

            var options = {weekday:'short', year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
            var date = new Date(parseInt(value));
            var dateString = date.toLocaleString("en-US", options);

            content += "<div class=\"form-group\">";
            content += "<label for=\"" + name + "\">Last Updated</label>";
            content += "<input type=\"text\" readonly class=\"form-control\" name=\"" + name + "\" id=\"" + name + "\" value=\"" + dateString + "\">";
            content += "</div>";
        }
        //string
        else {

            content += "<div class=\"form-group\">";
            content += "<label for=\"" + name + "\">" + propNameDisplay + "</label>";
            content += "<input type=\"text\" class=\"form-control\" name=\"" + name + "\" id=\"" + name + "\" value=\"" + value + "\">";
            content += "</div>";
        }
    }

    //Boolean often are at the bottom of forms
    content += contentBool + "<div class=\"modal-footer\"><button type=\"button\" class=\"btn btn-secondary\" data-dismiss=\"modal\">Close</button> <button type=\"button\" onclick=\"UpdateConfigInformation()\" data-dismiss=\"modal\" class=\"btn btn-primary\">Update Config</button></div></form>";
    document.getElementById("modalConfigSettingsBody").innerHTML = content;   
}

function InitializeDatePicker() {

    document.getElementById("Toolbar").style.display = "block";

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

    if (init !== true) {
        GetWeatherSetsForNewRange(currentStation, start.format('MM/DD/YYYY'), end.format('MM/DD/YYYY'));
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


function DisplayStationDataTable(statName) {
    //Keep track of current station that we are displaying data for
    currentStation = statName;

    if (document.getElementById("Toolbar").style.display === "none") {
        InitializeDatePicker();
    }
 
    var drp = $('#resultrange').data('daterangepicker');
    GetWeatherSetsForNewRange(statName, drp.startDate.format('MM/DD/YYYY'), drp.endDate.format('MM/DD/YYYY'));
}

function UpdateConfigInformation() {

    var formData = $("#configForm").serializeArray();

    $(formData).each(function (i, field) {
        //Timestamp needs special attention
        if (field.name === "Timestamp") {
            //We want to keep the date stored in a consitent matter, .net serializes the dates when we send them and they come out like this
            currentConfigOptions["Timestamp"] = moment().unix() * 1000;
        }
        else {
            //Otherwise just dynamically define it
            currentConfigOptions[field.name] = field.value;
        }
    });

    PostConfigInformation(currentConfigOptions);
}

function UpdateAllTableInfo() {

    document.getElementById("refreshIcon").classList.add("fa-spin");
    var drp = $('#resultrange').data('daterangepicker');
   
    RefreshWeatherSets(currentStation, drp.startDate.format('MM/DD/YYYY'), drp.endDate.format('MM/DD/YYYY'));
}




