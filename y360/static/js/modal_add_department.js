$('.modal-add-department-button').on('click', function(){
	let url = $(this).data('url');
	var name="", description="", label=""
	$(".input-check-add").each(function(){
		if($(this).attr('id') == 'department-name-add'){
			name = $(this).val();
		};
	});
	$(".input-not-check-add").each(function(){
		if($(this).attr('id') == 'department-description-add'){
			description = $(this).val();
		};
		if($(this).attr('id') == 'department-label-add'){
			label = $(this).val();
		};
	});
	var data = JSON.parse($.ajax({
			type: "POST",
			url : url,
			cache: false,
			async: false,
			data: {"name":name, "description":description, "label":label},
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