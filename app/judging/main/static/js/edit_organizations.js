$(document).on('focusin', 'form.submit-on-unfocus', function(){
    $(this).find('input[type="text"]').addClass('border-warning');
    $(this).find('input[type="text"]').css('box-shadow', 'none');
});

$(document).on('focusout', 'form.submit-on-unfocus', function(){
    $(this).find('input[type="text"]').removeClass('border-warning');
    $(this).submit();
});

$(document).on('submit', 'form.submit-on-unfocus', function(){
    let form = $(this);
    let url = $(this).attr('action');
    let data = $(this).serialize();
    $.post(url, data, function(response) {
        if (response['success']) {
            if (response['updated']) {
                form.find('input[type="text"]').addClass('border-success');
                setTimeout(() => {
                    form.find('input[type="text"]').removeClass('border-success');
                }, 1000);
            }
        } else {
            form.find('input[type="text"]').addClass('border-error');
            setTimeout(() => {
                form.find('input[type="text"]').removeClass('border-error');
            }, 1000);
        }
    });
    return false;
});
