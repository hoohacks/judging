$('input:checked').parent().button('toggle');

$('select').addClass('form-control');

// Change scores if user changes team in form
$('select').on('change', function (e) {
    let form = $(this).closest('form');
    let url = form.data('get-scores-action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        $('body').append();  // this line forces a redraw on mobile
        if (response['success']) {
            $.each(response['data'], function(criteria_id, score) {
                let label = $(`#id_criteria-${criteria_id}_${score - 1}`).parent('label');
                label.button('toggle');
            });
        } else {
            $('label > input:checked').prop('checked', false).parent().removeClass('active');
        }
    })
});