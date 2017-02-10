


var region = document.getElementById('region');
var deleteCommentButtons = document.querySelectorAll('#comments li button');
var sendCommentBtn = document.getElementById('send_comment')
if (sendCommentBtn) {sendCommentBtn.addEventListener('click', sendComment)}

if (region){
    window.onload = loadCities;
    region.addEventListener('change', loadCities);
}

if (deleteCommentButtons) {
    deleteCommentButtons.forEach(function(btn) {
        console.log(btn)
        btn.addEventListener('click', function (e) {
            return deleteComment(e.target)
        })
    })
}

function sendComment(e) {
    e.preventDefault()
    var btn = e.target;
    var form_data = ''
    var form = new FormData(document.getElementById('add_comment'));
    for (var key of form.keys()){
        var elem = document.querySelector('[name=' + key + ']')
        if (key=='comment') {elem.style.borderColor = '#FCD68A'}
        else{elem.style.borderBottomColor = '#FCD68A'}
        form_data += key+'='+form.get(key) + '&'
    }

    var callback = function (data) {
        btn.style.background = 'green'
        btn.innerHTML = 'Success'
    }
    
    var fallback = function (data) {
        var data = JSON.parse(data)
        for (var key in data.errors){
            var elem = document.querySelector('[name=' + key + ']')
            if (key=='comment') {elem.style.borderColor = '#D33F49'}
            else{elem.style.borderBottomColor = '#D33F49'}
        }
    }
    ajaxRequest('/save_comment', form_data, callback, fallback)
}

function loadCities() {
    var rid = region.options[region.selectedIndex].value;
    return getLocations(rid)
}

function getLocations(regionId) {
    var rid = 'region_id=' + regionId,
        city = document.getElementById('city');
    city.innerHTML = '';
    var callback = function (data) {
        var r = JSON.parse(data);
        for (var attr in r){
            var option = document.createElement('option');
            option.setAttribute('id', 'city_' + attr);
            option.setAttribute('value',attr);
            option.innerHTML = r[attr];
            city.appendChild(option);
        }
    };
    ajaxRequest('/get_locations', rid , callback, '');
}

function deleteComment(button){
    var cuid = 'comment_id=' + button.dataset.uid;
    var comments = document.getElementById('comments')
    var callback = function () {
        comments.removeChild(button.parentNode)
    };
    ajaxRequest('/delete_comment', cuid, callback, '');
}

function ajaxRequest(url, data, callback, fallback) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            return callback(this.responseText);
        }else if (this.readyState == 4 && this.status == 402) {
            return fallback(this.responseText);
        }
    };
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(data);
}


