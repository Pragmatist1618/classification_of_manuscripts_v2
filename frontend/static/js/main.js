$(document).ready(function (message) {
    //Ограничение на ввод в поле форматом
    //12345678 или 12345678-12345678
    $('body').on('input', '#man-creation-date-input', function () {
        let bgn_str = this.value.substr(0, 8);
        let mid_str = this.value.substr(8, 1);
        let end_str = this.value.substr(9, 8);
        bgn_str = bgn_str.replace(/[^0-9]/g, '');
        mid_str = mid_str.replace(/[^-]/g, '');
        end_str = end_str.replace(/[^0-9]/g, '');
        this.value = bgn_str + mid_str + end_str;
    })

    //Ограничение на ввод в поле форматом
    //12345678 или 12345678-12345678
    $('body').on('input', '#img-creation-date-input', function () {
        let bgn_str = this.value.substr(0, 8);
        let mid_str = this.value.substr(8, 1);
        let end_str = this.value.substr(9, 8);
        bgn_str = bgn_str.replace(/[^0-9]/g, '');
        mid_str = mid_str.replace(/[^-]/g, '');
        end_str = end_str.replace(/[^0-9]/g, '');
        this.value = bgn_str + mid_str + end_str;

    })

    //функция выравнивания высоты и ширины изображений для корректного поворота
    $(function(){
        let img_wrapper = $('.img-container')
        img_wrapper.height(img_wrapper.width());

        let img = $('.image');
        w = img.width;
        h = img.height;
        if (w > h){
            img.width(img_wrapper.width())

            $(window).resize(function(){
                img.width(img_wrapper.width());
                img.height(h*img_wrapper.width/w);
            });
        } else {
            img.height(img_wrapper.height())

            $(window).resize(function(){
                img.height(img_wrapper.height());
                img.width(w*img_wrapper.height/h);
            });
        }
    });


    // ajax-запрос для поворота изображения без поворота экрана
    $('.rotate-img').click(function() {
        // let id = self.getAttribute("data-creation-date-bgn");
        let id = $(this).attr("data-rotate-id");
        let cookie = document.cookie;
        let csrfToken = cookie.substring(cookie.indexOf('=') + 1);
        $.ajax({
            type: 'post',
            headers: {
                'X-CSRFToken': csrfToken
            },
            url: '/api/v1/manuscript/img_rotate/' + id + '/',
            success: function(response) {
                let img = $('#img_' + id);
                if(img.hasClass('north')){
                    img.removeClass('north');
                    img.addClass('west');
                }else if(img.hasClass('west')){
                    img.removeClass('west');
                    img.addClass('south');
                }else if(img.hasClass('south')){
                    img.removeClass('south');
                    img.addClass('east');
                }else if(img.hasClass('east')){
                    img.removeClass('east');
                    img.addClass('north');
                }
            },
            error: function(e, x, r) {
                console.log('Error send form to rotate img');
            }
        });
        return false;
    });

    // рукописи
    let select_type = $('#type');
    let select_storage = $('#storage');
    let btn_cipher = $('#cipher-btn');
    let select_lec_type = $('#lec_type')
    // изображения
    let select_lec_month_type = $('#lec_month_type');
    let select_lec_part_type = $('#lec_part_type')


    function set_filters(){
        // рукописи
        let type = select_type.val();
        let storage = select_storage.val();
        let cipher = $('#cipher-input').val();
        let lec_type = select_lec_type.val();
        // изображения
        let lec_month_type = select_lec_month_type.val();
        let lec_part_type = select_lec_part_type.val();

        let url = '/manuscript/?';
        // рукописи
        if (type !== '-') url += ('type=' + type + '&');
        if (storage !== '-') url += ('storage=' + storage + '&');
        if (cipher !== '') url += ('cipher=' + cipher + '&');
        if (lec_type !== '-') url += ('lec_type=' + lec_type + "&")
        // изображения
        if (lec_part_type !== '-') url += ('lec_part_type=' + lec_part_type + '&');
        if (lec_month_type !== '-') url += ('lec_month_type=' + lec_month_type + '&');

        let cookie = document.cookie;
        let csrfToken = cookie.substring(cookie.indexOf('=') + 1);
        $.ajax({
            type: 'get',
            headers: {
                'X-CSRFToken': csrfToken
            },
            url: url,
            success: function(response) {
                $('#main').hide();
                let data = response;
                data = data.substring(data.indexOf("<div class=\"col-7\" id=\"main\">"),
                    data.indexOf("<div id=\"aside\" class=\"col-5\">"));
                $('#pointer').after(data);
            },
            error: function(e, x, r) {
                console.log('Error get filters');
            }
        });
        return false;
    }

    // рукописи
    select_type.change(set_filters);
    select_storage.change(set_filters);
    btn_cipher.on('click', set_filters);
    select_lec_type.change(set_filters);
    // изображения
    select_lec_part_type.change(set_filters);
    select_lec_month_type.change(set_filters);


})
