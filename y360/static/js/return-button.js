$("#return-button").on("click", function(){
	let button = $("#return-button");
    let url = button.data('url');
    let container = $('#modal-window').find('#connector');
	container.empty();
	container.html('');
	$.ajax({
		url: url,
	}).done(function(data){
		container.html(data);
	});
});