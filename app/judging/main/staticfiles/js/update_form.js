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

// === Category
// Import
$(document).on('submit', '#import-categories', function(){
    let url = $(this).attr('action');
    let data = $(this).serialize();
    $.post(url, data, function(response) {
        $('#edit-categories-container').empty().append(response);
    })
    return false;
});

// Add
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

// Delete
$(document).on('click', 'input.category-delete-button', function() {
    let form = $(this).closest('form');
    let url = form.data('delete-action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        $('#category-list').empty().append(response);
    })
    return false;
});

// === Category
// Add
$(document).on('submit', '#add-organization-form', function(){
    let form = $(this);
    let url = form.attr('action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        $('#organizations-list').empty().append(response);
        form.trigger('reset');
        form.find('div.btn-group-toggle label').removeClass('active');
    })
    return false;
});

// Delete
$(document).on('click', 'input.org-delete-button', function() {
    let form = $(this).closest('form');
    let url = form.data('delete-action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        $('#organizations-list').empty().append(response);
    })
    return false;
});


// === Team
// Add
$(document).on('submit', '#add-team-form', function(){
    let form = $(this);
    let url = form.attr('action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        $('#team-list').empty().append(response);
        form.trigger('reset');
        form.find('div.btn-group-toggle label').removeClass('active');
    })
    return false;
});

// Delete
$(document).on('click', 'input.team-delete-button', function() {
    let form = $(this).closest('form');
    let url = form.data('delete-action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        $('#team-list').empty().append(response);
    })
    return false;
});


// === Anchor
// Add
$(document).on('submit', '#add-anchor-form', function(){
    let form = $(this);
    let url = form.attr('action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        $('#anchor-list').empty().append(response);
        form.trigger('reset');
        form.find('div.btn-group-toggle label').removeClass('active');
    })
    return false;
});

// Delete
$(document).on('click', 'input.anchor-delete-button', function() {
    let form = $(this).closest('form');
    let url = form.data('delete-action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        $('#anchor-list').empty().append(response);
    })
    return false;
});
// Assign

$(document).on('click', 'input.anchor-assign-all-button', function() {
    let form = $(this).closest('form');
    let url = form.data('assign-action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        $('#anchor-list').empty().append(response);
    })
    return false;
});