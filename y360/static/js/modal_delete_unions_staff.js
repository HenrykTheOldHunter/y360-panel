$("#delete-button-result").on("click", function(){
	$.ajax({
		type: "POST",
		url : $("#delete-button-result").data("url"),
		data: {"staffId":$("#delete-button-result").data("staff")},
		cache: false,
		success: function(data){
			location.reload()
		}
	});
});
$("#return-button").on("click", function(){
	location.reload();
});
