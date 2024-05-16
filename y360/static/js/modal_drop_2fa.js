$("#drop-button-result").on("click", function(){
	$.ajax({
		url : $("#drop-button-result").data("url"),
		cache: false,
		success: function(data){
			location.reload()
		}
	});
});