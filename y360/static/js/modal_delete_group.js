$("#delete-button-result").on("click", function(){
	$.ajax({
		url : $("#delete-button-result").data("url"),
		cache: false,
		success: function(data){
			location.reload()
		}
	});
});
$("#return-button").on("click", function(){
	location.reload();
});