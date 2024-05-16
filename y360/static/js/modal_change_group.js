$('.modal-change-group-button').on('click', function(){
	let url = $(this).data('url');
	var name="", description="", label=""
	$(".input-check-change").each(function(){
		if($(this).attr('id') == 'group-name-change'){
			name = $(this).val();
		};
	});
	$(".input-not-check-change").each(function(){
		if($(this).attr('id') == 'group-description-change'){
			description = $(this).val();
		};
		if($(this).attr('id') == 'group-label-change'){
			label = $(this).val();
		};
	});
	var check = true;
	document.querySelectorAll(".input-check-change").forEach(item => {
		if(!item.value){
			item.style.borderColor = "red";
		};
	});
	if(check==true){
		$.ajax({
			type: "POST",
			url : url,
			cache: false,
			data: {"name":name, "description":description, "label":label},
			success: function(data){
				location.reload()
			}
		});
	}
	else{
		alert("Заполните все обязательные поля");
	};
});