function SubForm() {
    if (validateForm()) {
        $.ajax({
            url: '/formSubmit',
            type: 'post',
            data: $('#myForm').serialize(),
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
}

function validateForm() {
    if (document.forms['myForm']['event-name'].value == '') {
        alert('Name must be filled out');
        return false;
    }
    if (document.forms['myForm']['api-url'].value == '') {
        alert('URL required for API command');
        return false;
    }
    if (document.getElementById('start-time-selector').disabled = false && document.forms['myForm']['start-time-selector'].value == '') {
        alert('Schedule must at least have a start time');
        return false;
    }

    return true
}

function typeSelect(type) {
    if (type == 'button') {
        document.getElementById('start-time-selector').disabled = true;
        document.getElementById('end-time-selector').disabled = true;
        document.getElementById('interval').disabled = true;
        document.getElementById('start-time-selector').style.backgroundColor = 'gray';
        document.getElementById('end-time-selector').style.backgroundColor = 'gray';
        document.getElementById('interval').style.backgroundColor = 'gray';
    } else if (type == 'schedule') {
        document.getElementById('start-time-selector').disabled = false;
        document.getElementById('end-time-selector').disabled = false;
        document.getElementById('interval').disabled = false;
        document.getElementById('start-time-selector').style.backgroundColor = 'initial';
        document.getElementById('end-time-selector').style.backgroundColor = 'initial';
        document.getElementById('interval').style.backgroundColor = 'initial';
    }
}

function removeSchedule(id) {
    var element = document.getElementById(id);
    element.parentNode.removeChild(element);
}

function addButton(attributes) {
    var ul = document.getElementById('buttons');
    var li = document.createElement('li');
    li.setAttribute('id', attributes.id);

    var a = document.createElement('a');
    a.setAttribute('herf', '#');
    a.setAttribute('onclick', 'controllerButtonPress(' + attributes.url + ')');

    var span = document.createElement('span');
    span.appendChild(document.createTextNode(attributes.name));

    a.appendChild(span);
    li.appendChild(a);

    ul.appendChild(li);
}

function addSchedule(attributes) {
    var table = document.getElementById('schedule-table').getElementsByTagName('tbody')[0];
    var trs = table.getElementsByTagName('tr');
    var row = table.insertRow(trs.length);
    row.id = attributes.id;
    var time = row.insertCell(0);
    time.innerHTML = attributes.time;
    var interval_time = row.insertCell(1);
    if (attributes.interval == undefined) {
        interval = ''
    } else {
        interval = attributes.interval;
    }
    interval_time.innerHTML = interval;
    var name = row.insertCell(2);
    name.innerHTML = attributes.name;
}

function controllerButtonPress(url) {
    var settings = {

        "async": true,
        "crossDomain": true,
        "url": "http://" + url,
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        ,
        "data": {}
    }

    $.ajax(settings).done(function(response) {
            console.log(response);
        }

    );
}
