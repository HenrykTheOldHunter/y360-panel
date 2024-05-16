$(window).on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let url = button.data('url');
    let container = $('#modal-window').find('#connector');
    container.html('');
	let staffId = button.data('staff');
	let type = button.data('type');
	if(staffId){
		$.ajax({
		type: "POST",
        url: url,
		data: {"staffId" : staffId}
		}).done(function(data){
		   container.html(data);
		});
	}
	else if(type){
		$.ajax({
		type: "POST",
		url: url,
		data: {"type" : type}
		}).done(function(data){
			container.html(data);
		});
	}
	else{
		$.ajax({
			url: url,
		}).done(function(data){
		   container.html(data);
		});
	};
});
