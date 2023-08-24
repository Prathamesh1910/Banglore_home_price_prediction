const BASE_URL = window.location.href

function getBathValue() {
    var uiBathrooms = document.getElementsByName("uiBathrooms");
    for(var i in uiBathrooms) {
      if(uiBathrooms[i].checked) {
          return parseInt(i)+1;
      }
    }
    return -1; // Invalid Value
  }  

function getBHKValue() {
    var uiBHK = document.getElementsByName("uiBHK");
    for(var i in uiBHK) {
      if(uiBHK[i].checked) {
          return parseInt(i)+1;
      }
    }
    return -1; // Invalid Value
  }

function getBalconyValue() {
    var uiBalconies = document.getElementsByName("uiBalconies");
    for(var i in uiBalconies) {
      if(uiBalconies[i].checked) {
          return parseInt(i)+1;
      }
    }
    return -1; // Invalid Value
  }

function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");
    var size = getBHKValue();
    var total_sqft = document.getElementById("uiSqft");
    var bath = getBathValue();
    var balcony = getBalconyValue();
    var area_type = document.getElementById("uiAreaTypes");
    var location = document.getElementById("uiLocations");
    var month_availability = document.getElementById("uiAvailability");
    var estPrice = document.getElementById("uiEstimatedPrice");
  
    var url =BASE_URL + "/predict_home_price"; 
   
    $.post(url, {
        size: size,
        total_sqft: parseFloat(total_sqft.value),
        bath: bath,
        balcony: balcony,
        area_type: area_type.value,
        location: location.value,
        month_availability: month_availability.value
    },function(data, status) {
        console.log(data.estimated_price);
        estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
        console.log(status);
    });
  }


function onPageLoad_location() {
    console.log( "document loaded" );
    var url = BASE_URL + "/get_location_names"; 

    $.get(url,function(data, status) {
        console.log("got response for get_location_names request");
        if(data) {
            var locations = data.locations;
            var uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty();
            for(var i in locations) {
                var opt = new Option(locations[i]);
                $('#uiLocations').append(opt);
            }
        }
    });
  }

function onPageLoad_area_type() {
    console.log( "document loaded" );
    var url = BASE_URL + "/get_area_type"; 

    $.get(url,function(data, status) {
        console.log("got response for get_area_type request");
        if(data) {
            var area_type = data.area_type;
            var uiAreaTypes = document.getElementById("uiAreaTypes");
            $('#uiAreaTypes').empty();
            for(var i in area_type) {
                var opt = new Option(area_type[i]);
                $('#uiAreaTypes').append(opt);
            }
        }
    });
  }

function onPageLoad_availability() {
    console.log( "document loaded" );
    var url = BASE_URL + "/get_availability"; 

    $.get(url,function(data, status) {
        console.log("got response for get_area_type request");
        if(data) {
            var availability = data.availability;
            var uiAvailability = document.getElementById("uiAvailability");
            $('#uiAvailability').empty();
            for(var i in availability) {
                var opt = new Option(availability[i]);
                $('#uiAvailability').append(opt);
            }
        }
    });
  }
  
function onPageLoad() {
    onPageLoad_location();
    onPageLoad_area_type();
    onPageLoad_availability();
}
window.onload = onPageLoad;
