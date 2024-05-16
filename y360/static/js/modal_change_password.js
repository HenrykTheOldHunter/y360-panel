$("#change-button-result").off().on("click",  function(){
	var password="";
	var passwordChangeRequired = true;
	$(".input-check").each(function(){
		if($(this).attr('id') == 'new-password'){
			password = $(this).val();
		};
		if($(this).attr('id') == 'password-change-required'){
			if($(this).is(':checked')){
				passwordChangeRequired = "True";
			}
			else{
				passwordChangeRequired = "False";
			};
		};
	});
	var data = JSON.parse($.ajax({
		type: "POST",
		url : $("#change-button-result").data("url"),
		cache: false,
		async: false,
		data: { "password":password, "passwordChangeRequired":passwordChangeRequired},
		success: function(result){
			return result;
		}
	}).responseText);
	if("Error" in data){
		if(typeof data["Error"] == "string"){
			var error = $("<a>"+data["Error"]+"</a>");
			error.css("color", "red");
			$(this).parent().parent().next().html(error);
		}
		else{
			$(".input-check").each(function(){
				if(data["Error"].indexOf($(this).attr('id')) != -1){
					$(this)[0].classList.add("error");
				}
			});
			var error = $("<a>Ошибка! Заполните все обязательные поля!</a>");
			error.css("color", "red");
			$(this).parent().parent().next().html(error);
		}
	}
	else{
		location.reload()
	};
});
