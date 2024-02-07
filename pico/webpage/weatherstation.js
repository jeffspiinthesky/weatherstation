$('#date').textfill({maxFontPixels: 1000});
$('#time').textfill({maxFontPixels: 1000});
$('#temperature').textfill({maxFontPixels: 1000});
$('#windspeed').textfill({maxFontPixels: 1000});
$('#pressure').textfill({maxFontPixels: 1000});
$('#humidityvalue').css("font-size", $("#pressurevalue").css("font-size"));
$( document ).ready(function() {
    getData();
});
function getData() {
    console.log('Getting data');
    $.ajax({
        type: 'GET',
        url: 'https://jksmith.ddns.net:60443/weatherdata/',
        dataType: 'json'

    })
    .done(function(data) {
            console.log('Success');
            console.log(JSON.stringify(data,null,2));
            var dateFromJson = data.time;
            var currentTime = moment(dateFromJson, 'YYYY/MM/DD-HH-mm-ss');
            $('.flex-container').css('background', data.tempcolour);
            $('#datevalue').html(currentTime.format(' Do MMMM YYYY HH:mm'));
            $('#date').textfill({maxFontPixels: 1000, widthOnly: true});
            $('#tempvalue').html(Math.round(data.temperature) + '&#176;C');
            $('#temperature').textfill({maxFontPixels: 1000});
            $('#windvalue').text('Wind: ' + (Math.round(data.wind_speed * 100) / 100).toFixed(2) + 'mph');
            $('#windspeed').textfill({maxFontPixels: 1000,});
            $('#pressurevalue').text('P: ' + data.pressure + 'hPa');
            $('#humidityvalue').text('H: ' + data.humidity + '%');
            var windSize = parseInt($('#windvalue').css('font-size'));
            console.log('Wind size: ' + windSize);
            var pressHumSize = windSize * 0.75;
            console.log('Pressure / Humidity size: ' + pressHumSize);
            $('#pressurevalue').css('font-size', Math.round(pressHumSize) + 'px');
            $('#humidityvalue').css('font-size', Math.round(pressHumSize) + 'px');
        })
    .fail(function(jqXHR, textStatus) {
        console.log('Failure: ' + textStatus);
        $('#tempvalue').text('Unable to retrieve temperature');
        $('#temperature').textfill({maxFontPixels: 1000});
    })
    .always(function() {
        console.log('Scheduling next update');
        setTimeout(getData, 5000);
    })
}