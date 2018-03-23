

function GetWeatherSetsForNewRange(statName, start, end) {
    var serviceURL = '/Home/GetWeatherSetsForNameAndRange';

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

function GetConfigSetForStation(stationName) {
    var serviceURL = '/Home/GetConfigSetForStation';

    //Get all the info for that table
    $.ajax({
        type: "Get",
        url: serviceURL,
        data: { statName: stationName },
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: SetCurrentConfig,
        error: errorFunc
    });
}

function PostConfigInformation(configInfo) {
    var serviceURL = '/Home/UpdateConfigSetting';
    var string = JSON.stringify(configInfo)

    //Get all the info for that table
    $.ajax({
        type: "POST",
        url: serviceURL,
        data: string,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            console.log("!");
            console.log(data);
        },
        error: errorFunc
    });
}

function errorFunc(err) {
    alert("Error Getting data for stations - Error Code: " + err.status.toString());
}