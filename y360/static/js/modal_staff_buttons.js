$("#change-button").on("click", function(){
	let button = $("#change-button");
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
$("#drop-button").on("click", function(){
	let button = $("#drop-button");
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
$("#enable-button").on("click", function(){
	let button = $("#enable-button");
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