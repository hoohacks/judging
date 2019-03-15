$(document).on('submit', '#import-categories', function(){
    let url = $(this).attr('action');
    let data = $(this).serialize();
    $.post(url, data, function(response) {
        $('#edit-categories-container').empty().append(response);
    })
    return false;
});