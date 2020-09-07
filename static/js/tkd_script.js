
var msg = function () {
    var popup = document.getElementById('popup');

    var alert = function showAlert(text, title, is_success){

        popup.innerHTML = `<h6>${title}</h6>${text}`;
        popup.style.display = 'block';

        popup.className = "";
        if (is_success){
            popup.classList.add('success');
        }
        else{
            popup.classList.add('error');
        }

        setTimeout( function(){
            popup.style.display = 'none';
        }, 2000);
    }

    return {
        success: function (msg , title) {
            alert(msg , title , true);
        },

        error: function (msg , title) {
            alert(msg , title , false);
        },
    };
}();


// Enable/Disable Buttons
var Button = function() {
    return {
        enable: function(button) {
            button.disabled = false;
            button.getElementsByClassName('spinner')[0].style.display = "none";
        },

        disable: function(button) {
            button.disabled = true;
            button.getElementsByClassName('spinner')[0].style.display = "inline-block";
        }
    }
}();


// Validate Forms
var FormValidate = function() {
    return {
        validate: function(form) {
            // Validates Form and returns if valid

            form.classList.add('was-validated');
            return form.checkValidity();
        },
    }
}();


// Fetch API
var Fetch = function(){

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    return {
        post: function(url, data, success, btn=null) {
            if (btn){
                Button.disable(btn);
            }

            // Fetch
            fetch(url, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Accept": "application/json",
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify(data),
            })
            .then(
                function(response) {
                    if (btn){
                        Button.enable(btn);
                    }

                    if (response.status !== 200) {
                        console.log('Looks like there was a problem. Status Code: ' +
                        response.status);

                        msg.error('Looks like there was a problem! Please try again.', 'Error');
                        return;
                    }

                    // Examine the text in the response
                    response.json().then(function(data) {
                        if (data.type == 'success'){
                            success(data);
                        }
                        else{
                            msg.error(data.message, 'Error');
                        }
                    });
                }
            )
            .catch(function(err) {
                console.log('Fetch Error :-S', err);
                msg.error('Looks like there was a problem! Please try again.', 'Error');

                if (btn){
                    Button.enable(btn);
                }
            });
        },

        post_multipart: function(url, data, success, btn=null) {
            if (btn){
                Button.disable(btn);
            }

            const formData  = new FormData();
            for(const name in data) {
                formData.append(name, data[name]);
            }

            // Fetch
            fetch(url, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Accept": "application/json",
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: formData,
            })
            .then(
                function(response) {
                    if (btn){
                        Button.enable(btn);
                    }

                    if (response.status !== 200) {
                        console.log('Looks like there was a problem. Status Code: ' +
                        response.status);

                        msg.error('Looks like there was a problem! Please try again.', 'Error');
                        return;
                    }

                    // Examine the text in the response
                    response.json().then(function(data) {
                        if (data.type == 'success'){
                            success(data);
                        }
                        else{
                            msg.error(data.message, 'Error');
                        }
                    });
                }
            )
            .catch(function(err) {
                console.log('Fetch Error :-S', err);
                msg.error('Looks like there was a problem! Please try again.', 'Error');

                if (btn){
                    Button.enable(btn);
                }
            });
        },

        get_crossorigin: function(url, success, btn=null) {
            if (btn){
                Button.disable(btn);
            }

            // Fetch
            fetch(url)
            .then(
                function(response) {
                    if (btn){
                        Button.enable(btn);
                    }

                    if (response.status !== 200) {
                        console.log('Looks like there was a problem. Status Code: ' +
                        response.status);

                        msg.error('Looks like there was a problem! Please try again.', 'Error');
                        return;
                    }

                    // Examine the text in the response
                    response.json().then(function(data) {
                        success(data);
                    });
                }
            )
            .catch(function(err) {
                console.log('Fetch Error :-S', err);
                msg.error('Looks like there was a problem! Please try again.', 'Error');

                if (btn){
                    Button.enable(btn);
                }
            });
        },
    }
}();


// Pagination
var Pagination = function(){

    function closest3(n, pos){
        if (pos == 0 || pos == 1){
            return [0,1,2]
        }
        else if (pos == n-1 || pos == n-2){
            return [n-3, n-2, n-1]
        }
        else{
            return [pos-1, pos, pos+1]
        }
    }

    return {
        create: function(page_count, page, page_elem, caller_name){

            var page_html = '';
            for(var i = 0; i < page_count; i++){
                if (page_count > 3 && !closest3(page_count, page).includes(i)){
                    continue;
                }
                page_html += `
                    <li class="page-item ${(page == i) ? 'active' : ''}">
                        <button class="page-link" onclick="${caller_name}(${i});">${i+1}</button>
                    </li>
                `;
            }
            if (page > 0){
                page_html = `
                    <li class="page-item">
                        <button class="page-link" onclick="${caller_name}(${page-1});">Previous</button>
                    </li>
                    <li class="page-item">
                        <button class="page-link" onclick="${caller_name}(0);">First</button>
                    </li>
                ` + page_html;
            }
            if (page < page_count-1){
                page_html += `
                    <li class="page-item">
                        <button class="page-link" onclick="${caller_name}(${page+1});">Next</button>
                    </li>
                `;
            }

            page_elem.innerHTML = `
                <nav aria-label="Page navigation">
                    <ul class="pagination mb-0 text-small">
                        ${page_html}
                    </ul>
                </nav>
            `;
        }
    }
}();


var sanitizeHTML = function (str) {
	var temp = document.createElement('div');
	temp.textContent = str;
	return temp.innerHTML;
};

function copyTextToClipboard(text) {
    var textArea = document.createElement("textarea");
    textArea.value = text
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        var successful = document.execCommand('copy');
        if (successful){
            msg.success('', 'Copied');
        }
        else{
            msg.error('', 'Not Copied');
        }
    }
    catch (err) {
        msg.error('Oops, unable to copy', 'Error');
    }

    document.body.removeChild(textArea);
}



window.addEventListener('load', (event) => {
    // Msg
    document.getElementById('popup').style.display = 'none';

    // Validation
    var forms = document.getElementsByClassName('needs-validation');

    Array.prototype.slice.call(forms).forEach((form) => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            if (FormValidate.validate(form)){
                var btn = form.querySelector('input[type="submit"], button[type="submit"]');
                Button.disable(btn);

                form.submit();
            }
        });
    });


    // Header
    var head_inp = document.getElementById('main-s');
    var search_area = document.getElementById('search-area');
    var search_res = document.getElementById('search-results');
    head_inp.addEventListener('focus', () => {
        search_area.style.opacity = 1;
        search_area.style.display = 'block';

        if (search_res.innerHTML.trim() == ''){
            search_res.innerHTML = `
                <div class="w-100 d-flex justify-content-center">
                    <h6 class="text-small">(Enter atleast 2 characters to search)</h6>
                </div>
            `;
        }
    });

    head_inp.addEventListener('blur', () => {
        search_area.style.opacity = 0;
        setTimeout(function(){
            search_area.style.display = 'none';
        }, 300);
    });

    head_inp.addEventListener('keyup', ()=>{
        var inp = head_inp.value;

        if (inp.length >= 2){
            if (search_res.innerHTML.trim() == ''){
                search_res.innerHTML = `
                    <div class="w-100 d-flex justify-content-center">
                        <div class="spinner-border spinner-border-sm text-primary" role="status">
                            <span class="sr-only">Loading...</span>
                        </div>
                    </div>
                `;
            }

            // Load Search results
            Fetch.post(
                '/controller/get_search',
                {
                    'inp' : inp,
                },
                function(data){
                    var dataHTML = '';
                    data = JSON.parse(data.data);
                    data.forEach((res) => {
                        dataHTML += `
                            <a href="/platform/${res.name}" class="search-res-element">
                                <img class="lazyload search-res-img" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII="
                                    data-src="${res.image_url}" alt="Request">

                                <span class="search-res-text text-truncate">${res.name}</span>
                            </a>
                        `;
                    });

                    if (dataHTML == ''){
                        dataHTML = `
                            <div class="w-100 d-flex justify-content-center">
                                <h6 class="text-small">Nothing Found :(</h6>
                            </div>
                        `;
                    }

                    search_res.innerHTML = dataHTML;
                }
            );
        }
    });

});
