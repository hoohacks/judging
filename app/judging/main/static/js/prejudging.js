$(document).on('submit', '#import-categories', function(){
    let url = $(this).attr('action');
    let data = $(this).serialize();
    $.post(url, data, function(response) {
        $('#edit-categories-container').empty().append(response);
    })
    return false;
});


$(document).on('submit', '#add-organization-form', function(){
    let url = $(this).attr('action');
    let data = $(this).serialize();
    $.post(url, data, function(response) {
        $('#edit-organizations-container').empty().append(response);
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
