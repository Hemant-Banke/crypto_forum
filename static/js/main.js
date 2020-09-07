

window.addEventListener('load', (event) => {

    // Request Form
    var form_request = document.getElementById('form-req');
    form_request.addEventListener('submit', (e) => {
        e.preventDefault();

        if (FormValidate.validate(form_request)){
            var btn = form_request.querySelector('input[type="submit"], button[type="submit"]');

            Fetch.post(
                'controller/register_requests',
                {
                    request_text: form_request.querySelector('textarea[name="request"]').value,
                },
                function(data){
                    msg.success('Your request has been received and will be acted upon shortly :)', 'Sent');
                    // Clear
                    form_request.classList.remove('was-validated');
                    form_request.querySelector('textarea[name="request"]').value = '';
                },
                btn
            );
        }
    });


    // Load Recent Reviews
    Fetch.post(
        'controller/get_recent',
        {},
        function(data){
            var dataHTML = '';
            data = JSON.parse(data.data);
            data.forEach((exc) => {
                dataHTML += `
                    <a href="platform/${exc.fields.name}" class="scroll-element exc-wrapper">
                        <img class="lazyload exc-img" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII="
                            data-src="${exc.fields.image_url}" alt="Request">

                        <span class="exc-text">${exc.fields.name}</span>
                    </a>
                `;
            });

            var wrapper = document.getElementById('main-recent');
            wrapper.innerHTML = dataHTML + wrapper.innerHTML;
        }
    );


    // Load Top Exchanges
    Fetch.post(
        'controller/get_top_exchanges',
        {},
        function(data){
            var dataHTML = '';
            data = JSON.parse(data.data);
            data.forEach((exc) => {
                dataHTML += `
                    <a href="platform/${exc.fields.name}" class="scroll-element exc-wrapper">
                        <img class="lazyload exc-img" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII="
                            data-src="${exc.fields.image_url}" alt="Request">

                        <span class="exc-text">${exc.fields.name}</span>
                    </a>
                `;
            });

            var wrapper = document.getElementById('main-exc');
            wrapper.innerHTML = dataHTML + wrapper.innerHTML;
        }
    );


    // Load Top Coins
    Fetch.post(
        'controller/get_top_coins',
        {},
        function(data){
            var dataHTML = '';
            data = JSON.parse(data.data);
            data.forEach((exc) => {
                dataHTML += `
                    <a href="platform/${exc.fields.name}" class="scroll-element exc-wrapper">
                        <img class="lazyload exc-img" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII="
                            data-src="${exc.fields.image_url}" alt="Request">

                        <span class="exc-text">${exc.fields.name}</span>
                    </a>
                `;
            });

            var wrapper = document.getElementById('main-coin');
            wrapper.innerHTML = dataHTML + wrapper.innerHTML;
        }
    );

    // Load Top Give aways
    Fetch.post(
        'controller/get_top_ga',
        {},
        function(data){
            var dataHTML = '';
            data = JSON.parse(data.data);
            data.forEach((exc) => {
                dataHTML += `
                    <a href="platform/${exc.fields.name}" class="scroll-element exc-wrapper">
                        <img class="lazyload exc-img" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII="
                            data-src="${exc.fields.image_url}" alt="Request">

                        <span class="exc-text">${exc.fields.name}</span>
                    </a>
                `;
            });

            var wrapper = document.getElementById('main-ga');
            wrapper.innerHTML = dataHTML + wrapper.innerHTML;
        }
    );
});
