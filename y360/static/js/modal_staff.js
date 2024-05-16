$(window).on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let url = button.data('url');
    let container = $('#modal-window').find('#connector');
    container.html('');
    $.ajax({
        url: url,
    }).done(function(data){
       container.html(data);
    });
});
$(window).on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let url = button.data('url');
    let container = $('#modal-add-staff').find('#connector');
    container.html('');
    $.ajax({
        url: url,
    }).done(function(data){
       container.html(data);
    });
});