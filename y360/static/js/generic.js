window.addEventListener("load", (event) => {
	document.querySelectorAll(".sidebar-nav-item").forEach(item =>{
		$(item).on("click", function(){
			let button = $(item);
			let url = button.data("url");
			window.location.replace(url);
		});
	});
	$("#admin").on("click", function(){
		window.location.replace($("#admin").data("url"));
	});
});
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

