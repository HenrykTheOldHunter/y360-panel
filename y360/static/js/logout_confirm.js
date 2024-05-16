$("#confirm-button").on("click", function(){
	$.ajax({
		url : $("#confirm-button").data("url"),
		cache: false,
		success: function(data){
			location.reload();
		}
	});
});
$("#return-button").on("click", function(){
	location.reload();
});
