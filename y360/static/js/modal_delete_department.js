$("#delete-button-result").on("click", function(){
	$.ajax({
		url : $("#delete-button-result").data("url"),
		cache: false,
		success: function(data){
			document.querySelector(".errord").style.display = "none";
			location.reload()
		},
		error: function(request){
			document.querySelector(".errord").style.display = "block";
		}
	});
});
$("#return-button").on("click", function(){
	location.reload();
});