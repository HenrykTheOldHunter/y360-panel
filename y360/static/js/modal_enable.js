$("#enable-button-result").on("click", function(){
	$.ajax({
		url : $("#enable-button-result").data("url"),
		cache: false,
		success: function(data){
			location.reload()
		}
	});
});