let addIndicatorClass = (form, statusLevel) => {
    let formWrapper = form.closest('.form-card-wrapper');
    if (formWrapper.length === 0) {
        form.find('input[type="text"]').addClass(`border-${statusLevel}`);
    } else {
        formWrapper.addClass(`border-${statusLevel}`);
        formWrapper.addClass(`border`);
        formWrapper.addClass(`border-2`);
    }
}

let removeIndicatorClass = (form, statusLevel) => {
    let formWrapper = form.closest('.form-card-wrapper');
    if (formWrapper.length === 0) {
        form.find('input[type="text"]').removeClass(`border-${statusLevel}`);
    } else {
        formWrapper.removeClass(`border-${statusLevel}`);
        formWrapper.removeClass(`border`);
        formWrapper.removeClass(`border-2`);
    }
}


$(document).on('focusin', 'form.submit-on-unfocus', function(){
    addIndicatorClass($(this), 'warning');
    $(this).find('input[type="text"]').css('box-shadow', 'none');
});

$(document).on('focusout', 'form.submit-on-unfocus', function(){
    removeIndicatorClass($(this), 'warning');
    $(this).submit();
});

$(document).on('submit', 'form.submit-on-unfocus', function(){
    let form = $(this);
    let url = $(this).attr('action');
    let data = $(this).serialize();
    $.post(url, data, function(response) {
        if (response['success']) {
            if (response['updated']) {
                addIndicatorClass(form, 'success');
                setTimeout(() => {
                    removeIndicatorClass(form, 'success');
                }, 1000);
            }
        } else {
            addIndicatorClass(form, 'error');
            setTimeout(() => {
                removeIndicatorClass(form, 'error');
            }, 1000);
        }
    });
    return false;
});


$(document).on('submit', '#add-category-form', function(){
    let form = $(this);
    let url = form.attr('action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        $('#category-list').empty().append(response);
        form.trigger('reset');
        form.find('div.btn-group-toggle label').removeClass('active');
    })
    return false;
});

$(document).on('click', 'input.category-delete-button', function() {
    let form = $(this).closest('form');
    let url = form.data('delete-action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        $('#category-list').empty().append(response);
    })
    return false;
});

$(document).on('submit', '#add-organization-form', function(){
    let form = $(this);
    let url = form.attr('action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        $('#edit-organizations-container').empty().append(response);
        form.trigger('reset');
        form.find('div.btn-group-toggle label').removeClass('active');
    })
    return false;
});

$(document).on('click', 'input.org-delete-button', function() {
    let form = $(this).closest('form');
    let url = form.data('delete-action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        $('#edit-organizations-container').empty().append(response);
    })
    return false;
});
