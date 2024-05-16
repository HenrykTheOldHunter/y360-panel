$('.modal-add-button').unbind().on('click', function(){
	document.querySelectorAll(".input-check").forEach(item => {
		if (item.classList.contains("error")){
			item.classList.remove("error");
		};
	});
	var last="", first="", middle="", email="", login="", password="", department=""; 
	$(".input-check").each(function(){
		if($(this).attr('id') == 'last'){
			last = $(this).val();
		};
		if($(this).attr('id') == 'first'){
			first = $(this).val();
		};
		if($(this).attr('id') == 'email'){
			email = $(this).val();
		};
		if($(this).attr('id') == 'login'){
			login = $(this).val();
		};
		if($(this).attr('id') == 'password'){
			password = $(this).val();
		};
	});
	$(".input-not-check").each(function(){
		if($(this).attr('id') == 'middle'){
			middle = $(this).val();
		};
	});
	department = getGlobalDepartment();
	var data = JSON.parse($.ajax({
		type: "POST",
		url : "/y360/add-staff-data/",
		cache: false,
		async: false,
		data: {"last":last, "first":first, "middle":middle, "email":email,"login":login, "password":password, "department":department},
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
var globalDepartment = $(department).val();
$("select").on("change", $(".select"), function(e){
	if(e.target.id == "department"){
		setGlobalDepartment(e.target.value);
	};
});
function setGlobalDepartment(value){
	globalDepartment = value;
};
function getGlobalDepartment(){
	return globalDepartment;
};