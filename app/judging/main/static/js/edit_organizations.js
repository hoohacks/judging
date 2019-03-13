$('form.submit-on-unfocus').focusin(function(){
    $(this).find('input[type="text"]').addClass('border-warning');
    $(this).find('input[type="text"]').css('box-shadow', 'none');
});

$('form.submit-on-unfocus').focusout(function(){
    $(this).find('input[type="text"]').removeClass('border-warning');
    $(this).submit();
});

$('form.submit-on-unfocus').submit(function(){
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

$('form.submit-on-enter').focusout(function(){
    $(this).submit();
});

$('form.submit-on-enter').submit(function(){
    let form = $(this);
    let url = $(this).attr('action');
    let data = $(this).serialize();
    $.post(url, data, function(response) {
        form.find('input[type="text"]').val("");
        if (response['success']) {
            // Add disabled form to list
            // If wanted a smoother experience, would need to grab the CSRF token
            //  and include that in this form too, but that's just too much work right now
            let elementId = 'org-' + response['org']['id'];
            $('#organization-list').append(`
            <div>
                <form class="p-1">
                    <input type="text" name="org_name" class="form-control" id="${elementId}" disabled>
                </form>
            </div>
            `);
            $(`#${elementId}`).val(response['org']['name']);
            
            form.find('input[type="text"]').addClass('border-success');
            setTimeout(() => {
                form.find('input[type="text"]').removeClass('border-success');
            }, 1000);
        } else {
            form.find('input[type="text"]').addClass('border-error');
            setTimeout(() => {
                form.find('input[type="text"]').removeClass('border-error');
            }, 1000);
        }
    });
    return false;
});

$('input.org-delete-button').click(function() {
    let form = $(this).closest('form');
    let parentDiv = form.parent('div');
    let url = form.data('delete-action');
    let data = form.serialize();
    $.post(url, data, function(response) {
        console.log(response);
        
        if (response['success']) {
            parentDiv.remove();
        }
    });
});