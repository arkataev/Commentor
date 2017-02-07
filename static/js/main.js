

window.onload = getRegions

function getRegions(e) {
    e.preventDefault()
    var region = document.getElementById('region')
    var callback = function (data) {
        var r = JSON.parse(data)
        for (var attr in r){
            var option = document.createElement('option')
            option.setAttribute('id', 'region_' + attr)
            option.setAttribute('value',attr)
            option.innerHTML = r[attr]
            region.appendChild(option)
        }
    }
    ajaxRequest('/get_regions', '', callback)
}


function ajaxRequest(url, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            return callback(this.responseText)
        }
    }
    xhr.open('POST', url, true);
    xhr.send(data)
}
