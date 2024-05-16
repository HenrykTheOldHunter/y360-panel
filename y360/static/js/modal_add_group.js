$('.modal-add-group-button').on('click', function(){
	let url = $(this).data('url');
	var name="", description="", label=""
	$(".input-check-add").each(function(){
		if($(this).attr('id') == 'group-name-add'){
			name = $(this).val();
		};
	});
	$(".input-not-check-add").each(function(){
		if($(this).attr('id') == 'group-description-add'){
			description = $(this).val();
		};
		if($(this).attr('id') == 'group-label-add'){
			label = $(this).val();
		};
	});
	var check = true;
	document.querySelectorAll(".input-check-add").forEach(item => {
		if(!item.value){
			item.style.borderColor = "red";
		};
	});
	var data = JSON.parse($.ajax({
			type: "POST",
			url : url,
			cache: false,
			async: false,
			data: {"name":name, "description":description, "label":label},
			success: function(data){
				location.reload();
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