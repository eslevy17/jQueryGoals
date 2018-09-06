function progress(percent, count){
  var total = document.getElementsByClassName("progress");

  var progressbar = document.getElementById("completion" + count);
  var width = 0;
  var timer = setInterval(frame, 10);
  function frame(){
    if (width >= percent){
      clearInterval(timer);
    } else {
      width++;
      if(width <= 100){ progressbar.style.width = width + '%'; }
      progressbar.innerHTML = width + '%';
      if(width >= 100){ progressbar.innerHTML += ' Congratulations!!!'; }
    }
  }
}

function weeklychart(id) {
  /*  WEEKLY DATA POINTS BUILDER */

  id = parseInt(id);

  var events = JSON.parse(document.getElementById('events').innerHTML.replace(/'/g, '"'));
  console.log(events[id]);

  var chart = new CanvasJS.Chart("chartContainer", {
    animationEnabled: true,
    theme: "light2", // "light1", "light2", "dark1", "dark2"
    title: {
      text: "Weekly Progress"
    },
    axisY: {
      title: "Time",
      suffix: " hours",
      includeZero: false
    },
    axisX: {
      title: "Day of the Week"
    },
    data: [{
      type: "column",
      yValueFormatString: "#,##0.0#",
      dataPoints: events[id]
    }]
  });
  chart.render();
}


function monthlychart(id){
  /* MONTHLY DATA POINTS CODE BUILDING */

  id = parseInt(id);
  console.log(id);

  var events = JSON.parse(document.getElementById('monthevents').innerHTML.replace(/'/g, '"'));
  console.log(events[id]);

  var chart = new CanvasJS.Chart("chartContainer", {
    animationEnabled: true,
    theme: "light2", // "light1", "light2", "dark1", "dark2"
    title: {
        text: "Monthly Progress"
    },
    axisY: {
        title: "Time",
        suffix: " hours",
        includeZero: false
    },
    axisX: {
        title: "Monthly progress"
    },
    data: [{
        type: "column",
        yValueFormatString: "#,##0.0#",
        dataPoints: events[id]
      }]
    });
  chart.render();
}

function addToEvent(id){
  var patt = /\d+/i;
  var n = parseInt(patt.exec(id)[0]);

  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log('Added 15 hours');
      json = JSON.parse(xhttp.responseText);

      data = JSON.parse(json.data);

      var total = 0;
      for(var i = 0; i < data.length; i++){
        total += data[i]['fields']['duration'];
      }

      document.getElementById('committed'+n).innerHTML = '' + total + ' of ' + json.total + ' hour(s)';

      progress(100*(total/json.total), n);
    }
  };
  xhttp.open("POST", "/addToEvent", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send(encodeURI("id="+n+"&csrfmiddlewaretoken="+csrftoken));
}
