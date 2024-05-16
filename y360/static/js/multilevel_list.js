window.addEventListener("load", (event) => {
	addInit(document);
});
$(window).on("update", function(){
	addInit(document);
});
function addInit(element){
	$("body").on("click", ".list-item-container", function(event) {
		if(!($(event.target).closest('.add').length > 0 || $(event.target).closest('.menu').length > 0)) {
			item = $(this).parent()[0];
			if(item.id != 1){
				let button = $(item);
				let url = button.data("url");
				let container = button;
				if (item.classList.contains("clicked")){
					item.querySelector("#drop-ico").src = "/static/ico/drop-close.png"
					var type="";
					if(url.includes("department")){
						type = "department";
					}
					if(url.includes("group")){
						type = "group";
					}
					$.ajax({
						type: "POST",
						url: "/y360/close-unit/"+item.id+"/",
						data: {"type":type},
					}).done(function(data){
						if(data.status == true){
							for(i = 0; i < data.result.length; i++){
								try{
									$(document).find("#"+data.result[i]).remove()
								}catch(err){};
								try{
									$(document).find("[data-unionid='" + data.result[i] + "']").remove(); 
								}catch(err1){};
							}
							try{
								$(document).find("[data-unionid='" + item.id + "']").remove(); 
							}catch(err1){};
						}
					});
					item.classList.remove("clicked");
				}
				else {
					item.querySelector("#drop-ico").src = "/static/ico/drop-open.png"
					item.classList.add("clicked");
					$.ajax({
						type: "POST",
						url: url,
						data: {"level":button.attr('class')},
					}).done(function(data){
						container.after(data);
					});
					if($("#union-lookup-input").val() != ""){
						if($("#union-lookup-button").data("url").indexOf("department")>=0){
							$(item).trigger("mark", "department");
						};
						if($("#union-lookup-button").data("url").indexOf("group")>=0){
							$(item).trigger("mark", "group");
						};
					}
					if($("#staff-lookup-input").val() != ""){
						$(item).trigger("mark", "staff");
					}
				};
			};
		};
	});
	$("body").on("click", "#menu-button",  function(){
		closeMenu($(this).parent().parent().next().find(".dropdown-content").get(0));
		$(this).parent().parent().next().find("#dropdown-content").get(0).classList.toggle("show");
	});
	window.onclick = function(event) {
	  if (!event.target.matches('#menu-button')) {
			closeMenu(document);
	  };
	};
};
function closeMenu(current){
	var dropdowns = document.getElementsByClassName("dropdown-content");
	var i;
	for (i = 0; i < dropdowns.length; i++) {
		var openDropdown = dropdowns[i];
		if (openDropdown.classList.contains('show')) {
			if(openDropdown != current){
				openDropdown.classList.remove('show');
			};
		};
	};
};