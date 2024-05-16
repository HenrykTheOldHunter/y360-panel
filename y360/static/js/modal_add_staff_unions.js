var users = [];

document.querySelectorAll('.modal-bio').forEach(item => {
	$(item).on("click", function() {
		if (item.classList.contains("picked")){
			const index = users.indexOf($(item).attr("id"));
			users.splice(index, 1);
		}
		else{
			users.push($(item).attr("id"));
		};
		item.classList.toggle("picked");
		$(".error-text").html("");
	});
});
$("#modal-add-staff-unions-button").on("click", function(){
	$(".message").css("display", "block");
    $(this).prop("disabled", true);
	let button = $("#modal-add-staff-unions-button");
	let url = button.data("url");
	var data = JSON.parse($.ajax({
			type: "POST",
			url: url,
			cache: false,
			async: false,
			data: {"users":JSON.stringify(users)},
			success: function(data){
				location.reload();
			}
		}).responseText);
	if("Error" in data){
		$(".message").css("display", "none");
    	$(this).prop("disabled", false);
		var error = $("<a>"+data["Error"]+"</a>");
		error.css("color", "red");
		$(".error-text").html(error);
	}
	else{
		location.reload();
	}
});